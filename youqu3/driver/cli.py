import click


@click.group()
def cli():
    from youqu3 import version
    click.echo(f"YouQu3 - {version}")


@cli.command()
@click.option("-f", "--filepath", default=None, type=click.STRING, help="filepath driver")
@click.option("-k", "--keywords", default=None, type=click.STRING, help="keywords driver")
@click.option("-t", "--tags", default=None, type=click.STRING, help="tags driver")
def run(
        filepath,
        keywords,
        tags,
):
    """RUN驱动"""
    args = {
        "filepath": filepath,
        "keywords": keywords,
        "tags": tags,
    }
    from youqu3.driver.run import Run
    Run(**args).run()


@cli.command()
@click.option("-c", "--clients", default=None, type=click.STRING, help="clients")
@click.option("-s", "--send", default=None, type=click.STRING, help="send code to client")
@click.option("-e", "--build-env", default=None, type=click.STRING, help="build client env")
@click.option("-m", "--mode", default="parallel", type=click.Choice(["parallel", "nginx"]),
              help="remote driver mode (parallel or nginx)")
@click.option("-f", "--filepath", default=None, type=click.STRING, help="filepath driver")
@click.option("-k", "--keywords", default=None, type=click.STRING, help="keywords driver")
@click.option("-t", "--tags", default=None, type=click.STRING, help="tags driver")
def remote(
        clients,
        send,
        build_env,
        mode,
        filepath,
        keywords,
        tags,
):
    """REMOTE驱动"""
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
@click.option("--python", default="3", type=click.STRING, help="指定虚拟环境的Python版本")
def envx(python):
    """超级环境管理器"""
    from youqu3.driver.envx import envx as env
    env(python_version=python)


if __name__ == '__main__':
    cli()
