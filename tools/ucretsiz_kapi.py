"""UCRETSIZ-HAVUZ-1 kapısı: eski zincir (video764_kos'un eski sabit sırası) vs ücretsiz havuz; 3 iş profili (özet · hakem · yazım).
python tools/ucretsiz_kapi.py [N_OZET=20 N_HAKEM=10 N_YAZIM=10]  → .kos/kopru/ucretsiz/kapi.json + özet satırları.
Kabul: başarı ≥%98 · sağlayıcı payı ≤%50 · Haiku ≤%5 · hakem doğruluğu eski zincirden düşük değil. Dış çağrı tavanı DIS_TAVAN (aşılırsa durur)."""
import json, re, sys, time
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
import ucretsiz_havuz as H  # noqa: E402

DIS_TAVAN = 105
SAY = Counter()  # kol -> dış çağrı


def tavan():
    if sum(SAY.values()) >= DIS_TAVAN:
        raise SystemExit(f"dış çağrı tavanı {DIS_TAVAN}")


def eski_modul():
    """Eski zincir parçaları (post/haiku/modeller/gecerli/KAPALI) video764_kos'ta duruyor; sıralı deneme eski_zincir'de yeniden kurulur."""
    sys.path.insert(0, str(KOK / ".kos/kopru"))
    import video764_kos
    return video764_kos


E = eski_modul()
KOL = ["eski"]
_post, _haiku = E.post, E.haiku
E.post = lambda *a, **k: (tavan(), SAY.update([KOL[0]]), _post(*a, **k))[2]
E.haiku = lambda i: (SAY.update([KOL[0]]), _haiku(i))[1]
_istek = H._istek
H._istek = lambda *a, **k: (tavan(), SAY.update([KOL[0]]), _istek(*a, **k))[2]
E.HAIKU_TAVAN = 3


def eski_zincir(zincir, istem, dogrula):
    """Eski sıra: sabit sırayla dene, hata alan halka 30 dk kapalı, son halka Haiku. (metin|None, kaynak)"""
    for ad, m in zincir:
        if E.KAPALI.get((ad, m), 0) > time.time():
            continue
        try:
            if ad == "gemini":
                o = E.post(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key=" + __import__("os").environ["GEMINI_API_KEY"],
                           {"contents": [{"parts": [{"text": istem}]}], "generationConfig": {"maxOutputTokens": 1500}}, {})["candidates"][0]["content"]["parts"][0]["text"]
            elif ad == "haiku":
                o = E.haiku(istem)[0]
            else:
                url, key = (("https://api.groq.com/openai/v1/chat/completions", "GROQ_API_KEY") if ad == "groq" else
                            ("https://openrouter.ai/api/v1/chat/completions", "OPENROUTER_API_KEY"))
                o = E.post(url, {"model": m, "max_tokens": 1500, "reasoning_effort": "low", "messages": [{"role": "user", "content": istem}]},
                           {"Authorization": "Bearer " + __import__("os").environ[key]})["choices"][0]["message"]["content"]
            o = (o or "").strip()
            if o and not dogrula(o):
                return o, ad
        except SystemExit:
            raise
        except Exception:
            if ad != "haiku":
                E.KAPALI[(ad, m)] = time.time() + 1800
    return None, None


def sec01(y):
    return None if re.search(r"[01]", y) else "okunamadı"


def yaz_gecerli(kavram):
    return lambda y: None if kavram.lower() in y.lower() and len(re.findall(r"[.!?](\s|$)", y)) >= 2 and 60 <= len(y) <= 700 and re.search(r"[şğıçöü]", y) else "geçersiz"


