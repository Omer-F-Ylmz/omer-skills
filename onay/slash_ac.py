"""SLASH-ÖĞREN d1 onay betiği — Desktop koşar. Köprü (ajan_sira) oturumlarında Skill aracını açar: .kos/kopru/ajan-sira.slash bayrağı.
(baslat_argv bayrağı görünce --disable-slash-commands'ı düşürür, --tools'a Skill ekler; oturum + alt ajanları skill/komut çağırabilir.)

  python onay/slash_ac.py          # --kuru (varsayılan)
  python onay/slash_ac.py uygula   # bayrağı yazar (çalışan runner'ın yenilenmesi gerekir)
  python onay/slash_ac.py uygula dar   # d2: yalnız çekirdek 15 skill/komut (--setting-sources "" + --plugin-dir)
  python onay/slash_ac.py --geri   # bayrağı siler → varsayılan kapalı
Settings/hook/MCP'ye dokunmaz."""
import sys
from pathlib import Path

BAYRAK = Path(__file__).resolve().parents[1] / ".kos" / "kopru" / "ajan-sira.slash"

if "--geri" in sys.argv:
    BAYRAK.unlink(missing_ok=True)
    print("geri alındı: köprü oturumlarında Skill aracı kapalı")
elif "uygula" in sys.argv:
    dar = "dar=cekirdek" if "dar" in sys.argv else ""  # d2: yalnız 15 kartlık küme (tam liste ≈ +35k token, dar ≈ -5k)
    if dar:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools" / "ogrenme"))
        import slash_dar
        slash_dar.kur()
    BAYRAK.write_text(f"SLASH-ÖĞREN d1: köprü oturumlarında Skill aracı açık {dar} (geri: python onay/slash_ac.py --geri)\n", encoding="utf-8")
    print("açıldı:", BAYRAK, dar, "— ajan_sira runner'ını yenile")
else:
    print(f"kuru: {'zaten açık' if BAYRAK.exists() else 'oluşturulacak'} {BAYRAK}")
