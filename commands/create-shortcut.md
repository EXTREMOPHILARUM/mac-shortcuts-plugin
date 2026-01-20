---
description: "Create a new .shortcut file from templates"
argument-hint: "[--template <type>] [--output <path>] [--interactive]"
allowed-tools: ["Bash(uv run:*)", "Read", "Write"]
---

# Create Shortcut File

Create a new .shortcut file from predefined templates or custom specifications.

## Usage

```bash
/mac-shortcuts:create [--template <type>] [--output <path>] [--interactive]
```

## Options

- `--template <type>`: Template type (text, notification, script)
- `--output <path>`: Output file path (default: ./shortcut.shortcut)
- `--interactive`: Use interactive mode to configure the shortcut

## Templates

### text
Creates a simple text output shortcut
- Displays static text
- Useful for quick notes or reminders

### notification
Creates a notification shortcut
- Shows a system notification
- Customizable title and body

### script
Creates a shell script runner shortcut
- Executes custom bash/shell scripts
- Captures script output

## Examples

```bash
# Create a text shortcut interactively
/mac-shortcuts:create --template text --interactive --output MyText.shortcut

# Create a notification shortcut
/mac-shortcuts:create --template notification --output Notify.shortcut

# Create a script runner
/mac-shortcuts:create --template script --output RunScript.shortcut
```

## Implementation

### Interactive Mode

In interactive mode, the command will prompt for:
1. Template selection
2. Configuration parameters (text content, script, etc.)
3. Output file path
4. Icon customization (optional)

Use the workflow builder with interactive prompts:
!`cd "${CLAUDE_PLUGIN_ROOT:-$(pwd)}/skills/shortcuts-cli/scripts" && uv run python3 -c "
from interactive_menu import select_shortcut, text_input, confirm_action
from workflow_builder import create_text_notification, create_script_runner, create_url_opener
import sys

# Select template
templates = ['text', 'notification', 'script', 'url']
template = select_shortcut(templates, 'Select template:')

if not template:
    sys.exit(1)

# Get content
content = text_input('Enter content:')
output = text_input('Output file:', 'shortcut.shortcut')

# Build workflow
if template == 'text' or template == 'notification':
    title = text_input('Notification title:', 'Shortcut')
    builder = create_text_notification(content, title)
elif template == 'script':
    builder = create_script_runner(content)
elif template == 'url':
    builder = create_url_opener(content)

builder.save(output)
print(f'✓ Created: {output}')
"`

### Template Mode

For non-interactive template creation:
!`cd "${CLAUDE_PLUGIN_ROOT:-$(pwd)}/skills/shortcuts-cli/scripts" && uv run python3 workflow_builder.py --type $1 --content "$2" --output $3`

## After Creation

After creating a .shortcut file:

1. **Sign the file** (required for sharing):
   ```bash
   /mac-shortcuts:sign --input MyShortcut.shortcut --output MyShortcut-signed.shortcut
   ```

2. **Import to Shortcuts app**:
   - Double-click the .shortcut file, or
   - Open in Shortcuts app via File > Import

3. **Test the shortcut**:
   ```bash
   /mac-shortcuts:run "Shortcut Name"
   ```

## Notes

- Created shortcuts are unsigned by default
- Use `/mac-shortcuts:sign` to sign before sharing
- Templates provide basic structure; edit in Shortcuts app for advanced features
- Interactive mode recommended for first-time users
