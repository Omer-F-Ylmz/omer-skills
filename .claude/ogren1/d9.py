"""ÖĞREN-1 d9 (Desktop 05:08): A alanları :free taslak + CLAUDE DOĞRULAYICI (pencereli bağlam) · mekanizma her kalemde Claude ·
:free gölge doğrulayıcı (kapıda rolü yok) · d7 geliştirme kontrolü · seed 9 görülmemiş örneklem kapısı.
  python -X utf8 .claude/ogren1/d9.py ornek            → d9-ornek.tsv (d7-aday − önceki tüm örnekler, seed 9, 28 kalem)
  python -X utf8 .claude/ogren1/d9.py doldur           → d11: kaynaksız kalemler çıkar, seed-9 dizisinin sıradaki kaynaklıları (d9-yeni.txt)
  python -X utf8 .claude/ogren1/d9.py d9 paket         → d9-paket.md (doğrulayıcı girdisi: iddia + alıntı ±25 satır + UYARI + başlıklar + anahtar satırlar)
  python -X utf8 .claude/ogren1/d9.py d9 birlestir     → d9-dogrulayici.jsonl gecerli_a/gecerli_b'den geçer → ozet-token-d9-dogrulanmis.jsonl + hakem-d9.jsonl
  python -X utf8 .claude/ogren1/d9.py d9 golge         → Groq gpt-oss-120b aynı paketle doğrular → d9-golge.jsonl + Claude'la uyum
  python -X utf8 .claude/ogren1/d9.py d7 kontrol       → d8'in 11 ortak hatasından kaçını yakaladı
  python -X utf8 .claude/ogren1/d9.py d9 puan h1 h2    → iki kör hakem: hata + ayrışan"""
import bisect, json, random, re, sys, time
from pathlib import Path

import ozet_kaynak
import ozet3
from ozet3 import BASLIK, UYARI, adlari, gecerli_a, gecerli_b, n
from son import oku

B = Path(__file__).parent
O = Path(r"C:\Projeler\omer-skills\.kos\kopru\ogren")
A = ["ne_yapar", "komut", "sinirlar"]
TASLAK = {"d7": O / "ozet-token-d7-son.jsonl", "d9": O / "ozet-token-d9.jsonl"}  # d7: d8 sonucu (13 hata) taslak sayılır


def ornek():
    gorulen = {s.split("\t")[0] for s in (B / "d7-ornek.tsv").read_text(encoding="utf-8").splitlines()}
    for p in O.glob("ozet-token*.jsonl"):
        gorulen |= set(oku(p))
    aday = [s for s in (B / "d7-aday.tsv").read_text(encoding="utf-8").splitlines() if s.split("\t")[0] not in gorulen and "backup" not in s.split("\t")[0]]  # d7 gibi yedek kopyalar hariç
    aday = [s for s in aday if acilir(s.split("\t")[3])]  # d7 örneklemi gibi: kaynağı açılan; claudeai_adlar.json belge değil, ad listesi
    sec = random.Random(9).sample(aday, 28)
    (B / "d9-ornek.tsv").write_text("".join(s + "\n" for s in sec), encoding="utf-8")
    print(f"aday {len(aday)} (görülen {len(gorulen)} hariç) → d9-ornek.tsv 28")


