---
description: "List all Mac Shortcuts with optional filtering"
argument-hint: "[--folders] [--show-identifiers] [--folder-name <name>]"
allowed-tools: ["Bash(shortcuts list:*)", "Bash(uv run:*)", "Read"]
---

# List Mac Shortcuts

List all available Mac Shortcuts, optionally filtered by folder or showing identifiers.

## Usage

```bash
/mac-shortcuts:list [--folders] [--show-identifiers] [--folder-name <name>]
```

## Options

- `--folders`: List folders instead of shortcuts
- `--show-identifiers`: Show shortcut identifiers (UUIDs)
- `--folder-name <name>`: List shortcuts in a specific folder

## Examples

```bash
# List all shortcuts
/mac-shortcuts:list

# List all folders
/mac-shortcuts:list --folders

# List shortcuts with identifiers
/mac-shortcuts:list --show-identifiers

# List shortcuts in a specific folder
/mac-shortcuts:list --folder-name "Work"
```

## Implementation

The command uses Python scripts to parse and format the output with colors and tables.

Get the current list of shortcuts:
!`shortcuts list $ARGUMENTS`

Parse and format the output:
!`cd "${CLAUDE_PLUGIN_ROOT:-$(pwd)}/skills/shortcuts-cli/scripts" && uv run python3 parse_shortcuts.py --json | uv run python3 -c "import sys, json; from format_output import format_shortcuts; data = json.load(sys.stdin); format_shortcuts(data, show_identifiers='--show-identifiers' in sys.argv)"  $ARGUMENTS`

## Notes

- Results are cached for 5 minutes by default
- Use colored output when available (requires `rich` package)
- Fallback to basic formatting if dependencies are missing
