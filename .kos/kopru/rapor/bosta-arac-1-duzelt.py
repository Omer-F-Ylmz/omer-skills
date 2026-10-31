import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
import ucretsiz_havuz as h

RAPOR = Path(__file__).resolve().parent
ornek = {l.split("\t")[0]: ["", *l.split("\t")] for l in (RAPOR / "bosta-arac-1-ornek40.tsv").read_text(encoding="utf-8").splitlines()}
hedef = ["27", "28", "29", "36"]  # iki hakemin işaretlediği satırların birleşimi
satirlar = (RAPOR / "bosta-arac-1-satirlar.tsv").read_text(encoding="utf-8").splitlines()
istem = (
    "Aşağıdaki her kurulu araç için, o aracın gerçek işine uyan TEK satır kullanım önerisi yaz (Türkçe, ≤20 kelime). "
    "Yalnız JSON dizisi döndür: [{\"no\": \"...\", \"oneri\": \"...\"}].\n\n"
    + "\n".join(f'{n}. [{ornek[n][2]}] {ornek[n][3]} :: {ornek[n][4]}' for n in hedef)
)
metin, saglayici, log = h.cagir("orta", istem, max_tokens=2000, etiket="bosta-duzelt", zaman=120)
print("saglayici:", saglayici, "log:", log)
if not metin:
    sys.exit("yanıt yok")
arr = json.loads(re.search(r"\[.*\]", metin, re.S).group(0))
yeni = {str(x["no"]): x["oneri"] for x in arr}
degisen = 0
for n in hedef:
    if n not in yeni:
        continue
    kat, ad = ornek[n][2], ornek[n][3]
    for i, s in enumerate(satirlar):
        p = s.split("\t")
        if len(p) >= 3 and p[0] == kat and p[1] == ad:
            p = [kat, ad, yeni[n].replace("\t", " ")]
            satirlar[i] = "\t".join(p)
            degisen += 1
            break
(RAPOR / "bosta-arac-1-satirlar.tsv").write_text("\n".join(satirlar) + "\n", encoding="utf-8")
print("degisen satir:", degisen, "/", len(hedef))
