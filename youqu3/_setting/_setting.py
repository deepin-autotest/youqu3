from youqu3._setting._dynamic import _DynamicSetting


class _Setting(_DynamicSetting):
    """Global Config"""

    MAX_FAIL = 1
    TIMEOUT = 300
    LOG_LEVEL = "INFO"
    RERUNS = 1
    RECORD_FAILED_CASE = 1


setting = _Setting()
