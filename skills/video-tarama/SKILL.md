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
2. video ozet <id...>                   # ≤4 eşzamanlı; altyazı önbelleğe (C:\Projeler\.video-cache\<id>\) · exit 4 (YouTube hız sınırı) → o video "ertelendi", diğerleriyle devam
3. video paket <id> [--kare 6]          # her id; tek satır: paket.md yolu · kare yolları · ~token · Jev istek (yalnız ekran sorusu, p önbellekte varsa 0)
4. Her dalga için dalgadaki id başına bir Agent çağrısı, aynı mesajda (subagent_type: video-tarayici — sonnet, yalnız Bash/Read/Write). Tanım yüklü değilse general-purpose'a DÜŞME: DUR, yeni oturum.
   Prompt yalnız videoya özgü tek satır: `id: <id> · paket: <yol> · kareler: <yollar> · rapor: docs/video-tarama/<tarih>-<id>.md`.
   Sabit görev metni (adımlar · kurallar · rapor şablonu) alt ajan tanımında (.claude/agents/video-tarayici.md): sistem metninin parçası, paralel alt ajanlar önbelleği paylaşır. Aynı anda en fazla 3 alt ajan.
5. video toplu <rapor.md...> [--istek-tavan M]  # tekille · sözlük eşleşmesi · kural karşılaştırması (ipucu/iş akışı) · jev tarama (≤2 batch) · işaret · <tarih>-toplu.md · kayit.jsonl (yalnız rapor-denetle'den geçen)
6. Sohbete: toplu'nun çıktısı (≤25 satır: video başına 1 satır + adaylar işaretiyle) + "atlandı: N" + "ertelendi: id…" + tahmini maliyet.
```

Videoda site/UI yapım promptu görünürse (ekranda ya da anlatımda) alt ajan onu `tur: prompt` aday olarak yazar (m:ss ile); prompt metni kopyalanmaz, anatomisi video-uygula'da çıkarılır.

Ana ajan paket.md, altyazı dosyası ya da segmentler.jsonl açmaz; alt ajan dönüşü dışında rapor gövdesi okumaz.

## Süzgeç varsayılanı: kapalı (12b ölçümü)

2 videoda süzgeçli okuma, tam okumanın adaylarının %74'ünü buldu (gevşek ad eşleşmesiyle; katı eşleşmeyle %55). Kabul eşiği %90 olduğu için
`video oku` ve `video paket` varsayılan olarak tüm segmentleri okur (paket dolgu sözcüklerini ve ardışık tekrarları atar). Süzgeç yalnız segmentlerin ~%10'unu atlıyordu, yani kazancı da küçüktü. Tekrar ölçmeden varsayılanı değiştirme.

## Denetim ve tavanlar

- `video rapor-denetle`: zorunlu bölümler · zaman damgaları video süresi içinde · 7 aday alanı dolu, tür listeden (skill · plugin · MCP · CLI · teknik · iş akışı · ipucu) · `## İddialar` zorunlu (17: iddia · zaman · tür ∈ sayısal/özellik/karşılaştırma/öneri) · tırnak içi alıntı ≤15 kelime · 23: frontend/site içerikli videoda `## Site/UI teknikleri` (teknik · kanıt m:ss · kütüphane ya da `tahmin:` · bizde).
- Jev: video başına ≤ segment+10 istek (paket, yalnız ekran sorusu; önbellekte p varsa 0); `jev tarama` ≤2 batch (toplu içinde); kural karşılaştırması ipucu/iş akışı aday başına ≤2 istek (`--istek-tavan` varsayılanı 2·aday+2+2·ipucu); kare ≤6/video. Tahmini toplam maliyeti rapora yaz.
- `rapor-denetle` sözlük hücresi `?` olan aday satırlarını ad sözlüğüyle (skill katalogu · plugin · MCP · kayıt) yerinde doldurur; eşleşme yoksa `yok`.
- Kural karşılaştırması: tür ipucu/iş akışı aday `video kurallar` önbelleğine (global CLAUDE.md + C:\Projeler\omer-kurallar.md; madde düzeyi, mtime'la yenilenir) karşı sınanır: aşama 1'in birinci seçimi (hiçbiri değilse) ve aşama 2 p≥0.5 → ÇİFT; tabloda `ÇİFT (kural: omer-kurallar:N)` görünür (N dosya satırı). Araç türleri kurala girmez.
- İşaret: sözlükte skill/plugin/MCP/yerleşik eşleşmesi ya da Jev çift p≥0.5 → ÇİFT · kayıt/ELE eşleşmesi → ÖNCEDEN-GÖRÜLDÜ · izin riski ≥2 ya da Jev yanıtı yok → BEKLE · kalan → UYGULA.
- Eski raporlar bir kez `video kayit --ice-al` ile kayda alındı; aynı id yeniden taranmaz (`--yeniden` zorlar).

## ÜRETİLEBİLİR ipucu (23b)
- Aday tür/ne sütununda token tasarrufu vaat eden özellik varsa hedef türü (skill · talimat · araç ayarı) yazılır; video-uygula bunu `hedef_tur:` alanına taşır, skill/talimat olanlar `## ÜRETİLEBİLİR`'e düşer.
