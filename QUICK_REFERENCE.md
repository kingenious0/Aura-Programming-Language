# Aura Programming Language - Quick Reference

## Project Overview

**Repository**: https://github.com/kingenious0/Aura-Programming-Language
**Language**: Natural English to HTML/CSS/JavaScript transpiler
**Status**: Ready for VS Code extension publishing

---

## Running Aura Programs

### Standard Mode
```bash
python transpiler/transpiler.py test.aura
```

### Watch Mode (Auto-transpile on save)
```bash
python watch.py test.aura
```

---

## Aura Syntax

### Themes
```aura
Use the dark theme
Use the light theme
```

### UI Elements
```aura
Create a heading with the text 'Title'
Create a paragraph with the text 'Description'
Create a button with the text 'Click Me'
Create a input with the text 'Enter name'
```

### Actions
```aura
When clicked, display 'Message'
When clicked, alert 'Alert message'
And refresh the page
```

### Comments
```aura
# This is a comment
```

---

## VS Code Extension

### Location
`vscode-extension/` directory

### Files Created
- `package.json` - Extension manifest
- `extension.js` - Extension code
- `aura.tmLanguage.json` - Syntax highlighting
- `language-configuration.json` - Language settings
- `snippets/aura.json` - Code snippets
- `README.md` - Documentation
- `PUBLISHING_GUIDE.md` - Publishing instructions

### Features
- Syntax highlighting for .aura files
- 9 code snippets (btn, h1, p, input, dark, light, etc.)
- Commands: "Aura: Transpile" and "Aura: Start Watch Mode"
- Auto-closing quotes and brackets

---

## Publishing to VS Code Marketplace

### Quick Steps
1. Install vsce: `npm install -g vsce`
2. Create publisher at: https://marketplace.visualstudio.com/manage
3. Generate PAT at: https://dev.azure.com
4. Update publisher in `package.json`
5. Package: `cd vscode-extension && vsce package`
6. Publish: `vsce publish`

### Cost
**FREE** - No fees for publishing or hosting

### Timeline
- Validation: 1-5 minutes
- Listing: Immediate
- Search indexing: Up to 24 hours

### Full Guide
See `vscode-extension/PUBLISHING_GUIDE.md`

---

## Git Commands

### Check Status
```bash
git status
```

### Commit Changes
```bash
git add .
git commit -m "Your message"
git push
```

### View History
```bash
git log --oneline
```

---

## Project Structure

```
AuraProgrammingLanguage/
├── transpiler/
│   ├── __init__.py
│   ├── transpiler.py       # Main transpiler
│   ├── parser.py           # Command parser
│   └── html_generator.py   # HTML generator
├── vscode-extension/
│   ├── package.json
│   ├── extension.js
│   ├── aura.tmLanguage.json
│   ├── language-configuration.json
│   ├── snippets/aura.json
│   ├── README.md
│   ├── PUBLISHING_GUIDE.md
│   └── EXTENSION_SUMMARY.md
├── watch.py                # Watch mode script
├── test.aura              # Test file
├── example.aura           # Example file
├── demo.aura              # Demo file
├── README.md              # Main documentation
├── WATCH_MODE.md          # Watch mode guide
└── .gitignore             # Git exclusions
```

---

## Code Snippets (VS Code)

| Prefix | Description |
|--------|-------------|
| `btn` | Create button with click handler |
| `h1` | Create heading |
| `p` | Create paragraph |
| `input` | Create input field |
| `dark` | Use dark theme |
| `light` | Use light theme |
| `click` | Add click handler |
| `aura-template` | Full page template |

---

## Common Tasks

### Test Extension Locally
```bash
cd vscode-extension
vsce package
code --install-extension aura-language-1.0.0.vsix
```

### Update Extension Version
```bash
# Edit version in package.json, then:
vsce publish patch  # 1.0.0 -> 1.0.1
vsce publish minor  # 1.0.0 -> 1.1.0
vsce publish major  # 1.0.0 -> 2.0.0
```

### Run Transpiler
```bash
python transpiler/transpiler.py yourfile.aura
```

### Start Watch Mode
```bash
python watch.py yourfile.aura
```

---

## Resources

- **GitHub**: https://github.com/kingenious0/Aura-Programming-Language
- **VS Code Marketplace**: https://marketplace.visualstudio.com/manage
- **Azure DevOps**: https://dev.azure.com
- **Extension Publishing**: See `vscode-extension/PUBLISHING_GUIDE.md`

---

## Next Steps

1. ✅ Test extension locally
2. ✅ Add icon (128x128 PNG) to `vscode-extension/icons/`
3. ✅ Update publisher ID in `package.json`
4. ✅ Publish to VS Code Marketplace
5. ✅ Share with the community!

---

**Aura Programming Language - Write code in plain English!**
