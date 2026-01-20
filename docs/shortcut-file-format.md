# .shortcut File Format Reference

Complete reference for the .shortcut property list file format used by macOS and iOS Shortcuts.

## Overview

.shortcut files are property list (plist) files that define workflows in the Shortcuts app. They can be:
- Binary format (most common)
- XML format (human-readable)
- Both are functionally equivalent

## File Structure

### Root Level Keys

```json
{
  "WFWorkflowActions": [...],
  "WFWorkflowClientVersion": "2690.0.2",
  "WFWorkflowClientRelease": "17.0",
  "WFWorkflowMinimumClientVersion": 1113,
  "WFWorkflowMinimumClientRelease": "15.0",
  "WFWorkflowIcon": {...},
  "WFWorkflowTypes": [...],
  "WFWorkflowInputContentItemClasses": [...]
}
```

### Required Keys

**`WFWorkflowActions`** (Array)
- Contains all workflow actions in execution order
- Each action is a dictionary with identifier and parameters
- Minimum: Empty array `[]`

**`WFWorkflowClientVersion`** (String)
- Version of Shortcuts app that created the file
- Example: `"2690.0.2"`

**`WFWorkflowClientRelease`** (String)
- macOS/iOS version
- Example: `"17.0"` for macOS Sonoma

**`WFWorkflowMinimumClientVersion`** (Number)
- Minimum Shortcuts app version required
- Example: `1113`

**`WFWorkflowMinimumClientRelease`** (String)
- Minimum OS version required
- Example: `"15.0"` for macOS Catalina

### Optional Keys

**`WFWorkflowIcon`** (Dictionary)
- Icon configuration
- Color and glyph number

**`WFWorkflowTypes`** (Array)
- Workflow types/contexts
- Examples: `"Watch"`, `"NCWidget"`, `"MenuBar"`

**`WFWorkflowInputContentItemClasses`** (Array)
- Expected input types
- Uses UTI format

**`WFWorkflowImportQuestions`** (Array)
- Questions to ask when importing
- For parameterized shortcuts

**`WFWorkflowNoInputBehavior`** (Dictionary)
- Behavior when no input provided

---

## Icon Configuration

### WFWorkflowIcon Structure

```json
{
  "WFWorkflowIcon": {
    "WFWorkflowIconStartColor": 4282601983,
    "WFWorkflowIconGlyphNumber": 59511
  }
}
```

### Color Values

Colors are RGBA integers (32-bit):

**Common Colors:**
- Red: `4282601983`
- Orange: `4271458815`
- Yellow: `4274264319`
- Green: `4292093695`
- Teal: `431817727`
- Blue: `463140863`
- Indigo: `946986751`
- Purple: `2071128575`
- Pink: `3679049983`
- Gray: `2846468607`

**Calculate from RGB:**
```python
def rgb_to_wf_color(r, g, b, a=255):
    return (r << 24) | (g << 16) | (b << 8) | a

# Example: Red (255, 0, 0)
red = rgb_to_wf_color(255, 0, 0)  # 4278190335
```

### Glyph Numbers

SF Symbols glyph numbers:

**Common Glyphs:**
- 59636: Gear (settings)
- 59511: Star
- 59734: Checkmark
- 61440: Plus
- 61443: Minus
- 59592: Calendar
- 59729: Clock
- 59716: Folder
- 59603: Document
- 59468: Camera

**Find Glyphs:**
1. Use SF Symbols app (free from Apple)
2. Copy glyph number from app
3. Use in `WFWorkflowIconGlyphNumber`

---

## Action Structure

### Basic Action Format

```json
{
  "WFWorkflowActionIdentifier": "is.workflow.actions.gettext",
  "WFWorkflowActionParameters": {
    "WFTextActionText": "Hello World",
    "UUID": "12345678-1234-1234-1234-123456789012"
  }
}
```

### Common Action Identifiers

**Text:**
- `is.workflow.actions.gettext`: Get/display text
- `is.workflow.actions.comment`: Add comment

**Notifications:**
- `is.workflow.actions.notification`: Show notification
- `is.workflow.actions.alert`: Show alert

**Scripts:**
- `is.workflow.actions.runshellscript`: Run shell script
- `is.workflow.actions.runjavascript`: Run JavaScript

