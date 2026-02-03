# Aura Language Support for VS Code

Professional syntax highlighting and language support for the Aura programming language.

## Features

- **Syntax Highlighting**: Beautiful syntax highlighting for Aura files
  - Keywords: `Create`, `Use`, `When`, `And`
  - UI Elements: `button`, `heading`, `paragraph`, `input`, `card`
  - Strings: Single and double quoted strings
  - Comments: Line comments with `#`
  - Themes: `dark`, `light`, `default`
  - Actions: `clicked`, `display`, `alert`, `refresh`

- **Code Snippets**: Quick snippets for common patterns
  - `btn` - Create a button with click handler
  - `h1` - Create a heading
  - `p` - Create a paragraph
  - `input` - Create an input field
  - `dark` - Use dark theme
  - `light` - Use light theme
  - `click` - Add click event handler
  - `aura-template` - Full page template

- **Commands**:
  - `Aura: Transpile` - Transpile current Aura file to HTML
  - `Aura: Start Watch Mode` - Start auto-transpilation on save

- **Auto-Closing**: Automatic closing of quotes and brackets
- **Comment Support**: Line comments with `#`

## Installation

### From Marketplace (Coming Soon)
Search for "Aura Language Support" in the VS Code Extensions marketplace.

### Manual Installation
1. Copy the `vscode-extension` folder to your VS Code extensions directory:
   - Windows: `%USERPROFILE%\.vscode\extensions\`
   - macOS/Linux: `~/.vscode/extensions/`
2. Restart VS Code

### Build from Source
```bash
cd vscode-extension
npm install
npm install -g vsce
vsce package
code --install-extension aura-language-*.vsix
```

## Usage

1. Open any `.aura` file
2. Syntax highlighting will be applied automatically
3. Use snippets by typing the prefix and pressing Tab
4. Run commands from the Command Palette (Ctrl+Shift+P / Cmd+Shift+P)

## Example

```aura
# My First Aura App
Use the dark theme

Create a heading with the text 'Welcome to Aura'
Create a paragraph with the text 'Build apps with natural language'
Create a button with the text 'Get Started'
When clicked, display 'Hello, World!'
```

## Requirements

- VS Code 1.60.0 or higher
- Python 3.6+ (for transpiler commands)
- Aura transpiler installed

## Extension Settings

This extension contributes the following settings:

* `aura.transpilerPath`: Path to the Aura transpiler (default: `transpiler/transpiler.py`)
* `aura.watchPath`: Path to the watch mode script (default: `watch.py`)

## Known Issues

None at this time. Please report issues on GitHub.

## Release Notes

### 1.0.0

Initial release:
- Syntax highlighting for Aura language
- Code snippets
- Transpiler and watch mode commands
- Auto-closing pairs
- Comment support

## Contributing

Contributions are welcome! Please visit the [GitHub repository](https://github.com/kingenious0/Aura-Programming-Language).

## License

Open source - see LICENSE file for details.

---

**Enjoy coding in Aura!**
