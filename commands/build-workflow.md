---
description: "Build a shortcut workflow programmatically using Python DSL"
argument-hint: "[--interactive] [--output <path>]"
allowed-tools: ["Bash(uv run:*)", "Read", "Write"]
---

# Build Shortcut Workflow

Build complex shortcut workflows programmatically using a Python Domain-Specific Language (DSL).

## Usage

```bash
/mac-shortcuts:build [--interactive] [--output <path>]
```

## Options

- `--interactive`: Interactive step-by-step workflow builder
- `--output <path>`: Output file path (default: workflow.shortcut)

## Interactive Mode

The interactive builder guides you through creating a workflow step-by-step:

1. **Add Actions**: Choose from available action types
2. **Configure**: Set parameters for each action
3. **Chain**: Actions are executed in sequence
4. **Preview**: See the workflow structure
5. **Save**: Generate the .shortcut file

## Available Actions

### Text Actions
- **Text**: Display or generate text
- **Comment**: Add comments to workflow

### Notifications
- **Notification**: Show system notifications with title and body

### Scripts
- **Shell Script**: Execute bash/shell scripts
- **Script Input**: Pass input to scripts

### Variables
- **Set Variable**: Store values in variables
- **Get Variable**: Retrieve stored values

### Clipboard
- **Get Clipboard**: Get clipboard content
- **Set Clipboard**: Copy text to clipboard

### URLs
- **URL**: Define URLs
- **Open URL**: Open URLs in browser/app

### Control Flow
- **Conditional**: If/else logic
- **Loop**: Repeat actions

## Examples

### Example 1: Simple Text to Notification

```bash
# Interactive mode
/mac-shortcuts:build --interactive
# Then select:
# 1. Add Text action with "Hello World"
# 2. Add Notification action
# 3. Save to hello.shortcut
```

### Example 2: Script Runner with Notification

```bash
# Build a workflow that runs a script and shows result
/mac-shortcuts:build --interactive
# Then add:
# 1. Shell Script: echo "System: $(uname -a)"
# 2. Notification with script output
```

### Example 3: Clipboard to File

```bash
# Build a workflow that saves clipboard to file
/mac-shortcuts:build --interactive
# Then add:
# 1. Get Clipboard
# 2. Save to File (with prompt)
```

## Python DSL Usage

For advanced users, you can write Python scripts using the WorkflowBuilder DSL:

```python
from workflow_builder import WorkflowBuilder

# Create builder
builder = WorkflowBuilder("My Workflow")

# Add actions
builder.add_text("Hello from Python!")
builder.add_notification("Hello from Python!", "Workflow")

# Set icon
builder.set_icon(glyph_number=59511, color=4282601983)

# Save
builder.save("my_workflow.shortcut")
```

## Implementation

Interactive workflow builder:
!`cd "${CLAUDE_PLUGIN_ROOT:-$(pwd)}/skills/shortcuts-cli/scripts" && uv run python3 -c "
from interactive_menu import select_shortcut, text_input, confirm_action
from workflow_builder import WorkflowBuilder, TextAction, NotificationAction, ScriptAction, ClipboardAction
import sys

builder = WorkflowBuilder()

print('Interactive Workflow Builder')
print('=' * 40)

while True:
    # Select action type
    actions = [
        'Add Text',
        'Add Notification',
        'Add Shell Script',
        'Add Clipboard (Get)',
        'Add Clipboard (Set)',
        'Add Comment',
        'Set Icon',
        'Finish & Save'
    ]

    choice = select_shortcut(actions, 'Select action to add:')

    if not choice or choice == 'Finish & Save':
        break

    if choice == 'Add Text':
        text = text_input('Enter text:')
        if text:
            builder.add_text(text)

    elif choice == 'Add Notification':
        body = text_input('Notification body:')
        title = text_input('Notification title:', 'Shortcut')
        if body:
            builder.add_notification(body, title)

    elif choice == 'Add Shell Script':
        script = text_input('Shell script:')
        if script:
            builder.add_script(script)

    elif choice == 'Add Clipboard (Get)':
        builder.add_clipboard('Get')

    elif choice == 'Add Clipboard (Set)':
        builder.add_clipboard('Set')

    elif choice == 'Add Comment':
        comment = text_input('Comment text:')
        if comment:
            builder.add_comment(comment)

    elif choice == 'Set Icon':
        try:
            glyph = int(text_input('Glyph number:', '59511'))
            color = int(text_input('Color (RGBA int):', '4282601983'))
            builder.set_icon(glyph, color)
        except ValueError:
            print('Invalid number, skipping')

print(f'\nWorkflow has {len(builder.actions)} actions')

output = text_input('Output file:', 'workflow.shortcut')
builder.save(output)
print(f'✓ Workflow saved to: {output}')
"`

## Workflow Structure

The generated .shortcut file contains:

- **WFWorkflowActions**: Array of actions in execution order
- **WFWorkflowClientVersion**: Shortcuts app version
- **WFWorkflowIcon**: Icon configuration
- **Action UUIDs**: Unique identifiers for each action
- **Parameters**: Action-specific configuration

## After Building

1. **Sign the workflow**:
   ```bash
   /mac-shortcuts:sign --input workflow.shortcut --output workflow-signed.shortcut
   ```

2. **Import to Shortcuts app**:
   - Double-click the .shortcut file

3. **Test the workflow**:
   ```bash
   /mac-shortcuts:run "Workflow Name"
   ```

4. **View in Shortcuts app**:
   ```bash
   /mac-shortcuts:view "Workflow Name"
   ```

## Notes

- Interactive mode is recommended for beginners
- Python DSL is available for advanced automation
- Actions execute in the order they're added
- Variables can be used to pass data between actions
- Use comments to document complex workflows
- Generated workflows are compatible with macOS and iOS Shortcuts
