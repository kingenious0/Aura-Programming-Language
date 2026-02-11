
from transpiler.brain import AuraBrain
import sys
import os

# Ensure transpiler is in path
sys.path.append(os.getcwd())


def test():
    brain = AuraBrain()
    print("Initializing brain...")
    if brain.initialize():
        print("Brain initialized.")
        broken = "create a card with the title is 'testing ai features' and description 'this is a card created using ai features'"
        print(f"Testing fix for: '{broken}'")
        fixed = brain.fix_syntax(broken)
        print(f"Result: '{fixed}'")
    else:
        print("Failed to initialize brain.")


if __name__ == "__main__":
    test()
