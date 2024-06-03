#!/usr/bin/python3
# -*- coding: utf-8 -*-

from funnylog import log
from funnylog import logger

from youqu3._setting import setting as setting

try:
    from youqu_imagecenter_rpc import ImageCenter as ImageCenter

    HAS_IMAGECENTER = False
except ImportError:
    HAS_IMAGECENTER = False

try:
    from pdocr_rpc import OCR as OCR

    HAS_OCR = True
except ImportError:
    HAS_OCR = False

try:
    from youqu_dogtail import DogtailUtils as Dogtail

    HAS_DOGTAIL = True
except ImportError:
    HAS_DOGTAIL = False

try:
    from youqu_mousekey import MouseKey as MouseKey

    HAS_MOUSEKEY = True
except ImportError:
    HAS_MOUSEKEY = False

__all__ = [
    "YouQu",
    "ImageCenter",
    "OCR",
    "Dogtail",
    "setting",
    "log",
    "logger",
]

if HAS_IMAGECENTER and HAS_OCR and HAS_MOUSEKEY:
    class YouQu(ImageCenter, OCR, MouseKey):
        ...
elif HAS_IMAGECENTER and HAS_OCR:
    class YouQu(ImageCenter, OCR):
        ...
elif HAS_IMAGECENTER and HAS_MOUSEKEY:
    class YouQu(ImageCenter, MouseKey):
        ...
elif HAS_OCR and HAS_MOUSEKEY:
    class YouQu(OCR, MouseKey):
        ...
elif HAS_IMAGECENTER:
    class YouQu(ImageCenter):
        ...
elif HAS_OCR:
    class YouQu(OCR):
        ...
elif HAS_MOUSEKEY:
    class YouQu(MouseKey):
        ...
