---
description: "Open a shortcut in the Shortcuts app"
argument-hint: "<shortcut-name>"
allowed-tools: ["Bash(shortcuts view:*)", "Bash(uv run:*)"]
---

# View Mac Shortcut

Open a shortcut in the Shortcuts app for viewing or editing.

## Usage

```bash
/mac-shortcuts:view <shortcut-name>
```

## Arguments

- `<shortcut-name>`: Name of the shortcut to view (required)

## Examples

```bash
# View a shortcut
/mac-shortcuts:view "My Shortcut"

# View a shortcut with spaces in name
/mac-shortcuts:view "Text Last Image"
```

## Implementation

Open the shortcut in Shortcuts app:
!`shortcuts view "$1"`

## Notes

- This opens the Shortcuts app and navigates to the specified shortcut
- Shortcut names are case-sensitive
- If the shortcut doesn't exist, an error will be shown
- The Shortcuts app must be installed (it's built into macOS)
