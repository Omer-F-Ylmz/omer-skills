import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
import ucretsiz_havuz as h

RAPOR = Path(__file__).resolve().parent
rows = []
for line in (RAPOR / "bosta-arac-1-ornek40.tsv").read_text(encoding="utf-8").splitlines():
    p = line.split("\t")
    rows.append({"no": p[0], "kategori": p[1], "ad": p[2], "oneri": p[3]})
kalem = "\n".join(f'{r["no"]}. [{r["kategori"]}] {r["ad"]} :: {r["oneri"]}' for r in rows)
istem = (
    "Aşağıda kurulu bir araç (skill/plugin/MCP) ve ona önerilen kullanım işi var. "
    "Her satır için: öneri bu aracın gerçek işine uyuyor mu? DOĞRU veya YANLIŞ yaz. "
    "Yalnız JSON dizisi döndür: [{\"no\": \"1\", \"karar\": \"DOGRU\"|\"YANLIS\"}, ...]. Başka metin yazma.\n\n" + kalem
)
metin, saglayici, log = h.cagir("orta", istem, max_tokens=3000, etiket="bosta-hakem2", zaman=120)
print("saglayici:", saglayici, "log:", log)
if not metin:
    sys.exit("hakem yanıtsız")
arr = json.loads(re.search(r"\[.*\]", metin, re.S).group(0))
karar = {str(x["no"]): x["karar"] for x in arr}
dogru = sum(1 for r in rows if karar.get(r["no"]) == "DOGRU")
print(f"DOGRU {dogru}/{len(rows)} = {dogru/len(rows)*100:.1f}%")
for r in rows:
    if karar.get(r["no"]) != "DOGRU":
        print("YANLIS/EKSIK", r["no"], r["ad"])
(RAPOR / "bosta-arac-1-hakem2-serbest.json").write_text(json.dumps(arr, ensure_ascii=False, indent=1), encoding="utf-8")
