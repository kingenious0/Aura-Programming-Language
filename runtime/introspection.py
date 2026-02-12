"""
Runtime Introspection
Expose internal runtime state for debugging and monitoring
"""

from typing import Dict, List, Any, Optional
from datetime import datetime


class RuntimeInspector:
    """Provides introspection capabilities for Aura runtime"""

    def __init__(self, runtime):
        self.runtime = runtime

    def dump_vars(self, scope: str = "all") -> Dict[str, Any]:
        """
        Dump all variables
        scope: 'all', 'global', 'local'
        """
        if scope == "global":
            return dict(self.runtime.state.global_scope.variables)
        elif scope == "local":
            return dict(self.runtime.state.current_scope.variables)
        else:  # all
            return self.runtime.state.get_all_vars()

    def dump_functions(self) -> List[str]:
        """List all defined functions"""
        return list(self.runtime.state.functions.keys())

    def dump_events(self) -> Dict[str, Any]:
        """Dump event queue status"""
        return {
            'pending': self.runtime.events.pending_count(),
            'processed': self.runtime.events.processed_count,
            'handlers': {
                event: len(handlers)
                for event, handlers in self.runtime.events.handlers.items()
            }
        }

    def dump_stack(self) -> List[str]:
        """Get current call stack"""
        return self.runtime.state.call_stack.copy()

    def dump_memory(self) -> Dict[str, Any]:
        """Get memory usage statistics"""
        import sys

        var_count = len(self.runtime.state.get_all_vars())
        func_count = len(self.runtime.state.functions)
        event_count = self.runtime.events.pending_count()

        # Approximate memory usage
        vars_size = sum(
            sys.getsizeof(k) + sys.getsizeof(v)
            for k, v in self.runtime.state.get_all_vars().items()
        )

        return {
            'variables': {
                'count': var_count,
                'bytes': vars_size
            },
            'functions': {
                'count': func_count
            },
            'events': {
                'pending': event_count
            },
            'call_stack_depth': len(self.runtime.state.call_stack)
        }

    def dump_status(self) -> Dict[str, Any]:
        """Get runtime status"""
        return self.runtime.status()

    def dump_full(self) -> Dict[str, Any]:
        """Complete runtime dump"""
        return {
            'timestamp': datetime.now().isoformat(),
            'status': self.dump_status(),
            'variables': self.dump_vars(),
            'functions': self.dump_functions(),
            'events': self.dump_events(),
            'stack': self.dump_stack(),
            'memory': self.dump_memory()
        }

    def format_vars(self) -> str:
        """Format variables for display"""
        vars_dict = self.dump_vars()
        if not vars_dict:
            return "No variables defined"

        lines = ["Variables:"]
        for name, value in vars_dict.items():
            value_str = repr(value)
            if len(value_str) > 50:
                value_str = value_str[:47] + "..."
            lines.append(f"  {name} = {value_str}")

        return "\n".join(lines)

    def format_functions(self) -> str:
        """Format functions for display"""
        funcs = self.dump_functions()
        if not funcs:
            return "No functions defined"

        return "Functions:\n  " + "\n  ".join(funcs)

    def format_events(self) -> str:
        """Format event queue for display"""
        events = self.dump_events()
        lines = [
            f"Event Queue:",
            f"  Pending: {events['pending']}",
            f"  Processed: {events['processed']}"
        ]

        if events['handlers']:
            lines.append("  Handlers:")
            for event, count in events['handlers'].items():
                lines.append(f"    {event}: {count}")

        return "\n".join(lines)

    def format_memory(self) -> str:
        """Format memory stats for display"""
        mem = self.dump_memory()
        lines = [
            "Memory:",
            f"  Variables: {mem['variables']['count']} ({mem['variables']['bytes']} bytes)",
            f"  Functions: {mem['functions']['count']}",
            f"  Events: {mem['events']['pending']} pending",
            f"  Stack depth: {mem['call_stack_depth']}"
        ]
        return "\n".join(lines)

    def format_full(self) -> str:
        """Complete formatted dump"""
        dump = self.dump_full()

        sections = [
            f"=== Aura Runtime Inspection ===",
            f"Timestamp: {dump['timestamp']}",
            f"Status: {'Running' if dump['status']['running'] else 'Stopped'}",
            "",
            self.format_vars(),
            "",
            self.format_functions(),
            "",
            self.format_events(),
            "",
            self.format_memory()
        ]

        return "\n".join(sections)
