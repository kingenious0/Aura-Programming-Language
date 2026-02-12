# Aura CLI Wrapper for Windows PowerShell
# Usage: .\aura.ps1 run myfile.aura

$args_string = $args -join ' '
python -m transpiler.cli $args_string
