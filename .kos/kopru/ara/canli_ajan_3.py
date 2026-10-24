"""AJAN-TAM-YETKI-1 adım 7: 3 canlı `claude -p` koşusu (video-tarama / rea / headroom-compress); stream-json'dan araç kanıtı + RAM tepe. Koşu: python -I canli_ajan_3.py"""
import json
import subprocess
import sys
import threading
import time
from pathlib import Path

import psutil

KOK = Path(r"C:\Projeler\omer-skills")
sys.path.insert(0, str(KOK / "tools"))
import mcp_profil  # noqa: E402

CLAUDE = "claude"
NO_WIN = subprocess.CREATE_NO_WINDOW
REA = json.dumps({"mcpServers": {"rea": mcp_profil.tanimlar()["rea"]}})
KOSULAR = [
    ("video-tarama", ["Skill"], None, "Skill aracını skill='video-tarama' ile çağır; skill yüklenince başka hiçbir şey yapma, tek kelime 'tamam' yaz."),
    ("rea", ["mcp__rea__list_browser_targets"], REA, "mcp__rea__list_browser_targets aracını bir kez çağır, sonuç satır sayısını söyle, başka araç çağırma."),
    ("headroom-compress", ["Skill"], None, "Skill aracını skill='headroom-compress' ile çağır; skill yüklenince başka hiçbir şey yapma, tek kelime 'tamam' yaz."),
]


def koş(ad, izin, mcp, istem):
    argv = [CLAUDE, "-p", "--output-format", "stream-json", "--verbose", "--model", "sonnet", "--max-budget-usd", "0.5",
            "--allowedTools", *izin]
    if mcp:
        argv += ["--strict-mcp-config", "--mcp-config", mcp]
    tepe = [psutil.virtual_memory().percent]
    dur = threading.Event()

    def ornekle():
        while not dur.wait(1):
            tepe[0] = max(tepe[0], psutil.virtual_memory().percent)

    th = threading.Thread(target=ornekle)
    th.start()
    t0 = time.time()
    r = subprocess.run(argv, input=istem, capture_output=True, text=True, encoding="utf-8", timeout=300, creationflags=NO_WIN, cwd=KOK)
    dur.set()
    th.join()
    araclar, maliyet, sonuc = [], None, ""
    for s in r.stdout.splitlines():
        try:
            o = json.loads(s)
        except ValueError:
            continue
        if o.get("type") == "assistant":
            for b in o["message"].get("content", []):
                if b.get("type") == "tool_use":
                    araclar.append(b["name"] + (":" + b["input"].get("skill", "") if b["name"] == "Skill" else ""))
        if o.get("type") == "result":
            maliyet, sonuc = o.get("total_cost_usd"), str(o.get("result"))[:120]
    print(json.dumps({"koşu": ad, "çıkış": r.returncode, "araçlar": araclar, "usd": maliyet, "ram_tepe_%": tepe[0],
                      "sn": round(time.time() - t0), "sonuç": sonuc, "hata": r.stderr[-200:]}, ensure_ascii=False), flush=True)


for k in KOSULAR:
    koş(*k)
