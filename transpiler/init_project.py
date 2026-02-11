"""
Aura Init - Project Scaffolding System
Creates a professional project structure with one command
"""

import os
import sys
import subprocess
import time
import requests
import zipfile
import io
from pathlib import Path
from tqdm import tqdm


class AuraProjectInitializer:
    """Initializes a new Aura project with professional structure"""

    # URL for the pre-built engine (You must create this release on GitHub!)
    ENGINE_ZIP_URL = "https://github.com/kingenious0/Aura-Programming-Language/releases/download/v1.0.0/aura_engine_v1.zip"

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

        steps = [
            ("Creating structure", self._create_folders),
            ("Creating samples", self._create_sample_files),
            ("Setting up Brain", self._setup_brain),
            ("Initializing Engine", self._init_engine),
            ("Creating config", self._create_config)
        ]

        with tqdm(total=len(steps), desc="🚀 Setting up Aura", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} steps") as pbar:
            for desc, step_func in steps:
                pbar.set_description(f"🚀 {desc}")
                step_func(pbar)
                pbar.update(1)

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

    def _create_folders(self, pbar):
        """Create the project folder structure"""
        folders = [
            'pages',
            'assets',
            'assets/images',
            'assets/fonts',
            'components',
        ]

        for folder in folders:
            folder_path = self.project_dir / folder
            folder_path.mkdir(parents=True, exist_ok=True)
            # tqdm.write(f"  ✓ Created {folder}/")

    def _create_sample_files(self, pbar):
        """Create sample .aura files to get started"""

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

        # About page
        about_content = """# About Page

Create a heading with the text 'About Us'
Create a paragraph with the text 'This app was built with Aura - the natural language programming language.'

Create a card with the title 'Why Aura?' and description 'Write code in plain English. No syntax to memorize!'
"""
        about_path = self.project_dir / 'pages' / 'About.aura'
        about_path.write_text(about_content, encoding='utf-8')

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
.venv/

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

    def _setup_brain(self, pbar):
        """Setup the Aura Brain (download model if needed)"""
        try:
            # Import setup module
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from transpiler.setup import ensure_aura_brain

            # We assume ensure_aura_brain might print things, which interferes with tqdm.
            # Ideally we'd wrap it or capture output. For now, let it run.
            # If it downloads, it takes time.
            if ensure_aura_brain():
                pass
            else:
                tqdm.write(
                    "  ⚠️ Aura Brain setup incomplete (will download on first use)")
        except Exception as e:
            tqdm.write(f"  ⚠️ Could not setup Brain: {e}")
            tqdm.write("  Brain will be downloaded on first transpile")

    def _download_prebuilt_engine(self, engine_dir):
        """Downloads and extracts the pre-built engine to avoid npm install"""
        try:
            # tqdm.write(f"   ⬇️ Downloading pre-built engine from GitHub...")
            response = requests.get(
                self.ENGINE_ZIP_URL, stream=True, timeout=30)

            if response.status_code != 200:
                tqdm.write(
                    f"   ⚠️ Failed to download pre-built engine. Status: {response.status_code}")
                return False

            total_size = int(response.headers.get('content-length', 0))

            # Download with progress
            block_size = 1024  # 1 Kibibyte
            buffer = io.BytesIO()

            with tqdm(total=total_size, unit='iB', unit_scale=True, desc="   ⬇️ Downloading Engine", leave=False) as dl_pbar:
                for data in response.iter_content(block_size):
                    dl_pbar.update(len(data))
                    buffer.write(data)

            # Extract
            tqdm.write("   📦 Extracting engine...")
            with zipfile.ZipFile(buffer) as zip_ref:
                # Zip should contain .aura_engine folder
                zip_ref.extractall(self.project_dir)

            # verify
            if (engine_dir / 'node_modules').exists():
                tqdm.write("   ✓ Engine installed (Skipped setup!)")
                return True

        except Exception as e:
            tqdm.write(f"   ⚠️ Pre-build download failed: {e}")
            tqdm.write("   ⚠️ Falling back to manual build...")

        return False

    def _init_engine(self, pbar=None):
        """Initialize the React/Vite engine"""
        engine_dir = self.project_dir / '.aura_engine'

        if engine_dir.exists():
            # basic check if package.json exists
            if (engine_dir / 'package.json').exists():
                return

        # 1. Try "Fast Path" (Download pre-built)
        if self._download_prebuilt_engine(engine_dir):
            return

        # 2. Slow Path (Manual Creation)
        try:
            # Create engine directory
            engine_dir.mkdir(exist_ok=True)

            # Windows requires shell=True for npm
            use_shell = sys.platform == 'win32'

            commands = [
                (['npm', 'create', 'vite@latest', '.', '--',
                 '--template', 'react'], "Creating Vite app"),
                (['npm', 'install'], "Installing core dependencies"),
                (['npm', 'install', 'react-router-dom'], "Installing Router"),
                (['npm', 'install', '-D', 'tailwindcss', 'postcss',
                 'autoprefixer'], "Installing Tailwind"),
                (['npx', 'tailwindcss', 'init', '-p'], "Configuring Tailwind")
            ]

            # Nested progress bar for engine steps
            # position=1 leaves the main bar at top
            with tqdm(total=len(commands), desc="   ⚙️ Engine Setup", leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as sub_pbar:
                for cmd, desc in commands:
                    sub_pbar.set_description(f"   ⚙️ {desc}")

                    # Increased timeouts significantly
                    timeout_val = 600 if 'install' in cmd else 120

                    result = subprocess.run(
                        cmd,
                        cwd=str(engine_dir),
                        capture_output=True,
                        text=True,
                        timeout=timeout_val,
                        shell=use_shell
                    )

                    if result.returncode != 0:
                        tqdm.write(
                            f"  ⚠️ Warning during '{desc}': {result.stderr[:200]}...")

                    sub_pbar.update(1)

        except subprocess.TimeoutExpired:
            tqdm.write(
                "  ⚠️ Setup timed out. You may need to run 'npm install' manually in .aura_engine/")
        except FileNotFoundError:
            tqdm.write("  ⚠️ npm not found. Please install Node.js and npm")
            tqdm.write("  Engine will be created on first build")
        except Exception as e:
            tqdm.write(f"  ⚠️ Engine setup error: {e}")
            tqdm.write("  Engine will be created on first build")

    def _create_config(self, pbar):
        """Create project configuration file"""
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
