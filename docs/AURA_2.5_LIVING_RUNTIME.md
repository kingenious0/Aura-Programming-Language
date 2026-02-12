# 🧠 Aura 2.5 - Living Runtime Guide

**Phase 2.5:** Transform Aura from one-shot execution to a persistent, event-driven platform.

---

## ✨ What's New in 2.5

### Watch Mode (`aura dev <file>`)
Auto-reload on file changes - like nodemon for Aura!

```bash
aura dev examples/watch_test.aura
```

Edit the file, save, and see changes instantly without restarting.

### Runtime Engine
- **Persistent State** - Variables survive across reloads
- **Hot Reload** - Code changes without losing state
- **Event System** - Internal event queue and handlers
- **Live Introspection** - Debug runtime while it's running

---

## 🚀 Getting Started

### Simple Watch Mode Example

Create `counter.aura`:
```aura
set count to 0
print "Count:"
print count
```

Run with watch mode:
```bash
aura dev counter.aura
```

Now edit the file while it's running:
```aura
set count to 10  # Change this
print "Count:"
print count      # See it update!
```

Save - it reloads instantly!

---

## 🏗️ Architecture

### Runtime Components

**State Manager** (`runtime/state.py`)
- Variable storage with scoping
- Function registry
- Call stack tracking
- State snapshots for debugging

**Event Queue** (`runtime/events.py`)
- FIFO event processing
- Event handler registration
- Timer/scheduler support

**Runtime Engine** (`runtime/engine.py`)
- Main execution loop
- Hot reload logic
- Lifecycle management
- State persistence

---

## 📖 Examples

### Example 1: Watch Mode Basics
```bash
# Create a file
echo "set score to 10
print score" > test.aura

# Start watch mode
aura dev test.aura

# Edit in another window - changes apply instantly!
```

### Example 2: State Preservation
Create `stateful.aura`:
```aura
set counter to 0
set name to "Aura"

print name
print counter
```

Run: `aura dev stateful.aura`

Edit to:
```aura
set counter to 5  # State changes
set name to "Living Runtime"

print name
print counter
```

**Notice:** When you save, the runtime reloads but the logic updates!

---

## 🔮 What's Coming

Phase 2.5 is the **foundation** for:

### Events (Coming Soon)
```aura
when timer ticks
    print "tick"
```

### Debug Mode (Coming Soon)
```bash
aura debug app.aura
> step
> vars
> break 10
```

### Runtime Inspection
```bash
aura inspect app.aura
# Shows: variables, functions, event queue
```

---

## 💡 Use Cases

**Development Workflow**
- Edit code → Save → See  results instantly
- No restart needed
- State persists between reloads

**Learning** 
- Experiment with code live
- See changes immediately
- No compilation delay

**Debugging**
- Hot reload to test fixes
- State inspection
- Live variable tracking

---

## 🎯 Commands Summary

| Command | Purpose |
|---------|---------|
| `aura run <file>` | One-shot execution (Phase 2) |
| `aura dev <file>` | Watch mode with hot reload (Phase 2.5) |
| `aura trace <file>` | Full execution trace |
| `aura compile <file>` | Generate Python file |

---

## 🔧 Technical Details

### How Hot Reload Works

When a file changes:
1. File watcher detects modification
2. Parser re-parses the file into AST
3. Runtime preserves existing variables
4. New code is loaded
5. Execution continues with updated logic

**State Preservation:**
- Variables: ✅ Preserved
- Functions: 🔄 Updated
- Code logic: 🔄 Updated

---

Built with ❤️ by **Kingenious**

*"Logic first. UI later. Platform always."*
