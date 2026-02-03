# Aura Programming Language

A revolutionary programming language that uses natural English to create beautiful web applications.

## Overview

Aura is a transpiler that converts English-like commands into professional HTML, CSS, and JavaScript. Write code the way you think!

## Features

- **Natural Language Syntax** - Write code in plain English
- **Beautiful Themes** - Dark, light, and default themes with modern design
- **Modular Architecture** - Easy to extend with new commands
- **Professional Output** - Generates clean, production-ready HTML
- **Simple Syntax** - Only 4 command types to learn
- **Watch Mode** - Auto-transpilation on file save for rapid development

## Installation

### Basic Installation
No installation required! Just Python 3.6+ with standard library.

```bash
# Clone or download this repository
cd AuraProgrammingLanguage
```

### Watch Mode (Optional)
For auto-transpilation on file save (like Vite!):

```bash
pip install watchdog
```

## Quick Start

### Option 1: Standard Mode

#### 1. Create an Aura file (`.aura`)

```aura
# my_app.aura
Use the dark theme

Create a heading with the text 'Hello World'
Create a button with the text 'Click Me'
When clicked, display 'Welcome to Aura!'
```

#### 2. Run the transpiler

```bash
python transpiler/transpiler.py my_app.aura
```

#### 3. Open the generated `index.html` in your browser! 🎉

### Option 2: Watch Mode ⚡ (Recommended for Development)

Start the watch server:

```bash
# Watch a specific file
python watch.py test.aura

# Watch all .aura files in current directory
python watch.py

# Watch all .aura files in a specific directory
python watch.py path/to/directory
```

Now every time you save your `.aura` file, it will automatically transpile! Just refresh your browser to see changes.

## Language Syntax

### 1. Variables (Data Storage)
```aura
The user's name is 'John'
The app's title is 'My App'
```

### 2. Actions (Event Handling)
```aura
When clicked, display 'Success!'
When clicked, alert 'Button pressed!'
```

### 3. UI Elements
```aura
Create a button with the text 'Submit'
Create a heading with the text 'Welcome'
Create a paragraph with the text 'Hello World'
Create a input with the text 'Enter name'
```

### 4. Themes
```aura
Use the dark theme
Use the light theme
```

## Project Structure

```
AuraProgrammingLanguage/
├── transpiler/
│   ├── __init__.py          # Package initialization
│   ├── transpiler.py        # Main transpiler engine
│   ├── parser.py            # Regex-based parser
│   └── html_generator.py    # HTML/CSS/JS generator
├── AURA_BIBLE.md            # Language specification
├── example.aura             # Example program
└── README.md                # This file
```

## How It Works

1. **Parser** (`parser.py`) - Uses regex to parse English commands
2. **Generator** (`html_generator.py`) - Uses string templates to create HTML
3. **Transpiler** (`transpiler.py`) - Orchestrates the process

## Adding New Commands

The modular architecture makes it easy to extend Aura:

### 1. Add a regex pattern in `parser.py`:
```python
self.patterns['new_command'] = re.compile(
    r"Your regex pattern here",
    re.IGNORECASE
)
```

### 2. Add a handler in `html_generator.py`:
```python
def _handle_new_command(self, cmd):
    # Your generation logic here
    pass
```

### 3. Update the command processor:
```python
elif cmd.command_type == 'new_command':
    self._handle_new_command(cmd)
```

## Examples

See `example.aura` for a complete demonstration of all features.

## Command-Line Usage

```bash
# Basic usage (outputs to index.html)
python transpiler/transpiler.py input.aura

# Specify output file
python transpiler/transpiler.py input.aura output.html

# Get help
python transpiler/transpiler.py
```

## Themes

### Dark Theme
- Modern glassmorphism design
- Gradient backgrounds
- Smooth animations
- Perfect for modern apps

### Light Theme
- Clean and professional
- High contrast
- Accessible design
- Great for business apps

### Default Theme
- Simple and minimal
- Fast loading
- Classic look

## Future Enhancements

- [ ] Loops and conditionals
- [ ] More UI components (tables, forms, cards)
- [ ] CSS customization commands
- [ ] Multi-page support
- [ ] Component reusability
- [ ] Data binding
- [ ] API integration commands

## Contributing

This is a modular system designed for easy extension. Feel free to:
- Add new command types
- Create new themes
- Improve the parser
- Add more UI elements

## License

Open source - feel free to use and modify!

## Author

Built with ❤️ for the Aura Programming Language project

---

**Start coding in English today!** 🚀
