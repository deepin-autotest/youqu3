import subprocess
import sys

from youqu3 import exception
from youqu3 import logger
from youqu3 import setting


class Cmd:

    @staticmethod
    def _run(command, _input=None, timeout=None, check=False, **kwargs):
        with subprocess.Popen(command, **kwargs) as process:
            try:
                stdout, stderr = process.communicate(_input, timeout=timeout)
            except:  # Including KeyboardInterrupt, communicate handled that.
                process.kill()
                raise
            retcode = process.poll()
            if check and retcode:
                raise subprocess.CalledProcessError(
                    retcode, process.args, output=stdout, stderr=stderr
                )
        return subprocess.CompletedProcess(process.args, retcode, stdout, stderr)

    @classmethod
    def _getstatusoutput(cls, command, timeout):
        kwargs = {
            "shell": True,
            "stderr": subprocess.STDOUT,
            "stdout": subprocess.PIPE,
            "timeout": timeout,
        }
        try:
            if sys.version_info >= (3, 7):
                kwargs["text"] = True
            result = cls._run(command, **kwargs)
            data = result.stdout
            if isinstance(data, bytes):
                data = data.decode("utf-8")
            exitcode = result.returncode
        except subprocess.CalledProcessError as ex:
            data = ex.output
            exitcode = ex.returncode
        except subprocess.TimeoutExpired as ex:
            # pylint: disable=unnecessary-dunder-call
            data = ex.__str__()
            exitcode = -1
        if data[-1:] == "\n":
            data = data[:-1]
        return exitcode, data

    @classmethod
    def sudo_run(
            cls,
            command,
            interrupt=False,
            timeout=25,
            print_log=True,
            command_log=True,
            password=None,
    ):
        if password is None:
            password = setting.PASSWORD
        return cls.run(
            f"echo '{password}' | sudo -S {command}",
            interrupt=interrupt,
            timeout=timeout,
            print_log=print_log,
            command_log=command_log,
        )

    @classmethod
    def run(cls, command, interrupt=False, timeout=25, print_log=True, command_log=True):
        """
         执行shell命令
        :param command: shell 命令
        :param interrupt: 命令异常时是否中断
        :param timeout: 命令执行超时
        :param out_debug_flag: 命令返回信息输出日志
        :param command_log: 执行的命令字符串日志
        :return: 返回终端输出
        """
        status, out = cls._getstatusoutput(command, timeout=timeout)
        if command_log:
            logger.debug(command)
        if status != 0 and interrupt:
            raise exception.ShellExecutionFailed(out)
        if print_log and out:
            logger.debug(out)
        return out


class RemoteCmd:

    def __init__(self, user: str, ip: str, password: str):
        self.user = user
        self.ip = ip
        self.password = password

    def remote_run(self, cmd: str):
        try:
            from fabric import Connection
        except ImportError:
            raise exception.YouQuPluginInstalledError("fabric")
        c = Connection(host=self.ip, user=self.user, connect_kwargs={'password': self.password})
        res = c.run(cmd)
        return res.stdout

    def remote_sudo_run(self, cmd: str):
        try:
            from fabric import Connection, Config
        except ImportError:
            raise exception.YouQuPluginInstalledError("fabric")
        c = Connection(
            host=self.ip, user=self.user, connect_kwargs={'password': self.password},
            config=Config(overrides={'sudo': {'password': self.password}})
        )
        res = c.sudo(cmd)
        return res.stdout


if __name__ == '__main__':
    stdout = Cmd.run(
        "sshpass -p '1' rsync -av -e ssh --exclude='__pycache__' --exclude='.pytest_cache' --exclude='.vscode' --exclude='.idea' --exclude='.git' --exclude='.github' --exclude='.venv' --exclude='report' --exclude='.gitignore'  /home/mikigo/github/youqu3-testcase/* uos@10.8.7.55:/home/uos/youqu3-testcase/",
        interrupt=True,
        print_log=False,
    )
    print(stdout)
