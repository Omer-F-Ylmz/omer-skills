"""Zayıf etiketi Haiku ile düzelt (uyuşmazlık >%10 olan kümeler): veri/{ad}_{train,test}.csv yeniden etiketlenir, eski dosya .zayif.csv.
python etiket_haiku.py <ad> [parti=70]  · en fazla ceil(satır/parti) claude -p çağrısı"""
import csv
import json
import os
import re
import shutil
import subprocess
import sys

from dogrula import D, KUME, SORU


def main():
    ad, parti = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 70
    yollar = [os.path.join(D, f"{ad}_{t}.csv") for t in ("train", "test")]
    veri = {y: list(csv.reader(open(y, encoding="utf-8"))) for y in yollar}
    tum = [(y, i) for y in yollar for i in range(1, len(veri[y]))]
    fark = cagri = 0
    for b in range(0, len(tum), parti):
        kesit = tum[b:b + parti]
        istek = f"{SORU[ad]} Seçenekler: {' | '.join(KUME[ad])}. Her numara için yalnız bir seçenek ver. Çıktı yalnız JSON: {{\"0\": \"seçenek\", ...}}\n\n"
        istek += "\n".join(f"[{n}] {veri[y][i][0][:400]}" for n, (y, i) in enumerate(kesit))
        p = subprocess.run(["claude", "-p", "--model", "claude-haiku-5-5", "--no-session-persistence"], input=istek,
                           capture_output=True, text=True, encoding="utf-8", timeout=300, creationflags=0x08000000)
        cagri += 1
        yanit = json.loads(re.search(r"\{.*\}", p.stdout, re.S).group(0))
        for n, (y, i) in enumerate(kesit):
            e = yanit.get(str(n))
            if e in KUME[ad]:
                fark += e != veri[y][i][1]
                veri[y][i][1] = e
        print(ad, "parti", cagri, flush=True)
    for y in yollar:
        if not os.path.exists(y.replace(".csv", ".zayif.csv")):
            shutil.copy(y, y.replace(".csv", ".zayif.csv"))
        csv.writer(open(y, "w", newline="", encoding="utf-8")).writerows(veri[y])
    print(ad, "çağrı", cagri, "değişen", fark, "/", len(tum))


if __name__ == "__main__":
    main()
