# 🧪 Testing Aura 2.6 Safety Systems

## Quick Test

Run this to verify all safety systems work:

```bash
python test_safety.py
```

You should see:
```
🎉 All Phase 2.6 Safety Systems Operational!

📊 Summary:
  ✅ Introspection - Full runtime visibility
  ✅ State Integrity - Snapshots & rollback
  ✅ Resource Limits - Memory protection
  ✅ Error Model - Human-readable errors

🛡️ The kernel is hardened!
```

---

## What Gets Tested

### 1. **Runtime Introspection**
- Variable inspection
- Memory tracking
- State visibility

### 2. **State Integrity**
- Snapshot creation
- State modification
- Rollback to checkpoint

### 3. **Resource Limits**
- Variable count limits
- Automatic enforcement
- Clean error messages

### 4. **Error Model**
- Human-readable error formatting
- Line numbers and context
- No Python stack traces

---

## Manual Testing

### Test Error Handling
```bash
# Create a file with an error
echo "set x to 10
print unknown_var" > error_test.aura

# Run it - you'll see a human-readable error
python -m transpiler.cli run error_test.aura
```

### Test Introspection
```python
from runtime import AuraRuntime
from transpiler.logic_parser import LogicParser

parser = LogicParser()
program = parser.parse_file('examples/my_calculator.aura')

runtime = AuraRuntime(program)
runtime.load_program(program)
runtime.execute_once()

# Inspect!
print(runtime.inspector.format_vars())
print(runtime.inspector.format_memory())
```

### Test State Rollback
```python
from runtime import AuraRuntime

runtime = AuraRuntime()

# Set state
runtime.state.set_var('score', 10)

# Snapshot
checkpoint = runtime.integrity.snapshot(runtime.state)

# Change it
runtime.state.set_var('score', 999)

# Rollback
runtime.integrity.rollback(runtime.state, checkpoint)

# Back to 10!
print(runtime.state.get_var('score'))  # → 10
```

---

## All Tests Passing ✅

If `test_safety.py` runs without errors, Phase 2.6 is complete and working!
