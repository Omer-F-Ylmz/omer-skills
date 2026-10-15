"""ÖĞREN-1 d13 (Desktop 07:44): ana yol CLAUDE DOĞRUDAN YAZAR (tam kaynak, birebir kanıt); :free taslak yok.
SERT denetim yalnız: alıntı/kanıt birebir · komut birebir (satır ya da ≥8 kr parça) · mekanizma kapalı listede · kaynaksızda hepsi "kaynak yetersiz".
Sahiplik / boş alan / olay adı (gecerli_a'nın geri kalanı) → yazara UYARI, yazar gerekçeyle karar verir.
  python -X utf8 .claude/ogren1/d13.py ornek       → d13-ornek.tsv (d7-aday − önceki tüm örnekler, kaynaklı, seed 10, 28 kalem)
  python -X utf8 .claude/ogren1/d13.py paket       → d13-paket-1..3.md (yazar alt ajanı başına ~10 kalem: kaynak + adlar + başlıklar)
  python -X utf8 .claude/ogren1/d13.py birlestir   → d13-yazar-*.jsonl → ozet-token-d13.jsonl + hakem-d13.jsonl
  python -X utf8 .claude/ogren1/d13.py puan h1 h2  → iki kör hakem: hata + ayrışan (d9.puan)"""
import json, random, sys
from pathlib import Path

import ozet_kaynak
import ozet3
from ozet3 import BASLIK, MEKANIZMA, adlari, bos, gecerli_a, gecerli_b, kaynaksiz, n
from son import oku

B = Path(__file__).parent
O = Path(r"C:\Projeler\omer-skills\.kos\kopru\ogren")
A = ["ne_yapar", "komut", "sinirlar"]


def sert(o, m, adlar):
    """→ (ret nedeni ya da None, uyarı listesi)"""
    if kaynaksiz(adlar, m):
        return gecerli_a(o, m, adlar), []
    al = o.get("alinti") if isinstance(o.get("alinti"), dict) else {}
    kendi = {p + x for x in adlar for p in ("", "/")}
    for a in A:
        if bos(o.get(a, "")):
            continue
        if len(n(al.get(a, ""))) < 10 or n(al[a]) not in n(m):
            return f"{a} alıntısı belgede yok", []
        if a == "komut" and o[a].strip() not in kendi:
            if n(o[a]) not in n(m):
                return "komut belgede birebir değil", []
            if len(n(o[a])) < 8 and n(o[a]) not in {n(x) for x in m.splitlines()}:
                return "komut parçası 8 karakterden kısa", []
    if not gecerli_b(o, m):
        return "mekanizma/kanıt geçersiz", []
    uyari = []
    u = gecerli_a(o, m, adlar, uyari)
    return None, uyari + ([u] if u else [])


def ornek():
    gorulen = set()
    for p in ["d7-ornek.tsv", "d9-ornek-ilk.tsv", "d9-ornek.tsv"]:
        gorulen |= {s.split("\t")[0] for s in (B / p).read_text(encoding="utf-8").splitlines()}
    for p in list(O.glob("ozet-token*.jsonl")) + list(O.glob("hakem-*.jsonl")):
        gorulen |= set(oku(p))
    aday = [s for s in (B / "d7-aday.tsv").read_text(encoding="utf-8").splitlines() if s.split("\t")[0] not in gorulen and "backup" not in s.split("\t")[0]]
    from d9 import acilir
    aday = [s for s in aday if acilir(s.split("\t")[3]) and not kaynaksiz(adlari(s.split("\t")[0], s.split("\t")[3]), ozet_kaynak.metin(s.split("\t")[3]))]
    sec = random.Random(10).sample(aday, 28)
    (B / "d13-ornek.tsv").write_text("".join(s + "\n" for s in sec), encoding="utf-8")
    print(f"aday {len(aday)} (görülen {len(gorulen)} hariç) → d13-ornek.tsv 28: {' · '.join(s.split(chr(9))[0] for s in sec)}")


def D():
    return dict(s.split("\t")[::3] for s in (B / "d13-ornek.tsv").read_text(encoding="utf-8").splitlines())


def paket():
    d = list(D().items())
    for i in range(3):
        parca = []
        for ad, kaynak in d[i::3]:
            m, an = ozet_kaynak.metin(kaynak), sorted(adlari(ad, kaynak))
            parca += [f"## {ad}", f"kaynak: {kaynak} · {len(m.splitlines())} satır · araç adları ({len(an)}): {' · '.join(an[:30])}",
                      "BAŞLIKLAR: " + " · ".join(p.split("\n", 1)[0].strip()[:60] for p in BASLIK.split(m)[1:])[:1500], ""]
        (B / f"d13-paket-{i + 1}.md").write_text("\n".join(parca), encoding="utf-8")
        print(f"d13-paket-{i + 1}.md · kalem {len(d[i::3])}")


def birlestir():
    c = {}
    for p in sorted(B.glob("d13-yazar-*.jsonl")):
        c.update(oku(p))
    son, ret = {}, {}
    for ad, kaynak in D().items():
        if ad not in c:
            ret[ad] = "yazar satırı yok"
            continue
        m, y = ozet_kaynak.metin(kaynak), c[ad]
        r = {"ad": ad, "kaynak": kaynak, **{a: y[a]["deger"] for a in A}, "alinti": {a: y[a].get("alinti", "") for a in A},
             "mekanizma": y["mekanizma"], "kanit": y.get("kanit", ""), "dogrulandi": "claude-yazar"}
        neden, r["uyari"] = sert(r, m, adlari(ad, kaynak))
        if neden:
            ret[ad] = neden
        son[ad] = r
    for ad, h in ret.items():
        print("RET", ad, h, sep="\t")
    for ad, r in son.items():
        for u in r["uyari"]:
            print("UYARI", ad, u, sep="\t")
    (O / "ozet-token-d13.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in son.values()), encoding="utf-8")
    (O / "hakem-d13.jsonl").write_text("".join(json.dumps({k: r[k] for k in ["ad", "kaynak"] + A + ["mekanizma"]}, ensure_ascii=False) + "\n"
                                               for r in son.values()), encoding="utf-8")
    print(f"son {len(son)} · RET {len(ret)} · UYARI {sum(len(r['uyari']) for r in son.values())}")


if __name__ == "__main__":
    k = sys.argv[1:]
    if k[0] != "ornek":
        ozet_kaynak.D = D()
    if k[0] == "puan":
        from d9 import puan
        puan(*k[1:3])
    else:
        {"ornek": ornek, "paket": paket, "birlestir": birlestir}[k[0]]()
