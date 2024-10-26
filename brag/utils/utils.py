import os
from pathlib import Path
from rich.console import Console
from datetime import datetime

def brag_is_setup():
    path = Path(os.environ.get("BRAG_DOCS_PATH"))
    console = Console()

    if path.exists():
        console.print("[bold green]BRAG is set up![/bold green]")
        return True
    else:
        console.print("[bold red]BRAG is not set up.[/bold red]")
        return False

def get_week_of_month(date:datetime):
    first_day = date.replace(day=1)
    dom = date.day
    adjusted_dom = dom + first_day.weekday()
    return (adjusted_dom-1) // 7 + 1


def _get_current_file_path(base_path: Path) -> Path:
    now = datetime.now()
    year = now.year
    month = now.month
    week_num = get_week_of_month(now)

    # Create year and month directories if they don't exist
    year_dir: Path = base_path / str(year)
    month_dir: Path = year_dir / str(month)
    month_dir.mkdir(parents=True, exist_ok=True)

    file_name = f"week_{week_num:02}.md"

    return month_dir / file_name


def validate_and_get_file(base_path: Path) -> tuple[Path, bool]:
    """
    Validates if current week's file exists and returns the path
    Returns tuple of (file_path, is_new_file)
    """
    file_path = _get_current_file_path(base_path)
    is_new_file = not file_path.exists()
    
    if is_new_file:
        # Create new file with header
        now = datetime.now()
        month_name = now.strftime("%B")
        week_num = get_week_of_month(now)
        
        file_path.write_text(
            f"# {month_name} Week {week_num}\n\n"
            "\n"
            f"Created: {now.strftime('%Y-%m-%d')}\n\n"
        )
    
    return file_path, is_new_file


