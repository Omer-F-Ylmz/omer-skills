"""ROUTER-1 onay betiği — Desktop koşar. skills/model-sec → ~/.claude/skills/model-sec (BASE_URL/settings'e dokunmaz).
python onay/router_1_uygula.py --kuru   # plan (varsayılan; hiçbir şey yazmaz)
python onay/router_1_uygula.py uygula   # varsa eskiyi ~/.claude/yedek/router1-<zaman>/ altına alır, kopyalar
python onay/router_1_uygula.py --geri   # son uygulamayı geri alır
claude.ai için dist/router-1/model-sec.zip.
"""
import json, shutil, sys, time
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
EV = Path.home()
AD = "model-sec"
YOKSAY = shutil.ignore_patterns("__pycache__", "*.pyc")
SON = EV / ".claude" / "yedek" / "router1-son.json"


def kuru():
    kaynak, hedef = KOK / "skills" / AD, EV / ".claude" / "skills" / AD
    n = sum(1 for p in kaynak.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    print(f"{AD}: {n} dosya → {hedef} ({'üzerine, yedekli' if hedef.exists() else 'yeni'})")


def uygula():
    hedef, yedek = EV / ".claude" / "skills" / AD, EV / ".claude" / "yedek" / f"router1-{time.strftime('%Y%m%d-%H%M%S')}"
    yedek.mkdir(parents=True)
    vardi = hedef.exists()
    if vardi:
        shutil.move(str(hedef), str(yedek / AD))
    shutil.copytree(KOK / "skills" / AD, hedef, ignore=YOKSAY)
    SON.write_text(json.dumps({"yedek": str(yedek), "vardi": vardi}), encoding="utf-8")
    print(f"kuruldu {hedef}" + (f" (eski → {yedek})" if vardi else ""))


def geri():
    son = json.loads(SON.read_text(encoding="utf-8"))
    hedef = EV / ".claude" / "skills" / AD
    shutil.rmtree(hedef, ignore_errors=True)
    if son["vardi"]:
        shutil.move(str(Path(son["yedek"]) / AD), str(hedef))
    print("geri alındı")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    k = sys.argv[1] if len(sys.argv) > 1 else "--kuru"
    {"--kuru": kuru, "uygula": uygula, "--geri": geri}[k]()
