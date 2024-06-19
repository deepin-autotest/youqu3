import click
from youqu3 import version


@click.group()
@click.help_option("-h", "--help", help="查看帮助信息")
@click.version_option(prog_name="YouQu3", version=version, help="查看版本号")
def cli(): ...


@cli.command()
@click.help_option("-h", "--help", help="查看帮助信息")
@click.option("-f", "--filepath", default=None, type=click.STRING,
              help="指定用例文件或目录路径执行，")
@click.option("-k", "--keywords", default=None, type=click.STRING,
              help="指定用例关键词执行，支持 'and/or/not' 逻辑表达式")
@click.option("-t", "--tags", default=None, type=click.STRING,
              help="指定用例标签执行，支持 'and/or/not' 逻辑表达式")
def run(
        filepath,
        keywords,
        tags,
):
    """本地执行"""
    args = {
        "filepath": filepath,
        "keywords": keywords,
        "tags": tags,
    }
    from youqu3.driver.run import Run
    Run(**args).run()


@cli.command()
@click.help_option("-h", "--help", help="查看帮助信息")
@click.option("-c", "--clients", default=None, type=click.STRING,
              help="远程机器信息:user@ip:password，多个机器之间用 '/' 连接")
@click.option("-s", "--send", default=None, type=click.STRING,
              help="发送代码到远程机器")
@click.option("-e", "--build-env", default=None, type=click.STRING,
              help="远程机器安装环境")
@click.option("-m", "--mode", default="parallel", type=click.Choice(["parallel", "nginx"]),
              help="远程控制驱动模式 (parallel or nginx)")
@click.option("-f", "--filepath", default=None, type=click.STRING,
              help="指定用例文件路径执行")
@click.option("-k", "--keywords", default=None, type=click.STRING,
              help="指定用例关键词执行，支持 'and/or/not' 逻辑表达式")
@click.option("-t", "--tags", default=None, type=click.STRING,
              help="指定用例标签执行，支持 'and/or/not' 逻辑表达式")
def remote(
        clients,
        send,
        build_env,
        mode,
        filepath,
        keywords,
        tags,
):
    """远程控制执行"""
    args = {
        "clients": clients,
        "send": send,
        "build_env": build_env,
        "mode": mode,
        "filepath": filepath,
        "keywords": keywords,
        "tags": tags,
    }
    from youqu3.driver.remote import Remote
    Remote(**args).run()


@cli.command()
def init():
    """创建用例工程"""
    from youqu3.driver.init import Init
    Init().init()


@cli.command()
@click.help_option("-h", "--help", help="查看帮助信息")
@click.option("--python", default="3", type=click.STRING, help="指定虚拟环境的Python版本")
def envx(python):
    """虚拟环境安装"""
    from youqu3.driver.envx import envx as env
    env(python_version=python)


if __name__ == '__main__':
    cli()
