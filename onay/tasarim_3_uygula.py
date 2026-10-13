"""TASARIM-3 onay betiği — Ömer/Desktop koşar.

  python onay/tasarim_3_uygula.py --kuru   # plan (varsayılan)
  python onay/tasarim_3_uygula.py uygula   # yedek alır → yazar
  python onay/tasarim_3_uygula.py --geri   # son yedeği geri koyar
CC: frontend-craft 1.8.0 dosyaları (SKILL.md Bölüm 7/10 işaretçileri, references/vitrin-teknikleri.md yeni, references/yon-hatti.md)
kurulu plugin önbelleğine (~/.claude/plugins/cache/omer-skills/frontend-craft/<kurulu sürüm>/skills/frontend-craft) yazılır.
claude.ai: dist/tasarim-3/{frontend-craft,web-sahne-desenleri}.zip Desktop'tan elle yüklenir. Hiçbir şey silinmez; ayar dosyalarına dokunulmaz.
"""
import shutil, sys, time
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
EV = Path.home() / ".claude"
YEDEK = EV / "yedek" / "tasarim-3"
FC = KOK / "plugins/frontend-craft/skills/frontend-craft"
DOSYALAR = ("SKILL.md", "references/yon-hatti.md", "references/vitrin-teknikleri.md")


def hedefler(ev=EV):
    """(kaynak, hedef) çiftleri; kurulu frontend-craft yoksa boş."""
    surumler = sorted((ev / "plugins/cache/omer-skills/frontend-craft").glob("*/skills/frontend-craft"))
    return [(FC / p, surumler[-1] / p) for p in DOSYALAR] if surumler else []


def uygula(ev=EV, yedek=YEDEK):
    hedef_yedek = yedek / time.strftime("%Y%m%d-%H%M%S")
    for k, h in hedefler(ev):
        if h.exists():
            y = hedef_yedek / h.relative_to(ev)
            y.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(h, y)
        h.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(k, h)
    hedef_yedek.mkdir(parents=True, exist_ok=True)
    (hedef_yedek / "yeni.txt").write_text("\n".join(str(h) for _, h in hedefler(ev)), encoding="utf-8")
    return hedef_yedek


def geri(ev=EV, yedek=YEDEK):
    son = sorted(p for p in yedek.iterdir() if p.is_dir())[-1]
    for h in map(Path, (son / "yeni.txt").read_text(encoding="utf-8").splitlines()):
        y = son / h.relative_to(ev)
        if y.exists():
            shutil.copy2(y, h)
        elif h.exists():
            h.unlink()  # yalnız bu betiğin eklediği (önceden yoktu)
    return son


def main(argv):
    if "--geri" in argv:
        print("geri alındı:", geri())
    elif "uygula" in argv:
        print("yedek:", uygula())
    else:
        cifts = hedefler()
        if not cifts:
            print("kurulu frontend-craft yok (~/.claude/plugins/cache/omer-skills/frontend-craft) — önce plugin kur")
        for k, h in cifts:
            print(("ÜZERİNE " if h.exists() else "YENİ    ") + str(h), "<-", k.relative_to(KOK))
        print("claude.ai: dist/tasarim-3/{frontend-craft,web-sahne-desenleri}.zip Desktop'tan yüklenir.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
