import json
from pathlib import Path

h = Path.home() / ".claude"
s = []
for ad in ("settings.json", "settings.local.json"):
    p = h / ad
    if p.exists():
        j = json.loads(p.read_text(encoding="utf-8"))
        env = j.get("env", {})
        s.append("%s env: %s" % (ad, {k: (v if "KEY" not in k and "TOKEN" not in k else "***") for k, v in env.items() if k.startswith(("ANTHROPIC", "CLAUDE"))}))
        s.append("%s hooks: %s" % (ad, {k: len(v) for k, v in j.get("hooks", {}).items()}))
        s.append("%s apiKeyHelper: %s" % (ad, j.get("apiKeyHelper")))
Path(r"C:\Users\pc\Desktop\DeepSeek V4.1 Flash Uncensored\ayar_bak.txt").write_text("\n".join(s), encoding="utf-8")
