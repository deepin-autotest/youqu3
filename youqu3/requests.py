from funnylog.conf import setting as log_setting

from youqu3 import log
from youqu3.exceptions import YouQuPluginDependencyError

try:
    import requests

    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

if HAS_REQUESTS is False:
    raise YouQuPluginDependencyError("requests")

log_setting.CLASS_NAME_ENDSWITH = "Requests"


@log
class Requests:

    def get(self, url, params=None, **kwargs):
        """
        get method
        [url:{{url}}]
        [params:{{params}}]
        [kwargs:{{kwargs}}]
        """
        return requests.get(url, params=params, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        """
        post method
        [url:{{url}}]
        [data: {{data}}]
        [json: {{json}}]
        [kwargs: {{kwargs}}]
        """
        return requests.post(url, data=data, json=json, **kwargs)
