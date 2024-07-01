from youqu3 import setting
from youqu3.exceptions import YouQuPluginDependencyError

try:
    import pylinuxauto as pylinuxauto

    from pylinuxauto.config import config

    config.OCR_SERVER_IP = setting.OCR_SERVER_HOST
    config.IMAGE_SERVER_IP = setting.IMAGE_SERVER_HOST

except ImportError:
    raise YouQuPluginDependencyError("pylinuxauto")
