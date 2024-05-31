#!/usr/bin/python3
# -*- coding: utf-8 -*-

from funnylog import log
from funnylog import logger

import_error_log = lambda x: f"{x} not installed, try: pip install {x}"

try:
    from image_center import ImageCenter as ImageCenter
except ImportError:
    raise ImportError(import_error_log("image_center"))

try:
    from pdocr_rpc import OCR as OCR
except ImportError:
    raise ImportError(import_error_log("pdocr-rpc"))

try:
    from youqu_dogtail import DogtailUtils
except ImportError:
    raise ImportError(import_error_log("youqu-dogtail"))

try:
    from youqu_mousekey import MouseKey as MouseKey
except ImportError:
    raise ImportError(import_error_log("youqu-mousekey"))

from youqu3.setting import setting

__all__ = [
    "YouQu",
    "ImageCenter",
    "OCR",
    "DogtailUtils",
    "setting",
    "log",
    "logger",
]


class YouQu(
    ImageCenter,
    OCR,
    MouseKey,
):
    ...
