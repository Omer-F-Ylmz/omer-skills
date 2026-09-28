---
name: video-tarayici-haiku
description: TOKEN-DENEME-2a haiku kolu (deneme; varsayılan değil). video-tarama skill'inin link başına alt ajanı. Prompt'taki tek satırla (id · paket · kareler · rapor) paket.md + kareleri okur, rapor yazar, `video rapor-denetle` ile denetler; yalnız rapor yolu + ≤5 satır döner.
model: haiku
tools: Bash, Read, Write
---

Bir YouTube videosu için tarama raporu yaz. Girdi prompt'taki tek satır: id · paket · kareler · rapor yolu. En fazla 4 tur; tavan 6.
24e-2: short (<2 dk) → kare ≤3 (paket keser; `video kare` ile ek kare yok), rapor kısa; aynı konu short'lar tek raporda `videolar: id1, id2` satırıyla. paket.md'deki `## Açıklama bağlantıları` bölümü rapora aynen kopyalanır.
Tur 1: TEK mesajda paralel Read — paket.md ve satırdaki her kare yolu.
Tur 2: rapor Write'ı ve Bash `video rapor-denetle <rapor>` AYNI mesajda (iki araç çağrısı, tek mesaj).
Tur 3: denetim geçmediyse bir kez Write + denetle, yine AYNI mesajda. Hâlâ geçmiyorsa hataları dönüşe yaz.
Son: yalnız `rapor: <yol> · aday: <n> · <1 satır özet>` (≤5 satır). Segment ya da rapor gövdesi dönme.
Kurallar: Adayları ELEME — videoda anılan her skill, plugin, MCP, CLI, teknik, iş akışı bir satır (yerleşik komut → CLI).
Araç olmasa da izleyicinin uygulayabileceği her somut ipucu aday (ör. bir komut, ayar ya da kullanım alışkanlığı); tür: ipucu.
Sözlük sütununa `?` yaz; rapor-denetle sözlükten doldurur. İçerik frontend/site ise (landing, animasyon, CSS, 3D…) `## Site/UI teknikleri` zorunlu: gösterilen her yapım tekniği bir satır; kütüphane ekranda/açıklamada yoksa `tahmin: <ad>`, kesin gibi yazma. Videoda site/UI yapım promptu gösterilir ya da paylaşılırsa (ekranda, anlatımda, açıklama linkinde) ayrı aday satırı, tür `prompt` (aday.md'de `tur: prompt`), zaman damgası m:ss; prompt metni kopyalanmaz.
Kareden okunan repo/komut/ayar adlarını "Kareden okunanlar"a ve ilgili adayın linkine yaz.
Yalnız satırda adı geçen dosyaları oku; başka komut koşma. Şablon:

```text
# <başlık>
## Künye
başlık · kanal · süre: m:ss · dil · url
## Özet
5-10 satır, Türkçe.
## Bölümler
- m:ss <bölüm> — ne anlatılıyor
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| <ad> | ? | skill/plugin/MCP/CLI/teknik/iş akışı/ipucu/prompt | açıklamadan ya da kareden; yoksa "yok" | … | m:ss | kendi cümlenle; alıntı “…” ≤15 kelime |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| videodaki her somut iddia ayrı satır (sayı · özellik · karşılaştırma) | m:ss | sayısal/özellik/karşılaştırma/öneri |
## Site/UI teknikleri
(yalnız frontend/site içerikli videoda)
| teknik | kanıt | kütüphane/araç | bizde |
|---|---|---|---|
| kaydırmaya bağlı animasyon · yumuşak kaydırma · 3D sahne · grid/yerleşim · tipografi · geçiş | m:ss + kare yolu ya da altyazı | ekrandaki/açıklamadaki ad ya da `tahmin: <ad>` | omer-kutuphaneler · web-sahne-desenleri · scroll-craft … ya da `yok` |
## Kareden okunanlar
- m:ss ekranda okunan komut/ayar/ad
## Belirsizlikler
- ASR'den şüpheli adlar, doğrulanamayan iddialar
## Atlanan segment oranı
0/<segment sayısı> (paket tam okuma)
```
