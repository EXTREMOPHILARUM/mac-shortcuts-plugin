---
description: "Parse a .shortcut file and display its contents"
argument-hint: "<file-path> [--json] [--actions-only] [--metadata-only]"
allowed-tools: ["Bash(uv run:*)", "Read"]
---

# Parse Shortcut File

Parse a .shortcut property list file and display its structure, actions, and metadata.

## Usage

```bash
/mac-shortcuts:parse <file-path> [--json] [--actions-only] [--metadata-only]
```

## Arguments

- `<file-path>`: Path to the .shortcut file (required)

## Options

- `--json`: Output as JSON format
- `--actions-only`: Show only workflow actions
- `--metadata-only`: Show only metadata

## Examples

```bash
# Parse and display full shortcut info
/mac-shortcuts:parse ~/Desktop/MyShortcut.shortcut

# Show only actions in JSON format
/mac-shortcuts:parse ~/Desktop/MyShortcut.shortcut --actions-only --json

# Show only metadata
/mac-shortcuts:parse ~/Desktop/MyShortcut.shortcut --metadata-only
```

## Implementation

Parse the .shortcut file using the plist parser:
!`cd "${CLAUDE_PLUGIN_ROOT:-$(pwd)}/skills/shortcuts-cli/scripts" && uv run python3 plist_parser.py parse $ARGUMENTS`

## What Gets Parsed

### Metadata
- Client version and release
- Minimum required version
- Icon configuration (color, glyph)
- Input/output types
- Import questions

### Actions
- Action identifiers (e.g., `is.workflow.actions.gettext`)
- Action parameters
- Variable references
- UUIDs for each action

## Output Format

**Default (readable):**
```
=== Metadata ===
{
  "client_version": "2690.0.2",
  "icon": {
    "start_color": 4282601983,
    "glyph_number": 59511
  }
}

=== Actions (3 total) ===
1. • gettext: "Hello World"
2. • notification: "Hello World"
3. • comment
```

**JSON:**
```json
{
  "metadata": {...},
  "actions": [...]
}
```

## Notes

- Supports both binary and XML property list formats
- Can parse any valid .shortcut file from macOS/iOS
- Use `--json` for programmatic processing
- Action details vary by action type
