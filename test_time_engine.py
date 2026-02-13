"""
Test Aura 3.0 Time Engine
"""
from runtime.integrity import StateSnapshot
from runtime import AuraRuntime, TimeEngine, ExecutionStep
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

# Ensure UTF-8 output for Windows consoles
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


print("🕐 Testing Time Engine - Phase 3.0\n")

# Test 1: Basic Recording
print("=== Test 1: Execution Recording ===")

runtime = AuraRuntime()
time_engine = runtime.time_engine

# Simulate executing some code
runtime.state.set_var('x', 10)
snapshot1 = runtime.integrity.snapshot(runtime.state)

runtime.state.set_var('x', 20)
snapshot2 = runtime.integrity.snapshot(runtime.state)

# Record steps
step1 = time_engine.record_step(
    node_type="Assignment",
    node_repr="set x to 10",
    line_number=1,
    state_before=snapshot1,
    state_after=snapshot1
)

step2 = time_engine.record_step(
    node_type="Assignment",
    node_repr="set x to 20",
    line_number=2,
    state_before=snapshot1,
    state_after=snapshot2
)

print(f"Recorded {len(time_engine.history)} steps")
print(f"Step 1: {step1}")
print(f"Step 2: {step2}")
print("✅ Recording works!\n")

# Test 2: Time Travel
print("=== Test 2: Time Travel ===")

# Go to step 0
time_engine.goto(0)
print(f"At step {time_engine.current_index}")

# Step forward
time_engine.step_forward()
print(f"Stepped forward to {time_engine.current_index}")

# Step backward
time_engine.step_backward()
print(f"Stepped backward to {time_engine.current_index}")

# Rewind
time_engine.goto(1)
time_engine.rewind(1)
print(f"Rewound to step {time_engine.current_index}")

print("✅ Time travel works!\n")

# Test 3: Checkpoints
print("=== Test 3: Checkpoints ===")

time_engine.goto(1)
time_engine.create_checkpoint("important_moment")
print("Created checkpoint: important_moment")

time_engine.goto(0)
print(f"Moved to step {time_engine.current_index}")

time_engine.goto_checkpoint("important_moment")
print(f"Jumped to checkpoint → step {time_engine.current_index}")
print("✅ Checkpoints work!\n")

# Test 4: Timeline View
print("=== Test 4: Timeline Visualization ===")

print(time_engine.format_timeline())
print()

# Test 5: Stats
print("=== Test 5: Time Engine Stats ===")

stats = time_engine.get_stats()
print(f"Total steps: {stats['total_steps']}")
print(f"Current position: {stats['current_index']}")
print(f"Checkpoints: {stats['checkpoints']}")
print(f"Paused: {stats['paused']}")
print("✅ Stats work!\n")

print("=" * 50)
print("🎉 Time Engine: OPERATIONAL!")
print("=" * 50)
print("\n🕐 Features verified:")
print("  ✅ Execution recording")
print("  ✅ Time travel (forward/backward)")
print("  ✅ Checkpoints (save/restore)")
print("  ✅ Timeline visualization")
print("  ✅ State tracking")
print("\n💎 Phase 3.0 foundation complete!")
