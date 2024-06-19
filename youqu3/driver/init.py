#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import os
import pathlib
import re
import shutil
from time import strftime

from youqu3 import setting



class Init:

    @staticmethod
    def copy_template_to_apps():
        # if os.listdir("."):
        #     if input("当前目录存在且里面存在文件，请确认是否清空（Y/N）：") in ("y", "Y"):
        #         os.system(f"rm -rf ./*")
        #     else:
        #         exit(0)
        os.system(f"cp -r {setting.TPL_PATH}/* .")
        os.system(f"cp {setting.TPL_PATH}/.gitignore-tpl  .")

    @classmethod
    def init(cls):
        cls.copy_template_to_apps()
        dirname = pathlib.Path(".").parent.name
        for root, dirs, files in os.walk("."):
            for file in files:
                app_name = dirname.lower()

                if file.endswith("-tpl"):

                    if "${app_name}" in file:
                        new_file = re.sub(
                            r"\${app_name}", app_name, file
                        )
                        shutil.move(f"{root}/{file}", f"{root}/{new_file}")
                        file = new_file

                    if ".py-tpl" in file or ".csv-tpl" in file:
                        with open(f"{root}/{file}", "r") as f:
                            codes = f.readlines()
                        new_codes = []
                        for code in codes:
                            if "${APP_NAME}" in code:
                                code = re.sub(r"\${APP_NAME}", app_name.upper(), code)
                            if "${app_name}" in code:
                                code = re.sub(r"\${app_name}", app_name, code)
                            if "${AppName}" in code:
                                code = re.sub(r"\${AppName}", app_name.title().replace("_", "").replace("-", ""), code)
                            if "${USER}" in code:
                                code = re.sub(r"\${USER}", setting.USERNAME, code)
                            if "${DATE}" in code:
                                code = re.sub(r"\${DATE}", strftime("%Y/%m/%d"), code)
                            if "${TIME}" in code:
                                code = re.sub(r"\${TIME}", strftime("%H:%M:%S"), code)
                            if "${FIXEDCSVTITLE}" in code:
                                code = re.sub(
                                    r"\${FIXEDCSVTITLE}",
                                    ",".join([i.value for i in setting.FixedCsvTitle]),
                                    code,
                                )
                            new_codes.append(code)
                        with open(f"{root}/{file}", "w") as f:
                            f.writelines([i for i in new_codes])

                    shutil.move(f"{root}/{file}", f"{root}/{file}".rstrip("-tpl"))

        tree = Tree(
            f":open_file_folder: [link file://{dirname}]{dirname}",
            guide_style="bold bright_blue",
        )
        walk_directory(pathlib.Path(dirname), tree)
        print(tree)
