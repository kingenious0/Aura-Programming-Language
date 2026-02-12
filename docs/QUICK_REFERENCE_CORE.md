# Aura Quick Reference

## 🧠 Core Logic Commands

| Command | Example | Purpose |
|---------|---------|---------|
| `set ... to ...` | `set score to 10` | Variable assignment |
| `print ...` | `print "Hello"` | Output to console |
| `if ... else` | `if score > 5` | Conditional logic |
| `repeat N times` | `repeat 3 times` | Loop N iterations |
| `define function` | `define function greet` | Create function |
| `call function` | `call function greet` | Execute function |

## 🌐 UI Commands (Partial List)

| Command | Example |
|---------|---------|
| `Create a heading` | `Create a heading with the text 'Welcome'` |
| `Create a button` | `Create a button with the text 'Click'` |
| `Create a paragraph` | `Create a paragraph with the text 'Info'` |
| `When clicked` | `When clicked, display 'Success'` |
| `Use the ... theme` | `Use the dark theme` |

## 🚀 CLI Commands

```bash
# Core Logic
aura run logic.aura          # Execute
aura trace logic.aura        # Debug mode
aura compile logic.aura      # Generate .py file

# UI Development
aura init my-app             # New project
aura dev                     # Hot reload server
aura build Home.aura         # Production build

# Info
aura --help                  # Show help
aura --version               # Show version
```

## 📐 Syntax Rules

### Indentation
Use **4 spaces** or **1 tab** for blocks:
```aura
if score > 5
    print "Win"
else
    print "Lose"
```

### Math Operators
- Addition: `+`
- Subtraction: `-`
- Multiplication: `*`
- Division: `/`

### Comparison Operators
- Greater: `>` or `greater than`
- Less: `<` or `less than`
- Equal: `==` or `is` or `equals`
- Not equal: `!=` or `not`

### Strings
Use quotes for literals:
```aura
set name to "Alice"     # String
print "Hello"           # String

set score to 10         # Number
print score             # Variable
```

## 🎯 Common Patterns

### Counter
```aura
set count to 0
repeat 5 times
    set count to count + 1
print count
```

### Grade Calculator
```aura
set score to 85

if score > 90
    print "A"
else
    if score > 80
        print "B"
    else
        print "C"
```

### Function with Logic
```aura
define function calculate
    set x to 10
    set y to x * 2
    print y

call function calculate
```

---

**📚 Full docs**: [docs/AURA_CORE.md](AURA_CORE.md)
