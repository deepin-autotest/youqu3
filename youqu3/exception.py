#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only

from funnylog import logger


class ApplicationStartError(Exception):

    def __init__(self, result):
        """
        应用程序未启动
        :param result: 结果
        """
        err = f"应用程序未启动,{result}"
        logger.error(err)
        Exception.__init__(self, err)


class ApplicationError(Exception):

    def __init__(self, msg):
        """
        应用程序错误
        :param msg: 结果
        """
        logger.error(msg)
        Exception.__init__(self, msg)


class ElementNotFound(Exception):

    def __init__(self, name):
        """
        未找到元素
        :param name: 命令
        """
        err = f"未找到“{name}”元素！"
        logger.error(err)
        Exception.__init__(self, err)


class TemplateElementNotFound(Exception):

    def __init__(self, *name):
        """
        通过模板资源未匹配到对应元素
        :param name: 命令
        """
        err = "通过图片资源, 未在屏幕上匹配到元素"
        template = [f"{i}.png" for i in name]
        Exception.__init__(self, err, *template)


class TemplateElementFound(Exception):

    def __init__(self, *name):
        """
        通过模板资源匹配到对应元素
        :param name: 命令
        """
        err = "通过图片资源, 在屏幕中匹配到了不应该出现的元素"
        template = [f"{i}.png" for i in name]
        Exception.__init__(self, err, *template)


class TemplatePictureNotExist(Exception):

    def __init__(self, name):
        """
        文件不存在
        :param name: 命令
        """
        err = f"图片资源：{name} 文件不存在!"
        logger.error(err)
        Exception.__init__(self, err)


class AssertOptionError(AssertionError):

    def __init__(self, e):
        """
        断言操作失败
        """
        err = f"断言操作失败，未知原因：{e}"
        logger.error(err)
        AssertionError.__init__(self, err)


class ParamError(Exception):

    def __init__(self, name, msg):
        """
        参数错误
        :param name: 命令
        """
        err = f"参数错误：{name}、\n{msg}"
        logger.error(err)
        Exception.__init__(self, err)


class NoIconOfThisSize(Exception):

    def __init__(self, size):
        """
        参数错误
        :param size:
        """
        err = f"参数错误：{size}"
        logger.error(err)
        Exception.__init__(self, err)


class NoSuchWindowPositionParameter(Exception):

    def __init__(self, size):
        """
        参数错误
        :param size:
        """
        err = f"参数错误：{size}, 没有此窗口位置参数"
        logger.error(err)
        Exception.__init__(self, err)


class GetWindowInformation(Exception):

    def __init__(self, msg):
        """
        获取窗口信息错误
        """
        logger.error(msg)
        Exception.__init__(self, msg)


class NoSetReferencePoint(Exception):

    def __init__(self, msg):
        err = f"没有设置参考点！| {msg}"
        logger.error(err)
        Exception.__init__(self, err)


class ShellExecutionFailed(Exception):

    def __init__(self, msg):
        err = f"shell执行失败！| {msg}"
        logger.error(err)
        Exception.__init__(self, err)


class ElementExpressionError(Exception):

    def __init__(self, msg):
        err = f"查找元素表达式错误 <{msg}>"
        logger.error(err)
        Exception.__init__(self, err)


class NoSuchSkipMethodFound(Exception):

    def __init__(self, msg):
        err = f"未找到判断是否跳过的自定义方法 <{msg}>"
        logger.error(err)
        Exception.__init__(self, err)


class OcrTextRecognitionError(Exception):

    def __init__(self, msg):
        err = f"Ocr文字识别失败 <{msg}>"
        logger.error(err)
        Exception.__init__(self, err)

class YouQuPluginDependencyError(Exception):

    def __init__(self, msg):
        err = f"YouQu插件未安装 <{msg}>, 请尝试安装：pip install {msg}"
        logger.error(err)
        Exception.__init__(self, err)
