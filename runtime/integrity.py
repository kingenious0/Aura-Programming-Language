"""
State Integrity System
Provides snapshots, rollback, and transaction-like execution
"""

from typing import Dict, Any, Optional, List
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime


@dataclass
class StateSnapshot:
    """Immutable snapshot of runtime state"""
    timestamp: str
    variables: Dict[str, Any]
    global_vars: Dict[str, Any]
    functions: List[str]
    call_stack: List[str]
    snapshot_id: int

    def __repr__(self) -> str:
        var_count = len(self.variables) + len(self.global_vars)
        func_count = len(self.functions)
        return f"<Snapshot #{self.snapshot_id}: {var_count} vars, {func_count} funcs @ {self.timestamp}>"


class StateIntegrity:
    """Manages state snapshots and rollback"""

    def __init__(self):
        self.snapshots: List[StateSnapshot] = []
        self.next_id = 0

    def snapshot(self, state_manager) -> StateSnapshot:
        """Create immutable snapshot of current state"""
        snapshot = StateSnapshot(
            timestamp=datetime.now().isoformat(),
            variables=deepcopy(state_manager.current_scope.variables),
            global_vars=deepcopy(state_manager.global_scope.variables),
            functions=list(state_manager.functions.keys()),
            call_stack=state_manager.call_stack.copy(),
            snapshot_id=self.next_id
        )

        self.next_id += 1
        self.snapshots.append(snapshot)

        # Keep only last 10 snapshots to prevent memory growth
        if len(self.snapshots) > 10:
            self.snapshots.pop(0)

        return snapshot

    def rollback(self, state_manager, snapshot: StateSnapshot) -> None:
        """Restore state from snapshot"""
        # Clear current state
        state_manager.current_scope.variables.clear()
        state_manager.global_scope.variables.clear()
        state_manager.call_stack.clear()

        # Restore from snapshot
        state_manager.current_scope.variables.update(
            deepcopy(snapshot.variables))
        state_manager.global_scope.variables.update(
            deepcopy(snapshot.global_vars))
        state_manager.call_stack.extend(snapshot.call_stack)

        # Note: Functions are not restored (they're code, not state)

    def get_latest_snapshot(self) -> Optional[StateSnapshot]:
        """Get most recent snapshot"""
        return self.snapshots[-1] if self.snapshots else None

    def get_snapshot(self, snapshot_id: int) -> Optional[StateSnapshot]:
        """Get specific snapshot by ID"""
        for snapshot in self.snapshots:
            if snapshot.snapshot_id == snapshot_id:
                return snapshot
        return None

    def list_snapshots(self) -> List[StateSnapshot]:
        """List all snapshots"""
        return self.snapshots.copy()

    def clear_snapshots(self) -> None:
        """Clear all snapshots"""
        self.snapshots.clear()

    def verify_state(self, state_manager) -> bool:
        """Verify state integrity (basic checks)"""
        try:
            # Check that variables are accessible
            state_manager.get_all_vars()

            # Check that functions are valid
            for func_name in state_manager.functions:
                assert isinstance(func_name, str)

            # Check call stack
            for func in state_manager.call_stack:
                assert isinstance(func, str)

            return True
        except Exception:
            return False


class TransactionContext:
    """Context manager for transactional execution"""

    def __init__(self, state_manager, integrity: StateIntegrity):
        self.state_manager = state_manager
        self.integrity = integrity
        self.snapshot: Optional[StateSnapshot] = None
        self.committed = False

    def __enter__(self):
        """Create snapshot on entry"""
        self.snapshot = self.integrity.snapshot(self.state_manager)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Rollback on error, commit on success"""
        if exc_type is not None and not self.committed:
            # Error occurred, rollback
            if self.snapshot:
                self.integrity.rollback(self.state_manager, self.snapshot)
            return False  # Re-raise exception

        # Success, commit (snapshot already taken)
        self.committed = True
        return True

    def commit(self):
        """Explicitly commit transaction"""
        self.committed = True

    def abort(self):
        """Explicitly abort and rollback"""
        if self.snapshot:
            self.integrity.rollback(self.state_manager, self.snapshot)
        self.committed = False
