"""graphify update . (AST-only) — sor2 bayatlık denetimi bunu arka.py ile koşturur; CREATE_NO_WINDOW."""
import subprocess, sys
sys.exit(subprocess.run(["graphify", "update", "."], creationflags=0x08000000).returncode)
