# 🚀 Using the Global `aura` Command

## Current Setup

The `aura` command is installed but there are **two ways to use it**:

---

## Option 1: Use the Batch Wrapper (Easiest)

From the project directory:
```powershell
.\aura --version
.\aura run examples/my_calculator.aura
.\aura dev examples/watch_test.aura
```

Or add the project directory to your current session:
```powershell
$env:PATH += ";C:\Users\kinge\AuraProgrammingLanguage"
aura --version  # Now works!
```

---

## Option 2: Add Python Scripts to PATH (Permanent)

The `aura` command is installed in: `C:\Python314\Scripts\aura.exe`

**Make it globally available:**

```powershell
# Run this once (admin PowerShell or restart terminal after)
[Environment]::SetEnvironmentVariable(
    "Path",
    [Environment]::GetEnvironmentVariable("Path", "User") + ";C:\Python314\Scripts",
    "User"
)
```

Then **restart your terminal** and:
```powershell
aura --version  # Works from anywhere!
```

---

## Option 3: Use python -m (Always Works)

This always works, no setup needed:
```powershell
python -m transpiler.cli run examples/my_calculator.aura
python -m transpiler.cli dev examples/watch_test.aura
```

---

## Recommended for Development

**Use the `.bat` wrapper:**

```powershell
# Add to current session
cd C:\Users\kinge\AuraProgrammingLanguage
$env:PATH += ";$PWD"

# Now use anywhere in this session
aura run test.aura
aura dev test.aura
aura --help
```

---

## Quick Test

Try this:
```powershell
# From project root
.\aura --version
```

You should see:
```
Aura Programming Language v1.0.0
Natural language programming - write code in plain English
https://github.com/kingenious0/Aura-Programming-Language
```

✅ If that works, `aura` is ready!

---

## TL;DR

**Quickest solution right now:**
```powershell
# In project directory
.\aura run examples/my_calculator.aura
```

**To make it permanent:**
Add `C:\Python314\Scripts` to your PATH environment variable, then restart terminal.
