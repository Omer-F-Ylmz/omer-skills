"""ORDU-1 onay betiği — Desktop koşar. Köprü ana oturumuna "derleyici" önsözünü açar: .kos/kopru/ajan-sira.ordu dosyasını oluşturur
(ajan_sira.ordu_onek bu dosyayı görünce istemin başına ≤80 jeton koyar: işi böl, alt işleri tools/ordu.py merdiveniyle dağıt, sen derle/doğrula/iyileştir).

  python onay/ordu_1.py          # --kuru (varsayılan): ne yapacağını söyler
  python onay/ordu_1.py uygula   # bayrak dosyasını yazar (çalışan runner'ın yenilenmesi gerekir)
  python onay/ordu_1.py kabul    # orta iş çapraz kontrol ölçütünü gevşetir (normalize eşitlik + üçüncü aile hakem); ordu.kabul bayrağı
  python onay/ordu_1.py --geri   # iki bayrağı da siler → varsayılan kapalı (birebir aynı yanıt)
Kapı (B Claude token ≤ A'nın %50'si, kalite ≥ A, başarısızlık ≤ A) geçmeden açılmaz: python tools/ordu.py kapi A.json B.json.
Settings/hook/MCP'ye dokunmaz."""
import sys
from pathlib import Path

BAYRAK = Path("C:/Projeler/omer-skills/.kos/kopru/ajan-sira.ordu")
KABUL = BAYRAK.with_name("ajan-sira.ordu-kabul")

if "--geri" in sys.argv:
    BAYRAK.unlink(missing_ok=True)
    KABUL.unlink(missing_ok=True)
    print("geri alındı: ordu önsözü ve gevşek kabul kapalı")
elif "kabul" in sys.argv:
    KABUL.write_text("ORDU-1 d6: orta iş kabulü normalize eşitlik + üçüncü aile hakem (geri: python onay/ordu_1.py --geri)\n", encoding="utf-8")
    print("açıldı:", KABUL)
elif "uygula" in sys.argv:
    BAYRAK.write_text("ORDU-1: ana oturum derleyici önsözü açık (geri: python onay/ordu_1.py --geri)\n", encoding="utf-8")
    print("açıldı:", BAYRAK, "— ajan_sira runner'ını yenile")
else:
    print(f"kuru: {'zaten açık' if BAYRAK.exists() else 'oluşturulacak'} {BAYRAK}")
