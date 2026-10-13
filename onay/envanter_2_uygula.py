"""ENVANTER-2 onay betiği — Desktop koşar (Ömer onayından sonra). CC: skills/yetenek-getir (SKILL.md + katalog_ara.py +
yetenek.jsonl/.tsv) ~/.claude/skills/yetenek-getir'e kurulur; varsa eskisi ~/.claude/skills-yedek-envanter2/'ye yedeklenir.
claude.ai: dist/envanter-2/ altına yetenek-getir + 13 departman-* zip'i (zip_denetle'den geçer) + LISTE.md. Departman
satırları repo'da (plugin güncellemesiyle CC'ye gelir); settings, plugin dosyaları, ajanlar değişmez.

  python onay/envanter_2_uygula.py --kuru   # plan (varsayılan): kurulacak dosyalar + zip listesi; hiçbir şey yazmaz
  python onay/envanter_2_uygula.py uygula   # yedekle + kur + zip'le + kayıp denetimi
  python onay/envanter_2_uygula.py --geri   # kurulanı kaldır, yedeği geri koy"""
import filecmp, shutil, sys, zipfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools" / "skill-paket"))
import zip_denetle  # noqa: E402

AD = "yetenek-getir"


def kaynaklar():
    return [KOK / "skills" / AD] + sorted(KOK.glob("skills/departman-*"))


def zip_yaz(d, dist):
    zp = dist / f"{d.name}.zip"
    dosyalar = sorted(p for p in d.rglob("*") if p.is_file())
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for p in dosyalar:
            z.write(p, f"{d.name}/{p.relative_to(d).as_posix()}")
    return zp, len(dosyalar)


def main(argv=None, ev=Path.home() / ".claude", dist=KOK / "dist" / "envanter-2"):
    a = (argv if argv is not None else sys.argv[1:]) or ["--kuru"]
    hedef, yedek = ev / "skills" / AD, ev / "skills-yedek-envanter2" / AD
    if a[0] == "--geri":
        if hedef.exists():
            shutil.rmtree(hedef)
        if yedek.exists():
            shutil.move(str(yedek), str(hedef)); yedek.parent.rmdir()
        print("geri:", AD, "eski hale döndü" if hedef.exists() else "kaldırıldı (öncesinde yoktu)"); return 0
    kaynak = KOK / "skills" / AD
    dosya = sorted(p.name for p in kaynak.iterdir() if p.is_file())
    if a[0] != "uygula":
        print(f"KURU: {hedef} ← {dosya} · mevcut {'var (yedeklenir)' if hedef.exists() else 'yok'}"
              f" · zip {len(kaynaklar())} → {dist}"); return 0
    if yedek.exists():
        sys.exit(f"yedek zaten var ({yedek}); önce --geri")
    if hedef.exists():
        yedek.parent.mkdir(parents=True); shutil.copytree(hedef, yedek); shutil.rmtree(hedef)
    shutil.copytree(kaynak, hedef)
    kayip = filecmp.dircmp(kaynak, hedef)
    assert not (kayip.left_only or kayip.diff_files), f"kurulum kaybı: {kayip.left_only} {kayip.diff_files}"
    dist.mkdir(parents=True, exist_ok=True)
    liste = ["# ENVANTER-2 claude.ai zip'leri (Settings → Capabilities → Skills → yükle; aynı adlı eskisinin yerine)", ""]
    for d in kaynaklar():
        zp, n = zip_yaz(d, dist)
        sorun = zip_denetle.denetle(zp)
        assert not sorun, f"{zp.name}: {sorun}"
        assert len(zipfile.ZipFile(zp).namelist()) == n, f"{zp.name}: zip kaybı"
        liste.append(f"- {zp.name} · {n} dosya · {zp.stat().st_size // 1024} KB")
    (dist / "LISTE.md").write_text("\n".join(liste) + "\n", encoding="utf-8")
    print("uygulandı:", hedef, f"({len(dosya)} dosya, kayıp 0)", "· zip", len(liste) - 2, "→", dist, "· geri: --geri"); return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
