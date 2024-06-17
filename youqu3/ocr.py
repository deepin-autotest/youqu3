import random

from youqu3.exception import YouQuPluginInstalledError

try:
    from pdocr_rpc import OCR as _OCR
    from pdocr_rpc import setting as ocr_setting

    from youqu3 import setting

    HAS_OCR = True
except ImportError:
    HAS_OCR = False

if HAS_OCR is False:
    raise YouQuPluginInstalledError("pdocr-rpc")

from youqu3.mkmixin import MouseKeyChainMixin


class OCR(MouseKeyChainMixin):

    ocr_setting.NETWORK_RETRY = int(setting.OCR_NETWORK_RETRY)
    ocr_setting.PAUSE = float(setting.OCR_PAUSE)
    ocr_setting.TIMEOUT = float(setting.OCR_TIMEOUT)
    ocr_setting.MAX_MATCH_NUMBER = int(setting.OCR_MAX_MATCH_NUMBER)
    ocr_setting.PORT = setting.OCR_PORT
    _ocr_servers = [i.strip() for i in setting.OCR_SERVER_HOST.split("/") if i]

    @classmethod
    def ocr(cls, *args, **kwargs):
        """ocr load balance"""
        servers = cls._ocr_servers
        while servers:
            ocr_setting.SERVER_IP = random.choice(servers)
            if _OCR.check_connected() is False:
                servers.remove(ocr_setting.SERVER_IP)
                ocr_setting.SERVER_IP = None
            else:
                break
        if ocr_setting.SERVER_IP is None:
            raise EnvironmentError(f"所有OCR服务器不可用: {cls._ocr_servers}")
        cls.result = _OCR.ocr(*args, **kwargs)

        if isinstance(cls.result, tuple):
            cls.x, cls.y = cls.result

        return cls


if __name__ == '__main__':
    OCR.ocr("所有").center()