"""
Aura Transpiler Engine
Main transpiler that orchestrates parsing and HTML generation
"""

import os
import sys
from pathlib import Path
from typing import Optional

from parser import AuraParser
from html_generator import HTMLGenerator


class AuraTranspiler:
    """Main transpiler engine for Aura programming language"""

    def __init__(self):
        self.parser = AuraParser()
        self.generator = HTMLGenerator()

    def transpile(self, input_file: str, output_file: Optional[str] = None) -> str:
        """
        Transpile an Aura file to HTML

        Args:
            input_file: Path to the .aura file
            output_file: Optional path for output HTML file (default: index.html)

        Returns:
            Path to the generated HTML file
        """
        # Validate input file
        if not input_file.endswith('.aura'):
            raise ValueError("Input file must have .aura extension")

        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")

        # Set default output file
        if output_file is None:
            output_dir = os.path.dirname(input_file) or '.'
            output_file = os.path.join(output_dir, 'index.html')

        print(f"Aura Transpiler v1.0")
        print(f"Input:  {input_file}")
        print(f"Output: {output_file}")
        print()

        # Parse the Aura file
        print("Parsing Aura commands...")
        try:
            commands = self.parser.parse_file(input_file)
            print(f"[OK] Parsed {len(commands)} command(s)")
        except Exception as e:
            print(f"[ERROR] Parsing failed: {str(e)}")
            raise

        # Validate commands
        try:
            self.parser.validate_commands(commands)
        except Exception as e:
            print(f"[WARNING] Validation warning: {str(e)}")

        # Display parsed commands
        print("\nCommands found:")
        for i, cmd in enumerate(commands, 1):
            print(f"   {i}. [{cmd.command_type.upper()}] {cmd.raw_line}")

        # Generate HTML
        print("\nGenerating HTML...")
        try:
            html_content = self.generator.generate(commands)
            print("[OK] HTML generated successfully")
        except Exception as e:
            print(f"[ERROR] Generation failed: {str(e)}")
            raise

        # Write output file
        print(f"\nWriting to {output_file}...")
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print("[OK] File written successfully")
        except Exception as e:
            print(f"[ERROR] Write failed: {str(e)}")
            raise

        print(f"\nTranspilation complete!")
        print(f"Open {output_file} in your browser to view the result.")

        return output_file

    def transpile_string(self, aura_code: str) -> str:
        """
        Transpile Aura code from a string (useful for testing)

        Args:
            aura_code: Aura code as a string

        Returns:
            Generated HTML string
        """
        # Create a temporary file
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.aura', delete=False, encoding='utf-8') as f:
            f.write(aura_code)
            temp_file = f.name

        try:
            commands = self.parser.parse_file(temp_file)
            html_content = self.generator.generate(commands)
            return html_content
        finally:
            # Clean up temp file
            os.unlink(temp_file)


def main():
    """Command-line interface for the transpiler"""
    if len(sys.argv) < 2:
        print("Usage: python transpiler.py <input.aura> [output.html]")
        print("\nExample:")
        print("  python transpiler.py app.aura")
        print("  python transpiler.py app.aura output.html")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    transpiler = AuraTranspiler()

    try:
        transpiler.transpile(input_file, output_file)
    except Exception as e:
        print(f"\n❌ Transpilation failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
