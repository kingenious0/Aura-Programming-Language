"""
Runtime Engine - The Living Heart of Aura
Persistent execution loop with event processing and hot reload
"""

from typing import Optional, Any, List, Callable
import time
import threading

from runtime.state import StateManager
from runtime.events import EventQueue, EventScheduler, Event
from runtime.introspection import RuntimeInspector
from runtime.integrity import StateIntegrity, TransactionContext
from runtime.memory import ResourceTracker, ResourceLimits
from runtime.errors import AuraError, ErrorContext, safe_execute
from runtime.time_engine import TimeEngine
from runtime.recorder import ExecutionRecorder
from transpiler.ast_nodes import Program, ASTNode, FunctionDefNode, FunctionCallNode


class AuraRuntime:
    """
    Living runtime for Aura programs
    Maintains state, processes ev events, supports hot reload
    """

    def __init__(self, program: Optional[Program] = None, limits: Optional[ResourceLimits] = None):
        self.program = program
        self.state = StateManager()
        self.events = EventQueue()
        self.scheduler = EventScheduler(self.events)

        # Phase 2.6: Safety systems
        self.inspector = RuntimeInspector(self)
        self.integrity = StateIntegrity()
        self.resource_tracker = ResourceTracker(limits)

        # Phase 3.0: Observability & Time Travel
        self.time_engine = TimeEngine()
        self.recorder = ExecutionRecorder()
        self.observable_hooks: List[Callable] = []  # User callbacks

        self.running = False
        self.paused = False
        self._thread: Optional[threading.Thread] = None

        # Statistics
        self.start_time: Optional[float] = None
        self.iterations = 0

        # Error handling
        self.last_error: Optional[AuraError] = None
        self.safe_mode = False  # If True, errors don't stop runtime

    def load_program(self, program: Program) -> None:
        """Load or reload program AST"""
        self.program = program
        # Pre-register all functions
        self._register_functions()

    def _register_functions(self) -> None:
        """Pre-scan and register all function definitions"""
        if not self.program:
            return

        for stmt in self.program.statements:
            if isinstance(stmt, FunctionDefNode):
                self.state.register_function(stmt.name, stmt)

    def reload(self, new_program: Program) -> None:
        """
        Hot reload - update program without losing state
        Variables persist, only code changes
        """
        print("🔄 Hot reloading...")
        old_vars = self.state.get_all_vars()

        # Clear state but preserve variables
        self.state.clear()

        # Restore variables
        for name, value in old_vars.items():
            self.state.set_var(name, value)

        # Load new program
        self.load_program(new_program)
        print(f"✅ Reloaded ({len(old_vars)} vars preserved)")

    def start(self, blocking: bool = True) -> None:
        """
        Start the runtime
        blocking=True: Runs in current thread (blocks)
        blocking=False: Runs in background thread
        """
        if self.running:
            print("⚠️ Runtime already running")
            return

        self.running = True
        self.start_time = time.time()

        if blocking:
            self._run_loop()
        else:
            self._thread = threading.Thread(target=self._run_loop, daemon=True)
            self._thread.start()

    def _run_loop(self) -> None:
        """Main event loop - the heart of the living runtime"""
        print("💓 Aura Runtime Started")

        try:
            while self.running:
                if self.paused:
                    time.sleep(0.1)
                    continue

                # 1. Process scheduled events (timers)
                self.scheduler.tick()

                # 2. Process event queue
                self.events.process_all()

                # 3. Small sleep to prevent CPU spinning
                time.sleep(0.01)

                self.iterations += 1

        except KeyboardInterrupt:
            print("\n⚠️ Interrupted")
        finally:
            self.running = False
            print("💔 Aura Runtime Stopped")

    def stop(self) -> None:
        """Gracefully stop the runtime"""
        if not self.running:
            return

        self.running = False
        if self._thread:
            self._thread.join(timeout=2.0)

    def pause(self) -> None:
        """Pause execution"""
        self.paused = True

    def resume(self) -> None:
        """Resume execution"""
        self.paused = False

    def execute_once(self) -> None:
        """
        One-shot execution (compatibility with Phase 2)
        Executes program and returns immediately
        """
        if not self.program:
            raise RuntimeError("No program loaded")

        # Import executor
        from transpiler.core import AuraCore
        core = AuraCore()

        # Execute using existing core
        core.execute(self.program)

    def status(self) -> dict:
        """Get runtime status"""
        uptime = time.time() - self.start_time if self.start_time else 0

        return {
            'running': self.running,
            'paused': self.paused,
            'uptime': uptime,
            'iterations': self.iterations,
            'state': str(self.state),
            'events': str(self.events),
            'pending_events': self.events.pending_count()
        }

    def inspect_state(self) -> dict:
        """Get current state for debugging"""
        return {
            'variables': self.state.get_all_vars(),
            'functions': list(self.state.functions.keys()),
            'call_stack': self.state.call_stack.copy(),
            'event_handlers': list(self.events.handlers.keys())
        }

    def __repr__(self) -> str:
        status = "Running" if self.running else "Stopped"
        return f"<AuraRuntime: {status}, {self.state}>"
