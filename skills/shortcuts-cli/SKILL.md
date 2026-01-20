---
name: shortcuts-cli
description: "Use this skill when the user asks about Mac Shortcuts, managing shortcuts, running shortcuts, creating shortcuts, the shortcuts CLI, workflow automation, or .shortcut files. Trigger phrases: 'mac shortcuts', 'shortcuts cli', 'manage shortcuts', 'run shortcut', 'create shortcut', 'build workflow', 'parse shortcut file', 'shortcut automation'."
---

# Mac Shortcuts Plugin - Skill Documentation

This skill provides comprehensive management of Mac Shortcuts through CLI integration, .shortcut file manipulation, and programmatic workflow building.

## Overview

The Mac Shortcuts plugin enables you to:

1. **Manage Shortcuts via CLI**: List, run, view, and sign shortcuts
2. **Parse .shortcut Files**: Extract and analyze shortcut structure
3. **Create Shortcuts**: Build new shortcuts from templates
4. **Build Workflows**: Programmatically construct complex workflows using Python DSL

## Available Commands

### Native CLI Commands

#### `/mac-shortcuts:list`
List all available shortcuts with optional filtering.

**Usage:**
```bash
/mac-shortcuts:list [--folders] [--show-identifiers] [--folder-name <name>]
```

**Features:**
- Displays shortcuts in formatted tables with colors
- Can list folders or shortcuts in specific folders
- Shows identifiers (UUIDs) when requested
- Results are cached for performance

**Examples:**
```bash
# List all shortcuts
/mac-shortcuts:list

# List folders
/mac-shortcuts:list --folders

# List shortcuts with identifiers
/mac-shortcuts:list --show-identifiers
```

---

#### `/mac-shortcuts:run`
Execute a shortcut by name.

**Usage:**
```bash
/mac-shortcuts:run <shortcut-name> [--input-path <path>] [--output-path <path>]
```

**Features:**
- Runs any installed shortcut
- Supports input files
- Can save output to files
- Captures and displays results

**Examples:**
```bash
# Run a simple shortcut
/mac-shortcuts:run "My Shortcut"

# Run with input file
/mac-shortcuts:run "Process Image" --input-path ~/photo.jpg

# Run and save output
/mac-shortcuts:run "Generate PDF" --output-path ~/report.pdf
```

---

#### `/mac-shortcuts:view`
Open a shortcut in the Shortcuts app.

**Usage:**
```bash
/mac-shortcuts:view <shortcut-name>
```

**Features:**
- Opens Shortcuts app to the specified shortcut
- Useful for viewing or editing shortcuts

**Example:**
```bash
/mac-shortcuts:view "My Shortcut"
```

---

#### `/mac-shortcuts:sign`
Sign a .shortcut file for sharing.

**Usage:**
```bash
/mac-shortcuts:sign --input <file> --output <file> [--mode <mode>]
```

**Modes:**
- `people-who-know-me` (default): Only you and contacts can run it
- `anyone`: Anyone can run the shortcut

**Examples:**
```bash
# Sign with default mode
/mac-shortcuts:sign --input my.shortcut --output my-signed.shortcut

# Sign for anyone
/mac-shortcuts:sign --input my.shortcut --output my-signed.shortcut --mode anyone
```

---

### .shortcut File Commands

#### `/mac-shortcuts:parse`
Parse and analyze .shortcut files.

**Usage:**
```bash
/mac-shortcuts:parse <file-path> [--json] [--actions-only] [--metadata-only]
```

**What Gets Parsed:**
- Workflow actions and their parameters
- Metadata (version, icon, types)
- Variable references
- Action identifiers

**Features:**
- Supports binary and XML plist formats
- JSON output for programmatic use
- Readable formatted output
- Extracts icons, colors, and configuration

**Examples:**
```bash
# Parse entire shortcut
/mac-shortcuts:parse ~/Downloads/MyShortcut.shortcut

# Show only actions
/mac-shortcuts:parse ~/Downloads/MyShortcut.shortcut --actions-only

# Get JSON output
/mac-shortcuts:parse ~/Downloads/MyShortcut.shortcut --json
```

---

#### `/mac-shortcuts:create`
Create new .shortcut files from templates.

**Usage:**
```bash
/mac-shortcuts:create [--template <type>] [--output <path>] [--interactive]
```

