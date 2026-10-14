"""RET kök nedeni: B0 metninin iş başlıkları + kor.md'deki B parçası boyu; kurulu-olmayan ad eşleşmeleri."""
import json, re, sys
from collections import Counter
from pathlib import Path

D = Path(__file__).parent
sys.path.insert(0, str(D.parents[1] / "tools"))
import plan_kur as pk  # noqa: E402

kayit = {(r["kol"], r["paket"]): r for r in map(json.loads, (D / "sonuc.jsonl").read_text(encoding="utf8").splitlines())}
b0 = kayit[("B", 0)]["metin"]
print("B0 başlıklar:", re.findall(r"^#{1,4}[^\n]{0,60}", b0, re.M)[:12])
print("B0 son 300:", b0[-300:].replace("\n", " | "))
a = json.loads((D / "anahtar.json").read_text())
kor = (D / "kor.md").read_text(encoding="utf8")
for n in ("2", "3"):
    blok = re.search(rf"^## {n}\..*?(?=^## \d+\.|\Z)", kor, re.S | re.M).group(0)
    x = blok.split("### Y")
    b = x[0] if a[n]["X"] == "B" else x[1]
    print(f"iş {n} B parça {len(b)}kr:", b[:200].replace("\n", " | "))
yasak = pk.kurulu_disi_adlar()
for k in "AB":
    c = Counter(w for p in range(4) for w in yasak if re.search(rf"\b{re.escape(w)}\b", kayit[(k, p)]["metin"].lower()))
    print(k, "kurulu-dışı eşleşme:", c.most_common(12))
