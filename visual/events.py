"""
Event Bridge - Converts UI interactions to Aura runtime events
UI → Runtime → State → Re-render
"""

from typing import Optional, List
from transpiler.ast_nodes import ASTNode


class EventBridge:
    """
    Bridge between UI events and Aura runtime

    Responsibilities:
    - Handle click events
    - Handle input changes
    - Execute Aura code from event handlers
    - Trigger state updates
    """

    def __init__(self, runtime, vre):
        self.runtime = runtime
        self.vre = vre  # Visual Runtime Engine

    def handle_click(self, node_id: str):
        """Handle button click event"""
        # Find node in render tree
        node = self.vre.render_tree.find_by_id(node_id)

        if not node:
            print(f"⚠️  Node not found: {node_id}")
            return

        if not node.on_click:
            print(f"⚠️  No click handler for node: {node_id}")
            return

        # Execute statements from 'when clicked' block
        print(f"🖱️  Click: {node.props.get('label', 'button')}")

        for statement in node.on_click:
            try:
                self._execute_statement(statement)
            except Exception as e:
                print(f"❌ Click handler error: {e}")

    def handle_input(self, node_id: str, value: str):
        """Handle input change event"""
        # Find node in render tree
        node = self.vre.render_tree.find_by_id(node_id)

        if not node:
            print(f"⚠️  Node not found: {node_id}")
            return

        if not node.binding:
            print(f"⚠️  Input has no binding: {node_id}")
            return

        # Update runtime state
        print(f"⌨️  Input: {node.binding} = {value}")
        self.runtime.state.set_var(node.binding, value)

        # Notify VRE of state change
        self.runtime.ui_binder.notify(node.binding, value)

        # Execute 'when changed' handler if exists
        if node.on_change:
            for statement in node.on_change:
                try:
                    self._execute_statement(statement)
                except Exception as e:
                    print(f"❌ Change handler error: {e}")

    def handle_hover(self, node_id: str):
        """Handle hover event"""
        node = self.vre.render_tree.find_by_id(node_id)

        if not node or not node.on_hover:
            return

        # Execute 'when hovered' handler
        for statement in node.on_hover:
            try:
                self._execute_statement(statement)
            except Exception as e:
                print(f"❌ Hover handler error: {e}")

    def _execute_statement(self, statement: ASTNode):
        """Execute a single Aura statement"""
        # Use the existing runtime execution system
        from transpiler.core import AuraCore

        core = AuraCore()
        core.state = self.runtime.state  # Use existing state
        core.execute_statement(statement)

    def __repr__(self):
        return "<EventBridge>"
