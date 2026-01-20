#!/usr/bin/env python3
"""
Mac Shortcuts Plugin - Interactive CLI Menus

Provides interactive selection menus for shortcuts operations.
Falls back to simple input() prompts if rich libraries are not available.
"""

import sys
from typing import List, Dict, Any, Optional

# Try to import questionary for interactive menus
try:
    import questionary
    from questionary import Style
    QUESTIONARY_AVAILABLE = True

    # Custom style for menus
    custom_style = Style([
        ('question', 'fg:#00FFFF bold'),  # Cyan
        ('answer', 'fg:#00FF00 bold'),    # Green
        ('pointer', 'fg:#FF00FF bold'),   # Magenta
        ('highlighted', 'fg:#00FF00'),    # Green
        ('selected', 'fg:#00FFFF'),       # Cyan
    ])
except ImportError:
    QUESTIONARY_AVAILABLE = False


def select_shortcut(shortcuts: List[str], prompt: str = "Select a shortcut:") -> Optional[str]:
    """
    Interactive shortcut selection from a list.

    Args:
        shortcuts: List of shortcut names
        prompt: Prompt message

    Returns:
        Selected shortcut name or None if cancelled
    """
    if not shortcuts:
        print("No shortcuts available", file=sys.stderr)
        return None

    if QUESTIONARY_AVAILABLE:
        try:
            return questionary.select(
                prompt,
                choices=shortcuts,
                style=custom_style
            ).ask()
        except KeyboardInterrupt:
            return None
    else:
        # Fallback to simple numbered menu
        print(f"\n{prompt}")
        for i, shortcut in enumerate(shortcuts, 1):
            print(f"  {i}. {shortcut}")

        try:
            choice = input("\nEnter number (or 'q' to quit): ").strip()
            if choice.lower() == 'q':
                return None

            index = int(choice) - 1
            if 0 <= index < len(shortcuts):
                return shortcuts[index]
            else:
                print("Invalid selection", file=sys.stderr)
                return None
        except (ValueError, KeyboardInterrupt):
            return None


def select_folder(folders: List[str], prompt: str = "Select a folder:") -> Optional[str]:
    """
    Interactive folder selection from a list.

    Args:
        folders: List of folder names
        prompt: Prompt message

    Returns:
        Selected folder name or None if cancelled
    """
    return select_shortcut(folders, prompt)


def select_signing_mode() -> Optional[str]:
    """
    Interactive signing mode selection.

    Returns:
        Selected mode ('anyone' or 'people-who-know-me') or None if cancelled
    """
    modes = [
        'people-who-know-me (default - only you and contacts)',
        'anyone (allows anyone to run the shortcut)'
    ]

    if QUESTIONARY_AVAILABLE:
        try:
            result = questionary.select(
                "Select signing mode:",
                choices=modes,
                style=custom_style
            ).ask()

            if result:
                return result.split(' ')[0]  # Extract mode name
            return None
        except KeyboardInterrupt:
            return None
    else:
        print("\nSelect signing mode:")
        print("  1. people-who-know-me (default)")
        print("  2. anyone")

        try:
            choice = input("\nEnter number: ").strip()
            if choice == '1':
                return 'people-who-know-me'
            elif choice == '2':
                return 'anyone'
            else:
                return 'people-who-know-me'  # Default
        except KeyboardInterrupt:
            return None


def prompt_for_path(prompt: str, must_exist: bool = False) -> Optional[str]:
    """
    Prompt for a file path with validation.

    Args:
        prompt: Prompt message
        must_exist: Whether the path must already exist

    Returns:
        Entered path or None if cancelled
    """
    from pathlib import Path

    if QUESTIONARY_AVAILABLE:
        try:
            path_str = questionary.path(
                prompt,
                only_directories=False,
                style=custom_style
            ).ask()

            if path_str and must_exist:
                path = Path(path_str).expanduser()
                if not path.exists():
                    print(f"Error: Path does not exist: {path}", file=sys.stderr)
                    return None

            return path_str
        except KeyboardInterrupt:
            return None
    else:
        try:
            path_str = input(f"\n{prompt} ").strip()

            if path_str and must_exist:
                path = Path(path_str).expanduser()
                if not path.exists():
                    print(f"Error: Path does not exist: {path}", file=sys.stderr)
                    return None

            return path_str if path_str else None
        except KeyboardInterrupt:
            return None


def confirm_action(message: str, default: bool = False) -> bool:
    """
    Get yes/no confirmation from user.

    Args:
        message: Question to ask
        default: Default value if user just presses enter

    Returns:
        True if confirmed, False otherwise
    """
    if QUESTIONARY_AVAILABLE:
        try:
            return questionary.confirm(
                message,
                default=default,
                style=custom_style
            ).ask()
        except KeyboardInterrupt:
            return False
    else:
        default_str = "Y/n" if default else "y/N"
        try:
            response = input(f"\n{message} [{default_str}]: ").strip().lower()

            if not response:
                return default

            return response in ['y', 'yes']
        except KeyboardInterrupt:
            return False


def text_input(prompt: str, default: str = "") -> Optional[str]:
    """
    Get text input from user.

    Args:
        prompt: Prompt message
        default: Default value

    Returns:
        User input or None if cancelled
    """
    if QUESTIONARY_AVAILABLE:
        try:
            return questionary.text(
                prompt,
                default=default,
                style=custom_style
            ).ask()
        except KeyboardInterrupt:
            return None
    else:
        try:
            default_hint = f" [{default}]" if default else ""
            response = input(f"\n{prompt}{default_hint}: ").strip()
            return response if response else (default if default else None)
        except KeyboardInterrupt:
            return None


def select_multiple(choices: List[str], prompt: str = "Select items:") -> List[str]:
    """
    Select multiple items from a list.

    Args:
        choices: List of items to choose from
        prompt: Prompt message

    Returns:
        List of selected items (empty if cancelled)
    """
    if QUESTIONARY_AVAILABLE:
        try:
            return questionary.checkbox(
                prompt,
                choices=choices,
                style=custom_style
            ).ask() or []
        except KeyboardInterrupt:
            return []
    else:
        print(f"\n{prompt}")
        print("Enter comma-separated numbers (e.g., 1,3,5):")
        for i, choice in enumerate(choices, 1):
            print(f"  {i}. {choice}")

        try:
            response = input("\nSelection: ").strip()
            if not response:
                return []

            indices = [int(x.strip()) - 1 for x in response.split(',')]
            return [choices[i] for i in indices if 0 <= i < len(choices)]
        except (ValueError, KeyboardInterrupt):
            return []


if __name__ == "__main__":
    # Test the interactive functions
    print("Interactive Menu Test")
    print("=" * 40)

    # Test shortcut selection
    test_shortcuts = ["Test 1", "Test 2", "Test 3"]
    selected = select_shortcut(test_shortcuts)
    print(f"Selected shortcut: {selected}")

    # Test confirmation
    confirmed = confirm_action("Continue with test?")
    print(f"Confirmed: {confirmed}")

    # Test text input
    name = text_input("Enter a name", "Default Name")
    print(f"Name entered: {name}")

    # Test signing mode
    mode = select_signing_mode()
    print(f"Signing mode: {mode}")
