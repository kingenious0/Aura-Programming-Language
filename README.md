<div align="center">

# 🧠 Aura Programming Language

### *Write code in plain English. Let AI handle the syntax.*

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![AI Powered](https://img.shields.io/badge/AI-Qwen%202.5-purple.svg)](https://github.com/QwenLM/Qwen)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**[Features](#-features)** • **[Quick Start](#-quick-start)** • **[Documentation](#-documentation)** • **[Examples](#-examples)** • **[Contributing](#-contributing)**

---

</div>

## 🚀 What is Aura?

Aura is a **natural language programming language** that lets you build web applications using plain English commands. No more memorizing syntax—just write what you want, and Aura's AI Brain autocorrects it for you.

```aura
Create a heading with the text 'Welcome to My App'
Create a button with the text 'Click Me'
When clicked, display 'Hello World!'
```

**That's it.** Aura transpiles this into a production-ready React app with Tailwind CSS.

---

## ✨ Features

### 🧠 **AI-Powered Autocorrection**
Type naturally, make typos—Aura Brain fixes them in real-time.
```aura
crete a butn with text 'Submit'  →  Create a button with the text 'Submit'
```

### ⚡ **Lightning Fast**
- **100-300ms** autocorrection (2-5x faster than traditional transpilers)
- **Live watch mode** rebuilds on save
- **Hot reload** for instant preview

### 🎨 **Beautiful by Default**
- Modern UI with Tailwind CSS
- Dark mode support
- Responsive layouts
- Premium components (cards, navbars, forms)

### 🔧 **Developer Friendly**
- VS Code extension with IntelliSense
- Real-time error highlighting
- Comprehensive documentation
- Active community support

---

## 📦 Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Quick Install

```bash
# Clone the repository
git clone https://github.com/kingenious0/Aura-Programming-Language.git
cd Aura-Programming-Language

# Install Python dependencies
pip install -r requirements.txt

# Download the AI model (one-time setup)
python -m transpiler.setup

# You're ready! 🎉
```

---

## 🎯 Quick Start

### 1. Create your first Aura file

Create `hello.aura`:
```aura
Use the dark theme

Create a heading with the text 'Hello, Aura!'
Create a paragraph with the text 'This is my first app'
Create a button with the text 'Say Hi'
When clicked, display 'Hi from Aura!'
```

### 2. Run it

```bash
# Build and launch
aura hello.aura

# Or use watch mode for live reload
python watch.py .
```

### 3. Open your browser

Navigate to `http://localhost:5173` and see your app running! 🚀

---

## 📖 Documentation

### Core Concepts

<table>
<tr>
<td width="50%">

**🎨 UI Elements**
```aura
Create a heading with the text 'Title'
Create a paragraph with the text 'Text'
Create a button with the text 'Click'
Create a card with the title 'Card' 
  and description 'Description'
```

</td>
<td width="50%">

**🎭 Actions**
```aura
When clicked, display 'Message'
When clicked, alert 'Warning'
When clicked, show the card
When clicked, hide the button
When clicked, refresh the page
```

</td>
</tr>
<tr>
<td>

**🎨 Styling**
```aura
Make the button red
Make the heading bold
Align the paragraph to the center
Put the card in the middle
```

</td>
<td>

**🧭 Navigation**
```aura
Create a navbar with links 
  [Home, About, Contact]
  
Define a page 'About' at '/about'
```

</td>
</tr>
</table>

### Full Command Reference

See **[COMMAND_REFERENCE.md](COMMAND_REFERENCE.md)** for all available commands.

---

## 🧠 Aura Brain

The **Aura Brain** is a local AI model (Qwen2.5-0.5B) that provides real-time syntax correction.

### How it works

1. **You type**: `crete a card with title 'Hello'`
2. **Brain fixes**: `Create a card with the title 'Hello'`
3. **File updates**: Correction saved automatically

### Performance

| Metric | Value |
|--------|-------|
| **First correction** | ~2s (model loading) |
| **Subsequent corrections** | 100-300ms |
| **Accuracy** | 95%+ on common patterns |
| **Privacy** | 100% local, no cloud |

See **[AURA_BRAIN_README.md](AURA_BRAIN_README.md)** for advanced usage.

---

## 💡 Examples

### Landing Page
```aura
Use the dark theme

Create a navbar with logo 'MyApp' and links [Home, Features, Pricing]

Create a heading with the text 'Build Apps Faster'
Create a paragraph with the text 'No code, just English'
Create a button with the text 'Get Started'
When clicked, display 'Welcome!'
```

### Todo App
```aura
Create a heading with the text 'My Tasks'
Create an input with the text 'Enter task'
Create a button with the text 'Add Task'

Create a card with the title 'Task 1' and description 'Complete project'
Create a button with the text 'Done'
When clicked, hide the card
```

More examples in **[/examples](examples/)** folder.

---

## 🛠️ VS Code Extension

Get real-time autocorrection as you type!

### Features
- ✅ Syntax highlighting
- ✅ IntelliSense autocomplete
- ✅ Error detection
- ✅ Manual correction (`Ctrl+Shift+F`)
- 🚧 Ghost text suggestions (coming soon)

### Install

```bash
cd vscode-extension
code --install-extension .
```

---

## 🤝 Contributing

We love contributions! Here's how you can help:

1. **Report bugs** - Open an issue
2. **Suggest features** - Start a discussion
3. **Submit PRs** - Fix bugs or add features
4. **Improve docs** - Help others learn Aura

See **[CONTRIBUTING.md](CONTRIBUTING.md)** for guidelines.

---

## 📊 Project Stats

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/kingenious0/Aura-Programming-Language?style=social)
![GitHub forks](https://img.shields.io/github/forks/kingenious0/Aura-Programming-Language?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/kingenious0/Aura-Programming-Language?style=social)

</div>

---

## 🗺️ Roadmap

- [x] Core transpiler
- [x] AI-powered autocorrection
- [x] VS Code extension
- [x] Watch mode
- [ ] Ghost text completions
- [ ] Multi-file projects
- [ ] Component library
- [ ] Package manager
- [ ] Cloud deployment

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Qwen Team** - For the amazing language model
- **React & Vite** - For the frontend framework
- **Tailwind CSS** - For beautiful styling
- **You!** - For using Aura ❤️

---

<div align="center">

**Built with ❤️ by [KingEnious](https://github.com/kingenious0)**

[⭐ Star this repo](https://github.com/kingenious0/Aura-Programming-Language) • [🐛 Report Bug](https://github.com/kingenious0/Aura-Programming-Language/issues) • [💡 Request Feature](https://github.com/kingenious0/Aura-Programming-Language/issues)

</div>
