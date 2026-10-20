"""Bağlam diyeti kalite A/B: claude-mem SessionStart enjeksiyonu 15 ↔ 6 gözlem (+ 6 gözlem + tek mem-search).
Soru seti BETİKLE üretilir (tohumlu; geliştiren oturum içeriği okumaz, yalnız sayı basılır). Kesme anındaki son N başlık = bağlam;
soru hedefi hedef rütbeden (1-6: iki kolda da bağlamda · 7-15: yalnız 15 kolunda). Yanıtlayıcı ücretsiz havuz, anahtar eşleşmesi betikle.
  python baglam_kalite.py uret <tohum> → heldout/baglam_<tohum>.json + .lock
  python baglam_kalite.py skor <tohum> → baglam_kalite_<tohum>.json (çağrı ≈ 1 + 3×soru)"""
import hashlib, json, random, re, sqlite3, sys
from pathlib import Path

BU = Path(__file__).parent
KOK = BU.parents[2]
HO = BU / "heldout"
DB = Path.home() / ".claude-mem" / "claude-mem.db"
PROJE, N_SORU = "omer-skills", 10
sys.path.insert(0, str(KOK / "tools"))


def gozlemler():
    c = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
    return c.execute("select id,type,title,narrative from observations where project=? and title is not null "
                     "order by created_at_epoch,id", (PROJE,)).fetchall()


def baglam(g, kesme, n):  # enjeksiyon biçimi: "ID TİP BAŞLIK", en yeni en altta
    return "\n".join(f"{i} {t} {b}" for i, t, b, _ in g[kesme - n:kesme])


def jeton(s):
    return round(len(s) / 3.5)  # her iki kolda aynı kaba ölçer; oran anlamlı


def uret(tohum):
    import ucretsiz_havuz as H
    g, rng = gozlemler(), random.Random(f"baglam-{tohum}")
    hedefler = []
    while len(hedefler) < N_SORU:
        k = len(hedefler)
        kesme = rng.randrange(max(40, len(g) - 1500), len(g) + 1)  # son ~1500 gözlem
        rutbe = rng.randint(1, 6) if k < N_SORU // 2 else rng.randint(7, 15)
        i, t, b, nar = g[kesme - rutbe]
        if len(b) < 25 or not nar or any(h["id"] == i for h in hedefler):
            continue
        hedefler.append(dict(kesme=kesme, rutbe=rutbe, id=i, baslik=b, anlati=(nar or "")[:500]))
    ist = ("Her numaralı olay için, o olaydan haberi olan birine sorulacak TEK Türkçe soru (en çok 20 sözcük) ve cevabı bu BAŞLIKTA bulunan "
           "KISA cevap anahtarı (1-4 özgün sözcük) yaz. Olayın başlığını soruya kopyalama. Biçim: her satır `soru ||| anahtar`, numarasız, aynı sırada.\n"
           + "\n".join(f"{n + 1}. BAŞLIK: {h['baslik']} | AYRINTI: {h['anlati']}" for n, h in enumerate(hedefler)))
    y, kaynak, _ = H.cagir("ozet", ist, max_tokens=2500, etiket="heldout-baglam",
                           dogrula=lambda m: None if len([l for l in m.splitlines() if "|||" in l]) == len(hedefler) else "satır sayısı")
    if not y:
        sys.exit("havuz yok")
    for h, l in zip(hedefler, [l for l in y.splitlines() if "|||" in l]):
        p = [x.strip() for x in l.split("|||") if x.strip()]
        h["soru"], h["anahtar"] = p[0].lstrip("0123456789.) `"), p[-1].strip("` ")
    HO.mkdir(exist_ok=True)
    ham = json.dumps(hedefler, ensure_ascii=False)
    (HO / f"baglam_{tohum}.json").write_text(ham, encoding="utf-8")
    (HO / f"baglam_{tohum}.lock").write_text(hashlib.sha256(ham.encode()).hexdigest(), encoding="utf-8")
    print("baglam", tohum, "n", len(hedefler), "kaynak", kaynak)


def kelimeler(s):
    return {w for w in re.findall(r"\w+", s.lower()) if len(w) >= 4}


