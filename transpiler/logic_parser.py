"""
Aura Logic Parser - Parses English logic commands into AST
Handles: Variables, Conditions, Loops, Functions, Math
"""

import re
from typing import List, Optional, Tuple
from .ast_nodes import (
    ASTNode, VariableNode, PrintNode, BinaryOpNode,
    IfNode, LoopNode, FunctionDefNode, FunctionCallNode, Program
)
from .ui_nodes import (
    ScreenNode, ColumnNode, RowNode, StackNode,
    TextNode, ButtonNode, InputNode, WhenClickedNode
)


class LogicParser:
    """Parser for Aura Core logic commands"""

    def __init__(self):
        self.current_line = 0

    def parse_file(self, filepath: str) -> Program:
        """Parse .aura file into AST"""
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        statements = self._parse_lines(lines)
        return Program(statements=statements)

    def _parse_lines(self, lines: List[str], parent_indent: int = 0) -> List[ASTNode]:
        """Parse lines with indentation awareness"""
        statements = []
        i = 0

        while i < len(lines):
            raw_line = lines[i]
            line = raw_line.strip()
            self.current_line = i + 1

            # Skip empty lines and comments
            if not line or line.startswith('#'):
                i += 1
                continue

            # Calculate indentation
            indent = len(raw_line) - len(raw_line.lstrip())

            # If indent is less than parent, we've exited the block
            if indent < parent_indent:
                break

            # Skip if this line is part of a nested block (handled by parent)
            if indent > parent_indent:
                i += 1
                continue

            # Try to parse the line
            node = self._parse_line(line, i + 1, lines, i)
            if node:
                statements.append(node)
                # If it's a block statement (if, loop, function), skip the parsed lines
                if isinstance(node, (IfNode, LoopNode, FunctionDefNode)):
                    # Find how many lines were consumed
                    consumed = self._count_block_lines(lines[i:], indent)
                    i += consumed
                    continue

            i += 1

        return statements

    def _count_block_lines(self, lines: List[str], base_indent: int) -> int:
        """Count how many lines belong to a block"""
        count = 1  # Include the header line
        for line in lines[1:]:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                count += 1
                continue
            indent = len(line) - len(line.lstrip())
            if indent <= base_indent and stripped:
                if not stripped.startswith('else'):
                    break
            count += 1
        return count

    def _parse_line(self, line: str, line_num: int, all_lines: List[str], current_idx: int) -> Optional[ASTNode]:
        """Parse a single line into an AST node"""

        # Variable: set score to 10
        if match := re.match(r"set\s+(\w+)\s+to\s+(.+)", line, re.IGNORECASE):
            var_name = match.group(1)
            value_expr = match.group(2).strip()
            value = self._parse_value(value_expr)
            return VariableNode(line_number=line_num, raw_line=line, name=var_name, value=value)

        # Print: print "Hello" or print score
        if match := re.match(r"print\s+(.+)", line, re.IGNORECASE):
            content_expr = match.group(1).strip()
            content = self._parse_value(content_expr)
            return PrintNode(line_number=line_num, raw_line=line, content=content)

        # If statement: if score > 5
        if match := re.match(r"if\s+(.+)", line, re.IGNORECASE):
            condition_expr = match.group(1).strip()
            condition = self._parse_condition(condition_expr)

            # Parse the if body and else body
            indent = len(all_lines[current_idx]) - \
                len(all_lines[current_idx].lstrip())
            body, else_body = self._parse_if_block(
                all_lines[current_idx + 1:], indent)

            return IfNode(
                line_number=line_num,
                raw_line=line,
                condition=condition,
                body=body,
                else_body=else_body
            )

        # Loop: repeat 5 times
        if match := re.match(r"repeat\s+(\d+)\s+times?", line, re.IGNORECASE):
            count = int(match.group(1))

            # Parse the loop body
            indent = len(all_lines[current_idx]) - \
                len(all_lines[current_idx].lstrip())
            body = self._parse_lines(
                all_lines[current_idx + 1:], parent_indent=indent + 4)

            return LoopNode(line_number=line_num, raw_line=line, count=count, body=body)

        # Function definition: define function greet
        if match := re.match(r"define\s+function\s+(\w+)", line, re.IGNORECASE):
            func_name = match.group(1)

            # Parse the function body
            indent = len(all_lines[current_idx]) - \
                len(all_lines[current_idx].lstrip())
            body = self._parse_lines(
                all_lines[current_idx + 1:], parent_indent=indent + 4)

            return FunctionDefNode(line_number=line_num, raw_line=line, name=func_name, body=body)

        # Function call: call function greet
        if match := re.match(r"call\s+function\s+(\w+)", line, re.IGNORECASE):
            func_name = match.group(1)
            return FunctionCallNode(line_number=line_num, raw_line=line, name=func_name)

        # === PHASE 3.1: VISUAL DSL ===

        # Screen (root UI container)
        if line.lower() == 'screen':
            indent = len(all_lines[current_idx]) - \
                len(all_lines[current_idx].lstrip())
            children = self._parse_lines(
                all_lines[current_idx + 1:], parent_indent=indent + 4)
            return ScreenNode(children=children)

        # Column layout
        if line.lower() == 'column':
            indent = len(all_lines[current_idx]) - \
                len(all_lines[current_idx].lstrip())
            children = self._parse_lines(
                all_lines[current_idx + 1:], parent_indent=indent + 4)
            return ColumnNode(children=children)

        # Row layout
        if line.lower() == 'row':
            indent = len(all_lines[current_idx]) - \
                len(all_lines[current_idx].lstrip())
            children = self._parse_lines(
                all_lines[current_idx + 1:], parent_indent=indent + 4)
            return RowNode(children=children)

        # Stack layout
        if line.lower() == 'stack':
            indent = len(all_lines[current_idx]) - \
                len(all_lines[current_idx].lstrip())
            children = self._parse_lines(
                all_lines[current_idx + 1:], parent_indent=indent + 4)
            return StackNode(children=children)

        # Text: text "Hello" or text score
        if match := re.match(r"text\s+(.+)", line, re.IGNORECASE):
            value_expr = match.group(1).strip()

            # Check if it's a literal string or variable
            if (value_expr.startswith('"') and value_expr.endswith('"')) or \
               (value_expr.startswith("'") and value_expr.endswith("'")):
                # Literal text
                text_value = value_expr[1:-1]  # Remove quotes
                return TextNode(value=text_value, is_binding=False)
            else:
                # Variable binding
                return TextNode(value=value_expr, is_binding=True)

        # Button: button "Click Me"
        if match := re.match(r"button\s+(.+)", line, re.IGNORECASE):
            label_expr = match.group(1).strip()

            # Remove quotes from label
            if (label_expr.startswith('"') and label_expr.endswith('"')) or \
               (label_expr.startswith("'") and label_expr.endswith("'")):
                label = label_expr[1:-1]
            else:
                label = label_expr

            # Check if next lines contain 'when clicked'
            indent = len(all_lines[current_idx]) - \
                len(all_lines[current_idx].lstrip())
            on_click = None

            # Look for 'when clicked' in next line
            if current_idx + 1 < len(all_lines):
                next_line = all_lines[current_idx + 1].strip()
                if next_line.lower() == 'when clicked':
                    # Parse the handler body
                    handler_indent = len(
                        all_lines[current_idx + 1]) - len(all_lines[current_idx + 1].lstrip())
                    on_click = self._parse_lines(
                        all_lines[current_idx + 2:], parent_indent=handler_indent + 4)

            return ButtonNode(label=label, on_click=on_click)

        # Input: input username
        if match := re.match(r"input\s+(\w+)", line, re.IGNORECASE):
            var_name = match.group(1)
            return InputNode(binding=var_name)

        return None

    def _parse_if_block(self, lines: List[str], base_indent: int) -> Tuple[List[ASTNode], Optional[List[ASTNode]]]:
        """Parse if body and optional else body"""
        if_body = []
        else_body = None
        else_start = None

        # Find where 'else' starts
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            indent = len(line) - len(line.lstrip())
            if indent == base_indent and stripped.lower() == 'else':
                else_start = i
                break
            if indent < base_indent:
                break

        # Parse if body
        if_lines = lines[:else_start] if else_start else lines
        if_body = self._parse_lines(if_lines, parent_indent=base_indent + 4)

        # Parse else body
        if else_start is not None:
            else_lines = lines[else_start + 1:]
            else_body = self._parse_lines(
                else_lines, parent_indent=base_indent + 4)

        return if_body, else_body

    def _parse_value(self, expr: str):
        """Parse a value (literal, variable, or expression)"""
        # Check if it's a math expression
        if any(op in expr for op in ['+', '-', '*', '/', '>', '<', '==', '!=']):
            return self._parse_expression(expr)

        # String literal
        if (expr.startswith('"') and expr.endswith('"')) or (expr.startswith("'") and expr.endswith("'")):
            return expr

        # Number
        try:
            if '.' in expr:
                return str(float(expr))
            return str(int(expr))
        except ValueError:
            pass

        # Variable name
        return expr

    def _parse_expression(self, expr: str) -> BinaryOpNode:
        """Parse a binary expression: a + b, x > 5"""
        # Try different operators in order of precedence
        for op in ['==', '!=', '>=', '<=', '>', '<', '+', '-', '*', '/']:
            if op in expr:
                parts = expr.split(op, 1)
                if len(parts) == 2:
                    left = self._parse_value(parts[0].strip())
                    right = self._parse_value(parts[1].strip())
                    return BinaryOpNode(
                        line_number=self.current_line,
                        raw_line=expr,
                        left=left,
                        operator=op,
                        right=right
                    )

        # Fallback: return as-is
        return expr

    def _parse_condition(self, expr: str) -> BinaryOpNode:
        """Parse a condition for if statements"""
        # Handle "score > 5", "x == y", "name is 'John'"

        # Natural language operators
        expr = re.sub(r'\s+is\s+', ' == ', expr, flags=re.IGNORECASE)
        expr = re.sub(r'\s+equals\s+', ' == ', expr, flags=re.IGNORECASE)
        expr = re.sub(r'\s+greater\s+than\s+', ' > ',
                      expr, flags=re.IGNORECASE)
        expr = re.sub(r'\s+less\s+than\s+', ' < ', expr, flags=re.IGNORECASE)

        return self._parse_expression(expr)
