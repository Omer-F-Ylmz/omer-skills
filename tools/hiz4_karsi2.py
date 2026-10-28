"""VIDEO-HIZ-4 TUR 2 kalite kapısı: düzeltilmiş referansa (ref2 = orijinal ses izi, large-v3 beam5) göre ASR benzerliği, link/komut (ref OCR + ref2 transkript),
OCR geri çağırımı (ham ve kararlı: ≥2 karede geçen ya da link/komut jetonları). Kullanım: hiz4_karsi2.py <koşu adı>"""
import difflib, json, re, sys
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
import video_hiz4_olc as o
import video_derin as vd

D = KOK / ".kos/kopru/ogren/hiz4"
ST = o.dur_sozcukler()
sat = []
for p in sorted((D / sys.argv[1]).glob("*.json")):
    r2p = D / "ref2" / p.name
    if p.name.startswith("_") or not r2p.exists():
        continue
    e, y, r2 = (json.loads(x.read_text(encoding="utf-8")) for x in (o.REF / p.name, p, r2p))
    ke, ky = o.kel(r2), o.kel(y)
    asr = difflib.SequenceMatcher(None, ke, ky, autojunk=False).ratio() if ke or ky else 1.0
    mt = "\n".join(x["t"] for x in e["ekran"]) + "\n" + " ".join(s["t"] for s in r2["transkript"])
    le = {m.strip(".,)") for m in vd.URL_RE.findall(mt)} | {m.strip() for m in vd.KOMUT_RE.findall(mt)}
    ly = set(y["linkler"] + y["komutlar"])
    lk = len(le & ly) / len(le) if le else 1.0
    cnt = Counter(t for x in e["ekran"] for t in set(o.tokens(x["t"])))
    sabit = {t for t, c in cnt.items() if c >= 2} | set(o.tokens(" ".join(le)))
    ref = {t for t in o.tokens(" ".join(x["t"] for x in e["ekran"])) if t not in ST}
    yo = set(o.tokens(" ".join(x["t"] for x in y["ekran"])))
    raw = len(ref & yo) / len(ref) if ref else 1.0
    sb = ref & sabit
    sbr = len(sb & yo) / len(sb) if sb else 1.0
    sat.append((p.stem, asr, lk, raw, sbr, r2.get("dil"), y.get("dil"), sorted(le - ly)[:2]))
    print(f"{p.stem}\tasr {asr:.3f}\tlink {lk:.2f}\tocr_ham {raw:.3f}\tocr_sabit {sbr:.3f}\t{r2.get('dil')}/{y.get('dil')}\t{sat[-1][7]}")
n = max(1, len(sat))
print(f"N={len(sat)} asr_ort {sum(s[1] for s in sat)/n:.3f} asr>=0.96 {sum(s[1]>=.96 for s in sat)}/{len(sat)} asr>=0.9 {sum(s[1]>=.9 for s in sat)}/{len(sat)} link_tam {sum(s[2]>=1 for s in sat)}/{len(sat)} ocr_ham_ort {sum(s[3] for s in sat)/n:.3f} ocr_sabit_ort {sum(s[4] for s in sat)/n:.3f} ocr_sabit>=.98 {sum(s[4]>=.98 for s in sat)}/{len(sat)}")
