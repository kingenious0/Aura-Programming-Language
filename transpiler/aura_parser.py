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

            # UI: Create a global navbar with links [Home, About]
            'ui_navbar': re.compile(
                r"Create\s+a\s+global\s+navbar\s+(?:with\s+logo\s+['\"](?P<logo>[^'\"]+)['\"]\s+(?:and\s+)?)?(?:with\s+)?links\s+\[(?P<links>[^\]]+)\]",
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
                r"Create\s+a\s+card\s+with\s+(?:the\s+)?title\s+['\"](?P<title>[^'\"]+)['\"](?:\s+and\s+(?:the\s+)?description\s+['\"](?P<description>[^'\"]+)['\"])?",
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

            # UI: Link to Internal Page
            'ui_link_page': re.compile(
                r"Create\s+a\s+link\s+to\s+page\s+['\"](?P<page>[^'\"]+)['\"]\s+with\s+(?:the\s+)?text\s+['\"](?P<text>[^'\"]+)['\"]",
                re.IGNORECASE
            ),

            # UI: Link to External URL
            'ui_link_url': re.compile(
                r"Create\s+a\s+link\s+to\s+['\"](?P<url>[^'\"]+)['\"]\s+with\s+(?:the\s+)?text\s+['\"](?P<text>[^'\"]+)['\"]",
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

            # === NEW NATURAL LANGUAGE COMMANDS ===

            # Size: Make the button bigger/smaller
            'style_size': re.compile(
                r"Make\s+the\s+(?P<element>\w+)\s+(?P<size>bigger|smaller|large|small)",
                re.IGNORECASE
            ),

            # Styling: Make the button red
            'style_color': re.compile(
                r"Make\s+the\s+(?P<element>\w+)\s+(?P<color>\w+)",
                re.IGNORECASE
            ),

            # Styling: Change the background to purple
            'style_background': re.compile(
                r"Change\s+the\s+background\s+to\s+(?P<color>\w+)",
                re.IGNORECASE
            ),

            # Visibility: Hide the button
            'visibility_hide': re.compile(
                r"Hide\s+the\s+(?P<element>\w+)",
                re.IGNORECASE
            ),

            # Visibility: Show the paragraph
            'visibility_show': re.compile(
                r"Show\s+the\s+(?P<element>\w+)",
                re.IGNORECASE
            ),

            # Formatting: Make the element bold/italic
            'style_format': re.compile(
                r"(?:Make|Set)\s+the\s+(?P<element>\w+)\s+(?:to\s+)?(?P<format>bold|italic|underlined|underline|uppercase|lowercase|capitalize)|(?P<verb>Bold|Italicize|Underline)\s+the\s+(?P<element_verb>\w+)",
                re.IGNORECASE
            ),

            # Formatting: Align the element
            # Supports: "Align the heading center", "Align the heading to the center", "Center the heading"
            'style_align': re.compile(
                r"(?:Align|Center)\s+the\s+(?P<element>\w+)(?:\s+(?:to\s+the\s+)?(?P<align>center|left|right|justify))?",
                re.IGNORECASE
            ),

            # Navigation: Go to page 'about'
            'nav_page': re.compile(
                r"Go\s+to\s+page\s+['\"](?P<page>[^'\"]+)['\"]",
                re.IGNORECASE
            ),

            # Visibility: Toggle the card
            'visibility_toggle': re.compile(
                r"Toggle\s+the\s+(?P<element>\w+)",
                re.IGNORECASE
            ),

            # Text: Change the heading to 'New Title'
            'text_change': re.compile(
                r"Change\s+the\s+(?P<element>\w+)\s+to\s+['\"](?P<text>[^'\"]+)['\"]",
                re.IGNORECASE
            ),

            # Text: Update the paragraph with 'New content'
            'text_update': re.compile(
                r"Update\s+the\s+(?P<element>\w+)\s+with\s+['\"](?P<text>[^'\"]+)['\"]",
                re.IGNORECASE
            ),

            # Text: Set the button text to 'Click Here'
            'text_set': re.compile(
                r"Set\s+the\s+(?P<element>\w+)\s+text\s+to\s+['\"](?P<text>[^'\"]+)['\"]",
                re.IGNORECASE
            ),

            # Text case: Make the text uppercase/lowercase/capitalize
            'text_case': re.compile(
                r"Make\s+the\s+(?P<element>\w+)\s+(?P<case>uppercase|lowercase|capitalize)",
                re.IGNORECASE
            ),

            # Input: Focus on the input
            'input_focus': re.compile(
                r"Focus\s+on\s+the\s+(?P<element>\w+)",
                re.IGNORECASE
            ),

            # Input: Disable the button
            'input_disable': re.compile(
                r"Disable\s+the\s+(?P<element>\w+)",
                re.IGNORECASE
            ),

            # Input: Enable the button
            'input_enable': re.compile(
                r"Enable\s+the\s+(?P<element>\w+)",
                re.IGNORECASE
            ),

            # Input: Check if the input is empty
            'input_validate_empty': re.compile(
                r"Check\s+if\s+the\s+(?P<element>\w+)\s+is\s+empty",
                re.IGNORECASE
            ),

            # Input: Get the value from the input
            'input_get_value': re.compile(
                r"Get\s+the\s+value\s+from\s+the\s+(?P<element>\w+)",
                re.IGNORECASE
            ),

            # Navigation: Go to 'about.html'
            'nav_goto': re.compile(
                r"Go\s+to\s+['\"](?P<url>[^'\"]+)['\"]",
                re.IGNORECASE
            ),

            # Navigation: Open 'contact.html' in new tab
            'nav_open_tab': re.compile(
                r"Open\s+['\"](?P<url>[^'\"]+)['\"]\s+in\s+new\s+tab",
                re.IGNORECASE
            ),

            # Scroll: Scroll to the top/bottom
            'scroll': re.compile(
                r"Scroll\s+to\s+the\s+(?P<position>top|bottom)",
                re.IGNORECASE
            ),

            # Storage: Save the input to storage
            'storage_save': re.compile(
                r"Save\s+the\s+(?P<element>\w+)\s+to\s+storage",
                re.IGNORECASE
            ),

            # Storage: Load data from storage
            'storage_load': re.compile(
                r"Load\s+(?P<key>\w+)\s+from\s+storage",
                re.IGNORECASE
            ),

            # Storage: Clear all saved data
            'storage_clear': re.compile(
                r"Clear\s+all\s+saved\s+data",
                re.IGNORECASE
            ),

            # Clipboard: Copy 'text' to clipboard
            'clipboard_copy': re.compile(
                r"Copy\s+['\"](?P<text>[^'\"]+)['\"]\s+to\s+clipboard",
                re.IGNORECASE
            ),

            # Clipboard: Copy the input value to clipboard
            'clipboard_copy_element': re.compile(
                r"Copy\s+the\s+(?P<element>\w+)\s+(?:value\s+)?to\s+clipboard",
                re.IGNORECASE
            ),

            # Notifications: Show a notification saying 'Welcome!'
            'notification': re.compile(
                r"Show\s+a\s+notification\s+saying\s+['\"](?P<message>[^'\"]+)['\"]",
                re.IGNORECASE
            ),

            # Toast: Display a toast message 'Saved!'
            'toast': re.compile(
                r"Display\s+a\s+toast\s+message\s+['\"](?P<message>[^'\"]+)['\"]",
                re.IGNORECASE
            ),

            # Animation: Fade in the card
            'animate_fade': re.compile(
                r"Fade\s+(?P<direction>in|out)\s+the\s+(?P<element>\w+)",
                re.IGNORECASE
            ),

            # Animation: Slide in the button from left
            'animate_slide': re.compile(
                r"Slide\s+(?P<direction>in|out)\s+the\s+(?P<element>\w+)(?:\s+from\s+(?P<from>left|right|top|bottom))?",
                re.IGNORECASE
            ),

            # Animation: Bounce the heading
            'animate_bounce': re.compile(
                r"Bounce\s+the\s+(?P<element>\w+)",
                re.IGNORECASE
            ),

            # Counter: Create a counter starting at 0
            'counter_create': re.compile(
                r"Create\s+a\s+counter\s+starting\s+at\s+(?P<value>\d+)",
                re.IGNORECASE
            ),

            # Counter: Increase the counter by 1
            'counter_increase': re.compile(
                r"Increase\s+the\s+counter\s+by\s+(?P<amount>\d+)",
                re.IGNORECASE
            ),

            # Counter: Decrease the counter
            'counter_decrease': re.compile(
                r"Decrease\s+the\s+counter(?:\s+by\s+(?P<amount>\d+))?",
                re.IGNORECASE
            ),
        }

    def parse_file(self, filepath: str) -> List[AuraCommand]:
        """
        Parse an Aura file and return a list of commands.
        If the Brain fixes any syntax, it updates the source file automatically.
        """
        commands = []
        modified_lines = []
        corrections_made = False

        try:
            # Read all lines first
            with open(filepath, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            for line_num, original_line_with_newline in enumerate(lines, start=1):
                line = original_line_with_newline.strip()

                # Preserve empty lines and comments in the output
                if not line or line.startswith('#'):
                    modified_lines.append(
                        original_line_with_newline.rstrip('\n'))
                    continue

                # Handle 'then' continuation (logic remains for commands list, but line stays same)
                if line.lower().startswith('then ') and commands:
                    last_cmd = commands[-1]
                    if last_cmd.command_type == 'action_sequence':
                        last_cmd.data['actions'] += ", " + line
                        last_cmd.raw_line += "\n" + line
                        # We don't change the file for 'then' lines, assume they are valid or brain doesn't touch them yet
                        modified_lines.append(line)
                        continue

                command = self._parse_line(line, line_num)
                if command:
                    commands.append(command)
                    modified_lines.append(line)
                else:
                    # 🧠 Aura Brain: Autocorrect
                    corrected = None
                    try:
                        # Lazy import
                        if not hasattr(self, 'brain'):
                            try:
                                from .brain import AuraBrain
                                self.brain = AuraBrain()
                            except ImportError:
                                from brain import AuraBrain
                                self.brain = AuraBrain()

                        corrected = self.brain.fix_syntax(line)
                    except:
                        pass

                    if corrected and corrected != line:
                        # Verify the correction is valid
                        retry_cmd = self._parse_line(corrected, line_num)
                        if retry_cmd:
                            print(
                                f"  ✨ [Aura Brain] Auto-corrected: '{line}' -> '{corrected}'")
                            commands.append(retry_cmd)
                            modified_lines.append(corrected)  # Save the fix
                            corrections_made = True
                            continue

                    # If we couldn't fix it, keep original list
                    print(
                        f"Warning: Unrecognized command on line {line_num}: {line}")
                    modified_lines.append(line)

            # Write improvements back to file if needed
            if corrections_made:
                try:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(modified_lines) + '\n')
                    print(f"  📝 [Source Update] Applied fixes to {filepath}")
                except Exception as e:
                    print(f"  ⚠️ [Error] Could not update source file: {e}")

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

            # Parse clear specific input
            clear_elem_match = re.match(
                r"clear\s+the\s+(?P<element>\w+)", action_str, re.IGNORECASE)
            if clear_elem_match:
                element = clear_elem_match.group(1)
                parsed_actions.append({
                    'type': 'clear_element',
                    'params': {'element': element}
                })
                continue

            # Parse wait X seconds
            wait_match = re.match(
                r"wait\s+(\d+)\s+seconds?", action_str, re.IGNORECASE)
            if wait_match:
                seconds = wait_match.group(1)
                parsed_actions.append({
                    'type': 'wait',
                    'params': {'seconds': seconds}
                })
                continue

            # Parse focus on the element
            focus_match = re.match(
                r"focus\s+on\s+the\s+(\w+)", action_str, re.IGNORECASE)
            if focus_match:
                element = focus_match.group(1)
                parsed_actions.append({
                    'type': 'focus',
                    'params': {'element': element}
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

            # Parse toggle the element
            toggle_match = re.match(
                r"toggle\s+the\s+(\w+)", action_str, re.IGNORECASE)
            if toggle_match:
                element = toggle_match.group(1)
                parsed_actions.append({
                    'type': 'toggle',
                    'params': {'element': element}
                })
                continue

            # Parse copy to clipboard (literal text)
            copy_match = re.match(
                r"copy\s+['\"]([^'\"]+)['\"]\s+to\s+clipboard", action_str, re.IGNORECASE)
            if copy_match:
                text = copy_match.group(1)
                parsed_actions.append({
                    'type': 'copy_clipboard',
                    'params': {'text': text}
                })
                continue

            # Parse copy element to clipboard
            copy_elem_match = re.match(
                r"copy\s+the\s+(\w+)\s+(?:value\s+)?to\s+clipboard", action_str, re.IGNORECASE)
            if copy_elem_match:
                element = copy_elem_match.group(1)
                parsed_actions.append({
                    'type': 'copy_element_clipboard',
                    'params': {'element': element}
                })
                continue

            # Parse scroll to top/bottom
            scroll_match = re.match(
                r"scroll\s+to\s+the\s+(top|bottom)", action_str, re.IGNORECASE)
            if scroll_match:
                position = scroll_match.group(1).lower()
                parsed_actions.append({
                    'type': 'scroll',
                    'params': {'position': position}
                })
                continue

            # Parse go to URL (New Tab)
            goto_new_match = re.match(
                r"go\s+to\s+['\"]([^'\"]+)['\"]\s+in\s+(?:a\s+)?new\s+tab", action_str, re.IGNORECASE)
            if goto_new_match:
                url = goto_new_match.group(1)
                parsed_actions.append({
                    'type': 'navigate_new_tab',
                    'params': {'url': url}
                })
                continue

            # Parse go to URL
            goto_match = re.match(
                r"go\s+to\s+['\"]([^'\"]+)['\"]", action_str, re.IGNORECASE)
            if goto_match:
                url = goto_match.group(1)
                parsed_actions.append({
                    'type': 'navigate',
                    'params': {'url': url}
                })
                continue

            # Parse open in new tab
            newtab_match = re.match(
                r"open\s+['\"]([^'\"]+)['\"]\s+in\s+new\s+tab", action_str, re.IGNORECASE)
            if newtab_match:
                url = newtab_match.group(1)
                parsed_actions.append({
                    'type': 'navigate_new_tab',
                    'params': {'url': url}
                })
                continue

            # Parse change element text
            change_match = re.match(
                r"change\s+the\s+(\w+)\s+to\s+['\"]([^'\"]+)['\"]", action_str, re.IGNORECASE)
            if change_match:
                element = change_match.group(1)
                text = change_match.group(2)
                parsed_actions.append({
                    'type': 'change_text',
                    'params': {'element': element, 'text': text}
                })
                continue

            # Parse update element text (alias for change)
            update_match = re.match(
                r"update\s+the\s+(\w+)\s+with\s+['\"]([^'\"]+)['\"]", action_str, re.IGNORECASE)
            if update_match:
                element = update_match.group(1)
                text = update_match.group(2)
                parsed_actions.append({
                    'type': 'change_text',
                    'params': {'element': element, 'text': text}
                })
                continue

            # Parse disable/enable element
            disable_match = re.match(
                r"(disable|enable)\s+the\s+(\w+)", action_str, re.IGNORECASE)
            if disable_match:
                action_type = disable_match.group(1).lower()
                element = disable_match.group(2)
                parsed_actions.append({
                    'type': action_type,
                    'params': {'element': element}
                })
                continue

            # Parse style color
            style_color_match = re.match(
                r"make\s+the\s+(\w+)\s+(\w+)", action_str, re.IGNORECASE)
            if style_color_match:
                element = style_color_match.group(1)
                color = style_color_match.group(2)
                parsed_actions.append({
                    'type': 'style_color',
                    'params': {'element': element, 'color': color}
                })
                continue

            # Parse fade in/out
            fade_match = re.match(
                r"fade\s+(in|out)\s+the\s+(\w+)", action_str, re.IGNORECASE)
            if fade_match:
                direction = fade_match.group(1).lower()
                element = fade_match.group(2)
                parsed_actions.append({
                    'type': 'fade',
                    'params': {'direction': direction, 'element': element}
                })
                continue

            # If no pattern matches, add as unknown action

            # Formatting: Make it bold
            format_match = re.match(
                r"make\s+the\s+(\w+)\s+(bold|italic|underlined|underline)", action_str, re.IGNORECASE)
            if format_match:
                parsed_actions.append({
                    'type': 'style_format',
                    'params': {'element': format_match.group(1), 'format': format_match.group(2)}
                })
                continue

            # Navigation: Go to page
            page_match = re.match(
                r"go\s+to\s+page\s+['\"]([^'\"]+)['\"]", action_str, re.IGNORECASE)
            if page_match:
                parsed_actions.append({
                    'type': 'navigate_page',
                    'params': {'page': page_match.group(1)}
                })
                continue

            # Navigation: Open link in new tab
            new_tab_match = re.match(
                r"open\s+the\s+link\s+['\"]([^'\"]+)['\"]\s+in\s+a\s+new\s+tab", action_str, re.IGNORECASE)
            if new_tab_match:
                parsed_actions.append({
                    'type': 'navigate_new_tab',
                    'params': {'url': new_tab_match.group(1)}
                })
                continue

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
