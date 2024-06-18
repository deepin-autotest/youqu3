#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import pathlib
import re
import time
from concurrent.futures import ALL_COMPLETED
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait

from allure_custom import AllureCustom

from youqu3 import logger
from youqu3 import setting
from youqu3 import sleep
from youqu3.cmd import Cmd


class Remote:
    __author__ = "mikigo <huangmingqiang@uniontech.com>"

    def __init__(
            self,
            keywords=None,
            tags=None,
            clients=None,
            send=None,
            build_env=None,
            mode=None,
            **kwargs
    ):
        logger("INFO")
        self.keywords = keywords
        self.tags = tags
        self.clients = clients
        self.send = send
        self.build_env = build_env
        self.mode = mode

        cli_clients = {}
        if self.clients:
            _cli_clients = self.clients.split("/")
            for index, _client in enumerate(_cli_clients):
                _cli_client_info = re.findall(r"^(.+?)@(\d+\.\d+\.\d+\.\d+):{0,1}(.*?)$", _client)
                if _cli_client_info:
                    _c = list(_cli_client_info[0])
                    if _c[2] == "":
                        _c[2] = setting.PASSWORD
                    cli_clients[f"client{index + 1}"] = _c

        else:
            raise ValueError("REMOTE驱动模式, 未传入远程客户端信息：--clients user@ip")

        self.clients = cli_clients
        self.send = self.send_code or setting.SEND
        self.build_env = self.build_env or setting.BUILD_ENV
        self.mode = self.mode or setting.MODE

        self.server_project_path = pathlib.Path(".").absolute()
        self.dirname = self.server_project_path.name

        self.client_project_path = lambda x: f"/home/{x}/{self.dirname}"
        self.client_report_path = lambda x: f"{self.client_project_path(x)}/report"
        self.client_allure_report_path = lambda x: f"{self.client_report_path(x)}/allure"
        self.client_json_report_path = lambda x: f"{self.client_report_path(x)}/json"

        self.strf_time = time.strftime("%m%d%p%I%M%S")
        self.rsync = "sshpass -p '%s' rsync -av -e ssh"
        self.empty = "> /dev/null 2>&1"

        self.collection_json = False
        self.server_json_dir_id = None
        self.pms_user = None
        self.pms_password = None

    def send_code(self, user, _ip, password):
        logger.info(f"开始发送代码到测试机 - < {user}@{_ip} >")
        Cmd.remote_sudo_run(user, _ip, password, f"rm -rf {self.client_project_path(user)}")
        Cmd.remote_run(user, _ip, password, f"mkdir -p {self.client_project_path(user)}")
        # 过滤目录
        exclude = ""
        for i in [
            "__pycache__",
            ".pytest_cache",
            ".vscode",
            ".idea",
            ".git",
            ".github",
            "report",
            ".gitignore",
        ]:
            exclude += f"--exclude='{i}' "
        _, return_code = Cmd.run(
            f"{self.rsync % (password,)} {exclude} {self.server_project_path}/* {user}@{_ip}:{self.client_project_path(user)}/ {self.empty}",
            return_code=True
        )
        _, return_code = Cmd.run(
            f"{self.rsync % (password,)} {exclude} {self.server_project_path}/.env {user}@{_ip}:~/{self.dirname}/ {self.empty}",
            return_code=True
        )
        logger.info(f"代码发送{'成功' if return_code == 0 else '失败'} - < {user}@{_ip} >")

    def build_client_env(self, user, _ip, password):
        logger.info(f"开始安装环境 - < {user}@{_ip} >")
        result = Cmd.remote_run(
            user, _ip, password,
            f"cd {self.client_project_path(user)}/ && youqu3-boom && echo 0 || echo 1"
        )
        logger.info(f"环境安装{'成功' if result == 0 else '失败'} - < {user}@{_ip} >")

    def send_code_and_env(self, user, _ip, password):
        self.send_code(user, _ip, password)
        self.build_client_env(user, _ip, password)

    @staticmethod
    def makedirs(dirs):
        pathlib.Path(dirs).mkdir(parents=True, exist_ok=True)

    def get_back_all_report(self, client_list):
        def get_back_report(user, _ip, password):
            html_dir_endswith = f"_{self.dirname}"
            server_allure_path = f"{self.server_project_path}/report/allure/{self.strf_time}_ip{_ip}{html_dir_endswith}"
            self.makedirs(server_allure_path)
            Cmd.run(
                f"{self.rsync % password} {user}@{_ip}:{self.client_allure_report_path(user)}/* {server_allure_path}/ {self.empty}")
            AllureCustom.gen(server_allure_path, f"{server_allure_path}/html")

        if len(self.clients) >= 2:
            _ps = []
            executor = ThreadPoolExecutor()
            for client in client_list[:-1]:
                user, _ip, password = self.clients.get(client)
                _p4 = executor.submit(get_back_report, user, _ip, password)
                _ps.append(_p4)
                sleep(2)
            user, _ip, password = self.clients.get(client_list[-1])
            get_back_report(user, _ip, password)
            wait(_ps, return_when=ALL_COMPLETED)
        else:
            user, _ip, password = self.clients.get(client_list[0])
            get_back_report(user, _ip, password)

    def generate_remote_cmd(self, user):
        cmd = ["cd", f"{self.client_project_path(user)}/", "&&", "youqu3", "run"]

        if self.keywords:
            cmd.extend(["-k", f"'{self.keywords}'"])
        if self.tags:
            cmd.extend(["-m", f"'{self.tags}'"])

        cmd.extend([
            f"--maxfail={setting.MAX_FAIL}",
            f"--reruns={setting.RERUNS}",
            f"--timeout={setting.TIMEOUT}",
            "--json-report",
            "--json-report-indent=2",
            f"--json-report-file={self.client_json_report_path(user)}/report_{setting.TIME_STRING}.json",
            f"--alluredir={self.client_allure_report_path(user)}",
        ])

        return cmd

    def run_test(self, user, _ip, password):
        Cmd.remote_run(user, _ip, password, " ".join(self.generate_remote_cmd(user)))

    def parallel_run(self):
        _ps = []
        executor = ThreadPoolExecutor()
        for client in list(self.clients.keys())[:-1]:
            user, _ip, password = self.clients.get(client)
            _p3 = executor.submit(self.run_test, user, _ip, password)
            _ps.append(_p3)
            sleep(1)
        user, _ip, password = list(self.clients.values())[-1]
        self.run_test(user, _ip, password)
        wait(_ps, return_when=ALL_COMPLETED)
        sleep(5)

    def mul_do(self, func_obj, client_list):
        if len(client_list) >= 2:
            executor = ThreadPoolExecutor()
            _ps = []
            for client in client_list[:-1]:
                user, _ip, password = self.clients.get(client)
                _p1 = executor.submit(func_obj, user, _ip, password)
                _ps.append(_p1)
            user, _ip, password = self.clients.get(client_list[-1])
            func_obj(user, _ip, password)
            wait(_ps, return_when=ALL_COMPLETED)
        else:
            user, _ip, password = self.clients.get(client_list[0])
            func_obj(user, _ip, password)

    def run(self):
        client_list = list(self.clients.keys())
        from rich.console import Console
        from rich.table import Table

        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("CLIENT", justify="center")
        table.add_column("USER", justify="center")
        table.add_column("IP", justify="center")
        table.add_column("PASSWORD", justify="center")
        for c, (user, _ip, password) in self.clients.items():
            table.add_row(c, user, _ip, password)
        console.print(table)
        if self.build_env:
            self.mul_do(self.send_code_and_env, client_list)
        else:
            if self.send_code:
                self.mul_do(self.send_code, client_list)

        if self.mode == "parallel":
            self.parallel_run()
        else:
            ...
        self.get_back_all_report(client_list)
