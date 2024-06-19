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
from youqu3.cmd import Cmd, RemoteCmd


class Remote:
    __author__ = "mikigo <huangmingqiang@uniontech.com>"

    def __init__(
            self,
            clients=None,
            send=None,
            build_env=None,
            mode=None,
            filepath=None,
            keywords=None,
            tags=None,
            **kwargs
    ):
        logger("INFO")

        self.filepath = filepath
        self.keywords = keywords
        self.tags = tags
        self.clients = clients
        self.send = send or setting.SEND
        self.build_env = build_env or setting.BUILD_ENV
        self.mode = mode or setting.MODE

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
            raise ValueError("REMOTE驱动模式, 未传入远程客户端信息：-c/--clients user@ip:pwd")

        self.clients = cli_clients

        self.server_rootdir = pathlib.Path(".").absolute()
        self.rootdir_name = self.server_rootdir.name

        self.client_rootdir = lambda x: f"/home/{x}/{self.rootdir_name}_{setting.TIME_STRING}"
        self.client_report_path = lambda x: f"{self.client_rootdir(x)}/report"
        self.client_html_report_path = lambda x: f"{self.client_report_path(x)}/html"
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
        RemoteCmd(user, _ip, password).remote_sudo_run(f"rm -rf {self.client_rootdir(user)}")
        RemoteCmd(user, _ip, password).remote_run(f"mkdir -p {self.client_rootdir(user)}")
        exclude = ""
        for i in [
            "__pycache__",
            ".pytest_cache",
            ".vscode",
            ".idea",
            ".git",
            ".github",
            ".venv",
            "report",
            ".gitignore",
            "LICENSE",
            "Pipfile",
            "Pipfile.lock",
            "README.md",
        ]:
            exclude += f"--exclude='{i}' "
        stdout = Cmd.run(
            f"{self.rsync % (password,)} {exclude} {self.server_rootdir}/* {user}@{_ip}:{self.client_rootdir(user)}/ && echo 0 || echo 1",
        )
        stdout = Cmd.run(
            f"{self.rsync % (password,)} {exclude} {self.server_rootdir}/.env {user}@{_ip}:{self.client_rootdir(user)}/ && echo 0 || echo 1",
        )
        logger.info(f"代码发送{'成功' if stdout == 0 else '失败'} - < {user}@{_ip} >")

    def install_client_env(self, user, _ip, password):
        logger.info(f"开始安装环境 - < {user}@{_ip} >")

        def _env(cmd):
            return RemoteCmd(user, _ip, password).remote_run(cmd)

        _env(f"pip3 install -U youqu3 -i {setting.PYPI_MIRROR}")
        print(f"export PATH=$PATH:$HOME/.local/bin;cd {self.client_rootdir(user)} && youqu3 env && echo 0 || echo 1")
        result = _env(f"cd {self.client_rootdir(user)} && youqu3 env && echo 0 || echo 1")
        logger.info(f"环境安装{'成功' if result == 0 else '失败'} - < {user}@{_ip} >")

    def send_code_and_env(self, user, _ip, password):
        self.send_code(user, _ip, password)
        self.install_client_env(user, _ip, password)

    @staticmethod
    def makedirs(dirs):
        pathlib.Path(dirs).mkdir(parents=True, exist_ok=True)

    def get_back_all_report(self, client_list):
        def get_back(user, _ip, password):
            server_html_path = f"{self.server_rootdir}/report/remote/{self.strf_time}_{_ip}_{self.rootdir_name}"
            self.makedirs(server_html_path)
            Cmd.run(
                f"{self.rsync % password} {user}@{_ip}:{self.client_report_path(user)}/* {server_html_path}/ {self.empty}")

        if len(self.clients) >= 2:
            _ps = []
            executor = ThreadPoolExecutor()
            for client in client_list[:-1]:
                user, _ip, password = self.clients.get(client)
                _p4 = executor.submit(get_back, user, _ip, password)
                _ps.append(_p4)
                sleep(2)
            user, _ip, password = self.clients.get(client_list[-1])
            get_back(user, _ip, password)
            wait(_ps, return_when=ALL_COMPLETED)
        else:
            user, _ip, password = self.clients.get(client_list[0])
            get_back(user, _ip, password)

    def generate_remote_cmd(self, user):
        cmd = ["cd", f"{self.client_rootdir(user)}/", "&&", "pipenv", "run", "youqu3", "run"]

        if self.filepath:
            cmd.append(self.filepath)
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
            f"--alluredir={self.client_html_report_path(user)}",
            "--clean-alluredir",
        ])

        return cmd

    def run_test(self, user, _ip, password):
        RemoteCmd(user, _ip, password).remote_run(" ".join(self.generate_remote_cmd(user)))

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

        for c, (user, _ip, password) in self.clients.items():
            print("{0:<5}".format(c, user, _ip, password))

        if self.build_env:
            self.mul_do(self.send_code_and_env, client_list)
        else:
            if self.send:
                self.mul_do(self.send_code, client_list)

        if self.mode == "parallel":
            self.parallel_run()
        else:
            ...
        self.get_back_all_report(client_list)
