#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).absolute().parent))

from youqu3.rpc.client import client
from youqu3.rpc.guard import guard_rpc

dogtail_port = 4242


@guard_rpc(pathlib.Path(__file__).name.rstrip(".py"))
def rpc_dogtail(user=None, ip=None, password=None, auto_restart=False):
    return client(ip=ip, port=dogtail_port)


if __name__ == '__main__':
    from youqu3.dogtail import Dogtail
    from youqu3.rpc.server import server

    server(Dogtail(), dogtail_port)
