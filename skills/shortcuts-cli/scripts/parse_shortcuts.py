#!/usr/bin/env python3
"""
Mac Shortcuts Plugin - Shortcuts List Parser

Parses output from 'shortcuts list' command into structured data.
"""

import json
import subprocess
import sys
from typing import List, Dict, Any, Optional


def parse_list_output(output: str, show_identifiers: bool = False) -> List[Dict[str, str]]:
    """
    Parse shortcuts list output into structured data.

    Args:
        output: Raw output from 'shortcuts list' command
        show_identifiers: Whether the output includes identifiers

    Returns:
        List of dictionaries with shortcut info
    """
    shortcuts = []
    lines = [line.strip() for line in output.strip().split('\n') if line.strip()]

    for line in lines:
        if show_identifiers:
            # Format: "Name (Identifier: UUID)"
            if ' (Identifier: ' in line:
                name, identifier_part = line.split(' (Identifier: ', 1)
                identifier = identifier_part.rstrip(')')
                shortcuts.append({
                    'name': name.strip(),
                    'identifier': identifier.strip()
                })
            else:
                # Fallback if format is different
                shortcuts.append({'name': line, 'identifier': ''})
        else:
            shortcuts.append({'name': line})

    return shortcuts


def parse_folders_output(output: str, show_identifiers: bool = False) -> List[Dict[str, str]]:
    """
    Parse shortcuts folders list output.

    Args:
        output: Raw output from 'shortcuts list --folders' command
        show_identifiers: Whether the output includes identifiers

    Returns:
        List of dictionaries with folder info
    """
    # Same parsing logic as regular shortcuts
    return parse_list_output(output, show_identifiers)


def get_shortcuts_by_folder(folder_name: Optional[str] = None) -> List[Dict[str, str]]:
    """
    Get shortcuts organized by folder.

    Args:
        folder_name: Specific folder to filter by, or None for all

    Returns:
        List of shortcuts with folder information
    """
    cmd = ['shortcuts', 'list']

    if folder_name:
        cmd.extend(['--folder-name', folder_name])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        shortcuts = parse_list_output(result.stdout)

        # Add folder information
        for shortcut in shortcuts:
            shortcut['folder'] = folder_name if folder_name else 'none'

        return shortcuts
    except subprocess.CalledProcessError as e:
        print(f"Error getting shortcuts: {e.stderr}", file=sys.stderr)
        return []


def get_all_shortcuts_with_folders() -> Dict[str, List[Dict[str, str]]]:
    """
    Get all shortcuts organized by their folders.

    Returns:
        Dictionary mapping folder names to lists of shortcuts
    """
    organized = {}

    # Get all folders first
    try:
        result = subprocess.run(['shortcuts', 'list', '--folders'],
                               capture_output=True, text=True, check=True)
        folders = parse_folders_output(result.stdout)

        # Get shortcuts in each folder
        for folder_info in folders:
            folder_name = folder_info['name']
            organized[folder_name] = get_shortcuts_by_folder(folder_name)

        # Get shortcuts not in any folder
        organized['No Folder'] = get_shortcuts_by_folder('none')

    except subprocess.CalledProcessError as e:
        print(f"Error organizing shortcuts: {e.stderr}", file=sys.stderr)

    return organized


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Parse shortcuts list output")
    parser.add_argument('--input', help='Input text to parse (default: run shortcuts list)')
    parser.add_argument('--show-identifiers', action='store_true',
                       help='Parse output with identifiers')
    parser.add_argument('--folders', action='store_true',
                       help='Parse folders output')
    parser.add_argument('--organize-by-folder', action='store_true',
                       help='Organize all shortcuts by folder')
    parser.add_argument('--json', action='store_true',
                       help='Output as JSON')

    args = parser.parse_args()

    try:
        if args.organize_by_folder:
            organized = get_all_shortcuts_with_folders()
            if args.json:
                print(json.dumps(organized, indent=2))
            else:
                for folder, shortcuts in organized.items():
                    print(f"\n{folder}:")
                    for shortcut in shortcuts:
                        print(f"  - {shortcut['name']}")

        elif args.input:
            # Parse provided input
            if args.folders:
                result = parse_folders_output(args.input, args.show_identifiers)
            else:
                result = parse_list_output(args.input, args.show_identifiers)

            if args.json:
                print(json.dumps(result, indent=2))
            else:
                for item in result:
                    if 'identifier' in item and item['identifier']:
                        print(f"{item['name']} (ID: {item['identifier']})")
                    else:
                        print(item['name'])

        else:
            # Run shortcuts list and parse
            cmd = ['shortcuts', 'list']
            if args.folders:
                cmd.append('--folders')
            if args.show_identifiers:
                cmd.append('--show-identifiers')

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            if args.folders:
                parsed = parse_folders_output(result.stdout, args.show_identifiers)
            else:
                parsed = parse_list_output(result.stdout, args.show_identifiers)

            if args.json:
                print(json.dumps(parsed, indent=2))
            else:
                for item in parsed:
                    if 'identifier' in item and item['identifier']:
                        print(f"{item['name']} (ID: {item['identifier']})")
                    else:
                        print(item['name'])

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
