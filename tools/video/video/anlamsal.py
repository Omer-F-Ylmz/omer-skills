"""VİDEO-AKIL-1b-2a DEVAM-1: serbest metin alanlarında anlamsal eşleşme (fastembed çok dilli; salt okur)."""
import json
import sys
from pathlib import Path

import numpy as np

from .tarama import bolum, tablolar

MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"  # ~0,22 GB
ESIK = {"is_akisi": 0.55, "promptlar": 0.527, "site_ui": 0.715, "ogrenimler": 0.514}  # 5 referans videonun (tur-1 yalın raporları) çapraz-video çiftlerinin %99'u: `python -m video.anlamsal <altin_dizin> <rapor_kalibi>`
_model, _onbellek = None, {}


def embed(metinler):
    global _model
    yeni = [t for t in dict.fromkeys(metinler) if t not in _onbellek]
    if yeni:
        _model = _model or __import__("fastembed").TextEmbedding(MODEL)
        for t, v in zip(yeni, _model.embed(yeni)):
            _onbellek[t] = v / np.linalg.norm(v)
    return np.array([_onbellek[t] for t in metinler]).reshape(len(metinler), -1)


def esle(altin, satirlar, esik):
    """Açgözlü bire-bir: tüm çiftler kosinüse göre azalan; iki taraf da boşsa ve kos ≥ eşik ise alınır → [(altın_i, satır_j, kos)]."""
    if not altin or not satirlar:
        return []
    k = embed(altin) @ embed(satirlar).T
    kul_a, kul_s, out = set(), set(), []
    for i, j in sorted(np.ndindex(k.shape), key=lambda p: -k[p]):
        if k[i, j] < esik:
            break
        if i not in kul_a and j not in kul_s:
            kul_a.add(i); kul_s.add(j); out.append((i, j, float(k[i, j])))
    return out


def _satirlar(metin, bas):
    return [s.lstrip("- ").strip() for s in bolum(metin, bas).splitlines() if s.strip() and not s.startswith("|")]


def alanlar(metin, altin):
    """alan → (altın metinleri, rapor satırları)."""
    teknik = [r[0] for h, rows in tablolar(bolum(metin, "Site/UI")) if h and h[0].casefold() == "teknik" for r in rows if r]
    tum = [s.lstrip("- ").strip() for s in metin.splitlines() if s.strip() and not s.startswith("#")]
    return {"is_akisi": ([a["adim"] for a in altin.get("is_akisi", [])], _satirlar(metin, "İş akışı")),
            "promptlar": ([q.get("ozet") or q["konu"] for q in altin.get("promptlar", [])], _satirlar(metin, "Promptlar")),
            "site_ui": ([u["teknik"] for u in altin.get("site_ui", [])], teknik),
            "ogrenimler": ([o["ogrenim"] for o in altin.get("ogrenimler", []) if not o.get("belirsiz")], tum)}


def esikler(videolar, yuzdelik=99):
    """videolar: [(rapor_metni, altın_dict)]. Alan başına: video i altınları × video j≠i rapor satırları kosinüslerinin yüzdeliği."""
    out = {}
    for alan in ESIK:
        k = []
        for i, (_, a) in enumerate(videolar):
            for j, (m, _) in enumerate(videolar):
                ga, rs = alanlar("", a)[alan][0], alanlar(m, {})[alan][1]
                if i != j and ga and rs:
                    k.extend((embed(ga) @ embed(rs).T).ravel())
        out[alan] = round(float(np.percentile(k, yuzdelik)), 3)
    return out


if __name__ == "__main__":  # python -m video.anlamsal <altin_dizin> <rapor_kalibi, {id} yer tutucu>
    d, kalip = Path(sys.argv[1]), sys.argv[2]
    ids = "aZe5ZTYcF1M 1nGx7WR8YLE YDAK1lvVXho FaChtkkG9X4 d_UE-wHLoZY".split()
    print(esikler([(Path(kalip.format(id=i)).read_text(encoding="utf-8"), json.loads((d / f"{i}.json").read_text(encoding="utf-8"))) for i in ids]))
