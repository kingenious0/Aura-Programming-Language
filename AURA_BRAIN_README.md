# 🧠 Aura Brain - Real-Time Autocorrection System

## Overview

The Aura Brain is a **persistent AI-powered autocorrection system** that provides instant syntax fixes as you type. It uses a local Qwen2.5-0.5B model running in the background for privacy and speed.

## Features

### 1. **Ghost Text Suggestions** (Coming Soon)
As you type, the Brain analyzes your code and shows corrections as gray "ghost text". Press `Tab` to accept.

```aura
You type:  crete a button with text 'Click'
Ghost:     Create a button with the text 'Click'  [Press Tab]
```

### 2. **Manual Correction** (Available Now)
Press `Ctrl+Shift+F` (or `Cmd+Shift+F` on Mac) to instantly correct the current line.

```aura
Before:  create is card with title 'Hello'
After:   Create a card with the title 'Hello'
```

### 3. **Auto-Save Correction** (Current Default)
When you save your file, the Brain automatically fixes all errors and rewrites the file.

## Architecture

```
┌─────────────────┐
│   VS Code       │
│   Extension     │
└────────┬────────┘
         │ JSON-RPC
         ▼
┌─────────────────┐
│  Brain Daemon   │  ← Persistent process
│  (Qwen 0.5B)    │     Keeps model in memory
└─────────────────┘
```

### Components

1. **`brain_daemon.py`** - Background service that keeps the AI model loaded
2. **`brain_client.py`** - Python client for communicating with the daemon
3. **`extension.js`** - VS Code extension with inline completion provider

## Speed Optimization

### Current Performance
- **Cold start** (first correction): ~2 seconds (model loading)
- **Warm corrections**: ~100-300ms per line
- **Target**: Sub-100ms with optimizations

### Optimization Strategies

1. **Persistent Daemon** ✅
   - Model stays loaded in memory
   - No startup overhead after first launch

2. **Reduced Context Window** ✅
   - `n_ctx=256` (down from 512)
   - Faster inference for single-line corrections

3. **Batch Processing** ✅
   - `n_batch=128` for efficient GPU utilization

4. **Future Optimizations**
   - [ ] Prompt caching (keep system prompt in memory)
   - [ ] Quantized model (GGUF Q4_K_M for 2x speed)
   - [ ] GPU acceleration (CUDA/Metal)
   - [ ] Pre-computed corrections for common typos

## Usage

### Starting the Daemon Manually

```bash
# Start the daemon
python -m transpiler.brain_daemon

# Test it with a correction request
echo '{"jsonrpc":"2.0","id":1,"method":"correct","params":{"line":"crete a button"}}' | python -m transpiler.brain_daemon
```

### Using in VS Code

1. **Automatic**: The daemon starts when you open an `.aura` file
2. **Manual Correction**: Press `Ctrl+Shift+F` on any line
3. **Ghost Text**: (Coming soon) Type and wait 100ms for suggestions

### Using Programmatically

```python
from transpiler.brain_client import get_brain_client

# Get the singleton client
client = get_brain_client()

# Start daemon (if not already running)
client.start_daemon()

# Request correction
result = client.correct("crete a button with text 'Click'")
print(result)
# {
#   "original": "crete a button with text 'Click'",
#   "corrected": "Create a button with the text 'Click'",
#   "changed": True,
#   "time_ms": 127.3
# }

# Stop daemon when done
client.stop_daemon()
```

## Aura Syntax Rules

The Brain is trained on these patterns:

### Themes
```aura
Use the dark theme
Use the light theme
Use the default theme
```

### UI Elements
```aura
Create a heading with the text 'Welcome'
Create a paragraph with the text 'Hello World'
Create a button with the text 'Click Me'
Create an input with the text 'Enter name'
Create a card with the title 'Title' and description 'Description'
Create an image from 'url.jpg'
```

### Navigation
```aura
Create a global navbar with links [Home, About, Contact]
Create a global navbar with logo 'MyApp' and links [Home, About]
```

### Actions
```aura
When clicked, display 'Success!'
When clicked, alert 'Warning!'
When clicked, refresh the page
When clicked, show the card
When clicked, hide the button
```

### Styling
```aura
Make the button red
Make the heading bold
Align the paragraph to the center
Put the card in the middle
```

## Common Fixes

| Error | Correction |
|-------|-----------|
| `crete` | `Create` |
| `create is card` | `Create a card` |
| `create card is title` | `Create a card with the title` |
| `with title` | `with the title` |
| `and description` | `and description` (or `and the description`) |
| Missing `a`, `the` | Automatically added |
| Lowercase commands | Capitalized |

## Troubleshooting

### Daemon won't start
```bash
# Check if llama-cpp-python is installed
pip install llama-cpp-python

# Ensure model is downloaded
python -c "from transpiler.setup import ensure_aura_brain; ensure_aura_brain()"
```

### Corrections are slow
- **First correction**: Model loading takes ~2 seconds (normal)
- **Subsequent corrections**: Should be <300ms
- **If still slow**: Check CPU usage, close other apps

### Ghost text not appearing
- Feature is currently in development
- Use manual correction (`Ctrl+Shift+F`) instead

## Performance Benchmarks

| Scenario | Time | Notes |
|----------|------|-------|
| Daemon startup | ~2s | One-time cost |
| First correction | ~300ms | Includes prompt processing |
| Subsequent corrections | ~100-200ms | Model is warm |
| With GPU (future) | ~50-100ms | Requires CUDA setup |

## Roadmap

- [x] Background daemon architecture
- [x] JSON-RPC communication
- [x] Manual correction command
- [ ] Ghost text inline completions
- [ ] Prompt caching for speed
- [ ] GPU acceleration
- [ ] Multi-line context awareness
- [ ] Visual feedback (purple glow)
- [ ] Confidence scoring
- [ ] Custom user corrections learning

## Contributing

To improve the Brain's accuracy, add examples to the system prompt in `brain_daemon.py`:

```python
"Input: your broken syntax\nOutput: Correct syntax\n"
```

The more examples, the smarter the Brain becomes!
