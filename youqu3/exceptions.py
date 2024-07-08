#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only

from youqu3 import logger


class ApplicationStartError(Exception):

    def __init__(self, result):
        """
        应用程序未启动
        :param result: 结果
        """
        err = f"应用程序未启动: {result}"
        logger.error(err)
        Exception.__init__(self, err)


class ElementNotFound(Exception):

    def __init__(self, name):
        """
        未找到元素
        :param name: 命令
        """
        err = f"未找到元素: {name}"
        logger.error(err)
        Exception.__init__(self, err)


class TemplateElementNotFound(Exception):

    def __init__(self, *name):
        """
        通过模板资源未匹配到对应元素
        :param name: 命令
        """
        err = "未在屏幕上匹配到图片: "
        template = [f"{i}.png" for i in name]
        logger.error(f"{err}{str(*template)}")
        Exception.__init__(self, err, *template)


class TemplateElementFound(Exception):

    def __init__(self, *name):
        """
        通过模板资源匹配到对应元素
        :param name: 命令
        """
        err = "在屏幕中匹配到了不应该出现的元素: "
        template = [f"{i}.png" for i in name]
        logger.error(f"{err}{str(*template)}")
        Exception.__init__(self, err, *template)


class TemplatePictureNotExist(Exception):

    def __init__(self, name):
        """
        文件不存在
        :param name: 命令
        """
        err = f"图片文件不存在: {name} "
        logger.error(err)
        Exception.__init__(self, err)


class ParamError(Exception):

    def __init__(self, name, msg):
        """
        参数错误
        :param name: 命令
        """
        err = f"参数错误：{name}、\n{msg}"
        logger.error(err)
        Exception.__init__(self, err)


class ShellExecutionFailed(Exception):

    def __init__(self, msg):
        err = f"Shell执行失败: {msg}"
        logger.error(err)
        Exception.__init__(self, err)


class YouQuPluginDependencyError(Exception):

    def __init__(self, msg):
        err = f"YouQu插件未安装 {msg}, 请尝试安装: pip install {msg}"
        logger.error(err)
        Exception.__init__(self, err)
