# Workflow Builder Guide

Complete guide to building Mac Shortcuts programmatically using the Python DSL.

## Overview

The Workflow Builder provides a Python Domain-Specific Language (DSL) for creating Mac Shortcuts programmatically. This enables:

- Automated shortcut generation
- Version-controlled workflow definitions
- Batch creation of similar shortcuts
- Complex workflow construction
- Template-based shortcut creation

## Quick Start

### Basic Workflow

```python
from workflow_builder import WorkflowBuilder

# Create builder
builder = WorkflowBuilder("My First Workflow")

# Add actions
builder.add_text("Hello World!")
builder.add_notification("Hello World!", "Greeting")

# Save
builder.save("hello.shortcut")
```

### Using the CLI

```bash
# Interactive mode
/mac-shortcuts:build --interactive

# Command-line with Python
cd skills/shortcuts-cli/scripts
uv run python3 workflow_builder.py \
  --type text \
  --content "Hello World" \
  --output hello.shortcut
```

---

## WorkflowBuilder Class

### Constructor

```python
WorkflowBuilder(name: Optional[str] = None)
```

**Parameters:**
- `name`: Optional workflow name for reference

**Example:**
```python
builder = WorkflowBuilder("Data Processor")
```

### Core Methods

#### `add_action(action: Action) -> WorkflowBuilder`

Add any action to the workflow.

```python
from workflow_builder import TextAction

action = TextAction("Custom text")
builder.add_action(action)
```

**Returns:** Self for method chaining

#### `build() -> Dict[str, Any]`

Build the workflow dictionary.

```python
workflow_dict = builder.build()
# Returns plist-compatible dictionary
```

#### `save(file_path: str) -> None`

Build and save to .shortcut file.

```python
builder.save("my_workflow.shortcut")
# Creates signed .shortcut file
```

---

## Action Methods

### Text Actions

#### `add_text(text: str) -> WorkflowBuilder`

Add a text action.

```python
builder.add_text("Hello World!")
builder.add_text("Line 1\nLine 2")
builder.add_text("Dynamic: {{variable}}")
```

#### `add_comment(comment: str) -> WorkflowBuilder`

Add a comment (documentation).

```python
builder.add_comment("This is what the workflow does")
builder.add_comment("TODO: Add error handling")
```

### Notifications

#### `add_notification(body: str, title: Optional[str] = None) -> WorkflowBuilder`

Add a notification action.

```python
builder.add_notification("Task complete!", "Success")
builder.add_notification("Error occurred", "Error")
builder.add_notification("{{result}}")  # Show variable
```

### Shell Scripts

#### `add_script(script: str, shell: str = '/bin/bash') -> WorkflowBuilder`

Add a shell script action.

```python
builder.add_script("date")
builder.add_script("echo 'Hello'")
builder.add_script("uname -a")

# Different shell
builder.add_script("echo 'test'", shell="/bin/zsh")

# Multi-line script
builder.add_script("""
#!/bin/bash
echo "Starting..."
date
echo "Done"
""")
```

### Clipboard Operations

#### `add_clipboard(mode: str = 'Get') -> WorkflowBuilder`

Add clipboard action.

```python
# Get clipboard content
builder.add_clipboard('Get')

# Set clipboard content (uses previous action output)
builder.add_clipboard('Set')
```

### Variables

#### `add_variable(name: str, set_value: bool = True) -> WorkflowBuilder`

Add variable action.

```python
# Set variable (store current value)
builder.add_variable('myVar', set_value=True)

# Get variable (retrieve stored value)
builder.add_variable('myVar', set_value=False)
```

**Example with variables:**
```python
builder.add_text("Original text")
builder.add_variable('original', set_value=True)
builder.add_text("Modified text")
builder.add_variable('original', set_value=False)
builder.add_notification("{{original}}")
```

### URL Operations

#### `add_url(url: str, open_it: bool = False) -> WorkflowBuilder`

Add URL action.

```python
# Just define URL
builder.add_url("https://example.com")

# Define and open
builder.add_url("https://example.com", open_it=True)
```

### Icon Customization

#### `set_icon(glyph_number: int = 59511, color: int = 4282601983) -> WorkflowBuilder`

Set workflow icon.

```python
# Default star icon
builder.set_icon()

# Custom glyph and color
builder.set_icon(glyph_number=59636, color=4292093695)  # Gear, green
```

**Common glyph numbers:**
- 59511: Star
- 59636: Gear
- 59734: Checkmark
- 61440: Plus
- 59592: Calendar

