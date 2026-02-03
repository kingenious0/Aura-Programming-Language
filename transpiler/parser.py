"""
Aura Language Parser Module
Handles parsing of .aura files using regex patterns
Supports: Variables, Actions, UI Elements, Themes, Images, Cards, Layout, and more
"""

import re
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class AuraCommand:
    """Represents a parsed Aura command"""
    command_type: str
    data: Dict[str, Any]
    line_number: int
    raw_line: str


class AuraParser:
    """Parser for Aura programming language"""

    def __init__(self):
        # Define regex patterns for each command type
        self.patterns = {
            # Variables: The user's name is 'John'
            'variable': re.compile(
                r"The\s+(?P<object>\w+)'s\s+(?P<property>\w+)\s+is\s+['\"](?P<value>[^'\"]+)['\"]",
                re.IGNORECASE
            ),

            # Actions with 'then' support: When clicked, display 'Success!', then clear the input, then refresh the page
            'action_sequence': re.compile(
                r"When\s+(?P<event>\w+),\s*(?P<actions>.+)",
                re.IGNORECASE
            ),

            # Modifier: And refresh the page (kept for backward compatibility)
            'modifier_refresh': re.compile(
                r"And\s+refresh\s+the\s+page",
                re.IGNORECASE
            ),

            # UI: Create a button with the text 'Submit'
            'ui_button': re.compile(
                r"Create\s+a\s+button\s+with\s+the\s+text\s+['\"](?P<text>[^'\"]+)['\"]",
                re.IGNORECASE
            ),

            # UI: Create a heading with the text 'Welcome'
            'ui_heading': re.compile(
                r"Create\s+a\s+heading\s+with\s+the\s+text\s+['\"](?P<text>[^'\"]+)['\"]",
                re.IGNORECASE
            ),

            # UI: Create a paragraph with the text 'Hello'
            'ui_paragraph': re.compile(
                r"Create\s+a\s+paragraph\s+with\s+the\s+text\s+['\"](?P<text>[^'\"]+)['\"]",
                re.IGNORECASE
            ),

            # UI: Create an input with the text 'Enter name'
            'ui_input': re.compile(
                r"Create\s+an?\s+input\s+with\s+the\s+text\s+['\"](?P<text>[^'\"]+)['\"]",
                re.IGNORECASE
            ),

            # UI: Create a card with the title 'Title' and description 'Desc'
            'ui_card': re.compile(
                r"Create\s+a\s+card\s+with\s+the\s+title\s+['\"](?P<title>[^'\"]+)['\"](?:\s+and\s+description\s+['\"](?P<description>[^'\"]+)['\"])?",
                re.IGNORECASE
            ),

            # UI: Create an image with the url 'https://...' and alt 'Description'
            'ui_image': re.compile(
                r"Create\s+an?\s+image\s+with\s+the\s+url\s+['\"](?P<url>[^'\"]+)['\"](?:\s+and\s+alt\s+['\"](?P<alt>[^'\"]+)['\"])?",
                re.IGNORECASE
            ),

            # UI: Create an image from 'path/to/image.jpg'
            'ui_image_simple': re.compile(
                r"Create\s+an?\s+image\s+from\s+['\"](?P<url>[^'\"]+)['\"]",
                re.IGNORECASE
            ),

            # Theme: Use the dark theme
            'theme': re.compile(
                r"Use\s+the\s+(?P<theme>dark|light|default)\s+theme",
                re.IGNORECASE
            ),

            # Layout: Put the button in the middle
            'layout_center': re.compile(
                r"Put\s+the\s+(?P<element>\w+)\s+in\s+the\s+(middle|center)",
                re.IGNORECASE
            ),

            # Networking: Ask "api.com" for the weather
            'network_request': re.compile(
                r"Ask\s+['\"](?P<url>[^'\"]+)['\"]\s+for\s+(?P<data>\w+)",
                re.IGNORECASE
            ),

            # Deployment: Go live
            'deployment': re.compile(
                r"Go\s+live",
                re.IGNORECASE
            ),
        }

    def parse_file(self, filepath: str) -> List[AuraCommand]:
        """
        Parse an Aura file and return a list of commands

        Args:
            filepath: Path to the .aura file

        Returns:
            List of AuraCommand objects
        """
        commands = []

        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, start=1):
                    line = line.strip()

                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue

                    command = self._parse_line(line, line_num)
                    if command:
                        commands.append(command)
                    else:
                        print(
                            f"Warning: Unrecognized command on line {line_num}: {line}")

        except FileNotFoundError:
            raise FileNotFoundError(f"Aura file not found: {filepath}")
        except Exception as e:
            raise Exception(f"Error reading file {filepath}: {str(e)}")

        return commands

    def _parse_line(self, line: str, line_num: int) -> AuraCommand:
        """
        Parse a single line and return an AuraCommand

        Args:
            line: The line to parse
            line_num: Line number in the file

        Returns:
            AuraCommand object or None if no match
        """
        # Try each pattern in priority order
        for cmd_type, pattern in self.patterns.items():
            match = pattern.match(line)
            if match:
                return AuraCommand(
                    command_type=cmd_type,
                    data=match.groupdict(),
                    line_number=line_num,
                    raw_line=line
                )

        return None

    def parse_action_sequence(self, actions_string: str) -> List[Dict[str, Any]]:
        """
        Parse a sequence of actions separated by 'then'

        Args:
            actions_string: String containing actions like "display 'X', then clear the input, then refresh the page"

        Returns:
            List of action dictionaries with 'type' and 'params'
        """
        # Split by ', then ' to get individual actions
        action_parts = re.split(
            r',\s*then\s+', actions_string, flags=re.IGNORECASE)

        parsed_actions = []

        for action_str in action_parts:
            action_str = action_str.strip()

            # Parse display/alert with quoted content
            display_match = re.match(
                r"(display|alert)\s+['\"]([^'\"]+)['\"]", action_str, re.IGNORECASE)
            if display_match:
                action_type = display_match.group(1).lower()
                content = display_match.group(2)
                parsed_actions.append({
                    'type': action_type,
                    'params': {'content': content}
                })
                continue

            # Parse refresh the page
            if re.match(r"refresh\s+the\s+page", action_str, re.IGNORECASE):
                parsed_actions.append({
                    'type': 'refresh',
                    'params': {}
                })
                continue

            # Parse clear the input
            if re.match(r"clear\s+the\s+input", action_str, re.IGNORECASE):
                parsed_actions.append({
                    'type': 'clear_input',
                    'params': {}
                })
                continue

            # Parse show/hide element
            show_match = re.match(
                r"(show|hide)\s+the\s+(\w+)", action_str, re.IGNORECASE)
            if show_match:
                action_type = show_match.group(1).lower()
                element = show_match.group(2)
                parsed_actions.append({
                    'type': action_type,
                    'params': {'element': element}
                })
                continue

            # If no pattern matches, add as unknown action
            parsed_actions.append({
                'type': 'unknown',
                'params': {'raw': action_str}
            })

        return parsed_actions

    def validate_commands(self, commands: List[AuraCommand]) -> bool:
        """
        Validate the parsed commands

        Args:
            commands: List of AuraCommand objects

        Returns:
            True if valid, raises exception otherwise
        """
        if not commands:
            raise ValueError("No valid commands found in the file")

        # Check if at least one UI element exists
        ui_types = ['ui_button', 'ui_heading', 'ui_paragraph',
                    'ui_input', 'ui_card', 'ui_image', 'ui_image_simple']
        has_ui = any(cmd.command_type in ui_types for cmd in commands)
        if not has_ui:
            print("Warning: No UI elements found. The output will be minimal.")

        return True
