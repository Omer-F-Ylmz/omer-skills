"""TOKEN-2 d1b K1b: doğal tetik (istem-r0e-B) ile 2 kol × 1 claude -p. Her kol temiz B worktree'si (ab_r0e.kur), vekil 6769, max_turns 12.
Kullanım: python k1b.py [--sil-eski] — --sil-eski önce B ve Bh'yi ab_r0e.sil ile (junction önce) kaldırır."""
import json, subprocess, sys, time
from pathlib import Path

import psutil

D = Path(__file__).parent
sys.path.insert(0, str(D)); sys.path.insert(0, r"C:\Users\pc\Desktop\TELVE-wt\token1\docs\r1\_ham\token1")
import ab_r0e  # noqa: E402
from k1_dogrula import kol  # noqa: E402

IZIN = ("--permission-mode", "acceptEdits", "--allowedTools", "Read,Edit,Write,Glob,Grep,Bash")

if "--sil-eski" in sys.argv:
    with open(D / "k1b_sil_oncesi.txt", "w", encoding="utf-8") as f:  # silinen koşu artıklarının izi
        for ad in ("B", "Bh"):
            w = ab_r0e.AB / ad
            if w.exists():
                f.write(f"== {ad}\n" + subprocess.run(["git", "-C", str(w), "status", "--short"], capture_output=True, text=True).stdout)
                ab_r0e.sil(ad)
for ad, e in (("A_varsayilan", {}), ("B_stable0", {"HEADROOM_STABLE_BOUNDARY_BREAKPOINT": "0"})):
    while psutil.virtual_memory().percent >= 85:  # d2b: RAM ≥%85 → yeni kol yok
        print("RAM", psutil.virtual_memory().percent, "bekle", flush=True); time.sleep(60)
    w = ab_r0e.kur("B")
    try:
        r = kol("b_" + ad, e, istem=ab_r0e.istem("B"), cwd=w, tur=12, ek=IZIN, sure=1500)  # kol başı 25 dk
    finally:
        ab_r0e.sil("B")
    if "onbelleksiz" in r:  # giriş tarafı ağırlıklı: önbelleksiz 1 · okuma 0.1 · yazma 1.25
        r["agirlikli_giris"] = round(r["onbelleksiz"] + 0.1 * r["okuma"] + 1.25 * r["yazma"])
    print(json.dumps(r, ensure_ascii=False), flush=True)
    with open(D / "k1b.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("BITTI", flush=True)
