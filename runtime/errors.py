"""
Aura Error Model
Human-readable errors without Python traces
"""

from typing import Optional, List
from dataclasses import dataclass


@dataclass
class ErrorContext:
    """Context information for an error"""
    line_number: Optional[int] = None
    file_path: Optional[str] = None
    code_line: Optional[str] = None
    function_name: Optional[str] = None


class AuraError(Exception):
    """Base class for all Aura errors"""

    def __init__(self, message: str, context: Optional[ErrorContext] = None):
        self.message = message
        self.context = context or ErrorContext()
        super().__init__(message)

    def format(self) -> str:
        """Format error for human consumption"""
        parts = [f"AuraError: {self.message}"]

        if self.context.line_number:
            parts.append(f"  Line: {self.context.line_number}")

        if self.context.file_path:
            parts.append(f"  File: {self.context.file_path}")

        if self.context.function_name:
            parts.append(f"  In: {self.context.function_name}")

        if self.context.code_line:
            parts.append(f"  Code: {self.context.code_line.strip()}")

        return "\n".join(parts)

    def __str__(self) -> str:
        return self.format()


class AuraVariableError(AuraError):
    """Variable not defined or invalid"""
    pass


class AuraMathError(AuraError):
    """Math operation error (division by zero, etc)"""
    pass


class AuraLoopError(AuraError):
    """Loop-related error (infinite loop, etc)"""
    pass


class AuraFunctionError(AuraError):
    """Function-related error (not found, recursion limit, etc)"""
    pass


class AuraMemoryError(AuraError):
    """Memory/resource limit exceeded"""
    pass


class AuraRuntimeError(AuraError):
    """General runtime error"""
    pass


def wrap_python_error(python_error: Exception, context: Optional[ErrorContext] = None) -> AuraError:
    """Convert Python exception to Aura error"""

    error_type = type(python_error).__name__

    # Map Python errors to Aura errors
    if isinstance(python_error, NameError):
        # Extract variable name from message
        msg = str(python_error)
        if "'" in msg:
            var_name = msg.split("'")[1]
            return AuraVariableError(f"Variable '{var_name}' not defined", context)
        return AuraVariableError(str(python_error), context)

    elif isinstance(python_error, ZeroDivisionError):
        return AuraMathError("Division by zero", context)

    elif isinstance(python_error, RecursionError):
        return AuraFunctionError("Recursion limit exceeded (maximum depth: 100)", context)

    elif isinstance(python_error, MemoryError):
        return AuraMemoryError("Out of memory", context)

    elif isinstance(python_error, TypeError):
        return AuraMathError(f"Invalid operation: {python_error}", context)

    elif isinstance(python_error, ValueError):
        return AuraMathError(f"Invalid value: {python_error}", context)

    else:
        return AuraRuntimeError(f"{error_type}: {python_error}", context)


def safe_execute(func, context: Optional[ErrorContext] = None):
    """Execute function and convert errors to Aura errors"""
    try:
        return func()
    except AuraError:
        raise  # Already an Aura error
    except Exception as e:
        raise wrap_python_error(e, context)
