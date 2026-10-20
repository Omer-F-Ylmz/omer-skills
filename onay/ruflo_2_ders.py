"""RUFLO-2 d4 onay betiği — Desktop koşar. Ana oturum ders enjeksiyonunu açar: .kos/kopru/ajan-sira.ders dosyasını oluşturur
(ajan_sira.ders_onek bu dosyayı görünce istemin başına ≤120 jeton ders bloğu koyar; ilgisiz/boşsa 0 jeton).

  python onay/ruflo_2_ders.py          # --kuru (varsayılan): ne yapacağını söyler
  python onay/ruflo_2_ders.py uygula   # bayrak dosyasını yazar (çalışan runner'ın yenilenmesi gerekir)
  python onay/ruflo_2_ders.py --geri   # bayrak dosyasını siler → varsayılan kapalı
Kanıt: rapor/ruflo-2.md d4 · docs/kutuphane/olcum/ruflo-2-kapi.tsv. Settings/hook/MCP'ye dokunmaz."""
import sys
from pathlib import Path

BAYRAK = Path("C:/Projeler/omer-skills/.kos/kopru/ajan-sira.ders")

if "--geri" in sys.argv:
    BAYRAK.unlink(missing_ok=True)
    print("geri alındı: ders enjeksiyonu kapalı")
elif "uygula" in sys.argv:
    BAYRAK.write_text("RUFLO-2 d4: ana oturum ders enjeksiyonu açık (geri: python onay/ruflo_2_ders.py --geri)\n", encoding="utf-8")
    print("açıldı:", BAYRAK, "— ajan_sira runner'ını yenile")
else:
    print(f"kuru: {'zaten açık' if BAYRAK.exists() else 'oluşturulacak'} {BAYRAK}")
