#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only

import os
from time import sleep

from funnylog import logger

os.environ["DISPLAY"] = ":0"

import pyautogui
import easyprocess

pyautogui.FAILSAFE = False


# pyautogui.PAUSE = 1

class MouseKey:
    """
    鼠标和键盘的常用操作
    """

    __author__ = "mikigo<huangmingqiang@uniontech.com>"

    MOUSE = {1: pyautogui.PRIMARY, 2: pyautogui.MIDDLE, 3: pyautogui.RIGHT}

    @classmethod
    def screen_size(cls):
        """
         获取屏幕大小
        :return: width, height
        """
        width, height = pyautogui.size()
        logger.debug(f"获取屏幕分辨率 {width}*{height}")
        return width, height

    @classmethod
    def current_location(cls, out_log=True):
        """
         获取当前鼠标位置
        :return: 鼠标当前的坐标
        """
        position = pyautogui.position()
        if out_log:
            logger.debug(f"当前鼠标坐标 {position}")
        return position

    @classmethod
    def move_to(cls, _x, _y, duration=0.4):
        """
         移动到指定位置
        :param _x: x
        :param _y: y
        :param duration:移动的速度
        :return:
        """
        logger.debug(f"鼠标移动至 ({_x, _y}, 速度：{duration})")
        pyautogui.moveTo(int(_x), int(_y), duration=duration)

    @classmethod
    def move_rel(cls, _x, _y, duration=0.4):
        """
         相对移动到位置
        :param _x:
        :param _y:
        :param duration:
        :return:
        """
        logger.debug(f"鼠标移动相对坐标位置 ({_x, _y}), 速度：{duration}")
        pyautogui.moveRel(xOffset=int(_x), yOffset=int(_y), duration=duration)

    @classmethod
    def click(cls, _x=None, _y=None):
        """
         点击鼠标左键
        :param _x:
        :param _y:
        :param _type: 使用 PyAutoGUI or Xdotool 点击
        :return:
        """
        logger.debug(f"点击坐标 {(_x, _y) if _x else cls.current_location(out_log=False)}")
        pyautogui.click(x=_x, y=_y)

    @classmethod
    def move_rel_and_click(cls, _x, _y):
        """
         move relative and click
        :param _x:
        :param _y:
        :return:
        """
        cls.move_rel(_x, _y)
        cls.click()

    @classmethod
    def middle_click(cls):
        """
        单击鼠标滚轮中间
        """
        logger.debug("单击鼠标滚轮中间")
        pyautogui.middleClick()

    @classmethod
    def right_click(cls, _x=None, _y=None):
        """
         单击鼠标右键
        :param _x:
        :param _y:
        :return:
        """
        logger.debug(f"鼠标右键坐标 {(_x, _y) if _x else cls.current_location(out_log=False)}")
        pyautogui.rightClick(x=_x, y=_y)
        sleep(1)

    @classmethod
    def double_click(cls, _x=None, _y=None, interval=0.3):
        """
         双击鼠标左键
        :param _x:
        :param _y:
        :param interval: 两次点击的间隔，默认 0.3s
        :return:
        """
        logger.debug(f"鼠标左键双击坐标 {(_x, _y) if _x else cls.current_location(out_log=False)}")
        pyautogui.doubleClick(x=_x, y=_y, interval=interval)
        # CmdCtl.run_cmd(f"xdotool mousemove {_x} {_y} click --repeat 2 1")
        sleep(1)

    @classmethod
    def triple_click(cls, _x=None, _y=None):
        """
         三击鼠标左键
        :param _x:
        :param _y:
        :return:
        """
        logger.debug(f"鼠标三连击坐标 {(_x, _y) if _x else cls.current_location(out_log=False)}")
        pyautogui.tripleClick(x=_x, y=_y, interval=0.3)
        sleep(1)

    @classmethod
    def drag_to(cls, _x, _y, duration=0.4, delay=1):
        """
         拖拽到指定位置(绝对位置)
        :param _x: 拖拽到的位置x
        :param _y: 拖拽到的位置y
        :param duration: 拖拽的时长
        :param delay: 拖拽后等待的时间
        :return:
        """
        logger.debug(f"鼠标从当前位置拖拽到坐标 ({_x, _y})")
        pyautogui.dragTo(x=int(_x), y=int(_y), duration=duration, mouseDownUp=True)
        sleep(delay)

    @classmethod
    def drag_rel(cls, _x, _y):
        """
         按住鼠标左键,拖拽到指定位置(相对位置)
        :param _x: 拖拽的相对位置x，正数向右，负数向左
        :param _y: 拖拽的相对位置y，正数向下，负数向上
        :return:
        """
        logger.debug(f"鼠标从当前位置拖拽到相对坐标 ({_x, _y})")
        pyautogui.dragRel(xOffset=int(_x), yOffset=int(_y), duration=0.4, mouseDownUp=True)
        sleep(1)

    @classmethod
    def mouse_down(cls, _x=None, _y=None, button=1):
        """
         按住鼠标键不放
        :param _x:
        :param _y:
        :param button: 1 左键， 2 中键， 3 右键
        :return:
        """
        logger.debug(
            f"在坐标 {(_x, _y) if _x else cls.current_location(out_log=False)} "
            f"处按住鼠标{['左', '中', '右'][button - 1]}键不放"
        )
        pyautogui.mouseDown(x=_x, y=_y, button=cls.MOUSE.get(button, pyautogui.PRIMARY))
        sleep(1)

    @classmethod
    def mouse_up(cls, button=1):
        """
         松开鼠标左键
        :param button: 1 左键， 2 中键， 3 右键
        :return:
        """
        logger.debug(f"松开鼠标{['左', '中', '右'][button - 1]}键")
        pyautogui.mouseUp(button=cls.MOUSE.get(button, pyautogui.PRIMARY))
        sleep(1)

    @classmethod
    def mouse_scroll(cls, amount_of_scroll, duration=1):
        """
         滚动鼠标滚轮,the_amount_of_scroll为传入滚轮数,正数为向上,负数为向下
        :param amount_of_scroll: 滚轮数
        :param duration:
        :return:
        """
        pyautogui.scroll(amount_of_scroll)
        if amount_of_scroll > 0:
            direct = "上"
        else:
            direct = "下"
        logger.debug(f"向<{direct}>滑动滚轮")
        sleep(duration)

    @classmethod
    def input_message(
            cls,
            message,
            delay_time: int = 300,
            interval: [int, float] = 0.2,
            wayland_shift: bool = False,
            _ydotool: bool = False,
    ):
        """
         输入字符串
        :param message: 输入的内容
        :param delay_time: 延迟时间
        :param interval:
        :return:
        """
        logger.debug(f"输入字符串<{message}>")
        message = str(message)

        def check_chinese():
            for _ch in message:
                if "\u4e00" <= _ch <= "\u9fff":
                    return True
            return False

        if check_chinese():
            easyprocess.EasyProcess(f"xdotool type --delay {delay_time} '{message}'".split(" ")).call()
        else:
            pyautogui.typewrite(message=str(message), interval=interval)

    @classmethod
    def press_key(cls, key: str, interval=0.0):
        """
         键盘上指定的按键
        :param key: 键盘按键
        :param interval:
        :return:
        """
        logger.debug(f"点击键盘上指定的按键<{key}>, 间隔<{interval}>")
        pyautogui.press(key, interval=interval)

    @classmethod
    def press_key_down(cls, key: str):
        """
         按住键盘按键不放
        :param key: 键盘按键
        :return:
        """
        logger.debug(f"按下<{key}>按键")
        pyautogui.keyDown(key)

    @classmethod
    def press_key_up(cls, key: str):
        """
         放松按键
        :param key: 键盘按键
        :return:
        """
        logger.debug(f"放松<{key}>按键")
        pyautogui.keyUp(key)

    @classmethod
    def hot_key(cls, *args, interval=0.03):
        """
         键盘组合按键操作
        :param args: 键盘组合键，比如："ctrl","alt","a"
        :return:
        """
        logger.debug(f"快捷键 {args}")
        pyautogui.hotkey(*args, interval=interval)

    @classmethod
    def hot_key_down(cls, *args):
        """
         组合按键按下不放
        :param args:
        :return:
        """
        for _c in args:
            if len(_c) > 1:
                _c = _c.lower()
            cls.press_key_down(_c)
            sleep(0.03)

    @classmethod
    def hot_key_up(cls, *args):
        """
         组合按键释放
        :param args:
        :return:
        """
        for c in reversed(args):
            if len(c) > 1:
                c = c.lower()
            cls.press_key_up(c)
            sleep(0.03)

    @classmethod
    def move_to_and_click(cls, _x, _y):
        """
         移动到某个位置点击
        :param _x: 移动到的位置 x
        :param _y: 移动到的位置 y
        :return:
        """
        cls.move_to(_x, _y)
        cls.click()

    @classmethod
    def move_to_and_right_click(cls, _x, _y):
        """
         移动到某个位置点击右键
        :param _x: 移动到的位置 x
        :param _y: 移动到的位置 y
        :return:
        """
        cls.move_to(_x, _y)
        cls.right_click()

    @classmethod
    def move_to_and_double_click(cls, _x, _y):
        """
         移动到某个位置点击双击
        :param _x: 移动到的位置 x
        :param _y: 移动到的位置 y
        :return:
        """
        cls.move_to(_x, _y)
        cls.double_click()

    @classmethod
    def move_on_and_drag_to(cls, start: tuple, end: tuple):
        """
         指定拖动的起始-终止坐标
        :param start: 开始坐标
        :param end: 终止坐标
        :return:
        """
        cls.move_to(*start)
        sleep(1)
        cls.drag_to(*end)

    @classmethod
    def move_on_and_drag_rel(cls, start: tuple, end: tuple):
        """
         指定拖动的起始-终止坐标
        :param start: 开始坐标
        :param end: 终止坐标
        :return:
        """
        cls.move_to(*start)
        sleep(1)
        cls.drag_rel(*end)

    @classmethod
    def select_menu(cls, number: int):
        """
         选择桌面右键菜单中的选项(从上到下)
        :param number: 在菜单中的位置数
        :return:
        """
        for _ in range(number):
            cls.press_key("down")
        sleep(0.3)
        cls.press_key("enter")
        logger.debug(f"选择右键菜单中的选项(从上到下)第{number}项")

    @classmethod
    def reverse_select_menu(cls, number: int):
        """
         选择桌面右键菜单中的选项（从下到上）
        :param number: 在菜单中的位置数
        :return:
        """
        for _ in range(number):
            cls.press_key("up")
        sleep(0.3)
        cls.press_key("enter")
        logger.debug(f"选择右键菜单中的选项(从下到上)第{number}项")

    @classmethod
    def select_submenu(cls, number: int):
        """
         选择右键菜单中的子菜单选项（从上到下）
        :param number: 在菜单中的位置数
        :return:
        """
        for _ in range(1, number):
            cls.press_key("down")
        cls.press_key("enter")

    @classmethod
    def locate_all_on_screen(cls, image_path):
        """
         识别所有匹配的图像
        :param image_path: 图像的路径
        :return: 所有匹配的位置的元组组成的列表
        """
        return pyautogui.locateAllOnScreen(image_path)

    @classmethod
    def draw_line(cls, start_x, start_y, rel_x, rel_y):
        """
         从某个坐标开始画线（框选）
        :param start_x: 开始的坐标的横坐标
        :param start_y: 开始的坐标的纵坐标
        :param rel_x: 向量的横坐标
        :param rel_y: 向量的纵坐标
        :return:
        """
        cls.move_to(start_x, start_y)
        cls.drag_rel(rel_x, rel_y)

    @classmethod
    def clear(cls):
        """
         清空表单
        :return:
        """
        logger.debug("清空表单")
        cls.hot_key("ctrl", "a")
        cls.press_key("backspace")

    @classmethod
    def ctrl_f9(cls):
        """
         ctrl_f9 快捷键设置壁纸
        :return:
        """
        cls.hot_key("ctrl", "f9")

    @classmethod
    def super_up(cls):
        """
         super_up 最大化窗口
        :return:
        """
        cls.hot_key("win", "up")

    @classmethod
    def win_left(cls):
        """
        win_left  向左切换工作区
        :return:
        """
        cls.hot_key("win", "left")

    @classmethod
    def win_right(cls):
        """
         win_right 向右切换工作区
        :return:
        """
        cls.hot_key("win", "Right")

    @classmethod
    def ctrl_shift_shortcut_down(cls):
        """
         ctrl shift ? 唤起快捷键面板
        :return:
        """
        cls.hot_key_down("ctrl", "shift", "/")

    @classmethod
    def ctrl_shift_shortcut_up(cls):
        """
         ctrl shift ? 收起快捷键面板
        :return:
        """
        cls.hot_key_up("ctrl", "shift", "/")

    @classmethod
    def shift(cls):
        """
         shift
        :return:
        """
        cls.hot_key("shift")

    @classmethod
    def shift_right(cls):
        """
         'shift' + 'right'
        :return:
        """
        cls.hot_key("shift", "right")

    @classmethod
    def shift_down(cls):
        """
         shift_down
        :return:
        """
        cls.hot_key("shift", "down")

    @classmethod
    def shift_up(cls):
        """
         shift_up
        :return:
        """
        cls.hot_key("shift", "up")

    @classmethod
    def tab(cls):
        """
         tab
        :return:
        """
        cls.press_key("tab")

    @classmethod
    def esc(cls):
        """
         esc
        :return:
        """
        cls.press_key("esc")

    @classmethod
    def right(cls):
        """
         right 键盘方向键-右键
        :return:
        """
        cls.press_key("right")

    @classmethod
    def left(cls):
        """
         left 键盘方向键-左键
        :return:
        """
        cls.press_key("left")

    @classmethod
    def dot(cls):
        """
         dot 键盘点号
        :return:
        """
        cls.press_key(".")

    @classmethod
    def press_left_sometime(cls, sometime: int):
        """
         按住键盘方向键-左键一段时间
        :param sometime: 一段时间
        :return:
        """
        cls.press_key_down("left")
        sleep(sometime)
        cls.press_key_up("left")

    @classmethod
    def up(cls):
        """
         up 键盘方向键-上键
        :return:
        """
        cls.press_key("up")

    @classmethod
    def press_up_sometime(cls, sometime: int):
        """
         按住键盘方向键-上键一段时间
        :param sometime: 一段时间
        :return:
        """
        cls.press_key_down("up")
        sleep(sometime)
        cls.press_key_up("up")

    @classmethod
    def down(cls):
        """
         down 键盘方向键-下键
        :return:
        """
        cls.press_key("down")

    @classmethod
    def enter(cls):
        """
         enter 回车
        :return:
        """
        cls.press_key("enter")

    @classmethod
    def ctrl_a(cls):
        """
         ctrl_a
        :return:
        """
        cls.hot_key("ctrl", "a")

    @classmethod
    def ctrl_l(cls):
        """
         ctrl_l
        :return:
        """
        cls.hot_key("ctrl", "l")

    @classmethod
    def ctrl_g(cls):
        """
         ctrl_g
        :return:
        """
        cls.hot_key("ctrl", "g")

    @classmethod
    def ctrl_n(cls):
        """
         ctrl_n
        :return:
        """
        cls.hot_key("ctrl", "n")

    @classmethod
    def ctrl_alt_t(cls):
        """
         ctrl_alt_t
        :return:
        """
        cls.hot_key("ctrl", "alt", "t")

    @classmethod
    def ctrl_alt_down(cls):
        """
         ctrl_alt_down
        :return:
        """
        cls.hot_key("ctrl", "alt", "down")

    @classmethod
    def ctrl_alt_up(cls):
        """
         ctrl_alt_up
        :return:
        """
        cls.hot_key("ctrl", "alt", "up")

    @classmethod
    def ctrl_alt_a(cls):
        """
         ctrl_alt_a
        :return:
        """
        cls.hot_key("ctrl", "alt", "a")

    @classmethod
    def ctrl_x(cls):
        """
         ctrl_x
        :return:
        """
        cls.hot_key("ctrl", "x")

    @classmethod
    def ctrl_s(cls):
        """
         ctrl_a
        :return:
        """
        cls.hot_key("ctrl", "s")

    @classmethod
    def alt_tab(cls):
        """
         快捷键alt+table
        :return:
        """
        cls.hot_key("alt", "tab")

    @classmethod
    def alt_m(cls):
        """
         ctrl_m
        :return:
        """
        cls.hot_key("alt", "m")

    @classmethod
    def ctrl_f(cls):
        """
         ctrl_f
        :return:
        """
        cls.hot_key("ctrl", "f")

    @classmethod
    def ctrl_v(cls):
        """
         ctrl_v
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "v")

    @classmethod
    def ctrl_c(cls):
        """
         ctrl_c
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "c")

    @classmethod
    def alt_f4(cls):
        """
         alt_f4
        :return:
        """
        sleep(1)
        cls.hot_key("alt", "f4")

    @classmethod
    def alt_f2(cls):
        """
         alt_f2
        :return:
        """
        sleep(1)
        cls.hot_key("alt", "f2")

    @classmethod
    def f2(cls):
        """
         f2
        :return:
        """
        sleep(1)
        cls.press_key("f2")

    @classmethod
    def f1(cls):
        """
         f1
        :return:
        """
        sleep(1)
        cls.press_key("f1")

    @classmethod
    def f3(cls):
        """
         f3
        :return:
        """
        sleep(1)
        cls.press_key("f3")

    @classmethod
    def f5(cls):
        """
         f5
        :return:
        """
        sleep(1)
        cls.press_key("f5")

    @classmethod
    def space(cls):
        """
         space
        :return:
        """
        sleep(1)
        cls.press_key("space")

    @classmethod
    def backspace(cls):
        """
         backspace
        :return:
        """
        sleep(1)
        cls.press_key("backspace")

    @classmethod
    def winleft_d(cls):
        """
         winleft_d
        :return:
        """
        sleep(1)
        cls.hot_key("winleft", "d")

    @classmethod
    def winleft_q(cls):
        """
         winleft_q
        :return:
        """
        sleep(1)
        cls.hot_key("winleft", "q")

    @classmethod
    def ctrl_z(cls):
        """
         ctrl_z
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "z")
        sleep(0.5)

    @classmethod
    def ctrl_y(cls):
        """
         ctrl_y
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "y")
        sleep(0.5)

    @classmethod
    def winleft_e(cls):
        """
         winleft_e
        :return:
        """
        sleep(1)
        cls.hot_key("winleft", "e")

    @classmethod
    def delete(cls):
        """
         delete
        :return:
        """
        cls.press_key("delete")

    @classmethod
    def shift_delete(cls):
        """
         shift_delete
        :return:
        """
        cls.hot_key("shift", "delete")

    @classmethod
    def shift_left(cls):
        """
         shift+左方向键
        :return:
        """
        cls.hot_key("shift", "left")

    @classmethod
    def ctrl_i(cls):
        """
         ctrl i
        :return:
        """
        cls.hot_key("ctrl", "i")

    @classmethod
    def ctrl_h(cls):
        """
         ctrl h
        :return:
        """
        cls.hot_key("ctrl", "h")

    @classmethod
    def ctrl_o(cls):
        """
         ctrl_o
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "o")

    @classmethod
    def ctrl_shift_up(cls):
        """
         ctrl_shift_up
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "shift", "up")

    @classmethod
    def ctrl_shift_n(cls):
        """
         ctrl_shift_n
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "shift", "n")

    @classmethod
    def ctrl_shift_down(cls):
        """
         ctrl_shift_down
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "shift", "down")

    @classmethod
    def ctrl_shift_left(cls):
        """
         ctrl_shift_left
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "shift", "left")

    @classmethod
    def ctrl_shift_right(cls):
        """
         ctrl_shift_right
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "shift", "right")

    @classmethod
    def ctrl_up(cls):
        """
         ctrl_up
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "up")

    @classmethod
    def ctrl_down(cls):
        """
         ctrl_down
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "down")

    @classmethod
    def ctrl_left(cls):
        """
         ctrl_left
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "left")

    @classmethod
    def ctrl_right(cls):
        """
         ctrl_right
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "right")

    @classmethod
    def shift_space(cls):
        """
         shift+space
        :return:
        """
        sleep(1)
        cls.hot_key("shift", "space")

    @classmethod
    def ctrl_rod(cls):
        """
         ctrl+-
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "-")

    @classmethod
    def ctrl_add(cls):
        """
         ctrl++
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "+")

    @classmethod
    def ctrl_r(cls):
        """
         ctrl+r
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "r")

    @classmethod
    def ctrl_shift_r(cls):
        """
         ctrl+shift+r
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "shift", "r")

    @classmethod
    def ctrl_shift_z(cls):
        """
         ctrl+shift+z
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "shift", "z")

    @classmethod
    def ctrl_scroll(cls, direction, amount_of_scroll=1):
        """
         ctrl+滚轮
        :param direction:
        :param amount_of_scroll:
        :return:
        """
        cls.press_key_down("ctrl")
        for _ in range(amount_of_scroll):
            cls.mouse_scroll(direction, duration=0)
        cls.press_key_up("ctrl")

    @classmethod
    def shift_scroll(cls, direction, amount_of_scroll=1):
        """
         shift+滚轮
        :param direction:
        :param amount_of_scroll:
        :return:
        """
        cls.press_key_down("shift")
        for _ in range(amount_of_scroll):
            cls.mouse_scroll(direction, duration=0)
        cls.press_key_up("shift")

    @classmethod
    def alt_d(cls):
        """
         alt+d
        :return:
        """
        sleep(1)
        cls.hot_key("alt", "d")

    @classmethod
    def ctrl_e(cls):
        """
         ctrl+e
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "e")

    @classmethod
    def ctrl_shift_s(cls):
        """
         ctrl+shift+s
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "shift", "s")

    @classmethod
    def ctrl_shift(cls):
        """
         ctrl+shift
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "shift")

    @classmethod
    def ctrl_space(cls):
        """
         ctrl+space
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "space")

    @classmethod
    def ctrl_shift_e(cls):
        """
         ctrl+shift+e
        :return:
        """
        cls.hot_key("ctrl", "shift", "e")

    @classmethod
    def ctrl_shift_w(cls):
        """
         ctrl+shift+w
        :return:
        """
        cls.hot_key("ctrl", "shift", "w")

    @classmethod
    def ctrl_alt_v(cls):
        """
         快捷键打开剪切板
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "alt", "v")

    @classmethod
    def ctrl_printscreen(cls):
        """
         快捷键启动延时截图
        :return:
        """
        sleep(1)
        cls.hot_key("ctrl", "printscreen")

    @classmethod
    def alt_enter(cls):
        """
         快捷键影院进入全屏
        :return:
        """
        sleep(1)
        cls.hot_key("alt", "enter")

    @classmethod
    def printscreen(cls):
        """
         快捷键截取全屏
        :return:
        """
        sleep(1)
        cls.hot_key("printscreen")

    @classmethod
    def alt_o(cls):
        """
         ocr应用内部快捷键
        :return:
        """
        sleep(1)
        cls.hot_key("alt", "o")

    @classmethod
    def alt_s(cls):
        """
         快捷键连拍截图
        :return:
        """
        sleep(1)
        cls.hot_key("alt", "s")

    @classmethod
    def alt_p(cls):
        """
         贴图应用内部快捷键
        :return:
        """
        sleep(1)
        cls.hot_key("alt", "p")

    @classmethod
    def p(cls):
        """
         按下p快捷键
        :return:
        """
        sleep(1)
        cls.press_key("p")

    @classmethod
    def h(cls):
        """
         按下h快捷键
        :return:
        """
        sleep(1)
        cls.press_key("h")

    @classmethod
    def f(cls):
        """
         按下f快捷键
        :return:
        """
        sleep(1)
        cls.press_key("f")

    @classmethod
    def s(cls):
        """
         按下s快捷键
        :return:
        """
        sleep(1)
        cls.press_key("s")

    @classmethod
    def o(cls):
        """
         按下o快捷键
        :return:
        """
        sleep(1)
        cls.press_key("o")

    @classmethod
    def r(cls):
        """
         按下r快捷键
        :return:
        """
        sleep(1)
        cls.press_key("r")

    @classmethod
    def i(cls):
        """
         按下i快捷键
        :return:
        """
        sleep(1)
        cls.press_key("i")

    @classmethod
    def alt_shift_tab(cls):
        """
         快捷键切换应用窗口
        :return:
        """
        cls.hot_key("alt", "shift", "tab")

    @classmethod
    def alt_printscreen(cls):
        """
         快捷键 <alt + PrintScreen>
        :return:
        """
        cls.hot_key("alt", "PrintScreen")

    @classmethod
    def super_d(cls):
        """快捷键 super + d
        :return:
        """
        cls.hot_key("win", "d")

    @classmethod
    def super(cls):
        """快捷键 super
        :return:
        """
        cls.hot_key("win")

    @classmethod
    def pageup(cls):
        """
         上一页
        :return:
        """
        cls.press_key("pageup")

    @classmethod
    def pagedown(cls):
        """
         下一页
        :return:
        """
        cls.press_key("pagedown")
