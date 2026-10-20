"""rtk2 kalite seti: 20 eğitim + 4 held-out (KİLİTLİ: rtk2_set.lock sha256; kapıya bakarak ayar yok). (ad, argv, anahtar|None)"""
EGITIM = [
    ("git log -10", ["git", "log", "-10", "--oneline"], "KONU"),
    ("git status", ["git", "status"], "BR"),
    ("ls -la tools", ["ls", "-la", "tools"], "token_olc.py"),
    ("git diff --stat 3", ["git", "diff", "HEAD~3", "--stat"], None),
    ("git log -30 --stat", ["git", "log", "-30", "--stat"], "KONU"),
    ("ls -la kök", ["ls", "-la"], "CLAUDE.md"),
    ("git diff HEAD~2", ["git", "diff", "HEAD~2"], None),
    ("git show --stat 5", ["git", "show", "--stat", "HEAD~5"], None),
    ("git branch -a", ["git", "branch", "-a"], "BR"),
    ("git diff --stat 5", ["git", "diff", "HEAD~5", "--stat"], None),
    ("ls -la docs", ["ls", "-la", "docs"], None),
    ("ls -la .kos/kopru", ["ls", "-la", ".kos/kopru"], None),
    ("git log -5 fuller", ["git", "log", "-5", "--format=fuller"], None),
    ("find tools py", ["find", "tools", "-maxdepth", "1", "-name", "*.py"], None),
    ("git status -sb", ["git", "status", "-sb"], "BR"),
    ("git diff cc_profil", ["git", "diff", "HEAD~1", "--", "tools/cc_profil.py"], None),
    ("git ls-files tools", ["git", "ls-files", "tools"], None),
    ("git diff HEAD~4", ["git", "diff", "HEAD~4"], None),
    ("ls -la .claude", ["ls", "-la", ".claude"], None),
    ("git log -15 --stat", ["git", "log", "-15", "--stat"], "KONU"),
]
HELD = [  # d2b kapısında tek seferlik
    ("H git blame", ["git", "blame", "-L", "1,30", "tools/cc_profil.py"], "def _yaz"),
    ("H find token-rea", ["find", ".kos/kopru/token-rea", "-type", "f"], "taban.py"),
    ("H ls -la .claude/agents", ["ls", "-la", ".claude/agents"], None),
    ("H git diff 3..1 tools", ["git", "diff", "HEAD~3", "HEAD~1", "--", "tools"], None),
]
HELD3 = [  # d3 kapısı, tek seferlik (kilit: rtk2_set3.lock); d3 süzgeçleri yazılırken seçildi, sonuç görülmeden
    ("H3 git status -s", ["git", "status", "-s"], "BR"),
    ("H3 git log -8 --stat", ["git", "log", "-8", "--stat"], "KONU"),
    ("H3 git diff 6 --stat", ["git", "diff", "HEAD~6", "--stat"], None),
    ("H3 ls -la mcp", ["ls", "-la", "mcp"], None),
    ("H3 find tools/olcum", ["find", "tools/olcum", "-type", "f"], None),
    ("H3 git diff 6 ogrenme", ["git", "diff", "HEAD~6", "--", "tools/ogrenme"], None),
    ("H3 git ls-files kos", ["git", "ls-files", ".kos/kopru"], None),
    ("H3 ls -la .claude/beyin4", ["ls", "-la", ".claude/beyin4"], None),
]
