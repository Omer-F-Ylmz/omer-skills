"""TOKEN-REA d13 UZUN bağlam devir A/B: görev başına ~150k tahmini bağlam (60+ dosya Read); B ~115k eşiğinde devir notu → taze oturum.
d12 ile aynı kos/kalite/topla (devir_ab.py); fark: dosya sayısı bağlam tahminiyle seçilir, tur tavanı yüksek, claude -p tavanı 8 (2 eşli görev = 6 çağrı).
Kapı: B ağırlıklı ≤ %70 x A VE B kalite ≥ A kalite. Bağlam boyu vekili: cacheCreation toplamı (oturumun kurduğu bağlam).
Kullanım: python -I devir_ab2.py [tohum] [--kuru]   → devir_ab2_<tohum>.json"""
import json, random, subprocess, sys
from pathlib import Path
import devir_ab as d

TOPLAM_TAHMIN, ESIK_TAHMIN, GOREV2 = 150_000, 115_000, 2
d.CAGRI_TAVAN, d.MAKS_TUR = 8, "150"


def tahmin(m):  # Read çıktısı: satır numarası öneki dahil kaba jeton; shortcut: tokenizer yok, gerçek boy cacheCreation'dan okunur
    return len(m) // 3.5 + 2 * len(m.splitlines())


def gorevler2(tohum):
    adaylar = []
    for y in subprocess.run(["git", "ls-files", "*.py"], cwd=d.KOK, capture_output=True, text=True, encoding="utf-8").stdout.split():
        try:
            m = (d.KOK / y).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if 100 <= len(m.splitlines()) <= 290 and "devir_ab" not in y:
            adaylar.append((y, m))
    random.Random(tohum).shuffle(adaylar)
    out, i = [], 0
    for g in range(GOREV2):
        anahtar, toplam, k = [], 0, None
        while toplam < TOPLAM_TAHMIN:
            y, m = adaylar[i]; i += 1
            dn = d.re.findall(r"(?m)^\s*(?:async\s+)?def\s+(\w+)", m)
            anahtar.append((y, len(dn), dn[-1] if dn else "-"))
            toplam += tahmin(m)
            if k is None and toplam >= ESIK_TAHMIN:
                k = len(anahtar)
        out.append((f"g{g + 1}", anahtar, k, int(toplam)))
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    tohum = next((a for a in sys.argv[1:] if not a.startswith("--")), "20102303")
    gs = gorevler2(tohum)
    if "--kuru" in sys.argv:
        for ad, an, k, t in gs:
            print(ad, "dosya", len(an), "devir_k", k, "tahmin_jeton", t)
        sys.exit()
    cikti = Path(__file__).with_name(f"devir_ab2_{tohum}.json")
    d.NOT_DIZIN.mkdir(exist_ok=True)
    sonuc = []
    for ad, anahtar, k, t in gs:
        temel = d.GOREV_METNI.format(liste=d.istem_liste(anahtar))
        a = d.kos(temel)
        yol = (d.NOT_DIZIN / f"{tohum}-{ad}.md").relative_to(d.KOK).as_posix()
        (d.KOK / yol).unlink(missing_ok=True)
        b1 = d.kos(temel + d.DEVIR_METNI.format(k=k, yol=yol))
        not_var = (d.KOK / yol).exists() and "DEVIR-HAZIR" in b1["yanit"]
        b2 = d.kos(d.DEVAM_METNI.format(yol=yol)) if not_var else None
        b = d.topla([b1, b2] if b2 else [b1])
        sonuc.append(dict(gorev=ad, dosya=len(anahtar), devir_k=k, tahmin=t,
                          A=dict(d.topla([a]), kalite=d.kalite(a["yanit"], anahtar)),
                          B=dict(b, kalite=d.kalite(b2["yanit"], anahtar) if b2 else 0.0, not_var=not_var, cagri=2 if b2 else 1),
                          A_yanit=a["yanit"][-400:], B_yanit=(b2 or b1)["yanit"][-400:]))
        cikti.write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
        print(ad, "A", sonuc[-1]["A"], "B", sonuc[-1]["B"], flush=True)
    top = {x: {s: sum(r[x][s] for r in sonuc) for s in ("girdi", "agirlikli", "tur", "sn", "usd")} for x in "AB"}
    kal = {x: round(sum(r[x]["kalite"] for r in sonuc) / len(sonuc), 3) for x in "AB"}
    oran = round(top["B"]["agirlikli"] / top["A"]["agirlikli"], 3)
    print("A", top["A"], kal["A"]); print("B", top["B"], kal["B"])
    print("ORAN_B/A", oran, "KAPI", "GEÇTİ" if oran <= .7 and kal["B"] >= kal["A"] else "GEÇMEDİ")