**Common colors:**
- Red: 4282601983
- Green: 4292093695
- Blue: 463140863
- Purple: 2071128575

---

## Action Classes

For advanced usage, create actions directly:

### TextAction

```python
from workflow_builder import TextAction

action = TextAction("Hello World!")
builder.add_action(action)
```

### NotificationAction

```python
from workflow_builder import NotificationAction

action = NotificationAction(
    body="Message body",
    title="Message title",
    sound=True
)
builder.add_action(action)
```

### ScriptAction

```python
from workflow_builder import ScriptAction

action = ScriptAction(
    script="echo 'test'",
    shell="/bin/bash",
    input_mode="Variable"
)
builder.add_action(action)
```

### ClipboardAction

```python
from workflow_builder import ClipboardAction

get_clipboard = ClipboardAction(mode='Get', local_only=False)
set_clipboard = ClipboardAction(mode='Set', local_only=False)
```

### SetVariableAction / GetVariableAction

```python
from workflow_builder import SetVariableAction, GetVariableAction

set_var = SetVariableAction('myVar')
get_var = GetVariableAction('myVar')
```

### URLAction / OpenURLAction

```python
from workflow_builder import URLAction, OpenURLAction

url = URLAction('https://example.com')
open_url = OpenURLAction()
```

---

## Convenience Functions

### create_text_notification

Quick text-to-notification workflow.

```python
from workflow_builder import create_text_notification

builder = create_text_notification(
    text="Hello World",
    title="Greeting"
)
builder.save("greeting.shortcut")
```

### create_script_runner

Shell script runner with optional notification.

```python
from workflow_builder import create_script_runner

builder = create_script_runner(
    script="date",
    notify_result=True
)
builder.save("run_date.shortcut")
```

### create_url_opener

URL opener workflow.

```python
from workflow_builder import create_url_opener

builder = create_url_opener("https://example.com")
builder.save("open_example.shortcut")
```

---

## Example Workflows

### Example 1: System Info Notifier

```python
from workflow_builder import WorkflowBuilder

builder = WorkflowBuilder("System Info")

# Get system info
builder.add_script("""
echo "macOS: $(sw_vers -productVersion)"
echo "User: $(whoami)"
echo "Hostname: $(hostname)"
""")

# Show in notification
builder.add_notification("{{result}}", "System Information")

# Set icon
builder.set_icon(glyph_number=59636, color=463140863)  # Gear, blue

builder.save("system_info.shortcut")
```

### Example 2: Clipboard Processor

```python
from workflow_builder import WorkflowBuilder

builder = WorkflowBuilder("Clipboard Processor")

# Get clipboard
builder.add_clipboard('Get')

# Save original
builder.add_variable('original', set_value=True)

# Process with script
builder.add_script('tr "[:lower:]" "[:upper:]"')  # Convert to uppercase

# Show result
builder.add_notification("Processed!", "Complete")

# Restore original to clipboard
builder.add_variable('original', set_value=False)
builder.add_clipboard('Set')

builder.save("clipboard_processor.shortcut")
```

### Example 3: Multi-Step Workflow

```python
from workflow_builder import WorkflowBuilder

builder = WorkflowBuilder("Daily Routine")

# Step 1: Morning greeting
builder.add_comment("Morning greeting")
builder.add_script("date '+Good morning! Today is %A, %B %d'")
builder.add_notification("{{result}}", "Daily Routine")

# Step 2: Weather check (example)
builder.add_comment("Check weather")
builder.add_url("https://wttr.in/", open_it=True)

# Step 3: Save log
builder.add_comment("Log execution")
builder.add_script("echo \"Routine ran at $(date)\" >> ~/daily_log.txt")

# Icon
builder.set_icon(glyph_number=59592, color=4271458815)  # Calendar, orange

builder.save("daily_routine.shortcut")
```

### Example 4: File Backup

```python
from workflow_builder import WorkflowBuilder

builder = WorkflowBuilder("Backup Documents")

# Create backup script
backup_script = """
#!/bin/bash
BACKUP_DIR="$HOME/Backups/$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"
cp -r "$HOME/Documents" "$BACKUP_DIR/"
echo "Backup complete: $BACKUP_DIR"
"""

builder.add_script(backup_script)
builder.add_notification("{{result}}", "Backup Complete")

builder.save("backup_docs.shortcut")
```

### Example 5: URL Launcher Menu

