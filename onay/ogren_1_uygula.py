"""ÖĞREN-1 onay betiği — Ömer/Desktop koşar. skills/is-akisi → ~/.claude/skills/is-akisi (CC'de yerel kopya yalnız bu;
departman-verimlilik ve video-uygula omer-skills marketplace'iyle gelir). claude.ai: dist/ogren-1/*.zip (.claude/ogren1/zipla.py).
python onay/ogren_1_uygula.py --kuru   # plan (varsayılan; hiçbir şey yazmaz)
python onay/ogren_1_uygula.py uygula   # eskiyi ~/.claude/yedek/ogren1-<zaman>/ altına alır, kopyalar
python onay/ogren_1_uygula.py --geri   # son uygulamayı geri alır
"""
import json, shutil, sys, time
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
EV = Path.home()
AD = "is-akisi"
YOKSAY = shutil.ignore_patterns("__pycache__", "*.pyc")


def uygula(ev=EV, kok=KOK):
    hedef, yedek = ev / ".claude" / "skills" / AD, ev / ".claude" / "yedek" / f"ogren1-{time.strftime('%Y%m%d-%H%M%S')}"
    yedek.mkdir(parents=True)
    vardi = hedef.exists()
    if vardi:
        shutil.move(str(hedef), str(yedek / AD))
    shutil.copytree(kok / "skills" / AD, hedef, ignore=YOKSAY)
    (ev / ".claude" / "yedek" / "ogren1-son.json").write_text(json.dumps({"yedek": str(yedek), "vardi": vardi}), encoding="utf-8")
    print(f"kuruldu {hedef}" + (f" (eski → {yedek})" if vardi else ""))


def geri(ev=EV):
    son = json.loads((ev / ".claude" / "yedek" / "ogren1-son.json").read_text(encoding="utf-8"))
    hedef = ev / ".claude" / "skills" / AD
    shutil.rmtree(hedef, ignore_errors=True)
    if son["vardi"]:
        shutil.copytree(Path(son["yedek"]) / AD, hedef)
    print("geri alındı" + (" (eski sürüm geri kondu)" if son["vardi"] else " (kaldırıldı)"))


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")
    kip = argv[0] if argv else "--kuru"
    if kip == "uygula":
        uygula()
    elif kip == "--geri":
        geri()
    else:
        hedef = EV / ".claude" / "skills" / AD
        dosyalar = [p for p in (KOK / "skills" / AD).rglob("*") if p.is_file() and "__pycache__" not in p.parts]
        print(f"{AD}: {len(dosyalar)} dosya → {hedef} ({'üzerine, yedekli' if hedef.exists() else 'yeni'})")


if __name__ == "__main__":
    main(sys.argv[1:])
