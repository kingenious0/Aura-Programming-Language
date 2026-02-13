"""
UI AST Nodes - Semantic nodes for Aura's visual layer
Pure representation, no rendering logic
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
try:
    from .ast_nodes import ASTNode
except ImportError:
    from ast_nodes import ASTNode


@dataclass
class UINode(ASTNode):
    """Base class for all UI nodes"""
    pass


@dataclass
class ScreenNode(UINode):
    """Root container - top-level UI"""
    children: List[UINode]

    def __repr__(self):
        return f"<Screen with {len(self.children)} children>"


@dataclass
class ColumnNode(UINode):
    """Vertical layout"""
    children: List[UINode]

    def __repr__(self):
        return f"<Column with {len(self.children)} children>"


@dataclass
class RowNode(UINode):
    """Horizontal layout"""
    children: List[UINode]

    def __repr__(self):
        return f"<Row with {len(self.children)} children>"


@dataclass
class StackNode(UINode):
    """Layered layout (z-axis)"""
    children: List[UINode]

    def __repr__(self):
        return f"<Stack with {len(self.children)} children>"


@dataclass
class TextNode(UINode):
    """Display text or variable value"""
    value: str  # Literal text or variable name
    is_binding: bool = False  # True if referencing a variable

    def __repr__(self):
        if self.is_binding:
            return f"<Text binding='{self.value}'>"
        return f"<Text '{self.value}'>"


@dataclass
class ButtonNode(UINode):
    """Interactive button"""
    label: str
    on_click: Optional[List[ASTNode]] = None  # Statements to execute

    def __repr__(self):
        return f"<Button '{self.label}'>"


@dataclass
class InputNode(UINode):
    """Text input field"""
    binding: str  # Variable name to bind to
    placeholder: Optional[str] = None

    def __repr__(self):
        return f"<Input binding='{self.binding}'>"


# UI Event nodes
@dataclass
class WhenClickedNode(ASTNode):
    """Click event handler"""
    statements: List[ASTNode]

    def __repr__(self):
        return f"<WhenClicked: {len(self.statements)} statements>"


@dataclass
class WhenChangedNode(ASTNode):
    """Input change event handler"""
    statements: List[ASTNode]

    def __repr__(self):
        return f"<WhenChanged: {len(self.statements)} statements>"


@dataclass
class WhenHoveredNode(ASTNode):
    """Hover event handler"""
    statements: List[ASTNode]

    def __repr__(self):
        return f"<WhenHovered: {len(self.statements)} statements>"


# === PHASE 6.0: ADVANCED UI ===

@dataclass
class TableNode(UINode):
    """Data table: columns, sortable"""
    columns: List[str]
    is_sortable: bool = False

    def __repr__(self):
        return f"<Table columns={self.columns}>"


@dataclass
class GridNode(UINode):
    """Responsive grid layout"""
    items_expr: str  # e.g. "products from inventory"
    children: List[UINode]

    def __repr__(self):
        return f"<Grid items='{self.items_expr}'>"


@dataclass
class LayoutBlockNode(UINode):
    """Specialized layout area: sidebar, main, footer"""
    block_type: str  # sidebar, main, header, footer
    children: List[UINode]

    def __repr__(self):
        return f"<LayoutBlock '{self.block_type}'>"


@dataclass
class CardNode(UINode):
    """Container with styles like hover, lift"""
    children: List[UINode]
    effects: List[str]  # hover, lift, etc.


@dataclass
class ListNode(UINode):
    """Vertical list of items"""
    items_expr: str
    children: List[UINode]


@dataclass
class PanelNode(UINode):
    """Themed container with title: panel 'Summary'"""
    title: str
    children: List[UINode]


@dataclass
class DividerNode(UINode):
    """Horizontal line separator"""
    pass


@dataclass
class IconNode(UINode):
    """Visual icon: icon 'check-circle'"""
    icon_name: str
    size: str = "medium"
    color: str = "currentColor"


@dataclass
class ImageNode(UINode):
    """Display image: image 'url'"""
    src: str
