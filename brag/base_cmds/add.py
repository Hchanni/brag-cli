from rich.console import Console
from typing import Union
from pathlib import Path
import os
import click
from datetime import datetime
from utils.utils import brag_is_setup, validate_and_get_file, get_week_of_month

console = Console()

def add_cmd(comment: str, type: Union[str, click.Choice]):

    if not brag_is_setup():
        console.print("BRAG is not set up. Please run `brag init`", style="red")
        exit(1)
    console.print(f"Adding a {type} entry: {comment}", style="green")
    _add_cmd(comment, type)


def _create_new_file(file_path: Path):
    """Create a new markdown file with proper headers"""
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    week_num = get_week_of_month(now)

    with file_path.open('w') as f:
        
        f.write(f"# Month: {month} - Year: {year}\n\n")
        f.write(f"## Week {week_num}\n\n")
        f.write(f"Created: {now.strftime('%Y-%m-%d %H:%M:%S')}\n\n")


def _append_to_file(file_path: Path, comment: str, entry_type: str = "brag"):
    """Append content to the markdown file"""
    timestamp = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")

    # Read existing content to check if date header exists
    existing_content = ""
    if file_path.exists():
        existing_content = file_path.read_text()

    with file_path.open('a') as f:
        # If file is new or date doesn't exist, add date header
        if not existing_content or timestamp not in existing_content:
            f.write(f"\n## {timestamp}\n")
        
        # Add entry with timestamp and type
        f.write(f"* [{time}] ({entry_type}) {comment}\n")


def _add_cmd(comment: str, type: Union[str, click.Choice]):
    path = Path(os.environ.get("BRAG_DOCS_PATH"))
    file_path, is_new_file = validate_and_get_file(path)
    if is_new_file:
        _create_new_file(file_path)
        console.print(f"Created new file: {file_path}", style="green")
    
    _append_to_file(file_path, comment,type)