**Templates:**
- `text`: Simple text output shortcut
- `notification`: System notification shortcut
- `script`: Shell script runner shortcut
- `url`: URL opener shortcut

**Features:**
- Interactive mode with prompts
- Template-based creation
- Customizable configuration
- Ready to import to Shortcuts app

**Examples:**
```bash
# Interactive creation
/mac-shortcuts:create --interactive

# Create from template
/mac-shortcuts:create --template notification --output notify.shortcut
```

---

### Workflow Builder

#### `/mac-shortcuts:build`
Build complex workflows programmatically.

**Usage:**
```bash
/mac-shortcuts:build [--interactive] [--output <path>]
```

**Available Actions:**
- Text actions (display, manipulate text)
- Notifications (show system notifications)
- Shell scripts (execute bash commands)
- Clipboard operations (get/set)
- Variables (store and retrieve values)
- URLs (define and open)
- Control flow (conditionals, loops)
- Comments (document workflows)

**Features:**
- Interactive step-by-step builder
- Python DSL for advanced users
- Action chaining
- Variable passing between actions
- Icon customization

**Example Workflows:**

**Simple Text to Notification:**
```bash
/mac-shortcuts:build --interactive
# 1. Add Text: "Hello World"
# 2. Add Notification
# 3. Save
```

**Clipboard to Notification:**
```bash
/mac-shortcuts:build --interactive
# 1. Get Clipboard
# 2. Add Notification with clipboard content
# 3. Save
```

**Script Runner:**
```bash
/mac-shortcuts:build --interactive
# 1. Add Shell Script: "date"
# 2. Add Notification with result
# 3. Save
```

---

## Python Scripts

The plugin includes Python helper scripts in `skills/shortcuts-cli/scripts/`:

### Core Utilities (`shortcut_utils.py`)
- Shortcut list caching (5-minute TTL)
- Validation functions
- Path resolution
- Error handling
- Shortcut execution wrapper

### Parser (`parse_shortcuts.py`)
- Parse `shortcuts list` output
- Organize by folders
- Extract identifiers
- JSON conversion

### Formatter (`format_output.py`)
- Colored terminal output (using `rich`)
- Table formatting
- Fallback to basic formatting
- Success/error message formatting

### Interactive Menu (`interactive_menu.py`)
- Interactive shortcut selection (using `questionary`)
- File path prompts
- Confirmation dialogs
- Multi-select options
- Fallback to basic input() prompts

### Plist Parser (`plist_parser.py`)
- Parse .shortcut property list files
- Extract actions and metadata
- Create shortcut plist structures
- Validate shortcut format
- Write .shortcut files

### Workflow Builder (`workflow_builder.py`)
- Python DSL for building workflows
- Action classes (Text, Notification, Script, etc.)
- WorkflowBuilder class with chaining
- Convenience functions for common workflows
- Icon customization

---

## Shortcuts CLI Reference

The Mac Shortcuts CLI provides these native commands:

### `shortcuts list`
List your shortcuts.

**Options:**
- `--folder-name <name>`: List shortcuts in specific folder
- `--folders`: List folders instead of shortcuts
- `--show-identifiers`: Show shortcut UUIDs

### `shortcuts run`
Run a shortcut.

**Options:**
- `--input-path <path>`: Input file for shortcut
- `--output-path <path>`: Save output to file
- `--output-type <type>`: Output type (UTI format)

### `shortcuts view`
View a shortcut in Shortcuts app.

### `shortcuts sign`
Sign a shortcut file.

**Options:**
- `--input <file>`: Input .shortcut file
- `--output <file>`: Output signed file
- `--mode <mode>`: Signing mode (anyone, people-who-know-me)

---

## .shortcut File Format

.shortcut files are property lists (plists) with this structure:

**Root Keys:**
- `WFWorkflowActions`: Array of actions
- `WFWorkflowClientVersion`: Shortcuts app version
- `WFWorkflowClientRelease`: macOS version
- `WFWorkflowMinimumClientVersion`: Minimum required version
- `WFWorkflowMinimumClientRelease`: Minimum required macOS version
- `WFWorkflowIcon`: Icon configuration
- `WFWorkflowTypes`: Workflow types
- `WFWorkflowInputContentItemClasses`: Input types

