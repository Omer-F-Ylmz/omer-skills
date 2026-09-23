# caveman
ad: caveman
tur: CLI
repo: JuliusBrussee/caveman
lisans: MIT + BSL-1.1
telemetri: açık
kaynak: yok
## Ne
Ajan token tasarrufu araç kümesi: konuşma tarzı skill (çıktı), okuma tarafını sıkıştıran proxy (girdi), yerel geçmişten token kaybı sıralaması (learn), CLAUDE.md sıkıştırma (compress).
## Kanıt
- repo README (gh api, 2026-09-23): lisans rozeti "MIT + BSL"; README: "Runs AI … MIT … CLI, BSL-1.1" (skill MIT, CLI/proxy BSL-1.1).
- Reponun kendi benchmark dokümanı: docs/WRAP-BENCHMARK.md (54 koşu, yazar ölçümü; ham artefakt yayımlanmamış, "pinned report, not public reproduction").
- Telemetri: CLI anonim sayım varsayılan açık (`caveman telemetry off`); skill hook'ları göndermez.
## Kurulum
- npm: @caveman-ai/cli
## Duman testi
- komut: caveman --version
- cikis: 0
- desen: \d+\.\d+
## Geri alma
- npm: @caveman-ai/cli
## Telemetri kapatma
- caveman telemetry off
## Özellikler
### skill
ne: konuşma tarzı skill; ajanın çıktısını mağara adamı diliyle kısaltır (kural dosyası her çağrıda ~1k girdi token).
kurulum: /caveman skill (plugin); bizde omni-compression ve cli-compression kurulu-kapalı.
lisans: MIT
etiket: token
karar: RED
gerekce: ölçüm: docs/denemeler/caveman-sonuc.md — bizim A/B çıktı −%20.7 (< eşik %30), kalite 2.97→2.75, maliyet +%7.7
### proxy
ne: okuma tarafını sıkıştırır (log, test çıktısı, JSON, diff); orijinal yerel SQLite'ta, geri çağrılabilir.
kurulum: `caveman claude` ajanı proxy arkasına alır; T2, bu dalgada koşulmaz.
lisans: BSL-1.1
etiket: token
karar: DENE
hipotez: caveman proxy girdi tokenını Headroom'dan belirgin fazla azaltır, doğruluk düşmez (yazar: −%33.2 18/18; Headroom −%6.7 15/18); README: Headroom caveman'ın önünde çalışabilir.
metrik: girdi token (provider-reported) ve doğruluk (bilinen-doğru cevap); 4 kol aynı görev seti: doğrudan · Headroom · caveman · Headroom+caveman.
butce: 3 görev × 4 kol (doğrudan · Headroom · caveman · Headroom+caveman) ≤12 claude -p, ≤$3, Jev ≤12; kurulum T2 onayı + hemen `caveman telemetry off`; BSL-1.1 lisans notu (kendi kullanım serbest).
geri_alma: `caveman disable claude` + npm rm -g @caveman-ai/cli; Headroom ayarı değişmez.
esik: caveman ya da Headroom+caveman girdi tokenı Headroom'a göre ≥%15 daha az ve doğruluk ≥ Headroom.
### learn
ne: yerel oturum geçmişinden token kaybı yapan kalıpları en kötüden sıralar, her birine tek satır düzeltme önerir (salt-okur rapor).
kurulum: `caveman learn` (CLI); `learn implement` KULLANILMAZ (diff uygular).
lisans: BSL-1.1
etiket: token
karar: DENE
hipotez: learn raporu bizim bilmediğimiz ≥1 büyük token kaybı kalıbı gösterir (RTK/headroom/graphify'ın kapsamadığı).
metrik: raporun ilk 5 kalemindeki tahmini token kaybı; mevcut araçlarla kapsanmayan kalem sayısı.
butce: 1 koşu, salt-okur, $0 model; telemetri kapalıyken.
geri_alma: rapor dosyasını sil; ayar değişmez.
esik: kapsanmayan ≥1 kalem ve tahmini kayıp oturum girdisinin ≥%5'i.
### compress
ne: `/caveman-compress CLAUDE.md` kural dosyasını sıkıştırır; başlık, kod, yol, URL korunur (yazar: ortalama −%46).
kurulum: skill komutu; hedef Divisima CLAUDE.md, önce yedek.
lisans: MIT
etiket: token
karar: DENE
hipotez: Divisima CLAUDE.md ≥%30 küçülür, hiçbir kural kaybolmaz.
metrik: CLAUDE.md token (önce/sonra, c.token) ve kural korunumu (madde başına Jev eşleşmesi ya da elle diff).
butce: 1 dosya, yedekli (CLAUDE.md.bak), Jev ≤10.
geri_alma: CLAUDE.md.bak'tan geri yükle.
esik: token −%30 ve korunmayan kural 0.
### kural-maliyeti
ne: kural dosyası (skill/CLAUDE.md) her çağrıda girdiye biner.
lisans: -
etiket: token
karar: ÖĞREN
iddia: kural dosyası her çağrıda girdiye biner; kısa görevlerde çıktı tasarrufunu aşabilir.
guven: yüksek
dogrulama: https://github.com/JuliusBrussee/caveman (README: skill kural dosyası ~1k girdi token) + docs/denemeler/caveman-sonuc.md (14b: çıktı −%20.7, maliyet +%7.7)
url: https://github.com/JuliusBrussee/caveman
etiketler: token, kural-dosyasi, olcum
### convert
ne: pixel mode — kurulu skill gövdelerini modelin görsel okuduğu PNG sayfalarına çevirir (yazar: caveman skill 1069 → 415 token); `--dry-run`, `--revert` var.
kurulum: `caveman convert` (CLI, BSL-1.1); T2, bu dalgada koşulmaz.
lisans: BSL-1.1
etiket: token
karar: DENE
hipotez: yüklenen skill gövdesi görsel sayfayla ≥%40 daha az girdi token harcar, skill kuralına uyum düşmez (skill listesi metni değişmez).
metrik: skill yüklemesinde girdi token (provider-reported) ve kural uyumu (görev başarısı + Jev kalite, 18 kapısı).
butce: 1 skill (video-uygula) × 18 kalite kapısı görev seti ≤18 claude -p, Jev ≤30, `--dry-run` önce.
geri_alma: `caveman convert --revert`; skill dosyaları değişmezse geri alma yok.
esik: girdi token −%40 ve 18 kapısı (başarı B ≥ A, kalite gürültü bandında).
### browse
ne: tarayıcı sayfasını sıkıştırılmış erişilebilirlik ağacıyla verir (yazar: 200 satırlık tabloda 121 vs 15.704 token; küçük formda 2.3× kayıp).
kurulum: `caveman browse` (CLI, BSL-1.1); T2.
lisans: BSL-1.1
etiket: token
karar: DENE
hipotez: büyük tablolu sayfada playwright snapshot / pixeljury'ye göre ≥%50 daha az girdi token, doğru öğe bulma düşmez.
metrik: sayfa başına girdi token ve doğru öğe/değer bulma; playwright-cli snapshot ve pixeljury ekran testine karşı A/B.
butce: 3 sayfa (büyük tablo · form · landing) × 3 kol ≤9 claude -p, ≤$2.
geri_alma: npm rm -g @caveman-ai/cli; playwright/pixeljury ayarı değişmez.
esik: büyük tabloda girdi token −%50 ve doğruluk ≥ playwright; formda kayıp ≤ playwright.
### shrink
ne: komut çıktısını sıkıştırır, geri alınabilir; RTK ile örtüşür.
kurulum: `caveman shrink` (CLI, BSL-1.1); T2.
lisans: BSL-1.1
etiket: token
karar: DENE
hipotez: aynı komut çıktılarında RTK'dan ≥%15 daha az token, sinyal kaybı yok.
metrik: komut başına çıktı token (RTK'ya karşı A/B) ve sinyal korunumu (hata satırı · test sayısı · yol).
butce: 5 komut çıktısı (pytest · dotnet test · git log · npm test · rg), model yok, $0.
geri_alma: npm rm -g @caveman-ai/cli; RTK ayarı değişmez.
esik: token RTK'ya göre −%15 ve kayıp sinyal 0.
### cavecrew
ne: sıkıştırılmış alt ajan ön ayarları (investigator · builder · reviewer).
lisans: MIT
etiket: token
karar: UYARLA
fikir: alt ajan tanımına kısa yanıt ve dolgusuz dönüş kuralı; en büyük maliyet kalemimiz alt ajan tabanı (12c).
hedef: .claude/agents/video-tarayici.md · .claude/agents/aday-arastirici.md
etki: alt ajan dönüşü ve tur başı çıktı token düşer; ölçüm 18 kalite kapısıyla.
kapsam: yalnız alt ajan tanım metni; araç ve model seçimi değişmez.
### calisma-kaliplari
ne: investigate-first · lean-build · surgical-patch · verify-and-stop çalışma kalıpları.
lisans: MIT
etiket: kural
karar: ÖĞREN
iddia: caveman çalışma kalıpları (önce araştır, az kod, cerrahi yama, doğrula ve dur) omer-kurallar ve Karpathy ilkeleriyle büyük ölçüde örtüşür; fark madde madde bakılmalı.
guven: orta
dogrulama: https://github.com/JuliusBrussee/caveman (README) + omer-kurallar + ~/.claude/CLAUDE.md genel ilkeler
url: https://github.com/JuliusBrussee/caveman
etiketler: kural, calisma-bicimi
### trial
ne: gerçek oturumu caveman'lı/caveman'sız A/B'ler.
lisans: MIT
etiket: token
karar: UYARLA
fikir: `video dene`'ye "gerçek oturum" kipi — tek atışlık görev yerine kayıtlı gerçek oturum istemleri A/B.
hedef: tools/video/video/kur.py (dene)
etki: ölçüm gerçek iş yüküne yaklaşır; tek atışlık görevlerin tavan etkisi azalır.
kapsam: fikir dokümanı; kod bu dalgada yazılmaz.
## Bağımsız kanıt
- https://blog.jetbrains.com/ai/2026/07/speak-to-ai-agents-like-cavemen-tosave-tokens/ — (README'de atıflı, doğrudan okunmadı) 86 gerçek görev, eşli A/B: skill çıktı −%8.5, kalite düz, maliyet ~−%10; ajan faturası çoğunlukla okuma.
- docs/denemeler/caveman-sonuc.md — bizim 14b A/B (3 görev, sonnet): çıktı −%20.7, kalite 2.97→2.75, maliyet +%7.7; kısa görevde kural girdisi kazancı yiyor.
- https://github.com/JuliusBrussee/caveman/blob/main/docs/WRAP-BENCHMARK.md — proxy −%33.2 / Headroom −%6.7 yazarın kendi koşusu; bağımsız tekrar yok.
## İddia sınama
| iddia | kaynak | sonuç | not | kart |
|---|---|---|---|---|
| caveman tarzı maliyeti 1.4–2.4× düşürür (Adobe) | docs/denemeler/caveman-sonuc.md | abartılı (ajan düzeni için) | bizde maliyet +%7.7; JetBrains yalnız ~−%10 | caveman-kural-maliyeti |
| skill çıktıyı −%8.5 azaltır, kalite düz (JetBrains) | https://github.com/JuliusBrussee/caveman | doğru (ikincil kaynak) | bizde çıktı −%20.7 ama kalite −0.22 | - |
| proxy girdi −%33.2, 18/18 doğru | https://github.com/JuliusBrussee/caveman/blob/main/docs/WRAP-BENCHMARK.md | doğrulanamadı | yazar ölçümü, ham artefakt yok; caveman-proxy DENE sınayacak | - |
| Headroom aynı testte −%6.7, 3/18 hata | https://github.com/JuliusBrussee/caveman/blob/main/docs/WRAP-BENCHMARK.md | doğrulanamadı | rakibin yazar ölçümü; bizde Headroom kurulu, A/B'de sınanır | - |
| compress CLAUDE.md ortalama −%46 | https://github.com/JuliusBrussee/caveman | doğrulanamadı | yazar ölçümü; caveman-compress DENE sınayacak | - |
## Bizde durum
- kurulum: yok (katalog ve settings'te yok; `video bizde` 15b)
- jev skill (Act): yok
kısmen: Concise çıktı stili + ≤15 satır kapanış raporu; omni-compression ve cli-compression kurulu-kapalı (skillOverrides off, 15b); RTK çıktı sıkıştırma; headroom girdi vekili. CACHE-1/ÇIKTI-1: maliyet ≈ girdi context × tur, çıktı payı %15.5.
