"""
Visual Dev Server - Live development server for Aura visual apps
HTTP server + WebSocket for live updates
"""

import asyncio
import json
import threading
import webbrowser
from pathlib import Path
from typing import Optional, Set
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socket

try:
    import websockets
    from websockets.server import WebSocketServerProtocol
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False
    print("⚠️  websockets not installed. Run: pip install websockets")

from runtime import AuraRuntime
from visual.engine import VisualRuntimeEngine
from visual.web_renderer import WebRenderer
from visual.events import EventBridge


class VisualDevServer:
    """
    Development server for visual Aura apps
    Serves HTML + handles WebSocket events
    """

    def __init__(self, aura_file: str, port: int = 3000):
        if not WEBSOCKETS_AVAILABLE:
            raise ImportError(
                "websockets library required. Install with: pip install websockets")

        self.aura_file = Path(aura_file)
        self.port = port
        self.ws_port = port + 1  # WebSocket on next port

        # Initialize runtime
        self.runtime = AuraRuntime()
        self.vre = VisualRuntimeEngine(self.runtime)
        self.renderer = WebRenderer(self.runtime)
        self.event_bridge = EventBridge(self.runtime, self.vre)

        # WebSocket clients
        self.clients: Set[WebSocketServerProtocol] = set()
        self.ws_loop = None

        # Register render callback
        self.vre.on_render(self.on_vre_render)

    def start(self):
        """Start HTTP + WebSocket servers"""
        print(f"🎨 Aura Visual Runtime")
        print(f"   File: {self.aura_file}")

        # Load and parse program
        self.load_program()

        # Start WebSocket in background
        ws_thread = threading.Thread(target=self._run_websocket, daemon=True)
        ws_thread.start()

        # Wait a moment for WebSocket to start
        import time
        time.sleep(0.5)

        # Open browser
        url = f"http://localhost:{self.port}"
        print(f"\n✅ Visual app running on {url}")
        print(f"   Press Ctrl+C to stop\n")

        # Serve HTML page
        self._serve_html()

    def load_program(self):
        """Load and parse Aura file"""
        from transpiler.logic_parser import LogicParser

        parser = LogicParser()
        program = parser.parse_file(str(self.aura_file))

        # Execute logic statements
        from transpiler.core import AuraCore
        core = AuraCore()
        core.state = self.runtime.state

        # Separate logic and UI
        logic_statements = []
        ui_node = None

        for stmt in program.statements:
            # Check if it's a UI node
            from transpiler.ui_nodes import UINode
            if isinstance(stmt, UINode):
                ui_node = stmt
            else:
                logic_statements.append(stmt)

        # Execute logic
        for stmt in logic_statements:
            core.execute_statement(stmt)

        # Load UI
        if ui_node:
            self.vre.load_ui(ui_node)
        else:
            print("⚠️  No UI defined in file")

    def _serve_html(self):
        """Serve HTML page on HTTP"""
        html = self._generate_html()

        # Simple HTTP server
        class AuraHandler(SimpleHTTPRequestHandler):
            html_content = html

            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(self.html_content.encode())

            def log_message(self, format, *args):
                pass  # Suppress logs

        try:
            with HTTPServer(('', self.port), AuraHandler) as server:
                # Open browser
                webbrowser.open(f"http://localhost:{self.port}")
                server.serve_forever()
        except KeyboardInterrupt:
            print("\n⚠️  Stopping server...")

    def _run_websocket(self):
        """Run WebSocket server in thread"""
        self.ws_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.ws_loop)

        start_server = websockets.serve(
            self._handle_ws_client,
            'localhost',
            self.ws_port
        )

        self.ws_loop.run_until_complete(start_server)
        self.ws_loop.run_forever()

    async def _handle_ws_client(self, websocket: WebSocketServerProtocol, path: str):
        """Handle WebSocket client connection"""
        self.clients.add(websocket)
        print(f"🔌 Client connected")

        try:
            # Send initial render
            await self._send_render(websocket)

            # Listen for events
            async for message in websocket:
                await self._handle_ws_message(websocket, message)

        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.remove(websocket)
            print(f"🔌 Client disconnected")

    async def _handle_ws_message(self, websocket: WebSocketServerProtocol, message: str):
        """Handle incoming WebSocket message"""
        try:
            data = json.loads(message)
            event_type = data.get('type')

            if event_type == 'click':
                node_id = data.get('nodeId')
                self.event_bridge.handle_click(node_id)

            elif event_type == 'input':
                node_id = data.get('nodeId')
                value = data.get('value')
                self.event_bridge.handle_input(node_id, value)

            elif event_type == 'hover':
                node_id = data.get('nodeId')
                self.event_bridge.handle_hover(node_id)

        except json.JSONDecodeError:
            print(f"⚠️  Invalid JSON: {message}")

    async def _send_render(self, websocket: WebSocketServerProtocol):
        """Send current render to client"""
        html = self.renderer.render(self.vre.render_tree)

        message = json.dumps({
            'type': 'render',
            'html': html
        })

        await websocket.send(message)

    async def _broadcast_render(self):
        """Broadcast render to all clients"""
        if not self.clients:
            return

        html = self.renderer.render(self.vre.render_tree)

        message = json.dumps({
            'type': 'render',
            'html': html
        })

        await asyncio.gather(
            *[client.send(message) for client in self.clients],
            return_exceptions=True
        )

    def on_vre_render(self, render_tree):
        """Called when VRE triggers render"""
        # Broadcast to all connected clients
        if self.ws_loop and self.clients:
            asyncio.run_coroutine_threadsafe(
                self._broadcast_render(),
                self.ws_loop
            )

    def _generate_html(self) -> str:
        """Generate HTML template"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aura App</title>
    {self.renderer.get_styles()}
</head>
<body>
    <div id="root">
        <div class="aura-empty">Connecting...</div>
    </div>
    
    <script>
        const ws = new WebSocket('ws://localhost:{self.ws_port}');
        
        ws.onopen = () => {{
            console.log('Connected to Aura runtime');
        }};
        
        ws.onmessage = (event) => {{
            const data = JSON.parse(event.data);
            
            if (data.type === 'render') {{
                document.getElementById('root').innerHTML = data.html;
                attachEventListeners();
            }}
        }};
        
        ws.onclose = () => {{
            console.log('Disconnected from Aura runtime');
            document.getElementById('root').innerHTML = 
                '<div class="aura-empty">Disconnected from server</div>';
        }};
        
        function attachEventListeners() {{
            // Button clicks
            document.querySelectorAll('.aura-button').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    ws.send(JSON.stringify({{
                        type: 'click',
                        nodeId: btn.dataset.nodeId
                    }}));
                }});
            }});
            
            // Input changes
            document.querySelectorAll('.aura-input').forEach(input => {{
                input.addEventListener('input', (e) => {{
                    ws.send(JSON.stringify({{
                        type: 'input',
                        nodeId: input.dataset.nodeId,
                        value: e.target.value
                    }}));
                }});
            }});
        }}
    </script>
</body>
</html>"""
