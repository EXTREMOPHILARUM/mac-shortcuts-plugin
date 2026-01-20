---
description: "Execute a Mac Shortcut by name"
argument-hint: "<shortcut-name> [--input-path <path>] [--output-path <path>] [--output-type <type>]"
allowed-tools: ["Bash(shortcuts run:*)", "Bash(uv run:*)", "Read", "Write"]
---

# Run Mac Shortcut

Execute a Mac Shortcut by name with optional input/output options.

## Usage

```bash
/mac-shortcuts:run <shortcut-name> [--input-path <path>] [--output-path <path>] [--output-type <type>]
```

## Arguments

- `<shortcut-name>`: Name of the shortcut to run (required)

## Options

- `--input-path <path>`: Path to input file to pass to the shortcut
- `--output-path <path>`: Path where to save the shortcut output
- `--output-type <type>`: Output type in Universal Type Identifier format

## Examples

```bash
# Run a shortcut by name
/mac-shortcuts:run "My Shortcut"

# Run with input file
/mac-shortcuts:run "Process Image" --input-path ~/Desktop/photo.jpg

# Run with output file
/mac-shortcuts:run "Generate Report" --output-path ~/Desktop/report.pdf

# Run with specific output type
/mac-shortcuts:run "Convert Text" --output-type public.plain-text
```

## Implementation

Run the shortcut using the native CLI:
!`shortcuts run $ARGUMENTS`

Alternatively, use the Python utility for validation and error handling:
!`cd "${CLAUDE_PLUGIN_ROOT:-$(pwd)}/skills/shortcuts-cli/scripts" && uv run python3 shortcut_utils.py run $ARGUMENTS`

## Notes

- Shortcut names are case-sensitive
- Input/output paths are resolved to absolute paths
- Output is displayed in the terminal
- Use `--output-path` to save results to a file
