"""
Aura Logic Parser - Parses English logic commands into AST
Handles: Variables, Conditions, Loops, Functions, Math
"""

import re
from typing import List, Optional, Tuple
from .ast_nodes import (
    ASTNode, VariableNode, PrintNode, BinaryOpNode,
    IfNode, LoopNode, FunctionDefNode, FunctionCallNode, Program,
    AppNode, PageNode, NavigationNode, LayoutNode, SlotNode,
    AddNode, RemoveNode, FetchNode, NotifyNode
)
from .ui_nodes import (
    ScreenNode, ColumnNode, RowNode, StackNode,
    TextNode, ButtonNode, InputNode, WhenClickedNode,
    TableNode, GridNode, LayoutBlockNode, CardNode, ListNode,
    PanelNode, DividerNode, IconNode, ImageNode
)
from .semantic_nodes import (
    HeroNode, FeatureNode, PricingNode, IntentPageNode,
    CtaNode, BookingNode, ContactNode
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

    def _get_indent(self, line: str) -> int:
        return len(line) - len(line.lstrip())

    def _get_next_indent(self, lines: List[str], current_indent: int) -> int:
        for line in lines:
            if not line.strip() or line.strip().startswith('#'):
                continue
            indent = self._get_indent(line)
            if indent > current_indent:
                return indent
        return current_indent + 2

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
            indent = self._get_indent(raw_line)

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
                # If it's a block statement (if, loop, function, or any with children), skip the parsed lines
                if hasattr(node, 'body') or hasattr(node, 'children') or hasattr(node, 'pages') or hasattr(node, 'statements'):
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

        # === PHASE 6.0: APPLICATION LAYER (High Priority) ===

        # App definition: app "Kingenious Store"
        if match := re.match(r"app\s+[\"']?([^\"']+)[\"']?", line, re.IGNORECASE):
            app_name = match.group(1)
            indent = self._get_indent(all_lines[current_idx])
            next_lines = all_lines[current_idx + 1:]
            child_indent = self._get_next_indent(next_lines, indent)
            pages = self._parse_lines(next_lines, parent_indent=child_indent)
            return AppNode(line_number=line_num, raw_line=line, name=app_name, pages=pages)

        # Page definition: page home [uses layout_name] or page product(id)
        if match := re.match(r"page\s+(\w+)(?:\(([^)]+)\))?(?:\s+uses\s+(\w+))?", line, re.IGNORECASE):
            page_name = match.group(1)
            params_raw = match.group(2)
            layout = match.group(3)
            params = [p.strip()
                      for p in params_raw.split(',')] if params_raw else []
            indent = self._get_indent(all_lines[current_idx])
            next_lines = all_lines[current_idx + 1:]
            child_indent = self._get_next_indent(next_lines, indent)
            children = self._parse_lines(
                next_lines, parent_indent=child_indent)
            return PageNode(line_number=line_num, raw_line=line, name=page_name, layout=layout, children=children, params=params)

        # Layout definition: layout shop_layout
        if match := re.match(r"layout\s+(\w+)", line, re.IGNORECASE):
            layout_name = match.group(1)
            indent = self._get_indent(all_lines[current_idx])
            next_lines = all_lines[current_idx + 1:]
            child_indent = self._get_next_indent(next_lines, indent)
            children = self._parse_lines(
                next_lines, parent_indent=child_indent)
            return LayoutNode(line_number=line_num, raw_line=line, name=layout_name, children=children)

        # Variable: set score to 10
        if match := re.match(r"set\s+(\w+)\s+to\s+(.+)", line, re.IGNORECASE):
            var_name = match.group(1)
            value_expr = match.group(2).strip()

            # Special case for fetch: set products to fetch from "inventory.json"
            if fetch_match := re.match(r"fetch\s+from\s+[\"']?([^\"']+)[\"']?", value_expr, re.IGNORECASE):
                value = FetchNode(line_number=line_num,
                                  raw_line=line, source=fetch_match.group(1))
            elif value_expr == '[]':
                value = []
            else:
                value = self._parse_value(value_expr)
            return VariableNode(line_number=line_num, raw_line=line, name=var_name, value=value)

        # Print: print "Hello" or print score
        if match := re.match(r"print\s+(.+)", line, re.IGNORECASE):
            content_expr = match.group(1).strip()
            content = self._parse_value(content_expr)
            return PrintNode(line_number=line_num, raw_line=line, content=content)

        # If statement: if cart is empty
        if match := re.match(r"if\s+(.+)", line, re.IGNORECASE):
            condition_expr = match.group(1).strip()

            # Handle "is empty" semantic
            if "is empty" in condition_expr.lower():
                var_name = condition_expr.lower().replace("is empty", "").strip()
                condition = BinaryOpNode(
                    line_number=line_num, raw_line=line, left=f"{var_name}.length", operator="==", right="0")
            else:
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

        # === PHASE 4.0/5.0: SEMANTIC INTENT ===

        # Landing Page/Website Intent: booking website for a barber shop
        if match := re.match(r"(?:landing page|website|official website|booking website|product website|application|app)\s+(?:for\s+)?(.+)", line, re.IGNORECASE):
            intent_text = line.strip()  # Aura 5.0: Pass the full intent to the DIE
            indent = len(all_lines[current_idx]) - \
                len(all_lines[current_idx].lstrip())
            sections = self._parse_lines(
                all_lines[current_idx + 1:], parent_indent=indent + 4)
            return IntentPageNode(line_number=line_num, raw_line=line, intent_text=intent_text, sections=sections)

        # Hero Section: hero "Build with Aura" subtitle "English to Web Apps"
        if match := re.match(r"(?:hero|hero section)\s+\"([^\"]+)\"(?:\s+subtitle\s+\"([^\"]+)\")?(?:\s+button\s+\"([^\"]+)\")?", line, re.IGNORECASE):
            title = match.group(1)
            subtitle = match.group(2)
            cta = match.group(3)
            return HeroNode(line_number=line_num, raw_line=line, title=title, subtitle=subtitle, cta_text=cta)

        # Feature: feature "AI Parsing" description "Smart code generation"
        if match := re.match(r"(?:feature|feature section)\s+\"([^\"]+)\"(?:\s+description\s+\"([^\"]+)\")?", line, re.IGNORECASE):
            title = match.group(1)
            desc = match.group(2)
            return FeatureNode(line_number=line_num, raw_line=line, title=title, description=desc)

        # Pricing: pricing "Pro Plan" at "$20/mo" features "AI, Priority, Custom"
        if match := re.match(r"pricing\s+\"([^\"]+)\"\s+(?:at\s+)?\"([^\"]+)\"(?:\s+features\s+\"([^\"]+)\")?", line, re.IGNORECASE):
            plan = match.group(1)
            price = match.group(2)
            features_raw = match.group(3)
            features = [f.strip() for f in features_raw.split(',')
                        ] if features_raw else []
            return PricingNode(line_number=line_num, raw_line=line, plan_name=plan, price=price, features=features)

        # Call to Action: cta "Ready to build?" button "Get Started"
        if match := re.match(r"cta\s+\"([^\"]+)\"(?:\s+button\s+\"([^\"]+)\")?", line, re.IGNORECASE):
            return CtaNode(line_number=line_num, raw_line=line, title=match.group(1), button_text=match.group(2) or "Join")

        # Booking: booking "Haircut" price "$30"
        if match := re.match(r"booking\s+\"([^\"]+)\"(?:\s+price\s+\"([^\"]+)\")?", line, re.IGNORECASE):
            return BookingNode(line_number=line_num, raw_line=line, service_name=match.group(1), price_prefix=match.group(2))

        # Contact: contact us at "hello@aura.lang"
        if match := re.match(r"(?:contact|contact us)(?:\s+at\s+)?\"([^\"]+)\"?", line, re.IGNORECASE):
            return ContactNode(line_number=line_num, raw_line=line, email=match.group(1) if match.groups() else None)

        # === PHASE 3.1: VISUAL DSL ===

        # Screen (root UI container)
        if line.lower() == 'screen':
            indent = len(all_lines[current_idx]) - \
                len(all_lines[current_idx].lstrip())
            indent = self._get_indent(all_lines[current_idx])
            next_lines = all_lines[current_idx + 1:]
            child_indent = self._get_next_indent(next_lines, indent)
            children = self._parse_lines(
                next_lines, parent_indent=child_indent)
            return ScreenNode(line_number=line_num, raw_line=line, children=children)

        # Column layout
        if match := re.match(r"(?:column|col)", line, re.IGNORECASE):
            indent = self._get_indent(all_lines[current_idx])
            next_lines = all_lines[current_idx + 1:]
            child_indent = self._get_next_indent(next_lines, indent)
            children = self._parse_lines(
                next_lines, parent_indent=child_indent)
            return ColumnNode(line_number=line_num, raw_line=line, children=children)

        # Row layout or Columns
        if match := re.match(r"(?:row|columns\s+(\d+))", line, re.IGNORECASE):
            indent = self._get_indent(all_lines[current_idx])
            next_lines = all_lines[current_idx + 1:]
            child_indent = self._get_next_indent(next_lines, indent)
            children = self._parse_lines(
                next_lines, parent_indent=child_indent)
            return RowNode(line_number=line_num, raw_line=line, children=children)

        # Stack layout
        if line.lower() == 'stack':
            indent = self._get_indent(all_lines[current_idx])
            next_lines = all_lines[current_idx + 1:]
            child_indent = self._get_next_indent(next_lines, indent)
            children = self._parse_lines(
                next_lines, parent_indent=child_indent)
            return StackNode(line_number=line_num, raw_line=line, children=children)

        # Text: text "Hello" or text score
        if match := re.match(r"text\s+(.+)", line, re.IGNORECASE):
            value_expr = match.group(1).strip()

            # Check if it's a literal string or variable
            if (value_expr.startswith('"') and value_expr.endswith('"')) or \
               (value_expr.startswith("'") and value_expr.endswith("'")):
                # Literal text
                text_value = value_expr[1:-1]  # Remove quotes
                return TextNode(line_number=line_num, raw_line=line, value=text_value, is_binding=False)
            else:
                # Variable binding
                return TextNode(line_number=line_num, raw_line=line, value=value_expr, is_binding=True)

        # Slot placeholder: slot
        # Slot placeholder: slot
        if line.lower().strip() == 'slot' or line.lower().startswith('slot '):
            return SlotNode(line_number=line_num, raw_line=line)

        # Button: button "Click Me" [goes to shop]
        if match := re.match(r"button\s+[\"']?([^\"']+)[\"']?(?:\s+goes\s+to\s+(\w+))?", line, re.IGNORECASE):
            label = match.group(1)
            target = match.group(2)

            # Check if next lines contain 'when clicked'
            indent = len(all_lines[current_idx]) - \
                len(all_lines[current_idx].lstrip())
            on_click = []

            if target:
                on_click.append(NavigationNode(
                    line_number=line_num, raw_line=line, target_page=target))

            # Look for 'when clicked' in next line
            if current_idx + 1 < len(all_lines):
                next_raw = all_lines[current_idx + 1]
                next_line = next_raw.strip()
                next_indent = len(next_raw) - len(next_raw.lstrip())
                if next_line.lower() == 'when clicked' and next_indent >= indent:
                    handler_indent = next_indent
                    on_click.extend(self._parse_lines(
                        all_lines[current_idx + 2:], parent_indent=handler_indent + 4))

            return ButtonNode(line_number=line_num, raw_line=line, label=label, on_click=on_click)

        # Table: table orders
        if match := re.match(r"table\s+(\w+)", line, re.IGNORECASE):
            # Very simple for now, can expand later
            return TableNode(line_number=line_num, raw_line=line, columns=[])

        # Grid: grid products from inventory [columns 3]
        if match := re.match(r"grid\s+(.+?)(?:\s+columns\s+(\d+))?$", line, re.IGNORECASE):
            items_expr = match.group(1)
            # col_count = match.group(2) # can store in node later if needed
            indent = self._get_indent(all_lines[current_idx])
            next_lines = all_lines[current_idx + 1:]
            child_indent = self._get_next_indent(next_lines, indent)
            children = self._parse_lines(
                next_lines, parent_indent=child_indent)
            return GridNode(line_number=line_num, raw_line=line, items_expr=items_expr, children=children)

        # Card: card hover lift
        if match := re.match(r"card(?:\s+(.+))?", line, re.IGNORECASE):
            effects_str = match.group(1) or ""
            effects = effects_str.split()
            indent = self._get_indent(all_lines[current_idx])
            next_lines = all_lines[current_idx + 1:]
            child_indent = self._get_next_indent(next_lines, indent)
            children = self._parse_lines(
                next_lines, parent_indent=child_indent)
            return CardNode(line_number=line_num, raw_line=line, children=children, effects=effects)

        # List Repeater: list cart
        if match := re.match(r"list\s+(.+)", line, re.IGNORECASE):
            items_expr = match.group(1)
            indent = self._get_indent(all_lines[current_idx])
            next_lines = all_lines[current_idx + 1:]
            child_indent = self._get_next_indent(next_lines, indent)
            children = self._parse_lines(
                next_lines, parent_indent=child_indent)
            return ListNode(line_number=line_num, raw_line=line, items_expr=items_expr, children=children)

        # Add: add item to cart
        if match := re.match(r"add\s+(.+)\s+to\s+(.+)", line, re.IGNORECASE):
            return AddNode(line_number=line_num, raw_line=line, item=match.group(1), target=match.group(2))

        # Remove: remove item from cart
        if match := re.match(r"remove\s+(.+)\s+from\s+(.+)", line, re.IGNORECASE):
            return RemoveNode(line_number=line_num, raw_line=line, item=match.group(1), target=match.group(2))

        # Notify: notify "Added to cart"
        if match := re.match(r"notify\s+(.+)", line, re.IGNORECASE):
            msg = self._parse_value(match.group(1))
            return NotifyNode(line_number=line_num, raw_line=line, message=msg)

        # Panel: panel "Summary"
        if match := re.match(r"panel\s+[\"']?([^\"']+)[\"']?", line, re.IGNORECASE):
            title = match.group(1)
            indent = self._get_indent(all_lines[current_idx])
            next_lines = all_lines[current_idx + 1:]
            child_indent = self._get_next_indent(next_lines, indent)
            children = self._parse_lines(
                next_lines, parent_indent=child_indent)
            return PanelNode(line_number=line_num, raw_line=line, title=title, children=children)

        # Divider: divider
        if line.lower().strip() == 'divider':
            return DividerNode(line_number=line_num, raw_line=line)

        # Icon: icon "check-circle" [size "huge"] [color "green"]
        if match := re.match(r"icon\s+[\"8]?([^\"']+)[\"']?(?:\s+size\s+[\"']?(\w+)[\"']?)?(?:\s+color\s+[\"']?(\w+)[\"']?)?", line, re.IGNORECASE):
            return IconNode(line_number=line_num, raw_line=line, icon_name=match.group(1), size=match.group(2) or "medium", color=match.group(3) or "currentColor")

        # Image: image "url" or image item.image
        if match := re.match(r"image\s+(.+)", line, re.IGNORECASE):
            return ImageNode(line_number=line_num, raw_line=line, src=match.group(1).strip())

        # Layout Blocks: sidebar, main, header, footer
        if match := re.match(r"(sidebar|main|header|footer)", line, re.IGNORECASE):
            block_type = match.group(1).lower()
            indent = self._get_indent(all_lines[current_idx])
            next_lines = all_lines[current_idx + 1:]
            child_indent = self._get_next_indent(next_lines, indent)
            children = self._parse_lines(
                next_lines, parent_indent=child_indent)
            return LayoutBlockNode(line_number=line_num, raw_line=line, block_type=block_type, children=children)

        # Input: input username
        if match := re.match(r"input\s+(\w+)", line, re.IGNORECASE):
            var_name = match.group(1)
            return InputNode(line_number=line_num, raw_line=line, binding=var_name)

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
