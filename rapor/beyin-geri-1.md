# BEYIN-GERI-1
- Tekilleştirme: beyin_dusun.tekillestir (kök örtüşmesi ≥0.4, ≥3 ortak kök; 0 jeton, embedding gerekmedi). Gerçek özet: 13 rg/grep kuralı → tek satır "(×13)", ≤20 satır.
- Geri okuma: beyin_dusun.geri_oku (özet + göreve uyan ders + Obsidian 50-dersler/90-log + uyan tekrar-hata, ≤2400 kr). tools/arka_ajan.py her görevin başına ekler; cc-kopru sunucu.mjs ajan aracı `beyin_dusun.py geri` ile aynısını yapar (BEYIN_GERI=0 kapatır); Desktop için .kos/kopru/beyin-kontrol.md (≤10 satır, her turda yenilenir).
- Hata tekrarı: olay() hata ikinci kez aynı imzayla gelince beyin-tekrar.jsonl'e kaynak + önceki kaynak + kaçırılan ders; özette "TEKRAR HATA" satırı, göstergede "canlı tekrar N".
- Test: tests/test_beyin_geri.py (11, önce kırmızı) + mevcut beyin testleri = 106 geçti; cc-kopru ajan-argv 13 geçti.
- Sapma: %2 hedefi bu işle ölçülür hale geldi, düşmesi yeni işlerde geri okumaya bağlı (henüz ölçülmedi). Eski testler gerçek imza dosyasını kirletiyordu, Taban'a yönlendirme eklendi. Commit/push yok.
