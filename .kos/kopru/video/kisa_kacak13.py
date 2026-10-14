"""d13: sınama kaçaklarının nerede kaybolduğu (paket / aday / gemini izle / metin geçişi). Ağ yok."""
import json
from pathlib import Path
from video import kisa, tarama as tr

ONB = Path(r"C:\Projeler\.video-cache")
KACAN = {"ig-DYKSh1iv8nP": [".TECH", "Sales Navigator"], "ig-DeXK9x7jQfb": ["Bytebase", "Go", "RustFS", "S3"],
         "ig-DcDfnzsM2wL": ["Claude", "GitHub", "agenthubstack.dev"]}
for v, adlar in KACAN.items():
    d = ONB / v
    paket = tr.normal((d / "paket.md").read_text(encoding="utf-8"))
    aday = {tr.normal(a["ad"]) for a in kisa.sozluk_tara(d, {})}
    g = json.loads((d / "gemini.json").read_text(encoding="utf-8")) if (d / "gemini.json").is_file() else {}
    gs = tr.normal(json.dumps(g, ensure_ascii=False))
    ga = {tr.normal(a["ad"]) for a in g.get("araclar", [])}
    m = json.loads((d / "gemini-metin.json").read_text(encoding="utf-8")) if (d / "gemini-metin.json").is_file() else {}
    ma = {tr.normal(a) for a in m.get("adlar", [])}
    print(v, "aday_say", len(aday), "metin_ad", len(ma))
    for a in adlar:
        n = tr.normal(a)
        print(f"  {a:18} paket={n in paket} aday={n in aday} izle_ad={n in ga} izle_metin={n in gs} metin_ad={n in ma}")
