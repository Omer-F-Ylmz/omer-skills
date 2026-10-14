"""TOKEN-2 d3 K1b kurtarma: A kolunda claude bitti ama kill döngüsü NoSuchProcess ile çöktü, vekil (6769) yetim kaldı.
Kaydedilmiş çıktı + iz + yetim vekilin /stats'ı → k1b.jsonl'a A satırı. Vekili durdurmaz.
Kullanım: python k1b_kurtar.py <vekil_pid>"""
import json, sys
from pathlib import Path

import psutil

sys.stdout.reconfigure(encoding="utf-8")
D = Path(__file__).parent
sys.path.insert(0, str(D))
from k1_dogrula import ozet, stats  # noqa: E402

ad = "b_A_varsayilan"
cikti = D / f"k1_cikti_{ad}.json"
bas = psutil.Process(int(sys.argv[1])).create_time()
r = ozet(ad, cikti.read_text(encoding="utf-8", errors="replace"), D / f"k1_iz_{ad}.tsv", stats(), cikti.stat().st_mtime - bas)
r["kurtarma"] = "d3: kill döngüsü çöktü; süre = vekil başlangıcı → çıktı dosyası mtime"
if "onbelleksiz" in r:
    r["agirlikli_giris"] = round(r["onbelleksiz"] + 0.1 * r["okuma"] + 1.25 * r["yazma"])
print(json.dumps(r, ensure_ascii=False))
with open(D / "k1b.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(r, ensure_ascii=False) + "\n")