```python
from workflow_builder import WorkflowBuilder

builder = WorkflowBuilder("Quick Links")

# Add multiple URL opens
builder.add_comment("Open frequently used websites")

urls = [
    "https://github.com",
    "https://stackoverflow.com",
    "https://developer.apple.com"
]

for url in urls:
    builder.add_url(url, open_it=True)

builder.save("quick_links.shortcut")
```

---

## Advanced Techniques

### Variable Chaining

```python
builder = WorkflowBuilder("Variable Chain")

# Store multiple values
builder.add_text("Value 1")
builder.add_variable('val1', set_value=True)

builder.add_text("Value 2")
builder.add_variable('val2', set_value=True)

# Combine
builder.add_variable('val1', set_value=False)
builder.add_text(" and ")
builder.add_variable('val2', set_value=False)

builder.add_notification("{{result}}")
```

### Dynamic Content

```python
builder = WorkflowBuilder("Dynamic Content")

# Get current date
builder.add_script("date '+%Y-%m-%d'")
builder.add_variable('today', set_value=True)

# Create message with date
builder.add_text("Report for: ")
builder.add_variable('today', set_value=False)

builder.add_notification("{{result}}", "Report Generated")
```

### Error Handling (via comments)

```python
builder = WorkflowBuilder("Safe Script")

builder.add_comment("Try to execute command")
builder.add_script("""
if command -v git >/dev/null 2>&1; then
    git --version
else
    echo "Git not installed"
fi
""")

builder.add_notification("{{result}}")
```

---

## Integration with Plugin Commands

### After Building

1. **Save the workflow:**
```python
builder.save("my_workflow.shortcut")
```

2. **Sign it:**
```bash
/mac-shortcuts:sign \
  --input my_workflow.shortcut \
  --output my_workflow-signed.shortcut
```

3. **Import to Shortcuts:**
- Double-click the .shortcut file
- Or use Shortcuts app File > Import

4. **Run it:**
```bash
/mac-shortcuts:run "My Workflow"
```

5. **View it:**
```bash
/mac-shortcuts:view "My Workflow"
```

---

## Best Practices

### Naming

```python
# Good names
builder = WorkflowBuilder("Process Images")
builder = WorkflowBuilder("Daily Backup")
builder = WorkflowBuilder("Send Report")

# Avoid
builder = WorkflowBuilder("Workflow1")
builder = WorkflowBuilder("Test")
```

### Comments

```python
# Add comments to document complex workflows
builder.add_comment("Step 1: Fetch data from API")
builder.add_script("curl https://api.example.com/data")

builder.add_comment("Step 2: Process JSON response")
builder.add_script("jq '.results[]'")

builder.add_comment("Step 3: Notify user")
builder.add_notification("Data processed successfully")
```

### Variables

```python
# Use descriptive variable names
builder.add_variable('original_text', set_value=True)
builder.add_variable('processed_result', set_value=True)

# Avoid
builder.add_variable('x', set_value=True)
builder.add_variable('temp', set_value=True)
```

### Error Messages

```python
# Include error handling in scripts
builder.add_script("""
if [ $? -eq 0 ]; then
    echo "Success"
else
    echo "Error: Operation failed"
fi
""")
```

---

## Troubleshooting

### Workflow doesn't run

- Check all required parameters are set
- Validate .shortcut file: `/mac-shortcuts:parse file.shortcut`
- Sign the file before importing
- Check script syntax if using shell scripts

### Actions execute in wrong order

- Actions run in the order they're added
- Use `add_comment()` to document execution flow
- Check variable dependencies

### Variables not working

- Ensure variable is set before getting
- Use correct variable names (case-sensitive)
- Check variable references in notification text

### Icons not showing

- Use valid glyph numbers (see SF Symbols app)
- Color must be valid RGBA integer
- Call `set_icon()` before `save()`

---

## Resources

**Plugin Commands:**
- `/mac-shortcuts:build`: Interactive workflow builder
- `/mac-shortcuts:parse`: Analyze existing shortcuts
- `/mac-shortcuts:sign`: Sign workflows for sharing

**Documentation:**
- `shortcut-file-format.md`: .shortcut file structure
- `shortcuts-cli-reference.md`: CLI command reference

**Python Modules:**
- `workflow_builder.py`: Main builder module
- `plist_parser.py`: Plist manipulation
- `shortcut_utils.py`: Utilities and validation

**Examples:**
- All examples in this guide
- Templates in `skills/shortcuts-cli/scripts/templates/`
- CLI help: `uv run python3 workflow_builder.py --help`
