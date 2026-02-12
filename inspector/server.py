"""
Inspector Server - WebSocket server for live state broadcasting
Streams runtime state to web inspector dashboard
"""

import json
import asyncio
import threading
from typing import Optional, Set
try:
    import websockets
    from websockets.server import WebSocketServerProtocol
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False
    print("⚠️  websockets not installed. Run: pip install websockets")


class InspectorServer:
    """WebSocket server for live runtime inspection"""

    def __init__(self, runtime, host='localhost', port=8080):
        if not WEBSOCKETS_AVAILABLE:
            raise ImportError(
                "websockets library required. Install with: pip install websockets")

        self.runtime = runtime
        self.host = host
        self.port = port
        self.clients: Set[WebSocketServerProtocol] = set()
        self.server = None
        self.loop = None
        self.thread = None
        self.running = False

    def start(self):
        """Start server in background thread"""
        if self.running:
            print("⚠️  Server already running")
            return

        self.running = True
        self.thread = threading.Thread(target=self._run_server, daemon=True)
        self.thread.start()

        print(f"🔍 Inspector server starting on http://{self.host}:{self.port}")

    def stop(self):
        """Stop server"""
        self.running = False
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)

    def _run_server(self):
        """Run asyncio server in thread"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        start_server = websockets.serve(
            self._handle_client,
            self.host,
            self.port
        )

        self.loop.run_until_complete(start_server)
        print(f"✅ Inspector server running on ws://{self.host}:{self.port}")
        self.loop.run_forever()

    async def _handle_client(self, websocket: WebSocketServerProtocol, path: str):
        """Handle WebSocket client connection"""
        self.clients.add(websocket)
        print(f"🔌 Client connected: {websocket.remote_address}")

        try:
            # Send initial state
            await self._send_state(websocket)

            # Listen for commands
            async for message in websocket:
                await self._handle_command(websocket, message)

        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.remove(websocket)
            print(f"🔌 Client disconnected: {websocket.remote_address}")

    async def _send_state(self, websocket: WebSocketServerProtocol):
        """Send current runtime state to client"""
        state_dump = self.runtime.inspector.dump_full()

        message = {
            'type': 'state_update',
            'data': state_dump
        }

        await websocket.send(json.dumps(message))

    async def _handle_command(self, websocket: WebSocketServerProtocol, message: str):
        """Handle command from client"""
        try:
            data = json.loads(message)
            cmd_type = data.get('type')

            if cmd_type == 'get_state':
                await self._send_state(websocket)

            elif cmd_type == 'execute_command':
                # Execute console command
                from runtime.console import AuraConsole
                console = AuraConsole(self.runtime)
                console.execute(data.get('command', ''))

                # Send updated state
                await self._send_state(websocket)

            else:
                await websocket.send(json.dumps({
                    'type': 'error',
                    'message': f'Unknown command type: {cmd_type}'
                }))

        except json.JSONDecodeError:
            await websocket.send(json.dumps({
                'type': 'error',
                'message': 'Invalid JSON'
            }))

    async def broadcast_state(self):
        """Broadcast state to all connected clients"""
        if not self.clients:
            return

        state_dump = self.runtime.inspector.dump_full()
        message = json.dumps({
            'type': 'state_update',
            'data': state_dump
        })

        # Send to all clients
        await asyncio.gather(
            *[client.send(message) for client in self.clients],
            return_exceptions=True
        )

    def notify_state_change(self):
        """Notify clients of state change (called from runtime)"""
        if self.loop and self.clients:
            asyncio.run_coroutine_threadsafe(
                self.broadcast_state(),
                self.loop
            )
