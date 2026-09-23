---
name: video-tarama
description: "1-8 YouTube linkini toplu tarar: link başına alt ajan segmentleri okur, aday raporu yazar; adaylar tekillenip işaretlenir, eleme yok. /video-tarama url... Toplu tarama yalnız CC'de."
---

# video-tarama — toplu, alt ajanlı video taraması

Ham altyazı **ana ajanın context'ine girmez**: yalnız alt ajan okur. Ana ajan her videodan rapor yolu + ≤5 satır alır.
claude.ai'de: bu belge okuma rehberidir (sandbox'ta `video` yok); tek video için Desktop'ta cc-kopru `komut` ile `video ozet/suz/oku/kare`.

## Akış (ana ajan)

```text
1. video kayit <url...> [--yeniden]     # kayit.jsonl'dekiler atlanır → "tara: …" · "atlandı: N" · "dalga i: ≤3 id"
2. video ozet <id...>                   # ≤4 eşzamanlı; altyazı önbelleğe (C:\Projeler\.video-cache\<id>\)
3. video paket <id> [--kare 6]          # her id; tek satır: paket.md yolu · kare yolları · ~token · Jev istek (yalnız ekran sorusu, p önbellekte varsa 0)
4. Her dalga için dalgadaki id başına bir Agent çağrısı, aynı mesajda (subagent_type: video-tarayici — sonnet, yalnız Bash/Read/Write).
   Prompt = aşağıdaki sabit metin AYNEN + en sonda tek satır: `id: <id> · paket: <yol> · kareler: <yollar> · rapor: docs/video-tarama/<tarih>-<id>.md`.
   Sabit kısım tüm alt ajanlarda bayt bayt aynı kalır (önbellek paylaşımı); videoya özgü olan yalnız son satır. Aynı anda en fazla 3 alt ajan.
5. video toplu <rapor.md...> [--istek-tavan M]  # tekille · sözlük eşleşmesi · jev tarama (≤2 batch) · işaret · <tarih>-toplu.md · kayit.jsonl
6. Sohbete: toplu'nun çıktısı (≤25 satır: video başına 1 satır + adaylar işaretiyle) + "atlandı: N" + tahmini maliyet.
```

Ana ajan paket.md, altyazı dosyası ya da segmentler.jsonl açmaz; alt ajan dönüşü dışında rapor gövdesi okumaz.

## Alt ajan görevi (sabit metin; değiştirmeden kopyala, videoya özgü satır en sonda)

````text
Bir YouTube videosu için tarama raporu yaz. Girdi son satırda: id · paket · kareler · rapor yolu. En fazla 4 tur; tavan 6.
Tur 1: TEK mesajda paralel Read — paket.md ve son satırdaki her kare yolu.
Tur 2: TEK mesajda Write rapor + Bash `video rapor-denetle <rapor>`.
Tur 3: denetim geçmediyse bir kez Write + denetle. Hâlâ geçmiyorsa hataları dönüşe yaz.
Son: yalnız `rapor: <yol> · aday: <n> · <1 satır özet>` (≤5 satır). Segment ya da rapor gövdesi dönme.
Kurallar: Adayları ELEME — videoda anılan her skill, plugin, MCP, CLI, teknik, iş akışı bir satır (yerleşik komut → CLI).
Sözlük sütununa `?` yaz; rapor-denetle sözlükten doldurur. Kareden okunan repo/komut/ayar adlarını "Kareden okunanlar"a ve ilgili adayın linkine yaz.
Başka komut koşma, başka dosya okuma. Şablon:
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
| <ad> | ? | skill/plugin/MCP/CLI/teknik/iş akışı | açıklamadan ya da kareden; yoksa "yok" | … | m:ss | kendi cümlenle; alıntı “…” ≤15 kelime |
## Kareden okunanlar
- m:ss ekranda okunan komut/ayar/ad
## Belirsizlikler
- ASR'den şüpheli adlar, doğrulanamayan iddialar
## Atlanan segment oranı
0/<segment sayısı> (paket tam okuma)
````

## Süzgeç varsayılanı: kapalı (12b ölçümü)

2 videoda süzgeçli okuma, tam okumanın adaylarının %74'ünü buldu (gevşek ad eşleşmesiyle; katı eşleşmeyle %55). Kabul eşiği %90 olduğu için
`video oku` ve `video paket` varsayılan olarak tüm segmentleri okur (paket dolgu sözcüklerini ve ardışık tekrarları atar). Süzgeç yalnız segmentlerin ~%10'unu atlıyordu, yani kazancı da küçüktü. Tekrar ölçmeden varsayılanı değiştirme.

## Denetim ve tavanlar

- `video rapor-denetle`: zorunlu bölümler · zaman damgaları video süresi içinde · 7 aday alanı dolu, tür listeden · tırnak içi alıntı ≤15 kelime.
- Jev: video başına ≤ segment+10 istek (paket, yalnız ekran sorusu; önbellekte p varsa 0); `jev tarama` ≤2 batch (toplu içinde); kare ≤6/video. Tahmini toplam maliyeti rapora yaz.
- `rapor-denetle` sözlük hücresi `?` olan aday satırlarını ad sözlüğüyle (skill katalogu · plugin · MCP · kayıt) yerinde doldurur; eşleşme yoksa `yok`.
- İşaret: sözlükte skill/plugin/MCP/yerleşik eşleşmesi ya da Jev çift p≥0.5 → ÇİFT · kayıt/ELE eşleşmesi → ÖNCEDEN-GÖRÜLDÜ · izin riski ≥2 ya da Jev yanıtı yok → BEKLE · kalan → UYGULA.
- Eski raporlar bir kez `video kayit --ice-al` ile kayda alındı; aynı id yeniden taranmaz (`--yeniden` zorlar).
