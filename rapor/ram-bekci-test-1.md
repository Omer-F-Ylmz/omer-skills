RAM-BEKCI-TEST-1: tests/test_ajan_ram_bekci.py 12 → 17 test, 17 yeşil (mevcut dosya genişletildi).
Kırmızı-önce: TEK_MIN_MB=0 → test_sinir_599_secilmez_600_secilir düştü; geri alınca yeşil. korumali satırı çıkarılınca 2 test düştü.
Hata 1 (kod): hedef_sec yalnız izinli() bakıyordu; oyun/Epic/WindowsApps ajan altındaysa seçilebiliyordu → `not korumali(...)` eklendi.
Hata 2 (test): test_torun_da_alt_surectir 50 MB bekliyordu (24.10 eşiğiyle bayat) → 700 MB.
Not: yönetici ajan altı değil, kökün üstü; ayrı koruma gerekmedi. Bekçi yeniden başlatılmadı.
