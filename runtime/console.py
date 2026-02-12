"""
Aura Console - Interactive REPL for Runtime Control
Commands: pause, resume, step, inspect, inject, etc.
"""

from typing import Optional, Dict, Callable, List
import sys


class AuraConsole:
    """Interactive console for runtime control and debugging"""

    def __init__(self, runtime):
        self.runtime = runtime
        self.running = False
        self.history: List[str] = []

        # Command registry
        self.commands: Dict[str, Callable] = {
            'help': self.cmd_help,
            'pause': self.cmd_pause,
            'resume': self.cmd_resume,
            'step': self.cmd_step,
            'back': self.cmd_back,
            'goto': self.cmd_goto,
            'inspect': self.cmd_inspect,
            'watch': self.cmd_watch,
            'inject': self.cmd_inject,
            'checkpoint': self.cmd_checkpoint,
            'timeline': self.cmd_timeline,
            'rollback': self.cmd_rollback,
            'reset': self.cmd_reset,
            'kill': self.cmd_kill,
            'exit': self.cmd_exit,
            'quit': self.cmd_exit
        }

    def start(self):
        """Start interactive console"""
        self.running = True
        print("🎮 Aura Console - Interactive Runtime Control")
        print("Type 'help' for commands, 'exit' to quit\n")

        while self.running:
            try:
                # Prompt
                cmd_input = input("aura> ").strip()

                if not cmd_input:
                    continue

                # Add to history
                self.history.append(cmd_input)

                # Parse and execute
                self.execute(cmd_input)

            except KeyboardInterrupt:
                print("\n^C - Use 'exit' to quit")
            except EOFError:
                break
            except Exception as e:
                print(f"❌ Error: {e}")

        print("\nConsole closed.")

    def execute(self, cmd_input: str):
        """Execute a console command"""
        parts = cmd_input.split()
        if not parts:
            return

        cmd_name = parts[0].lower()
        args = parts[1:]

        if cmd_name in self.commands:
            try:
                self.commands[cmd_name](args)
            except Exception as e:
                print(f"❌ Command error: {e}")
        else:
            print(f"❌ Unknown command: {cmd_name}")
            print("   Type 'help' for available commands")

    # === COMMAND IMPLEMENTATIONS ===

    def cmd_help(self, args):
        """Show help"""
        print("""
Available Commands:

  🎮 Execution Control:
    pause              Pause execution
    resume             Resume execution  
    step               Execute one step forward
    back               Go back one step
    goto <n>           Jump to step N
    
  🔍 Inspection:
    inspect state      Show all state
    inspect vars       Show variables
    inspect events     Show event queue
    inspect memory     Show memory usage
    watch <var>        Monitor variable
    timeline           Show execution timeline
    
  💉 Injection:
    inject <code>      Execute Aura code live
    
  📍 Checkpoints:
    checkpoint <name>  Create named checkpoint
    rollback <n>       Go back N steps
    
  🔧 Control:
    reset              Reset runtime
    kill               Stop execution
    exit/quit          Exit console
    help               Show this help
        """)

    def cmd_pause(self, args):
        """Pause execution"""
        self.runtime.time_engine.pause()
        print("⏸️  Execution paused")

    def cmd_resume(self, args):
        """Resume execution"""
        self.runtime.time_engine.resume()
        print("▶️  Execution resumed")

    def cmd_step(self, args):
        """Step forward one statement"""
        self.runtime.time_engine.enable_step_mode()
        step = self.runtime.time_engine.step_forward()
        if step:
            print(f"➡️  Step {step.step_number}: {step.node_repr}")
        else:
            print("⚠️  No more steps")

    def cmd_back(self, args):
        """Step backward"""
        step = self.runtime.time_engine.step_backward()
        if step:
            print(f"⬅️  Step {step.step_number}: {step.node_repr}")
        else:
            print("⚠️  Already at beginning")

    def cmd_goto(self, args):
        """Jump to specific step"""
        if not args:
            print("❌ Usage: goto <step_number>")
            return

        try:
            step_num = int(args[0])
            step = self.runtime.time_engine.goto(step_num)
            if step:
                print(f"⏩ Jumped to step {step.step_number}: {step.node_repr}")
            else:
                print(f"❌ Invalid step number: {step_num}")
        except ValueError:
            print("❌ Step number must be an integer")

    def cmd_inspect(self, args):
        """Inspect runtime state"""
        if not args:
            args = ['state']

        target = args[0].lower()

        if target == 'state':
            print(self.runtime.inspector.format_full())
        elif target == 'vars':
            print(self.runtime.inspector.format_vars())
        elif target == 'events':
            print(self.runtime.inspector.format_events())
        elif target == 'memory':
            print(self.runtime.inspector.format_memory())
        elif target == 'functions':
            print(self.runtime.inspector.format_functions())
        else:
            # Inspect specific variable
            try:
                value = self.runtime.state.get_var(target)
                print(f"{target} = {repr(value)}")
            except:
                print(f"❌ Unknown target: {target}")

    def cmd_watch(self, args):
        """Watch a variable"""
        if not args:
            print("❌ Usage: watch <variable>")
            return

        var_name = args[0]
        history = self.runtime.time_engine.get_variable_history(var_name)

        if history:
            print(f"📊 History of '{var_name}':")
            for step_num, value in history:
                print(f"  Step {step_num}: {repr(value)}")
        else:
            print(f"⚠️  No history for variable '{var_name}'")

    def cmd_inject(self, args):
        """Inject and execute code"""
        if not args:
            print("❌ Usage: inject <aura code>")
            return

        code = ' '.join(args)
        print(f"💉 Injecting: {code}")

        try:
            from transpiler.logic_parser import LogicParser
            parser = LogicParser()

            # Create temp file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.aura', delete=False) as f:
                f.write(code)
                temp_path = f.name

            # Parse
            program = parser.parse_file(temp_path)

            # Execute in current runtime
            from transpiler.core import AuraCore
            core = AuraCore()
            core.state = self.runtime.state  # Use existing state
            core.execute(program)

            print("✅ Code executed")

            # Cleanup
            import os
            os.unlink(temp_path)

        except Exception as e:
            print(f"❌ Injection failed: {e}")

    def cmd_checkpoint(self, args):
        """Create named checkpoint"""
        if not args:
            print("❌ Usage: checkpoint <name>")
            return

        name = args[0]
        step_num = self.runtime.time_engine.create_checkpoint(name)
        print(f"📍 Checkpoint '{name}' created at step {step_num}")

    def cmd_timeline(self, args):
        """Show execution timeline"""
        print(self.runtime.time_engine.format_timeline())

    def cmd_rollback(self, args):
        """Rollback N steps"""
        n = 1
        if args:
            try:
                n = int(args[0])
            except ValueError:
                print("❌ Argument must be a number")
                return

        step = self.runtime.time_engine.rewind(n)
        if step:
            print(f"⏪ Rolled back {n} step(s) to {step.step_number}")
        else:
            print("⚠️  Cannot rollback further")

    def cmd_reset(self, args):
        """Reset runtime"""
        confirm = input(
            "⚠️  Reset runtime? This will clear all state. (y/N): ")
        if confirm.lower() == 'y':
            self.runtime.state.clear()
            self.runtime.time_engine.clear_history()
            print("✅ Runtime reset")
        else:
            print("Cancelled")

    def cmd_kill(self, args):
        """Kill execution"""
        self.runtime.stop()
        print("🛑 Execution stopped")

    def cmd_exit(self, args):
        """Exit console"""
        self.running = False


def start_console(runtime):
    """Convenience function to start console"""
    console = AuraConsole(runtime)
    console.start()
