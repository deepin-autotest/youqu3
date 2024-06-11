import click
from rich.console import Console

console = Console()


@click.group()
def cli():
    console.print(
        "YouQu3 :dragon:",
        style="blue",
    )


@cli.command()
@click.option("-k", "--keywords", default=None, type=click.STRING, help="keywords")
@click.option("-t", "--tags", default=None, type=click.STRING, help="tags")
def run(
        keywords,
        tags,
):
    """RUN模式"""
    args = {
        "keywords": keywords,
        "tags": tags,
    }
    # console.print(args)
    from youqu3.driver.run import Run
    Run(**args).run()


@cli.command()
def remote():
    """REMOTE模式"""
    console.print("Remote Running YouQu3")

@cli.command()
def init():
    """初始化APP工程"""
    console.print("init")
    from youqu3.driver.init import Init
    Init().init()


if __name__ == '__main__':
    cli()
