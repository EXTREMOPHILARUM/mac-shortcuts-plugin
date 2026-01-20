---
description: "Sign a .shortcut file with specified signing mode"
argument-hint: "--input <file> --output <file> [--mode <mode>]"
allowed-tools: ["Bash(shortcuts sign:*)", "Read"]
---

# Sign Shortcut File

Sign a .shortcut file to make it shareable with others.

## Usage

```bash
/mac-shortcuts:sign --input <input-file> --output <output-file> [--mode <mode>]
```

## Options

- `--input <file>`: Path to the unsigned .shortcut file (required)
- `--output <file>`: Path for the signed output file (required)
- `--mode <mode>`: Signing mode (optional, default: `people-who-know-me`)
  - `people-who-know-me`: Only you and people in your contacts can run it
  - `anyone`: Anyone can run the shortcut

## Examples

```bash
# Sign a shortcut with default mode
/mac-shortcuts:sign --input MyShortcut.shortcut --output MyShortcut-signed.shortcut

# Sign for anyone
/mac-shortcuts:sign --input MyShortcut.shortcut --output MyShortcut-signed.shortcut --mode anyone

# Sign for contacts only
/mac-shortcuts:sign --input MyShortcut.shortcut --output MyShortcut-signed.shortcut --mode people-who-know-me
```

## Implementation

Sign the shortcut file:
!`shortcuts sign $ARGUMENTS`

## Notes

- Input file must be a valid .shortcut file
- Output file will be created (overwrites if exists)
- Signed shortcuts can be shared via AirDrop, Messages, or other methods
- The signing mode affects who can run the shortcut
- Default mode (`people-who-know-me`) provides better security
