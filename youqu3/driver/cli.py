import click
from rich.console import Console

console = Console()


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    from youqu3 import version
    click.echo(version)
    ctx.exit()


@click.group()
def cli():
    ...


@cli.command()
@click.option("-k", "--keywords", default=None, type=click.STRING, help="keywords driver")
@click.option("-t", "--tags", default=None, type=click.STRING, help="tags driver")
def run(
        keywords,
        tags,
):
    """RUN驱动"""
    args = {
        "keywords": keywords,
        "tags": tags,
    }
    from youqu3.driver.run import Run
    Run(**args).run()


@cli.command()
@click.option("-k", "--keywords", default=None, type=click.STRING, help="keywords driver")
@click.option("-t", "--tags", default=None, type=click.STRING, help="tags driver")
@click.option("-c", "--clients", default=None, type=click.STRING, help="clients")
@click.option("-s", "--send", default=None, type=click.STRING, help="send code")
@click.option("-e", "--build-env", default=None, type=click.STRING, help="buildenv")
@click.option("-m", "--mode", default="parallel", type=click.Choice(["parallel", "nginx"]), help="mode")
def remote(
        keywords,
        tags,
        clients,
        send,
        build_env,
        mode,
):
    """REMOTE驱动"""
    args = {
        "keywords": keywords,
        "tags": tags,
        "clients": clients,
        "send": send,
        "build_env": build_env,
        "mode": mode,
    }
    from youqu3.driver.remote import Remote
    Remote(**args).run()


@cli.command()
def init():
    """创建用例工程"""
    from youqu3.driver.init import Init
    Init().init()


@cli.command()
def env():
    """安装YouQu环境"""
    from youqu3.driver.env import env
    env()


if __name__ == '__main__':
    cli()
