# Mac Shortcuts Plugin for Claude Code

Comprehensive Mac Shortcuts management through Claude Code: CLI integration, .shortcut file parsing, and programmatic workflow building.

## Features

- **Native CLI Commands**: List, run, view, and sign shortcuts via the Mac Shortcuts CLI
- **.shortcut File Manipulation**: Parse and create .shortcut property list files
- **Workflow Builder**: Build complex shortcuts programmatically using Python DSL
- **Interactive Menus**: User-friendly selection and configuration prompts
- **Colored Output**: Rich terminal formatting with tables and colors
- **Smart Caching**: Performance optimization with 5-minute TTL cache

## Installation

### Prerequisites

- macOS 12.0 (Monterey) or later
- Claude Code CLI
- Python 3.8+
- `uv` package manager

### Install Plugin

1. Clone or copy this plugin to your Claude plugins directory:
```bash
git clone <repo-url> ~/.claude/plugins/mac-shortcuts-plugin
```

2. Install Python dependencies (optional, for enhanced features):
```bash
cd ~/.claude/plugins/mac-shortcuts-plugin/skills/shortcuts-cli/scripts
uv pip install -r requirements.txt
```

**Optional Dependencies:**
- `rich`: Colored output and tables
- `questionary`: Interactive menus

The plugin will work without these but with reduced features (basic formatting, simple input prompts).

### Verify Installation

```bash
# Check if shortcuts CLI is available
which shortcuts

# List available shortcuts
shortcuts list

# Verify plugin loaded in Claude Code
# (Commands should appear as /mac-shortcuts:* )
```

## Quick Start

### List Shortcuts

```bash
# List all shortcuts
/mac-shortcuts:list

# List folders
/mac-shortcuts:list --folders

# List with identifiers
/mac-shortcuts:list --show-identifiers
```

### Run a Shortcut

```bash
# Run by name
/mac-shortcuts:run "My Shortcut"

# Run with input file
/mac-shortcuts:run "Process Image" --input-path ~/photo.jpg

# Run and save output
/mac-shortcuts:run "Generate Report" --output-path ~/report.pdf
```

### Create a Shortcut

```bash
# Interactive creation
/mac-shortcuts:create --interactive

# From template
/mac-shortcuts:create --template notification --output notify.shortcut
```

### Build a Workflow

```bash
# Interactive workflow builder
/mac-shortcuts:build --interactive

# Follow prompts to add actions, configure, and save
```

### Parse a .shortcut File

```bash
# Parse and display structure
/mac-shortcuts:parse ~/Downloads/MyShortcut.shortcut

# Show only actions
/mac-shortcuts:parse ~/Downloads/MyShortcut.shortcut --actions-only

# JSON output
/mac-shortcuts:parse ~/Downloads/MyShortcut.shortcut --json
```

### Sign a Shortcut

```bash
# Sign for contacts only (default)
/mac-shortcuts:sign --input my.shortcut --output my-signed.shortcut

# Sign for anyone
/mac-shortcuts:sign --input my.shortcut --output my-signed.shortcut --mode anyone
```

## Available Commands

| Command | Description |
|---------|-------------|
| `/mac-shortcuts:list` | List all shortcuts with filtering options |
| `/mac-shortcuts:run` | Execute a shortcut by name |
| `/mac-shortcuts:view` | Open shortcut in Shortcuts app |
| `/mac-shortcuts:sign` | Sign .shortcut files for sharing |
| `/mac-shortcuts:parse` | Parse and analyze .shortcut files |
| `/mac-shortcuts:create` | Create new shortcuts from templates |
| `/mac-shortcuts:build` | Build workflows programmatically |

## Usage Examples

### Example 1: Daily Automation

```bash
# List your morning routine shortcuts
/mac-shortcuts:list --folder-name "Morning"

# Run them in sequence
/mac-shortcuts:run "Check Calendar"
/mac-shortcuts:run "Get Weather"
/mac-shortcuts:run "Daily Summary"
```

### Example 2: Create and Share a Shortcut

