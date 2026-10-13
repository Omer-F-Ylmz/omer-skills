"""TASARIM-2 (3) kanıt: 2 brief × 4 koşu × (frontend-craft 1.6.0 / 1.7.0 yakınsama kırıcı) — yakınsama düşmeli, slop 0 kalmalı.
    python tools/tasarim/kanit2.py <cikti_dizini> --kol 160|170 [--kuru]
1.6.0'ın 1-2. koşuları TASARIM-1 'yeni' kolundan (aynı skill, .kos/kopru/tasarim-kanit/*-yeni-*), burada yalnız 3-4: 4 çağrı.
1.7.0: 8 çağrı sırayla, brief'ler iç içe (gerçek kullanım: proje proje), ortak geçmiş FC_GECMIS=<cikti>/gecmis-170.tsv (boş başlar).
171 = 1.7.0 + web fontu kuralı (kör yargıda 170 portfolyo 6.0 < 160 7.25), 8 çağrı $2.5.
Toplam 12 claude -p (≤20); kol tavanı 160 $2, 170 $3.5 (Σ ≤ $5.5, kör yargı için $0.5 kalır).
"""
import os
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import kanit  # noqa: E402

FC160 = kanit.WT / ".claude/fc160/plugins/frontend-craft/skills/frontend-craft"  # git archive b212787
kanit.KOLLAR = {"160": FC160, "170": kanit.KOLLAR["yeni"], "171": kanit.KOLLAR["yeni"], "yeni": kanit.KOLLAR["yeni"]}  # "yeni" = ölçüm betikleri (slop/audit)


def main(argv):
    kol = argv[argv.index("--kol") + 1]
    kok = pathlib.Path(argv[0]).resolve()
    kanit.PORT = {"160": 3919, "170": 3920, "171": 3921}[kol]  # iki kol olcum_sira'da paralel
    tavan = {"160": 2.0, "170": 3.5, "171": 2.5}[kol]
    plan = [(b, t) for t in ((3, 4) if kol == "160" else (1, 2, 3, 4)) for b in kanit.BRIEF
            if not (kok / f"{b}-{kol}-{t}" / "index.html").exists()]  # devam: üretilmiş koşu tekrarlanmaz
    if "--kuru" in argv:
        print(len(plan), "çağrı:", plan, "port", kanit.PORT, "sistem uzunluğu", len(kanit.sistem(kol)))
        return 0
    kok.mkdir(parents=True, exist_ok=True)
    os.environ["FC_GECMIS"] = str(kok / f"gecmis-{kol}.tsv")
    tsv, toplam = kok / f"kanit-{kol}.tsv", 0.0
    if not tsv.exists():
        tsv.write_text("kol\tbrief\ttekrar\tbayrak_n\tbayraklar\taudit\tbayt\tusd\ttur\tgirdi\tcikti\n", encoding="utf-8")
    for b, t in plan:
        if toplam >= tavan:
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
