"""
Aura Brain Daemon - Persistent Background Service
Keeps the Qwen model loaded in memory for instant autocorrection.
"""

import sys
import json
import time
from pathlib import Path

try:
    from llama_cpp import Llama
except ImportError:
    print("[ERROR] llama-cpp-python not installed. Run: pip install llama-cpp-python")
    sys.exit(1)

try:
    from .setup import ensure_aura_brain, MODEL_PATH
except ImportError:
    from setup import ensure_aura_brain, MODEL_PATH


class AuraBrainDaemon:
    """Persistent Aura Brain service for real-time corrections"""

    def __init__(self):
        self.model = None
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """Build the comprehensive Aura syntax guide"""
        return (
            "Fix Aura syntax. Return ONLY corrected code.\n\n"
            "RULES:\n"
            "- Capitalize: Create, Use, When, Make, The\n"
            "- Add missing: a, the, with\n"
            "- Fix typos: crete→Create, butn→button, crteate→Create\n\n"
            "PATTERNS:\n"
            "Use the [dark/light] theme\n"
            "Create a [button/heading/paragraph/input] with the text '[text]'\n"
            "Create a card with the title '[title]' and description '[desc]'\n"
            "Create a navbar with links [Home, About]\n"
            "When clicked, [display/alert/show/hide] '[text]'\n"
            "Make the [element] [color/bold/italic]\n\n"
            "FIXES:\n"
            "create→Create | crete→Create | butn→button\n"
            "create is card→Create a card\n"
            "with title→with the title\n"
        )

    def start(self):
        """Initialize and keep the model warm"""
        if not ensure_aura_brain():
            print("[ERROR] Failed to ensure Aura Brain model")
            return False

        print("[Aura Brain Daemon] Starting...")
        print("[Aura Brain Daemon] Loading Qwen2.5-0.5B model...")

        try:
            # Optimized for speed: smaller context, more threads
            self.model = Llama(
                model_path=MODEL_PATH,
                n_ctx=256,  # Reduced for faster inference
                n_batch=128,  # Batch processing
                n_threads=6,  # More CPU threads
                verbose=False
            )
            print("[Aura Brain Daemon] ✓ Model loaded and ready")
            print("[Aura Brain Daemon] Listening on stdin for correction requests...")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to load model: {e}")
            return False

    def correct_line(self, line: str) -> dict:
        """
        Correct a single line of Aura code.
        Returns: {"original": str, "corrected": str, "changed": bool, "time_ms": float}
        """
        start_time = time.time()

        if not self.model:
            return {
                "original": line,
                "corrected": line,
                "changed": False,
                "error": "Model not loaded",
                "time_ms": 0
            }

        # Build prompt with cached system context
        prompt = f"<|im_start|>system\n{self.system_prompt}<|im_end|>\n<|im_start|>user\n{line}<|im_end|>\n<|im_start|>assistant\n"

        try:
            output = self.model(
                prompt,
                max_tokens=64,
                stop=["<|im_end|>", "\n"],
                echo=False,
                temperature=0.05,  # Very strict for consistency
                top_p=0.9
            )

            corrected = output['choices'][0]['text'].strip()
            elapsed_ms = (time.time() - start_time) * 1000

            # Validate correction
            if len(corrected) < 3 or corrected == line:
                return {
                    "original": line,
                    "corrected": line,
                    "changed": False,
                    "time_ms": elapsed_ms
                }

            return {
                "original": line,
                "corrected": corrected,
                "changed": True,
                "time_ms": elapsed_ms
            }

        except Exception as e:
            return {
                "original": line,
                "corrected": line,
                "changed": False,
                "error": str(e),
                "time_ms": (time.time() - start_time) * 1000
            }

    def run(self):
        """Main daemon loop - reads from stdin, writes to stdout"""
        if not self.start():
            sys.exit(1)

        # JSON-RPC style communication
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break

                request = json.loads(line.strip())

                if request.get("method") == "correct":
                    code_line = request.get("params", {}).get("line", "")
                    result = self.correct_line(code_line)
                    response = {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "result": result
                    }
                    print(json.dumps(response), flush=True)

                elif request.get("method") == "ping":
                    response = {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "result": {"status": "alive"}
                    }
                    print(json.dumps(response), flush=True)

                elif request.get("method") == "shutdown":
                    print(json.dumps({"result": "shutting down"}), flush=True)
                    break

            except KeyboardInterrupt:
                break
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {"message": str(e)}
                }
                print(json.dumps(error_response), flush=True)


if __name__ == "__main__":
    daemon = AuraBrainDaemon()
    daemon.run()
