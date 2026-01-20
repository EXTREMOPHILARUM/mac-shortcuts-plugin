#!/usr/bin/env python3
"""
Mac Shortcuts Plugin - Output Formatter

Formats shortcut data with colors and tables for terminal display.
"""

import json
import sys
from typing import List, Dict, Any, Optional

# Try to import rich for advanced formatting, fallback to basic if not available
try:
    from rich.console import Console
    from rich.table import Table
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# ANSI color codes for fallback
class Colors:
    """ANSI color codes for terminal output."""
    RESET = '\033[0m'
    BOLD = '\033[1m'

    # Foreground colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

    # Success/Error
    SUCCESS = GREEN
    ERROR = RED
    WARNING = YELLOW
    INFO = CYAN


def colorize(text: str, color: str) -> str:
    """
    Add ANSI color codes to text.

    Args:
        text: Text to colorize
        color: Color code (from Colors class)

    Returns:
        Colorized text string
    """
    return f"{color}{text}{Colors.RESET}"


def format_table_basic(shortcuts: List[Dict[str, str]], show_identifiers: bool = False) -> str:
    """
    Format shortcuts as a basic text table (fallback when rich is not available).

    Args:
        shortcuts: List of shortcut dictionaries
        show_identifiers: Whether to show identifier column

    Returns:
        Formatted table string
    """
    if not shortcuts:
        return colorize("No shortcuts found", Colors.WARNING)

    # Calculate column widths
    max_name_len = max(len(s.get('name', '')) for s in shortcuts)
    max_name_len = max(max_name_len, len("Name"))

    if show_identifiers:
        max_id_len = max(len(s.get('identifier', '')) for s in shortcuts)
        max_id_len = max(max_id_len, len("Identifier"))

    # Header
    header = colorize(f"{'Name':<{max_name_len}}", Colors.BOLD + Colors.CYAN)
    separator = "─" * max_name_len

    if show_identifiers:
        header += "  " + colorize(f"{'Identifier':<{max_id_len}}", Colors.BOLD + Colors.CYAN)
        separator += "  " + ("─" * max_id_len)

    lines = [header, separator]

    # Rows
    for shortcut in shortcuts:
        name = shortcut.get('name', '')
        row = colorize(f"{name:<{max_name_len}}", Colors.WHITE)

        if show_identifiers:
            identifier = shortcut.get('identifier', '')
            row += "  " + colorize(f"{identifier:<{max_id_len}}", Colors.BLUE)

        lines.append(row)

    return '\n'.join(lines)


def format_table_rich(shortcuts: List[Dict[str, str]], show_identifiers: bool = False) -> None:
    """
    Format shortcuts as a rich table with colors.

    Args:
        shortcuts: List of shortcut dictionaries
        show_identifiers: Whether to show identifier column
    """
    if not shortcuts:
        console = Console()
        console.print("[yellow]No shortcuts found[/yellow]")
        return

    console = Console()
    table = Table(show_header=True, header_style="bold cyan")

    table.add_column("Name", style="white", no_wrap=False)

    if show_identifiers:
        table.add_column("Identifier", style="blue", no_wrap=False)

    # Add folder column if present
    has_folders = any('folder' in s for s in shortcuts)
    if has_folders:
        table.add_column("Folder", style="magenta")

    for shortcut in shortcuts:
        row = [shortcut.get('name', '')]

        if show_identifiers:
            row.append(shortcut.get('identifier', ''))

        if has_folders:
            folder = shortcut.get('folder', 'none')
            row.append(folder if folder != 'none' else '[dim]No Folder[/dim]')

        table.add_row(*row)

    console.print(table)


