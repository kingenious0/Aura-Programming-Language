"""
State Manager - Central storage for variables and functions
Handles scoping, snapshots, and state persistence
"""

from typing import Any, Dict, Optional, List
from copy import deepcopy


class Scope:
    """Represents a variable scope (global or function-local)"""

    def __init__(self, parent: Optional['Scope'] = None):
        self.variables: Dict[str, Any] = {}
        self.parent = parent

    def get(self, name: str) -> Any:
        """Get variable, checking parent scopes if needed"""
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        raise NameError(f"Variable '{name}' not defined")

    def set(self, name: str, value: Any) -> None:
        """Set variable in current scope"""
        self.variables[name] = value

    def has(self, name: str) -> bool:
        """Check if variable exists in any scope"""
        if name in self.variables:
            return True
        if self.parent:
            return self.parent.has(name)
        return False


class StateManager:
    """
    Central state management for Aura runtime
    Manages variables, functions, scopes, and call stack
    """

    def __init__(self):
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        self.functions: Dict[str, Any] = {}
        self.call_stack: List[str] = []
        self.snapshots: List[Dict] = []

    def set_var(self, name: str, value: Any) -> None:
        """Set variable in current scope"""
        self.current_scope.set(name, value)

    def get_var(self, name: str) -> Any:
        """Get variable from current or parent scope"""
        try:
            return self.current_scope.get(name)
        except NameError:
            # Try global scope as fallback
            if name in self.global_scope.variables:
                return self.global_scope.variables[name]
            raise

    def has_var(self, name: str) -> bool:
        """Check if variable exists"""
        return self.current_scope.has(name)

    def register_function(self, name: str, ast_node: Any) -> None:
        """Register a function definition"""
        self.functions[name] = ast_node

    def get_function(self, name: str) -> Any:
        """Get function AST node"""
        if name not in self.functions:
            raise NameError(f"Function '{name}' not defined")
        return self.functions[name]

    def has_function(self, name: str) -> bool:
        """Check if function exists"""
        return name in self.functions

    def push_scope(self) -> None:
        """Enter a new scope (for function calls)"""
        self.current_scope = Scope(parent=self.current_scope)

    def pop_scope(self) -> None:
        """Exit current scope"""
        if self.current_scope.parent:
            self.current_scope = self.current_scope.parent

    def push_call(self, function_name: str) -> None:
        """Add function to call stack"""
        self.call_stack.append(function_name)

    def pop_call(self) -> str:
        """Remove function from call stack"""
        return self.call_stack.pop()

    def snapshot(self) -> Dict[str, Any]:
        """Create snapshot of current state"""
        snapshot = {
            'variables': deepcopy(self.current_scope.variables),
            'global_vars': deepcopy(self.global_scope.variables),
            'functions': list(self.functions.keys()),
            'call_stack': self.call_stack.copy()
        }
        self.snapshots.append(snapshot)
        return snapshot

    def get_all_vars(self) -> Dict[str, Any]:
        """Get all variables in current scope (for debugging)"""
        result = {}
        scope = self.current_scope
        while scope:
            result.update(scope.variables)
            scope = scope.parent
        return result

    def clear(self) -> None:
        """Reset state (useful for hot reload)"""
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        self.functions.clear()
        self.call_stack.clear()

    def __repr__(self) -> str:
        vars_count = len(self.get_all_vars())
        funcs_count = len(self.functions)
        return f"<StateManager: {vars_count} vars, {funcs_count} functions>"
