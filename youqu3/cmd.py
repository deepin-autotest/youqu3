from typing import Union
from typing import List

import easyprocess

from youqu3 import logger
from youqu3 import setting


class Cmd:

    @staticmethod
    def run_cmd(cmd: Union[List[str], str]) -> easyprocess.EasyProcess:
        logger.debug(cmd)
        return easyprocess.EasyProcess(cmd).call()

    @classmethod
    def sudo_run_cmd(cls, cmd: str) -> easyprocess.EasyProcess:
        logger.debug(cmd)
        return cls.run_cmd(f"echo '{setting.PASSWORD}' | sudo -S {cmd}")


if __name__ == '__main__':
    stdout = Cmd.run_cmd("ls").stdout
    return_code = Cmd.run_cmd("ls").return_code
    print(stdout)
    print(return_code)
