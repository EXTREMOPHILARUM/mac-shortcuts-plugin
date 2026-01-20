#!/usr/bin/env python3
"""
Mac Shortcuts Plugin - Property List Parser

Parses and creates .shortcut files (which are property list files).
"""

import plistlib
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional


def parse_shortcut_file(file_path: str) -> Dict[str, Any]:
    """
    Parse a .shortcut file into a dictionary.

    Args:
        file_path: Path to the .shortcut file

    Returns:
        Dictionary containing the shortcut data

    Raises:
        FileNotFoundError: If file doesn't exist
        plistlib.InvalidFileException: If file is not a valid plist
    """
    path = Path(file_path).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(f"Shortcut file not found: {path}")

    with open(path, 'rb') as f:
        return plistlib.load(f)


def extract_actions(shortcut_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract workflow actions from a shortcut dictionary.

    Args:
        shortcut_dict: Parsed shortcut dictionary

    Returns:
        List of action dictionaries
    """
    return shortcut_dict.get('WFWorkflowActions', [])


def get_metadata(shortcut_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract metadata from a shortcut dictionary.

    Args:
        shortcut_dict: Parsed shortcut dictionary

    Returns:
        Dictionary containing metadata
    """
    metadata = {
        'client_version': shortcut_dict.get('WFWorkflowClientVersion'),
        'client_release': shortcut_dict.get('WFWorkflowClientRelease'),
        'minimum_client_version': shortcut_dict.get('WFWorkflowMinimumClientVersion'),
        'minimum_client_release': shortcut_dict.get('WFWorkflowMinimumClientRelease'),
    }

    # Icon data if present
    if 'WFWorkflowIcon' in shortcut_dict:
        icon = shortcut_dict['WFWorkflowIcon']
        metadata['icon'] = {
            'start_color': icon.get('WFWorkflowIconStartColor'),
            'glyph_number': icon.get('WFWorkflowIconGlyphNumber'),
            'image_data': bool(icon.get('WFWorkflowIconImageData'))
        }

    # Input/output types
    if 'WFWorkflowInputContentItemClasses' in shortcut_dict:
        metadata['input_types'] = shortcut_dict['WFWorkflowInputContentItemClasses']

    if 'WFWorkflowTypes' in shortcut_dict:
        metadata['workflow_types'] = shortcut_dict['WFWorkflowTypes']

    # Import questions if present
    if 'WFWorkflowImportQuestions' in shortcut_dict:
        metadata['import_questions'] = shortcut_dict['WFWorkflowImportQuestions']

    return metadata


def format_action_readable(action: Dict[str, Any]) -> str:
    """
    Format a single action into a readable string.

    Args:
        action: Action dictionary

    Returns:
        Formatted action description
    """
    identifier = action.get('WFWorkflowActionIdentifier', 'Unknown')
    params = action.get('WFWorkflowActionParameters', {})

    # Extract action type from identifier
    action_type = identifier.split('.')[-1] if '.' in identifier else identifier

    # Build description based on action type
    description = f"• {action_type}"

    # Add relevant parameters
    if 'WFTextActionText' in params:
        text = params['WFTextActionText']
        if isinstance(text, dict):
            text = text.get('Value', str(text))
        description += f": \"{text}\""

    elif 'WFInput' in params:
        description += f": {params['WFInput']}"

    elif 'WFNotificationActionBody' in params:
        body = params['WFNotificationActionBody']
        description += f": \"{body}\""

    elif 'UUID' in params:
        description += f" (ID: {params['UUID'][:8]}...)"

    return description


def create_shortcut_plist(actions: List[Dict[str, Any]],
                          metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Create a shortcut property list dictionary from actions and metadata.

    Args:
        actions: List of action dictionaries
        metadata: Optional metadata dictionary

    Returns:
        Complete shortcut dictionary ready to be written as plist
    """
    shortcut = {
        'WFWorkflowActions': actions,
        'WFWorkflowClientVersion': metadata.get('client_version', '2690.0.2') if metadata else '2690.0.2',
        'WFWorkflowClientRelease': metadata.get('client_release', '17.0') if metadata else '17.0',
        'WFWorkflowMinimumClientVersion': metadata.get('minimum_client_version', 1113) if metadata else 1113,
        'WFWorkflowMinimumClientRelease': metadata.get('minimum_client_release', '15.0') if metadata else '15.0',
    }

    if metadata:
        # Add icon if present
        if 'icon' in metadata:
            shortcut['WFWorkflowIcon'] = {
                'WFWorkflowIconStartColor': metadata['icon'].get('start_color', 4282601983),
                'WFWorkflowIconGlyphNumber': metadata['icon'].get('glyph_number', 59511),
            }

        # Add input types if present
        if 'input_types' in metadata:
            shortcut['WFWorkflowInputContentItemClasses'] = metadata['input_types']

        # Add workflow types if present
        if 'workflow_types' in metadata:
            shortcut['WFWorkflowTypes'] = metadata['workflow_types']

    return shortcut


def write_shortcut_file(shortcut_dict: Dict[str, Any], file_path: str) -> None:
    """
    Write a shortcut dictionary to a .shortcut file.

    Args:
        shortcut_dict: Shortcut dictionary
        file_path: Path where to save the .shortcut file
    """
    path = Path(file_path).expanduser().resolve()

    # Ensure .shortcut extension
    if path.suffix != '.shortcut':
        path = path.with_suffix('.shortcut')

    with open(path, 'wb') as f:
        plistlib.dump(shortcut_dict, f, fmt=plistlib.FMT_BINARY)

    print(f"Shortcut saved to: {path}")


def validate_shortcut_structure(shortcut_dict: Dict[str, Any]) -> bool:
    """
    Validate that a dictionary has the proper structure for a shortcut.

    Args:
        shortcut_dict: Dictionary to validate

    Returns:
        True if valid, False otherwise
    """
    required_keys = [
        'WFWorkflowActions',
        'WFWorkflowClientVersion',
        'WFWorkflowMinimumClientVersion'
    ]

    for key in required_keys:
        if key not in shortcut_dict:
            print(f"Missing required key: {key}", file=sys.stderr)
            return False

    if not isinstance(shortcut_dict['WFWorkflowActions'], list):
        print("WFWorkflowActions must be a list", file=sys.stderr)
        return False

    return True


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Parse or create .shortcut files")
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Parse command
    parse_parser = subparsers.add_parser('parse', help='Parse a .shortcut file')
    parse_parser.add_argument('file', help='Path to .shortcut file')
    parse_parser.add_argument('--json', action='store_true', help='Output as JSON')
    parse_parser.add_argument('--actions-only', action='store_true', help='Show only actions')
    parse_parser.add_argument('--metadata-only', action='store_true', help='Show only metadata')

    # Create command
    create_parser = subparsers.add_parser('create', help='Create a .shortcut file')
    create_parser.add_argument('--output', required=True, help='Output file path')
    create_parser.add_argument('--actions', required=True, help='JSON file with actions')
    create_parser.add_argument('--metadata', help='JSON file with metadata')

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate a .shortcut file')
    validate_parser.add_argument('file', help='Path to .shortcut file')

    args = parser.parse_args()

    try:
        if args.command == 'parse':
            shortcut_data = parse_shortcut_file(args.file)

            if args.actions_only:
                actions = extract_actions(shortcut_data)
                if args.json:
                    print(json.dumps(actions, indent=2, default=str))
                else:
                    print(f"\nActions ({len(actions)} total):")
                    for i, action in enumerate(actions, 1):
                        print(f"{i}. {format_action_readable(action)}")

            elif args.metadata_only:
                metadata = get_metadata(shortcut_data)
                print(json.dumps(metadata, indent=2, default=str))

            else:
                # Show both
                metadata = get_metadata(shortcut_data)
                actions = extract_actions(shortcut_data)

                if args.json:
                    output = {
                        'metadata': metadata,
                        'actions': actions
                    }
                    print(json.dumps(output, indent=2, default=str))
                else:
                    print("\n=== Metadata ===")
                    print(json.dumps(metadata, indent=2, default=str))
                    print(f"\n=== Actions ({len(actions)} total) ===")
                    for i, action in enumerate(actions, 1):
                        print(f"{i}. {format_action_readable(action)}")

        elif args.command == 'create':
            # Load actions
            with open(args.actions, 'r') as f:
                actions = json.load(f)

            # Load metadata if provided
            metadata = None
            if args.metadata:
                with open(args.metadata, 'r') as f:
                    metadata = json.load(f)

            # Create shortcut
            shortcut_dict = create_shortcut_plist(actions, metadata)

            # Validate before writing
            if not validate_shortcut_structure(shortcut_dict):
                print("Invalid shortcut structure", file=sys.stderr)
                sys.exit(1)

            # Write file
            write_shortcut_file(shortcut_dict, args.output)

        elif args.command == 'validate':
            shortcut_data = parse_shortcut_file(args.file)
            if validate_shortcut_structure(shortcut_data):
                print("✓ Valid shortcut file")
            else:
                print("✗ Invalid shortcut file", file=sys.stderr)
                sys.exit(1)

        else:
            parser.print_help()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
