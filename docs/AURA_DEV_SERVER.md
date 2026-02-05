# 🚀 Aura Dev Server

## The Professional Development Experience

The `aura dev` command transforms Aura into a **world-class development environment** with hot-reload, automatic page discovery, and instant feedback.

---

## 🎯 What Makes It Special

### **React/Vite Way** (Manual)
```bash
# Create component
touch About.jsx

# Import React
import React from 'react'

# Export component
export default function About() { ... }

# Add to router
import About from './About'
<Route path="/about" element={<About />} />

# Refresh browser
```

### **Aura Way** (Automatic)
```bash
# Create file
touch About.aura

# That's it! Page is live at /about
```

---

## 🚀 Quick Start

### Start the Dev Server

```bash
aura dev
```

That's it! The server will:
1. ✅ Scan all `.aura` files in your project
2. ✅ Build them into React components
3. ✅ Start Vite dev server at `http://localhost:5173`
4. ✅ Watch for changes and hot-reload instantly

---

## ✨ Features

### 1. **Automatic Page Discovery**

Create a new file:
```bash
# Create Store.aura
Create a heading with the text 'Our Store'
Create a paragraph with the text 'Browse our products'
```

**Result**: Page instantly available at `/store`

No imports, no routing config, no manual setup!

### 2. **Hot Reload**

Edit any `.aura` file:
```aura
Create a button with the text 'Click Me'
```

Save (`Ctrl+S`) → Browser updates in **~500ms**

No page refresh, no lost state!

### 3. **Multi-Page Watching**

The dev server watches **ALL** `.aura` files simultaneously:

```
my-project/
  ├── Home.aura       ← Watching
  ├── About.aura      ← Watching
  ├── Contact.aura    ← Watching
  └── Store.aura      ← Watching
```

Change any file → Instant rebuild

### 4. **AI-Powered Autocorrection**

Type with typos:
```aura
crete a butn with text 'Submit'
```

Save → Aura Brain fixes it:
```aura
Create a button with the text 'Submit'
```

And hot-reloads the corrected version!

### 5. **Debounced Rebuilds**

Rapid saves? No problem!
- Saves within 500ms are batched
- Only one rebuild triggered
- No wasted CPU cycles

---

## 📊 Performance

| Action | Time | Notes |
|--------|------|-------|
| **Initial build** | ~2-3s | One-time startup |
| **File change detection** | <50ms | Watchdog is instant |
| **Transpile + Brain** | ~200-500ms | AI correction included |
| **Vite hot-reload** | ~100-200ms | Browser update |
| **Total (save → browser)** | **~500-800ms** | Feels instant! |

---

## 🎮 Commands

### `aura dev`
Start the hot-reload development server

```bash
aura dev
```

**Output:**
```
============================================================
  🚀 AURA DEV SERVER
============================================================
  Watching: C:\Users\...\MyProject
  Press Ctrl+C to stop
============================================================

[BUILD] Scanning for .aura files...
  Found 3 page(s)
  - Home
  - About
  - Contact

✓ Build complete

[VITE] Starting dev server...

✓ Dev server running at http://localhost:5173
✓ Watching for .aura file changes...
```

### `aura run <file>`
Build and launch a single file (old way)

```bash
aura run Home.aura
```

### `aura build <file>`
Build without launching server

```bash
aura build Home.aura
```

---

## 🔥 Real-World Workflow

### Day 1: Start a New Project

```bash
# Create project folder
mkdir my-app
cd my-app

# Create first page
echo "Create a heading with the text 'Welcome'" > Home.aura

# Start dev server
aura dev
```

Browser opens at `http://localhost:5173` → See your app!

### Day 2: Add More Pages

```bash
# Create About page (while dev server is running)
echo "Create a heading with the text 'About Us'" > About.aura
```

**Instantly** available at `/about` (no restart needed!)

### Day 3: Iterate Fast

1. Open `Home.aura` in VS Code
2. Type: `crete a butn with text 'Learn More'`
3. Save (`Ctrl+S`)
4. **500ms later**: Browser shows corrected button

---

## 🧠 How It Works

### Architecture

```
┌─────────────────────────────────────────────────┐
│  Your .aura Files                               │
│  ├── Home.aura                                  │
│  ├── About.aura                                 │
│  └── Contact.aura                               │
└────────────┬────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────┐
│  Watchdog (File System Monitor)                 │
│  • Detects file changes                         │
│  • Triggers rebuild on save                     │
│  • Debounces rapid saves                        │
└────────────┬────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────┐
│  Aura Brain + Transpiler                        │
│  • AI fixes syntax errors                       │
│  • Generates React components                   │
│  • Updates .aura_engine/                        │
└────────────┬────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────┐
│  Vite Dev Server                                │
│  • Detects React file changes                   │
│  • Hot-reloads browser                          │
│  • Preserves component state                    │
└─────────────────────────────────────────────────┘
```

