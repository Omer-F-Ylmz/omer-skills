import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
k = Path(__file__).resolve().parent / "ajan-sira"
liste = Path(__file__).resolve().parent / "sonuc_kisa.txt"
adlar = sys.argv[1:] or [s.strip() for s in liste.read_text(encoding="utf-8").split() if s.strip()]
for ad in adlar:
    adaylar = sorted([p for p in k.glob(f"{ad}*.json") if p.stem.count(".") == 0], key=lambda p: p.stat().st_mtime)
    if not adaylar:
        print(f"== {ad}: SONUÇ YOK")
        continue
    p = adaylar[-1]
    try:
        d, _ = json.JSONDecoder().raw_decode(p.read_text(encoding="utf-8", errors="replace").lstrip())  # RAM-BEKCI-3c: sonuna yapışan hook hata metni ("Extra data") yok sayılır
    except Exception as e:
        print(f"== {p.stem}: okunamadı {e}")
        continue
    r = (d.get("result") or "").strip()
    print(f"== {p.stem} · ${d.get('total_cost_usd', 0):.2f} · {d.get('num_turns')} tur · {d.get('subtype')}")
    print(r[:900])
    print()
