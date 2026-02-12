# 🎉 Aura 2.5 Living Runtime - Quick Start

## ✅ What Works Now

### Phase 2 Commands (Stable)
```bash
aura run examples/my_calculator.aura      # Execute once
aura trace examples/grade_calculator.aura # Show generated Python
aura compile examples/simple_logic.aura   # Create .py file
```

### Phase 2.5 Watch Mode (NEW!)
```bash
# Note: Use python -m for now, global 'aura' command needs refresh
python -m transpiler.cli dev examples/watch_test.aura
```

**What it does:**
- Watches the file for changes
- Auto-reloads when you save
- Preserves variable state
- Instant feedback

---

## 🚀 Try Watch Mode

### Step 1: Start watching
```bash
python -m transpiler.cli dev examples/watch_test.aura
```

You'll see:
```
👁️ Aura Watch Mode: examples/watch_test.aura
Press Ctrl+C to stop

Starting...
0
```

### Step 2: Edit the file (keep watch mode running!)

Open `examples/watch_test.aura` in another window/tab and change:
```aura
set counter to 0
```

To:
```aura
set counter to 100
```

### Step 3: Save

Watch mode detects the change and reloads automatically!

```
🔄 File changed, reloading...
Starting...
100
```

---

## 📝 Current Status

### ✅ Working
- Runtime engine
- State management
- Event system infrastructure  
- Watch mode with hot reload
- State preservation

### 🔄 Coming Soon
- Event syntax in Aura language
- Debug mode (`aura debug`)
- Runtime introspection
- Global `aura` command (needs PATH refresh after install)

---

## 🛠️ Quick Fix for 'aura' Command

If `aura` command doesn't work, use:
```bash
python -m transpiler.cli <command> <file>
```

Or reinstall:
```bash
pip uninstall aura-prog-lang
pip install -e .
# Then restart terminal
```

---

**The Living Runtime is alive!** 💓
