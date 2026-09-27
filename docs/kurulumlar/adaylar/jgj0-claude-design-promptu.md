# jgj0-claude-design-promptu
ad: jgj0-claude-design-promptu
tur: prompt
video: jGJ09wdTGDI
repo: yok
lisans: yok
son_commit: yok
arsiv: hayır
kaynak: yok
telemetri: yok
## Ne
Claude Design'a (claude.ai/design, hosted SaaS) tek doğal-dil promptuyla komple bir e-ticaret sitesi (saat markası: video arkaplan + ürün görselleri + stil dosyaları + renk paleti + component ağacı) ürettirme, sonra tek cümlelik doğal-dil komutlarıyla revize etme tekniği.
## Kanıt
Claude Design ürün sayfası (claude.com/product/design): beta, Pro/Max/Team/Enterprise planlarda; export/handoff Claude Code'a. Repo yok, kurulacak araç yok — hosted ürün.
## Kurulum
(yok — hosted SaaS, yerel kurulum gerektirmiyor; gerekçe: İzinler)
## İzinler
Hesap + Pro/Max/Team/Enterprise abonelik gerekiyor; kod/asset claude.ai sunucusuna yükleniyor (kendi ürün görselleri, video).
## Duman testi
(yok — çalıştırılabilir yerel komut yok)
## Geri alma
(yok — kurulum yapılmadı)
## Köprü izni
(yok — köprü/CLI aracı değil)
## Önerilen katman
RED (gerekçe: hosted SaaS, yerel kurulum/paket yok; fikir UYARLA olarak aşağıda değerlendirildi)
## Telemetri kapatma
yok — Anthropic'in hosted üründeki telemetrisi kullanıcı tarafından kapatılamıyor (bilgi yok)
## Özellikler
### tek-prompt-e-ticaret-sitesi
ne: Domain+hazır asset+stil sıfatı+CTA hedefini tek promptta vererek stil dosyaları, renk paleti, component ağacı ve ana taslağı tek geçişte ürettirme.
kurulum: claude.ai/design veya Claude Code içinde /design; kurulum yok, abonelik gerekir.
lisans: yok
etiket: teknik
karar: UYARLA
gerekce: kurulacak araç değil; fikir (asset+sıfat kısıtlı tek prompt kalıbı) kendi frontend-craft akışımıza aktarılabilir, kod yazılmaz.
### dogal-dille-iteratif-revizyon
ne: Üretilen siteyi "ortadaki yazıyı kaldır", "responsive yap" gibi tek cümlelik doğal-dil komutlarıyla revize etme.
kurulum: aynı chat arayüzü; kurulum yok.
lisans: yok
etiket: -
karar: ZATEN VAR
gerekce: zaten var: commit 3321f38 (BIRLESTIR K15 -> omer-kurallar:10 iterasyon cümlesi) bu kalıbı zaten kataloglamış.
### ciktiyi-claude-code-a-tasiyip-optimize-etme
ne: Tasarım-öncelikli çıktıyı (video ölçümü: Lighthouse %71) Claude Code'a aktarıp performans/loading optimizasyonu yaptırma önerisi.
kurulum: Claude Code içinde /design ile import; kurulum yok.
lisans: yok
etiket: -
karar: DENE
gerekce: hipotez: tasarım-öncelikli çıktının performans açığı Claude Code'a aktarılıp optimize edilince ölçülebilir kapanır · metrik: Lighthouse performans skoru · bütçe: 1 örnek site, ≤30 dk oturum · geri_alma: iyileşme yoksa bırak · eşik: ≥85 Lighthouse.
## Mekanizma
### tek-prompt-e-ticaret-sitesi
nasıl: Prompt 4 sabit parça taşıyor: domain/marka niyeti, hazır asset referansı ("bunları kullan"), stil sıfatları (premium/dark), davranışsal hedef (Shop Now CTA). Asset+sıfat sabit tutulduğu için marka kimliği korunuyor, yalnız layout/spacing/tipografi modele bırakılıyor; sonradan tek cümlelik NL komutuyla düzeltiliyor.
neden: Moodboard+palet+tipografi+component sistemi kurma işini tek geçişte birleştirip elle tasarım/iterasyon süresini kısaltıyor (zaman kazancı, token kazancı değil).
koşul: Hazır asset/net sıfat verilmezse model rastgele seçim yapar, marka tutarlılığı bozulur; hosted beta üründe token/kota tüketimi yüksek olabiliyor (bkz. bağımsız kanıt), kısa oturum/limitli planda pahalıya patlar.
bizde: frontend-craft'ta "tek prompt + zorunlu asset referansı" kalıbı yok; kurulum gerekmediği için doğrudan uygulanabilir örnek olarak not edildi.
## Bağımsız kanıt
- [VentureBeat — Anthropic Claude Design overhaul](https://venturebeat.com/technology/anthropic-ships-major-claude-design-overhaul-with-design-system-imports-code-round-trips-and-a-fix-for-its-token-burning-problem) — erken sürümde bir PCWorld incelemesi ~25 dakikada haftalık Pro kotasının %80'ini tüketmiş, Haziran 2026 güncellemesi bunu düzeltmeye çalışmış.
- [Claude Design (Anthropic) 2026 Guide — agence-scroll.com](https://agence-scroll.com/en/blog/claude-design-anthropic-2026-guide) — dışa aktarılan kod production-ready değil, güvenlik/ölçeklenebilirlik/erişilebilirlik/SEO açısından denetim gerekiyor; showcase/landing sayfası için önerilir, fonksiyonel MVP için değil.
## İddia sınama
| iddia | kaynak | sonuç | not | kart |
|---|---|---|---|---|
| Tek promptla birkaç dakikada tüm stil/renk paleti/taslak çıkar (3:15-4:18) | Claude Design ürün sayfası (claude.com/product/design) | doğru | Ürün sayfası tek prompt/asset/repo referansından tasarım+kod handoff akışını doğruluyor | - |
| Performans zayıf, sadece optimizasyon eksik, tasarım güçlü (12:00) | agence-scroll.com 2026 Guide | doğru | Bağımsız rehber de çıktının production-ready olmadığını, denetim gerektirdiğini doğruluyor | - |
| İngilizce prompt yazmak AI'dan daha iyi sonuç verir (1:39) | - | doğrulanamadı | Bu videoda ayrı candidate var (prompt-u-i-ngilizce-yazma.md); bağımsız kaynak bütçe dışında arandı | - |
## Prompt anatomisi
bolumler: hero (tam ekran video arkaplan + logo + CTA), ürün galerisi (saat görselleri), tipografi/renk paleti bildirimi (dark tema), buton/CTA (Shop Now), responsive gereksinimi (ikinci turda eklendi)
hareket: tam ekran video loop (arka plan); site tarafında ayrı animasyon yok (kanal bunu eksiklik olarak belirtiyor, 9:54)
teknoloji: React (component .jsx dosyaları), Claude Design (sürüm belirtilmemiş)
dosya: HomeHero.jsx, ProductCard.jsx, asset/ (saat görselleri), upload/ (yüklenen görseller)
config: belirtilmemiş (stil dosyaları var, dosya adı geçmiyor)
asset: kendi üretilen saat görselleri (AI), Adobe Firefly + Veo 3.1 ile üretilen ilk+son kare tanıtım videosu
kabul: responsive (iPhone 14 Pro Max/iPad Mini/iPhone X'te test; ilk üretimde responsive DEĞİLDİ, ikinci promptla düzeltildi), performans skoru (Lighthouse %71, düşük)
### Kalıplar
- E-ticaret sitesi yap, videoyu arka plana full yerleştir · 3:15 · teknik: asset referanslı prompt · şablon: asset
- Kendi ürettiğim ürün görsellerini ver, bunları kullan de · 3:15 · teknik: asset zorunluluğu · şablon: asset
- Premium, dark temalı, Shop Now CTA'li site iste · 3:15 · teknik: stil sıfatı + CTA belirtme · şablon: config
- Ortadaki yazıyı kaldır, butonları köşeye al tek cümle · 5:36 · teknik: doğal dil revizyon · şablon: hareket
- Bu web siteyi responsive yap tek cümle · 5:36 · teknik: doğal dil revizyon · şablon: kabul
