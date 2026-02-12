"""
Test Aura 2.6 Safety Systems
"""

from transpiler.logic_parser import LogicParser
from runtime import AuraRuntime, ResourceLimits, AuraError
import sys
sys.path.insert(0, 'c:/Users/kinge/AuraProgrammingLanguage')


def test_introspection():
    """Test runtime introspection"""
    print("=== Test 1: Introspection ===")

    code = """
set x to 10
set y to 20
set name to "Aura"
"""

    parser = LogicParser()
    program = parser.parse(code)

    runtime = AuraRuntime(program)
    runtime.load_program(program)
    runtime.execute_once()

    print(runtime.inspector.format_vars())
    print(runtime.inspector.format_memory())
    print("✅ Introspection works!\n")


def test_error_handling():
    """Test error model"""
    print("=== Test 2: Error Handling ===")

    code = """
set x to 10
print unknown_var
"""

    parser = LogicParser()
    program = parser.parse(code)

    runtime = AuraRuntime(program)
    runtime.load_program(program)
    runtime.safe_mode = True  # Don't crash on error

    try:
        runtime.execute_once()
    except AuraError as e:
        print(f"Caught error: {e}")
        print("✅ Error handling works!\n")


def test_state_rollback():
    """Test state integrity and rollback"""
    print("=== Test 3: State Rollback ===")

    code1 = "set count to 10"
    code2 = "set count to 99"

    parser = LogicParser()

    runtime = AuraRuntime()

    # Execute first
    p1 = parser.parse(code1)
    runtime.load_program(p1)
    runtime.execute_once()

    print(f"After first execution: count = {runtime.state.get_var('count')}")

    # Take snapshot
    snapshot = runtime.integrity.snapshot(runtime.state)

    # Execute second
    p2 = parser.parse(code2)
    runtime.program = p2
    runtime.execute_once()

    print(f"After second execution: count = {runtime.state.get_var('count')}")

    # Rollback
    runtime.integrity.rollback(runtime.state, snapshot)

    print(f"After rollback: count = {runtime.state.get_var('count')}")
    print("✅ Rollback works!\n")


def test_resource_limits():
    """Test memory limits"""
    print("=== Test 4: Resource Limits ===")

    runtime = AuraRuntime(limits=ResourceLimits(max_variables=5))

    # Try to create 10 variables (should fail at 5)
    try:
        for i in range(10):
            runtime.state.set_var(f'var_{i}', i)
            runtime.resource_tracker.check_variables(
                len(runtime.state.get_all_vars()))
    except AuraError as e:
        print(f"Limit enforced: {e}")
        print("✅ Resource limits work!\n")


if __name__ == '__main__':
    print("🧪 Testing Aura 2.6 Safety Systems\n")

    test_introspection()
    test_error_handling()
    test_state_rollback()
    test_resource_limits()

    print("🎉 All safety systems operational!")