def format_by_folder_basic(organized: Dict[str, List[Dict[str, str]]]) -> str:
    """
    Format shortcuts organized by folder (basic version).

    Args:
        organized: Dictionary mapping folder names to shortcut lists

    Returns:
        Formatted string
    """
    lines = []

    for folder, shortcuts in organized.items():
        if not shortcuts:
            continue

        # Folder header
        folder_header = f"\n{folder}:"
        lines.append(colorize(folder_header, Colors.BOLD + Colors.BLUE))

        # Shortcuts in folder
        for shortcut in shortcuts:
            name = shortcut.get('name', '')
            lines.append(f"  • {colorize(name, Colors.WHITE)}")

    return '\n'.join(lines)


def format_by_folder_rich(organized: Dict[str, List[Dict[str, str]]]) -> None:
    """
    Format shortcuts organized by folder (rich version).

    Args:
        organized: Dictionary mapping folder names to shortcut lists
    """
    console = Console()

    for folder, shortcuts in organized.items():
        if not shortcuts:
            continue

        console.print(f"\n[bold blue]{folder}:[/bold blue]")

        for shortcut in shortcuts:
            name = shortcut.get('name', '')
            console.print(f"  • {name}")


def format_shortcuts(shortcuts: List[Dict[str, str]], show_identifiers: bool = False,
                    use_rich: bool = True) -> Optional[str]:
    """
    Format shortcuts list for display.

    Args:
        shortcuts: List of shortcut dictionaries
        show_identifiers: Whether to show identifier column
        use_rich: Whether to use rich formatting (if available)

    Returns:
        Formatted string if basic formatting, None if rich (prints directly)
    """
    if use_rich and RICH_AVAILABLE:
        format_table_rich(shortcuts, show_identifiers)
        return None
    else:
        return format_table_basic(shortcuts, show_identifiers)


def format_organized(organized: Dict[str, List[Dict[str, str]]],
                    use_rich: bool = True) -> Optional[str]:
    """
    Format organized shortcuts (by folder) for display.

    Args:
        organized: Dictionary mapping folder names to shortcut lists
        use_rich: Whether to use rich formatting (if available)

    Returns:
        Formatted string if basic formatting, None if rich (prints directly)
    """
    if use_rich and RICH_AVAILABLE:
        format_by_folder_rich(organized)
        return None
    else:
        return format_by_folder_basic(organized)


def format_success(message: str) -> str:
    """Format a success message."""
    if RICH_AVAILABLE:
        from rich.console import Console
        console = Console()
        console.print(f"[green]✓[/green] {message}")
        return ""
    else:
        return colorize(f"✓ {message}", Colors.SUCCESS)


def format_error(message: str) -> str:
    """Format an error message."""
    if RICH_AVAILABLE:
        from rich.console import Console
        console = Console()
        console.print(f"[red]✗[/red] {message}", file=sys.stderr)
        return ""
    else:
        return colorize(f"✗ {message}", Colors.ERROR)


def format_info(message: str) -> str:
    """Format an info message."""
    if RICH_AVAILABLE:
        from rich.console import Console
        console = Console()
        console.print(f"[cyan]ℹ[/cyan] {message}")
        return ""
    else:
        return colorize(f"ℹ {message}", Colors.INFO)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Format shortcuts output")
    parser.add_argument('--input', required=True, help='JSON input file or string')
    parser.add_argument('--show-identifiers', action='store_true',
                       help='Show identifier column')
    parser.add_argument('--organize-by-folder', action='store_true',
                       help='Format as folder-organized output')
    parser.add_argument('--no-rich', action='store_true',
                       help='Disable rich formatting (use basic)')

    args = parser.parse_args()

    try:
        # Load JSON data
        try:
            with open(args.input, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            # Try parsing as JSON string
            data = json.loads(args.input)

        use_rich = not args.no_rich

        if args.organize_by_folder:
            result = format_organized(data, use_rich)
        else:
            result = format_shortcuts(data, args.show_identifiers, use_rich)

        if result:
            print(result)

    except Exception as e:
        print(f"Error formatting output: {e}", file=sys.stderr)
        sys.exit(1)
