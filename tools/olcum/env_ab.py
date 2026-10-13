"""MCP-HAFIF-2: kosucu -p env (DISABLE_AUTOUPDATER + CLAUDE_MEM_INTERNAL) önce/sonra — kol başına 2, tam 4 claude -p (tavan 4).
Girdi jetonu (input+cache_creation+cache_read), süre, kendi süreç ağacımızda görülen git.exe sayısı (temp_git klonu; paralel
oturumların temp_* klasörleri sayıma karışmasın diye klasör değil süreç sayılır). python tools/olcum/env_ab.py <cikti.tsv>"""
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mcp_hafif_kabul import torunlar  # noqa: E402


def anlik():
    """{pid: (ppid, ad, komut)} — git'in repo tespiti ile eklenti klonunu (clone/temp_git) ayırmak için komut satırı da."""
    ps = ("Get-CimInstance Win32_Process | ForEach-Object { \"$($_.ProcessId)`t$($_.ParentProcessId)`t$($_.Name)`t"
          "$($_.CommandLine -replace '\\s+',' ')\" }")
    r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", creationflags=0x08000000, timeout=60)
    return {int(p[0]): (int(p[1]), p[2], p[3]) for p in (s.split("\t", 3) for s in r.stdout.splitlines())
            if len(p) == 4 and p[0].isdigit() and p[1].isdigit()}

# $0.50 tavanı ilk turda aşılıyordu (tek "tamam" ≈ $0.66 → error_max_budget_usd, usage sıfır): d4 ölçümü geçersizdi
BUTCE = "2.00"


def sonuc(stdout):
    d = json.loads(stdout)
    if d.get("is_error"):
        raise SystemExit(f"claude -p hata: {d.get('subtype')} {d.get('errors') or str(d.get('result'))[:80]}")
    u = d.get("usage", {})
    girdi = u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)
    if not girdi:
        raise SystemExit(f"usage boş: {str(d.get('result'))[:80]}")  # plan limiti düz metin döner
    return girdi, u.get("cache_creation_input_tokens", 0)


def kos(ek_env):
    env = {k: v for k, v in os.environ.items()
           if k not in ("ANTHROPIC_BASE_URL", "ANTHROPIC_API_KEY", "DISABLE_AUTOUPDATER", "CLAUDE_MEM_INTERNAL")}
    env.update(ek_env, BROWSER="none")
    git, klon, kom, zin = set(), set(), {}, {}
    with tempfile.TemporaryDirectory(prefix="envab-", ignore_cleanup_errors=True) as bos:
        t = time.time()
        p = subprocess.Popen(["claude", "-p", "Sadece 'tamam' yaz.", "--output-format", "json", "--max-budget-usd", BUTCE],
                             env=env, cwd=bos, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True,
                             encoding="utf-8", creationflags=0x08000000)
        while p.poll() is None and time.time() - t < 300:
            d = anlik()
            yeni = {q for q in torunlar(d, p.pid) if d[q][1].lower() == "git.exe"}
            git |= yeni
            kom.update({q: d[q][2] for q in yeni})
            for q in yeni - set(zin):  # klonu kim açıyor: claude mı, bir hook mu (ebeveyn zinciri, komut başları)
                z, a = [], d[q][0]
                while a in d and a != p.pid and len(z) < 6:
                    z.append(d[a][1] + ":" + d[a][2][:70]); a = d[a][0]
                zin[q] = (d[q][2][:120], z)
            klon |= {q for q in yeni if "clone" in d[q][2] or "temp_" in d[q][2] or "fetch" in d[q][2] or "pull" in d[q][2]}
            time.sleep(1)
        out = p.communicate(timeout=60)[0]
        sure = time.time() - t
    print("  git:", sorted({k.split(" ", 2)[1][:40] if " " in k else "?" for k in kom.values()}), flush=True)
    for q in klon:
        print("  klon:", zin[q][0], "\n    <=", " <= ".join(zin[q][1]), flush=True)
    return (*sonuc(out), round(sure, 1), len(git), len(klon))


if __name__ == "__main__":
    satir = ["kol\tgirdi_jeton\tcache_yazma\tsure_sn\tgit_surec\tgit_klon"]
    tekrar = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    for ad, e in (("once", {}), ("sonra", {"DISABLE_AUTOUPDATER": "1", "CLAUDE_MEM_INTERNAL": "1"})) * tekrar:
        satir.append("\t".join(map(str, (ad, *kos(e)))))
        print(satir[-1], flush=True)
    Path(sys.argv[1]).write_text("\n".join(satir) + "\n", encoding="utf-8")
