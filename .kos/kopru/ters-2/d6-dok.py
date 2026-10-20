"""d6: önbellekten skill/zemin notları + hakem oyları dök (YENİ çağrı yok; eksikse '(önbellekte yok)'). Çıktı: %TEMP%/ters-kapi/d6/<hedef>.txt"""
import hashlib, json, random, sys
from pathlib import Path
sys.path.insert(0, "tools/ters")
import kapi_kos as K

AD = sys.argv[1:] or ["ink-puppet", "Fiyat.Tests", "ortak-js"]
H = {h["ad"]: h for h in json.loads((K.DIZ / "hedefler.json").read_text(encoding="utf-8"))["hedefler"]}
OUT = K.CIKTI / "d6"; OUT.mkdir(exist_ok=True)


def oku(tur, anahtar):
    o = K.CIKTI / "onbellek" / (hashlib.sha1((tur + anahtar).encode()).hexdigest() + ".json")
    return json.loads(o.read_text(encoding="utf-8"))["y"] if o.exists() else None


for ad in AD:
    h = H[ad]; s = [f"# {ad} ({h['tur']}) — sorular: {h['sorular']}", "## referans"] + [f"{i+1}. {m['madde']}" for i, m in enumerate(h["maddeler"])]
    kanit = K.rea_kanit(h); s.append(f"## kanıt uzunluğu {len(kanit)} · ham {len(K.ham(h))}")
    veri = {"zemin": K.ham(h), "skill": K.ham(h) + "\n\n### Kanıt (prob/REA)\n" + kanit}
    for r in K.TEKRAR:
        notlar = {}
        for kol in ("skill", "zemin"):
            ist = (f"{K.SKILL}\n\n" if kol == "skill" else "") + f"Hedef: {h['ad']} ({h['tur']}). Soru: {h['sorular']}\n\nVeri:\n{veri[kol]}\n\n" \
                "Görev: tam 5 mekanizma maddesi yaz. Her madde ayrı satırda JSON: {\"madde\":\"...\",\"dosya\":\"...\",\"alinti\":\"veride birebir geçen en çok 120 karakter\"}. " \
                f"[tekrar {r}] Önce yalnız bu 5 JSON satırı."
            y = oku("yazar", ist); s.append(f"## tekrar {r} {kol}: " + ("(önbellekte yok)" if y is None else ""))
            notlar[kol] = []
            for l in (y or "").splitlines():
                l = l.strip().rstrip(",")
                if l.startswith("{"):
                    try: notlar[kol].append(json.loads(l)); s.append("- " + notlar[kol][-1].get("madde", "")[:300])
                    except ValueError: pass
        rng = random.Random(h["id"] * 10 + r); sira = ["skill", "zemin"]; rng.shuffle(sira)
        gt = "\n".join(f"{i + 1}. {m['madde']}" for i, m in enumerate(h["maddeler"]))
        nt = lambda k: "\n".join(f"- {x.get('madde', '')}" for x in notlar[k])
        ist = (f"Referans mekanizma maddeleri ({h['ad']}):\n{gt}\n\nNot A:\n{nt(sira[0])}\n\nNot B:\n{nt(sira[1])}\n\n"
               "Her not için 5 referans maddesinin her birinin notta (aynı olgu, doğru) verilip verilmediğini 1/0 işaretle. "
               "Yalnız JSON: {\"A\":[5 sayı],\"B\":[5 sayı]}")
        s.append(f"## tekrar {r} hakem (A={sira[0]}, B={sira[1]})")
        for aile in K.YARGIC:
            y = oku("hakem", aile + ist)
            if y: s.append(f"- {aile}: {y.strip()[:160]}")
    (OUT / f"{ad}.txt").write_text("\n".join(s), encoding="utf-8"); print(ad, len(s))
