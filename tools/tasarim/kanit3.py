"""TASARIM-3 (4) kanıt: 4 site görevi × 2 tekrar × (taban = main frontend-craft / vitrin = + references/vitrin-teknikleri.md).
    python tools/tasarim/kanit3.py <cikti_dizini> --kol taban|vitrin [--kuru]
Kol başına 8 claude -p (sonnet, plan limiti; anahtar alt sürece verilmez), kol tavanı $3.5; Σ 16 + kör yargı 4 = 20 çağrı.
Taban = `git archive main` kopyası (.claude/fc-taban3), vitrin = wt'deki frontend-craft.
"""
import os
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import kanit  # noqa: E402

kanit.BRIEF = {**kanit.BRIEF,
               "saas": "Geliştiriciler için log izleme aracı 'İz' tanıtım sayfası: hero, 3 özellik, entegrasyonlar, fiyat, CTA, footer.",
               "etkinlik": "İstanbul'da 3 günlük elektronik müzik festivali 'Dalga 26' sitesi: hero, sanatçı kadrosu, program, bilet, konum."}
TABAN = kanit.WT / ".claude/fc-taban3/plugins/frontend-craft/skills/frontend-craft"
kanit.KOLLAR = {"taban": TABAN, "vitrin": kanit.KOLLAR["yeni"], "yeni": kanit.KOLLAR["yeni"]}  # "yeni" = ölçüm betikleri (slop/audit)


def main(argv):
    kol = argv[argv.index("--kol") + 1]
    kok = pathlib.Path(argv[0]).resolve()
    kanit.PORT = {"taban": 3931, "vitrin": 3932}[kol]  # iki kol olcum_sira'da paralel
    plan = [(b, t) for t in (1, 2) for b in kanit.BRIEF if not (kok / f"{b}-{kol}-{t}" / "index.html").exists()]  # devam: üretilmiş koşu tekrarlanmaz
    if "--kuru" in argv:
        print(len(plan), "çağrı:", plan, "port", kanit.PORT, "sistem uzunluğu", len(kanit.sistem(kol)))
        return 0
    kok.mkdir(parents=True, exist_ok=True)
    os.environ["FC_GECMIS"] = str(kok / f"gecmis-{kol}.tsv")
    tsv, toplam = kok / f"kanit-{kol}.tsv", 0.0
    if not tsv.exists():
        tsv.write_text("kol\tbrief\ttekrar\tbayrak_n\tbayraklar\taudit\tbayt\tusd\ttur\tgirdi\tcikti\n", encoding="utf-8")
    for b, t in plan:
        if toplam >= 3.5:
            print("TAVAN", toplam, flush=True)
            break
        t0 = time.time()
        satir = kanit.kos(kol, b, t, kok)
        toplam += float(satir[7])
        with tsv.open("a", encoding="utf-8") as f:
            f.write("\t".join(map(str, satir)) + "\n")
        print(kol, b, t, "bayrak", satir[3], "usd", satir[7], f"{time.time() - t0:.0f}s", flush=True)
    print("BITTI toplam_usd", round(toplam, 2), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
