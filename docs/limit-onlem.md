# Limit önlemi (CmOs0LZUOMM, "Claude 5.5'te 23 limit hatası")

Kaynak: video YouTube CmOs0LZUOMM; yerelde yalnız başlık + kuyruk ipucu var ("limite ulaşmama önlemleri; doğru işe doğru model"). Transkript/rapor çıkarılmadı, videonun kendi madde listesi doğrulanmadı. Aşağıdakiler ipucuna uyan, bizde zaten çalışan önlemlerdir.

1. Doğru işe doğru model: tek seferlik küçük iş = haiku, tek blok; okuma/analiz = okuyucu (sonnet); Opus yalnız plan/mimari/kod yazımı.
2. Yeni ajan kapısı: `.kos/kopru/ajan_sira.py` `kullanim_dolu()`, 5 saatlik ≥%85 ya da haftalık ≥%80 iken yeni ajan başlamaz (veri `~/.claude/rate-limits.json`, yoksa/15 dk eskiyse kapı açık).
3. Kalıcı oturum: gereksiz yeni oturum açma, önbellek ısınık kalsın (bkz. `docs/cc-kullanim-kurali.md`).
4. Büyük çıktı bağlama girmez: log/tarama `jev log|triage`, dosya dar aralıkla Read; araç çıktısı `rtk`/headroom ile sıkışır.
5. Limit mesajı alınırsa: DUR, döngüyle yeniden deneme yok (`claude -p` limit yanıtı düz metindir, "API Error" değil); sıfırlanma sonrası devam, bekleyen iş `DEVAM:` satırıyla yazılır.
6. Ücretli/paralel çağrılara sayısal tavan ("en fazla N").
