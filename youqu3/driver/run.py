#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import pathlib
import re
import sys

import pytest

from youqu3 import logger, setting


class Run:
    """
    本地执行器
    """

    __author__ = "mikigo <huangmingqiang@uniontech.com>"

    def __init__(
            self,
            keywords=None,
            tags=None,
            **kwargs,
    ):
        logger("INFO")

        self.keywords = keywords
        self.tags = tags
        self.cwd = pathlib.Path(".").absolute()
        self.report_path = self.cwd / "report"
        self.allure_path = self.report_path / "allure"
        self.allure_html_path = self.report_path / "allure_html"
        self.allure_json_path = self.report_path / "json"

    @staticmethod
    def makedirs(dirs):
        pathlib.Path(dirs).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def set_recursion_limit(strings):
        len_tags = len(re.split("or |and |not ", strings))
        if len_tags >= 999:
            sys.setrecursionlimit(len_tags + 100)

    def generate_pytest_cmd(self):
        cmd = ["pytest"]

        if self.keywords:
            self.set_recursion_limit(self.keywords)
            cmd.extend(["-k", f"'{self.keywords}'"])
        if self.tags:
            self.set_recursion_limit(self.tags)
            cmd.extend(["-m", f"'{self.tags}'"])

        cmd.extend([
            f"--max_fail={setting.MAX_FAIL}",
            f"--reruns={setting.RERUNS}",
            f"--timeout={setting.TIMEOUT}",
            f"--log_level={setting.LOG_LEVEL}",
            "--json-report",
            "--json-report-indent=2",
            f"--json-report-file={self.allure_json_path / f'report_{setting.TIME_STRING}.json'}",
            f"--alluredir={self.allure_path}",
        ])

        return cmd

    def run(self):
        run_test_cmd_list = self.generate_pytest_cmd()
        pytest.main([i.strip("'") for i in run_test_cmd_list[1:]])

        from allure_custom import AllureCustom
        AllureCustom.gen(str(self.allure_path), str(self.allure_html_path))


if __name__ == "__main__":
    Run().run()
