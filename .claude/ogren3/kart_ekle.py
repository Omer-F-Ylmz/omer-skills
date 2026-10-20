"""ozet-ajan-o3.jsonl (A, sert denetimden geçmiş) → docs/atlas/kart.jsonl A katmanı (G3 A şeması: ne · ne_zaman · nasil · kosul · kanit · tur · kategori · katman).
Aynı (ad, katman A) varsa eklenmez; dosyaya bayt olarak eklenir (write_text CRLF yapar)."""
import json
from pathlib import Path

K = Path(r"C:\Projeler\omer-skills\docs\atlas\kart.jsonl")
O = Path(r"C:\Projeler\omer-skills\.kos\kopru\ogren")


def satirlar():
    kat = {r["id"]: r["kategori_son"] for r in map(json.loads, (O / "katalog-son.jsonl").read_text(encoding="utf-8").splitlines())}
    for r in map(json.loads, (O / "ozet-ajan-o3.jsonl").read_text(encoding="utf-8").splitlines()):
        rol = [r["mekanizma"]] if isinstance(r["mekanizma"], str) else r["mekanizma"]
        yield {"ad": r["ad"], "ne": r["ne_yapar"], "ne_zaman": f"{r['ne_zaman']} Sınır: {r['sinirlar']}", "nasil": r["komut"], "kosul": ", ".join(rol),
               "kanit": r["ozgun"], "tur": r["tur"], "kategori": kat.get(r["id"], "ajan-orkestrasyon"), "katman": "A"}


if __name__ == "__main__":
    var = {(r["ad"], r.get("kategori")) for r in map(json.loads, K.read_text(encoding="utf-8").splitlines()) if r.get("katman") == "A"}
    yeni = [r for r in satirlar() if (r["ad"], r["kategori"]) not in var]
    K.open("ab").write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in yeni).encode("utf-8"))
    print(f"eklendi {len(yeni)} · zaten vardı {sum(1 for _ in satirlar()) - len(yeni)}")
