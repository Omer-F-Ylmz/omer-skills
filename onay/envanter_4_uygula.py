"""ENVANTER-4 onay betiği — Desktop koşar (Ömer onayından sonra; ENVANTER-2 uygula'dan SONRA).

CC: docs/katalog/tarifler/ + kilavuz/ + derin.tsv (derin.jsonl'den) ~/.claude/skills/yetenek-getir/ altına
kurulur; SKILL.md ve katalog dosyaları değişmez. Varsa eski tarifler/kilavuz/derin.tsv
~/.claude/skills-yedek-envanter4/'e yedeklenir.
claude.ai: dist/envanter-4/yetenek-getir.zip (skills/yetenek-getir + aynı üç ek; zip_denetle'den geçer) + LISTE.md.

  python onay/envanter_4_uygula.py --kuru   # plan (varsayılan): hiçbir şey yazmaz
  python onay/envanter_4_uygula.py uygula   # yedekle + kur + zip'le + kayıp denetimi
  python onay/envanter_4_uygula.py --geri   # kurulanı kaldır, yedeği geri koy"""
import filecmp, json, shutil, sys, zipfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools" / "skill-paket"))
import zip_denetle  # noqa: E402

AD = "yetenek-getir"
KAT = KOK / "docs" / "katalog"
EK = ("tarifler", "kilavuz", "derin.tsv")
ALAN = ("nasil", "neden", "en_iyi", "birlikte", "tuzak", "maliyet")


def derin_tsv():
    satir = ["\t".join(("tur", "ad", "durum") + ALAN)]
    for j in map(json.loads, open(KAT / "derin.jsonl", encoding="utf8")):
        satir.append("\t".join(" ".join(str(j.get(a, "")).split()) for a in ("tur", "ad", "durum") + ALAN))
    return "\n".join(satir) + "\n"


def ekle(hedef):
    for d in EK[:2]:
        shutil.copytree(KAT / d, hedef / d)
    (hedef / "derin.tsv").write_text(derin_tsv(), encoding="utf-8", newline="\n")


def main(argv=None, ev=Path.home() / ".claude", dist=KOK / "dist" / "envanter-4"):
    a = (argv if argv is not None else sys.argv[1:]) or ["--kuru"]
    hedef, yedek = ev / "skills" / AD, ev / "skills-yedek-envanter4"
    if a[0] == "--geri":
        for e in EK:
            p = hedef / e
            shutil.rmtree(p) if p.is_dir() else p.unlink(missing_ok=True)
        if yedek.exists():
            for p in yedek.iterdir():
                shutil.move(str(p), str(hedef / p.name))
            yedek.rmdir()
        print("geri alındı:", hedef); return 0
    n = {d: len(list((KAT / d).glob("*.md"))) for d in EK[:2]}
    if a[0] == "--kuru":
        print(f"KURU: {hedef} ({'var' if hedef.exists() else 'YOK → önce ENVANTER-2 uygula'}) ← tarifler {n['tarifler']} · kilavuz {n['kilavuz']} · derin.tsv"
              f" · zip {dist / (AD + '.zip')}"); return 0
    if not hedef.exists():
        sys.exit(f"{hedef} yok — önce onay/envanter_2_uygula.py uygula")
    if yedek.exists():
        sys.exit(f"yedek var: {yedek} — önce --geri")
    var = [hedef / e for e in EK if (hedef / e).exists()]
    if var:
        yedek.mkdir(parents=True)
        for p in var:
            shutil.move(str(p), str(yedek / p.name))
    ekle(hedef)
    for d in EK[:2]:
        k = filecmp.dircmp(KAT / d, hedef / d)
        assert not (k.left_only or k.diff_files), f"{d}: kayıp {k.left_only} {k.diff_files}"
    dist.mkdir(parents=True, exist_ok=True)
    gecici = dist / AD
    shutil.rmtree(gecici, ignore_errors=True)
    shutil.copytree(KOK / "skills" / AD, gecici)
    ekle(gecici)
    zp, dosyalar = dist / f"{AD}.zip", sorted(p for p in gecici.rglob("*") if p.is_file())
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for p in dosyalar:
            z.write(p, f"{AD}/{p.relative_to(gecici).as_posix()}")
    shutil.rmtree(gecici)
    sorun = zip_denetle.denetle(zp)
    assert not sorun, f"{zp.name}: {sorun}"
    assert len(zipfile.ZipFile(zp).namelist()) == len(dosyalar), f"{zp.name}: zip kaybı"
    (dist / "LISTE.md").write_text(f"# ENVANTER-4 claude.ai zip (yetenek-getir'in yerine yüklenir)\n\n"
                                   f"- {zp.name} · {len(dosyalar)} dosya · {zp.stat().st_size // 1024} KB\n", encoding="utf-8")
    print("uygulandı:", hedef, f"(tarifler {n['tarifler']} · kilavuz {n['kilavuz']} · derin.tsv, kayıp 0)",
          "· zip", len(dosyalar), "dosya →", dist, "· geri: --geri"); return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
