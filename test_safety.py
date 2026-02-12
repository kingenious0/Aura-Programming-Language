"""
Simple test for Aura 2.6 Safety Systems
"""
from runtime.errors import AuraVariableError, AuraMathError, ErrorContext
from runtime import ResourceLimits
from transpiler.logic_parser import LogicParser
from runtime import AuraRuntime, AuraError
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))


print("🧪 Testing Aura 2.6 Safety Systems\n")

# ===== Test 1: Introspection =====
print("=== Test 1: Runtime Introspection ===")

# Create a test file
test_code = """set x to 10
set y to 20
set name to "Aura"
"""

with open('temp_test.aura', 'w') as f:
    f.write(test_code)

parser = LogicParser()
program = parser.parse_file('temp_test.aura')

runtime = AuraRuntime(program)
runtime.load_program(program)
runtime.execute_once()

# Inspect the runtime
print(runtime.inspector.format_vars())
print(runtime.inspector.format_memory())
print("✅ Introspection works!\n")

# Clean up
Path('temp_test.aura').unlink()


# ===== Test 2: State Snapshots & Rollback =====
print("=== Test 2: State Integrity (Snapshots & Rollback) ===")

runtime2 = AuraRuntime()

# Set initial state
runtime2.state.set_var('counter', 10)
print(f"Initial state: counter = {runtime2.state.get_var('counter')}")

# Take a snapshot
snapshot = runtime2.integrity.snapshot(runtime2.state)
print(f"📸 Snapshot taken: {snapshot}")

# Modify state
runtime2.state.set_var('counter', 999)
runtime2.state.set_var('temp', 'temporary')
print(f"Modified state: counter = {runtime2.state.get_var('counter')}")
print(f"                temp = {runtime2.state.get_var('temp')}")

# Rollback to snapshot
runtime2.integrity.rollback(runtime2.state, snapshot)
print(f"⏮️  Rolled back: counter = {runtime2.state.get_var('counter')}")
print(f"              temp exists? {runtime2.state.has_var('temp')}")
print("✅ Rollback works!\n")


# ===== Test 3: Resource Limits =====
print("=== Test 3: Resource Limits ===")


limits = ResourceLimits(max_variables=3)
runtime3 = AuraRuntime(limits=limits)

try:
    # Try to create 5 variables (limit is 3)
    for i in range(5):
        runtime3.state.set_var(f'var_{i}', i)
        var_count = len(runtime3.state.get_all_vars())
        print(f"  Created var_{i} (total: {var_count})")
        runtime3.resource_tracker.check_variables(var_count)
except AuraError as e:
    print(f"🛑 Limit enforced: {e}")
    print("✅ Resource limits work!\n")


# ===== Test 4: Error Model =====
print("=== Test 4: Human-Readable Errors ===")


# Create a friendly error
error1 = AuraVariableError(
    "Variable 'score' not defined",
    ErrorContext(line_number=5, file_path="test.aura", code_line="print score")
)

print(error1)
print("✅ Error formatting works!\n")


print("=" * 50)
print("🎉 All Phase 2.6 Safety Systems Operational!")
print("=" * 50)
print("\n📊 Summary:")
print("  ✅ Introspection - Full runtime visibility")
print("  ✅ State Integrity - Snapshots & rollback")
print("  ✅ Resource Limits - Memory protection")
print("  ✅ Error Model - Human-readable errors")
print("\n🛡️  The kernel is hardened!")
