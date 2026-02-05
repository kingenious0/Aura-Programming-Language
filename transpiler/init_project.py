"""
Aura Init - Project Scaffolding System
Creates a professional project structure with one command
"""

import os
import sys
import subprocess
from pathlib import Path
import shutil


class AuraProjectInitializer:
    """Initializes a new Aura project with professional structure"""

    def __init__(self, project_name: str = None):
        self.project_name = project_name or Path.cwd().name
        self.project_dir = Path.cwd()

    def init(self):
        """Initialize the Aura project"""
        print("\n" + "="*60)
        print("  🚀 AURA PROJECT INITIALIZER")
        print("="*60)
        print(f"  Project: {self.project_name}")
        print(f"  Location: {self.project_dir}")
        print("="*60 + "\n")

        # Step 1: Create folder structure
        self._create_folders()

        # Step 2: Create sample files
        self._create_sample_files()

        # Step 3: Setup Aura Brain
        self._setup_brain()

        # Step 4: Initialize React/Vite engine
        self._init_engine()

        # Step 5: Create config files
        self._create_config()

        print("\n" + "="*60)
        print("  ✅ PROJECT INITIALIZED SUCCESSFULLY!")
        print("="*60)
        print("\n📁 Project Structure:")
        print("  ├── pages/          # Your .aura files go here")
        print("  ├── assets/         # Images, fonts, etc.")
        print("  ├── .aura_engine/   # React/Vite (auto-managed)")
        print("  └── aura.config.py  # Project settings")
        print("\n🚀 Next Steps:")
        print("  1. cd pages/")
        print("  2. Create your first page: echo 'Create a heading...' > Home.aura")
        print("  3. Start dev server: aura dev")
        print("\n💡 Tip: Run 'aura dev' to start hot-reload development!")
        print("="*60 + "\n")

    def _create_folders(self):
        """Create the project folder structure"""
        print("[1/5] Creating project structure...")

        folders = [
            'pages',           # User's .aura files
            'assets',          # Images, fonts, etc.
            'assets/images',
            'assets/fonts',
            'components',      # Future: Reusable Aura components
        ]

        for folder in folders:
            folder_path = self.project_dir / folder
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ Created {folder}/")

        print()

    def _create_sample_files(self):
        """Create sample .aura files to get started"""
        print("[2/5] Creating sample files...")

        # Home page
        home_content = """# Welcome to Aura!
# This is your home page. Edit it to customize your app.

Use the dark theme

Create a heading with the text 'Welcome to {project_name}'
Create a paragraph with the text 'Build beautiful web apps using plain English!'

Create a button with the text 'Get Started'
When clicked, display 'Hello from Aura!'

# Try creating more pages in the pages/ folder!
# Each .aura file becomes a route automatically.
""".format(project_name=self.project_name)

        home_path = self.project_dir / 'pages' / 'Home.aura'
        home_path.write_text(home_content, encoding='utf-8')
        print(f"  ✓ Created pages/Home.aura")

        # About page
        about_content = """# About Page

Create a heading with the text 'About Us'
Create a paragraph with the text 'This app was built with Aura - the natural language programming language.'

Create a card with the title 'Why Aura?' and description 'Write code in plain English. No syntax to memorize!'
"""

        about_path = self.project_dir / 'pages' / 'About.aura'
        about_path.write_text(about_content, encoding='utf-8')
        print(f"  ✓ Created pages/About.aura")

        # README
        readme_content = f"""# {self.project_name}

An Aura project - build web apps using natural English!

## Getting Started

```bash
# Start the development server
aura dev

# Open http://localhost:5173 in your browser
```

## Project Structure

- `pages/` - Your .aura files (each file = one page)
- `assets/` - Images, fonts, and other static files
- `.aura_engine/` - Auto-managed React/Vite (don't edit)

## Adding Pages

Just create a new `.aura` file in the `pages/` folder:

```bash
echo "Create a heading with the text 'Products'" > pages/Products.aura
```

The page is instantly available at `/products`!

## Learn More

- [Aura Documentation](https://github.com/kingenious0/Aura-Programming-Language)
- [Command Reference](../COMMAND_REFERENCE.md)
"""

        readme_path = self.project_dir / 'README.md'
        readme_path.write_text(readme_content, encoding='utf-8')
        print(f"  ✓ Created README.md")

        # .gitignore
        gitignore_content = """# Aura
.aura_engine/
.aura_brain/
*.gguf

# Python
__pycache__/
*.py[cod]
*.so
.Python
venv/
env/

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
"""

        gitignore_path = self.project_dir / '.gitignore'
        gitignore_path.write_text(gitignore_content, encoding='utf-8')
        print(f"  ✓ Created .gitignore")

        print()

    def _setup_brain(self):
        """Setup the Aura Brain (download model if needed)"""
        print("[3/5] Setting up Aura Brain...")

        try:
            # Import setup module
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from transpiler.setup import ensure_aura_brain

            if ensure_aura_brain():
                print("  ✓ Aura Brain ready")
            else:
                print("  ⚠️ Aura Brain setup incomplete (will download on first use)")
        except Exception as e:
            print(f"  ⚠️ Could not setup Brain: {e}")
            print("  Brain will be downloaded on first transpile")

        print()

    def _init_engine(self):
        """Initialize the React/Vite engine"""
        print("[4/5] Initializing React/Vite engine...")

        engine_dir = self.project_dir / '.aura_engine'

        if engine_dir.exists():
            print("  ✓ Engine already exists")
            print()
            return

        print("  This may take a minute (one-time setup)...")

        try:
            # Create engine directory
            engine_dir.mkdir(exist_ok=True)

            # Initialize Vite project
            print("  → Creating Vite project...")
            result = subprocess.run(
                ['npm', 'create', 'vite@latest', '.', '--', '--template', 'react'],
                cwd=str(engine_dir),
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode != 0:
                print(f"  ⚠️ Vite init warning: {result.stderr}")

            # Install dependencies
            print("  → Installing dependencies...")
            subprocess.run(
                ['npm', 'install'],
                cwd=str(engine_dir),
                capture_output=True,
                timeout=300
            )

            # Install React Router
            print("  → Installing React Router...")
            subprocess.run(
                ['npm', 'install', 'react-router-dom'],
                cwd=str(engine_dir),
                capture_output=True,
                timeout=120
            )

            # Install Tailwind CSS
            print("  → Installing Tailwind CSS...")
            subprocess.run(
                ['npm', 'install', '-D', 'tailwindcss', 'postcss', 'autoprefixer'],
                cwd=str(engine_dir),
                capture_output=True,
                timeout=120
            )

            subprocess.run(
                ['npx', 'tailwindcss', 'init', '-p'],
                cwd=str(engine_dir),
                capture_output=True,
                timeout=60
            )

            print("  ✓ React/Vite engine initialized")

        except subprocess.TimeoutExpired:
            print(
                "  ⚠️ Setup timed out. You may need to run 'npm install' manually in .aura_engine/")
        except FileNotFoundError:
            print("  ⚠️ npm not found. Please install Node.js and npm")
            print("  Engine will be created on first build")
        except Exception as e:
            print(f"  ⚠️ Engine setup error: {e}")
            print("  Engine will be created on first build")

        print()

    def _create_config(self):
        """Create project configuration file"""
        print("[5/5] Creating configuration...")

        config_content = """# Aura Project Configuration

PROJECT_NAME = "{project_name}"
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
""".format(project_name=self.project_name)

        config_path = self.project_dir / 'aura.config.py'
        config_path.write_text(config_content, encoding='utf-8')
        print(f"  ✓ Created aura.config.py")

        print()


def main():
    """Entry point for aura init command"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Initialize a new Aura project')
    parser.add_argument('name', nargs='?', help='Project name (optional)')
    args = parser.parse_args()

    initializer = AuraProjectInitializer(args.name)
    initializer.init()


if __name__ == "__main__":
    main()
