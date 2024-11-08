import click
from rich.console import Console
from base_cmds.add import add_cmd
from base_cmds.init import init as init_cmd
from base_cmds.show import show as show_cmd

console = Console()

@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--show', '--s', help='Show brag entries')
@click.option('--add', '--a', help='Add a quick entry')
@click.option('--type', '--t', default='brag',
              type=click.Choice(['brag', 'todo', 'meeting', 'idea']),
              help='Type of entry')
def cli(ctx, add, type):
    """Cli Group Parameter"""
    if ctx.invoked_subcommand is None and add:
        add_cmd(add, type)
    elif ctx.invoked_subcommand is None and show:
        show_cmd(show)
    else:
        console.print("No command specified",style="red")
       
@cli.command()
@click.argument('comment')
@click.option('--type', '--t', default='brag',
              type=click.Choice(['brag', 'todo', 'meeting', 'idea']),
              help='Type of entry')
def add(comment, type):
    """Add a brag entry"""
    add_cmd(comment, type)


@cli.command()
@click.argument('show',type=click.Choice(['today','week','all','last-week']))
def show(show):
    """Show brag entries"""
    console.print(f"Showing {show} entries", style="green")
    show_cmd(show)


@cli.command()
@click.argument


@cli.command()
def init():
    """Initialize the application"""
    init_cmd()



if __name__ == '__main__':
    cli()
