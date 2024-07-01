#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import os
import pathlib

from youqu3.gui import pylinuxauto
from youqu3.gui._rpc.client import client
from youqu3.gui._rpc.guard import guard_rpc

port = 4242


@guard_rpc(os.path.splitext(pathlib.Path(__file__).name)[0])
def _rpc_gui_client(
        user=None,
        ip=None,
        password=None,
        auto_restart=False,
        project_abspath=None
):
    return client(ip=ip, port=port)


class _RpcGuiServer:

    # attr
    def click_element_by_attr_path(self, attr_path):
        pylinuxauto.find_element_by_attr_path(attr_path).click()

    def double_click_element_by_attr_path(self, attr_path):
        pylinuxauto.find_element_by_attr_path(attr_path).double_click()

    def right_click_element_by_attr_path(self, attr_path):
        pylinuxauto.find_element_by_attr_path(attr_path).right_click()

    def element_center_by_attr_path(self, attr_path):
        return pylinuxauto.find_element_by_attr_path(attr_path).center()

    # image
    def click_element_by_image(self, image_path):
        pylinuxauto.find_element_by_image(image_path).click()

    def double_click_element_by_image(self, image_path):
        pylinuxauto.find_element_by_image(image_path).double_click()

    def right_click_element_by_image(self, image_path):
        pylinuxauto.find_element_by_image(image_path).right_click()

    def element_center_by_image(self, image_path):
        pylinuxauto.find_element_by_image(image_path).center()

    # ocr
    def click_element_by_ocr(self, target):
        pylinuxauto.find_element_by_ocr(target).click()

    def double_click_element_by_ocr(self, target):
        pylinuxauto.find_element_by_ocr(target).double_click()

    def right_click_element_by_ocr(self, target):
        pylinuxauto.find_element_by_ocr(target).right_click()

    def element_center_by_ocr(self, target):
        pylinuxauto.find_element_by_ocr(target).center()

    # ui
    def click_element_by_ui(self, appname, config_path, btn_name):
        pylinuxauto.find_element_by_ui(appname, config_path, btn_name).click()

    def double_click_element_by_ui(self, appname, config_path, btn_name):
        pylinuxauto.find_element_by_ui(appname, config_path, btn_name).double_click()

    def right_click_element_by_ui(self, appname, config_path, btn_name):
        pylinuxauto.find_element_by_ui(appname, config_path, btn_name).right_click()


class RpcGui:

    def __init__(
            self,
            user,
            ip,
            password,
            project_abspath,
            auto_restart=False,
    ):
        self.user = user
        self.ip = ip
        self.password = password
        self.project_abspath = project_abspath
        self.auto_restart = auto_restart

    def rpc_gui(self) -> _RpcGuiServer:
        return _rpc_gui_client(
            user=self.user,
            ip=self.ip,
            password=self.password,
            auto_restart=self.auto_restart,
            project_abspath=self.project_abspath
        )


if __name__ == '__main__':
    from youqu3.gui._rpc.server import server

    server(_RpcGuiServer, port)
