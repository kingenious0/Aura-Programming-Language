# 🌟 Aura Watch Mode

Lightning-fast auto-transpilation for Aura - just like Vite! ⚡

## What is Watch Mode?

Watch Mode automatically monitors your `.aura` files and transpiles them instantly whenever you save. No more manually running the transpiler - just save and refresh your browser!

## Installation

Install the `watchdog` library:

```bash
pip install watchdog
```

That's it! The `watch.py` script is already included in your Aura installation.

## Usage

### Watch a Specific File (Recommended)

```bash
python watch.py test.aura
```

This will:
- ✅ Monitor only `test.aura` for changes
- ⚡ Auto-transpile on every save
- 🎯 Ignore other `.aura` files in the directory

### Watch All Files in Current Directory

```bash
python watch.py
```

This will:
- ✅ Monitor ALL `.aura` files in the current directory
- ⚡ Auto-transpile any `.aura` file when saved
- 📂 Watch only the current directory (not subdirectories)

### Watch a Specific Directory

```bash
python watch.py path/to/directory
```

This will:
- ✅ Monitor all `.aura` files in the specified directory
- ⚡ Auto-transpile on save
- 📂 Watch only that directory (not subdirectories)

## Development Workflow

Here's the recommended workflow for developing with Aura:

### 1. Start Watch Mode

```bash
python watch.py test.aura
```

You'll see:
```
============================================================
  🌟 AURA WATCH MODE
============================================================
  Lightning-fast auto-transpilation for Aura
  Press Ctrl+C to stop
============================================================

⚡ Server started at 12:42:48
📂 Watching: C:\Users\kinge\AuraProgrammingLanguage
🎯 Target: test.aura

💡 Tip: Save your .aura file to trigger auto-transpilation!
```

### 2. Open Your HTML File

Open `index.html` in your browser (the output of the transpiler).

### 3. Edit Your Aura File

Make changes to `test.aura` in your editor.

### 4. Save and See Changes

When you save:
```
🔄 Change detected in test.aura
⚡ Transpiling at 12:43:15...

🔵 Aura Transpiler v1.0
📂 Input:  test.aura
📄 Output: .\index.html

⚙️  Parsing Aura commands...
✅ Parsed 7 command(s)
...
✅ Ready in 500ms
```

### 5. Refresh Browser

Just refresh your browser to see the changes! 🎉

### 6. Stop Watch Mode

Press `Ctrl+C` when done:
```
👋 Stopping Aura watch mode...
✅ Goodbye!
```

## Features

### ⚡ Lightning Fast
- Debounced file watching (500ms)
- Instant transpilation on save
- No unnecessary rebuilds

### 🎯 Smart Watching
- Watch specific files or entire directories
- Ignores non-.aura files
- Prevents duplicate transpilations

### 🎨 Beautiful Output
- Vite-inspired interface
- Clear status messages
- Timestamps for each transpilation
- Color-coded output

### 🛡️ Robust
- Handles errors gracefully
- Shows transpiler output
- Clean shutdown with Ctrl+C

## Tips & Tricks

### Tip 1: Use with Live Server
Combine watch mode with a live server for the ultimate dev experience:

**Terminal 1:**
```bash
python watch.py test.aura
```

**Terminal 2:**
```bash
# If you have Python's http.server
python -m http.server 8000

# Or use VS Code's Live Server extension
```

Now you get:
- ✅ Auto-transpilation on save (watch.py)
- ✅ Auto-refresh in browser (live server)

### Tip 2: Multiple Files
If working on multiple Aura files, use directory watching:

```bash
python watch.py .
```

### Tip 3: Keep Terminal Visible
Keep the watch mode terminal visible while coding - it provides instant feedback on transpilation status and any errors.

## Troubleshooting

### "Module 'watchdog' not found"
Install the watchdog library:
```bash
pip install watchdog
```

### Watch Mode Not Detecting Changes
- Make sure you're saving the file (Ctrl+S)
- Check that the file has a `.aura` extension
- Verify the file is in the watched directory
- Try restarting watch mode

### Multiple Transpilations on One Save
This is normal - some editors trigger multiple save events. The debouncing (500ms) helps minimize this.

### Changes Not Showing in Browser
- Make sure to **refresh** your browser after transpilation
- Check the terminal to confirm transpilation completed successfully
- Verify you're viewing the correct `index.html` file

## Comparison: Standard vs Watch Mode

| Feature | Standard Mode | Watch Mode |
|---------|--------------|------------|
| Command | `python transpiler/transpiler.py test.aura` | `python watch.py test.aura` |
| Auto-transpile | ❌ Manual | ✅ Automatic |
| Best for | Production builds | Development |
| Speed | Fast | Lightning fast ⚡ |
| Convenience | Run each time | Set and forget |

## Advanced Usage

### Custom Debounce Time
Edit `watch.py` and change the `debounce_seconds` value:

```python
def __init__(self, target_file=None):
    self.target_file = target_file
    self.last_modified = {}
    self.debounce_seconds = 0.5  # Change this value
```

### Watch Subdirectories
Edit `watch.py` and change `recursive=False` to `recursive=True`:

```python
observer.schedule(event_handler, str(watch_dir), recursive=True)
```

## Why Watch Mode?

Watch mode makes Aura development feel like modern web development with tools like Vite, Webpack, or Parcel. You get:

- 🚀 **Faster iteration** - No manual transpilation
- 💡 **Better focus** - Stay in your editor
- ✨ **Modern DX** - Development experience that feels premium
- 🎯 **Fewer errors** - Instant feedback on syntax issues

## Next Steps

1. ✅ Install watchdog: `pip install watchdog`
2. ✅ Start watch mode: `python watch.py test.aura`
3. ✅ Open `index.html` in your browser
4. ✅ Edit your `.aura` file
5. ✅ Save and refresh to see changes!

---

**Happy coding with Aura! 🌟**
