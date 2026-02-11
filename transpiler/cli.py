"""
Aura CLI - Command Line Interface
The global entry point for all Aura commands
"""

import sys
from pathlib import Path


def print_version():
    """Print Aura version"""
    print("Aura Programming Language v1.0.0")
    print("Natural language programming - write code in plain English")
    print("https://github.com/kingenious0/Aura-Programming-Language")


def print_help():
    """Print help message"""
    print("""
╔════════════════════════════════════════════════════════════╗
║              AURA PROGRAMMING LANGUAGE                     ║
║          Write code in plain English!                      ║
╚════════════════════════════════════════════════════════════╝

USAGE:
  aura <command> [options]

COMMANDS:
  init              Initialize a new Aura project
  dev               Start hot-reload development server
  run <file>        Build and run a single .aura file
  build <file>      Build project without launching server
  
  --version, -v     Show version information
  --help, -h        Show this help message

EXAMPLES:
  # Create a new project
  aura init
  
  # Start development server (watches all .aura files)
  aura dev
  
  # Run a single file
  aura run Home.aura
  
  # Build for production
  aura build Home.aura

GETTING STARTED:
  1. Create a new project:
     mkdir my-app && cd my-app
     aura init
  
  2. Start developing:
     aura dev
  
  3. Open http://localhost:5173 in your browser

DOCUMENTATION:
  https://github.com/kingenious0/Aura-Programming-Language

SUPPORT:
  Report issues: https://github.com/kingenious0/Aura-Programming-Language/issues
    """)


def main():
    """Main CLI entry point"""

    # Handle no arguments
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    command = sys.argv[1].lower()

    # Handle version flag
    if command in ['--version', '-v', 'version']:
        print_version()
        sys.exit(0)

    # Handle help flag
    if command in ['--help', '-h', 'help']:
        print_help()
        sys.exit(0)

    # Handle init command
    if command == 'init':
        from transpiler.init_project import AuraProjectInitializer
        project_name = sys.argv[2] if len(sys.argv) > 2 else None
        initializer = AuraProjectInitializer(project_name)
        initializer.init()
        sys.exit(0)

    # Handle dev command
    if command == 'dev':
        from transpiler.dev_server import AuraDevServer

        # Check if we're in a project with pages/ folder
        project_dir = Path.cwd()
        pages_dir = project_dir / 'pages'

        if pages_dir.exists():
            # Watch the pages/ folder
            dev_server = AuraDevServer(pages_dir)
        else:
            # Watch current directory (legacy mode)
            dev_server = AuraDevServer(project_dir)

        dev_server.start()
        sys.exit(0)

    # Handle run command
    if command == 'run':
        if len(sys.argv) < 3:
            print("❌ Error: 'run' command requires a file argument")
            print("Usage: aura run <filename.aura>")
            sys.exit(1)

        from transpiler.transpiler import AuraTranspiler
        transpiler = AuraTranspiler()
        transpiler.run(sys.argv[2])
        sys.exit(0)

    # Handle build command
    if command == 'build':
        # Case 1: Build specific file
        if len(sys.argv) >= 3:
            from transpiler.transpiler import AuraTranspiler
            transpiler = AuraTranspiler()
            transpiler.build(sys.argv[2])
            sys.exit(0)

        # Case 2: Build project (auto-detect)
        project_dir = Path.cwd()
        pages_dir = project_dir / 'pages'

        # Also check current directory for legacy projects
        aura_files = []
        if pages_dir.exists():
            aura_files = list(pages_dir.glob('*.aura'))
        else:
            aura_files = list(project_dir.glob('*.aura'))

        if not aura_files:
            print("❌ No .aura files found in pages/ or current directory")
            print("Usage: aura build <filename.aura>")
            sys.exit(1)

        print(f"📦 Building project: {project_dir.name}")

        # Check if engine exists, if not initialize it
        engine_dir = project_dir / '.aura_engine'
        if not engine_dir.exists():
            print("⚠️ Engine not found. Initializing...")
            try:
                from .init_project import AuraProjectInitializer
            except ImportError:
                from init_project import AuraProjectInitializer

            initializer = AuraProjectInitializer(project_dir.name)
            initializer._init_engine()

        from transpiler.transpiler import AuraTranspiler
        transpiler = AuraTranspiler()

        # Building any file triggers the project scanner
        # But let's be explicit and ensure the first file triggers the process
        print(f"  Found {len(aura_files)} pages. Starting build...")
        transpiler.build(str(aura_files[0]))
        print("✓ Project build complete")
        sys.exit(0)

    # Handle direct .aura file (legacy support)
    if command.endswith('.aura'):
        from transpiler.transpiler import AuraTranspiler
        transpiler = AuraTranspiler()
        transpiler.run(command)
        sys.exit(0)

    # Unknown command
    print(f"❌ Unknown command: {command}")
    print("Run 'aura --help' to see available commands")
    sys.exit(1)


if __name__ == "__main__":
    main()
