from rich.table import Table
from rich.console import Console
from click.types import Choice
from datetime import datetime, timedelta
from pathlib import Path
import re
import glob
import os

console = Console()

def show(show_type: Choice):
    base_path = Path(os.environ.get("BRAG_DOCS_PATH"))

    _show_impl(show_type,base_path)


def _fetch_entries(show_type: str, base_path: Path):
    """Fetch entries based on time filter"""
    now = datetime.now()
    entries = []

    # Define date ranges based on show_type
    if show_type == 'today':
        print(f"now: {now}")
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    elif show_type == 'week':
        start_date = now - timedelta(days=now.weekday())
        start_date = start_date.replace(hour=0, minute=0, second=0)
        end_date = start_date + timedelta(days=6, hours=23, minutes=59, seconds=59)
    elif show_type == 'last-week':
        start_date = now - timedelta(days=now.weekday() + 7)
        start_date = start_date.replace(hour=0, minute=0, second=0)
        end_date = start_date + timedelta(days=6, hours=23, minutes=59, seconds=59)
    else:  # 'all'
        start_date = datetime.min
        end_date = datetime.max

    # Search through all markdown files
    for file in glob.glob(str(base_path / "**/*.md"), recursive=True):
        with open(file, 'r') as f:
            content = f.read()
            
            # Extract month and year
            month_year_pattern = r'# Month: (\d+) - Year: (\d+)'
            month_year_match = re.search(month_year_pattern, content)
            if not month_year_match:
                continue
                
            month = int(month_year_match.group(1))
            year = int(month_year_match.group(2))
            
            # Extract created date
            created_pattern = r'Created: (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})'
            created_match = re.search(created_pattern, content)
            if not created_match:
                continue
                
            file_date = datetime.strptime(created_match.group(1), '%Y-%m-%d')
            
            if start_date <= file_date <= end_date:
                # Extract entries
                entry_pattern = r'\* \[(\d{2}:\d{2}:\d{2})\] \((\w+)\) (.+?)(?=\n|$)'
                for entry_match in re.finditer(entry_pattern, content):
                    time, entry_type, comment = entry_match.groups()
                    
                    entries.append({
                        'date': file_date.strftime('%Y-%m-%d'),
                        'time': time,
                        'type': entry_type,
                        'comment': comment.strip()
                    })

    return sorted(entries, key=lambda x: (x['date'], x['time']), reverse=True)

    return sorted(entries, key=lambda x: (x['date'], x['time']), reverse=True)
    

def _show_impl(show_type: str,  base_path: Path):
    table = Table(title="Brag Entries")
    table.add_column("Date", justify="center", style="cyan", no_wrap=True)
    table.add_column("Time", justify="center", style="magenta", no_wrap=True)
    table.add_column("Type", justify="center", style="green", no_wrap=True)
    table.add_column("Comment", justify="center", style="yellow", no_wrap=True)

    entries = _fetch_entries(show_type, base_path)

    if not entries:
        console.print(f"No entries found for {show_type}", style="yellow")
        return

    for entry in entries:
        table.add_row(
            entry['date'],
            entry['time'],
            entry['type'],
            entry['comment']
        )

    console.print(table)