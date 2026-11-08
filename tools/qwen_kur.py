import hashlib
import json
import os
import shutil
import subprocess
import time
import urllib.request
from pathlib import Path

KOK = Path(r"C:\Users\pc\Desktop\Yerel Sansursuz Model")
ESKI = Path(r"C:\Users\pc\Desktop\DeepSeek V4.1 Flash Uncensored")
REPO = "llmfan46/Qwen3.6-35B-A3B-uncensored-heretic-Native-MTP-Preserved-GGUF"
DOSYA = "Qwen3.6-35B-A3B-uncensored-heretic-Native-MTP-Preserved-Q4_K_S.gguf"
SHA = "44ee825ebc26640e81a751ea9333701dc21166eb4e96e2e0dc59ffff93860182"
BOY = 20433712288
ALIAS = "qwen3.6-35b-a3b-heretic"
CURL = r"C:\Windows\System32\curl.exe"
LLAMA = Path.home() / ".local" / "llama.cpp" / "llama-server.exe"
LOG = KOK / "kurulum.log"


def yaz(m):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(time.strftime("%H:%M:%S ") + m + "\n")


def istek(yol, veri=None, t=900):
    req = urllib.request.Request("http://127.0.0.1:8080" + yol, data=json.dumps(veri).encode() if veri else None,
                                 headers={"Content-Type": "application/json", "x-api-key": "yerel", "anthropic-version": "2023-06-01"})
    with urllib.request.urlopen(req, timeout=t) as r:
        return r.read().decode("utf-8", "replace")


KOK.mkdir(exist_ok=True)
(KOK / "model").mkdir(exist_ok=True)
LOG.write_text("", encoding="utf-8")
hedef = KOK / "model" / DOSYA
if not (hedef.exists() and hedef.stat().st_size == BOY):
    for d in range(1, 8):
        yaz("indir deneme %d bos %.0f GB" % (d, shutil.disk_usage("C:\\").free / 2**30))
        r = subprocess.run([CURL, "-sS", "-L", "--fail", "--retry", "5", "-C", "-", "-o", str(hedef),
                            "https://huggingface.co/%s/resolve/main/%s" % (REPO, DOSYA)], capture_output=True)
        if r.returncode in (0, 33) and hedef.stat().st_size == BOY:
            break
        yaz("curl %s %s" % (r.returncode, r.stderr[-300:]))
        time.sleep(30)
h = hashlib.sha256()
with open(hedef, "rb") as f:
    for b in iter(lambda: f.read(16 * 2**20), b""):
        h.update(b)
yaz("SHA %s" % ("OK" if h.hexdigest() == SHA else "UYUSMAZ " + h.hexdigest()))
if h.hexdigest() != SHA:
    raise SystemExit

arg = ["-m", str(hedef), "--jinja", "-c", "65536", "-ctk", "q8_0", "-ctv", "q8_0", "-fa", "on",
       "--host", "127.0.0.1", "--port", "8080", "--alias", ALIAS]
ayar = {"env": {"ANTHROPIC_BASE_URL": "http://127.0.0.1:8080", "ANTHROPIC_AUTH_TOKEN": "yerel", "ANTHROPIC_MODEL": ALIAS,
                "ANTHROPIC_SMALL_FAST_MODEL": ALIAS, "ANTHROPIC_DEFAULT_HAIKU_MODEL": ALIAS, "ANTHROPIC_DEFAULT_SONNET_MODEL": ALIAS,
                "ANTHROPIC_DEFAULT_OPUS_MODEL": ALIAS, "CLAUDE_CODE_SUBAGENT_MODEL": ALIAS,
                "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1", "DISABLE_TELEMETRY": "1"}, "disableAllHooks": True}
