# RAM kuralı (F2, 27 Eki)

- Hedef tavan RAM %89. Aşarsa bekle, tekrar ölç; kural dışına çıkma.
- `.kos/kopru/ajan_sira.py` zaten RAM'e bakar: başlatma eşiği `esik()` (varsayılan %88, dosyayla 60–89), eşzamanlı iş tavanı `tavan()`, `ram_bekle()` kademeleri (≥%87 en büyük alt süreç, ≥%88 durdur, ≥%92 ajan ağacını kes). Yeni mekanizma eklenmedi.
- İş bitince kapat: Docker Desktop/Ollama/STRIX konteyneri/Blender/tarayıcı işi bitirenin sorumluluğu. İstisna: clodfarm Docker'ı açık tutar (yalnız STRIX konteyneri kapanır). Headroom durdurulmaz.
- Arka plan işi ekran açmaz (`.kos/kopru/arka.py`, CREATE_NO_WINDOW).
