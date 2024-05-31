#!/usr/bin/python3
# -*- coding: utf-8 -*-

from funnylog import log
from funnylog import logger

try:
    from image_center import ImageCenter as ImageCenter
except ImportError:
    raise ImportError("image-center not installed, try: pip install image-center")
try:
    from pdocr_rpc import OCR as OCR
except ImportError:
    raise ImportError("pdocr-rpc not installed, try: pip install pdocr-rpc")
try:
    from youqu_dogtail import DogtailUtils
except ImportError:
    raise ImportError("youqu-dogtail not installed, try: pip install youqu-dogtail")

from youqu3.mousekey import MouseKey as MouseKey
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
