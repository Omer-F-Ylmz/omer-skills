"""ORDU-1 onay betiği — Desktop koşar. Köprü ana oturumuna "derleyici" önsözünü açar: .kos/kopru/ajan-sira.ordu dosyasını oluşturur
(ajan_sira.ordu_onek bu dosyayı görünce istemin başına ≤80 jeton koyar: işi böl, alt işleri tools/ordu.py merdiveniyle dağıt, sen derle/doğrula/iyileştir).

  python onay/ordu_1.py          # --kuru (varsayılan): ne yapacağını söyler
  python onay/ordu_1.py uygula   # bayrak dosyasını yazar (çalışan runner'ın yenilenmesi gerekir)
  python onay/ordu_1.py --geri   # bayrak dosyasını siler → varsayılan kapalı
Kapı (B Claude token ≤ A'nın %50'si, kalite ≥ A, başarısızlık ≤ A) geçmeden açılmaz: python tools/ordu.py kapi A.json B.json.
Settings/hook/MCP'ye dokunmaz."""
import sys
from pathlib import Path

BAYRAK = Path("C:/Projeler/omer-skills/.kos/kopru/ajan-sira.ordu")

if "--geri" in sys.argv:
    BAYRAK.unlink(missing_ok=True)
    print("geri alındı: ordu önsözü kapalı")
elif "uygula" in sys.argv:
    BAYRAK.write_text("ORDU-1: ana oturum derleyici önsözü açık (geri: python onay/ordu_1.py --geri)\n", encoding="utf-8")
    print("açıldı:", BAYRAK, "— ajan_sira runner'ını yenile")
else:
    print(f"kuru: {'zaten açık' if BAYRAK.exists() else 'oluşturulacak'} {BAYRAK}")
