import os.path
import pathlib

from youqu3 import exception
from youqu3 import logger
from youqu3 import setting
from youqu3.cmd import Cmd


def env():
    rootdir = pathlib.Path(".").absolute()
    logger.info(rootdir)
    # pip
    try:
        Cmd.run("pip3 --version", interrupt=True)
    except exception.ShellExecutionFailed:
        Cmd.run('curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py')
    # youqu3
    Cmd.run(f'pip3 install youqu3 -i {setting.PYPI_MIRROR}')
    # youqu3-env
    youqu3_env_cmd_txt = 'pipenv run youqu3 "$@"'
    youqu3_env_cmd_path = os.path.expanduser("~/.local/bin/youqu3-env")
    if not os.path.exists(youqu3_env_cmd_path):
        Cmd.run(f"echo '{youqu3_env_cmd_txt}' >> {youqu3_env_cmd_path}")
    # PATH
    with open(os.path.expanduser("~/.bashrc"), 'r') as f:
        bashrc = f.read()
    path_cmd = "export PATH=$PATH:$HOME/.local/bin"
    if path_cmd not in bashrc:
        Cmd.run(f"echo '{path_cmd}' >> ~/.bashrc")
    Cmd.run("source ~/.bashrc")
    # pipenv
    Cmd.run(f'pip3 install pipenv -i {setting.PYPI_MIRROR}')
    Cmd.run(f"cd {rootdir} && pipenv --python 3")
    Cmd.run(f"cd {rootdir} && pipenv run pip install -r requirements.txt")


if __name__ == '__main__':
    env()
