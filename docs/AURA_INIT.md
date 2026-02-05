# 🏗️ Aura Init - Project Scaffolding

## The "Birth" of Your Aura Project

`aura init` is the **architect** that transforms an empty folder into a professional development environment in seconds.

---

## 🎯 What It Does

### **One Command, Complete Setup**

```bash
aura init
```

This single command:
1. ✅ Creates professional folder structure
2. ✅ Generates sample `.aura` files
3. ✅ Downloads Aura Brain (AI model)
4. ✅ Initializes React/Vite engine
5. ✅ Creates configuration files
6. ✅ Sets up `.gitignore`

**Result**: A production-ready project in ~2 minutes!

---

## 🚀 Quick Start

### Create a New Project

```bash
# Create project folder
mkdir my-awesome-app
cd my-awesome-app

# Initialize Aura project
aura init

# Start developing!
aura dev
```

### Named Project

```bash
# Initialize with custom name
aura init "My Awesome App"
```

---

## 📁 Project Structure Created

```
my-awesome-app/
├── pages/                  # Your .aura files
│   ├── Home.aura          # Sample home page
│   └── About.aura         # Sample about page
│
├── assets/                 # Static files
│   ├── images/            # Your images
│   └── fonts/             # Custom fonts
│
├── components/             # Future: Reusable components
│
├── .aura_engine/          # Auto-managed (don't touch!)
│   ├── src/               # Generated React code
│   ├── node_modules/      # Dependencies
│   └── package.json       # NPM config
│
├── aura.config.py         # Project settings
├── README.md              # Project documentation
└── .gitignore             # Git ignore rules
```

---

## 🎨 Sample Files

### `pages/Home.aura`

```aura
# Welcome to Aura!
# This is your home page. Edit it to customize your app.

Use the dark theme

Create a heading with the text 'Welcome to My Awesome App'
Create a paragraph with the text 'Build beautiful web apps using plain English!'

Create a button with the text 'Get Started'
When clicked, display 'Hello from Aura!'
```

### `pages/About.aura`

```aura
# About Page

Create a heading with the text 'About Us'
Create a paragraph with the text 'This app was built with Aura.'

Create a card with the title 'Why Aura?' 
  and description 'Write code in plain English!'
```

---

## ⚙️ Configuration File

### `aura.config.py`

```python
# Aura Project Configuration

PROJECT_NAME = "my-awesome-app"
VERSION = "1.0.0"

# Paths
PAGES_DIR = "pages"
ASSETS_DIR = "assets"
ENGINE_DIR = ".aura_engine"

# Development
DEV_PORT = 5173
HOT_RELOAD = True
AUTO_CORRECT = True

# Build
OUTPUT_DIR = "dist"
MINIFY = True

# Aura Brain
BRAIN_ENABLED = True
BRAIN_MAX_TOKENS = 128
BRAIN_TEMPERATURE = 0.1
```

---

## 🔄 Workflow Comparison

### **React/Vite Way** (Manual, 30+ minutes)

```bash
# Create project
npm create vite@latest my-app -- --template react
cd my-app

# Install dependencies
npm install

# Install router
npm install react-router-dom

# Install Tailwind
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Configure Tailwind
# Edit tailwind.config.js
# Edit index.css

# Create folder structure
mkdir src/pages src/components src/hooks

# Create first page
touch src/pages/Home.jsx
# Write boilerplate...

# Configure routing
# Edit App.jsx
# Import components
# Add routes

# Start dev server
npm run dev
```

**Total time**: 30-60 minutes (for experienced devs!)

### **Aura Way** (Automatic, 2 minutes)

```bash
# Create and initialize
mkdir my-app
cd my-app
aura init

# Start developing
aura dev
```

**Total time**: 2 minutes (for anyone!)

---

## 🎯 The "Zero to Hero" Journey

### Minute 0: Empty Folder

```bash
mkdir my-startup
cd my-startup
ls
# (empty)
```

### Minute 1: Initialize

```bash
aura init
```

**Output:**
```
============================================================
  🚀 AURA PROJECT INITIALIZER
============================================================
  Project: my-startup
  Location: C:\Users\...\my-startup
============================================================

[1/5] Creating project structure...
  ✓ Created pages/
  ✓ Created assets/
  ✓ Created assets/images/
  ✓ Created assets/fonts/
  ✓ Created components/

[2/5] Creating sample files...
  ✓ Created pages/Home.aura
  ✓ Created pages/About.aura
  ✓ Created README.md
  ✓ Created .gitignore

[3/5] Setting up Aura Brain...
  ✓ Aura Brain ready

[4/5] Initializing React/Vite engine...
  This may take a minute (one-time setup)...
  → Creating Vite project...
  → Installing dependencies...
  → Installing React Router...
  → Installing Tailwind CSS...
  ✓ React/Vite engine initialized

[5/5] Creating configuration...
  ✓ Created aura.config.py

============================================================
  ✅ PROJECT INITIALIZED SUCCESSFULLY!
============================================================

📁 Project Structure:
  ├── pages/          # Your .aura files go here
  ├── assets/         # Images, fonts, etc.
  ├── .aura_engine/   # React/Vite (auto-managed)
  └── aura.config.py  # Project settings

🚀 Next Steps:
  1. cd pages/
  2. Create your first page: echo 'Create a heading...' > Home.aura
  3. Start dev server: aura dev

💡 Tip: Run 'aura dev' to start hot-reload development!
============================================================
```

