#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import pathlib
import re
from concurrent.futures import ALL_COMPLETED
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait

from youqu3 import logger
from youqu3 import setting
from youqu3 import sleep
from youqu3.cmd import Cmd, RemoteCmd


class Remote:
    __author__ = "mikigo <huangmingqiang@uniontech.com>"

    def __init__(
            self,
            clients=None,
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

        if not self.clients:
            raise ValueError("REMOTE驱动模式, 未传入远程客户端信息：-c/--clients user@ip:pwd")
        self.group_type = False
        if "{" in self.clients and "}" in self.clients:
            self.group_type = True

        if self.group_type is False:
            self.cli_clients = {}
            _cli_clients = self.clients.split("/")
            for index, _client in enumerate(_cli_clients):
                _cli_client_info = re.findall(r"^(.+?)@(\d+\.\d+\.\d+\.\d+):{0,1}(.*?)$", _client)
                if _cli_client_info:
                    _c = list(_cli_client_info[0])
                    if _c[2] == "":
                        _c[2] = setting.PASSWORD
                    self.cli_clients[f"client{index + 1}"] = _c
        else:
            self.cli_groups = {}
            groups = re.findall(r'\{(.*?)\}', self.clients)
            for group_index, group in enumerate(groups):
                cli_clients = {}
                for client_index, _client in enumerate(group.split("/")):
                    _cli_client_info = re.findall(r"^(.+?)@(\d+\.\d+\.\d+\.\d+):{0,1}(.*?)$", _client)
                    if _cli_client_info:
                        _c = list(_cli_client_info[0])
                        if _c[2] == "":
                            _c[2] = setting.PASSWORD
                        cli_clients[f"client{client_index + 1}"] = _c
                self.cli_groups[f"group{group_index + 1}"] = cli_clients

        self.server_rootdir = pathlib.Path(".").absolute()
        self.rootdir_name = self.server_rootdir.name
        self.client_rootdir = lambda x: f"/home/{x}/{self.rootdir_name}_{setting.TIME_STRING}"
        self.client_report_path = lambda x: f"{self.client_rootdir(x)}/report"
        self.client_html_report_path = lambda x: f"{self.client_report_path(x)}/html"
        self.client_json_report_path = lambda x: f"{self.client_report_path(x)}/json"

        self.rsync = "rsync -av -e ssh -o StrictHostKeyChecking=no"
        self.empty = "> /dev/null 2>&1"

        self.collection_json = False
        self.server_json_dir_id = None

        from funnylog.conf import setting as log_setting

        log_setting.LOG_FILE_PATH = self.server_rootdir

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
        _, return_code = Cmd.expect_run(
            f"{self.rsync} {exclude} {self.server_rootdir}/* {user}@{_ip}:{self.client_rootdir(user)}/",
            events={'(?i)password': f'{password}\\n'}
        )
        _, return_code = Cmd.expect_run(
            f"{self.rsync} {exclude} {self.server_rootdir}/.env {user}@{_ip}:{self.client_rootdir(user)}/",
            events={'(?i)password': f'{password}\\n'}
        )
        logger.info(f"代码发送{'成功' if return_code == 0 else '失败'} - < {user}@{_ip} >")

    def install_client_env(self, user, _ip, password):
        logger.info(f"开始安装环境 - < {user}@{_ip} >")

        def _remote_run(cmd):
            return RemoteCmd(user, _ip, password).remote_run(cmd, return_code=True)

        _, return_code = _remote_run("pip3 --version")
        if return_code != 0:
            _remote_run("curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py")
        _remote_run(f"pip3 install -U youqu3 -i {setting.PYPI_MIRROR}")
        _, return_code = _remote_run(
            f"export PATH=$PATH:$HOME/.local/bin;cd {self.client_rootdir(user)} && youqu3 envx")
        logger.info(f"环境安装{'成功' if return_code == 0 else '失败'} - < {user}@{_ip} >")

    def send_code_and_env(self, user, _ip, password):
        self.send_code(user, _ip, password)
        self.install_client_env(user, _ip, password)

    @staticmethod
    def makedirs(dirs):
        pathlib.Path(dirs).mkdir(parents=True, exist_ok=True)

    def get_back_all_report(self, client_list, clients):
        def get_back(user, _ip, password):
            server_html_path = f"{self.server_rootdir}/report/remote/{setting.TIME_STRING}_{_ip}_{self.rootdir_name}"
            self.makedirs(server_html_path)
            Cmd.run(
                f"{self.rsync % password} {user}@{_ip}:{self.client_report_path(user)}/* {server_html_path}/ {self.empty}")

        if len(clients) >= 2:
            _ps = []
            executor = ThreadPoolExecutor()
            for client in client_list[:-1]:
                user, _ip, password = clients.get(client)
                _p4 = executor.submit(get_back, user, _ip, password)
                _ps.append(_p4)
                sleep(2)
            user, _ip, password = clients.get(client_list[-1])
            get_back(user, _ip, password)
            wait(_ps, return_when=ALL_COMPLETED)
        else:
            user, _ip, password = clients.get(client_list[0])
            get_back(user, _ip, password)

    def changdir_remote_cmd(self, user):
        return ["cd", f"{self.client_rootdir(user)}/", "&&"]

    @property
    def generate_cmd(self):
        cmd = ["youqu3-cargo", "run"]

        if self.filepath:
            cmd.append(self.filepath)
        if self.keywords:
            cmd.extend(["-k", f"'{self.keywords}'"])
        if self.tags:
            cmd.extend(["-m", f"'{self.tags}'"])

        return cmd

    def run_test(self, user, _ip, password):
        RemoteCmd(user, _ip, password).remote_run(
            " ".join(
                self.changdir_remote_cmd(user) + self.generate_cmd
            )
        )

    @property
    def collection_only_cmd(self):
        return self.generate_cmd + ["--setup-plan"]

    @property
    def get_collection_only_cases(self):
        stdout = Cmd.run(f"cd {self.server_rootdir} && {' '.join(self.collection_only_cmd)}", timeout=600)
        lines = stdout.split("\n")
        _collection_cases = []
        for line in lines:
            line = line.strip()
            if line and " " not in line:
                _collection_cases.append(line.split("::")[0])
        collection_cases = set(_collection_cases)
        return collection_cases

    def parallel_run(self, clients):
        _ps = []
        executor = ThreadPoolExecutor()
        for client in list(clients.keys())[:-1]:
            user, _ip, password = clients.get(client)
            _p3 = executor.submit(self.run_test, user, _ip, password)
            _ps.append(_p3)
            sleep(1)
        user, _ip, password = list(clients.values())[-1]
        self.run_test(user, _ip, password)
        wait(_ps, return_when=ALL_COMPLETED)
        sleep(5)

    def mul_do(self, func_obj, client_list, clients):
        if len(client_list) >= 2:
            executor = ThreadPoolExecutor()
            _ps = []
            for client in client_list[:-1]:
                user, _ip, password = clients.get(client)
                _p1 = executor.submit(func_obj, user, _ip, password)
                _ps.append(_p1)
            user, _ip, password = clients.get(client_list[-1])
            func_obj(user, _ip, password)
            wait(_ps, return_when=ALL_COMPLETED)
        else:
            user, _ip, password = clients.get(client_list[0])
            func_obj(user, _ip, password)

    def run(self):
        Cmd.run(f"rm -rf ~/.ssh/known_hosts {self.empty}")

        if self.group_type:
            print("远程测试机列表".center(54))
            print("-" * 58)
            print(
                f"|{'GROUPS'.center(8)}|{'CLIENTS'.center(9)}|{'USER'.center(10)}|{'IP'.center(15)}|{'PASSWORD'.center(10)}|")
            print("-" * 58)
            for group, clients in self.cli_groups.items():
                for c, (user, _ip, password) in clients.items():
                    print(f"|{group.center(8)}|{c.center(9)}|{user.center(10)}|{_ip.center(15)}|{password.center(10)}|")
                print("-" * 58)

            for group, clients in self.cli_groups.items():
                client_list = list(clients.keys())
                if len(client_list) > 1:
                    # TODO
                    cases = self.get_collection_only_cases
                    def split_list(lst, n):
                        k, m = divmod(len(lst), n)
                        return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

                    client_case_list = split_list(list(cases), len(client_list))
                    client_case_map = dict(zip(client_list, client_case_list))
                    print(1)


                else:
                    self.mul_do(self.send_code_and_env, client_list, clients)
                    self.parallel_run(clients)
                    self.get_back_all_report(client_list, clients)


        else:
            print("远程测试机列表".center(47))
            print("-" * 49)
            print(f"|{'CLIENTS'.center(9)}|{'USER'.center(10)}|{'IP'.center(15)}|{'PASSWORD'.center(10)}|")
            print("-" * 49)
            for c, (user, _ip, password) in self.cli_clients.items():
                print(f"|{c.center(9)}|{user.center(10)}|{_ip.center(15)}|{password.center(10)}|")
            print("-" * 49)

            client_list = list(self.cli_clients.keys())
            self.mul_do(self.send_code_and_env, client_list, self.cli_clients)
            self.parallel_run(self.cli_clients)
            self.get_back_all_report(client_list, self.cli_clients)