def ara(g, kesme, soru, k=3):  # tek mem-search benzeri: soru sözcükleriyle başlık+anlatı örtüşmesi, kesmeden önceki gözlemler
    q = kelimeler(soru)
    s = sorted(g[:kesme], key=lambda r: -len(q & kelimeler(f"{r[2]} {r[3] or ''}")))[:k]
    return "\n".join(f"{i} {t} {b}" for i, t, b, _ in s)


def dogru(yanit, anahtar):
    a = kelimeler(anahtar) or {anahtar.lower()}
    return int(bool(yanit) and "yok" != yanit.strip().lower().strip(".") and len(a & kelimeler(yanit)) >= max(1, round(0.6 * len(a))))


def skor(tohum):
    import ucretsiz_havuz as H
    ham = (HO / f"baglam_{tohum}.json").read_text(encoding="utf-8")
    assert hashlib.sha256(ham.encode()).hexdigest() == (HO / f"baglam_{tohum}.lock").read_text(), "kilit bozuk"
    g, sonuc = gozlemler(), []
    def sor(ctx, soru):
        y, _, _ = H.cagir("ozet", f"Önceki oturumlardan kalan not başlıkları:\n{ctx}\n\nSoru: {soru}\nYalnız bu başlıklardan yanıtla, kısa yaz; başlıklarda yoksa tam olarak YOK yaz.",
                          max_tokens=200, etiket="baglam-skor")
        return y or ""
    for h in json.loads(ham):
        c15, c6 = baglam(g, h["kesme"], 15), baglam(g, h["kesme"], 6)
        y15, y6 = sor(c15, h["soru"]), sor(c6, h["soru"])
        ek = "" if dogru(y6, h["anahtar"]) else ara(g, h["kesme"], h["soru"])
        y6s = y6 if not ek else sor(c6 + "\n" + ek, h["soru"])
        sonuc.append(dict(rutbe=h["rutbe"], d15=dogru(y15, h["anahtar"]), d6=dogru(y6, h["anahtar"]), d6s=dogru(y6s, h["anahtar"]),
                          j15=jeton(c15), j6=jeton(c6), j6s=jeton(c6 + "\n" + ek)))
    ort = lambda a, k: round(sum(r[k] for r in a) / max(1, len(a)), 2)
    ozet = {}
    for ad, a in (("hepsi", sonuc), ("rutbe1-6", [r for r in sonuc if r["rutbe"] <= 6]), ("rutbe7-15", [r for r in sonuc if r["rutbe"] > 6])):
        ozet[ad] = dict(n=len(a), **{k: ort(a, k) for k in ("d15", "d6", "d6s", "j15", "j6", "j6s")})
    (BU / f"baglam_kalite_{tohum}.json").write_text(json.dumps(dict(ozet=ozet, satirlar=sonuc), ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(ozet, ensure_ascii=False))


def kapsam(*tohumlar):  # havuzsuz, gürültüsüz üst sınır: anahtar sözcükleri bağlamda var mı (yanıtlayıcı hatası dışarıda)
    g, ort, satir = gozlemler(), {}, []
    for t in tohumlar:
        for h in json.loads((HO / f"baglam_{t}.json").read_text(encoding="utf-8")):
            a = kelimeler(h["anahtar"]) or {h["anahtar"].lower()}
            var = lambda c: int(len(a & kelimeler(c)) >= max(1, round(0.6 * len(a))))
            c6 = baglam(g, h["kesme"], 6)
            c6s = c6 + "\n" + ara(g, h["kesme"], h.get("soru") or h["anahtar"])
            satir.append((h["rutbe"] > 6, var(baglam(g, h["kesme"], 15)), var(c6), var(c6s), jeton(c6) if var(c6) else jeton(c6s)))
    for ad, f in (("hepsi", lambda r: True), ("rutbe1-6", lambda r: not r[0]), ("rutbe7-15", lambda r: r[0])):
        a = [r for r in satir if f(r)]
        ort[ad] = dict(n=len(a), kap15=round(sum(r[1] for r in a) / len(a), 2), kap6=round(sum(r[2] for r in a) / len(a), 2),
                       kap6_arama=round(sum(r[3] for r in a) / len(a), 2), j6_arama_ort=round(sum(r[4] for r in a) / len(a)))
    print(json.dumps(ort, ensure_ascii=False))


if __name__ == "__main__":
    if sys.argv[1] == "kapsam": kapsam(*sys.argv[2:]); sys.exit()
    {"uret": uret, "skor": skor}[sys.argv[1]](sys.argv[2])
