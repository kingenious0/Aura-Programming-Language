"""
Aura Core - English to Python Logic Compiler
Transforms Aura AST into executable Python code
"""

from typing import List
from .ast_nodes import (
    ASTNode, VariableNode, PrintNode, BinaryOpNode,
    IfNode, LoopNode, FunctionDefNode, FunctionCallNode, Program,
    FetchNode
)


class PythonGenerator:
    """Generates Python code from Aura AST"""

    def __init__(self):
        self.indent_level = 0
        self.indent_str = "    "  # 4 spaces

    def generate(self, program: Program) -> str:
        """Generate Python code from AST"""
        lines = []
        for stmt in program.statements:
            code = self._generate_statement(stmt)
            if code:
                lines.append(code)
        return "\n".join(lines)

    def _generate_statement(self, node: ASTNode) -> str:
        """Generate code for a single statement"""
        if isinstance(node, VariableNode):
            return self._generate_variable(node)
        elif isinstance(node, PrintNode):
            return self._generate_print(node)
        elif isinstance(node, IfNode):
            return self._generate_if(node)
        elif isinstance(node, LoopNode):
            return self._generate_loop(node)
        elif isinstance(node, FunctionDefNode):
            return self._generate_function(node)
        elif isinstance(node, FunctionCallNode):
            return self._generate_function_call(node)
        elif isinstance(node, FetchNode):
            # For logic execution, we can skip or simulate fetch
            return f"# Fetch from {node.source}"
        return ""

    def _indent(self) -> str:
        """Get current indentation"""
        return self.indent_str * self.indent_level

    def _generate_variable(self, node: VariableNode) -> str:
        """Generate: score = 10"""
        value = self._generate_value(node.value)
        return f"{self._indent()}{node.name} = {value}"

    def _generate_print(self, node: PrintNode) -> str:
        """Generate: print("Hello") or print(score)"""
        content = self._generate_value(node.content)
        return f"{self._indent()}print({content})"

    def _generate_if(self, node: IfNode) -> str:
        """Generate if-else block"""
        condition = self._generate_expression(node.condition)
        lines = [f"{self._indent()}if {condition}:"]

        # If body
        self.indent_level += 1
        for stmt in node.body:
            lines.append(self._generate_statement(stmt))
        self.indent_level -= 1

        # Else body
        if node.else_body:
            lines.append(f"{self._indent()}else:")
            self.indent_level += 1
            for stmt in node.else_body:
                lines.append(self._generate_statement(stmt))
            self.indent_level -= 1

        return "\n".join(lines)

    def _generate_loop(self, node: LoopNode) -> str:
        """Generate: for _ in range(5):"""
        lines = [f"{self._indent()}for _ in range({node.count}):"]

        self.indent_level += 1
        for stmt in node.body:
            lines.append(self._generate_statement(stmt))
        self.indent_level -= 1

        return "\n".join(lines)

    def _generate_function(self, node: FunctionDefNode) -> str:
        """Generate: def greet():"""
        lines = [f"{self._indent()}def {node.name}():"]

        self.indent_level += 1
        for stmt in node.body:
            lines.append(self._generate_statement(stmt))
        self.indent_level -= 1

        return "\n".join(lines)

    def _generate_function_call(self, node: FunctionCallNode) -> str:
        """Generate: greet()"""
        return f"{self._indent()}{node.name}()"

    def _generate_expression(self, expr) -> str:
        """Generate an expression (for conditions)"""
        if isinstance(expr, BinaryOpNode):
            left = self._generate_value(expr.left)
            right = self._generate_value(expr.right)
            op = self._map_operator(expr.operator)
            return f"{left} {op} {right}"
        return str(expr)

    def _generate_value(self, value) -> str:
        """Generate a value (literal or variable)"""
        if isinstance(value, BinaryOpNode):
            return self._generate_expression(value)
        elif isinstance(value, str):
            # Check if it's a number
            try:
                float(value)
                return value
            except ValueError:
                # Check if it's a variable (no quotes) or string literal (has quotes)
                if value.startswith('"') or value.startswith("'"):
                    return value
                else:
                    # It's a variable reference
                    return value
        if isinstance(value, FetchNode):
            return "[]"  # Return empty list for logic simulation of fetch
        return str(value)

    def _map_operator(self, op: str) -> str:
        """Map Aura operators to Python operators"""
        mapping = {
            'is': '==',
            'equals': '==',
            'greater than': '>',
            'less than': '<',
            'not': '!='
        }
        return mapping.get(op, op)


class AuraCore:
    """Main execution engine for Aura Core logic"""

    def __init__(self):
        self.generator = PythonGenerator()
        self.state = {}  # Runtime state dictionary

    def compile(self, program: Program) -> str:
        """Compile Aura AST to Python code"""
        return self.generator.generate(program)

    def execute(self, program: Program) -> None:
        """Compile and execute Aura program"""
        python_code = self.compile(program)
        exec(python_code, {})

    def execute_statement(self, statement: ASTNode) -> None:
        """Execute a single statement"""
        from .ast_nodes import Program
        # Create a temporary program with just this statement
        temp_program = Program(statements=[statement])
        python_code = self.compile(temp_program)
        # Execute with the runtime state
        exec(python_code, self.state)

    def trace(self, program: Program) -> None:
        """Execute with step-by-step tracing"""
        python_code = self.compile(program)
        print(python_code)
        print("\n=== Execution ===")
        exec(python_code, {})
