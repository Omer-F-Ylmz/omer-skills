"""TASARIM-1 onay betiği — Ömer/Desktop koşar.

  python onay/tasarim_1_uygula.py --kuru   # plan (varsayılan)
  python onay/tasarim_1_uygula.py uygula   # yedek alır → yazar
  python onay/tasarim_1_uygula.py --geri   # son yedeği geri koyar
CC: skills/tasarim-katalog → ~/.claude/skills/tasarim-katalog; frontend-craft 1.6.0 dosyaları (SKILL.md, scripts/slop.mjs)
kurulu plugin önbelleğine (~/.claude/plugins/cache/omer-skills/frontend-craft/<kurulu sürüm>/skills/frontend-craft) yazılır.
claude.ai: dist/tasarim-1/*.zip Desktop'tan elle yüklenir. Hiçbir şey silinmez; ayar dosyalarına dokunulmaz.
"""
import shutil, sys, time
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
EV = Path.home() / ".claude"
YEDEK = EV / "yedek" / "tasarim-1"
FC = KOK / "plugins/frontend-craft/skills/frontend-craft"


def hedefler(ev=EV):
    """(kaynak, hedef) çiftleri; kaynak dizinse dizin kopyalanır."""
    cifts = [(KOK / "skills/tasarim-katalog", ev / "skills/tasarim-katalog")]
    surumler = sorted((ev / "plugins/cache/omer-skills/frontend-craft").glob("*/skills/frontend-craft"))
    if surumler:
        cifts += [(FC / p, surumler[-1] / p) for p in ("SKILL.md", "scripts/slop.mjs")]
    return cifts


def uygula(ev=EV, yedek=YEDEK):
    hedef_yedek = yedek / time.strftime("%Y%m%d-%H%M%S")
    for k, h in hedefler(ev):
        if h.exists():
            y = hedef_yedek / h.relative_to(ev)
            y.parent.mkdir(parents=True, exist_ok=True)
            (shutil.copytree if h.is_dir() else shutil.copy2)(h, y)
        h.parent.mkdir(parents=True, exist_ok=True)
        if k.is_dir():
            shutil.copytree(k, h, dirs_exist_ok=True)
        else:
            shutil.copy2(k, h)
    (hedef_yedek / "yeni.txt").parent.mkdir(parents=True, exist_ok=True)
    (hedef_yedek / "yeni.txt").write_text("\n".join(str(h) for _, h in hedefler(ev)), encoding="utf-8")
    return hedef_yedek


def geri(ev=EV, yedek=YEDEK):
    son = sorted(p for p in yedek.iterdir() if p.is_dir())[-1]
    for h in map(Path, (son / "yeni.txt").read_text(encoding="utf-8").splitlines()):
        y = son / h.relative_to(ev)
        if y.exists():
            (shutil.copytree(y, h, dirs_exist_ok=True) if y.is_dir() else shutil.copy2(y, h))
        elif h.is_dir():
            shutil.rmtree(h)  # yalnız bu betiğin eklediği (önceden yoktu)
        elif h.exists():
            h.unlink()
    return son


def main(argv):
    if "--geri" in argv:
        print("geri alındı:", geri())
    elif "uygula" in argv:
        print("yedek:", uygula())
    else:
        for k, h in hedefler():
            print(("ÜZERİNE " if h.exists() else "YENİ    ") + str(h), "<-", k.relative_to(KOK))
        print("claude.ai: dist/tasarim-1/frontend-craft.zip + tasarim-katalog.zip Desktop'tan yüklenir.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