```bash
# Build a new workflow
/mac-shortcuts:build --interactive
# Add actions: Text → "Hello World" → Notification

# Sign for sharing
/mac-shortcuts:sign --input workflow.shortcut --output workflow-signed.shortcut --mode anyone

# Share workflow-signed.shortcut via AirDrop, email, etc.
```

### Example 3: Analyze Existing Shortcut

```bash
# Export a shortcut from Shortcuts app as .shortcut file
# Then analyze it

# View full structure
/mac-shortcuts:parse ~/Downloads/complex.shortcut

# Extract just the actions
/mac-shortcuts:parse ~/Downloads/complex.shortcut --actions-only --json > actions.json

# Modify and rebuild
# (Use workflow_builder.py with the JSON data)
```

### Example 4: Programmatic Workflow Creation

```python
from workflow_builder import WorkflowBuilder

# Create builder
builder = WorkflowBuilder("System Info")

# Add actions
builder.add_script("uname -a")
builder.add_notification("{{result}}", "System Information")
builder.set_icon(glyph_number=59636, color=463140863)

# Save
builder.save("system_info.shortcut")
```

```bash
# Sign and import
/mac-shortcuts:sign --input system_info.shortcut --output system_info-signed.shortcut

# Double-click system_info-signed.shortcut to import

# Run it
/mac-shortcuts:run "System Info"
```

## Plugin Structure

```
mac-shortcuts-plugin/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── commands/
│   ├── list.md                  # List shortcuts command
│   ├── run.md                   # Run shortcut command
│   ├── view.md                  # View shortcut command
│   ├── sign.md                  # Sign shortcut command
│   ├── parse-shortcut.md        # Parse .shortcut file
│   ├── create-shortcut.md       # Create .shortcut file
│   └── build-workflow.md        # Build workflow command
├── skills/
│   └── shortcuts-cli/
│       ├── SKILL.md             # Main skill documentation
│       └── scripts/
│           ├── __init__.py
│           ├── requirements.txt
│           ├── shortcut_utils.py        # Core utilities + caching
│           ├── parse_shortcuts.py       # CLI output parser
│           ├── format_output.py         # Formatter with colors
│           ├── interactive_menu.py      # Interactive CLI
│           ├── plist_parser.py          # .shortcut file parser
│           └── workflow_builder.py      # Workflow DSL
├── docs/
│   ├── shortcuts-cli-reference.md       # Full CLI reference
│   ├── shortcut-file-format.md          # .shortcut format guide
│   └── workflow-builder-guide.md        # Workflow builder tutorial
├── README.md
└── LICENSE
```

## Python Scripts

All scripts are located in `skills/shortcuts-cli/scripts/` and can be used standalone:

### shortcut_utils.py

```bash
# List shortcuts (with caching)
uv run python3 shortcut_utils.py list

# Validate shortcut name
uv run python3 shortcut_utils.py validate --name "My Shortcut"

# Clear cache
uv run python3 shortcut_utils.py clear-cache

# Run shortcut
uv run python3 shortcut_utils.py run --name "My Shortcut"
```

### parse_shortcuts.py

```bash
# Parse shortcuts list
shortcuts list | uv run python3 parse_shortcuts.py --json

# Organize by folder
uv run python3 parse_shortcuts.py --organize-by-folder
```

### format_output.py

```bash
# Format JSON data
echo '[{"name": "Test"}]' | uv run python3 format_output.py --input -
```

### plist_parser.py

```bash
# Parse .shortcut file
uv run python3 plist_parser.py parse myfile.shortcut

# Show only actions
uv run python3 plist_parser.py parse myfile.shortcut --actions-only

# Validate structure
uv run python3 plist_parser.py validate myfile.shortcut
```

### workflow_builder.py

```bash
# Build simple workflow
uv run python3 workflow_builder.py \
  --type text \
  --content "Hello World" \
  --output hello.shortcut
```

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[shortcuts-cli-reference.md](docs/shortcuts-cli-reference.md)**: Complete Mac Shortcuts CLI reference
- **[shortcut-file-format.md](docs/shortcut-file-format.md)**: .shortcut property list format specification
- **[workflow-builder-guide.md](docs/workflow-builder-guide.md)**: Guide to building workflows with Python DSL

## Caching

