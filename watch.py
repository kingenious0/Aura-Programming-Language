#!/usr/bin/env python3
"""
Aura Watch Mode - Auto-transpile on file changes
Professional development mode for Aura
"""

import sys
import time
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class AuraWatcher(FileSystemEventHandler):
    """Watches for .aura file changes and auto-transpiles"""

    def __init__(self, target_file=None):
        self.target_file = target_file
        self.last_modified = {}
        self.debounce_seconds = 0.5  # Prevent multiple rapid triggers

    def on_modified(self, event):
        """Called when a file is modified"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Only process .aura files
        if file_path.suffix != '.aura':
            return

        # If target_file is specified, only watch that file
        if self.target_file and file_path.name != self.target_file:
            return

        # Debounce: ignore if modified too recently
        current_time = time.time()
        if file_path in self.last_modified:
            if current_time - self.last_modified[file_path] < self.debounce_seconds:
                return

        self.last_modified[file_path] = current_time

        # Transpile the file
        self.transpile(file_path)

    def transpile(self, file_path):
        """Run the transpiler on the given file"""
        print(f"\n[CHANGE] Detected in {file_path.name}")
        print(f"[BUILD] Transpiling at {time.strftime('%H:%M:%S')}...")

        try:
            # Run the transpiler
            result = subprocess.run(
                [sys.executable, 'transpiler/transpiler.py', str(file_path)],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                cwd=Path(__file__).parent
            )

            # Print output
            if result.stdout:
                print(result.stdout)

            if result.returncode == 0:
                print(f"[OK] Ready in {int(self.debounce_seconds * 1000)}ms")
            else:
                print(f"[ERROR] Transpilation failed!")
                if result.stderr:
                    print(result.stderr)

        except Exception as e:
            print(f"[ERROR] {e}")


def print_banner():
    """Print a professional banner"""
    print("\n" + "="*60)
    print("  AURA WATCH MODE")
    print("="*60)
    print("  Lightning-fast auto-transpilation for Aura")
    print("  Press Ctrl+C to stop")
    print("="*60 + "\n")


def main():
    """Main entry point"""
    # Parse command line arguments
    target_file = None
    watch_dir = Path.cwd()

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        arg_path = Path(arg)

        if arg_path.is_file() and arg_path.suffix == '.aura':
            target_file = arg_path.name
            watch_dir = arg_path.parent
            print(f"Watching: {target_file}")
        elif arg_path.is_dir():
            watch_dir = arg_path
            print(f"Watching all .aura files in: {watch_dir}")
        else:
            print(f"[ERROR] Invalid argument: {arg}")
            print("Usage: python watch.py [file.aura|directory]")
            sys.exit(1)
    else:
        print(f"Watching all .aura files in: {watch_dir}")

    print_banner()

    # Create event handler and observer
    event_handler = AuraWatcher(target_file)
    observer = Observer()
    observer.schedule(event_handler, str(watch_dir), recursive=False)

    # Start watching
    observer.start()
    print(f"Server started at {time.strftime('%H:%M:%S')}")
    print(f"Watching: {watch_dir.absolute()}")
    if target_file:
        print(f"Target: {target_file}")
    print("\nTip: Save your .aura file to trigger auto-transpilation!\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nStopping Aura watch mode...")
        observer.stop()
        observer.join()
        print("Goodbye!\n")


if __name__ == "__main__":
    main()