def koş():
    O = Path(r"C:\Projeler\.video764")
    n_o, n_h, n_y = (list(map(int, sys.argv[1:4])) + [20, 10, 10][len(sys.argv) - 1:])[:3] if len(sys.argv) > 1 else (20, 10, 10)
    girdiler = [g.read_text(encoding="utf-8") for g in sorted(O.glob("*.girdi.txt"))][:n_o]
    sor = [json.loads(s) for s in (KOK / ".claude/beyin4/sorular-2011.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()][:n_h]
    kav = ["token önbelleği", "rate limit", "round-robin", "regresyon testi", "idempotent işlem", "dairesel bağımlılık", "cache invalidation",
           "feature flag", "backoff", "hash tablosu"][:n_y]
    zincir = E.modeller()
    ozet_ist = lambda g: E.ISTEM + "\n\n" + g  # noqa: E731
    baslik = lambda g: re.search(r"BAŞLIK: (.*)", g).group(1) if "BAŞLIK:" in g else ""  # noqa: E731
    fam = lambda a: [z for z in zincir if z[0] in a]  # noqa: E731
    hk = lambda q, i: (f"Soru: {q['soru']}\nReferans: {q['cevap']}\nAday: {(q if i % 2 == 0 else sor[(i + 1) % len(sor)])['cevap']}\n"
                      "Aday, referanstaki olguyu doğru veriyor mu? Yalnız tek rakam yaz: 1 (evet) ya da 0 (hayır).")
    sonuc = {}
    for kol in ("eski", "havuz"):
        KOL[0] = kol; r = {"ozet": [], "hakem": [], "yazim": [], "kaynak": Counter(), "gecikme": []}
        for g in girdiler:
            t = time.time()
            if kol == "eski":
                y, k = eski_zincir(zincir, ozet_ist(g), lambda o: E.gecerli(o, g, baslik(g)))
            else:
                y, k, _ = H.cagir("ozet", ozet_ist(g), max_tokens=1500, haiku_tavan=2, etiket="kapi", dogrula=lambda o: E.gecerli(o, g, baslik(g)))
            r["ozet"].append(bool(y)); r["kaynak"][(k or "yok").split("/")[0]] += 1; r["gecikme"].append(time.time() - t)
        for i, q in enumerate(sor):
            t = time.time(); dogru = 1 if i % 2 == 0 else 0; oy = []
            if kol == "eski":
                for aile in (fam(("openrouter",)), fam(("groq", "haiku"))):
                    y, k = eski_zincir(aile, hk(q, i), sec01)
                    oy.append(int(re.search(r"[01]", y).group()) if y else None); r["kaynak"][(k or "yok").split("/")[0]] += 1
            else:
                for y, k, _ in H.iki_aile("hakem", hk(q, i), max_tokens=300, dogrula=sec01, haiku_tavan=0):
                    oy.append(int(re.search(r"[01]", y).group())); r["kaynak"][k.split("/")[0]] += 1
                oy += [None] * (2 - len(oy))
            r["hakem"].append({"oy": oy, "dogru": dogru}); r["gecikme"].append(time.time() - t)
        for kv in kav:
            t = time.time(); ist = f"'{kv}' kavramını Türkçe, 2-3 cümleyle açıkla; '{kv}' ifadesi aynen geçsin."
            if kol == "eski":
                y, k = eski_zincir(zincir, ist, yaz_gecerli(kv))
            else:
                y, k, _ = H.cagir("yazim", ist, max_tokens=1000, haiku_tavan=2, etiket="kapi", dogrula=yaz_gecerli(kv))
            r["yazim"].append(bool(y)); r["kaynak"][(k or "yok").split("/")[0]] += 1; r["gecikme"].append(time.time() - t)
        sonuc[kol] = r
    ozetle(sonuc)


def ozetle(sonuc):
    cikti = {}
    for kol, r in sonuc.items():
        hk = [o for h in r["hakem"] for o in h["oy"]]; dogru = [o == h["dogru"] for h in r["hakem"] for o in h["oy"]]
        n = len(r["ozet"]) + len(r["hakem"]) * 2 + len(r["yazim"])
        basari = sum(r["ozet"]) + sum(o is not None for o in hk) + sum(r["yazim"])
        uyum = [h["oy"][0] == h["oy"][1] for h in r["hakem"] if None not in h["oy"]]
        kay = {k: v for k, v in r["kaynak"].items() if k != "yok"}
        cikti[kol] = {"basari": f"{basari}/{n}", "basari_yuzde": round(100 * basari / n, 1), "ort_gecikme_sn": round(sum(r["gecikme"]) / len(r["gecikme"]), 1),
                      "dis_cagri": SAY[kol], "kaynak": dict(r["kaynak"]), "en_buyuk_pay_yuzde": round(100 * max(kay.values()) / sum(kay.values()), 1) if kay else 0,
                      "haiku_yuzde": round(100 * kay.get("haiku", 0) / n, 1), "hakem_dogruluk": f"{sum(dogru)}/{len(dogru)}",
                      "hakem_aile_uyumu": f"{sum(uyum)}/{len(uyum)}"}
    (H.DIZIN / "kapi.json").write_text(json.dumps(cikti, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(cikti, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    koş()
