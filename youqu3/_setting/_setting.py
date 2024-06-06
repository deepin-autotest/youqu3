from dataclasses import dataclass

from youqu3._setting._dynamic import _DynamicSetting


class _Setting(_DynamicSetting):
    """Global Config"""

    MAX_FAIL = 1
    TIMEOUT = 300
    LOG_LEVEL = "INFO"
    RERUNS = 1
    RECORD_FAILED_CASE = 1

    # OCR
    OCR_NETWORK_RETRY = 1
    OCR_PAUSE = 1
    OCR_TIMEOUT = 5
    OCR_MAX_MATCH_NUMBER = 100
    OCR_PORT = 8890
    OCR_SERVER_HOST = "10.8.13.7/10.8.13.66/10.8.13.55/10.8.13.100"

    @dataclass
    class Sleepx:
        x86_64: [float, int] = 1
        aarch64: [float, int] = 1.5
        loongarch64: [float, int] = 2
        mips64: [float, int] = 2.5
        sw64: [float, int] = 2.5


setting = _Setting()
