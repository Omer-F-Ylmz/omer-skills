# YONETICI-YENILE-2
Sorun: yenileme 'not calisan' bekliyordu; uzun ajan yeni işi 25+ dk durdurdu. Ajanlar Popen çocuğu, yenileme onları öldürmüyor.
Çözüm (.kos/kopru/ajan_sira.py): devral() — .basladi'sı canlı + kuyrukta satırı olan ajan yeni yöneticide calisan'a girer (Devralinan: poll=claude_sureci, rc=sonuc_var); yenile_hazir() — yalnız bekleyen yeniden denemeler yenilemeyi tutar, en çok 300 sn.
Test: tests/test_ajan_sira.py 57 geçti (yeni 4: yenile_hazir, Devralinan.poll, main'de DEVRAL→BİTTİ+is_kaydi, canlı ajanla anında yenile); önce kırmızı (AttributeError yenile_hazir) görüldü.
Eksik: devralınan ajan için üst basamak yeniden denemesi yok (bas=None); canlı yönetici elle öldürülmedi, değişiklik sonraki yenilemede devreye girer; gerçek execv uçtan uca denenmedi.
Push yok.
