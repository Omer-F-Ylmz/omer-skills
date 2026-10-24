"""SKILL-MODE Faz 1: her-sey-ara — tek dizin, karma arama (BM25 + çok dilli yoğun vektör, RRF birleştirme).
python her_sey_ara.py dizin            -> dizin kur (bm25.pkl + vek.npy)
python her_sey_ara.py olc              -> tetik.jsonl ile recall @5/20/40/80 (bm25 / yogun / karma)
python her_sey_ara.py ara "<iş>" [N]   -> ilk N (vars. 40) ad · tür · iş
M1 tembel şema: yalnız ad+tür+kısa iş döner; tam şema istenince okunur. M3 sözcük skoru = BM25 (katalog_ara ile aynı).
"""
import json, math, pickle, sys, time
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
KOK = Path(r"C:\Projeler\omer-skills")
sys.path.insert(0, str(KOK / "tools"))
import katalog_ara as ka  # noqa: E402

D = Path(__file__).resolve().parent
KAT = D / "yetenek-tam.jsonl"
MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
RRF_K = 60
yukle = lambda p: [json.loads(s) for s in p.read_text(encoding="utf-8").splitlines() if s.strip()]


def belge_metin(o):
    return f"{o['ad']} · {o.get('is', '')} · {o.get('tetik', '')} · {str(o.get('metin', ''))[:400]}"


def dizin():
    rows = yukle(KAT)
    docs = [ka.kelimeler(o["ad"]) * 2 + ka.kelimeler(f"{o.get('is', '')} {o.get('tetik', '') or ka.tetik(o.get('metin', ''))} {o.get('metin', '')}") for o in rows]
    tf = [Counter(d) for d in docs]
    df = Counter(w for d in docs for w in set(d))
    ln = [len(d) for d in docs]
    pickle.dump({"rows": rows, "tf": tf, "df": df, "ln": ln}, open(D / "bm25.pkl", "wb"))
    print("bm25 tamam", len(rows), flush=True)
    import numpy as np
    from fastembed import TextEmbedding
    m = TextEmbedding(MODEL, threads=4)
    t = time.time()
    v = np.array(list(m.embed([belge_metin(o) for o in rows], batch_size=64)), dtype="float32")
    v /= np.linalg.norm(v, axis=1, keepdims=True) + 1e-9
    np.save(D / "vek.npy", v)
    print("vek tamam", v.shape, f"{time.time() - t:.0f}s", flush=True)


