import click

from brag.cmds import hello


@click.group()
def cli():
    """Cli Group Parameter"""


def register_commands():
    cli.add_command(hello)

if __name__ == '__main__':
    register_commands()
    cli()
