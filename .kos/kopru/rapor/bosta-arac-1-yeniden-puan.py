import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
import ucretsiz_havuz as h

RAPOR = Path(__file__).resolve().parent
ornek = {l.split("\t")[0]: ["", *l.split("\t")] for l in (RAPOR / "bosta-arac-1-ornek40.tsv").read_text(encoding="utf-8").splitlines()}
satirlar = [s.split("\t") for s in (RAPOR / "bosta-arac-1-satirlar.tsv").read_text(encoding="utf-8").splitlines()]
hedef = ["27", "28", "29", "36"]
rows = []
for n in hedef:
    kat, ad = ornek[n][2], ornek[n][3]
    yeni = next((p for p in satirlar if len(p) >= 3 and p[0] == kat and p[1] == ad), None)
    rows.append({"no": n, "kategori": kat, "ad": ad, "oneri": yeni[2] if yeni else "BULUNAMADI"})
print("\n".join(f'{r["no"]}\t{r["kategori"]}\t{r["ad"]}\t{r["oneri"]}' for r in rows))
kalem = "\n".join(f'{r["no"]}. [{r["kategori"]}] {r["ad"]} :: {r["oneri"]}' for r in rows)
istem = (
    "Aşağıda kurulu bir araç (skill/plugin/MCP) ve ona önerilen kullanım işi var. "
    "Her satır için: öneri bu aracın gerçek işine uyuyor mu? DOĞRU veya YANLIŞ yaz. "
    "Yalnız JSON dizisi döndür: [{\"no\": \"1\", \"karar\": \"DOGRU\"|\"YANLIS\"}, ...]. Başka metin yazma.\n\n" + kalem
)
metin, saglayici, log = h.cagir("orta", istem, max_tokens=1500, etiket="bosta-yeniden-puan", zaman=120)
print("saglayici:", saglayici, "log:", log)
if not metin:
    sys.exit("hakem yanıtsız")
arr = json.loads(re.search(r"\[.*\]", metin, re.S).group(0))
print("ucretsiz_karar:", {str(x["no"]): x["karar"] for x in arr})
