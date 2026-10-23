"""SKILL-DOGRULA-2 onay betiği: skills/departman-* → ~/.claude/skills/departman-* (CC'de departman skill'leri).

  python onay/departman_cc_uygula.py --kuru   # plan (varsayılan)
  python onay/departman_cc_uygula.py uygula   # farklı/eksik olanları kopyalar (varsa yedek alır); özdeş olana dokunmaz
  python onay/departman_cc_uygula.py --geri   # her departman için son yedeği geri koyar (yedek yoksa kopyayı siler)
Senkron: departman skill'i değişince `uygula` yeniden koşulur. claude.ai tarafı: dist zip (iki taraf kuralı).
"""
import hashlib, shutil, sys, time
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
EV = Path.home() / ".claude"
KAYNAK = KOK / "skills"
HEDEF = EV / "skills"
YEDEK = EV / "yedek" / "departman"


def ozet(d):
    h = hashlib.sha256()
    for f in sorted(p for p in d.rglob("*") if p.is_file() and "__pycache__" not in p.parts):
        h.update(f.relative_to(d).as_posix().encode())
        h.update(f.read_bytes())
    return h.hexdigest()


def liste(kaynak=KAYNAK):
    return sorted(p for p in kaynak.glob("departman-*") if (p / "SKILL.md").exists())


def uygula(kaynak=KAYNAK, hedef=HEDEF, yedek=YEDEK):
    yazilan = []
    for k in liste(kaynak):
        h = hedef / k.name
        if h.exists():
            if ozet(h) == ozet(k):
                continue
            y = yedek / k.name / time.strftime("%Y%m%d-%H%M%S")
            y.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(h), y)
        hedef.mkdir(parents=True, exist_ok=True)
        shutil.copytree(k, h, ignore=shutil.ignore_patterns("__pycache__"))
        yazilan.append(k.name)
    return yazilan


def geri(kaynak=KAYNAK, hedef=HEDEF, yedek=YEDEK):
    geri_alinan = []
    for k in liste(kaynak):
        h = hedef / k.name
        sonlar = sorted(p for p in (yedek / k.name).glob("*") if p.is_dir()) if (yedek / k.name).exists() else []
        if h.exists():
            shutil.rmtree(h)
        if sonlar:
            shutil.move(str(sonlar[-1]), h)
        geri_alinan.append(k.name)
    return geri_alinan


if __name__ == "__main__":
    a = sys.argv[1] if len(sys.argv) > 1 else "--kuru"
    if a == "uygula":
        print("yazıldı:", uygula())
    elif a == "--geri":
        print("geri alındı:", geri())
    else:
        print(f"plan: {len(liste())} departman skill'i {KAYNAK} → {HEDEF} (farklıysa {YEDEK} altına yedek)")
