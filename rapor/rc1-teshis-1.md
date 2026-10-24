# RC1-TESHIS-1
- Kök neden: rc 1 + boş json = başlama hatası DEĞİL; RAM-BEKÇİ ≥%88'de ajan ağacını öldürüyor (log: "AĞAÇ DURDURULDU … 13-16 alt süreç, 1.7-2.2 GB" → "RAM İLE KESİLDİ" → BİTTİ rc 1, 2-4 dk). yarim-g2/g7/g3-a/a2-devam-a hepsinde eşleşti (17:13, 17:11, 16:47, 17:26, 17:33). Log'da 52 rc≠0'ın 20'si bu kalıp.
- Elenenler: --resume (4 işte "baştan"), .mcp.json, ordu-on, limit mesajı (log'da yok). Makine tabanı %82 (python 5.3 GB/55 süreç, node 4.8 GB); ajan başına ~2 GB × 4 eşzamanlı → %88.
- stderr zaten stdout'a (json'a) gidiyor (stderr=STDOUT); json boş = SIGKILL, çıktı yok.
- Düzeltme: `baslamadan_dustu()` (rc≠0 + boş json + RAM kesmedi + <3 dk) → log "BAŞLAMADAN DÜŞTÜ", merdiven yükselmez. Test kırmızı→yeşil; tests/test_ajan_sira.py 58 geçti.
- Yeniden kuyruk: yarim-g7-r1, yarim-g3-a-r1 eklendi; yarim-g2 yönetici tarafından 17:44'te başlatıldı (pid 64968 canlı, 1.2 GB, ağaç 13 alt süreç) = gerçekten koşuyor.
- Yapılmadı: yarim-a2-devam-a (kuyrukta satırı yok, görev dosyası bulunamadı). LİMİT/ajan-sira.dur: limit kanıtı yok → eklenmedi. Çalışan yönetici eski kodla; yeni kod yeniden başlatmada devreye girer.
- Asıl çözüm Ömer kararı: ajan-sira.tavan 5→2-3 (eşzamanlı ağaç sayısı) ya da MCP profilini daralt; aksi halde RAM kesmeleri sürer.
