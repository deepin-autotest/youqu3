from youqu3.cmd import Cmd


def venv():
    Cmd.run('pip3 install pipenv -i https://pypi.tuna.tsinghua.edu.cn/simple')
    Cmd.run("pipenv --python 3")
    Cmd.run("pipenv run pip install -r requirements.txt")


if __name__ == '__main__':
    venv()
