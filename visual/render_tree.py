"""
Render Tree - Semantic tree for visual rendering
State-bound nodes that resolve to actual values
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import uuid


@dataclass
class RenderNode:
    """
    Semantic render node
    Represents a UI element bound to runtime state
    """
    type: str  # 'screen', 'column', 'row', 'stack', 'text', 'button', 'input'
    children: List['RenderNode'] = field(default_factory=list)
    props: Dict[str, Any] = field(default_factory=dict)
    binding: Optional[str] = None  # Variable name if bound
    on_click: Optional[List] = None  # Click handler statements
    on_change: Optional[List] = None  # Change handler statements
    on_hover: Optional[List] = None  # Hover handler statements
    node_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def resolve_value(self, runtime):
        """Get actual value from runtime state"""
        if self.binding:
            try:
                return runtime.state.get_var(self.binding)
            except:
                return f"[{self.binding}]"  # Show variable name if not found
        return self.props.get('value', '')

    def __repr__(self):
        if self.binding:
            return f"<{self.type} binding={self.binding}>"
        return f"<{self.type}>"


class RenderTree:
    """
    Complete render tree for a visual app
    """

    def __init__(self, root: Optional[RenderNode] = None):
        self.root = root

    def traverse(self, callback):
        """Traverse tree depth-first"""
        if self.root:
            self._traverse_node(self.root, callback)

    def _traverse_node(self, node, callback):
        """Recursively traverse"""
        callback(node)
        for child in node.children:
            self._traverse_node(child, callback)

    def find_by_id(self, node_id: str) -> Optional[RenderNode]:
        """Find node by ID"""
        result = None

        def finder(node):
            nonlocal result
            if node.node_id == node_id:
                result = node

        self.traverse(finder)
        return result

    def get_all_bindings(self) -> List[str]:
        """Get all variable bindings in tree"""
        bindings = []

        def collector(node):
            if hasattr(node, 'binding') and node.binding:
                bindings.append(node.binding)

        self.traverse(collector)
        return bindings

    def __repr__(self):
        return f"<RenderTree root={self.root}>"
