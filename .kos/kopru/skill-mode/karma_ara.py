"""SKILL-MODE-3: katalog_ara / zorunlu_arac için karma arama girişi. ara(q, n) -> yetenek-tam satırları (sıralı).
Sorgu ücretsiz havuzla İngilizceye çevrilir (önbellek sorgu-cevir.json; çeviri kosinüsü <0.5 ise bir kez daha çevrilir, yine kötüyse atılır);
havuz kapalıysa çevirisiz karma (bm25 + yoğun + soz3) çalışır. Dizin/vektör yoksa ya da yüklenemezse None döner (çağıran BM25'e düşer)."""
import json, sys
from pathlib import Path

D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))
_a = None


def _arayici():
    global _a
    if _a is None:
        import her_sey_ara as h
        _a = h.Arayici()
        _a.etiketle(D / "etiket.json")
    return _a


def _cos(a, x, y):
    v = a.np.array(list(a.m.embed([x, y])), dtype="float32")
    return float(v[0] @ v[1] / (a.np.linalg.norm(v[0]) * a.np.linalg.norm(v[1]) + 1e-9))


def cevir(a, q):
    """Önbellekten ya da havuzdan EN yeniden yazım; kayan çeviri '' döner."""
    import sorgu_cevir as sc
    ob = json.loads(sc.CIK.read_text(encoding="utf-8")) if sc.CIK.exists() else {}
    for deneme in range(2):
        if q not in ob:
            ob = sc.cevir([q], ob)
            if q in ob:
                sc.CIK.write_text(json.dumps(ob, ensure_ascii=False, indent=0), encoding="utf-8")
        if q not in ob:
            return ""
        if _cos(a, q, ob[q].split("|")[0]) >= 0.5:
            return ob[q]
        ob.pop(q)
    return ""


def ara(q, n=80, cevirli=True):
    try:
        a = _arayici()
        en = cevir(a, q) if cevirli else ""
    except Exception:
        try:
            en = ""
            a = _arayici()
        except Exception:
            return None
    return [a.rows[i] for i in a.karma(q, n, en)]


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for o in ara(" ".join(sys.argv[1:])) or []:
        print(o["ad"], "·", o["tur"])