The plugin caches shortcuts lists for performance:

- **Location**: `~/.cache/mac-shortcuts-plugin/shortcuts_cache.json`
- **TTL**: 5 minutes
- **Invalidation**: Automatic on create/delete operations

**Clear cache manually:**
```bash
cd skills/shortcuts-cli/scripts
uv run python3 shortcut_utils.py clear-cache
```

## Advanced Usage

### Batch Operations

```bash
# Run multiple shortcuts
for name in "Shortcut 1" "Shortcut 2" "Shortcut 3"; do
  /mac-shortcuts:run "$name"
done

# Sign multiple files
for file in *.shortcut; do
  /mac-shortcuts:sign --input "$file" --output "signed/$file"
done
```

### Python Integration

```python
from workflow_builder import WorkflowBuilder
from shortcut_utils import get_shortcut_list, run_shortcut

# List all shortcuts
shortcuts = get_shortcut_list()
print(f"Found {len(shortcuts)} shortcuts")

# Build workflow
builder = WorkflowBuilder("Auto Generated")
builder.add_text("Generated at runtime")
builder.add_notification("{{result}}")
builder.save("auto.shortcut")

# Run it after importing
run_shortcut("Auto Generated")
```

### Automation Scripts

```bash
#!/bin/bash
# daily_automation.sh

echo "Running daily automation..."

# Morning routine
/mac-shortcuts:run "Morning Routine"

# Backup important files
/mac-shortcuts:run "Backup Documents"

# Send summary
/mac-shortcuts:run "Daily Summary Email"

echo "Automation complete!"
```

Add to crontab:
```cron
# Run daily at 8 AM
0 8 * * * /path/to/daily_automation.sh
```

## Troubleshooting

### Command not found

**Problem**: `/mac-shortcuts:*` commands not available

**Solution**:
- Verify plugin is installed: `ls ~/.claude/plugins/mac-shortcuts-plugin`
- Restart Claude Code
- Check plugin.json syntax

### Permission denied

**Problem**: Cannot run shortcuts or access files

**Solution**:
- Grant Shortcuts app permissions in System Preferences
- Check file permissions: `ls -l file.shortcut`
- Ensure Python scripts are executable

### Shortcut not found

**Problem**: "Shortcut 'Name' not found"

**Solution**:
- List all shortcuts: `/mac-shortcuts:list`
- Check spelling (names are case-sensitive)
- Verify shortcut is installed in Shortcuts app

### Invalid .shortcut file

**Problem**: Cannot parse or import .shortcut file

**Solution**:
- Validate: `uv run python3 plist_parser.py validate file.shortcut`
- Re-export from Shortcuts app
- Check file isn't corrupted: `file file.shortcut`

### Dependencies missing

**Problem**: `ModuleNotFoundError: No module named 'rich'`

**Solution**:
```bash
cd skills/shortcuts-cli/scripts
uv pip install -r requirements.txt
```

**Note**: Commands fall back to basic features if dependencies missing

## Contributing

Contributions welcome! Areas for improvement:

- Additional action types in workflow builder
- More shortcut templates
- Enhanced error handling
- Additional utility scripts
- Documentation improvements

## License

See [LICENSE](LICENSE) file for details.

## Resources

**Official Apple Documentation:**
- [Shortcuts User Guide](https://support.apple.com/guide/shortcuts/)
- [Shortcuts Gallery](https://support.apple.com/en-us/HT208309)

**Plugin Documentation:**
- [CLI Reference](docs/shortcuts-cli-reference.md)
- [File Format Guide](docs/shortcut-file-format.md)
- [Workflow Builder Guide](docs/workflow-builder-guide.md)

**Claude Code:**
- [Claude Code Documentation](https://docs.anthropic.com/claude/docs)

## Version

**Plugin Version**: 1.0.0
**Compatibility**: macOS 12.0+ (Monterey and later)
**Python**: 3.8+

## Support

For issues, questions, or contributions:
1. Check documentation in `docs/` directory
2. Review SKILL.md for command usage
3. Examine script help: `uv run python3 script.py --help`
4. Open an issue on GitHub (if repository configured)

---

Made with Claude Code
