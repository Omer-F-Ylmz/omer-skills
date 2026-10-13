"""KANCA-SAYAÇ-1 onay betiği: çağrı sayacı kancasını (session_id başına sayaç + 140k bağlam
eşiği) canlı repoya kurar. Kanca repo içi: .claude/settings.json kaydı C:/Projeler/omer-skills/
tools/cagri_sayac.py'yi koşar — kayıt değişmez, yalnız betik içeriği. Hedef
<hedef>.kancasayac1-yedek olarak yedeklenir; --geri yedeği geri koyar.
  python onay/kanca_sayac_1_uygula.py --kuru   # plan (varsayılan)
  python onay/kanca_sayac_1_uygula.py uygula   # yedekle + kopyala
  python onay/kanca_sayac_1_uygula.py --geri   # yedekten geri koy"""
import shutil, sys
from pathlib import Path

KAYNAK = Path(__file__).resolve().parents[1] / "tools" / "cagri_sayac.py"
HEDEF = Path("C:/Projeler/omer-skills/tools/cagri_sayac.py")
YEDEK = ".kancasayac1-yedek"


def main(argv=None, kaynak=KAYNAK, hedef=HEDEF):
    a = (argv if argv is not None else sys.argv[1:]) or ["--kuru"]
    y = hedef.with_name(hedef.name + YEDEK)
    if a[0] == "--geri":
        if not y.exists():
            print("yedek yok:", y); return 1
        shutil.move(str(y), hedef)
        print("geri:", hedef); return 0
    if not hedef.exists() or not kaynak.exists():
        print("yok:", hedef if not hedef.exists() else kaynak); return 1
    if hedef.read_bytes() == kaynak.read_bytes():
        print("zaten güncel:", hedef); return 0
    if a[0] != "uygula":
        print(f"KURU: {kaynak} -> {hedef} · yedek {y.name}"); return 0
    if not y.exists():
        shutil.copy2(hedef, y)
    shutil.copyfile(kaynak, hedef)
    print("uygulandı:", hedef, "· geri: --geri")
    return 0


if __name__ == "__main__":
    sys.exit(main())
