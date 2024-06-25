#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import os
import pathlib

from youqu3.dogtail import Dogtail
from youqu3.rpc.client import client
from youqu3.rpc.guard import guard_rpc

dogtail_port = 4242


@guard_rpc(os.path.splitext(pathlib.Path(__file__).name)[0])
def rpc_dogtail(
        user=None,
        ip=None,
        password=None,
        auto_restart=False,
        project_abspath=None
):
    return client(ip=ip, port=dogtail_port)


class RPCDogtail:
    def __init__(self, user, ip, password, project_abspath):
        self.user = user
        self.ip = ip
        self.password = password
        self.project_abspath = project_abspath

    @property
    def rdog(self) -> Dogtail:
        return rpc_dogtail(
            user=self.user,
            ip=self.ip,
            password=self.password,
            project_abspath=self.project_abspath,
        )

    def ele_click(self, ele_name):
        self.rdog.ele(ele_name).click()

    def ele_double_click(self, ele_name):
        self.rdog.ele(ele_name).doubleClick()

    def ele_right_click(self, ele_name):
        self.rdog.ele(ele_name).click(3)


if __name__ == '__main__':
    from youqu3.rpc.server import server

    server(Dogtail(), dogtail_port)