### Event Flow

1. **You save** `Home.aura`
2. **Watchdog** detects change (< 50ms)
3. **Aura Brain** fixes syntax (~200ms)
4. **Transpiler** generates React (~300ms)
5. **Vite** detects React change (~100ms)
6. **Browser** hot-reloads (~100ms)

**Total**: ~750ms from save to browser update!

---

## 🎨 VS Code Integration

For the best experience, use with the Aura VS Code extension:

```bash
cd vscode-extension
code --install-extension .
```

**Features:**
- Syntax highlighting
- Error detection
- Manual correction (`Ctrl+Shift+F`)
- Works seamlessly with `aura dev`

---

## 🐛 Troubleshooting

### Dev server won't start

**Problem**: `No .aura files found`

**Solution**: Create at least one `.aura` file in the current directory

```bash
echo "Create a heading with the text 'Hello'" > Home.aura
aura dev
```

### Vite fails to start

**Problem**: `Failed to start Vite`

**Solution**: Install Node.js and npm

```bash
node --version  # Should be 16+
npm --version
```

### Changes not hot-reloading

**Problem**: Browser not updating

**Solution**: 
1. Check terminal for errors
2. Ensure Vite is running (check `http://localhost:5173`)
3. Hard refresh browser (`Ctrl+Shift+R`)

### Port 5173 already in use

**Problem**: `EADDRINUSE: address already in use`

**Solution**: Kill the existing process

```bash
# Windows
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5173 | xargs kill -9
```

---

## 🚀 Advanced Usage

### Custom Port

Edit `.aura_engine/vite.config.js`:

```javascript
export default defineConfig({
  server: {
    port: 3000  // Change from 5173
  }
})
```

### Multiple Projects

Run separate dev servers in different terminals:

```bash
# Terminal 1
cd project-a
aura dev

# Terminal 2
cd project-b
aura dev  # Will use port 5174 automatically
```

### Production Build

```bash
# Build for production
cd .aura_engine
npm run build

# Preview production build
npm run preview
```

---

## 📈 Comparison

| Feature | React + Vite | Aura Dev |
|---------|-------------|----------|
| **Setup time** | 5-10 min | 10 seconds |
| **New page** | Create file, import, route | Create file |
| **Hot reload** | ✅ | ✅ |
| **Syntax errors** | Manual fix | AI auto-fixes |
| **Learning curve** | Steep | Flat |
| **Code verbosity** | High | Minimal |

---

## 🎯 Best Practices

### 1. **Keep Dev Server Running**
Start `aura dev` once, leave it running all day

### 2. **Use Meaningful Filenames**
```
Home.aura     → /home
About.aura    → /about
Contact.aura  → /contact
```

### 3. **Let AI Fix Typos**
Don't stress about perfect syntax—Aura Brain has your back

### 4. **Organize by Feature**
```
my-app/
  ├── Home.aura
  ├── About.aura
  ├── Products.aura
  └── Contact.aura
```

### 5. **Use Version Control**
```bash
git add *.aura
git commit -m "Add new pages"
```

---

## 🎉 What's Next

- [ ] **Multi-directory support** - Organize pages in folders
- [ ] **Component library** - Reusable Aura components
- [ ] **Live collaboration** - Multiple devs, one project
- [ ] **Cloud deployment** - One-click deploy to Vercel/Netlify
- [ ] **TypeScript support** - Type-safe Aura

---

## 💡 Tips & Tricks

### Rapid Prototyping

```bash
# Create 5 pages in 10 seconds
echo "Create a heading with the text 'Home'" > Home.aura
echo "Create a heading with the text 'About'" > About.aura
echo "Create a heading with the text 'Services'" > Services.aura
echo "Create a heading with the text 'Blog'" > Blog.aura
echo "Create a heading with the text 'Contact'" > Contact.aura

# Start dev server
aura dev

# All 5 pages are live!
```

### Quick Navbar Test

```aura
Create a navbar with links [Home, About, Services, Blog, Contact]
```

Save → Instant navigation between all pages!

---

**The `aura dev` command makes Aura feel like magic.** 🪄

No configuration, no boilerplate, just pure productivity! 🚀
