---
name: tersine
description: "Tersine mühendislik: 'X nasıl yapılmış' sorusunu mekanizma notuna çevirir (site animasyonu, WebGL sahnesi, araç/repo, ikili). Kod/varlık kopyalamaz. Taslak (TERS-1 d1), REA kurulu değilse REA adımı atlanır."
---

# tersine — "X nasıl yapılmış" → mekanizma notu

Çıktı: `docs/ters/ornek-<ad>.md` (mekanizma · kanıt satırı · yeniden kurulum farkı sayıyla). Önce `graphify query` / `docs/ters/` içinde aynı desen var mı bak; varsa yeniden keşfetme.

## SINIR
Mekanizma ve teknik çıkarılır. Birebir klon yok; izinsiz görsel, font, model, ses, marka, kod kopyası yok. Kaynak dosya notta yalnız kanıt satırı olarak alıntılanır (≤5 satır). Tarayıcı headless; pencere açılmaz (`start <url>`, webbrowser.open yok). RAM ≥%85 iken tarayıcı adımı yok.

## Adımlar (site hedefi)
1. Teknoloji tespiti: ağ/kaynak dosyalarından kütüphane + sürüm (three r?, GSAP, Lenis, kendi motoru); açık source map varsa okunur kod.
2. Zamanlama: playwright headless + chrome-devtools performans izi; scroll sırasında zaman damgalı kareler → animasyon eğrisi/süre sayıyla.
3. WebGL: shader kaynağı, draw call, texture listesi (sayfaya `getContext` kancası).
4. Ekran kaydı varsa `video kare` + RapidOCR ile sahne sahne anlatım (yerel VLM yok, yerel model yasak).
5. Tasarım: design-dna / create-design-md → DESIGN.md token'ları; ekran görüntüsünden iskelet için image-to-code (kurulu değilse atla, nedenini yaz).
6. Ölçümlü yeniden kurulum: mekanizmayı küçük bir kendi örneğimizde kur; referansla sayısal screenshot farkı + Lighthouse. Fark sayıyla nota yazılır ("anladık mı" testi).
7. `graphify update .` ile çıkan kodun haritası; desen notu `web-sahne-desenleri` ile bağlanır.

## Adımlar (araç/repo/ikili hedefi)
REA (yapı/mantık; MCP ile ikili, Electron/JS, .NET) → graphify → küçük yeniden-yazım testi (mekanizmayı doğru anladık mı → testle kanıt). REA yalnız tarama temizse ve onay betiğiyle kurulduysa.

## Ek kombinler (öneri)
- **HAR + source map diff**: iki sürümün HAR'ı ve map'i farklanır → "ne değişti, hangi sürümde" sorusu ağdan cevaplanır. Gerekçe: video/ekran görüntüsü olmadan, sayıyla, ucuz.
- **Trace → tablo**: performans izinden frame-süre/long-task tablosu çıkarıp sadece tabloyu modele ver. Gerekçe: ham iz yüzbinlerce satır; tablo token'ı düşürür, eğri sayıya döner.
- **Mutasyon testi**: bulunan mekanizmanın bir parametresini (süre, easing) değiştirip kendi örneğinde farkı ölç. Gerekçe: "anladım" iddiası ölçümle sınanır.

## Kapanış
Not + kanıt satırları + fark sayısı; ≤15 satır rapor. Kapı: `docs/ters/kapi-tasarim.md`.
