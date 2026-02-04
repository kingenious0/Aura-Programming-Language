
import os
import sys
import time
import requests
from pathlib import Path

# Configuration
BRAIN_DIR = os.path.join(os.getcwd(), ".aura_brain")
# Qwen 2.5 0.5B Instruct - Q4_K_M (High performance, low RAM)
MODEL_URL = "https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/qwen2.5-0.5b-instruct-q4_k_m.gguf"
MODEL_FILENAME = "aura_brain_qwen.gguf"
MODEL_PATH = os.path.join(BRAIN_DIR, MODEL_FILENAME)


def ensure_aura_brain():
    """Checks for the Aura Brain model and downloads it if missing."""

    if os.path.exists(MODEL_PATH):
        return True

    print(f"[Aura Brain] 🧠 Initializing Semantic Core...")
    print(f"[Aura Brain] Model specific: Qwen2.5-0.5B (Fast & Intelligent)")

    if not os.path.exists(BRAIN_DIR):
        os.makedirs(BRAIN_DIR)

    print(f"[Download] Downloading model to {BRAIN_DIR}...")
    try:
        start_time = time.time()
        response = requests.get(MODEL_URL, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192
        downloaded = 0

        with open(MODEL_PATH, 'wb') as f:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    # Simple progress indicator
                    done = int(50 * downloaded / total_size)
                    sys.stdout.write(
                        f"\r[{'=' * done}{' ' * (50-done)}] {downloaded//1024//1024}MB / {total_size//1024//1024}MB")
                    sys.stdout.flush()

        print(
            f"\n[Aura Brain] Download Complete! ({int(time.time() - start_time)}s)")
        return True

    except Exception as e:
        print(f"\n[Error] Failed to download Aura Brain: {e}")
        # Clean up partial download
        if os.path.exists(MODEL_PATH):
            os.remove(MODEL_PATH)
        return False


if __name__ == "__main__":
    ensure_aura_brain()
