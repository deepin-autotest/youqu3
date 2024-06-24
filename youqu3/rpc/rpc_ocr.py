#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).absolute().parent))

from youqu3.rpc.client import client
from youqu3.rpc.guard import guard_rpc

ocr_port = 4244


@guard_rpc(pathlib.Path(__file__).name.rstrip(".py"))
def rpc_ocr(user=None, ip=None, password=None, auto_restart=False):
    return client(ip=ip, port=ocr_port)


if __name__ == '__main__':
    from youqu3.ocr import OCR
    from youqu3.rpc.server import server

    server(OCR(), ocr_port)