def doldur():
    """d11 (c): kaynaksız (yalnız aday satırı) kalemler örneklemden çıkar → aynı seed-9 dizisinin sıradaki kaynaklı kalemleri.
    d9 çekimi anındaki görülen kümesi: sonradan yazılan d9 / d7-dogrulanmis dosyaları hariç; ilk 28 d9-ornek-ilk.tsv ile aynı olmalı"""
    ilk = (B / "d9-ornek-ilk.tsv").read_text(encoding="utf-8").splitlines()
    gorulen = {s.split("\t")[0] for s in (B / "d7-ornek.tsv").read_text(encoding="utf-8").splitlines()}
    for p in O.glob("ozet-token*.jsonl"):
        if not p.name.startswith(("ozet-token-d9", "ozet-token-d7-dogrulanmis")):
            gorulen |= set(oku(p))
    aday = [s for s in (B / "d7-aday.tsv").read_text(encoding="utf-8").splitlines() if s.split("\t")[0] not in gorulen and "backup" not in s.split("\t")[0]]
    aday = [s for s in aday if acilir(s.split("\t")[3])]
    dizi = random.Random(9).sample(aday, len(aday))  # pool yöntemi: sample(aday, 28) bu dizinin ilk 28'i
    assert dizi[:28] == ilk, "seed-9 dizisi d9 çekimini üretmiyor"
    def ks(s):
        ad, k = s.split("\t")[0], s.split("\t")[3]
        return ozet3.kaynaksiz(adlari(ad, k), ozet_kaynak.metin(k))
    yeni = [s for s in dizi[28:] if not ks(s)][:sum(map(ks, ilk))]
    son = [s for s in ilk if not ks(s)] + yeni
    (B / "d9-ornek.tsv").write_text("".join(s + "\n" for s in son), encoding="utf-8")
    (B / "d9-yeni.txt").write_text("".join(s.split("\t")[0] + "\n" for s in yeni), encoding="utf-8")
    print(f"aday {len(aday)} · çıkan {sum(map(ks, ilk))} · eklenen {len(yeni)}: {' · '.join(s.split(chr(9))[0] for s in yeni)}")


def acilir(k):
    try:
        return "claudeai_adlar.json" not in k and bool(ozet_kaynak.metin(k).strip())
    except Exception:
        return False


def D(o):
    return dict(s.split("\t")[::3] for s in (B / f"{o}-ornek.tsv").read_text(encoding="utf-8").splitlines())


def pencere(r, m):
    """iddia başına alıntının ±25 satırı + tüm UYARI satırları + iddia/komut anahtar sözcüklerinin geçtiği satırlar (satır no'lu)"""
    L = m.splitlines()
    bas, tum = [], ""
    for x in L:  # n(m) == satır satır n()'lerin " " ile birleşimi → ofset → satır no
        bas.append(len(tum))
        tum += n(x) + " " if n(x) else ""
    sec = {i for i, x in enumerate(L) if UYARI.search(x)}
    anahtar = set()
    for a in A:
        al = n((r.get("alinti") or {}).get(a, ""))
        k = tum.find(al) if len(al) >= 10 else -1
        if k >= 0:
            i = bisect.bisect_right(bas, k) - 1
            sec |= set(range(max(0, i - 25), min(len(L), i + 26)))
        if not ozet3.bos(r.get(a, "")):
            anahtar |= {w.lower() for w in re.findall(r"[A-Za-z][\w./-]{4,}", str(r.get(a, "")))}
    # shortcut: anahtar satırları 60 ile sınırlı (genel sözcük binlerce satır getirebilir); doğrulayıcı "yetmedi" derse kaynak açılır
    sec |= set([i for i, x in enumerate(L) if any(w in x.lower() for w in anahtar)][:60])
    cikti, onceki = [], -2
    for i in sorted(sec):
        if i != onceki + 1:
            cikti.append("…")
        cikti.append(f"{i + 1}: {L[i][:300]}")
        onceki = i
    return cikti


def paket(o):
    d, t = D(o), oku(TASLAK[o])
    parca = []
    for ad, kaynak in d.items():
        m, r = ozet_kaynak.metin(kaynak), t.get(ad, {})
        al = r.get("alinti") or {}
        parca += [f"## {ad}", f"kaynak: {kaynak} · araç adları: {' · '.join(sorted(adlari(ad, kaynak)))} · {len(m.splitlines())} satır",
                  "TASLAK YOK — tüm alanları kaynaktan sen yaz (kaynağı parçalı Read ile oku)" if ad not in t else "İDDİALAR:"]
        parca += [f"- {a}: {r[a]}\n  alıntı: {al.get(a, '')}" for a in A if ad in t]
        parca += ["BAŞLIKLAR: " + " · ".join(p.split("\n", 1)[0].strip()[:60] for p in BASLIK.split(m)[1:]), "SATIRLAR:"] + pencere(r, m) + [""]
    (B / f"{o}-paket.md").write_text("\n".join(parca), encoding="utf-8")
    print(f"{o}-paket.md · kalem {len(d)} · taslaklı {sum(ad in t for ad in d)} · {sum(map(len, parca))} karakter "
          f"(kaynakların tamamı {sum(len(ozet_kaynak.metin(k)) for k in d.values())})")


