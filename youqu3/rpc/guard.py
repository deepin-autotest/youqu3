#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import functools
import pathlib
import shutil

from youqu3 import logger
from youqu3 import setting
from youqu3.cmd import Cmd, RemoteCmd


def exclude():
    exclude_files = [
        "report",
        "__pycache__",
        ".pytest_cache",
        ".vscode",
        ".idea",
        ".git",
    ]

    exclude_str = ""
    for i in exclude_files:
        exclude_str += f"--exclude='{i}' "

    return exclude_str


def client_rootdir(user):
    client_rootdir_path = f"/home/{user}/_rpc_{pathlib.Path('.').absolute().name}"
    return client_rootdir_path


def transfer_to_client(ip, password, user):
    rsync = 'rsync -av -e "ssh -o StrictHostKeyChecking=no"'
    server_rootdir = pathlib.Path(".").absolute()
    Cmd.run(f"rm -rf ~/.ssh/known_hosts")
    remote_cmd = RemoteCmd(user, ip, password)
    remote_cmd.remote_run(f"mkdir -p {client_rootdir(user)}")
    Cmd.expect_run(
        f"/bin/bash -c '{rsync} {exclude()} {server_rootdir}/* {user}@{ip}:{client_rootdir(user)}/'",
        events={'password': f'{password}\n'},
        return_code=True
    )
    Cmd.expect_run(
        f"/bin/bash -c '{rsync} {exclude()} {server_rootdir}/.env {user}@{ip}:{client_rootdir(user)}/'",
        events={'password': f'{password}\n'},
        return_code=True
    )

    stdout, return_code = remote_cmd.remote_run(f"cd {client_rootdir(user)}/ && ls env_ok", return_code=True)
    if return_code != 0:
        _, return_code = remote_cmd.remote_run(
            "export PATH=$PATH:$HOME/.local/bin;"
            f"cd {client_rootdir(user)} && youqu3 envx && touch env_ok"
        )
        logger.info(f"RPC环境安装{'成功' if return_code == 0 else '失败'} - < {user}@{ip} >")


def start_client_service(ip, password, user, filename):
    service_name = f"{filename}.service"
    remote_cmd = RemoteCmd(user, ip, password)
    remote_cmd.remote_sudo_run(f"cp {service_name} /lib/systemd/system/")
    remote_cmd.remote_sudo_run(f"sudo chmod 644 /lib/systemd/system/{service_name}")
    remote_cmd.remote_sudo_run(f"sudo systemctl daemon-reload")
    remote_cmd.remote_sudo_run(f"sudo systemctl restart {service_name}")


def restart_client_service(ip, password, user, filename):
    RemoteCmd(user, ip, password).remote_sudo_run(f"sudo systemctl restart {filename}.service")


def gen_service_file(user, filename):
    service_file = pathlib.Path(".").absolute() / f"{filename}.service"
    service_py = pathlib.Path(".").absolute() / f"{filename}.py"
    if service_file.exists() and service_py.exists():
        return

    tpl_file = setting.RPC_PATH / "rpc_tpl.service"
    with open(tpl_file, "r", encoding="utf-8") as sf:
        service_tmp = sf.read()
    service_tmp.format(
        user=user,
        client_rootdir=client_rootdir(user),
        start_service=f"pipenv run python {filename}"
    )
    with open(service_file, "w", encoding="utf-8") as sf:
        sf.write(
            service_tmp.format(
                user=user,
                client_rootdir=client_rootdir(user),
                start_service=f"pipenv run python {filename}.py"
            )
        )
    shutil.copyfile(service_py, client_rootdir(user))


def guard_rpc(filename):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get("user") or args[0]
            ip = kwargs.get("ip") or args[1]
            if not user or not ip:
                raise ValueError("user and ip are required")
            password = kwargs.get("password")
            auto_restart = kwargs.get("auto_restart")

            _, return_code = RemoteCmd(user, ip, password).remote_sudo_run(f"sudo systemctl status {filename}.service")
            if return_code != 0:
                gen_service_file(user, filename)
                transfer_to_client(ip, password, user)
                start_client_service(ip, password, user, filename)
            if auto_restart:
                restart_client_service(ip, password, user, filename)
            res = func(*args, **kwargs)
            return res

        return wrapper

    return deco
