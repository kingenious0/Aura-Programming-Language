"""
Aura CLI - Command Line Interface
The global entry point for all Aura commands
"""

import sys
from pathlib import Path

# Add project root to Python path for runtime module
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


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
║       A Human Interface to Computation                     ║
╚════════════════════════════════════════════════════════════╝

USAGE:
  aura <command> [options]

COMMANDS:
  🌐 UI Development:
    init              Initialize a new Aura UI project
    dev               Start hot-reload development server
    build <file>      Build project for production
  
  🧠 Core Logic (NEW):
    run <file>        Execute Aura logic file
    trace <file>      Execute with step-by-step output
    compile <file>    Compile to Python (.py)
  
  ℹ️  Info:
    --version, -v     Show version information
    --help, -h        Show this help message

EXAMPLES:
  # UI Development
  aura init
  aura dev
  
  # Core Logic (Pure Python execution)
  aura run logic.aura
  aura trace logic.aura
  aura compile logic.aura

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
        # Check if argument is a .aura logic file
        if len(sys.argv) >= 3 and sys.argv[2].endswith('.aura'):
            # Logic Watch Mode
            filepath = sys.argv[2]
            if not Path(filepath).exists():
                print(f"❌ Error: File not found: {filepath}")
                sys.exit(1)

            print(f"👁️  Aura Watch Mode: {filepath}")
            print("Press Ctrl+C to stop\n")

            from transpiler.logic_parser import LogicParser
            from runtime.engine import AuraRuntime
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler
            import time

            runtime = None
            parser = LogicParser()

            def load_and_start():
                nonlocal runtime
                try:
                    program = parser.parse_file(filepath)
                    if runtime and runtime.running:
                        runtime.reload(program)
                    else:
                        runtime = AuraRuntime(program)
                        runtime.load_program(program)
                        runtime.execute_once()
                except Exception as e:
                    print(f"❌ Error: {e}")

            class AuraFileHandler(FileSystemEventHandler):
                def on_modified(self, event):
                    if event.src_path.endswith(Path(filepath).name):
                        print(f"\n🔄 File changed, reloading...")
                        load_and_start()

            # Initial load
            load_and_start()

            # Watch for changes
            observer = Observer()
            observer.schedule(AuraFileHandler(), path=str(
                Path(filepath).parent), recursive=False)
            observer.start()

            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n⚠️  Stopping watch mode...")
                observer.stop()
            observer.join()
            sys.exit(0)

        # UI Dev Server (existing behavior)
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

    # Phase 3.0: Console command
    if command == 'console':
        print("🎮 Starting Aura Console...")
        from runtime import AuraRuntime
        from runtime.console import start_console

        runtime = AuraRuntime()
        start_console(runtime)
        sys.exit(0)

    # Phase 3.0: Inspector command
    if command == 'inspect':
        print("🔍 Starting Aura Inspector...")
        import webbrowser
        from pathlib import Path

        # Get inspector HTML path
        inspector_path = Path(__file__).parent.parent / \
            'inspector' / 'web' / 'index.html'

        # Start inspector server
        from inspector.server import InspectorServer
        from runtime import AuraRuntime

        runtime = AuraRuntime()
        server = InspectorServer(runtime, port=8080)
        server.start()

        # Open browser
        webbrowser.open(f'file:///{inspector_path}')

        print("✅ Inspector running on http://localhost:8080")
        print("   Dashboard opened in browser")
        print("   Press Ctrl+C to stop")

        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⚠️  Stopping inspector...")
            server.stop()

        sys.exit(0)

    # Phase 3.1: Visual UI command
    if command == 'ui':
        if len(sys.argv) < 3:
            print("❌ Usage: aura ui <file.aura>")
            sys.exit(1)

        filepath = sys.argv[2]

        if not Path(filepath).exists():
            print(f"❌ File not found: {filepath}")
            sys.exit(1)

        print("🎨 Starting Aura Visual Runtime...")
        from visual.dev_server import VisualDevServer

        try:
            server = VisualDevServer(filepath, port=3000)
            server.start()
        except ImportError as e:
            print(f"❌ {e}")
            print("   Install with: pip install websockets")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\n⚠️  Stopping visual server...")

        sys.exit(0)

    # Handle run command (CORE LOGIC or UI)
    if command == 'run':
        if len(sys.argv) < 3:
            print("❌ Error: 'run' command requires a file argument")
            print("Usage: aura run <filename.aura>")
            sys.exit(1)

        filepath = sys.argv[2]
        if not Path(filepath).exists():
            print(f"❌ Error: File not found: {filepath}")
            sys.exit(1)

        # Detect if file is logic-only or UI
        is_logic_file = _is_logic_file(filepath)

        if is_logic_file:
            # Core Logic Mode
            from transpiler.logic_parser import LogicParser
            from transpiler.core import AuraCore

            parser = LogicParser()
            core = AuraCore()

            try:
                print("🧠 Aura Core - Logic Execution")
                program = parser.parse_file(filepath)
                core.execute(program)
            except Exception as e:
                print(f"❌ Execution Error: {e}")
                import traceback
                traceback.print_exc()
                sys.exit(1)
        else:
            # UI Mode (existing behavior)
            from transpiler.transpiler import AuraTranspiler
            transpiler = AuraTranspiler()
            transpiler.run(filepath)

        sys.exit(0)

    # Handle trace command (Core Logic only)
    if command == 'trace':
        if len(sys.argv) < 3:
            print("❌ Error: 'trace' command requires a file argument")
            print("Usage: aura trace <filename.aura>")
            sys.exit(1)

        filepath = sys.argv[2]
        from transpiler.logic_parser import LogicParser
        from transpiler.core import AuraCore

        parser = LogicParser()
        core = AuraCore()

        try:
            print("🔍 Aura Trace Mode")
            program = parser.parse_file(filepath)
            core.trace(program)
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

        sys.exit(0)

    # Handle compile command (Core Logic only)
    if command == 'compile':
        if len(sys.argv) < 3:
            print("❌ Error: 'compile' command requires a file argument")
            print("Usage: aura compile <filename.aura>")
            sys.exit(1)

        filepath = sys.argv[2]
        output_file = Path(filepath).stem + '.py'

        from transpiler.logic_parser import LogicParser
        from transpiler.core import AuraCore

        parser = LogicParser()
        core = AuraCore()

        try:
            print(f"📦 Compiling {filepath} -> {output_file}")
            program = parser.parse_file(filepath)
            python_code = core.compile(program)

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(python_code)

            print(f"✅ Compilation successful: {output_file}")
        except Exception as e:
            print(f"❌ Compilation Error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

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


def _is_logic_file(filepath: str) -> bool:
    """Detect if a .aura file contains logic or UI commands"""
    logic_keywords = ['set ', 'if ', 'print ',
                      'repeat ', 'define function', 'call function']
    ui_keywords = ['Create a', 'Use the', 'When clicked', 'show ']

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    logic_count = sum(1 for kw in logic_keywords if kw in content)
    ui_count = sum(1 for kw in ui_keywords if kw in content)

    # If more logic keywords than UI, treat as logic file
    return logic_count > ui_count


if __name__ == "__main__":
    main()