**Clipboard:**
- `is.workflow.actions.getclipboard`: Get clipboard content
- `is.workflow.actions.setclipboard`: Set clipboard content

**Variables:**
- `is.workflow.actions.setvariable`: Set variable
- `is.workflow.actions.getvariable`: Get variable

**URLs:**
- `is.workflow.actions.url`: Define URL
- `is.workflow.actions.openurl`: Open URL

**Files:**
- `is.workflow.actions.getfile`: Get file
- `is.workflow.actions.savefile`: Save file

**Control Flow:**
- `is.workflow.actions.conditional`: If/else
- `is.workflow.actions.repeat.each`: For each loop
- `is.workflow.actions.repeat.count`: Repeat N times

### Action Parameters

Each action type has specific parameters:

**Text Action:**
```json
{
  "WFWorkflowActionIdentifier": "is.workflow.actions.gettext",
  "WFWorkflowActionParameters": {
    "WFTextActionText": "Your text here",
    "UUID": "..."
  }
}
```

**Notification Action:**
```json
{
  "WFWorkflowActionIdentifier": "is.workflow.actions.notification",
  "WFWorkflowActionParameters": {
    "WFNotificationActionTitle": "Title",
    "WFNotificationActionBody": "Body text",
    "WFNotificationActionSound": true,
    "UUID": "..."
  }
}
```

**Shell Script Action:**
```json
{
  "WFWorkflowActionIdentifier": "is.workflow.actions.runshellscript",
  "WFWorkflowActionParameters": {
    "WFShellScriptActionScript": "echo 'Hello'",
    "WFShellScriptActionShell": "/bin/bash",
    "WFShellScriptActionInputMode": "Variable",
    "UUID": "..."
  }
}
```

**Variable Actions:**
```json
// Set Variable
{
  "WFWorkflowActionIdentifier": "is.workflow.actions.setvariable",
  "WFWorkflowActionParameters": {
    "WFVariableName": "myVar",
    "UUID": "..."
  }
}

// Get Variable
{
  "WFWorkflowActionIdentifier": "is.workflow.actions.getvariable",
  "WFWorkflowActionParameters": {
    "WFVariable": {
      "Value": {
        "Type": "Variable",
        "Variable": "myVar"
      },
      "WFSerializationType": "WFTextTokenAttachment"
    },
    "UUID": "..."
  }
}
```

---

## Variable References

### Magic Variables

Variables can be referenced using special syntax:

```json
{
  "Value": {
    "attachmentsByRange": {
      "{0, 1}": {
        "Type": "Variable",
        "Variable": "variableName"
      }
    },
    "string": "�"
  },
  "WFSerializationType": "WFTextTokenString"
}
```

### Variable Types

- `Variable`: Named variable
- `ActionOutput`: Output from specific action
- `Input`: Workflow input
- `Clipboard`: Clipboard content

---

## Conditional Logic

### If Statement Structure

```json
{
  "WFWorkflowActionIdentifier": "is.workflow.actions.conditional",
  "WFWorkflowActionParameters": {
    "WFCondition": "Equals",
    "WFConditionalActionString": "test",
    "GroupingIdentifier": "ABC123",
    "UUID": "..."
  }
}
```

**Condition Types:**
- `Equals`: Exact match
- `Contains`: String contains
- `IsGreaterThan`: Numeric comparison
- `IsLessThan`: Numeric comparison
- `BeginsWith`: String starts with
- `EndsWith`: String ends with

### Grouping

Related conditional actions use the same `GroupingIdentifier`:

```json
// If
{"GroupingIdentifier": "ABC123", ...}

// Then actions
{"GroupingIdentifier": "ABC123", ...}

// Else (if any)
{"GroupingIdentifier": "ABC123", ...}

// End If
{"GroupingIdentifier": "ABC123", ...}
```

---

## Input/Output Types

### UTI (Universal Type Identifiers)

Specify expected input types:

```json
{
  "WFWorkflowInputContentItemClasses": [
    "WFImageContentItem",
    "WFPDFContentItem",
    "WFStringContentItem"
  ]
}
```

