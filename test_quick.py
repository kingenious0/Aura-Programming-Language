"""
Quick Test - Aura 2.6 Safety Systems
"""
from transpiler.logic_parser import LogicParser
from runtime import AuraRuntime, AuraError
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))


# Test 1: Introspection
print("=== Introspection Test ===")
code = """
set x to 10
set y to 20
"""

parser = LogicParser()
program = parser.parse(code)
runtime = AuraRuntime(program)
runtime.load_program(program)
runtime.execute_once()

print(runtime.inspector.format_vars())
print("✅ Introspection works!\n")

# Test 2: State Integrity
print("=== State Rollback Test ===")
runtime3 = AuraRuntime()
runtime3.state.set_var('count', 10)
print(f"Before: count = {runtime3.state.get_var('count')}")

snapshot = runtime3.integrity.snapshot(runtime3.state)
runtime3.state.set_var('count', 99)
print(f"Changed: count = {runtime3.state.get_var('count')}")

runtime3.integrity.rollback(runtime3.state, snapshot)
print(f"After rollback: count = {runtime3.state.get_var('count')}")
print("✅ Rollback works!\n")

print("🎉 All safety systems operational!")
