"""d10 kuru doğrulama: REA kanıtı (11 kod hedefi... 8 kod + 3 site), site kare düzlüğü. Yazar/hakem çağrısı yok."""
import json, sys
from pathlib import Path

sys.path.insert(0, "C:/Projeler/omer-skills/tools/ters")
import kapi_kos as k

H = json.loads(Path("C:/Projeler/omer-skills/.kos/kopru/ters-2/hedef-d9.json").read_text(encoding="utf-8"))["hedefler"]
print("RAM", k.ram())
print("rea", k.rea_yol())
for h in (x for x in H if x["tur"] != "site"):
    try:
        print(h["ad"], "REA", len(k.rea_kanit(h)), "bayt")
    except Exception as e:
        print(h["ad"], "REA HATA", type(e).__name__, str(e)[:100])
port = k.sunucu("skills")
for h in (x for x in H if x["tur"] == "site"):
    d = Path("C:/Projeler/omer-skills/.kos/kopru/ters-2/d10-probe") / h["ad"]
    d.mkdir(parents=True, exist_ok=True)
    try:
        kanit = json.dumps(k.probe(f"http://127.0.0.1:{port}{h['sayfa']}", d / "orijinal"), ensure_ascii=False)
        print(h["ad"], "probe", len(kanit), "geçerli kareler", k.gecerli_kareler(d / "orijinal"))
    except Exception as e:
        print(h["ad"], "PROBE HATA", type(e).__name__, str(e)[:120])
