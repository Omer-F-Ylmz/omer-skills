# Video öğrenme — sertifika koşusu kontrol listesi (23)

Koşu: bir site yapımı videosu, `/video-uygula <url>` uçtan uca. Her madde kanıtla işaretlenir (dosya yolu, sayı ya da transcript satırı).

## Aday videolar (K6: kayit.jsonl 70 video → Jev choice, 70 istek; site 16 · frontend-araç 4 · diğer 50)
1. JfmAm3sxCSc — "Claude'a Ödüllü Siteler Gibi 3D Website Yaptırdım" · p(site) 1.00 · ödüllü site referansından 3D site yapımı adım adım.
2. iYwCzKy6W40 — "Claude'a Premium 3D Web Sitesi Yaptırdım" · 0.99 · premium 3D sahne + kaydırma, yapım süreci ekranda.
3. 4cE9t4rE0-0 — "Claude Code ile Premium Animasyonlu Web Sitesi Yaptım" · 0.98 · animasyon/geçiş teknikleri, CC ile yapım.

## Kontrol
- [ ] Araştırıcı modeli: her aday için `subagent_type: aday-arastirici`; subagents/*.meta.json `agentType: aday-arastirici`, assistant `model: claude-sonnet-5`; aday başına subagent_tokens ≤40k. Koşu öncesi `video ajan-denetle` GEÇTİ. general-purpose'a düşüş = DUR.
- [ ] Mekanizma: token ya da teknik etiketli her özellikte `## Mekanizma` (nasıl · neden · koşul · bizde) dolu; en az bir dolu bölüm; `video rapor-denetle <aday.md>` GEÇTİ.
- [ ] Prompt anatomisi: videoda gösterilen site yapım promptu `tur: prompt` aday; `## Prompt anatomisi` 7 alan + `### Kalıplar` (m:ss · şablon); `video rapor-denetle` GEÇTİ; kalıplar docs/departmanlar/frontend-promptlar.md'de (video + zaman), şablonda olmayan UYARLA docs/kurulumlar/bekleyen/prompt-*.md. Metin kopyalanmaz.
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

## Sertifika-1 koşusu — 2026-09-24 · JfmAm3sxCSc (GEÇTİ 11 · KALDI 1 · uygulanamaz 5)
- KALDI · Araştırıcı: model GEÇTİ (bed69dbb…/subagents/agent-ab6e…meta.json + agent-a914…meta.json `agentType: aday-arastirici`, jsonl `model: claude-sonnet-5` 54/55 satır; tarayıcı `video-tarayici` sonnet-5; `video ajan-denetle` GEÇTİ; general-purpose 0). Token KALDI: threejs-spiral-gallery 128.386 · motionsites-ai 94.146 > 40k (31/33 araç çağrısı; tanımdaki 8 tur tutmadı). Web 1 ve 3 (≤3).
- GEÇTİ · Mekanizma: motionsites-ai.md 2 · threejs-spiral-gallery.md 4 `nasıl:` dolu; `video rapor-denetle (aday)` ikisi GEÇTİ. İpucu adaylarında özellik yok (rapor-denetle aday kipi uygulanamaz).
- GEÇTİ · Departman: 2026-09-24-uygula.md ## DEPARTMAN 5/5 (frontend 4 · belge 1); `video brief` ## Departman 5 satır; bu koşunun 10 kayıt satırı departmanlı; karar kayıtları (yargi) 33/33 departmanlı, departman-geri 0 (kalan 9 satır yargi'siz onay/dene kaydı); frontend.md ## Videodan gelen.
- GEÇTİ · Site/UI teknikleri: 2026-09-24-JfmAm3sxCSc.md 6 satır (kanıt m:ss + kare); tahmin 4 (Lenis, hover, tipografi, ScrollTrigger), kesin 2 (GSAP: 6:37 karede `gsap.context()`; Three.js: `buildSpiral`); `video teknik` ÖĞREN 3 kart · UYARLA 3 bekleyen/teknik-*.md, tahmin: karta/bekleyene taşındı; frontend.md ## Teknikler 6.
- GEÇTİ · İddia sınama: 5 adayın hepsinde tablo; uygula.md ## İDDİA SINAMA 12 satır, kaynaksız sonuç yok (kaynak `-` → doğrulanamadı); abartılı 1 (hover geri kayma) → bekleyen/teknik-hover…md'ye not (kart yok). Resmi doküman: platform.claude.com prompting best practices "Be clear and direct".
- GEÇTİ · Kural çifti: toplu `İkinci promptta bozma kısıtı` → ÇİFT (kural: CLAUDE:4) → ZATEN VAR; T0 prompt-teknoloji-dosya · merkezi-config `çift/çelişki: yok` → bekleyen/kural-*.md, `ONAY kural` bekliyor (kural dosyasına yazılmadı).
- uygulanamaz · Kalite kapısı: DENE 1 (motionsites-ai/kopyala-yapistir-prompt) → docs/denemeler/motionsites-ai-kopyala-yapistir-prompt.md yazıldı (bütçe ≤6 claude -p, ≤$2); tarif tavanı claude -p 0 → koşulmadı.
- GEÇTİ · ÜRETİLEBİLİR: uygula.md ## ÜRETİLEBİLİR 1 (threejs-spiral-gallery-gsap-scroll-reveal-hmr · claude -p ≤24 · ≈$7.20); araç ayarı satırı yok.
- uygulanamaz · Takas tablosu: deneme koşmadı (claude -p 0).
- uygulanamaz · Tasarruf mekanizması kaydı: token etiketli tek özellik (kopyala-yapistir-prompt) ölçülmedi, tasarruf yok → docs/mekanizmalar kaydı doğmaz; mekanizma aday.md ## Mekanizma'da.
- uygulanamaz · Ayrıştırma: RED(kalite/takas)/SOR yok.
- uygulanamaz · Desktop ikinci görüş: `video brief` 32 satır hazır; Desktop cevabı bu oturumda yok, bölüm boş.
- GEÇTİ · YÜKLENECEK ZIP: uygula.md ## YÜKLENECEK ZIP "yok (T1 skill çıkmadı)".
- GEÇTİ · Toplam maliyet: Jev 66/150 · kare 5/10 · claude -p 0 ($0) · alt ajan 297.926 token (uygula.md ## MALİYET).
- GEÇTİ · rapor-denetle: tarama raporu GEÇTİ (rc 0) · 2 araç adayı GEÇTİ.
- GEÇTİ · Kayıt: docs/video-tarama/kayit.jsonl eski satır (2026-09-15) korundu + yeni satır `etiket: yeniden:sertifika`.
- GEÇTİ · Kararlar: 5 aday / 7 özellik → RED 1 · DENE 1 · ÖĞREN 2 · ZATEN VAR 3 · UYARLA 1 · KUR(T0) 2; ÖĞREN kartları bilgi/prompt-turkce-cevirt.md, bilgi/motionsites-ai-mcp-entegrasyonu.md.

## KURULUM-23c-B yeniden koşu — 2026-09-24 · JfmAm3sxCSc (iki madde)
- GEÇTİ · Araştırıcı bütçesi: `video on` önce (on.md ~390/~350 token) → aday-arastirici ×2 (general-purpose 0, `video ajan-denetle` GEÇTİ, maxTurns 12). threejs-spiral-gallery 128.386/31 → 30.257 token/7 araç · motionsites-ai 94.146/33 → 29.841/7; ikisi ≤40k ve ≤12. Kararlar değişmedi (threejs RED lisanssız · ZATEN VAR 3 · UYARLA 1; motionsites RED · ÖĞREN). Not: ikisi de mevcut raporu meta ile doğrulayıp rapor-denetle GEÇTİ aldı, sıfırdan yazmadı.
- GEÇTİ · Prompt anatomisi: docs/kurulumlar/adaylar/jfm-yapim-promptu.md (2:01–6:07, 7 kalıp) + motionsites-ai-kopyala-yapistir-prompt.md (DENE → ÖĞREN; eski deneme dosyası git mv ile buraya, kayit.jsonl +1 satır); ikisi `rapor-denetle` GEÇTİ. frontend-promptlar.md 9 kalıp (şablonda var 5 · UYARLA 4 → bekleyen/prompt-*.md).
- Son durum (sertifika-1 + 23c-B): GEÇTİ 13 · KALDI 0 · uygulanamaz 5 (Araştırıcı KALDI → GEÇTİ; Prompt anatomisi yeni madde GEÇTİ; Kalite kapısı: DENE kalktı, ölçüm gereği kalmadı).
