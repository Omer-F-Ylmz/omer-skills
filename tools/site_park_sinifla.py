"""YARIM-D3 1a: 'diger' kalan siteleri icerikteki park/satilik/erisim-engeli/arsiv izinden 'kapali/park' turune cevirir (yeniden calistirilabilir)."""
import json, re, sys
from pathlib import Path

CIK = Path(__file__).resolve().parents[1] / ".kos/kopru/ara/site-sinif"
IZ = re.compile(r"domain|alan ad|parked|park edil|parklan|for sale|satil|satis|sat[ıi]ş|acquisition|access denied|eri[sş]im engel|erisme engel|"
                r"wayback|internet archive|ar[sş]iv|expired|godaddy|hosting|buy this|sale|blocked|under construction|coming soon|içerik yok|icerik yok|"
                r"hicbir hizmet|hiçbir hizmet|no content", re.I)
n = d = 0
for f in sorted(CIK.glob("*.json")):
    j = json.loads(f.read_text(encoding="utf-8"))
    if j.get("tur") != "diger":
        continue
    d += 1
    metin =" ".join([j.get("sunar") or "", (j.get("metin3") or "")[:600]])
    if not (j.get("metin3") and len(j["metin3"]) > 80) or IZ.search(metin):
        j["tur"] = "kapali/park"
        f.write_text(json.dumps(j, ensure_ascii=False), encoding="utf-8")
        n += 1
print("diger", d, "-> kapali/park", n)
