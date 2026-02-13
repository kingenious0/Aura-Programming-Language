
import sys
# Ensure UTF-8 output for Windows consoles
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

import unittest
from unittest.mock import MagicMock
from runtime.engine import AuraRuntime
from visual.engine import VisualRuntimeEngine
from visual.events import EventBridge
from transpiler.ast_nodes import VariableNode, ASTNode


class TestVisualLogic(unittest.TestCase):
    def test_click_updates_state(self):
        # Setup Runtime
        runtime = AuraRuntime()
        # Create a dummy variable in state
        runtime.state.set_var('score', 0)

        # Setup VRE (mocked where necessary)
        vre = VisualRuntimeEngine(runtime)
        # Mock render tree to return a node with on_click handler
        vre.render_tree = MagicMock()

        # Create a fake node that sends "set score to 1"
        # We need a real AST node for the handler
        # "set score to 1" -> VariableNode(name='score', value='1')
        # But wait, value '1' is a string in AST?
        # Parser produces: VariableNode(name='score', value='1')
        # Core executes it.

        handler_stmt = VariableNode(
            line_number=1, raw_line="set score to 1", name="score", value="1")

        # Mock finding the node
        mock_node = MagicMock()
        mock_node.on_click = [handler_stmt]
        mock_node.props = {'label': 'Test Button'}
        vre.render_tree.find_by_id.return_value = mock_node

        # Setup EventBridge
        bridge = EventBridge(runtime, vre)

        # Simulate Click
        print("Simulating click...")
        bridge.handle_click("node-123")

        # Verify State
        new_score = runtime.state.get_var('score')
        print(f"Score after click: {new_score}")
        self.assertEqual(int(new_score), 1)


if __name__ == '__main__':
    unittest.main()
