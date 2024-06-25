#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import os
import pathlib

from youqu3.mousekey import MouseKey
from youqu3.rpc.client import client
from youqu3.rpc.guard import guard_rpc

mousekey_port = 4245


@guard_rpc(os.path.splitext(pathlib.Path(__file__).name)[0])
def rpc_mousekey(
        user=None,
        ip=None,
        password=None,
        auto_restart=False,
        project_abspath=None
):
    return client(ip=ip, port=mousekey_port)


class RpcMouseKey:

    def __init__(self, user, ip, password, project_abspath):
        self.user = user
        self.ip = ip
        self.password = password
        self.project_abspath = project_abspath

    @property
    def rmk(self) -> MouseKey:
        return rpc_mousekey(
            user=self.user,
            ip=self.ip,
            password=self.password,
            project_abspath=self.project_abspath,
        )

    def click(self, x=None, y=None):
        self.rmk.click(x, y)

    def double_click(self, x=None, y=None):
        self.rmk.double_click(x, y)

    def right_click(self, x=None, y=None):
        self.rmk.right_click(x, y)


if __name__ == '__main__':
    from youqu3.rpc.server import server

    server(MouseKey(), mousekey_port)