def birlestir(o):
    d, t, c = D(o), oku(TASLAK[o]), oku(B / f"{o}-dogrulayici.jsonl")
    son, ret, duz = {}, {}, []
    for ad, kaynak in d.items():
        m = ozet_kaynak.metin(kaynak)
        r = dict(t.get(ad, {}), ad=ad, kaynak=kaynak)
        r["alinti"] = dict(r.get("alinti") or {})
        if ad not in c:
            ret[ad] = "doğrulayıcı satırı yok"
            continue
        for a in A:
            if c[ad][a]["karar"] == "Y" or ad not in t:
                r[a], r["alinti"][a] = c[ad][a]["deger"], c[ad][a].get("alinti", "")
                duz.append((ad, a))
        r.update(mekanizma=c[ad]["mekanizma"], kanit=c[ad]["kanit"], cekismeli=False, dogrulandi="claude", uyari=[])
        neden = gecerli_a(r, m, adlari(ad, kaynak), r["uyari"]) or (None if ozet3.kaynaksiz(adlari(ad, kaynak), m) or gecerli_b(r, m)
                                                                    else "mekanizma/kanıt geçersiz")
        if neden:
            ret[ad] = neden
        son[ad] = r
    for ad, h in ret.items():
        print("RET", ad, h, sep="\t")
    for ad, r in son.items():
        for u in r["uyari"]:
            print("UYARI", ad, u, sep="\t")
    (O / f"ozet-token-{o}-dogrulanmis.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in son.values()), encoding="utf-8")
    if o == "d9":
        (O / "hakem-d9.jsonl").write_text("".join(json.dumps({k: r[k] for k in ["ad", "kaynak"] + A + ["mekanizma"]}, ensure_ascii=False) + "\n"
                                                  for r in son.values()), encoding="utf-8")
    cf = len(duz) + len(son)  # düzeltilen/yazılan A alanları + her kalemin mekanizması
    print(f"son {len(son)} · RET {len(ret)} · düzeltilen A alanı {len(duz)} · Claude alan {cf}/{len(son) * 4} = %{100 * cf / max(len(son), 1) / 4:.1f}")
    return duz


GOLGE_ISTEM = ("Sen bir doğrulayıcısın. Aşağıda bir aracın özet iddiaları ve kaynak belgesinden seçilmiş satırlar var. Her alan (ne_yapar, komut, "
               "sinirlar) için karar ver: D = iddia kaynakça destekleniyor, çelişen satır yok, komut aracın KENDİ komutu, sinirlar kaynakta uyarı "
               "varken 'belirsiz' değil; aksi Y. YALNIZ şu JSON'u döndür: "
               '{"ne_yapar":{"karar":"D|Y"},"komut":{"karar":"D|Y"},"sinirlar":{"karar":"D|Y"}}\n---\n')


def golge(o):
    """Desktop (3): kapıda rolü yok; yalnız Claude doğrulayıcıyla alan uyumu ölçülür (god mode girdisi)"""
    ozet3.TAVAN = 60
    bloklar = {b.split("\n", 1)[0]: b for b in ("\n" + (B / f"{o}-paket.md").read_text(encoding="utf-8")).split("\n## ")[1:]}
    c, g = oku(B / f"{o}-dogrulayici.jsonl"), oku(B / f"{o}-golge.jsonl")
    for ad, blok in bloklar.items():
        if ad in g or "TASLAK YOK" in blok:
            continue
        for kol, model in [("groq", "openai/gpt-oss-120b"), ("omni", "openrouter/nvidia/nemotron-3-ultra-550b-a55b:free")]:
            try:
                y = ozet3.sor(kol, model, GOLGE_ISTEM + "## " + blok)
                assert all(y[a]["karar"] in "DY" for a in A)
            except AssertionError:
                if ozet3.CAGRI >= ozet3.TAVAN:
                    sys.exit("TAVAN")
                continue
            except Exception as e:
                print(ad, model, "HATA", type(e).__name__, str(e)[:80], flush=True)
                time.sleep(20)  # Groq TPM
                continue
            with (B / f"{o}-golge.jsonl").open("a", encoding="utf-8") as f:
                f.write(json.dumps(dict(y, ad=ad, model=model), ensure_ascii=False) + "\n")
            g[ad] = y
            break
    ortak = [(ad, a) for ad in g if ad in c for a in A]
    uy = sum(g[ad][a]["karar"] == c[ad][a]["karar"] for ad, a in ortak)
    yy = sum(g[ad][a]["karar"] == c[ad][a]["karar"] == "Y" for ad, a in ortak)
    print(f"gölge {len(g)} kalem · uyum {uy}/{len(ortak)} = %{100 * uy / max(len(ortak), 1):.1f} · "
          f"Claude Y {sum(c[ad][a]['karar'] == 'Y' for ad, a in ortak)} · gölge Y {sum(g[ad][a]['karar'] == 'Y' for ad, a in ortak)} · ikisi Y {yy}")


def kontrol():
    """Desktop (4): d8 iki hakemin ortak Y'leri (11) yeni hatta yakalanmalı; mekanizma: Claude'un seçimi eskisinden farklıysa yakalandı"""
    from d8 import karar
    h1, h2 = karar(B / "d8-h1.jsonl"), karar(B / "d8-h2.jsonl")
    hata = sorted(k for k in h1 if h1[k] == h2[k] == "Y")
    c, t = oku(B / "d7-dogrulayici.jsonl"), oku(TASLAK["d7"])
    for ad, a in hata:
        ok = sorted(c[ad]["mekanizma"]) != sorted(t[ad]["mekanizma"]) if a == "mekanizma" else c[ad][a]["karar"] == "Y"
        print("YAKALADI" if ok else "KAÇTI", ad, a, sep="\t")
    yanlis = [(ad, a) for ad in c for a in A if c[ad][a]["karar"] == "Y" and (ad, a) not in hata]
    print(f"ortak hata {len(hata)} · yakalanan {sum(1 for ad, a in hata if (sorted(c[ad]['mekanizma']) != sorted(t[ad]['mekanizma']) if a == 'mekanizma' else c[ad][a]['karar'] == 'Y'))} · "
          f"hakemlerin D dediği alanda Y (yanlış alarm/kapsam) {len(yanlis)}: {yanlis}")


def puan(h1p, h2p):
    from d8 import karar
    h1, h2 = karar(h1p), karar(h2p)
    assert h1.keys() == h2.keys() and len(h1) == 28 * 4, f"alan sayısı: {len(h1)} / {len(h2)}"
    ayri = sorted(k for k in h1 if h1[k] != h2[k])
    print(f"alan {len(h1)} · hakem1 Y {sum(x == 'Y' for x in h1.values())} · hakem2 Y {sum(x == 'Y' for x in h2.values())} · ayrışan {len(ayri)}")
    for ad, a in ayri:
        print("AYRI", ad, a, h1[ad, a], h2[ad, a], sep="\t")


if __name__ == "__main__":
    k = sys.argv[1:]
    if k == ["ornek"]:
        ornek()
    elif k == ["doldur"]:
        doldur()
    else:
        ozet_kaynak.D = D(k[0])
        {"paket": lambda: paket(k[0]), "birlestir": lambda: birlestir(k[0]), "golge": lambda: golge(k[0]),
         "kontrol": kontrol, "puan": lambda: puan(*k[2:4])}[k[1]]()
