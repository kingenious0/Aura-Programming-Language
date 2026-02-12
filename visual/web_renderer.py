"""
Web Renderer - Converts render tree to HTML/DOM
Simple string templates for MVP (can optimize to vDOM later)
"""

from visual.render_tree import RenderTree, RenderNode
from typing import Optional


class WebRenderer:
    """
    Renders VRE output to HTML
    Uses string templates (simple, fast to ship)
    """

    def __init__(self, runtime):
        self.runtime = runtime

    def render(self, render_tree: RenderTree) -> str:
        """Convert render tree to HTML"""
        if not render_tree or not render_tree.root:
            return '<div class="aura-empty">No UI defined</div>'

        return self._render_node(render_tree.root)

    def _render_node(self, node: RenderNode) -> str:
        """Render single node to HTML"""

        if node.type == 'screen':
            children_html = ''.join(self._render_node(child)
                                    for child in node.children)
            return f'<div class="aura-screen">{children_html}</div>'

        elif node.type == 'column':
            children_html = ''.join(self._render_node(child)
                                    for child in node.children)
            return f'<div class="aura-column">{children_html}</div>'

        elif node.type == 'row':
            children_html = ''.join(self._render_node(child)
                                    for child in node.children)
            return f'<div class="aura-row">{children_html}</div>'

        elif node.type == 'stack':
            children_html = ''.join(self._render_node(child)
                                    for child in node.children)
            return f'<div class="aura-stack">{children_html}</div>'

        elif node.type == 'text':
            value = node.resolve_value(self.runtime)
            # Escape HTML
            value = str(value).replace('<', '&lt;').replace('>', '&gt;')
            return f'<span class="aura-text">{value}</span>'

        elif node.type == 'button':
            label = node.props.get('label', 'Button')
            return f'''<button class="aura-button" data-node-id="{node.node_id}">{label}</button>'''

        elif node.type == 'input':
            placeholder = node.props.get('placeholder', '')
            current_value = node.resolve_value(
                self.runtime) if node.binding else ''
            return f'''<input 
                class="aura-input" 
                data-node-id="{node.node_id}"
                data-binding="{node.binding or ''}"
                placeholder="{placeholder}"
                value="{current_value}"
            />'''

        else:
            return f'<div class="aura-unknown">Unknown: {node.type}</div>'

    def get_styles(self) -> str:
        """Return basic CSS styles"""
        return """
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                padding: 20px;
                background: #f5f5f5;
            }
            
            .aura-screen {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            .aura-column {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            
            .aura-row {
                display: flex;
                flex-direction: row;
                gap: 15px;
                align-items: center;
            }
            
            .aura-stack {
                position: relative;
            }
            
            .aura-stack > * {
                position: absolute;
                top: 0;
                left: 0;
            }
            
            .aura-text {
                font-size: 16px;
                color: #333;
            }
            
            .aura-button {
                padding: 10px 20px;
                font-size: 16px;
                background: #007acc;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                transition: background 0.2s;
            }
            
            .aura-button:hover {
                background: #005a9e;
            }
            
            .aura-button:active {
                transform: translateY(1px);
            }
            
            .aura-input {
                padding: 10px;
                font-size: 16px;
                border: 2px solid #ddd;
                border-radius: 4px;
                outline: none;
                transition: border-color 0.2s;
            }
            
            .aura-input:focus {
                border-color: #007acc;
            }
            
            .aura-empty {
                color: #999;
                font-style: italic;
                text-align: center;
                padding: 40px;
            }
        </style>
        """