(KOK / "ayar.json").write_text(json.dumps(ayar, indent=2), encoding="utf-8")
(KOK / "mcp-bos.json").write_text('{ "mcpServers": {} }\n', encoding="utf-8")
ps1 = r'''param([int]$BeklemeDk = 10)
$llama = "%s"
$argStr = '%s'
function Hazir { try { Invoke-RestMethod "http://127.0.0.1:8080/health" -TimeoutSec 3 | Out-Null; $true } catch { $false } }
$sunucu = $null
if (-not (Hazir)) {
  $log = Join-Path $PSScriptRoot "sunucu.log"
  $sunucu = Start-Process $llama -ArgumentList $argStr -WindowStyle Hidden -RedirectStandardError $log -PassThru
  Write-Host "Model yukleniyor..."
  $bitis = (Get-Date).AddMinutes($BeklemeDk)
  while (-not (Hazir)) {
    if ($sunucu.HasExited) { Write-Host "Sunucu kapandi: $log"; Get-Content $log -Tail 15; Read-Host "Enter"; exit 1 }
    if ((Get-Date) -gt $bitis) { Stop-Process -Id $sunucu.Id -Force; Write-Host "Zaman asimi"; Read-Host "Enter"; exit 1 }
    Start-Sleep -Seconds 3
  }
}
Write-Host "Model hazir (%s). Claude Code aciliyor..."
$ayar = Join-Path $PSScriptRoot "ayar.json"
$mcp = Join-Path $PSScriptRoot "mcp-bos.json"
try { claude --settings "$ayar" --strict-mcp-config --mcp-config "$mcp" --disable-slash-commands @args }
finally { if ($sunucu -and -not $sunucu.HasExited) { Stop-Process -Id $sunucu.Id -Force; Write-Host "Model kapatildi, RAM bosaltildi." } }
''' % (LLAMA, " ".join('"%s"' % a if " " in a else a for a in arg), ALIAS)
(KOK / "baslat.ps1").write_text(ps1, encoding="utf-8-sig")
(Path.home() / ".local/bin/claude-ds.cmd").write_bytes(
    ('@echo off\r\npowershell -NoProfile -ExecutionPolicy Bypass -File "%s" %%*\r\n' % (KOK / "baslat.ps1")).encode("utf-8"))
(KOK / "BASLAT.cmd").write_bytes(('@echo off\r\ncd /d "%~dp0"\r\npowershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0baslat.ps1"\r\n').encode("utf-8"))
yaz("betikler yazildi; test basliyor")

subprocess.run(["taskkill", "/IM", "llama-server.exe", "/F"], capture_output=True)
sl = open(KOK / "sunucu.log", "w", encoding="utf-8")
p = subprocess.Popen([str(LLAMA)] + arg, stdout=sl, stderr=subprocess.STDOUT, creationflags=0x08000000)
bas = time.time()
while time.time() - bas < 600:
    if p.poll() is not None:
        yaz("SUNUCU KAPANDI %s" % p.returncode)
        break
    try:
        istek("/health", t=5)
        yaz("HAZIR %.0f sn" % (time.time() - bas))
        break
    except Exception:
        time.sleep(5)
try:
    t0 = time.time()
    r = istek("/v1/messages", {"model": ALIAS, "max_tokens": 400, "messages": [{"role": "user", "content": "Tek cümleyle: hangi modelsin?"}]})
    yaz("DOGRUDAN %.1f sn: %s" % (time.time() - t0, r[-500:]))
except Exception as e:
    yaz("DOGRUDAN HATA %r" % e)
env = {k: v for k, v in os.environ.items() if not k.startswith("ANTHROPIC_")}
t0 = time.time()
try:
    r = subprocess.run([str(Path.home() / ".local/bin/claude.exe"), "-p", "Bu klasördeki dosyaları listele ve tek cümleyle hangi model olduğunu söyle.",
                        "--settings", str(KOK / "ayar.json"), "--strict-mcp-config", "--mcp-config", str(KOK / "mcp-bos.json"),
                        "--disable-slash-commands", "--output-format", "json", "--allowedTools", "Bash(ls:*),Bash(dir:*),Glob,Read"],
                       capture_output=True, text=True, errors="replace", env=env, timeout=900, cwd=str(KOK))
    yaz("CLAUDE -p %.0f sn exit %s: %s %s" % (time.time() - t0, r.returncode, r.stdout[-1200:], r.stderr[-300:]))
except Exception as e:
    yaz("CLAUDE HATA %r" % e)
sl.flush()
hiz = [l for l in (KOK / "sunucu.log").read_text(encoding="utf-8", errors="replace").splitlines()
       if "eval time" in l or "offloaded" in l or "fit" in l.lower() or "CUDA0 model buffer" in l]
yaz("HIZ\n" + "\n".join(hiz[-14:]))
p.kill()
yaz("BITTI")
