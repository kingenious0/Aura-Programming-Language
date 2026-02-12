# 🚀 Aura Command Reference

## How to Run Aura Commands

**From the project directory, use:**
```powershell
.\aura <command>
```

That's it! The `.bat` wrapper handles everything.

---

## Examples

```powershell
# Show help
.\aura --help

# Show version
.\aura --version

# Run a file
.\aura run examples/my_calculator.aura

# Watch mode (auto-reload)
.\aura dev examples/simple_logic.aura

# Trace execution
.\aura trace examples/grade_calculator.aura

# Compile to Python
.\aura compile examples/my_calculator.aura
```

---

## Phase 2.6 - Test Safety Systems

```powershell
# Test all safety features
python test_safety.py
```

---

## All Commands

| Command | Purpose |
|---------|---------|
| `.\aura run <file>` | Execute Aura file |
| `.\aura dev <file>` | Watch mode with hot reload |
| `.\aura trace <file>` | Debug with execution trace |
| `.\aura compile <file>` | Generate Python file |
| `.\aura --help` | Show help |
| `.\aura --version` | Show version |

---

## Current Phase Status

✅ **Phase 2** - Core Logic (complete)  
✅ **Phase 2.5** - Living Runtime (complete)  
✅ **Phase 2.6** - Runtime Maturity (complete)  

🔜 **Phase 3** - UI + Logic Integration

---

**Simple. Clean. Ready to build.** 🚀
