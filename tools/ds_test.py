import json
import os
import subprocess
import time
import urllib.request
from pathlib import Path

kok = Path(r"C:\Users\pc\Desktop\DeepSeek V4.1 Flash Uncensored")
log = kok / "ds_test.txt"
llama = Path.home() / ".local" / "llama.cpp" / "llama-server.exe"
m = kok / "model" / "DeepSeek-V4.1-Flash-1017-GSQ-RCO-IQ2_XXS-00001-of-00006.gguf"


def yaz(s):
    with open(log, "a", encoding="utf-8") as f:
        f.write(time.strftime("%H:%M:%S ") + s + "\n")


def istek(yol, veri=None, t=600):
    req = urllib.request.Request("http://127.0.0.1:8080" + yol, data=json.dumps(veri).encode() if veri else None,
                                 headers={"Content-Type": "application/json", "x-api-key": "yerel", "anthropic-version": "2023-06-01"})
    with urllib.request.urlopen(req, timeout=t) as r:
        return r.read().decode("utf-8", "replace")


log.write_text("", encoding="utf-8")
subprocess.run(["taskkill", "/IM", "llama-server.exe", "/F"], capture_output=True)
time.sleep(5)
sl = open(kok / "sunucu.log", "w", encoding="utf-8")
p = subprocess.Popen([str(llama), "-m", str(m), "--jinja", "-ngl", "99", "--n-cpu-moe", "40", "-c", "131072",
                      "--reasoning", "on", "--reasoning-effort", "50", "--host", "127.0.0.1", "--port", "8080",
                      "--alias", "deepseek-v4.1-flash-uncensored"], stdout=sl, stderr=subprocess.STDOUT, creationflags=0x08000000)
yaz("sunucu PID %d" % p.pid)
bas = time.time()
while time.time() - bas < 1500:
    if p.poll() is not None:
        yaz("SUNUCU KAPANDI kod %s" % p.returncode)
        break
    try:
        istek("/health", t=5)
        yaz("HAZIR %.0f sn" % (time.time() - bas))
        break
    except Exception:
        time.sleep(10)
try:
    t0 = time.time()
    r = istek("/v1/messages", {"model": "deepseek-v4.1-flash-uncensored", "max_tokens": 200,
                               "messages": [{"role": "user", "content": "Tek cümleyle: hangi modelsin?"}]})
    yaz("DOGRUDAN /v1/messages %.0f sn: %s" % (time.time() - t0, r[:600]))
except Exception as e:
    yaz("DOGRUDAN HATA %r" % e)
env = dict(os.environ)
for k in list(env):
    if k.startswith("ANTHROPIC_"):
        env.pop(k)
t0 = time.time()
r = subprocess.run([str(Path.home() / ".local/bin/claude.exe"), "-p", "Tek cümleyle: hangi modelsin?",
                    "--settings", str(kok / "ds-ayar.json"), "--strict-mcp-config", "--mcp-config", str(kok / "ds-mcp-bos.json"),
                    "--disable-slash-commands", "--output-format", "json"],
                   capture_output=True, text=True, errors="replace", env=env, timeout=900, cwd=str(kok))
yaz("CLAUDE -p %.0f sn exit %s: %s %s" % (time.time() - t0, r.returncode, r.stdout[-1500:], r.stderr[-500:]))
yaz("sunucu.log son: " + (kok / "sunucu.log").read_text(encoding="utf-8", errors="replace")[-1500:].replace("\n", " / "))
p.kill()
yaz("sunucu kapatildi; BITTI")
