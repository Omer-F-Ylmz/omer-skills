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
hipotez: caveman proxy girdi tokenını Headroom'dan belirgin fazla azaltır, doğruluk düşmez (yazar: −%33.2 18/18; Headroom −%6.7 15/18).
metrik: girdi token (provider-reported) ve doğruluk (bilinen-doğru cevap); Headroom'a karşı A/B, aynı görev seti.
butce: 3 görev × (doğrudan · Headroom · caveman) ≤9 claude -p, ≤$3, Jev ≤12; kurulum T2 onayı + hemen `caveman telemetry off`; BSL-1.1 lisans notu (kendi kullanım serbest).
geri_alma: `caveman disable claude` + npm rm -g @caveman-ai/cli; Headroom ayarı değişmez.
esik: girdi token Headroom'a göre ≥%15 daha az ve doğruluk ≥ Headroom.
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
## Bağımsız kanıt
- https://blog.jetbrains.com/ai/2026/07/speak-to-ai-agents-like-cavemen-tosave-tokens/ — (README'de atıflı, doğrudan okunmadı) 86 gerçek görev, eşli A/B: skill çıktı −%8.5, kalite düz, maliyet ~−%10; ajan faturası çoğunlukla okuma.
- docs/denemeler/caveman-sonuc.md — bizim 14b A/B (3 görev, sonnet): çıktı −%20.7, kalite 2.97→2.75, maliyet +%7.7; kısa görevde kural girdisi kazancı yiyor.
- https://github.com/JuliusBrussee/caveman/blob/main/docs/WRAP-BENCHMARK.md — proxy −%33.2 / Headroom −%6.7 yazarın kendi koşusu; bağımsız tekrar yok.
## İddia sınama
| iddia | kaynak | sonuç | not | kart |
|---|---|---|---|---|
| caveman tarzı maliyeti 1.4–2.4× düşürür (Adobe) | docs/denemeler/caveman-sonuc.md | abartılı | bizde maliyet +%7.7; JetBrains yalnız ~−%10 | caveman-kural-maliyeti |
| skill çıktıyı −%8.5 azaltır, kalite düz (JetBrains) | https://github.com/JuliusBrussee/caveman | doğru | bizde çıktı −%20.7 ama kalite −0.22 | - |
| proxy girdi −%33.2, 18/18 doğru | https://github.com/JuliusBrussee/caveman/blob/main/docs/WRAP-BENCHMARK.md | doğrulanamadı | yazar ölçümü, ham artefakt yok; caveman-proxy DENE sınayacak | - |
| Headroom aynı testte −%6.7, 3/18 hata | https://github.com/JuliusBrussee/caveman/blob/main/docs/WRAP-BENCHMARK.md | doğrulanamadı | rakibin yazar ölçümü; bizde Headroom kurulu, A/B'de sınanır | - |
| compress CLAUDE.md ortalama −%46 | https://github.com/JuliusBrussee/caveman | doğrulanamadı | yazar ölçümü; caveman-compress DENE sınayacak | - |
## Bizde durum
- kurulum: yok (katalog ve settings'te yok; `video bizde` 15b)
- jev skill (Act): yok
kısmen: Concise çıktı stili + ≤15 satır kapanış raporu; omni-compression ve cli-compression kurulu-kapalı (skillOverrides off, 15b); RTK çıktı sıkıştırma; headroom girdi vekili. CACHE-1/ÇIKTI-1: maliyet ≈ girdi context × tur, çıktı payı %15.5.
