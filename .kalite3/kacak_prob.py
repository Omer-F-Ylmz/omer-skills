"""MCP-HAFIF-2 (a) kaçak yeniden üretimi: ajn-mcp-kurulum-denetci yeni kolunu tek sefer koşar, 5 sn'de bir
kendi RAM'imi ve claude ağacının RAM'ini yazar; toplam > TAVAN_GB ise yalnız kendi claude çocuklarımı PID ile öldürür.
  python .kalite3/kacak_prob.py   (≤ 2 claude -p: dene() bir yeniden deneme yapabilir)"""
import os, subprocess, sys, threading, time
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(KOK / "tools"), str(KOK / "tools" / "olcum")]
sys.stdout.reconfigure(encoding="utf-8")
os.environ["OLCUM_MCP_HAFIF"] = "1"
import kosucu, model_olc, mcp_hafif_kabul as k  # noqa: E402

TAVAN_GB = 4.0
olcu = {}
_eski = kosucu.calistir


def calistir(*a, **kw):
    out, rc, err = _eski(*a, **kw)
    olcu.setdefault("stdout_mb", []).append(round(len(out) / 2**20, 1))
    olcu.setdefault("rc", []).append(rc)
    return out, rc, err


kosucu.calistir = calistir
import json  # noqa: E402
g = {x["ajan"]: x for x in json.loads((model_olc.AJAN / "gorevler.json").read_text(encoding="utf-8"))}["ajn-mcp-kurulum-denetci"]
_, t = model_olc.tanim(next(model_olc.AJAN.glob("*/ajn-mcp-kurulum-denetci.md")), g["model"])
sonuc = {}
th = threading.Thread(target=lambda: sonuc.update(model_olc.kos("ajn-mcp-kurulum-denetci", t, g["model"], g["istem"])), daemon=True)
t0 = time.monotonic()
th.start()
while th.is_alive():
    th.join(5)
    try:
        d = k.anlik()
    except subprocess.TimeoutExpired:
        continue
    ben = d.get(os.getpid(), (0, "", 0))[2]
    cc = [p for p, (pp, ad, _) in d.items() if pp == os.getpid() and ad.lower().startswith("claude")]
    agac = [p for c in cc for p in [c, *k.torunlar(d, c)]]
    ram = sum(d[p][2] for p in agac)
    print(f"{time.monotonic() - t0:6.0f}s ben={ben / 2**20:6.0f}MB agac={ram / 2**20:6.0f}MB n={len(agac)}", flush=True)
    if (ben + ram) / 2**30 > TAVAN_GB:
        for c in cc:
            subprocess.run(["taskkill", "/PID", str(c), "/T", "/F"], capture_output=True, creationflags=kosucu.PENCERESIZ)
        print("TAVAN aşıldı → claude çocukları öldürüldü", flush=True)
print("bitti", round(time.monotonic() - t0), olcu, "metin", len(sonuc.get("metin", "")), "usd", sonuc.get("usd"))
