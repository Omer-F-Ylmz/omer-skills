import json
import subprocess
from pathlib import Path

out = Path(r"C:\Users\pc\Desktop\DeepSeek V4.1 Flash Uncensored\varliklar.txt")
r = subprocess.run([r"C:\Windows\System32\curl.exe", "-sSL", "-A", "x",
                    "https://api.github.com/repos/ggml-org/llama.cpp/releases?per_page=6"], capture_output=True)
s = []
for rel in json.loads(r.stdout):
    s.append("## %s %s %s" % (rel["tag_name"], rel.get("prerelease"), rel.get("published_at")))
    s += ["  " + a["name"] for a in rel["assets"] if "win" in a["name"].lower()]
out.write_text("\n".join(s), encoding="utf-8")
