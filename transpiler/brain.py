
import os
import sys

try:
    from llama_cpp import Llama
except ImportError:
    Llama = None

# Internal import for setup
from .setup import ensure_aura_brain, MODEL_PATH


class AuraBrain:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuraBrain, cls).__new__(cls)
        return cls._instance

    def initialize(self):
        """Lazy load the LLM only when needed"""
        if self._model:
            return True

        if Llama is None:
            print("[Aura Brain] ⚠️ Error: 'llama-cpp-python' not installed.")
            print("Run: pip install llama-cpp-python")
            return False

        # Ensure model exists
        if not ensure_aura_brain():
            return False

        print("[Aura Brain] 🧠 Waking up the Syntax Engine...")

        try:
            # Initialize Qwen-0.5B
            # n_ctx=512 is tiny but enough for single-line correction, extremely fast
            self._model = Llama(
                model_path=MODEL_PATH,
                n_ctx=512,
                n_threads=4,  # Adjust based on CPU
                verbose=False
            )
            return True
        except Exception as e:
            print(f"[Aura Brain] Failed to load model: {e}")
            return False

    def fix_syntax(self, broken_line: str) -> str:
        """
        Uses Qwen-0.5B to autocorrect a broken Aura command.
        """
        if not self._model and not self.initialize():
            return None

        system_prompt = (
            "You are the Aura Language Engine. Your only job is to receive broken Aura syntax and return the corrected version. "
            "Do not explain yourself. Do not say 'Here is the correction.' Just return the code.\n"
            "Examples:\n"
            "Input: Use dark theme\nOutput: Use the dark theme\n"
            "Input: Create button 'Click'\nOutput: Create a button with the text 'Click'\n"
            "Input: [home about]\nOutput: [Home, About]\n"
            "Input: create card with title 'Hello'\nOutput: Create a card with the title 'Hello'\n"
            "Input: create is card with title 'Hi'\nOutput: Create a card with the title 'Hi'\n"
            "Input: create card is title 'God'\nOutput: Create a card with the title 'God'\n"
        )

        prompt = f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{broken_line}<|im_end|>\n<|im_start|>assistant\n"

        try:
            output = self._model(
                prompt,
                max_tokens=128,  # Increased for longer lines
                stop=["<|im_end|>", "\n"],
                echo=False,
                temperature=0.1  # Strict logic
            )

            corrected = output['choices'][0]['text'].strip()

            # Basic validation: If it returns empty or garbage, ignore
            if len(corrected) < 3:
                return None

            return corrected

        except Exception as e:
            print(f"[Aura Brain] Error thinking: {e}")
            return None
