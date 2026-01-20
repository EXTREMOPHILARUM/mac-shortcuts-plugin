#!/usr/bin/env python3
"""
Mac Shortcuts Plugin - Workflow Builder

Provides a Python DSL for building Mac Shortcuts programmatically.
"""

import uuid
from typing import Dict, List, Any, Optional
from plist_parser import create_shortcut_plist, write_shortcut_file


class Action:
    """Base class for all shortcut actions."""

    def __init__(self, identifier: str, parameters: Optional[Dict[str, Any]] = None):
        """
        Initialize an action.

        Args:
            identifier: WFWorkflowActionIdentifier
            parameters: Action parameters dictionary
        """
        self.identifier = identifier
        self.parameters = parameters or {}
        self.uuid = str(uuid.uuid4())

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert action to dictionary format for plist.

        Returns:
            Action dictionary
        """
        action_dict = {
            'WFWorkflowActionIdentifier': self.identifier,
            'WFWorkflowActionParameters': {
                **self.parameters,
                'UUID': self.uuid
            }
        }
        return action_dict


class TextAction(Action):
    """Action for displaying or manipulating text."""

    def __init__(self, text: str):
        """
        Create a text action.

        Args:
            text: The text content
        """
        super().__init__(
            'is.workflow.actions.gettext',
            {'WFTextActionText': text}
        )


class CommentAction(Action):
    """Action for adding comments to workflow."""

    def __init__(self, comment: str):
        """
        Create a comment action.

        Args:
            comment: Comment text
        """
        super().__init__(
            'is.workflow.actions.comment',
            {'WFCommentActionText': comment}
        )


class NotificationAction(Action):
    """Action for showing notifications."""

    def __init__(self, body: str, title: Optional[str] = None, sound: bool = True):
        """
        Create a notification action.

        Args:
            body: Notification body text
            title: Optional notification title
            sound: Whether to play sound
        """
        params = {
            'WFNotificationActionBody': body,
            'WFNotificationActionSound': sound
        }

        if title:
            params['WFNotificationActionTitle'] = title

        super().__init__('is.workflow.actions.notification', params)


class ScriptAction(Action):
    """Action for running shell scripts."""

    def __init__(self, script: str, shell: str = '/bin/bash', input_mode: str = 'Variable'):
        """
        Create a script action.

        Args:
            script: Shell script to execute
            shell: Path to shell interpreter
            input_mode: How to pass input ('Variable', 'STDIN', 'Arguments')
        """
        super().__init__(
            'is.workflow.actions.runshellscript',
            {
                'WFShellScriptActionScript': script,
                'WFShellScriptActionShell': shell,
                'WFShellScriptActionInputMode': input_mode
            }
        )


class ClipboardAction(Action):
    """Action for clipboard operations."""

    def __init__(self, mode: str = 'Get', local_only: bool = False):
        """
        Create a clipboard action.

        Args:
            mode: 'Get' to get clipboard content, 'Set' to set it
            local_only: Only use local clipboard (not universal)
        """
        if mode == 'Get':
            super().__init__('is.workflow.actions.getclipboard', {
                'WFLocalOnly': local_only
            })
        else:
            super().__init__('is.workflow.actions.setclipboard', {
                'WFLocalOnly': local_only
            })


class SetVariableAction(Action):
    """Action for setting workflow variables."""

    def __init__(self, variable_name: str):
        """
        Create a set variable action.

        Args:
            variable_name: Name of the variable to set
        """
        super().__init__(
            'is.workflow.actions.setvariable',
            {'WFVariableName': variable_name}
        )


class GetVariableAction(Action):
    """Action for getting workflow variables."""

    def __init__(self, variable_name: str):
        """
        Create a get variable action.

        Args:
            variable_name: Name of the variable to get
        """
        super().__init__(
            'is.workflow.actions.getvariable',
            {
                'WFVariable': {
                    'Value': {
                        'Type': 'Variable',
                        'Variable': variable_name
                    },
                    'WFSerializationType': 'WFTextTokenAttachment'
                }
            }
        )


class URLAction(Action):
    """Action for opening URLs."""

    def __init__(self, url: str):
        """
        Create a URL action.

        Args:
            url: URL to open
        """
        super().__init__(
            'is.workflow.actions.url',
            {'WFURLActionURL': url}
        )


class OpenURLAction(Action):
    """Action for opening URLs in browser/app."""

    def __init__(self):
        """Create an open URL action (uses input URL)."""
        super().__init__('is.workflow.actions.openurl', {})


class ConditionalAction(Action):
    """Action for if/else conditionals."""

    def __init__(self, condition: str = 'Equals', compare_to: str = ''):
        """
        Create a conditional action.

        Args:
            condition: Type of condition (Equals, Contains, etc.)
            compare_to: Value to compare against
        """
        super().__init__(
            'is.workflow.actions.conditional',
            {
                'WFCondition': condition,
                'WFConditionalActionString': compare_to,
                'GroupingIdentifier': str(uuid.uuid4())
            }
        )


class WorkflowBuilder:
    """Builder for creating shortcuts workflows programmatically."""

    def __init__(self, name: Optional[str] = None):
        """
        Initialize workflow builder.

        Args:
            name: Optional workflow name (for reference)
        """
        self.name = name or "Untitled Workflow"
        self.actions: List[Action] = []
        self.metadata: Dict[str, Any] = {}

    def add_action(self, action: Action) -> 'WorkflowBuilder':
        """
        Add an action to the workflow.

        Args:
            action: Action to add

        Returns:
            Self for chaining
        """
        self.actions.append(action)
        return self

    def add_text(self, text: str) -> 'WorkflowBuilder':
        """
        Add a text action.

        Args:
            text: Text content

        Returns:
            Self for chaining
        """
        return self.add_action(TextAction(text))

    def add_comment(self, comment: str) -> 'WorkflowBuilder':
        """
        Add a comment.

        Args:
            comment: Comment text

        Returns:
            Self for chaining
        """
        return self.add_action(CommentAction(comment))

    def add_notification(self, body: str, title: Optional[str] = None) -> 'WorkflowBuilder':
        """
        Add a notification action.

        Args:
            body: Notification body
            title: Optional notification title

        Returns:
            Self for chaining
        """
        return self.add_action(NotificationAction(body, title))

    def add_script(self, script: str, shell: str = '/bin/bash') -> 'WorkflowBuilder':
        """
        Add a shell script action.

        Args:
            script: Shell script to execute
            shell: Path to shell

        Returns:
            Self for chaining
        """
        return self.add_action(ScriptAction(script, shell))

    def add_clipboard(self, mode: str = 'Get') -> 'WorkflowBuilder':
        """
        Add clipboard action.

        Args:
            mode: 'Get' or 'Set'

        Returns:
            Self for chaining
        """
        return self.add_action(ClipboardAction(mode))

    def add_variable(self, name: str, set_value: bool = True) -> 'WorkflowBuilder':
        """
        Add variable action.

        Args:
            name: Variable name
            set_value: True to set, False to get

        Returns:
            Self for chaining
        """
        if set_value:
            return self.add_action(SetVariableAction(name))
        else:
            return self.add_action(GetVariableAction(name))

    def add_url(self, url: str, open_it: bool = False) -> 'WorkflowBuilder':
        """
        Add URL action.

        Args:
            url: URL to use
            open_it: Whether to also open the URL

        Returns:
            Self for chaining
        """
        self.add_action(URLAction(url))
        if open_it:
            self.add_action(OpenURLAction())
        return self

    def set_icon(self, glyph_number: int = 59511, color: int = 4282601983) -> 'WorkflowBuilder':
        """
        Set workflow icon.

        Args:
            glyph_number: SF Symbol glyph number
            color: Icon color (RGBA integer)

        Returns:
            Self for chaining
        """
        if 'icon' not in self.metadata:
            self.metadata['icon'] = {}

        self.metadata['icon']['glyph_number'] = glyph_number
        self.metadata['icon']['start_color'] = color
        return self

    def build(self) -> Dict[str, Any]:
        """
        Build the workflow dictionary.

        Returns:
            Complete workflow plist dictionary
        """
        actions_list = [action.to_dict() for action in self.actions]
        return create_shortcut_plist(actions_list, self.metadata)

    def save(self, file_path: str) -> None:
        """
        Build and save the workflow to a .shortcut file.

        Args:
            file_path: Path where to save the file
        """
        workflow_dict = self.build()
        write_shortcut_file(workflow_dict, file_path)


# Convenience functions for common workflows

def create_text_notification(text: str, title: str = "Shortcut") -> WorkflowBuilder:
    """
    Create a simple text-to-notification workflow.

    Args:
        text: Text to show in notification
        title: Notification title

    Returns:
        WorkflowBuilder instance
    """
    return WorkflowBuilder("Text Notification").add_text(text).add_notification(text, title)


def create_script_runner(script: str, notify_result: bool = True) -> WorkflowBuilder:
    """
    Create a script runner workflow.

    Args:
        script: Shell script to run
        notify_result: Whether to show result in notification

    Returns:
        WorkflowBuilder instance
    """
    builder = WorkflowBuilder("Script Runner").add_script(script)

    if notify_result:
        builder.add_notification("Script completed: {{result}}", "Script Result")

    return builder


def create_url_opener(url: str) -> WorkflowBuilder:
    """
    Create a URL opener workflow.

    Args:
        url: URL to open

    Returns:
        WorkflowBuilder instance
    """
    return WorkflowBuilder("URL Opener").add_url(url, open_it=True)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build shortcuts workflows")
    parser.add_argument('--output', required=True, help='Output .shortcut file')
    parser.add_argument('--type', choices=['text', 'script', 'url'],
                       default='text', help='Type of workflow to create')
    parser.add_argument('--content', required=True, help='Content (text, script, or URL)')
    parser.add_argument('--title', default='Shortcut', help='Title for notifications')

    args = parser.parse_args()

    try:
        if args.type == 'text':
            builder = create_text_notification(args.content, args.title)
        elif args.type == 'script':
            builder = create_script_runner(args.content)
        elif args.type == 'url':
            builder = create_url_opener(args.content)
        else:
            raise ValueError(f"Unknown type: {args.type}")

        builder.save(args.output)
        print(f"✓ Workflow saved to: {args.output}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
