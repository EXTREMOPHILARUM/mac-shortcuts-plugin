# Mac Shortcuts CLI Reference

Complete reference for the Mac Shortcuts command-line interface.

## Overview

The `shortcuts` command-line tool is built into macOS (Monterey 12.0+) and provides access to the Shortcuts app functionality from the terminal.

## Installation

The `shortcuts` command is pre-installed on macOS 12.0 (Monterey) and later. No installation required.

**Verify installation:**
```bash
which shortcuts
# Output: /usr/bin/shortcuts

shortcuts --help
```

## Commands

### `shortcuts list`

List your shortcuts with optional filtering.

**Syntax:**
```bash
shortcuts list [OPTIONS]
```

**Options:**
- `-f, --folder-name <name>`: List shortcuts in a specific folder, or "none" for shortcuts not in any folder
- `--folders`: List folders instead of shortcuts
- `--show-identifiers`: Show shortcut UUIDs with each result
- `-h, --help`: Show help information

**Examples:**
```bash
# List all shortcuts
shortcuts list

# List shortcuts in "Work" folder
shortcuts list --folder-name "Work"

# List shortcuts not in any folder
shortcuts list --folder-name none

# List all folders
shortcuts list --folders

# List shortcuts with their UUIDs
shortcuts list --show-identifiers
```

**Output Format:**
```
Shortcut Name 1
Shortcut Name 2
Shortcut Name 3
```

**With identifiers:**
```
Shortcut Name 1 (Identifier: 12345678-1234-1234-1234-123456789012)
Shortcut Name 2 (Identifier: 87654321-4321-4321-4321-210987654321)
```

---

### `shortcuts run`

Execute a shortcut by name or identifier.

**Syntax:**
```bash
shortcuts run <shortcut-name-or-identifier> [OPTIONS]
```

**Arguments:**
- `<shortcut-name-or-identifier>`: Name or UUID of the shortcut to run (required)

**Options:**
- `-i, --input-path <path>`: Provide input file(s) to the shortcut (can be specified multiple times)
- `-o, --output-path <path>`: Save shortcut output to file
- `--output-type <type>`: Specify output type in Universal Type Identifier (UTI) format
- `-h, --help`: Show help information

**Examples:**
```bash
# Run a simple shortcut
shortcuts run "My Shortcut"

# Run with UUID
shortcuts run 12345678-1234-1234-1234-123456789012

# Run with input file
shortcuts run "Process Image" --input-path ~/Desktop/photo.jpg

# Run with multiple inputs
shortcuts run "Combine PDFs" \
  --input-path file1.pdf \
  --input-path file2.pdf \
  --input-path file3.pdf

# Run and save output
shortcuts run "Generate Report" --output-path ~/Desktop/report.pdf

# Run with specific output type
shortcuts run "Convert to Text" \
  --input-path document.pdf \
  --output-type public.plain-text

# Run and pipe output
shortcuts run "Get System Info" | grep "macOS"
```

**Universal Type Identifiers (UTI):**
Common UTI values for `--output-type`:
- `public.plain-text`: Plain text (.txt)
- `public.html`: HTML (.html)
- `public.json`: JSON data
- `public.xml`: XML data
- `com.adobe.pdf`: PDF documents
- `public.jpeg`: JPEG images
- `public.png`: PNG images
- `public.mp3`: MP3 audio
- `public.mpeg-4`: MP4 video

**Return Values:**
- `0`: Success
- Non-zero: Error (with error message to stderr)

---

### `shortcuts view`

Open a shortcut in the Shortcuts app.

**Syntax:**
```bash
shortcuts view <shortcut-name>
```

**Arguments:**
- `<shortcut-name>`: Name of the shortcut to view (required)

**Options:**
- `-h, --help`: Show help information

**Examples:**
```bash
# View a shortcut
shortcuts view "My Shortcut"

# View and edit
shortcuts view "Complex Workflow"
```

**Behavior:**
- Opens the Shortcuts app
- Navigates to the specified shortcut
- Shortcut can be viewed and edited
- If shortcut doesn't exist, shows error

---

### `shortcuts sign`

Sign a shortcut file for sharing.

**Syntax:**
```bash
shortcuts sign [OPTIONS] --input <input> --output <output>
```

**Options:**
- `-m, --mode <mode>`: Signing mode (default: `people-who-know-me`)
  - `anyone`: Anyone can run the shortcut
  - `people-who-know-me`: Only you and your contacts can run it
- `-i, --input <file>`: Input .shortcut file to sign (required)
- `-o, --output <file>`: Output path for signed file (required)
- `-h, --help`: Show help information

**Examples:**
```bash
# Sign with default mode (people-who-know-me)
shortcuts sign \
  --input MyShortcut.shortcut \
  --output MyShortcut-signed.shortcut

# Sign for anyone
shortcuts sign \
  --mode anyone \
  --input MyShortcut.shortcut \
  --output MyShortcut-public.shortcut

# Sign for contacts only (explicit)
shortcuts sign \
  --mode people-who-know-me \
  --input MyShortcut.shortcut \
  --output MyShortcut-private.shortcut
```

**Signing Modes:**

**`people-who-know-me` (default):**
- More secure
- Only you and people in your Contacts can run it
- Recommended for personal shortcuts
- Better privacy protection

**`anyone`:**
- Less secure
- Anyone can run the shortcut
- Use for public sharing
- Good for shortcuts without sensitive data

