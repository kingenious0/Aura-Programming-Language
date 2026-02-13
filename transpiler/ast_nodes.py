"""
Aura AST (Abstract Syntax Tree) Node Definitions
Represents the semantic structure of Aura programs
"""

from dataclasses import dataclass
from typing import List, Any, Optional


@dataclass
class ASTNode:
    """Base class for all AST nodes"""
    line_number: int
    raw_line: str


@dataclass
class VariableNode(ASTNode):
    """Variable assignment: set score to 10"""
    name: str
    value: Any  # Can be literal, expression, or another variable


@dataclass
class PrintNode(ASTNode):
    """Print statement: print "Hello" or print score"""
    content: Any  # String literal or variable name


@dataclass
class BinaryOpNode(ASTNode):
    """Binary operation: x + y, price * quantity"""
    left: Any
    operator: str  # +, -, *, /, >, <, ==, >=, <=, !=
    right: Any


@dataclass
class IfNode(ASTNode):
    """Conditional statement"""
    condition: BinaryOpNode
    body: List[ASTNode]
    else_body: Optional[List[ASTNode]] = None


@dataclass
class LoopNode(ASTNode):
    """Loop statement: repeat 5 times"""
    count: int
    body: List[ASTNode]


@dataclass
class FunctionDefNode(ASTNode):
    """Function definition: define function greet"""
    name: str
    body: List[ASTNode]


@dataclass
class FunctionCallNode(ASTNode):
    """Function call: call function greet"""
    name: str


@dataclass
class NavigationNode(ASTNode):
    """Navigation target: goes to shop"""
    target_page: str


@dataclass
class PageNode(ASTNode):
    """Page definition: page home [uses layout_name]"""
    name: str
    layout: Optional[str]
    children: List[ASTNode]
    params: List[str] = None  # For page product(id)


@dataclass
class AppNode(ASTNode):
    """App container: app 'My Store'"""
    name: str
    pages: List[ASTNode]  # Can be PageNode or LayoutNode


@dataclass
class LayoutNode(ASTNode):
    """Layout definition: layout shop_layout"""
    name: str
    children: List[ASTNode]


@dataclass
class SlotNode(ASTNode):
    """Slot placeholder for layout content: slot"""
    pass


@dataclass
class UINode(ASTNode):
    """UI-related command (legacy support for Phase 1)"""
    command_type: str
    data: dict


@dataclass
class AddNode(ASTNode):
    """List mutation: add item to cart"""
    item: str
    target: str


@dataclass
class RemoveNode(ASTNode):
    """List mutation: remove item from cart"""
    item: str
    target: str


@dataclass
class FetchNode(ASTNode):
    """Data fetching: fetch from 'url'"""
    source: str


@dataclass
class NotifyNode(ASTNode):
    """UI notification: notify 'Success'"""
    message: Any


@dataclass
class Program:
    """Root node representing the entire program"""
    statements: List[ASTNode]
