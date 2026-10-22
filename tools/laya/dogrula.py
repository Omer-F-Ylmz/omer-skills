"""Etiket doğrulama: veri/{ad}_{train,test}.csv'den rastgele %10 -> Haiku (veri kümesi başına TEK claude -p çağrısı) -> sınıf başına uyuşmazlık.
python dogrula.py model tur konu   · çıktı veri/dogrula-<ad>.json (örnek, Haiku etiketi, uyuşmazlık)"""
import csv
import json
import os
import random
import re
import subprocess
import sys
from collections import Counter

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "veri")
KUME = {"model": ["haiku", "sonnet", "opus"],
        "tur": ["site-3d", "video", "guvenlik", "belge", "logo", "render", "diger"],
        "konu": ["ai-model", "kodlama-ajan", "tasarim-ui", "video-medya", "otomasyon", "guvenlik", "diger"]}
SORU = {"model": "Görev metni için işi doğru yapmaya yetecek EN UCUZ model katmanı hangisi (haiku|sonnet|opus)?",
        "tur": "Metnin iş türü hangisi?", "konu": "Metnin ana konusu hangisi?"}


def main():
    sonuc = {}
    for ad in sys.argv[1:]:
        satir = [r for t in ("train", "test") for r in list(csv.reader(open(os.path.join(D, f"{ad}_{t}.csv"), encoding="utf-8")))[1:]]
        rng = random.Random(7)
        ornek = rng.sample(range(len(satir)), max(8, len(satir) // 10))
        istek = f"{SORU[ad]} Seçenekler: {' | '.join(KUME[ad])}. Her numara için yalnız bir seçenek ver. Çıktı yalnız JSON: {{\"0\": \"seçenek\", ...}}\n\n"
        istek += "\n".join(f"[{n}] {satir[i][0][:400]}" for n, i in enumerate(ornek))
        p = subprocess.run(["claude", "-p", "--model", "claude-haiku-5-5", "--no-session-persistence"], input=istek,
                           capture_output=True, text=True, encoding="utf-8", timeout=300, creationflags=0x08000000)
        yanit = json.loads(re.search(r"\{.*\}", p.stdout, re.S).group(0))
        sonuc[ad] = [{"i": i, "etiket": satir[i][1], "haiku": yanit.get(str(n))} for n, i in enumerate(ornek)]
        sayi, ters = Counter(x["etiket"] for x in sonuc[ad]), Counter(x["etiket"] for x in sonuc[ad] if x["haiku"] != x["etiket"])
        print(ad, "örnek", len(ornek), "uyuşmazlık", sum(ters.values()), {k: f"{ters[k]}/{sayi[k]}" for k in sayi}, flush=True)
        json.dump(sonuc[ad], open(os.path.join(D, f"dogrula-{ad}.json"), "w", encoding="utf-8"), ensure_ascii=False)


if __name__ == "__main__":
    main()