class Arayici:
    def __init__(self, yogun=True):
        b = pickle.load(open(D / "bm25.pkl", "rb"))
        self.rows, self.tf, self.df, self.ln = b["rows"], b["tf"], b["df"], b["ln"]
        self.N, self.ort = len(self.rows), sum(self.ln) / len(self.ln)
        self.inv = {}
        for i, t in enumerate(self.tf):
            for w in t:
                self.inv.setdefault(w, []).append(i)
        self.m = self.v = None
        if yogun and (D / "vek.npy").exists():
            import numpy as np
            from fastembed import TextEmbedding
            self.np, self.v = np, np.load(D / "vek.npy")
            self.m = TextEmbedding(MODEL, threads=4)

    def bm25(self, q):
        s = Counter()
        for w, qn in ka.genislet(q).items():
            if w in ka.DURAK or w not in self.inv:
                continue
            idf = math.log(1 + (self.N - self.df[w] + 0.5) / (self.df[w] + 0.5))
            for i in self.inv[w]:
                f = self.tf[i][w]
                s[i] += qn * idf * f * 2.2 / (f + 1.2 * (0.25 + 0.75 * self.ln[i] / self.ort))
        for i in list(s):
            if "kapal" in str(self.rows[i].get("durum", "")):
                s[i] *= 0.5
        return [i for i, _ in s.most_common(400)]

    def etiketle(self, yol):
        """M3 üçüncü kol: etiket/eşanlam kaydı (ad|imza → 'tr/en anahtar sözcükler'), yoksa yalnız ad+açıklama."""
        et = json.loads(yol.read_text(encoding="utf-8")) if yol.exists() else {}
        self.sad, self.sdf = [], Counter()
        for o in self.rows:
            ad = set(ka.kelimeler(o["ad"]))
            tg = set(ka.kelimeler(et.get(f"{o['ad']}|{o.get('imza', '')}", "")))
            ac = set(ka.kelimeler(f"{o.get('is', '')} {o.get('tetik', '')}"))
            self.sad.append((ad, tg, ac))
            self.sdf.update(ad | tg | ac)

    def soz3(self, q, n=400):
        """Sözcük skoru: ad×2 + etiket×1 + açıklama×1, idf ağırlıklı (BM25'ten bağımsız kol)."""
        sor = [w for w in ka.genislet(q) if w not in ka.DURAK and w in self.sdf]
        agir = {w: math.log(1 + self.N / self.sdf[w]) for w in sor}
        s = {}
        for i, (ad, tg, ac) in enumerate(self.sad):
            v = sum(agir[w] * (2 * (w in ad) + (w in tg) + (w in ac)) for w in sor)
            if v:
                s[i] = v * (0.5 if "kapal" in str(self.rows[i].get("durum", "")) else 1)
        return sorted(s, key=s.get, reverse=True)[:n]

    def yogun(self, q, n=400):
        if self.m is None:
            return []
        e = self.np.array(list(self.m.embed([q])), dtype="float32")[0]
        e /= self.np.linalg.norm(e) + 1e-9
        sk = self.v @ e
        return list(self.np.argsort(-sk)[:n])

    def karma(self, q, n=80, en=""):
        """en = sorgu_cevir.cevir çıktısı (İngilizce yeniden yazım | anahtarlar); etiketle() çağrıldıysa soz3 kolu da girer (SKILL-MODE-2: ayar %99.4 / test %100 @80)."""
        r = Counter()
        kol = [self.bm25(q), self.yogun(q)]
        if en:
            kol += [self.bm25(en), self.yogun(en)]
        if getattr(self, "sad", None):
            kol += [self.soz3(q)] + ([self.soz3(en)] if en else [])
        for liste in kol:
            for k, i in enumerate(liste):
                r[i] += 1 / (RRF_K + k + 1)
        return [i for i, _ in r.most_common(n)]


def olc():
    a = Arayici()
    tet = yukle(D / "tetik.jsonl")
    K = (5, 20, 40, 80)
    sonuc = {}
    t0 = time.time()
    for t in tet:
        h = t["ad"].lower()
        for q in t["sorgular"]:
            bm, yo = a.bm25(q), a.yogun(q)
            r = Counter()
            for liste in (bm, yo):
                for k, i in enumerate(liste):
                    r[i] += 1 / (RRF_K + k + 1)
            for yol, liste in (("bm25", bm), ("yogun", yo), ("karma", [i for i, _ in r.most_common(80)])):
                adlar = [a.rows[i]["ad"].lower() for i in liste[:80]]
                s = sonuc.setdefault((yol, "yeni" if t["ek"] else "eski"), {"n": 0, **{k: 0 for k in K}})
                s["n"] += 1
                sira = adlar.index(h) + 1 if h in adlar else None
                for k in K:
                    s[k] += bool(sira and sira <= k)
    for (yol, g), s in sorted(sonuc.items()):
        print(f"{yol:6} {g:5} n={s['n']} " + " ".join(f"@{k}=%{100 * s[k] / s['n']:.1f}" for k in K))
    print(f"süre {time.time() - t0:.0f}s")
    (D / "recall-karma.json").write_text(json.dumps({f"{a_}|{b}": v for (a_, b), v in sonuc.items()}, indent=1), encoding="utf-8")


if __name__ == "__main__":
    k = sys.argv[1] if len(sys.argv) > 1 else "olc"
    if k == "dizin":
        dizin()
    elif k == "olc":
        olc()
    else:
        a = Arayici()
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 40
        for i in a.karma(sys.argv[2], n):
            o = a.rows[i]
            print(f"{o['ad']} · {o['tur']} · {str(o.get('is') or o.get('metin'))[:90]}")
