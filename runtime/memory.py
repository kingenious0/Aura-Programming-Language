"""
Memory Management & Resource Limits
Prevents runaway execution and resource exhaustion
"""

from dataclasses import dataclass
from typing import Optional
import time


@dataclass
class ResourceLimits:
    """Resource limits for Aura runtime"""
    max_variables: int = 1000          # Maximum number of variables
    max_functions: int = 100           # Maximum number of functions
    max_recursion_depth: int = 100     # Maximum recursion depth
    max_events: int = 500              # Maximum queued events
    max_execution_time: float = 60.0   # Maximum execution time (seconds)
    max_iterations: int = 1_000_000    # Maximum loop iterations

    def __repr__(self) -> str:
        return (f"<ResourceLimits: vars={self.max_variables}, "
                f"funcs={self.max_functions}, "
                f"recursion={self.max_recursion_depth}>")


class ResourceTracker:
    """Tracks resource usage against limits"""

    def __init__(self, limits: Optional[ResourceLimits] = None):
        self.limits = limits or ResourceLimits()
        self.start_time: Optional[float] = None
        self.iteration_count = 0
        self.enabled = True

    def start(self):
        """Start tracking (reset counters)"""
        self.start_time = time.time()
        self.iteration_count = 0

    def check_variables(self, count: int) -> None:
        """Check if variable count exceeds limit"""
        if not self.enabled:
            return

        if count > self.limits.max_variables:
            from runtime.errors import AuraMemoryError, ErrorContext
            raise AuraMemoryError(
                f"Too many variables ({count}). Maximum: {self.limits.max_variables}",
                ErrorContext()
            )

    def check_functions(self, count: int) -> None:
        """Check if function count exceeds limit"""
        if not self.enabled:
            return

        if count > self.limits.max_functions:
            from runtime.errors import AuraMemoryError, ErrorContext
            raise AuraMemoryError(
                f"Too many functions ({count}). Maximum: {self.limits.max_functions}",
                ErrorContext()
            )

    def check_recursion(self, depth: int) -> None:
        """Check if recursion depth exceeds limit"""
        if not self.enabled:
            return

        if depth > self.limits.max_recursion_depth:
            from runtime.errors import AuraFunctionError, ErrorContext
            raise AuraFunctionError(
                f"Recursion limit exceeded. Maximum depth: {self.limits.max_recursion_depth}",
                ErrorContext()
            )

    def check_events(self, count: int) -> None:
        """Check if event queue size exceeds limit"""
        if not self.enabled:
            return

        if count > self.limits.max_events:
            from runtime.errors import AuraMemoryError, ErrorContext
            raise AuraMemoryError(
                f"Too many queued events ({count}). Maximum: {self.limits.max_events}",
                ErrorContext()
            )

    def check_execution_time(self) -> None:
        """Check if execution time exceeds limit"""
        if not self.enabled or not self.start_time:
            return

        elapsed = time.time() - self.start_time
        if elapsed > self.limits.max_execution_time:
            from runtime.errors import AuraRuntimeError, ErrorContext
            raise AuraRuntimeError(
                f"Execution timeout ({elapsed:.1f}s). Maximum: {self.limits.max_execution_time}s",
                ErrorContext()
            )

    def check_iterations(self) -> None:
        """Check if iteration count exceeds limit (for infinite loop detection)"""
        if not self.enabled:
            return

        self.iteration_count += 1
        if self.iteration_count > self.limits.max_iterations:
            from runtime.errors import AuraLoopError, ErrorContext
            raise AuraLoopError(
                f"Too many iterations ({self.iteration_count}). Possible infinite loop?",
                ErrorContext()
            )

    def disable(self):
        """Disable all checks (for debugging)"""
        self.enabled = False

    def enable(self):
        """Enable all checks"""
        self.enabled = True

    def get_usage(self) -> dict:
        """Get current resource usage"""
        elapsed = time.time() - self.start_time if self.start_time else 0

        return {
            'execution_time': elapsed,
            'iterations': self.iteration_count,
            'limits': {
                'max_variables': self.limits.max_variables,
                'max_functions': self.limits.max_functions,
                'max_recursion': self.limits.max_recursion_depth,
                'max_events': self.limits.max_events,
                'max_time': self.limits.max_execution_time,
                'max_iterations': self.limits.max_iterations
            }
        }
