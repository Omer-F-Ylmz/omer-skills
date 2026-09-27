# Bekleyen kural özeti — yeniden:2026-09-24 (VİDEO-YENİDEN-1b K4)

Girdi: bekleyen/kural-*.md 25 dosya (21 yeniden:2026-09-24 + 4 SORULMADI'dan gelen yeniden:2026-09-28b). Sahte işaretli 8 dışarıda (kayıt `sahte` alanı; dosyalar silinmedi):
3d-derinlik · commit-leri-alan-bazında · her-güncelleme-sonrası · kalıcı-hafıza · loop-gece-koşusu · scroll-a-bağlı · skill-context-değişikliği · tam-proje-review.

Yöntem: kalan 17 madde `kural_esle` ile global CLAUDE.md (21 dilim) + omer-kurallar.md (26 dilim) + öteki 16 bekleyen maddeye karşı; Jev istek 29/60. Jev eşleşmesi: 3 (K1 çift, K2 → CLAUDE:18, K3 → CLAUDE:4); kalan 14 tekil. Öneri satırı maddenin kendi notuna ve mevcut metne dayanır; hiçbiri uygulanmadı, hepsi ONAY bekler.
Öneri: ONAYLA 3 · BİRLEŞTİR 3 · RED 10 (16 küme).

## K1 — frontend prompt ipuçları listesi (Jev çifti)
- dosyalar: diğer-anthropics-skills-frontend-design · diğer-ekran-görüntüsüyle-kendini-test
- kaynak: 39IlNR-P3-Q · EezLdmm8l1c
- madde: —
- öneri: RED — zaten var: frontend-craft Bölüm 0/2/8/9 (REF modu, 390/768/1440 screenshot, iki-pass, kapalı çevrim) + CLAUDE.md "/frontend-craft önce".

## K2 — Claude Code komut listesi (/btw, /loop, /resume …)
- dosya: claude-code-btw-loop-goal-resume-plugin · kaynak: Gg35_iQWx7g · Jev → CLAUDE:18
- madde: —
- öneri: RED — çelişiyor: video /resume öneriyor, CLAUDE.md "uzun aradan sonra /resume değil yeni oturum"; komut listesi kural değil.

## K3 — hazır tasarım promptunu mevcut siteye entegre etme
- dosya: hazır-tasarım-promptunu-mevcut-siteye-en · kaynak: QGyKyFcqyDE · Jev → CLAUDE:4 (Surgical changes)
- madde (kapsam: hazır tasarım promptunu mevcut siteye uygularken): Dokunulmaz alanlar (hero, mevcut animasyonlar) adıyla yazılır; prompttan yalnız ilgili bölüm alınır, loading ekranı ve port satırı çıkarılır.
- öneri: BİRLEŞTİR — CLAUDE.md "Surgical changes" maddesine kapsam cümlesi olarak.

## K4 — animasyonlu açılış + logo + Veo videoları
- dosya: animasyonlu-açılış-animasyonlu-logo-veo- · kaynak: ydO2_a97J6g
- öneri: RED — çelişiyor: proje-özgü stil kararı; frontend-craft Bölüm 3 "gereksiz animasyon yok".

## K5 — bağımsız doğrulayıcı
- dosya: bağımsız-doğrulayıcı-kodu-yazan-test-ede · kaynak: 2WIUAp4Z8EA
- madde (kapsam: uygulama davranışı değişen işlerde): "Bitti" kanıtı kodu yazandan bağımsız doğrulayıcıdan gelir: canlı uygulamada uçtan uca akış; hata raporu kök neden + kayıt ile.
- öneri: BİRLEŞTİR — omer-kurallar 2 ("bitti yalnız kanıtla") içine "yazandan bağımsız" şartı.

## K6 — yayın sonrası E2E regresyon
- dosya: güncelleme-sonrası-ve-gün-sonu-canlı-lin · kaynak: eck2ihs56Xs
- madde (kapsam: canlı linki olan sitelerde): Her yayın sonrası canlı linkte tüm sayfaları gezen E2E regresyon koşulur; geçmeden kapanış yok.
- öneri: ONAYLA — mevcut kurallar değişiklik başına test ister, sayfa geneli regresyon yok.

## K7 — context içeriği (rol, "premium ve sinematik", hedef kitle, mobil perf)
- dosya: context-içeriği-rol-premium-ve-sinematik · kaynak: QGyKyFcqyDE
- öneri: RED — zaten var: frontend-craft Bölüm 0 (sektör/REF), Bölüm 7 (stil adı), Bölüm 4 (perf).

## K8 — referansa bağlı kal, tüm cihazlar, hatayı sen çöz
- dosya: diğer-referansa-bağlı-kal-tasarımı-değiş · kaynak: Yunu27g7sLw
- öneri: RED — zaten var: frontend-craft Bölüm 0 (REF iyileştirilmez), Bölüm 2 (390/768/1440), Bölüm 9 (kapalı çevrim).

## K9 — "asla/her zaman" kesin ifadeler, skill README'siz
- dosya: diğer-talimata-uymuyorsa-asla-her-zaman- · kaynak: oGI1YmC2L00
- öneri: RED — çelişiyor: skill-creator "ağır MUST yerine nedenini açıkla"; README zaten yok.

## K10 — dört adımlı web prompt yapısı
- dosya: dört-adımlı-web-prompt-yapısı · kaynak: p9pPveeSOCQ
- öneri: RED — zaten var: frontend-craft Bölüm 0 + 7 + 8; yapım promptu şablonu departman-frontend'de.

## K11 — kısa brief (stil + tek mesaj + süre/format + tek referans)
- dosya: kısa-brief-stil-tek-mesaj-süre-format-te · kaynak: aa84rWKk8kw
- öneri: RED — zaten var: frontend-craft Bölüm 0 (REF, tek satır karar), Bölüm 7, Bölüm 5.

## K12 — renk/font/hareket brief'i
- dosya: renk-font-ve-hareket-brief-i-gold-palet- · kaynak: p9pPveeSOCQ
- öneri: RED — zaten var: frontend-craft Bölüm 0 mor/indigo yasağı, Bölüm 3, Bölüm 7.

## K13 — iş alanı başına ayrı klasör
- dosya: iş-alanı-başına-ayrı-klasör-uygulama-top · kaynak: u_cw1mIzvpY
- öneri: RED — kanıtsız: token iddiası ölçümsüz; ölçüm gelirse yeniden.

## K14 — alan bazlı commit + gerekçe + backlog
- dosya: iş-takibi-alan-bazlı-commit-gerekçe-notu · kaynak: 2n84xa99FRY
- madde (kapsam: birden çok alana dokunan işlerde): Commit'ler alan bazında ayrılır (frontend/backend), mesajda gerekçe; yarım kalan iş backlog'a yazılır.
- öneri: ONAYLA — mevcut kurallarda commit ayırma ve backlog yok.

## K15 — loop anatomisi (plan.md hafıza + stop)
- dosya: loop-anatomisi-plan-md-hafıza-açık-stop- · kaynak: HOHPUFauSWY
- madde (kapsam: tekrarlı/gözetimsiz döngülerde): Her iterasyon önce dalga.md'yi okur; ölçülebilir stop koşulu dalga.md'de yazılıdır.
- öneri: BİRLEŞTİR — omer-kurallar 10 (en fazla N tur + dalga.md) içine iterasyon cümlesi.

## K16 — tek buton bileşeni
- dosya: tek-buton-bileşeni · kaynak: EezLdmm8l1c
- madde (kapsam: site/UI yapımında): Bütün butonlar tek bileşenden varyantla türetilir; hover/focus/active o bileşende.
- öneri: ONAYLA — frontend-craft Bölüm 3 durumları ister, tek bileşen şartı yok.
