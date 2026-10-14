"""PLAN-KUR-3 K eğrisi (eğitim kümesi = PLAN-KUR-2'nin 7 zor işi; bekletilmiş plan_kur3 kümesi KULLANILMAZ).
Altın = A planlarında (sonuc.jsonl, yargıçta araç doğruluğu 2/2) geçen KURULU katalog adları; isabet@K = altının ilk K adayda olan oranı (@999 = havuz tavanı).
python .claude/plankur3/k_egrisi.py"""
import json
import re
import sys
from pathlib import Path

WT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(WT / "tools"))
import katalog_ara as ka  # noqa: E402
import plan_kur as pk  # noqa: E402

IS = [s.split("\t")[2] for s in (WT / "tests" / "fixtures" / "plan_kur2_isler.tsv").read_text(encoding="utf8").splitlines()[1:]]
PAKET = [[0, 1, 2], [3, 4], [5, 6]]
A = {str(r["paket"]): r["metin"] for r in map(json.loads, (WT / ".claude" / "plankur2" / "sonuc.jsonl").read_text(encoding="utf8").splitlines())
     if r["kol"] == "A"}
kurulu = {o["ad"] for o in pk.kayitlar() if ka.kurulu(o) and o["tur"] in ("skill", "ajan", "mcp", "cli")}
KS = (10, 20, 30, 40, 42, 43, 44, 45, 50, 999)
top = {"uzman": [0] * len(KS), "duz": [0] * len(KS)}
n_alt = 0
for p, grup in enumerate(PAKET):
    parca = re.split(r"(?m)^#{1,4} .*?(?=\d)(\d+)", A[str(p)])
    for i in grup:
        no = str(i + 1)  # A başlıkları küme genelinde numaralı (### 4, ### 6)
        metin = next((parca[j + 1] for j in range(1, len(parca) - 1, 2) if parca[j] == no), "")
        alt = {a for a in kurulu if (len(a) > 4 or re.search(r"[-:]", a)) and re.search(rf"(?<![\w:-]){re.escape(a)}(?![\w-])", metin)}
        kal, _, _ = pk.havuz(IS[i], ka.yigin(IS[i]))
        uz = [o["ad"] for o in pk.adaylar(IS[i], kal, 999)]
        duz = [o["ad"] for o in sorted(pk.adaylar(IS[i], kal, 999), key=lambda o: [x["ad"] for x in kal].index(o["ad"]))]
        n_alt += len(alt)
        for j, k in enumerate(KS):
            top["uzman"][j] += len(alt & set(uz[:k]))
            top["duz"][j] += len(alt & set(duz[:k]))
        print(f"iş {i + 1}: altın {len(alt)} · varlık {sorted(pk.varliklar(IS[i]))} · @20 uzman {len(alt & set(uz[:20]))} düz {len(alt & set(duz[:20]))}")
print(f"altın toplam {n_alt}")
for ad, v in top.items():
    print(ad.ljust(6), " ".join(f"@{k}={x / max(n_alt, 1):.2f}({x})" for k, x in zip(KS, v)))
