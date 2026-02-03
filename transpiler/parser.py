"""
Aura Language Parser Module
Handles parsing of .aura files using regex patterns
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
            'variable': re.compile(
                r"The\s+(?P<object>\w+)'s\s+(?P<property>\w+)\s+is\s+['\"](?P<value>[^'\"]+)['\"]",
                re.IGNORECASE
            ),
            'action': re.compile(
                r"When\s+(?P<event>\w+),\s+(?P<action>display|show|hide|alert)\s+['\"](?P<content>[^'\"]+)['\"]",
                re.IGNORECASE
            ),
            'ui_element': re.compile(
                r"Create\s+a\s+(?P<element>button|input|heading|paragraph|div|span)\s+with\s+the\s+text\s+['\"](?P<text>[^'\"]+)['\"]",
                re.IGNORECASE
            ),
            'theme': re.compile(
                r"Use\s+the\s+(?P<theme>\w+)\s+theme",
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
                        print(f"Warning: Unrecognized command on line {line_num}: {line}")
        
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
        # Try each pattern
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
        has_ui = any(cmd.command_type == 'ui_element' for cmd in commands)
        if not has_ui:
            print("Warning: No UI elements found. The output will be minimal.")
        
        return True