**Common Content Item Classes:**
- `WFStringContentItem`: Text
- `WFImageContentItem`: Images
- `WFPDFContentItem`: PDF files
- `WFURLContentItem`: URLs
- `WFPhotoMediaContentItem`: Photos
- `WFContactContentItem`: Contacts
- `WFLocationContentItem`: Locations

---

## Import Questions

### Parameterized Shortcuts

Allow customization on import:

```json
{
  "WFWorkflowImportQuestions": [
    {
      "ActionIndex": 0,
      "Category": "Parameter",
      "ParameterKey": "WFTextActionText",
      "Text": "What text should be displayed?"
    }
  ]
}
```

**Question Structure:**
- `ActionIndex`: Which action to configure
- `Category`: Type of question
- `ParameterKey`: Parameter to set
- `Text`: Question to ask user
- `DefaultValue`: Optional default

---

## Complete Example

### Simple Text to Notification Shortcut

```json
{
  "WFWorkflowActions": [
    {
      "WFWorkflowActionIdentifier": "is.workflow.actions.gettext",
      "WFWorkflowActionParameters": {
        "WFTextActionText": "Hello from Shortcuts!",
        "UUID": "11111111-1111-1111-1111-111111111111"
      }
    },
    {
      "WFWorkflowActionIdentifier": "is.workflow.actions.notification",
      "WFWorkflowActionParameters": {
        "WFNotificationActionBody": "Hello from Shortcuts!",
        "WFNotificationActionSound": true,
        "UUID": "22222222-2222-2222-2222-222222222222"
      }
    }
  ],
  "WFWorkflowClientVersion": "2690.0.2",
  "WFWorkflowClientRelease": "17.0",
  "WFWorkflowMinimumClientVersion": 1113,
  "WFWorkflowMinimumClientRelease": "15.0",
  "WFWorkflowIcon": {
    "WFWorkflowIconStartColor": 4282601983,
    "WFWorkflowIconGlyphNumber": 59511
  },
  "WFWorkflowTypes": []
}
```

---

## Working with Plists

### Reading (Python)

```python
import plistlib

with open('shortcut.shortcut', 'rb') as f:
    data = plistlib.load(f)

# Access actions
actions = data['WFWorkflowActions']
for action in actions:
    print(action['WFWorkflowActionIdentifier'])
```

### Writing (Python)

```python
import plistlib

shortcut = {
    'WFWorkflowActions': [...],
    'WFWorkflowClientVersion': '2690.0.2',
    ...
}

with open('new_shortcut.shortcut', 'wb') as f:
    plistlib.dump(shortcut, f, fmt=plistlib.FMT_BINARY)
```

### Converting Formats

```python
# Binary to XML
with open('binary.shortcut', 'rb') as f:
    data = plistlib.load(f)

with open('xml.shortcut', 'wb') as f:
    plistlib.dump(data, f, fmt=plistlib.FMT_XML)
```

---

## Validation

### Required Checks

1. **Has WFWorkflowActions array**
2. **Has version information**
3. **All actions have identifiers**
4. **All actions have UUIDs**
5. **Valid parameter types**

### Using Plugin

```bash
# Validate with plugin script
cd skills/shortcuts-cli/scripts
uv run python3 plist_parser.py validate myshortcut.shortcut
```

---

## Common Issues

**Invalid Plist:**
- Ensure proper JSON/XML structure
- Check all braces/brackets match
- Validate with `plutil -lint file.shortcut`

**Missing UUIDs:**
- Each action must have unique UUID
- Generate with: `uuidgen` or Python `uuid.uuid4()`

**Version Mismatch:**
- Set appropriate minimum versions
- Test on target OS version

**Parameter Errors:**
- Check parameter names match action type
- Verify value types (string, number, boolean)

---

## Resources

**Plugin Tools:**
- `/mac-shortcuts:parse`: Parse .shortcut files
- `/mac-shortcuts:build`: Build shortcuts programmatically
- `plist_parser.py`: Python plist manipulation

**Apple Documentation:**
- [Property List Programming Guide](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/PropertyLists/)
- [Shortcuts File Format](https://support.apple.com/guide/shortcuts/)

**Tools:**
- `plutil`: Validate and convert plists
- SF Symbols app: Browse icon glyphs
- Xcode: View and edit plists
