"""
Aura Dev Server - Professional development environment with hot reload
Watches all .aura files and automatically transpiles on changes
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

try:
    from .transpiler import AuraTranspiler
except ImportError:
    from transpiler import AuraTranspiler


class AuraDevServer(FileSystemEventHandler):
    """Watches .aura files and triggers hot reload"""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.transpiler = AuraTranspiler()
        self.vite_process = None
        self.last_build_time = 0
        self.debounce_delay = 0.5  # 500ms debounce

        print("\n" + "="*60)
        print("  🚀 AURA DEV SERVER")
        print("="*60)
        print(f"  Watching: {project_dir}")
        print("  Press Ctrl+C to stop")
        print("="*60 + "\n")

    def start(self):
        """Start the dev server"""
        # Initial build of all pages
        self._build_all_pages()

        # Start Vite dev server
        self._start_vite()

        # Start file watcher
        observer = Observer()
        observer.schedule(self, str(self.project_dir), recursive=False)
        observer.start()

        print(f"\n✓ Dev server running at http://localhost:5173")
        print(f"✓ Watching for .aura file changes...\n")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n[Aura Dev] Shutting down...")
            observer.stop()
            self._stop_vite()

        observer.join()

    def on_created(self, event):
        """Handle new .aura file creation"""
        if event.is_directory or not event.src_path.endswith('.aura'):
            return

        file_path = Path(event.src_path)
        print(f"\n[NEW FILE] {file_path.name}")
        self._rebuild_project()

    def on_modified(self, event):
        """Handle .aura file modification"""
        if event.is_directory or not event.src_path.endswith('.aura'):
            return

        # Debounce rapid saves
        current_time = time.time()
        if current_time - self.last_build_time < self.debounce_delay:
            return

        file_path = Path(event.src_path)
        print(f"\n[CHANGE] {file_path.name}")
        self._rebuild_project()
        self.last_build_time = current_time

    def on_deleted(self, event):
        """Handle .aura file deletion"""
        if event.is_directory or not event.src_path.endswith('.aura'):
            return

        file_path = Path(event.src_path)
        print(f"\n[DELETED] {file_path.name}")
        self._rebuild_project()

    def _build_all_pages(self):
        """Build all .aura files in the project"""
        print("[BUILD] Scanning for .aura files...")

        aura_files = list(self.project_dir.glob('*.aura'))

        if not aura_files:
            print("  ⚠️ No .aura files found in current directory")
            return

        print(f"  Found {len(aura_files)} page(s)")

        for aura_file in aura_files:
            print(f"  - {aura_file.stem}")

        # Build the project (transpiler handles all files)
        try:
            # Build triggers full scan
            self.transpiler.build(str(aura_files[0]))
            print("\n✓ Build complete")
        except Exception as e:
            print(f"\n✗ Build failed: {e}")

    def _rebuild_project(self):
        """Rebuild the entire project"""
        print("  [REBUILD] Transpiling...")

        try:
            # Find any .aura file to trigger full rebuild
            aura_files = list(self.project_dir.glob('*.aura'))
            if aura_files:
                self.transpiler.build(str(aura_files[0]))
                print("  ✓ Hot reload triggered")
        except Exception as e:
            print(f"  ✗ Error: {e}")

    def _start_vite(self):
        """Start the Vite dev server"""
        engine_dir = self.project_dir / '.aura_engine'

        if not engine_dir.exists():
            print("  ⚠️ .aura_engine not found. Run a build first.")
            return

        print("\n[VITE] Starting dev server...")
        print("  Opening in new window...")

        try:
            if sys.platform == 'win32':
                # Windows: Open in new command prompt
                self.vite_process = subprocess.Popen(
                    'start cmd /k "npm run dev"',
                    cwd=str(engine_dir),
                    shell=True
                )
            else:
                # Linux/Mac: Run in background
                self.vite_process = subprocess.Popen(
                    ['npm', 'run', 'dev'],
                    cwd=str(engine_dir),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

            # Give Vite time to start
            time.sleep(2)
            print("  ✓ Vite dev server started")

        except Exception as e:
            print(f"  ⚠️ Could not auto-start Vite: {e}")
            print(f"  Please run manually: cd .aura_engine && npm run dev")

    def _stop_vite(self):
        """Stop the Vite dev server"""
        if self.vite_process:
            print("[VITE] Stopping dev server...")
            self.vite_process.terminate()
            try:
                self.vite_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.vite_process.kill()


def main():
    """Entry point for aura dev command"""
    project_dir = Path.cwd()

    # Check if we're in a valid Aura project
    aura_files = list(project_dir.glob('*.aura'))
    if not aura_files:
        print("❌ No .aura files found in current directory")
        print("   Create a .aura file to get started!")
        sys.exit(1)

    # Start the dev server
    dev_server = AuraDevServer(project_dir)
    dev_server.start()


if __name__ == "__main__":
    main()
