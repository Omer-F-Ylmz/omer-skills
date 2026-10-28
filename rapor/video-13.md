# video-13 rapor (28 Eki, kalan-6 ajanı; ek API yok, yeni canlı koşu yok)
Kanıt: .kos/kopru/v13b_olc.log (K ↔ KO ↔ KA, altın 4 video ×3, bitti rc 0, Σusd 10.4), özet bu ajanda hesaplandı.
Ortalama (short | uzun jeton·usd·süre; aday Σ · ad Σ · komut Σ · url Σ):
- K  : 226k·.299·362 | 471k·.810·577 ; 67.7 · 53.0 · 26.3 · 30.7
- KO : 231k·.345·344 | 511k·.917·617 ; 64.7 · 50.7 · 28.0 · 30.7
- KA : 215k·.349·374 | 482k·.746·544 ; 65.3 · 47.0 · 20.0 · 32.0
Karar (Kabul: yakalama ≥ taban, ad ≥ taban, jeton ↓, USD ≤ taban):
- C3a (KO): RET. Jeton +2/+9%, USD +15/+13%, aday −4%, ad −4%; bayrakta kalır.
- C3d (KA): RET. Ad −11%, komut 26→20, short USD +17%; bayrakta kalır (uzun USD −8% gürültü bandı).
- K varsayılan kalır (devam-2'de uygulandı, 13bc246 / 114b36c).
- Haiku "kaçan tarayıcı" ikinci geçiş: ENGEL — yazmak için ölçüm gerekir, ölçüm ücretli API ister; bu ajan ücretli API kullanamaz. Kuru koşu yapılacak yeni kod yazılmadı, canlı runner'a dokunulmadı.
- İki taraf skill notu: K iç varsayılan, skills/video-* metninde VIDEO_JETON yüzeyi yok → değişiklik yok; zip değişmedi (yalnız not konusu, kullanıcı yüzeyi değişmedi).
Sonraki: haiku ikinci geçiş kodu + ölçümü API izinli oturumda (≤$20).
