from youqu3.exception import YouQuPluginInstalledError

try:
    import requests

    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

if HAS_REQUESTS is False:
    raise YouQuPluginInstalledError("requests")