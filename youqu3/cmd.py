from typing import List
from typing import Union

import easyprocess

from youqu3 import logger
from youqu3 import setting


class Cmd:

    @staticmethod
    def run(cmd: Union[List[str], str], return_code=False):
        logger.debug(cmd)
        call = easyprocess.EasyProcess(cmd).call()
        if return_code:
            return call.stdout, call.return_code
        return call.stdout

    @classmethod
    def sudo_run(cls, cmd: str, return_code=False):
        logger.debug(cmd)
        return cls.run(f"echo '{setting.PASSWORD}' | sudo -S {cmd}", return_code=return_code)



if __name__ == '__main__':
    stdout, return_code = Cmd.run("ls", return_code=True)
    # stdout = Cmd.run("ls")
    print(stdout)
    print(return_code)
