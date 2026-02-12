"""
Time Engine - Execution History & Time Travel Debugging
Records every execution step for pause, rewind, replay capabilities
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from copy import deepcopy

from runtime.integrity import StateSnapshot


@dataclass
class ExecutionStep:
    """Represents a single execution step"""
    step_number: int
    timestamp: float
    node_type: str  # Type of AST node executed
    node_repr: str  # String representation
    line_number: Optional[int]
    state_before: StateSnapshot
    state_after: StateSnapshot
    variables_changed: List[str]  # Which variables changed

    def __repr__(self) -> str:
        return f"<Step #{self.step_number}: {self.node_type} @ line {self.line_number}>"


class TimeEngine:
    """
    Manages execution history and time travel
    The foundation of Aura's observability
    """

    def __init__(self, max_history: int = 1000):
        self.history: List[ExecutionStep] = []
        self.current_index: int = -1  # -1 = at latest
        self.max_history = max_history
        self.checkpoints: Dict[str, int] = {}  # name -> step_number
        self.paused = False
        self.step_mode = False

    def record_step(
        self,
        node_type: str,
        node_repr: str,
        line_number: Optional[int],
        state_before: StateSnapshot,
        state_after: StateSnapshot
    ) -> ExecutionStep:
        """Record an execution step"""

        # Detect changed variables
        vars_changed = []
        before_vars = {**state_before.global_vars, **state_before.variables}
        after_vars = {**state_after.global_vars, **state_after.variables}

        for var_name in after_vars:
            if var_name not in before_vars:
                vars_changed.append(var_name)
            elif before_vars[var_name] != after_vars[var_name]:
                vars_changed.append(var_name)

        # Create step
        step = ExecutionStep(
            step_number=len(self.history),
            timestamp=datetime.now().timestamp(),
            node_type=node_type,
            node_repr=node_repr,
            line_number=line_number,
            state_before=state_before,
            state_after=state_after,
            variables_changed=vars_changed
        )

        # Add to history
        self.history.append(step)

        # Limit history size
        if len(self.history) > self.max_history:
            self.history.pop(0)
            # Adjust checkpoint indices
            for name in self.checkpoints:
                self.checkpoints[name] -= 1

        self.current_index = len(self.history) - 1

        return step

    def pause(self) -> None:
        """Pause execution"""
        self.paused = True

    def resume(self) -> None:
        """Resume execution"""
        self.paused = False
        self.step_mode = False

    def enable_step_mode(self) -> None:
        """Enable step-by-step execution"""
        self.step_mode = True
        self.paused = True

    def step_forward(self) -> Optional[ExecutionStep]:
        """Move forward one step"""
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            return self.history[self.current_index]
        return None

    def step_backward(self) -> Optional[ExecutionStep]:
        """Move backward one step"""
        if self.current_index > 0:
            self.current_index -= 1
            return self.history[self.current_index]
        return None

    def goto(self, step_number: int) -> Optional[ExecutionStep]:
        """Jump to specific step"""
        if 0 <= step_number < len(self.history):
            self.current_index = step_number
            return self.history[step_number]
        return None

    def rewind(self, n_steps: int = 1) -> Optional[ExecutionStep]:
        """Go back N steps"""
        target = max(0, self.current_index - n_steps)
        return self.goto(target)

    def fast_forward(self, n_steps: int = 1) -> Optional[ExecutionStep]:
        """Go forward N steps"""
        target = min(len(self.history) - 1, self.current_index + n_steps)
        return self.goto(target)

    def create_checkpoint(self, name: str) -> int:
        """Create named checkpoint at current position"""
        step_num = self.current_index
        self.checkpoints[name] = step_num
        return step_num

    def goto_checkpoint(self, name: str) -> Optional[ExecutionStep]:
        """Jump to named checkpoint"""
        if name in self.checkpoints:
            return self.goto(self.checkpoints[name])
        return None

    def get_current_step(self) -> Optional[ExecutionStep]:
        """Get current execution step"""
        if 0 <= self.current_index < len(self.history):
            return self.history[self.current_index]
        return None

    def get_current_state(self) -> Optional[StateSnapshot]:
        """Get state at current position"""
        step = self.get_current_step()
        return step.state_after if step else None

    def get_timeline(self, start: int = 0, end: Optional[int] = None) -> List[ExecutionStep]:
        """Get slice of execution timeline"""
        if end is None:
            end = len(self.history)
        return self.history[start:end]

    def get_variable_history(self, var_name: str) -> List[tuple]:
        """Get history of variable changes"""
        changes = []
        for step in self.history:
            all_vars = {**step.state_after.global_vars,
                        **step.state_after.variables}
            if var_name in all_vars:
                changes.append((step.step_number, all_vars[var_name]))
        return changes

    def clear_history(self) -> None:
        """Clear all history"""
        self.history.clear()
        self.current_index = -1
        self.checkpoints.clear()

    def get_stats(self) -> dict:
        """Get timeline statistics"""
        return {
            'total_steps': len(self.history),
            'current_index': self.current_index,
            'checkpoints': len(self.checkpoints),
            'paused': self.paused,
            'step_mode': self.step_mode,
            'max_history': self.max_history
        }

    def format_timeline(self, context_lines: int = 5) -> str:
        """Format timeline around current position"""
        if not self.history:
            return "No execution history"

        start = max(0, self.current_index - context_lines)
        end = min(len(self.history), self.current_index + context_lines + 1)

        lines = ["Timeline:"]
        for i in range(start, end):
            step = self.history[i]
            marker = "→" if i == self.current_index else " "

            # Format changed variables
            if step.variables_changed:
                vars_str = ", ".join(step.variables_changed)
                lines.append(
                    f"  {marker} {step.step_number}: {step.node_type} [{vars_str}]")
            else:
                lines.append(
                    f"  {marker} {step.step_number}: {step.node_type}")

        return "\n".join(lines)

    def __repr__(self) -> str:
        status = "Paused" if self.paused else "Running"
        return f"<TimeEngine: {len(self.history)} steps, {status}, @ step {self.current_index}>"
