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
    __author__ = "mikigo <huangmingqiang@uniontech.com>"

    def __init__(
            self,
            filepath=None,
            keywords=None,
            tags=None,
            setup_plan=None,
            **kwargs,
    ):
        logger("INFO")

        self.filepath = filepath
        self.keywords = keywords
        self.tags = tags
        self.setup_plan = setup_plan

        self.rootdir = pathlib.Path(".").absolute()
        self.report_path = self.rootdir / "report"
        self.html_report_path = self.report_path / "html"
        self.allure_data_path = self.html_report_path / "_data"
        self.allure_html_path = self.html_report_path / "html"
        self.json_report_path = self.report_path / "json"

        from funnylog.conf import setting as log_setting

        log_setting.LOG_FILE_PATH = self.report_path

    @staticmethod
    def makedirs(dirs):
        pathlib.Path(dirs).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def set_recursion_limit(strings):
        len_tags = len(re.split("or |and |not ", strings))
        if len_tags >= 999:
            sys.setrecursionlimit(len_tags + 100)

    def generate_cmd(self):
        cmd = ["pytest"]

        if self.filepath:
            cmd.append(self.filepath)
        if self.keywords:
            self.set_recursion_limit(self.keywords)
            cmd.extend(["-k", f"'{self.keywords}'"])
        if self.tags:
            self.set_recursion_limit(self.tags)
            cmd.extend(["-m", f"'{self.tags}'"])

        if self.setup_plan:
            cmd.append("--setup-plan")
        else:
            cmd.extend([
            "--json-report",
            "--json-report-indent=2",
            f"--json-report-file={self.json_report_path / f'report_{setting.TIME_STRING}.json'}",
            f"--alluredir={self.allure_data_path}",
            "--clean-alluredir",
            ])

        cmd.extend([
            f"--maxfail={setting.MAX_FAIL}",
            f"--reruns={setting.RERUNS}",
            f"--timeout={setting.TIMEOUT}",
        ])

        return cmd

    def run(self):
        pytest.main(
            [i.strip("'") for i in self.generate_cmd()[1:]]
        )
        if self.setup_plan:
            return
        from youqu_html import YouQuHtml
        YouQuHtml.gen(str(self.allure_data_path), str(self.allure_html_path), clean=True)


if __name__ == "__main__":
    Run().run()
