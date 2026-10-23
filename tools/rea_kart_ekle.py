"""KAYNAK-SITE-3 adim 3: docs/site-inceleme/rea/*.json teknik cikarimini ilgili kartin sonuna 'REA teknik' bolumu olarak ekler (kart yoksa kisa kart acar). Yeniden calistirilabilir (varsa atlar)."""
import json, re
from pathlib import Path
KOK = Path(__file__).resolve().parents[1]
KART = KOK / "docs/site-inceleme/kart"
n = yeni = 0
for f in sorted((KOK / "docs/site-inceleme/rea").glob("*.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    k = KART / (d["site"] + ".md")
    blok = "\n## REA teknik (inspect_web_page, 29 Eki degil 23 Eki 2026)\n- DOM %d dugum, %d script, canvas=%d\n- Algilanan altyapi: %s\n- Kanit: docs/site-inceleme/rea/%s.json\n" % (
        d["dom"], d["scripts"], d["canvas"], ", ".join(d["vendor"]) or "belirgin kutuphane yok (paketlenmis/ozel)", d["site"])
    blok = blok.replace("29 Eki degil 23 Eki 2026", "23 Eki 2026")
    if k.exists():
        t = k.read_text(encoding="utf-8")
        if "## REA teknik" in t:
            continue
        k.write_text(t.rstrip("\n") + "\n" + blok, encoding="utf-8"); n += 1
    else:
        k.write_text("---\nsite: https://%s\nkaynak: rea\n---\n# %s\n%s" % (d["site"], d["site"], blok), encoding="utf-8"); yeni += 1
print("kart guncel", n, "yeni kart", yeni)
