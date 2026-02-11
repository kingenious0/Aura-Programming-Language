# 🌟 Aura Transpiler - Quick Start Guide

## What You've Built

A **modular transpiler engine** that converts English-like Aura code into professional HTML/CSS/JavaScript!

## 📁 Project Structure

```
AuraProgrammingLanguage/
├── transpiler/              # Core transpiler engine
│   ├── __init__.py         # Package initialization
│   ├── parser.py           # Regex-based parser (3.9 KB)
│   ├── html_generator.py   # HTML/CSS/JS generator (11.6 KB)
│   └── transpiler.py       # Main orchestrator (4.5 KB)
│
├── AURA_BIBLE.md           # Language specification
├── README.md               # Full documentation
├── EXTENDING.md            # Developer guide for adding commands
│
├── example.aura            # Example Aura program
├── test.aura               # Simple test file
└── index.html              # Generated output (3.5 KB)
```

## ✅ What's Working

### 1. **Parser Module** (`parser.py`)
- ✅ Regex-based parsing for all 4 command types
- ✅ Line-by-line processing with error reporting
- ✅ Validation and debugging support
- ✅ Modular pattern system (easy to extend)

### 2. **HTML Generator** (`html_generator.py`)
- ✅ String template-based HTML generation
- ✅ Three professional themes (dark, light, default)
- ✅ Modern CSS with glassmorphism and gradients
- ✅ JavaScript event handling
- ✅ Unique element ID generation

### 3. **Main Transpiler** (`transpiler.py`)
- ✅ Clean CLI interface
- ✅ Beautiful console output with emojis
- ✅ Error handling and validation
- ✅ File I/O management

## 🚀 How to Use

### Basic Usage

```bash
# Transpile a .aura file (outputs to index.html)
python transpiler/transpiler.py example.aura

# Specify custom output file
python transpiler/transpiler.py example.aura output.html
```

### Example Output

```
🔵 Aura Transpiler v1.0
📂 Input:  example.aura
📄 Output: .\index.html

⚙️  Parsing Aura commands...
✅ Parsed 10 command(s)

📋 Commands found:
   1. [THEME] Use the dark theme
   2. [VARIABLE] The user's name is 'Akwasi'
   3. [VARIABLE] The app's title is 'Welcome to Aura'
   4. [UI_ELEMENT] Create a heading with the text 'Welcome to Aura Programming Language'
   5. [UI_ELEMENT] Create a paragraph with the text 'This is a revolutionary way to code using natural English!'
   6. [UI_ELEMENT] Create a button with the text 'Click Me'
   7. [ACTION] When clicked, display 'Hello from Aura! 🎉'
   8. [UI_ELEMENT] Create a input with the text 'Enter your name'
   9. [UI_ELEMENT] Create a button with the text 'Submit'
   10. [ACTION] When clicked, display 'Form submitted successfully!'

🎨 Generating HTML...
✅ HTML generated successfully

💾 Writing to .\index.html...
✅ File written successfully

🎉 Transpilation complete!
📍 Open .\index.html in your browser to view the result.
```

## 📝 Aura Language Syntax

### 1. Variables
```aura
The user's name is 'John'
The app's title is 'My App'
```

### 2. UI Elements
```aura
Create a heading with the text 'Welcome'
Create a paragraph with the text 'Hello World'
Create a button with the text 'Click Me'
Create a input with the text 'Enter name'
```

### 3. Actions (Events)
```aura
When clicked, display 'Success!'
When clicked, alert 'Button pressed!'
```

### 4. Themes
```aura
Use the dark theme
Use the light theme
```

## 🎨 Generated HTML Features

The transpiler generates **professional, production-ready HTML** with:

### Dark Theme
- Modern glassmorphism design
- Gradient backgrounds (#1a1a2e → #16213e)
- Smooth animations and transitions
- Gradient text effects
- Hover effects with elevation

### Light Theme
- Clean, professional design
- Gradient backgrounds (#f5f7fa → #c3cfe2)
- High contrast for accessibility
- Smooth interactions

### Default Theme
- Simple, minimal design
- Fast loading
- Classic look

### All Themes Include:
- Responsive design
- Modern typography (Segoe UI)
- Smooth transitions (0.3s ease)
- Focus states for accessibility
- Unique element IDs
- Event handling with JavaScript

## 🔧 Extending Aura

The system is **highly modular** and easy to extend. See `EXTENDING.md` for detailed instructions.

### Quick Example: Adding a Link Command

**1. Add regex pattern in `parser.py`:**
```python
'link': re.compile(
    r"Create\s+a\s+link\s+to\s+['\"](?P<url>[^'\"]+)['\"]\s+with\s+the\s+text\s+['\"](?P<text>[^'\"]+)['\"]",
    re.IGNORECASE
),
```

**2. Add handler in `html_generator.py`:**
```python
def _handle_link(self, cmd):
    url = cmd.data['url']
    text = cmd.data['text']
    element_id = f"aura_link_{len(self.body_elements)}"
    html = f'<a id="{element_id}" href="{url}" target="_blank">{text}</a>'
    self.body_elements.append(html)
```

**3. Connect in `_process_command`:**
```python
elif cmd.command_type == 'link':
    self._handle_link(cmd)
```

That's it! 🎉

## 🧪 Testing

Try the included examples:

```bash
# Test the dark theme example
python transpiler/transpiler.py example.aura

# Test the light theme
python transpiler/transpiler.py test.aura

# Open the generated HTML in your browser
start index.html  # Windows
```

## 📚 Documentation

- **`README.md`** - Full project documentation
- **`AURA_BIBLE.md`** - Language specification
- **`EXTENDING.md`** - Developer guide for adding commands

## 🎯 Key Features

✅ **Modular Architecture** - Easy to maintain and extend
✅ **Regex-Based Parsing** - Fast and flexible
✅ **String Templates** - Clean HTML generation
✅ **Professional Output** - Production-ready HTML/CSS/JS
✅ **Beautiful Themes** - Modern, responsive designs
✅ **Error Handling** - Clear error messages
✅ **CLI Interface** - User-friendly command-line tool
✅ **No Dependencies** - Uses only Python standard library

## 🚀 Next Steps

1. **Try the examples** - Run `example.aura` and `test.aura`
2. **Create your own** - Write a `.aura` file with your own commands
3. **Extend the language** - Add new commands (see `EXTENDING.md`)
4. **Customize themes** - Modify the CSS in `html_generator.py`

## 💡 Future Ideas

- Loops and conditionals
- More UI components (tables, forms, cards)
- Multi-page support
- Component reusability
- Data binding
- API integration commands
- Custom CSS commands
- Responsive layout commands

## 🎉 Success!

You now have a fully functional transpiler that:
- ✅ Reads `.aura` files
- ✅ Parses English commands with regex
- ✅ Generates professional HTML with string templates
- ✅ Is modular and extensible
- ✅ Has beautiful, modern themes
- ✅ Includes comprehensive documentation

**Open `index.html` in your browser to see the magic!** 🌟
