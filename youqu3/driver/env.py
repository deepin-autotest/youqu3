import pathlib
from youqu3.cmd import Cmd
from youqu3 import exception
from youqu3 import setting


def env():
    rootdir = pathlib.Path(".").absolute()
    try:
        Cmd.run("pip3 --version", interrupt=True)
    except exception.ShellExecutionFailed:
        Cmd.run('curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py')

    Cmd.run(f'pip3 install youqu3 -i {setting.PYPI_MIRROR}')
    Cmd.run(f'pip3 install pipenv -i {setting.PYPI_MIRROR}')
    Cmd.run("pipenv --python 3")
    Cmd.run(f"pipenv run pip install -r {rootdir}/requirements.txt")


if __name__ == '__main__':
    env()
