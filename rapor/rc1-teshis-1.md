# RC1-TESHIS-1
- Kök neden 1 (kanıtlı): rc 1 + boş json = RAM-BEKÇİ ≥%88'de ajan ağacını öldürüyor (log "AĞAÇ DURDURULDU" → "RAM İLE KESİLDİ" → rc 1, 2-4 dk); 52 rc≠0'ın 20'si bu kalıp. Elenenler: --resume, .mcp.json, ordu-on, limit mesajı.
- Kök neden 2 (kanıtlı): Windows PATH'inde `bash` yok (Get-Command boş; Git\bin ekli değil) → datadog eklentisinin `bash session_end.sh` SessionEnd hook'u "Executable not found" → rc 1 + JSON'un arkasına hata satırı. Hook kaldırılmadı: `bash_yolu_ekle()` çocuk süreç PATH'ine Git\bin ekler (önce None → sonra bash.EXE).
- (b) `json_satir()` raw_decode: sonuc_var / is_kaydi / sonuc_temizle ilk geçerli JSON'u alır, yapışık metin ad.stray.txt'ye; subtype=success ise rc'ye bakmadan BAŞARILI. (c) `kopya_calisiyor()`: ad-b/ad-r koşuyor ya da bitmişse KURTAR atlar ("tek kopya kilidi").
- Önceki tur: `baslamadan_dustu()` (rc≠0 + boş json + RAM kesmedi + <3 dk) merdiveni harcamaz.
- Test: kırmızı görüldü (hook_hatasi rc1 → False) → yeşil; tests/test_ajan_sira.py 61 geçti (+3 yeni).
- Yeniden kuyruk: yarim-g2-b gerçekten koşuyor (pid 65112, 17:45'ten beri, canlı); yarim-g7-r1 ve yarim-g3-a-r1 kuyrukta RAM bekliyor.
- Yapılmadı: yarim-a2-devam-a (kuyrukta -a satırı yok, görev dosyası yok). Çalışan yönetici eski kodla; yeni kod yönetici yeniden başlayınca devreye girer (başlatmadım, koşan işleri keserdi). LİMİT/ajan-sira.dur: limit kanıtı yok → eklenmedi.
- Ömer kararı: ajan-sira.tavan 5→2-3 ya da MCP profilini daralt; yoksa RAM kesmeleri sürer.
