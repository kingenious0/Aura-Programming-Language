# Windows Encoding Fix for Aura

## Problem
Windows terminal uses `cp1252` encoding by default, which cannot display Unicode emojis (🔵, ✅, ❌, etc.) used in Aura's output.

## Solution
Added UTF-8 encoding configuration to both `transpiler.py` and `watch.py`:

```python
# Fix Windows console encoding for emoji support
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
```

## What This Does
- Detects if running on Windows (`sys.platform == 'win32'`)
- Wraps stdout and stderr with UTF-8 encoding
- Uses `errors='replace'` to handle any characters that still can't be encoded
- Allows emojis to display correctly in Windows terminal

## Files Modified
1. `transpiler/transpiler.py` - Main transpiler
2. `watch.py` - Watch mode script

## Testing
Run the transpiler to verify emojis display correctly:
```bash
python transpiler/transpiler.py test.aura
```

You should now see:
- 🔵 Aura Transpiler v1.0
- ✅ Success messages
- ❌ Error messages (if any)
- 🎉 Completion message

## Watch Mode
The watch mode now also properly displays emojis:
```bash
python watch.py test.aura
```

Output:
- 🌟 AURA WATCH MODE banner
- 🔄 Change detected messages
- ⚡ Transpiling messages
- ✅ Ready messages

## Cross-Platform Compatibility
This fix:
- ✅ Works on Windows (fixes the encoding issue)
- ✅ Works on macOS (no effect, already UTF-8)
- ✅ Works on Linux (no effect, already UTF-8)

The `if sys.platform == 'win32'` check ensures it only applies the fix on Windows systems.
