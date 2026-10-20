"""ozet-g1.jsonl (A, sert denetimden geçmiş) → docs/atlas/kart.jsonl A katmanı (ogren3/kart_ekle.py şeması). Aynı (ad, kategori, A) varsa satır yerinde değişir, yoksa eklenir; bayt olarak yazar (CRLF yok)."""
import json
from pathlib import Path

K = Path(r"C:\Projeler\omer-skills\docs\atlas\kart.jsonl")
O = Path(r"C:\Projeler\omer-skills\.kos\kopru\ogren")


def satirlar():
    kat = {r["ad"]: r["kategori_son"] for r in map(json.loads, (O / "katalog-son.jsonl").read_text(encoding="utf-8").splitlines())}
    for r in map(json.loads, (O / "ozet-g1.jsonl").read_text(encoding="utf-8").splitlines()):
        rol = [r["mekanizma"]] if isinstance(r["mekanizma"], str) else r["mekanizma"]
        yield {"ad": r["ad"], "ne": r["ne_yapar"], "ne_zaman": f"{r['ne_zaman']} Sınır: {r['sinirlar']}", "nasil": r["komut"], "kosul": ", ".join(rol),
               "kanit": r["ozgun"], "tur": "", "kategori": kat.get(r["ad"], "frontend-tasarım"), "katman": "A"}


if __name__ == "__main__":
    yeni = {(r["ad"], r["kategori"]): r for r in satirlar()}
    cikti, degisen = [], 0
    for l in K.read_bytes().decode("utf-8").split("\n"):
        r = json.loads(l) if l.strip() else None
        k = (r["ad"], r.get("kategori")) if r and r.get("katman") == "A" else None
        if k in yeni:
            cikti.append(json.dumps(yeni.pop(k), ensure_ascii=False))
            degisen += 1
        elif l.strip():
            cikti.append(l)
    cikti += [json.dumps(r, ensure_ascii=False) for r in yeni.values()]
    K.write_bytes(("\n".join(cikti) + "\n").encode("utf-8"))
    print(f"değişen {degisen} · eklenen {len(yeni)} · toplam satır {len(cikti)}")
