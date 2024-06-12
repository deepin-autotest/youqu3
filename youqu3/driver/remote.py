#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import json
import os
import pathlib
import re
import time
from concurrent.futures import ALL_COMPLETED
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
from itertools import cycle

from youqu3 import logger
from youqu3 import setting
from youqu3.cmd import Cmd
from youqu3 import sleep

from allure_custom import AllureCustom



class RemoteRunner:
    """
    远程执行器：控制多台测试机远程执行用例。
    """

    __author__ = "mikigo <huangmingqiang@uniontech.com>"

    def __init__(
            self,
            remote_kwargs: dict = None,
            local_kwargs: dict = None,
    ):
        logger("INFO")
        self.remote_kwargs = remote_kwargs
        self.local_kwargs = local_kwargs
        self.client_password = remote_kwargs.get("client_password") or setting.CLIENT_PASSWORD

        client_dict = {}
        _client = remote_kwargs.get("clients")
        if _client:
            clients = _client.split("/")
            for index, client in enumerate(clients):
                client_info = re.findall(r"^(.+?)@(\d+\.\d+\.\d+\.\d+):{0,1}(.*?)$", client)
                if client_info:
                    _c = list(client_info[0])
                    if _c[2] == "":
                        _c[2] = self.client_password
                    client_dict[f"client{index + 1}"] = _c

        else:
            raise ValueError("--clients user@ip")

        self.clients= client_dict
        self.send_code= remote_kwargs.get("send_code") or setting.SEND_CODE
        self.build_env= remote_kwargs.get("build_env") or setting.BUILD_ENV
        self.parallel= remote_kwargs.get("parallel") or setting.PARALLEL
        self.scan = int(setting.SCAN)

        self.server_project_path = "."
        self.dirname = pathlib.Path(".").parent.name

        self.client_report_path = lambda x: f"/home/{x}/{self.dirname}/report"
        self.client_allure_report_path = lambda x: f"{self.client_report_path(x)}/allure"
        self.client_json_report_path = lambda x: f"{self.client_report_path(x)}/json"
        self.client_xml_report_path = lambda x: f"{self.client_report_path(x)}/xml"

        self.strf_time = time.strftime("%m%d%p%I%M%S")
        self.client_list = list(self.clients.keys())
        _pty = "t"
        if len(self.client_list) >= 2:
            _pty = "T"
        self.ssh = f"sshpass -p '%s' ssh -{_pty}"
        self.scp = "sshpass -p '%s' scp -r"
        self.rsync = "sshpass -p '%s' rsync -av -e ssh"
        self.empty = "> /dev/null 2>&1"

        self.collection_json = False
        self.server_json_dir_id = None
        self.pms_user = None
        self.pms_password = None
        
    def pre_env(self):
        # rm hosts
        Cmd.run_cmd(f"rm -rf ~/.ssh/known_hosts {self.empty}")
        # rm client report
        if not self.send_code:
            for client in self.clients:
                user, _ip, password = self.clients.get(client)
                Cmd.run_cmd(
                    f"""{self.ssh % password} {user}@{_ip} "rm -rf {self.client_report_path(user)}/*" {self.empty}"""
                )
        # delete ssh ask
        sudo = f"echo '{setting.PASSWORD}' | sudo -S"
        if "StrictHostKeyChecking no" not in Cmd.run_cmd("cat /etc/ssh/ssh_config").stdout:
            Cmd.run_cmd(
                f"""{sudo} sed -i "s/#   StrictHostKeyChecking ask/ StrictHostKeyChecking no/g" /etc/ssh/ssh_config {self.empty}"""
            )
        # install sshpass
        if "(C)" not in Cmd.run_cmd("sshpass -V").stdout:
            Cmd.run_cmd(f"{sudo} apt update {self.empty}")
            Cmd.run_cmd(f"{sudo} apt install sshpass {self.empty}")

    def send_code_to_client(self, user, _ip, password):
        logger.info(f"发送代码到测试机 - < {user}@{_ip} >")
        Cmd.run_cmd(
            f"{self.ssh % password} {user}@{_ip} "
            f""""echo '{password}' | sudo -S rm -rf ~/{self.server_project_path}" {self.empty}"""
        )
        Cmd.run_cmd(
            f'{self.ssh % password} {user}@{_ip} "mkdir -p ~/{self.server_project_path}" {self.empty}'
        )
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
        Cmd.run_cmd(
            f"{self.rsync % (password,)} {exclude} ./* {user}@{_ip}:~/{self.dirname}/ {self.empty}"
        )
        Cmd.run_cmd(
            f"{self.rsync % (password,)} {exclude} ./.env {user}@{_ip}:~/{self.dirname}/ {self.empty}"
        )
        logger.info(f"代码发送成功 - < {user}@{_ip} >")

    def build_client_env(self, user, _ip, password):
        logger.info(f"安装环境 - < {user}@{_ip} >")
        # TODO
        Cmd.run_cmd(
            f"{self.ssh % password} {user}@{_ip} "
            f'"cd ~/{self.server_project_path}/ && bash env.sh"'
        )
        logger.info(f"环境安装完成 - < {user}@{_ip} >")

    def send_code_and_env(self, user, _ip, password):
        self.send_code_to_client(user, _ip, password)
        self.build_client_env(user, _ip, password)

    def mul_do(self, func_obj, client_list):
        """
         异步发送代码
        :param func_obj: 函数对象
        :param client_list: 测试机列表
        :return:
        """
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

    def get_client_test_status(self, user, _ip, password):
        status_test = Cmd.run_cmd(
            f'{self.ssh % password} {user}@{_ip} "ps -aux | grep pytest | grep -v grep"'
        ).stdout
        return bool(status_test)

    @staticmethod
    def makedirs(dirs):
        if not os.path.exists(dirs):
            os.makedirs(dirs)

    def run_pytest_cmd(self, user, _ip, password):
        cmd = [
            self.ssh % password,
            f"{user}@{_ip}",
            '"',
            "cd",
        ]

        l_args = list(self.local_kwargs.items())
        real_app_name = ""
        _tmp_args = []
        for i in l_args:
            if i[1] is None:
                continue
            i = list(i)
            i[0] = f"--{i[0]}"
            i[1] = f"'{i[1]}'"

            _tmp_args.extend(i)
        cmd.extend(
            [
                f"~/{self.server_project_path}/{real_app_name}",
                "&&",
                "pipenv",
                "run",
            ]
        )
        from youqu3.driver.run import Run

        lr = Run(debug=True)
        lr_args = {k: v for k, v in lr.export_default.items() if v}
        rr_args = {k: v for k, v in self.local_kwargs.items() if v}
        lr_args.update(rr_args)
        pytest_cmd = lr.generate_pytest_cmd()

        cmd.extend(pytest_cmd)
        cmd.append('"')
        cmd_str = " ".join(cmd)
        logger.info(f"\n{cmd_str}\n")
        Cmd.run_cmd(cmd_str)

    def scp_report(self, user, _ip, password):
        html_dir_endswith = f"_{self.dirname}"
        if not self.parallel:
            self.nginx_server_allure_path = f"./report/allure/{self.strf_time}{html_dir_endswith}"
            self.makedirs(self.nginx_server_allure_path)
            Cmd.run_cmd(
                f"{self.scp % password} {user}@{_ip}:{self.client_allure_report_path(user)}/* {self.nginx_server_allure_path}/ {self.empty}"
            )
        else:
            server_allure_path = f"./report/allure/{self.strf_time}_ip{_ip}{html_dir_endswith}"
            self.makedirs(server_allure_path)
            Cmd.run_cmd(
                f"{self.scp % password} {user}@{_ip}:{self.client_allure_report_path(user)}/* {server_allure_path}/ {self.empty}"
            )
            generate_allure_html = f"{server_allure_path}/html"

            AllureCustom.gen(server_allure_path, generate_allure_html)


    def get_report(self, client_list):
        # mul get report
        if len(self.clients) >= 2:
            _ps = []
            executor = ThreadPoolExecutor()
            for client in client_list[:-1]:
                user, _ip, password = self.clients.get(client)
                _p4 = executor.submit(self.scp_report, user, _ip, password)
                _ps.append(_p4)
                sleep(2)
            user, _ip, password = self.clients.get(client_list[-1])
            self.scp_report(user, _ip, password)
            wait(_ps, return_when=ALL_COMPLETED)
        else:
            user, _ip, password = self.clients.get(client_list[0])
            self.scp_report(user, _ip, password)

        # 分布式执行的情况下需要汇总结果
        if not self.parallel:
            summarize = {
                "total": 0,
                "pass": 0,
                "fail": 0,
                "skip": 0,
            }
            for file in os.listdir(self.server_detail_json_path):
                if file.startswith("summarize_") and file.endswith(".json"):
                    with open(f"{self.server_detail_json_path}/{file}", "r", encoding="utf-8") as f:
                        res = json.load(f)
                    for i in summarize.keys():
                        summarize[i] += res.get(i)
            with open(f"{self.server_detail_json_path}/summarize.json", "w", encoding="utf-8") as _f:
                _f.write(json.dumps(summarize, indent=2, ensure_ascii=False))

            generate_allure_html = f"{self.nginx_server_allure_path}/html"
            AllureCustom.gen(self.nginx_server_allure_path, generate_allure_html)

    def parallel_run(self, client_list):
        """
         并行跑
        :param client_list:
        :return:
        """
        _ps = []
        executor = ThreadPoolExecutor()
        for client in client_list[:-1]:
            user, _ip, password = self.clients.get(client)
            _p3 = executor.submit(self.run_pytest_cmd, user, _ip, password)
            _ps.append(_p3)
            time.sleep(1)
        user, _ip, password = self.clients.get(client_list[-1])
        self.run_pytest_cmd(
            user,
            _ip,
            password,
        )
        wait(_ps, return_when=ALL_COMPLETED)
        time.sleep(5)

    def nginx_run(self, client_list):
        """
         分布式执行
        :param client_list: 客户端列表
        :return:
        """
        # pylint: disable=too-many-nested-blocks
        case_files = self.pytest_co_cmd()
        logger.info(f"Collected {len(case_files)} case.")
        # sort case
        case_files.sort(key=lambda x: int(re.findall(r"(\d+)", x)[0]))
        _ps = []
        executor = ThreadPoolExecutor()
        for case in case_files:
            counter = {}
            try:
                # pylint: disable=unsubscriptable-object
                for client in cycle(client_list)[::-1]:
                    user, _ip, password = self.clients.get(client)
                    if not self.get_client_test_status(user, _ip, password):
                        _p2 = executor.submit(
                            self.run_pytest_cmd,
                            user,
                            _ip,
                            password,
                            f"{os.path.splitext(case)[0]} and ({self.keywords})",
                            self.tags,
                        )
                        _ps.append(_p2)
                        # relax and wait for pytest start
                        for _ in range(self.scan):
                            if self.get_client_test_status(user, _ip, password):
                                counter[client] = 0
                                break
                            # else:
                            sleep(1)
                        else:
                            client_list.remove(client)
                    else:
                        # relax
                        counter[client] = counter.get(client, 0) + 1
                        if counter.get(client) >= self.scan:
                            client_list.remove(client)
                        sleep(1)
            except ValueError:
                break
        # Wait for all child processes to end
        wait(_ps, return_when=ALL_COMPLETED)

    def remote_run(self):
        """
         远程执行主函数
        :return:
        """
        client_list = list(self.clients.keys())
        self.pre_env()
        logger.info(
            "\n测试机列表:\n"
            + "\n".join([str(i) for i in self.clients.items()])
        )
        if self.build_env:
            self.mul_do(self.send_code_and_env, client_list)
        else:
            if self.send_code:
                self.mul_do(self.send_code_to_client, client_list)
        if self.parallel:
            self.parallel_run(client_list)
        else:
            self.nginx_run(client_list)
        # collect and integrate result data after all tests.
        self.get_report(client_list)
