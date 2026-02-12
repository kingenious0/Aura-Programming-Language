# 🧠 Aura Core - The Brain

**Phase 2: English → Python Logic Engine**

---

## Overview

Aura Core transforms natural English into executable Python code. No UI, no DOM—just pure computational logic. This is the foundation that makes Aura a true "human interface to computation."

---

## ✨ Features

### Supported Commands

| Feature | Syntax | Python Output |
|---------|--------|---------------|
| **Variables** | `set score to 10` | `score = 10` |
| **Math** | `set total to price * quantity` | `total = price * quantity` |
| **Print** | `print "Hello"` or `print score` | `print("Hello")` or `print(score)` |
| **Conditionals** | `if score > 5` | `if score > 5:` |
| **Else** | `else` | `else:` |
| **Loops** | `repeat 5 times` | `for _ in range(5):` |
| **Functions** | `define function greet` | `def greet():` |
| **Call Function** | `call function greet` | `greet()` |

---

## 🚀 CLI Commands

### `aura run <file>`
Executes an Aura logic file immediately.

```bash
aura run logic.aura
```

**Auto-detects** whether your file contains logic or UI commands and routes accordingly.

### `aura trace <file>`
Executes with detailed debugging output (shows generated Python code + execution).

```bash
aura trace logic.aura
```

**Output:**
```
=== Generated Python Code ===
score = 10
if score > 5:
    print("Win!")

=== Execution ===
Win!
```

### `aura compile <file>`
Compiles Aura to a standalone Python `.py` file.

```bash
aura compile logic.aura
# Creates: logic.py
```

---

## 📖 Examples

### Example 1: Variables & Math
```aura
set price to 100
set quantity to 3
set total to price * quantity

print "Total cost:"
print total
```

**Output:**
```
Total cost:
300
```

---

### Example 2: Conditionals
```aura
set age to 18

if age > 18
    print "Adult"
else
    print "Minor"
```

**Output:**
```
Minor
```

---

### Example 3: Loops
```aura
repeat 3 times
    print "Hello, Aura!"
```

**Output:**
```
Hello, Aura!
Hello, Aura!
Hello, Aura!
```

---

### Example 4: Functions
```aura
define function welcome
    print "Welcome to Aura Core"
    print "The future of programming"

call function welcome
```

**Output:**
```
Welcome to Aura Core
The future of programming
```

---

### Example 5: Complete Program
```aura
# Game logic
set score to 0
set lives to 3

repeat 5 times
    set score to score + 10

if score > 40
    print "You win!"
else
    print "Try again"

define function show_stats
    print "Score:"
    print score
    print "Lives:"
    print lives

call function show_stats
```

**Output:**
```
You win!
Score:
50
Lives:
3
```

---

## 🎯 Design Philosophy

### Logic First, UI Later
- Phase 2 focuses on **pure logic execution**
- No browser dependencies
- No React/DOM overhead
- Python native performance

### Block Structure
Aura uses **indentation** (like Python) to define code blocks:
- **4 spaces** or **1 tab** = nested block
- Works for `if`, `else`, `repeat`, `define function`

### Type Inference
Aura automatically infers:
- **Numbers**: `10`, `3.14`
- **Strings**: `"Hello"` (with quotes) or variables (without quotes)
- **Operations**: `+`, `-`, `*`, `/`, `>`, `<`, `==`

---

## 🔮 Coming Soon (Phase 3 & 4)

### Phase 3: Aura Engine
Connect logic to UI:
```aura
set counter to 0

show button with text "Click Me"
when clicked
    set counter to counter + 1
    call function update_display

define function update_display
    show text counter
```

### Phase 4: Full Stack
One language, backend + frontend:
```aura
# Backend (Python)
set user to "Kingenious"

# Frontend (React)
show heading with text user
```

---

## 🛠️ Advanced Features

### Custom Operators
Aura supports natural language operators:
- `score is 10` → `score == 10`
- `score greater than 5` → `score > 5`
- `score less than 100` → `score < 100`

### Debugging
Use `aura trace` to see:
1. Generated Python code
2. Line-by-line execution
3. Variable states

---

## 🤝 Contributing

Want to add more logic features? Check out:
- `transpiler/logic_parser.py` - Add new patterns
- `transpiler/ast_nodes.py` - Define new node types
- `transpiler/core.py` - Implement Python generation

---

Built with ❤️ by **Kingenious**
