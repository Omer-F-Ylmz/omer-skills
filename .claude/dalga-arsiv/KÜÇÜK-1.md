# KÜÇÜK-1 — birikmiş düzeltmeler
KARAR: sıra K5 → K1 → K3 → K4 → K2; ≤40 araç çağrısı (paralel ayrı sayılır), 35'te commit+push DUR; claude -p 0; okuma kuralı; PYTHONIOENCODING=utf-8; eski test çelişirse DUR.
K1 cc-kopru geç kapanan süreçler (suit.mjs:46 / suit.test.mjs:25; testler geçiyor ama "işaretli canlı süreç 2" ile çıkış 1; süreçler birkaç sn sonra kendiliğinden kapanıyor): önce teşhis — erken sayım mı, kapatılmayan süreç mi. Sayım öncesi işaretli süreçlerin çıkışı zaman aşımıyla beklenir; gerçek sızıntıysa kök neden düzeltilir. Test: kasıtlı yavaş kapanan sahte süreç → bekleme sonrası temiz; gerçekten asılı süreç → hâlâ yakalanır.
K2 `video kuyruk yenile`: kuyruk.md'de süresi/başlığı "?" olan satırları metadata ile yeniden doldurur (≥2 sn, 429/403 kuralı mevcut gibi; yine başarısızsa hata metni satır notuna). Test (sahte yt-dlp).
K3 `video parti baslat` hedef yoksa docs/video-tarama/kuyruk.md varsayılır (kuyruk alt komutundaki gibi); traceback yok. Test.
K4 bpy_kontrol: pyright çıktısı çözülemezse (çıkış 2) hata mesajına stderr'in ve ham çıktının ilk satırları eklenir; çıkış kodu değişmez. Test.
K5 h2a_kayit: feed veriyorsa frozen_message_count ve dönüşüm etiketleri satıra yazılır (vermiyorsa raporda, kod değişmez). Değişirse kayıtçı yeniden başlatılır: eski durdurulur, tek kopya doğrulanır, yeni pid buraya. Test (sahte feed).
KABUL: kırmızı-önce ayrı commit (her K) · eski test değişmez · tam suit (suite-kosucu; RAM≥6GB, oyun yok) · gitleaks · yalnız bu dalganın dosyaları add (parti/adaylar/video-tarama/.kos hariç) · dalga.md→.claude/dalga-arsiv/KÜÇÜK-1.md · push · graphify update . ön planda.
DURUM: kapandı — tam suit yeşil (558·81·319·179·40·22). K5 alan yok (pid 36820, kod değişmedi); K1 bitti; K3 bitti (395566e+6148fac; test sorunu _ns str(None)); K4 bitti (57ab4ab+yeşil); kapanış.
KALAN: K2 (video kuyruk yenile) — araç bütçesi (25) kapanışa ayrıldı.
