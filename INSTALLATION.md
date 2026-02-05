# 🚀 Installing Aura Globally

## Make `aura` a System-Wide Command

Transform Aura from a project-in-a-folder to a **globally recognized command** like `npm`, `python`, or `git`!

---

## 📦 Installation

### Step 1: Install Aura

```bash
# Navigate to Aura directory
cd C:\Users\kinge\AuraProgrammingLanguage

# Install globally (editable mode)
pip install -e .
```

**What this does:**
- ✅ Registers `aura` as a global command
- ✅ Installs all dependencies
- ✅ Creates executable in Python Scripts folder
- ✅ Editable mode = changes update instantly!

### Step 2: Add to PATH (Windows)

The `aura` command is installed at:
```
C:\Users\<YourName>\AppData\Roaming\Python\Python3XX\Scripts\
```

**Option A: Automatic (PowerShell)**

```powershell
# Add to PATH for current session
$env:Path += ";C:\Users\$env:USERNAME\AppData\Roaming\Python\Python314\Scripts"

# Add permanently (requires admin)
[Environment]::SetEnvironmentVariable(
    "Path",
    [Environment]::GetEnvironmentVariable("Path", "User") + ";C:\Users\$env:USERNAME\AppData\Roaming\Python\Python314\Scripts",
    "User"
)
```

**Option B: Manual (GUI)**

1. Press `Win + X` → System
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "User variables", select `Path` → Edit
5. Click "New" and add:
   ```
   C:\Users\<YourName>\AppData\Roaming\Python\Python314\Scripts
   ```
6. Click OK on all dialogs
7. **Restart your terminal**

### Step 3: Verify Installation

```bash
# Open a NEW terminal window
aura --version
```

**Expected output:**
```
Aura Programming Language v1.0.0
Natural language programming - write code in plain English
https://github.com/kingenious0/Aura-Programming-Language
```

---

## ✨ Available Commands

### `aura --version`
Show version information

```bash
aura --version
# or
aura -v
```

### `aura --help`
Show help and all available commands

```bash
aura --help
# or
aura -h
```

### `aura init`
Initialize a new Aura project

```bash
mkdir my-app
cd my-app
aura init
```

### `aura dev`
Start hot-reload development server

```bash
aura dev
```

### `aura run <file>`
Build and run a single file

```bash
aura run Home.aura
```

### `aura build <file>`
Build without launching server

```bash
aura build Home.aura
```

---

## 🎯 The Complete Workflow

### Before (Local Commands)

```bash
# Had to use full paths
python -m transpiler.transpiler dev
.\aura.bat Home.aura
python watch.py .
```

### After (Global Commands)

```bash
# Clean, professional commands
aura init
aura dev
aura run Home.aura
```

---

## 🔄 Updating Aura

Since you installed with `-e` (editable mode), any changes you make to the code will be reflected immediately!

```bash
# Make changes to Aura code
# No need to reinstall!

# Just use the updated command
aura dev
```

---

## 🐛 Troubleshooting

### "aura is not recognized"

**Problem**: PATH not set correctly

**Solution**:
```bash
# Check where aura is installed
python -c "import site; print(site.USER_BASE + '\\Scripts')"

# Add that path to your PATH environment variable
```

### "Permission denied"

**Problem**: Need admin rights

**Solution**:
```bash
# Run PowerShell as Administrator
# Then run the PATH command
```

### "Module not found"

**Problem**: Dependencies not installed

**Solution**:
```bash
# Reinstall with dependencies
pip install -e . --force-reinstall
```

---

## 🌍 Cross-Platform Support

### Windows
```bash
pip install -e .
# Add Scripts folder to PATH
```

### Linux/Mac
```bash
pip install -e .
# Usually auto-added to PATH
```

---

## 🎉 Success!

Once installed, you can:

```bash
# From ANYWHERE on your system
cd ~/Desktop
mkdir my-startup
cd my-startup
aura init
aura dev
```

**No more `python -m`, no more `.\`, just pure `aura`!** 🚀

---

## 📊 Comparison

| Before | After |
|--------|-------|
| `python -m transpiler.transpiler dev` | `aura dev` |
| `.\aura.bat Home.aura` | `aura run Home.aura` |
| `python watch.py .` | `aura dev` |

**Professional. Clean. Industry-standard.** ✨

---

## 🚀 Next Steps

1. **Test it**: `aura --version`
2. **Create a project**: `aura init`
3. **Start developing**: `aura dev`
4. **Share with the world**: Your language is now installable!

---

**Aura is now a globally recognized command!** 🌟
