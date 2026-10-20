"""SLASH-ÖĞREN d1 onay betiği — Desktop koşar. Köprü (ajan_sira) oturumlarında Skill aracını açar: .kos/kopru/ajan-sira.slash bayrağı.
(baslat_argv bayrağı görünce --disable-slash-commands'ı düşürür, --tools'a Skill ekler; oturum + alt ajanları skill/komut çağırabilir.)

  python onay/slash_ac.py          # --kuru (varsayılan)
  python onay/slash_ac.py uygula   # bayrağı yazar (çalışan runner'ın yenilenmesi gerekir)
  python onay/slash_ac.py --geri   # bayrağı siler → varsayılan kapalı
Settings/hook/MCP'ye dokunmaz."""
import sys
from pathlib import Path

BAYRAK = Path(__file__).resolve().parents[1] / ".kos" / "kopru" / "ajan-sira.slash"

if "--geri" in sys.argv:
    BAYRAK.unlink(missing_ok=True)
    print("geri alındı: köprü oturumlarında Skill aracı kapalı")
elif "uygula" in sys.argv:
    BAYRAK.write_text("SLASH-ÖĞREN d1: köprü oturumlarında Skill aracı açık (geri: python onay/slash_ac.py --geri)\n", encoding="utf-8")
    print("açıldı:", BAYRAK, "— ajan_sira runner'ını yenile")
else:
    print(f"kuru: {'zaten açık' if BAYRAK.exists() else 'oluşturulacak'} {BAYRAK}")
