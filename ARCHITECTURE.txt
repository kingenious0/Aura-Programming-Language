"""
Aura Transpiler - Architecture Diagram

┌─────────────────────────────────────────────────────────────────┐
│                     AURA TRANSPILER ENGINE                       │
│                         Version 1.0                              │
└─────────────────────────────────────────────────────────────────┘

                            INPUT
                              ↓
                    ┌─────────────────┐
                    │  example.aura   │
                    │                 │
                    │  Use the dark   │
                    │  theme          │
                    │                 │
                    │  Create a       │
                    │  button with    │
                    │  the text       │
                    │  'Click Me'     │
                    │                 │
                    │  When clicked,  │
                    │  display 'Hi!'  │
                    └─────────────────┘
                              ↓
        ┌─────────────────────────────────────────────┐
        │         PARSER MODULE (parser.py)            │
        │                                              │
        │  ┌────────────────────────────────────┐     │
        │  │  Regex Pattern Matching            │     │
        │  │  ────────────────────────          │     │
        │  │  • Variables Pattern               │     │
        │  │  • Actions Pattern                 │     │
        │  │  • UI Elements Pattern             │     │
        │  │  • Theme Pattern                   │     │
        │  └────────────────────────────────────┘     │
        │                                              │
        │  ┌────────────────────────────────────┐     │
        │  │  AuraCommand Objects               │     │
        │  │  ────────────────────              │     │
        │  │  command_type: 'theme'             │     │
        │  │  data: {'theme': 'dark'}           │     │
        │  │  line_number: 1                    │     │
        │  └────────────────────────────────────┘     │
        └─────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────────────────────────────┐
        │    HTML GENERATOR (html_generator.py)       │
        │                                              │
        │  ┌────────────────────────────────────┐     │
        │  │  Theme Selection                   │     │
        │  │  ────────────────                  │     │
        │  │  • Dark Theme CSS                  │     │
        │  │  • Light Theme CSS                 │     │
        │  │  • Default Theme CSS               │     │
        │  └────────────────────────────────────┘     │
        │                                              │
        │  ┌────────────────────────────────────┐     │
        │  │  HTML Element Generation           │     │
        │  │  ────────────────────────          │     │
        │  │  <button id="aura_button_0">       │     │
        │  │    Click Me                        │     │
        │  │  </button>                         │     │
        │  └────────────────────────────────────┘     │
        │                                              │
        │  ┌────────────────────────────────────┐     │
        │  │  JavaScript Event Binding          │     │
        │  │  ────────────────────────          │     │
        │  │  document.getElementById(...)      │     │
        │  │    .addEventListener('click', ...) │     │
        │  └────────────────────────────────────┘     │
        │                                              │
        │  ┌────────────────────────────────────┐     │
        │  │  String Template Assembly          │     │
        │  │  ────────────────────────          │     │
        │  │  HTML_TEMPLATE.substitute(...)     │     │
        │  └────────────────────────────────────┘     │
        └─────────────────────────────────────────────┘
                              ↓
                    ┌─────────────────┐
                    │   index.html    │
                    │                 │
                    │  <!DOCTYPE html>│
                    │  <html>         │
                    │    <head>       │
                    │      <style>    │
                    │        /* Dark  │
                    │        Theme */ │
                    │      </style>   │
                    │    </head>      │
                    │    <body>       │
                    │      <button>   │
                    │        Click Me │
                    │      </button>  │
                    │      <script>   │
                    │        /* Event │
                    │        Handler*/│
                    │      </script>  │
                    │    </body>      │
                    │  </html>        │
                    └─────────────────┘
                              ↓
                         OUTPUT


═══════════════════════════════════════════════════════════════════

                      MODULE BREAKDOWN

┌─────────────────────────────────────────────────────────────────┐
│  parser.py (3.9 KB)                                              │
│  ──────────────────                                              │
│                                                                  │
│  Classes:                                                        │
│    • AuraCommand (dataclass)                                    │
│    • AuraParser                                                 │
│                                                                  │
│  Key Methods:                                                   │
│    • parse_file(filepath) → List[AuraCommand]                   │
│    • _parse_line(line, line_num) → AuraCommand                  │
│    • validate_commands(commands) → bool                         │
│                                                                  │
│  Regex Patterns:                                                │
│    • variable: The [obj]'s [prop] is '[value]'                  │
│    • action: When [event], [action] '[content]'                 │
│    • ui_element: Create a [element] with the text '[text]'      │
│    • theme: Use the [theme] theme                               │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  html_generator.py (11.6 KB)                                     │
│  ────────────────────────────                                    │
│                                                                  │
│  Classes:                                                        │
│    • HTMLGenerator                                              │
│                                                                  │
│  Key Methods:                                                   │
│    • generate(commands) → str                                   │
│    • _process_command(cmd)                                      │
│    • _handle_variable(cmd)                                      │
│    • _handle_theme(cmd)                                         │
│    • _handle_ui_element(cmd)                                    │
│    • _handle_action(cmd)                                        │
│    • _build_html() → str                                        │
│                                                                  │
│  Templates:                                                     │
│    • HTML_TEMPLATE (string.Template)                            │
│    • THEMES (dict with dark, light, default)                    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  transpiler.py (4.5 KB)                                          │
│  ───────────────────────                                         │
│                                                                  │
│  Classes:                                                        │
│    • AuraTranspiler                                             │
│                                                                  │
│  Key Methods:                                                   │
│    • transpile(input_file, output_file) → str                   │
│    • transpile_string(aura_code) → str                          │
│    • main() - CLI interface                                     │
│                                                                  │
│  Features:                                                      │
│    • File I/O management                                        │
│    • Error handling                                             │
│    • Progress reporting                                         │
│    • Beautiful console output                                   │
└─────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════

                    COMMAND FLOW EXAMPLE

Input Aura Code:
  "Create a button with the text 'Click Me'"

Step 1: PARSER
  ↓
  Pattern Match: ui_element regex
  ↓
  Capture Groups:
    - element: "button"
    - text: "Click Me"
  ↓
  Create AuraCommand:
    - command_type: "ui_element"
    - data: {"element": "button", "text": "Click Me"}
    - line_number: 1

Step 2: HTML GENERATOR
  ↓
  Process Command Type: ui_element
  ↓
  Call _handle_ui_element()
  ↓
  Generate HTML:
    <button id="aura_button_0">Click Me</button>
  ↓
  Add to body_elements list

Step 3: ASSEMBLY
  ↓
  Combine all elements
  ↓
  Apply theme CSS
  ↓
  Add event scripts
  ↓
  Use HTML_TEMPLATE.substitute()
  ↓
  Output complete HTML document


═══════════════════════════════════════════════════════════════════

                      EXTENSIBILITY

Adding a new command is simple:

1. Add regex pattern to parser.py:
   ────────────────────────────────
   'new_cmd': re.compile(r"Your pattern here", re.IGNORECASE)

2. Add handler to html_generator.py:
   ─────────────────────────────────
   def _handle_new_cmd(self, cmd):
       # Your logic here
       pass

3. Connect in _process_command():
   ──────────────────────────────
   elif cmd.command_type == 'new_cmd':
       self._handle_new_cmd(cmd)

That's it! The modular architecture makes extension trivial.


═══════════════════════════════════════════════════════════════════

                    TECHNOLOGY STACK

• Python 3.6+ (Standard Library Only)
  ├── re (Regular Expressions)
  ├── string (Template)
  ├── os (File Operations)
  ├── sys (CLI Arguments)
  ├── pathlib (Path Handling)
  ├── dataclasses (Data Structures)
  └── datetime (Timestamps)

• No External Dependencies!


═══════════════════════════════════════════════════════════════════

                      FILE SIZES

parser.py         : 3.9 KB  (120+ lines)
html_generator.py : 11.6 KB (300+ lines)
transpiler.py     : 4.5 KB  (130+ lines)
────────────────────────────────────────
Total Engine      : 20 KB   (550+ lines)

Documentation     : 20 KB   (4 files)
Examples          : 1 KB    (2 files)
Generated Output  : 3.5 KB  (2 files)


═══════════════════════════════════════════════════════════════════

                    SUCCESS METRICS

✅ Modular Architecture
✅ Regex-Based Parsing
✅ String Template Generation
✅ Professional HTML Output
✅ Zero Dependencies
✅ Easy to Extend
✅ Well Documented
✅ Tested & Working

"""
