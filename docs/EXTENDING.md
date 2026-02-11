# Extending Aura - Developer Guide

This guide shows you how to add new commands to the Aura programming language.

## Architecture Overview

The Aura transpiler has three main components:

1. **Parser** (`parser.py`) - Uses regex to parse English commands
2. **HTML Generator** (`html_generator.py`) - Converts commands to HTML/CSS/JS
3. **Transpiler** (`transpiler.py`) - Orchestrates the process

## Adding a New Command - Step by Step

Let's add a new command: **"Create a link to [url] with the text [text]"**

### Step 1: Add Regex Pattern to Parser

Edit `transpiler/parser.py` and add your pattern to the `__init__` method:

```python
def __init__(self):
    self.patterns = {
        # ... existing patterns ...
        
        # NEW: Link creation pattern
        'link': re.compile(
            r"Create\s+a\s+link\s+to\s+['\"](?P<url>[^'\"]+)['\"]\s+with\s+the\s+text\s+['\"](?P<text>[^'\"]+)['\"]",
            re.IGNORECASE
        ),
    }
```

**Regex Tips:**
- Use `(?P<name>...)` for named capture groups
- `\s+` matches whitespace
- `[^'\"]+` matches anything except quotes
- `re.IGNORECASE` makes it case-insensitive

### Step 2: Add Handler to HTML Generator

Edit `transpiler/html_generator.py` and add a handler method:

```python
def _handle_link(self, cmd):
    """Handle link creation"""
    url = cmd.data['url']
    text = cmd.data['text']
    
    element_id = f"aura_link_{len(self.body_elements)}"
    
    html = f'<a id="{element_id}" href="{url}" target="_blank">{text}</a>'
    self.body_elements.append(html)
```

### Step 3: Connect Handler in Process Method

In `html_generator.py`, update the `_process_command` method:

```python
def _process_command(self, cmd):
    """Process a single command"""
    if cmd.command_type == 'variable':
        self._handle_variable(cmd)
    elif cmd.command_type == 'theme':
        self._handle_theme(cmd)
    elif cmd.command_type == 'ui_element':
        self._handle_ui_element(cmd)
    elif cmd.command_type == 'action':
        self._handle_action(cmd)
    elif cmd.command_type == 'link':  # NEW
        self._handle_link(cmd)
```

### Step 4: (Optional) Add Styling

If your new element needs custom styling, add it to the theme templates in `html_generator.py`:

```python
THEMES = {
    'dark': """
        /* ... existing styles ... */
        
        a {
            color: #667eea;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        
        a:hover {
            color: #764ba2;
            text-decoration: underline;
        }
    """,
    # ... repeat for other themes ...
}
```

### Step 5: Test Your New Command

Create a test file `test_link.aura`:

```aura
Use the dark theme

Create a heading with the text 'My Links'
Create a link to "https://github.com" with the text "Visit GitHub"
```

Run the transpiler:

```bash
python transpiler/transpiler.py test_link.aura
```

## More Examples

### Example 1: Image Command

**Syntax:** `"Display an image from [url] with alt text [text]"`

```python
# In parser.py
'image': re.compile(
    r"Display\s+an\s+image\s+from\s+['\"](?P<url>[^'\"]+)['\"]\s+with\s+alt\s+text\s+['\"](?P<alt>[^'\"]+)['\"]",
    re.IGNORECASE
),

# In html_generator.py
def _handle_image(self, cmd):
    url = cmd.data['url']
    alt = cmd.data['alt']
    element_id = f"aura_image_{len(self.body_elements)}"
    html = f'<img id="{element_id}" src="{url}" alt="{alt}" style="max-width: 100%; border-radius: 10px;">'
    self.body_elements.append(html)
```

### Example 2: List Command

**Syntax:** `"Create a list with items [item1], [item2], [item3]"`