### Minute 2: Start Developing

```bash
aura dev
```

Browser opens at `http://localhost:5173` → See your app running!

### Minute 3: Add Features

```bash
cd pages
echo "Create a heading with the text 'Products'" > Products.aura
```

Page instantly available at `/products`!

---

## 🧠 What Gets Installed

### 1. **Aura Brain** (AI Model)

- **Model**: Qwen2.5-0.5B
- **Size**: ~500MB
- **Location**: `.aura_brain/`
- **Purpose**: Autocorrect syntax errors

### 2. **React/Vite Engine**

- **React**: v18+
- **Vite**: v5+
- **React Router**: v6+
- **Tailwind CSS**: v3+
- **Location**: `.aura_engine/`

### 3. **NPM Packages**

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0"
  },
  "devDependencies": {
    "vite": "^5.0.0",
    "tailwindcss": "^3.3.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0"
  }
}
```

---

## 🎨 Customization

### Change Project Name

Edit `aura.config.py`:

```python
PROJECT_NAME = "My Custom Name"
```

### Change Dev Port

```python
DEV_PORT = 3000  # Instead of 5173
```

### Disable AI Autocorrection

```python
AUTO_CORRECT = False
```

---

## 🐛 Troubleshooting

### "npm not found"

**Problem**: Node.js not installed

**Solution**:
```bash
# Install Node.js from nodejs.org
# Then run:
aura init
```

### "Engine setup timed out"

**Problem**: Slow internet connection

**Solution**:
```bash
# Initialize without engine
aura init

# Install manually
cd .aura_engine
npm install
```

### "Aura Brain download failed"

**Problem**: Model download interrupted

**Solution**:
```bash
# Re-download model
python -m transpiler.setup
```

---

## 🚀 Best Practices

### 1. **One Project, One Folder**

```bash
# Good
mkdir my-app
cd my-app
aura init

# Bad (don't init in existing project)
cd existing-react-app
aura init  # ❌ Will conflict!
```

### 2. **Use Version Control**

```bash
# After init
git init
git add .
git commit -m "Initial Aura project"
```

### 3. **Keep .aura_engine Hidden**

Never edit files in `.aura_engine/` manually!
- Aura manages this folder automatically
- Your changes will be overwritten

### 4. **Organize by Feature**

```
pages/
  ├── Home.aura
  ├── About.aura
  ├── Products.aura
  ├── Contact.aura
  └── Blog.aura
```

---

## 📊 Comparison Table

| Feature | React Init | Aura Init |
|---------|-----------|-----------|
| **Time** | 30-60 min | 2 min |
| **Steps** | 15+ manual | 1 command |
| **Knowledge required** | React, npm, config | None |
| **Folder structure** | Manual | Automatic |
| **Sample code** | None | Included |
| **AI autocorrect** | ❌ | ✅ |
| **Hot reload** | Manual setup | Automatic |

---

## 🎯 When to Use

### Use `aura init` when:
- ✅ Starting a new project from scratch
- ✅ Want professional structure automatically
- ✅ Need sample files to learn from
- ✅ Want AI-powered development

### Don't use `aura init` when:
- ❌ Already have an existing Aura project
- ❌ Just want to test a single `.aura` file (use `aura run` instead)

---

## 🔄 Migration from Legacy

### Old Way (No Structure)

```
my-project/
  ├── Home.aura
  ├── About.aura
  └── .aura_engine/
```

### New Way (Professional)

```bash
# Create new project
mkdir my-project-v2
cd my-project-v2
aura init

# Move old files
mv ../my-project/*.aura pages/

# Done!
aura dev
```

---

## 🎉 What's Next

After `aura init`, you can:

1. **Start developing**: `aura dev`
2. **Add pages**: Create `.aura` files in `pages/`
3. **Add assets**: Put images in `assets/images/`
4. **Customize**: Edit `aura.config.py`
5. **Deploy**: Build with `aura build` (coming soon!)

---

**`aura init` is the foundation of world-class Aura development!** 🏗️✨
