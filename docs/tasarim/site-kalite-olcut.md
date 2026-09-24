# Site kalite ölçütü — `video dene --site` tasarımı (KURULUM-24 girdisi)

Amaç: videodan gelen site/UI tekniği, prompt kalıbı ya da skill adayını "güzel görünüyor" yerine sayıyla tartmak. Bu doküman tasarımdır; kod KURULUM-24'te.

## 1. Awwwards jüri ölçütleri
Kaynak: https://www.awwwards.com/about-evaluation/ (2026-09-24 okundu).
- Ağırlıklar: Design %40 · Usability %30 · Creativity %20 · Content %10.
- Oylama: site en az 18 jüri üyesine gider; ortalamaya en uzak 3 puan otomatik atılır; oylama 5 gün sürer.
- Eşikler: Honorable Mention ≥ 6.5 · Developer Award: SOTD siteleri ayrı geliştirici jürisinde "Developer Guidelines"a göre > 7.
- Developer Guidelines alt ölçütleri bu dalgada okunamadı (sayfa 404, web tavanı 2). KURULUM-24'te kaynaklı eklenir; kaynağı olmadığı için buraya yazılmadı.

Bizdeki karşılık (0–10, jüri ağırlığıyla): `oznel = 0.4·D + 0.3·U + 0.2·C + 0.1·I`
- D (tasarım): tipografi hiyerarşisi, renk/kontrast tutarlılığı, boşluk ritmi, görsel bütünlük.
- U (kullanılabilirlik): gezinme açıklığı, CTA bulunurluğu, okunabilirlik, mobil dokunma hedefleri.
- C (yaratıcılık): şablon dışı imza hareketi/sahne; departman-frontend yasak listesi (generic AI görünümü) ceza.
- I (içerik): metnin ürüne özgülüğü, görsel–metin uyumu (lorem/stok yer tutucu = 0).
- Çıkarım (Awwwards gibi): 3 puanlayıcıda uç puan atılır, ortalama alınır.

## 2. Ek ölçütler (nesnel kapılar)
Eşikler web-sahne-desenleri §3 ve departman-frontend `kabul:` satırıyla aynı; yeni eşik yok.
| ölçüt | araç | kapı |
|---|---|---|
| performans | Lighthouse CLI, mobil profil | perf ≥ 85 · LCP < 2.5 s |
| erişilebilirlik | axe-core (Playwright içinde) | ihlal 0 (serious/critical) |
| 390 px mobil | Playwright `scrollWidth ≤ innerWidth` + ekran görüntüsü | yatay taşma 0 (390/768/1440) |
| hareket akıcılığı | betikli kaydırmada rAF kare süreleri | p95 kare ≤ 20 ms (≈50 fps), uzun kare (>50 ms) ≤ %2 |
| azaltılmış hareket | `prefers-reduced-motion: reduce` emülasyonu | sürekli animasyon yok, içerik görünür |
Kapıdan biri kalırsa `kapı: KALDI (<ölçüt>)`; öznel puan yine hesaplanır ama kol kalite değeri 0'a çekilmez, rapora ayrı yazılır.

## 3. Ölçüm yöntemi
1. Kol çıktısı (statik site klasörü) `npx serve` ya da Vite preview ile yerelde açılır; ağ dışı.
2. Ekran görüntüsü: 390 · 768 · 1440 genişlikte ilk ekran (3 kare) + 1440'ta sayfa boyunca kaydırma kareleri (%0/20/40/60/80/100 → 6 kare). Toplam 9 kare, kol başına.
3. Nesnel kapılar aynı Playwright oturumunda (Lighthouse ayrı süreç).
4. Öznel puan: 9 kare + rubrik (§1 D/U/C/I tanımları) puanlayıcıya; çıktı JSON `{D,U,C,I,gerekce≤2 satır}`.
5. Kareler repo dışı önbellekte (`C:/Projeler/.video-cache/site/<ad>/<kol>/`), rapora yalnız yol.

## 4. Puanlayıcı seçenekleri
| seçenek | ne | maliyet | not |
|---|---|---|---|
| A. claude -p (Sonnet, görsel) | 9 kare + rubrik, 3 bağımsız çağrı, uç puan atılır | kol başına 3 claude -p (~$0.30/çağrı repo tahmini → ~$0.90/kol) | varsayılan; çağrı başı ≈ 9 görsel + rubrik |
| B. Jev | kare yerine nesnel ölçüm özeti + DOM metni üzerinden tipli yargı (p) | kol başına ≤2 Jev isteği | görsel görmez; yalnız U ve I için ikinci görüş |
| C. Ömer | aynı 9 kare, aynı rubrik, elle 0–10 | $0, zaman | kalibrasyon: ilk 3 sitede A ile karşılaştır; fark > 1.5 ise rubrik düzeltilir |
Öneri: A + kalibrasyonda C; B yalnız A'nın puanları arasında ayrışma > 2 olduğunda (SOR öncesi).

## 5. `video dene --site` tasarımı
`video dene <ad> --site --gorevler site-<SET> --tavan N`
- Görev seti `docs/denemeler/gorevler-site-<SET>/`: her görev bir sayfa briefi (landing · SaaS · portfolyo); aynı brief iki kola.
- Kollar: A = mevcut yöntem (departman-frontend `## Yapım promptu şablonu`), B = aday (prompt kalıbı / skill / teknik).
- Kol başına: claude -p ile site üretimi (1) + puanlama (3, seçenek A) → görev × kol × 4 claude -p; `--tavan` bunu keser (mevcut `görev × kol × 2` sayımı site için ×4).
- Her kolda ölçülen: toplam token/$ (mevcut dene sayacı) · düzeltme turu · `oznel` · 5 kapı.
- Çıktı `docs/denemeler/<ad>-sonuc.md`: mevcut `## Kol ortalamaları` tablosuna `site_puan` ve `kapi` sütunları; takas-geri bu dosyayı okumaya devam eder.

## 6. Takas tablosuna bağlanış
`kur.takas(s, d, esik_ok)` değişmez; site için girdiler:
- `s` (tasarruf %) = A'ya göre B'nin sıcak $ göreli düşüşü (mevcut tanım).
- `d` (kalite düşüşü %) = `max(0, (oznel_A − oznel_B) / oznel_A · 100)`; iki kolun farkı puanlayıcı yayılımı (3 çağrının std) içindeyse bant içi → 0 (mevcut "bant içi 0" kuralı).
- Kapı: A'da geçen bir kapı B'de kalıyorsa `d` ne olursa olsun `RED(kalite)` — kapı gerilemesi takasla telafi edilmez.
- `esik_ok`: B'nin öznel puanı A'dan en az 0.5 yüksek ya da tasarruf eşiği (mevcut) aşıldı.
Sonuç AL/SOR/RED mevcut K9 akışına girer (SOR → bekleyen/sor-<ad>.md, 2 örnek çıktı = 1440 ilk ekran kareleri).

## 7. KURULUM-24'e açık kalan
- Developer Guidelines alt ölçütleri (kaynaklı) → §1'e.
- Puanlayıcı yayılımı: aynı siteyi 3× puanlayıp std ölçülmeden "bant içi" eşiği sabitlenmez.
- Canlı tavan önerisi: ilk koşu 1 görev × 2 kol = 8 claude -p (~$2.40).
