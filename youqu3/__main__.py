from image_center import ImageCenter as ImageCenter
from pdocr_rpc import OCR as OCR

from youqu3.mousekey import MouseKey as MouseKey


class YouQu(
    ImageCenter,
    OCR,
    MouseKey,
):
    ...