**Action Structure:**
```json
{
  "WFWorkflowActionIdentifier": "is.workflow.actions.gettext",
  "WFWorkflowActionParameters": {
    "WFTextActionText": "Hello World",
    "UUID": "12345678-1234-1234-1234-123456789012"
  }
}
```

---

## Common Workflows

### List and Run a Shortcut
```bash
# List available shortcuts
/mac-shortcuts:list

# Run a shortcut
/mac-shortcuts:run "Shortcut Name"
```

### Create, Sign, and Import
```bash
# Create a new shortcut
/mac-shortcuts:create --template notification --output my.shortcut

# Sign it
/mac-shortcuts:sign --input my.shortcut --output my-signed.shortcut

# Import by double-clicking my-signed.shortcut
# Then run it
/mac-shortcuts:run "My Shortcut"
```

### Parse Existing Shortcut
```bash
# Export a shortcut from Shortcuts app as .shortcut file
# Then parse it
/mac-shortcuts:parse ~/Downloads/exported.shortcut

# View actions only
/mac-shortcuts:parse ~/Downloads/exported.shortcut --actions-only
```

### Build Complex Workflow
```bash
# Build interactively
/mac-shortcuts:build --interactive

# Follow prompts to add:
# 1. Get Clipboard
# 2. Set Variable "original"
# 3. Text action with transformation
# 4. Notification with result
# 5. Save to workflow.shortcut

# Sign and import
/mac-shortcuts:sign --input workflow.shortcut --output workflow-signed.shortcut
```

---

## Dependencies

**Required (stdlib):**
- `plistlib`, `json`, `pathlib`, `subprocess`, `datetime`, `uuid`

**Optional (enhanced features):**
- `rich`: Colored terminal output and tables
- `questionary`: Interactive menus

**Installation:**
```bash
cd skills/shortcuts-cli/scripts
uv pip install -r requirements.txt
```

---

## Caching

The plugin caches shortcuts lists for performance:

**Location:** `~/.cache/mac-shortcuts-plugin/shortcuts_cache.json`
**TTL:** 5 minutes
**Invalidation:** On create/delete operations

**Clear cache:**
```bash
cd skills/shortcuts-cli/scripts
uv run python3 shortcut_utils.py clear-cache
```

---

## Troubleshooting

### Shortcut not found
- Check spelling (names are case-sensitive)
- List all shortcuts: `/mac-shortcuts:list`
- Verify shortcut is installed in Shortcuts app

### Permission denied
- Ensure Shortcuts app has necessary permissions
- Check file permissions for .shortcut files
- Try signing the shortcut file

### Invalid .shortcut file
- Validate with: `uv run python3 plist_parser.py validate file.shortcut`
- Re-export from Shortcuts app
- Check file is not corrupted

### Dependencies missing
- Install: `uv pip install -r requirements.txt`
- Commands fall back to basic features if dependencies are missing

---

## Advanced Usage

### Python DSL Example

```python
from workflow_builder import WorkflowBuilder

# Create workflow
builder = WorkflowBuilder("Clipboard Processor")

# Add actions
builder.add_clipboard('Get')
builder.add_variable('original', set_value=True)
builder.add_text("Processed: ")
builder.add_variable('original', set_value=False)
builder.add_notification("{{result}}", "Processing Complete")

# Customize icon
builder.set_icon(glyph_number=59511, color=4282601983)

# Save
builder.save("clipboard_processor.shortcut")
```

### Batch Operations

```bash
# List all shortcuts and save to file
/mac-shortcuts:list > shortcuts.txt

# Run multiple shortcuts in sequence
for name in "Shortcut 1" "Shortcut 2" "Shortcut 3"; do
  /mac-shortcuts:run "$name"
done
```

---

## Resources

**Documentation:**
- `docs/shortcuts-cli-reference.md`: Full CLI reference
- `docs/shortcut-file-format.md`: .shortcut file format details
- `docs/workflow-builder-guide.md`: Workflow builder tutorial

**Scripts:**
- All Python scripts in `skills/shortcuts-cli/scripts/`
- Each script has CLI interface for direct use

**Apple Documentation:**
- [Shortcuts User Guide](https://support.apple.com/guide/shortcuts/)
- [Shortcuts Gallery](https://support.apple.com/en-us/HT208309)

---

## Version

Plugin Version: 1.0.0
macOS: Compatible with macOS 12.0+ (Monterey and later)
