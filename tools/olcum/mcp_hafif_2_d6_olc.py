"""MCP-HAFIF-2 d6 ölçümü (0 claude -p): auth0 stdio ve Serena (uvx git+ / geçici dizine uv tool install) açılış süresi + ağaç RAM'i.
Kurulum yalnız geçici UV_TOOL_DIR'e (canlı uv araçlarına ve ~/.claude.json'a dokunmaz). Çıktı: docs/kutuphane/olcum/mcp-hafif-2-d6.jsonl"""
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mcp_acilis import GIZLI, kos  # noqa: E402

KOK = Path(__file__).resolve().parents[2]
CIKTI = KOK / "docs/kutuphane/olcum/mcp-hafif-2-d6.jsonl"
SERENA = "git+https://github.com/oraios/serena@v1.7.0"
N = 3


def yaz(etiket, i, r):
    r = {"etiket": etiket, "kosu": i, "zaman": time.strftime("%H:%M:%S"), **r}
    r["arac_sayisi"] = len(r.pop("araclar", []) or [])
    with open(CIKTI, "a", encoding="utf-8") as f:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(json.dumps(r, ensure_ascii=False), flush=True)


def olc(etiket, komut, araclar_kayit):
    for i in range(1, N + 1):
        r = kos(komut, sinir=180)
        araclar_kayit[etiket] = r.get("araclar") or araclar_kayit.get(etiket)
        yaz(etiket, i, r)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    os.chdir(KOK)  # CC MCP'leri proje cwd'siyle açar
    araclar = {}
    olc("auth0-stdio", ["cmd", "/c", "npx", "-y", "@auth0/auth0-mcp-server@0.1.0-beta.19", "run"], araclar)
    olc("serena-uvx", ["uvx", "--from", SERENA, "serena", "start-mcp-server"], araclar)
    gecici = Path(tempfile.mkdtemp(prefix="serena-olc-"))
    env = {**os.environ, "UV_TOOL_DIR": str(gecici / "tools"), "UV_TOOL_BIN_DIR": str(gecici / "bin")}
    t0 = time.time()
    k = subprocess.run(["uv", "tool", "install", SERENA], env=env, capture_output=True, text=True, creationflags=GIZLI)
    yaz("serena-kurulum", 1, {"rc": k.returncode, "sure": round(time.time() - t0, 1), "hata": k.stderr[-300:] if k.returncode else ""})
    exe = gecici / "bin" / "serena.exe"
    if exe.exists():
        olc("serena-sabit", [str(exe), "start-mcp-server"], araclar)
    print("ARAC-ESIT serena", araclar.get("serena-uvx") == araclar.get("serena-sabit"), flush=True)
    print("BITTI", gecici, flush=True)
