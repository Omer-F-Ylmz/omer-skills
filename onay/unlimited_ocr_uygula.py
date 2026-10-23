"""UNLIMITED-OCR-KUR onay betiği — Ömer/Desktop koşar.

  python onay/unlimited_ocr_uygula.py --kuru   # plan (varsayılan)
  python onay/unlimited_ocr_uygula.py uygula   # skills/unlimited-ocr → ~/.claude/skills/unlimited-ocr (varsa yedek alır)
  python onay/unlimited_ocr_uygula.py --geri   # son yedeği geri koyar (yedek yoksa kopyayı siler)
claude.ai: dist/unlimited-ocr.zip Desktop'tan elle yüklenir (GPU/model yerelde; sandbox'ta koşmaz). Ayar dosyalarına dokunulmaz.
"""
import shutil, sys, time
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
EV = Path.home() / ".claude"
KAYNAK = KOK / "skills" / "unlimited-ocr"
HEDEF = EV / "skills" / "unlimited-ocr"
YEDEK = EV / "yedek" / "unlimited-ocr"


def uygula(hedef=HEDEF, yedek=YEDEK):
    if hedef.exists():
        y = yedek / time.strftime("%Y%m%d-%H%M%S")
        y.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(hedef), y)
    hedef.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(KAYNAK, hedef)
    return hedef


def geri(hedef=HEDEF, yedek=YEDEK):
    sonlar = sorted(p for p in yedek.glob("*") if p.is_dir()) if yedek.exists() else []
    if hedef.exists():
        shutil.rmtree(hedef)
    if sonlar:
        shutil.move(str(sonlar[-1]), hedef)
    return sonlar[-1] if sonlar else None


if __name__ == "__main__":
    a = sys.argv[1] if len(sys.argv) > 1 else "--kuru"
    if a == "uygula":
        print("yazıldı:", uygula())
    elif a == "--geri":
        print("geri alındı:", geri())
    else:
        print(f"plan: {KAYNAK} → {HEDEF} (mevcutsa {YEDEK} altına yedek)")