```python
# In parser.py
'list': re.compile(
    r"Create\s+a\s+list\s+with\s+items\s+(?P<items>.+)",
    re.IGNORECASE
),

# In html_generator.py
def _handle_list(self, cmd):
    items_str = cmd.data['items']
    # Split by comma and clean up
    items = [item.strip().strip("'\"") for item in items_str.split(',')]
    
    element_id = f"aura_list_{len(self.body_elements)}"
    html = f'<ul id="{element_id}">\n'
    for item in items:
        html += f'    <li>{item}</li>\n'
    html += '</ul>'
    
    self.body_elements.append(html)
```

### Example 3: Conditional Styling

**Syntax:** `"Make the [element] [style property] [value]"`

```python
# In parser.py
'style': re.compile(
    r"Make\s+the\s+(?P<element>\w+)\s+(?P<property>color|background|size)\s+['\"](?P<value>[^'\"]+)['\"]",
    re.IGNORECASE
),

# In html_generator.py
def _handle_style(self, cmd):
    element = cmd.data['element']
    property = cmd.data['property']
    value = cmd.data['value']
    
    # Map to CSS properties
    css_map = {
        'color': 'color',
        'background': 'background-color',
        'size': 'font-size'
    }
    
    css_property = css_map.get(property, property)
    
    # Apply to last element or create a style rule
    script = f"""
    document.querySelectorAll('[id*="{element}"]').forEach(el => {{
        el.style.{css_property.replace('-', '')} = '{value}';
    }});
    """
    self.scripts.append(script)
```

## Best Practices

1. **Keep Patterns Simple** - Start with simple regex, add complexity as needed
2. **Use Named Groups** - Makes data extraction cleaner
3. **Validate Input** - Check for required fields in handlers
4. **Add Comments** - Document your regex patterns
5. **Test Thoroughly** - Create test files for each new command
6. **Follow Naming** - Use `_handle_<command_type>` for handlers
7. **Maintain Modularity** - Each command should be independent

## Command Categories

### Data Commands
- Variables
- Constants
- Data structures

### UI Commands
- Elements (buttons, inputs, etc.)
- Layouts (containers, grids)
- Media (images, videos)

### Action Commands
- Events (click, hover, submit)
- Animations
- Transitions

### Style Commands
- Themes
- Custom styling
- Responsive design

## Debugging Tips

1. **Test Regex Online** - Use regex101.com to test patterns
2. **Print Debug Info** - Add print statements in handlers
3. **Check Line Numbers** - Parser tracks line numbers for errors
4. **Validate HTML** - Use W3C validator on output
5. **Browser Console** - Check for JavaScript errors

## Common Pitfalls

❌ **Don't:** Use greedy regex that matches too much
✅ **Do:** Use specific patterns with boundaries

❌ **Don't:** Forget to escape special characters
✅ **Do:** Use raw strings (r"...") and escape properly

❌ **Don't:** Hard-code element IDs
✅ **Do:** Generate unique IDs dynamically

❌ **Don't:** Mix parsing and generation logic
✅ **Do:** Keep parser and generator separate

## Future Ideas

Here are some commands you could implement:

- **Forms:** `"Create a form with fields [name], [email], [message]"`
- **Tables:** `"Create a table with columns [col1], [col2]"`
- **Cards:** `"Create a card with title [title] and content [content]"`
- **Modals:** `"Create a modal with the text [text]"`
- **Navigation:** `"Create a navbar with links [link1], [link2]"`
- **Animations:** `"Animate the [element] with [effect]"`
- **Conditionals:** `"If [condition], then [action]"`
- **Loops:** `"Repeat [number] times: [action]"`

## Contributing

When adding new commands:

1. Update `AURA_BIBLE.md` with the new syntax
2. Add examples to `example.aura`
3. Update `README.md` with documentation
4. Create test cases
5. Ensure backward compatibility

## Questions?

The codebase is well-commented and modular. Start by reading:
1. `parser.py` - See how patterns work
2. `html_generator.py` - See how HTML is generated
3. `example.aura` - See syntax examples

Happy coding! 🚀
