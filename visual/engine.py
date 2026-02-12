"""
Visual Runtime Engine (VRE) - Core of Aura's visual layer
Subscribes to runtime state, builds render tree, triggers updates
"""

from typing import Optional, List, Callable
from visual.render_tree import RenderTree, RenderNode
from transpiler.ui_nodes import (
    ScreenNode, ColumnNode, RowNode, StackNode,
    TextNode, ButtonNode, InputNode, UINode
)


class VisualRuntimeEngine:
    """
    Visual Runtime Engine

    Responsibilities:
    - Convert UI AST to render tree
    - Subscribe to runtime state changes
    - Trigger re-renders on state updates
    - Maintain render tree (NOT state)
    """

    def __init__(self, runtime):
        self.runtime = runtime
        self.render_tree: Optional[RenderTree] = None
        self.ui_ast: Optional[UINode] = None
        self.on_render_callbacks: List[Callable] = []

    def load_ui(self, ui_ast: UINode):
        """Load UI AST and build initial render tree"""
        self.ui_ast = ui_ast
        self.render_tree = self.build_render_tree()
        self.subscribe_to_state()
        self.trigger_render()

    def build_render_tree(self) -> RenderTree:
        """Convert UI AST to render tree"""
        if not self.ui_ast:
            return RenderTree()

        root = self._convert_node(self.ui_ast)
        return RenderTree(root)

    def _convert_node(self, ast_node: UINode) -> RenderNode:
        """Convert single AST node to render node"""

        if isinstance(ast_node, ScreenNode):
            return RenderNode(
                type='screen',
                children=[self._convert_node(child)
                          for child in ast_node.children]
            )

        elif isinstance(ast_node, ColumnNode):
            return RenderNode(
                type='column',
                children=[self._convert_node(child)
                          for child in ast_node.children]
            )

        elif isinstance(ast_node, RowNode):
            return RenderNode(
                type='row',
                children=[self._convert_node(child)
                          for child in ast_node.children]
            )

        elif isinstance(ast_node, StackNode):
            return RenderNode(
                type='stack',
                children=[self._convert_node(child)
                          for child in ast_node.children]
            )

        elif isinstance(ast_node, TextNode):
            # Check if it's a variable binding or literal text
            if ast_node.is_binding:
                return RenderNode(
                    type='text',
                    binding=ast_node.value,
                    props={'value': ast_node.value}
                )
            else:
                # Literal text
                return RenderNode(
                    type='text',
                    props={'value': ast_node.value}
                )

        elif isinstance(ast_node, ButtonNode):
            return RenderNode(
                type='button',
                props={'label': ast_node.label},
                on_click=ast_node.on_click
            )

        elif isinstance(ast_node, InputNode):
            return RenderNode(
                type='input',
                binding=ast_node.binding,
                props={'placeholder': ast_node.placeholder or ''}
            )

        else:
            # Unknown node type
            return RenderNode(type='unknown')

    def subscribe_to_state(self):
        """Subscribe to runtime state changes"""
        # Get all variable bindings in tree
        if not self.render_tree:
            return

        bindings = self.render_tree.get_all_bindings()

        # Subscribe to each
        for var_name in bindings:
            self.runtime.ui_binder.subscribe(var_name, self.on_state_change)

    def on_state_change(self, value):
        """Called when subscribed state changes"""
        # Trigger re-render
        self.trigger_render()

    def trigger_render(self):
        """Notify all render callbacks"""
        for callback in self.on_render_callbacks:
            try:
                callback(self.render_tree)
            except Exception as e:
                print(f"⚠️  Render callback error: {e}")

    def on_render(self, callback: Callable):
        """Register callback for render events"""
        self.on_render_callbacks.append(callback)

    def reload_ui(self, new_ui_ast: UINode):
        """Hot reload - rebuild tree without losing runtime state"""
        self.ui_ast = new_ui_ast
        self.render_tree = self.build_render_tree()
        self.subscribe_to_state()
        self.trigger_render()

    def __repr__(self):
        return f"<VisualRuntimeEngine tree={self.render_tree}>"
