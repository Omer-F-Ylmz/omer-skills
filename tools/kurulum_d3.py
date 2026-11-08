"""SKILL-KUR-4: kurulum-coz-4 DOGRULANDI kalemlerini kurar (guvenlik + HARIC listesi disinda).
Kullanim: python tools/kurulum_d3.py [--deneme] [--n N] [--is K]
--deneme: kurulum yapmadan yalniz kapiyi kosar (kurulum_d2 --sadece-kapi)."""
import csv, re, sys
from pathlib import Path

R = Path(__file__).resolve().parent.parent
HARIC = re.compile(r"baserow|fooocus|tex ?live|openclaw|clawdbot|moltbot|wireshark|tshark|kubectl|twenty|clickhouse", re.I)
def oku(p):
    with open(R / p, encoding="utf-8") as f:
        return list(csv.reader(f, delimiter="\t"))
guv = set((R / "tmp/sk4_guv.txt").read_text(encoding="utf-8").splitlines())
kal = [r[0] for r in oku("tmp/sk4_kapsam.tsv") if r[1] in ("SKILL", "CLI", "PAKET") and r[0] not in guv and not HARIC.search(r[0])]
a = sys.argv[1:]
deneme = "--deneme" in a
a = [x for x in a if x != "--deneme"]
sys.argv = [sys.argv[0], "--faz", "kur", "--coz", str(R / "docs/video-tarama/kurulum-coz-4.tsv"), "--kalem", "|".join(kal)] + a + (["--sadece-kapi"] if deneme else [])
sys.path.insert(0, str(R / "tools"))
import kurulum_d2
kurulum_d2.main()
