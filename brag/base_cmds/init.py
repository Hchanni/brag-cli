import os
from pathlib import Path
from rich.console import Console
from rich.spinner import Spinner

console = Console()

def init():
    console.print("Welcome to brag by @Hchanni")
    with console.status("[bold green]Setting up your brag docs...", spinner="dots") as status:
        _initialize()
        console.print("[green]✓[/green] Initialization complete!")

def _initialize():
    base_path = os.environ.get("BRAG_DOCS_PATH")
    if base_path is None:
        console.print("BRAG_DOCS_PATH environment variable not set", style="red")
        exit(1)
    else:
        base_path = Path(base_path)
        base_path.mkdir(mode=0o777, parents=True, exist_ok=True)
