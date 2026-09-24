# Video öğrenme — sertifika koşusu kontrol listesi (23)

Koşu: bir site yapımı videosu, `/video-uygula <url>` uçtan uca. Her madde kanıtla işaretlenir (dosya yolu, sayı ya da transcript satırı).

## Aday videolar (K6: kayit.jsonl 70 video → Jev choice, 70 istek; site 16 · frontend-araç 4 · diğer 50)
1. JfmAm3sxCSc — "Claude'a Ödüllü Siteler Gibi 3D Website Yaptırdım" · p(site) 1.00 · ödüllü site referansından 3D site yapımı adım adım.
2. iYwCzKy6W40 — "Claude'a Premium 3D Web Sitesi Yaptırdım" · 0.99 · premium 3D sahne + kaydırma, yapım süreci ekranda.
3. 4cE9t4rE0-0 — "Claude Code ile Premium Animasyonlu Web Sitesi Yaptım" · 0.98 · animasyon/geçiş teknikleri, CC ile yapım.

## Kontrol
- [ ] Araştırıcı modeli: her aday için `subagent_type: aday-arastirici`; subagents/*.meta.json `agentType: aday-arastirici`, assistant `model: claude-sonnet-5`; aday başına subagent_tokens ≤40k. Koşu öncesi `video ajan-denetle` GEÇTİ. general-purpose'a düşüş = DUR.
- [ ] Mekanizma: token ya da teknik etiketli her özellikte `## Mekanizma` (nasıl · neden · koşul · bizde) dolu; en az bir dolu bölüm; `video rapor-denetle <aday.md>` GEÇTİ.
- [ ] Departman: uygula raporunda `## DEPARTMAN` her aday için dolu; `video brief` çıktısında görünür; kayit.jsonl'de departmansız karar kaydı 0; katalogda `## Videodan gelen` satırları.
- [ ] Site/UI teknikleri: tarama raporunda bölüm dolu (teknik · kanıt m:ss · kütüphane ya da `tahmin:` · bizde); `video teknik <rapor>` → ÖĞREN kartı/UYARLA bekleyen; frontend.md `## Teknikler`.
- [ ] İddia sınama: her adayda `## İddia sınama` tablosu, kaynaksız sonuç yok; abartılı/yanlış → karta not.
- [ ] Kalite kapısı: DENE/UYARLA-talimat çıkarsa `video dene` (claude -p tavanı yazılı: en fazla N); çıkmazsa "gerekmedi".
- [ ] ÜRETİLEBİLİR: UYARLA-skill/talimat varsa raporda `## ÜRETİLEBİLİR` dolu (ad · kaynak özellik · fayda · claude -p ve $); araç ayarı yok.
- [ ] Deneme kararları takas tablosuyla (AL/SOR/RED) ve tutan kademeyle (`[kademe: …]`) yazılmış; SOR → bekleyen/sor-<ad>.md.
- [ ] Token tasarrufu olan her özellikte docs/mekanizmalar/<ad>.md `## Tasarruf mekanizması` kaydı.
- [ ] RED(kalite/takas)/SOR alan tasarruflu özellikte docs/uyarlamalar/<ad>-ayristir.md.
- [ ] Desktop ikinci görüş: `video brief` → Desktop; cevap `## Desktop ikinci görüş` bölümüne olduğu gibi.
- [ ] YÜKLENECEK ZIP: raporda liste; `skill_denetim.py` 0 hata.
- [ ] Toplam maliyet: Jev istek (tavanla) · claude -p sayısı ve $ · alt ajan token toplamı.