**File Format:**
- Input: `.shortcut` file (property list)
- Output: Signed `.shortcut` file
- Can sign both new and old format shortcuts

---

## Common Use Cases

### List and Select

```bash
# List all shortcuts
shortcuts list

# List shortcuts in a folder
shortcuts list --folder-name "Productivity"

# Get shortcuts with IDs
shortcuts list --show-identifiers
```

### Run with Different Inputs

```bash
# Text input via echo
echo "Hello World" | shortcuts run "Process Text"

# File input
shortcuts run "Image Resize" --input-path photo.jpg

# Multiple files
shortcuts run "Merge PDFs" \
  --input-path doc1.pdf \
  --input-path doc2.pdf \
  --input-path doc3.pdf

# With output
shortcuts run "Screenshot to PDF" \
  --input-path screenshot.png \
  --output-path result.pdf \
  --output-type com.adobe.pdf
```

### Automation Scripts

```bash
#!/bin/bash
# Run multiple shortcuts in sequence

shortcuts run "Morning Routine"
shortcuts run "Check Calendar"
shortcuts run "Get Weather"
shortcuts run "Daily Summary"
```

### Export and Sign

```bash
# Export shortcut from Shortcuts app as .shortcut file
# Then sign it for sharing

shortcuts sign \
  --input exported.shortcut \
  --output shared.shortcut \
  --mode anyone

# Share via AirDrop, email, or other methods
```

---

## Error Handling

**Shortcut not found:**
```
Error: Shortcut "Name" not found
```
Solution: Check spelling, list shortcuts to verify name

**Permission denied:**
```
Error: Operation not permitted
```
Solution: Grant Shortcuts app permissions in System Preferences

**Invalid input file:**
```
Error: Input file not found
```
Solution: Verify file path exists, use absolute paths

**Invalid .shortcut file:**
```
Error: Unable to read shortcut file
```
Solution: Ensure file is valid .shortcut format, re-export from Shortcuts app

---

## Shortcuts App Integration

### Importing .shortcut Files

**Methods:**
1. Double-click .shortcut file
2. Drag to Shortcuts app
3. File > Import in Shortcuts app
4. Open with Shortcuts app

**Signed vs. Unsigned:**
- Signed: Can be shared with others
- Unsigned: Only works for creator
- Sign before sharing

### Exporting Shortcuts

1. Open Shortcuts app
2. Right-click shortcut
3. Select "Export..."
4. Save as .shortcut file
5. Sign if sharing: `shortcuts sign --input ... --output ...`

---

## Scripting Best Practices

### Error Handling

```bash
#!/bin/bash

# Check if shortcut exists
if shortcuts list | grep -q "My Shortcut"; then
  shortcuts run "My Shortcut"
else
  echo "Error: Shortcut not found" >&2
  exit 1
fi
```

### Input Validation

```bash
#!/bin/bash

input_file="$1"

if [ ! -f "$input_file" ]; then
  echo "Error: Input file does not exist" >&2
  exit 1
fi

shortcuts run "Process File" --input-path "$input_file"
```

### Output Capture

```bash
#!/bin/bash

# Capture output to variable
result=$(shortcuts run "Get System Info")

# Process output
echo "$result" | grep "macOS"

# Save to file
shortcuts run "Generate Report" --output-path report.txt
```

---

## Environment Variables

The shortcuts command doesn't use special environment variables, but you can use standard shell variables:

```bash
# Define shortcut name
SHORTCUT="My Shortcut"
shortcuts run "$SHORTCUT"

# Define paths
INPUT_DIR="$HOME/Documents"
OUTPUT_DIR="$HOME/Desktop"

shortcuts run "Process Files" \
  --input-path "$INPUT_DIR/file.txt" \
  --output-path "$OUTPUT_DIR/result.txt"
```

---

## Limitations

**CLI Limitations:**
- Cannot create new shortcuts (use Shortcuts app or Python builder)
- Cannot modify existing shortcuts (use Shortcuts app)
- Cannot delete shortcuts
- Cannot organize into folders
- Limited to installed shortcuts

**Workarounds:**
- Use `/mac-shortcuts:build` to create shortcuts programmatically
- Use `/mac-shortcuts:parse` to analyze shortcuts
- Use Shortcuts app for visual editing

---

## Related Commands

**macOS Automation:**
- `osascript`: Run AppleScript and JavaScript
- `automator`: Run Automator workflows
- `say`: Text-to-speech
- `afplay`: Play audio files

**Integration Examples:**
```bash
# Combine with osascript
osascript -e 'tell application "Finder" to get name of front window'
shortcuts run "Process Window Name"

# Combine with system commands
date | shortcuts run "Log Time"

# Pipe to other commands
shortcuts run "Get Data" | jq '.'
```

---

## Resources

**Official Documentation:**
- [Shortcuts User Guide](https://support.apple.com/guide/shortcuts/)
- [UTI Reference](https://developer.apple.com/library/archive/documentation/Miscellaneous/Reference/UTIRef/)

**Plugin Commands:**
- `/mac-shortcuts:list`: Enhanced list with formatting
- `/mac-shortcuts:run`: Enhanced run with validation
- `/mac-shortcuts:build`: Create shortcuts programmatically

**Help:**
```bash
shortcuts --help
shortcuts help list
shortcuts help run
shortcuts help view
shortcuts help sign
```
