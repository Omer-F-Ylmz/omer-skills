"""ENVANTER-3 onay betiği — Desktop koşar (Ömer onayından sonra). CC: skills/plan-kur + skills/yetenek-getir (öğrenim
kataloğu içinde) ~/.claude/skills/'e kurulur; global ~/.claude/CLAUDE.md'ye tek KOŞULLU satır eklenir. Eskiler
~/.claude/skills-yedek-envanter3/'e yedeklenir. claude.ai: dist/envanter-3/ altına iki zip (zip_denetle'den geçer) + LISTE.md
(--kuru da üretir; repo içi, canlıya dokunmaz). Settings, plugin dosyaları, ajanlar değişmez.

  python onay/envanter_3_uygula.py --kuru   # plan (varsayılan): dist zip'leri + kurulacaklar + satır jetonu; canlıya yazmaz
  python onay/envanter_3_uygula.py uygula   # yedekle + kur + CLAUDE.md satırı + kayıp denetimi
  python onay/envanter_3_uygula.py --geri   # kurulanı kaldır, yedekleri (skill + CLAUDE.md) geri koy"""
import filecmp, shutil, sys, zipfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools" / "skill-paket"))
import zip_denetle  # noqa: E402

ADLAR = ("plan-kur", "yetenek-getir")
SATIR = ("- Hard/multi-domain work (2+ domains, out of domain, tool name unknown): first Skill plan-kur, ONE call "
         "(it includes yetenek-getir); routine single-domain work: no catalog call.")
TAVAN = 1300  # global CLAUDE.md jeton tavanı


def jeton(metin):
    # shortcut: ~3.5 karakter/jeton tahmini (TR+EN karışık); kesin sayım gerekirse count_tokens API'si
    return round(len(metin) / 3.5)


def zip_yaz(d, dist):
    zp = dist / f"{d.name}.zip"
    dosyalar = sorted(p for p in d.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for p in dosyalar:
            z.write(p, f"{d.name}/{p.relative_to(d).as_posix()}")
    return zp, len(dosyalar)


def paketle(dist):
    dist.mkdir(parents=True, exist_ok=True)
    liste = ["# ENVANTER-3 claude.ai zip'leri (Settings → Capabilities → Skills → yükle; aynı adlı eskisinin yerine)", ""]
    for ad in ADLAR:
        zp, n = zip_yaz(KOK / "skills" / ad, dist)
        sorun = zip_denetle.denetle(zp)
        assert not sorun, f"{zp.name}: {sorun}"
        assert len(zipfile.ZipFile(zp).namelist()) == n, f"{zp.name}: zip kaybı"
        liste.append(f"- {zp.name} · {n} dosya · {zp.stat().st_size // 1024} KB")
    (dist / "LISTE.md").write_text("\n".join(liste) + "\n", encoding="utf-8")
    return len(liste) - 2


def main(argv=None, ev=Path.home() / ".claude", dist=KOK / "dist" / "envanter-3"):
    a = (argv if argv is not None else sys.argv[1:]) or ["--kuru"]
    yedek, md = ev / "skills-yedek-envanter3", ev / "CLAUDE.md"
    if a[0] == "--geri":
        for ad in ADLAR:
            if (ev / "skills" / ad).exists():
                shutil.rmtree(ev / "skills" / ad)
            if (yedek / ad).exists():
                shutil.move(str(yedek / ad), str(ev / "skills" / ad))
        if (yedek / "CLAUDE.md").exists():
            shutil.move(str(yedek / "CLAUDE.md"), str(md))
        if yedek.exists():
            yedek.rmdir()
        print("geri:", ", ".join(ADLAR), "+ CLAUDE.md eski hale döndü"); return 0
    eski = md.read_bytes() if md.exists() else b""
    yeni = eski if SATIR.encode("utf-8") in eski else eski.rstrip(b"\r\n") + b"\n" + SATIR.encode("utf-8") + b"\n"
    j = jeton(yeni.decode("utf-8"))
    if a[0] != "uygula":
        n = paketle(dist)
        print(f"KURU: {', '.join(ADLAR)} → {ev / 'skills'} · CLAUDE.md +1 satır ({jeton(SATIR)} jeton; dosya ~{j}/{TAVAN})"
              f" · zip {n} → {dist}"); return 0
    assert j <= TAVAN, f"CLAUDE.md ~{j} jeton > {TAVAN}: önce satır birleştir"
    if yedek.exists():
        sys.exit(f"yedek zaten var ({yedek}); önce --geri")
    yedek.mkdir(parents=True)
    for ad in ADLAR:
        hedef, kaynak = ev / "skills" / ad, KOK / "skills" / ad
        if hedef.exists():
            shutil.copytree(hedef, yedek / ad); shutil.rmtree(hedef)
        shutil.copytree(kaynak, hedef, ignore=shutil.ignore_patterns("__pycache__"))
        kayip = filecmp.dircmp(kaynak, hedef, ignore=["__pycache__"])
        assert not (kayip.left_only or kayip.diff_files), f"kurulum kaybı: {kayip.left_only} {kayip.diff_files}"
    if md.exists():
        shutil.copy2(md, yedek / "CLAUDE.md")
    md.write_bytes(yeni)  # bayt olarak: Windows write_text LF→CRLF yapar
    print("uygulandı:", ", ".join(ADLAR), f"· CLAUDE.md ~{j} jeton", "· geri: --geri"); return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
