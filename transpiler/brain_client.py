"""
Aura Brain Client - Communicates with the daemon for instant corrections
"""

import json
import subprocess
import time
from typing import Optional, Dict


class AuraBrainClient:
    """Client for communicating with the Aura Brain Daemon"""

    def __init__(self):
        self.process: Optional[subprocess.Popen] = None
        self.request_id = 0

    def start_daemon(self) -> bool:
        """Start the background daemon process"""
        try:
            import sys
            from pathlib import Path

            daemon_path = Path(__file__).parent / "brain_daemon.py"

            self.process = subprocess.Popen(
                [sys.executable, "-m", "transpiler.brain_daemon"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )

            # Wait for daemon to be ready (ping test)
            time.sleep(2)  # Give it time to load model

            if self.ping():
                return True
            else:
                self.stop_daemon()
                return False

        except Exception as e:
            print(f"[ERROR] Failed to start daemon: {e}")
            return False

    def ping(self) -> bool:
        """Check if daemon is alive"""
        try:
            response = self._send_request("ping", {})
            return response.get("result", {}).get("status") == "alive"
        except:
            return False

    def correct(self, line: str) -> Dict:
        """
        Request correction for a line of code.
        Returns: {"original": str, "corrected": str, "changed": bool, "time_ms": float}
        """
        try:
            response = self._send_request("correct", {"line": line})
            return response.get("result", {
                "original": line,
                "corrected": line,
                "changed": False,
                "error": "No response from daemon"
            })
        except Exception as e:
            return {
                "original": line,
                "corrected": line,
                "changed": False,
                "error": str(e)
            }

    def _send_request(self, method: str, params: dict) -> dict:
        """Send JSON-RPC request to daemon"""
        if not self.process:
            raise RuntimeError("Daemon not started")

        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params
        }

        # Send request
        self.process.stdin.write(json.dumps(request) + "\n")
        self.process.stdin.flush()

        # Read response
        response_line = self.process.stdout.readline()
        return json.loads(response_line)

    def stop_daemon(self):
        """Gracefully stop the daemon"""
        if self.process:
            try:
                self._send_request("shutdown", {})
                self.process.wait(timeout=2)
            except:
                self.process.terminate()
            finally:
                self.process = None


# Global singleton instance
_client_instance: Optional[AuraBrainClient] = None


def get_brain_client() -> AuraBrainClient:
    """Get or create the global brain client instance"""
    global _client_instance
    if _client_instance is None:
        _client_instance = AuraBrainClient()
    return _client_instance
