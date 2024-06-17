import random

from youqu3.exception import YouQuPluginInstalledError

try:
    from youqu_imagecenter_rpc import ImageCenter as _ImageCenter
    from youqu_imagecenter_rpc import setting as image_setting

    from youqu3 import setting

    HAS_IMAGECENTER = False
except ImportError:
    HAS_IMAGECENTER = False

if HAS_IMAGECENTER is False:
    raise YouQuPluginInstalledError("youqu-imagecenter-rpc")

from youqu3.mkmixin import MouseKeyChainMixin


class ImageCenter(MouseKeyChainMixin):
    image_setting.NETWORK_RETRY = int(setting.IMAGE_NETWORK_RETRY)
    image_setting.PAUSE = float(setting.IMAGE_PAUSE)
    image_setting.TIMEOUT = float(setting.IMAGE_TIMEOUT)
    image_setting.MAX_MATCH_NUMBER = int(setting.IMAGE_MAX_MATCH_NUMBER)
    image_setting.PORT = setting.IMAGE_PORT
    _image_servers = [i.strip() for i in setting.IMAGE_SERVER_HOST.split("/") if i]
    x = None
    y = None
    result = None

    @classmethod
    def find_image(cls, *args, **kwargs):
        servers = cls._image_servers
        while servers:
            image_setting.SERVER_IP = random.choice(servers)
            if _ImageCenter.check_connected() is False:
                servers.remove(image_setting.SERVER_IP)
                image_setting.SERVER_IP = None
            else:
                break
        if image_setting.SERVER_IP is None:
            raise EnvironmentError(f"所有IMAGE服务器不可用: {cls._image_servers}")
        cls.result = _ImageCenter.find_image(*args, **kwargs)

        if isinstance(cls.result, tuple):
            cls.x, cls.y = cls.result

        return cls
