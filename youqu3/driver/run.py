#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

import os
# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
# pylint: disable=C0301,R0913,R0914,W0613,R0912,R0915,E0401,C0413,C0103,C0116
import re
import sys

import pytest

from youqu3 import logger
from youqu3 import setting

os.environ["DISPLAY"] = ":0"


class Run:
    """
    本地执行器
    """

    __author__ = "Mikigo <huangmingqiang@uniontech.com>"

    def __init__(
            self,
            keywords=None,
            tags=None,
            **kwargs,
    ):
        logger("INFO")

        self.keywords = keywords
        self.tags = tags

    @staticmethod
    def make_dir(dirs):
        try:
            dirs = os.path.expanduser(dirs)
            if not os.path.exists(dirs):
                os.makedirs(dirs)
        except FileExistsError:
            pass

    def generate_pytest_cmd(self):
        cmd = ["pytest"]

        if self.keywords:
            self.set_recursion_limit(self.keywords)
            cmd.extend(["-k", f"'{self.keywords}'"])
        if self.tags:
            self.set_recursion_limit(self.tags)
            cmd.extend(["-m", f"'{self.tags}'"])

        cmd.extend(
            [
                f"--max_fail={setting.MAX_FAIL}",
                f"--reruns={setting.RERUNS}",
                f"--record_failed_case={setting.RECORD_FAILED_CASE}",
                f"--log_level={setting.LOG_LEVEL}",
                f"--timeout={setting.TIMEOUT}",
            ]
        )
        return cmd

    @staticmethod
    def set_recursion_limit(strings):
        len_tags = len(re.split("or |and |not ", strings))
        if len_tags >= 999:
            sys.setrecursionlimit(len_tags + 100)

    def run(self):
        run_test_cmd_list = self.generate_pytest_cmd()

        pytest.main([i.strip("'") for i in run_test_cmd_list[1:]])


if __name__ == "__main__":
    Run().run()
