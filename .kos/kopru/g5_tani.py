"""G5 tani: claude -p + OmniRoute kucuk istem, sure + debug log. Cikti: g5-tani-<ad>.log"""
import os, subprocess, sys, time
sys.path.insert(0, "C:/Projeler/omer-skills/tools")
import ucretsiz_motor as m
ad = sys.argv[1]; ek = sys.argv[2:]
log = f"C:/Projeler/omer-skills/.kos/kopru/g5-tani-{ad}.log"
t = time.time()
try:
    r = subprocess.run(["claude", "-p", "--model", m.model(), "--output-format", "json", "--strict-mcp-config",
                        "--mcp-config", '{"mcpServers":{}}', "--disable-slash-commands", "--no-session-persistence",
                        "--debug-file", log, *ek], input="Sadece 'tamam' yaz.", capture_output=True, text=True,
                       encoding="utf-8", cwd="C:/Projeler/omer-skills", timeout=100, creationflags=0x08000000,
                       env=m.env_kur(dict(os.environ)))
    print(ad, round(time.time() - t), "sn rc", r.returncode, (r.stdout or r.stderr)[:200])
except subprocess.TimeoutExpired:
    print(ad, "ZAMAN ASIMI 100sn")
