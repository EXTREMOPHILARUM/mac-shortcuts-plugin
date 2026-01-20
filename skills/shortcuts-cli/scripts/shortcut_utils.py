#!/usr/bin/env python3
"""
Mac Shortcuts Plugin - Core Utilities

Provides caching, validation, and common helper functions for shortcuts operations.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta


class ShortcutCache:
    """Manages caching of shortcuts list with TTL."""

    def __init__(self, cache_dir: Optional[Path] = None, ttl_minutes: int = 5):
        """
        Initialize cache manager.

        Args:
            cache_dir: Directory for cache files (default: ~/.cache/mac-shortcuts-plugin)
            ttl_minutes: Time-to-live for cache in minutes (default: 5)
        """
        if cache_dir is None:
            cache_dir = Path.home() / ".cache" / "mac-shortcuts-plugin"

        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "shortcuts_cache.json"
        self.ttl = timedelta(minutes=ttl_minutes)

    def get(self) -> Optional[List[str]]:
        """
        Retrieve cached shortcuts list if valid.

        Returns:
            List of shortcuts or None if cache is invalid/expired
        """
        if not self.cache_file.exists():
            return None

        try:
            with open(self.cache_file, 'r') as f:
                data = json.load(f)

            cached_time = datetime.fromisoformat(data['timestamp'])
            if datetime.now() - cached_time > self.ttl:
                return None

            return data['shortcuts']
        except (json.JSONDecodeError, KeyError, ValueError):
            return None

    def set(self, shortcuts: List[str]) -> None:
        """
        Cache shortcuts list with current timestamp.

        Args:
            shortcuts: List of shortcut names to cache
        """
        data = {
            'timestamp': datetime.now().isoformat(),
            'shortcuts': shortcuts
        }

        with open(self.cache_file, 'w') as f:
            json.dump(data, f, indent=2)

    def clear(self) -> None:
        """Clear the cache file."""
        if self.cache_file.exists():
            self.cache_file.unlink()


def get_shortcut_list(use_cache: bool = True, show_identifiers: bool = False) -> List[str]:
    """
    Get list of all shortcuts, optionally using cache.

    Args:
        use_cache: Whether to use cached results
        show_identifiers: Include shortcut identifiers in output

    Returns:
        List of shortcut names

    Raises:
        subprocess.CalledProcessError: If shortcuts command fails
    """
    cache = ShortcutCache()

    # Try cache first if enabled
    if use_cache:
        cached = cache.get()
        if cached is not None:
            return cached

    # Execute shortcuts list command
    cmd = ['shortcuts', 'list']
    if show_identifiers:
        cmd.append('--show-identifiers')

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        shortcuts = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]

        # Cache the results
        if use_cache:
            cache.set(shortcuts)

        return shortcuts
    except subprocess.CalledProcessError as e:
        print(f"Error running shortcuts command: {e.stderr}", file=sys.stderr)
        raise


def validate_shortcut_name(name: str, shortcuts_list: Optional[List[str]] = None) -> bool:
    """
    Validate if a shortcut name exists.

    Args:
        name: Shortcut name to validate
        shortcuts_list: Optional pre-fetched list of shortcuts

    Returns:
        True if shortcut exists, False otherwise
    """
    if shortcuts_list is None:
        shortcuts_list = get_shortcut_list(use_cache=True)

    return name in shortcuts_list


def resolve_path(path: str) -> Path:
    """
    Resolve a file path, expanding ~ and making it absolute.

    Args:
        path: Path string to resolve

    Returns:
        Resolved absolute Path object
    """
    return Path(path).expanduser().resolve()


def handle_shortcut_error(error: Exception, context: str = "") -> None:
    """
    Print standardized error messages.

    Args:
        error: The exception that occurred
        context: Additional context about what was being attempted
    """
    error_msg = f"Error"
    if context:
        error_msg += f" {context}"
    error_msg += f": {str(error)}"

    print(error_msg, file=sys.stderr)
    sys.exit(1)


def clear_cache() -> None:
    """Clear the shortcuts cache."""
    cache = ShortcutCache()
    cache.clear()
    print("Cache cleared successfully")


def run_shortcut(name: str, input_path: Optional[str] = None,
                 output_path: Optional[str] = None,
                 output_type: Optional[str] = None) -> str:
    """
    Execute a shortcut by name.

    Args:
        name: Name of the shortcut to run
        input_path: Optional path to input file
        output_path: Optional path to output file
        output_type: Optional output type (UTI format)

    Returns:
        Output from the shortcut

    Raises:
        subprocess.CalledProcessError: If shortcut execution fails
    """
    cmd = ['shortcuts', 'run', name]

    if input_path:
        cmd.extend(['--input-path', str(resolve_path(input_path))])

    if output_path:
        cmd.extend(['--output-path', str(resolve_path(output_path))])

    if output_type:
        cmd.extend(['--output-type', output_type])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running shortcut '{name}': {e.stderr}", file=sys.stderr)
        raise


if __name__ == "__main__":
    # CLI for testing utilities
    import argparse

    parser = argparse.ArgumentParser(description="Shortcut utilities")
    parser.add_argument('action', choices=['list', 'validate', 'clear-cache', 'run'],
                       help='Action to perform')
    parser.add_argument('--name', help='Shortcut name (for validate/run)')
    parser.add_argument('--no-cache', action='store_true', help='Bypass cache')
    parser.add_argument('--input', help='Input path (for run)')
    parser.add_argument('--output', help='Output path (for run)')

    args = parser.parse_args()

    try:
        if args.action == 'list':
            shortcuts = get_shortcut_list(use_cache=not args.no_cache)
            for s in shortcuts:
                print(s)

        elif args.action == 'validate':
            if not args.name:
                print("Error: --name required for validate", file=sys.stderr)
                sys.exit(1)

            is_valid = validate_shortcut_name(args.name)
            print(f"Valid: {is_valid}")
            sys.exit(0 if is_valid else 1)

        elif args.action == 'clear-cache':
            clear_cache()

        elif args.action == 'run':
            if not args.name:
                print("Error: --name required for run", file=sys.stderr)
                sys.exit(1)

            output = run_shortcut(args.name, args.input, args.output)
            if output:
                print(output)

    except Exception as e:
        handle_shortcut_error(e, f"during {args.action}")
