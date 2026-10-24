"""RET-KUR-1: taranmış (gitleaks+semgrep temiz, MIT) topluluk marketplace'lerini Claude Code'a ekler.
Yalnız marketplace kaydı; hiçbir plugin kurulmaz (bağlam maliyeti yok). Geri alma: claude plugin marketplace remove <ad>.
Kullanım: python onay/ret_kur_1_uygula.py"""
import os
import subprocess

MARKETPLACE = [
    "wshobson/agents",
    "VoltAgent/awesome-claude-code-subagents",
    "rashedInt32/jev-mcp",
    "klukacin/JEV_Claude_plugin",
]

for m in MARKETPLACE:
    p = subprocess.run(["claude", "plugin", "marketplace", "add", m], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=180, env=os.environ.copy())
    print(m, "->", p.returncode, (p.stdout + p.stderr).strip().splitlines()[-1:] or "")
