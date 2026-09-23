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
3. video suz <id> --istek-tavan <segment+10>   # her id; ekran p'si kare --suzgecten için; Jev ≤ segment+14/video
4. Her dalga için dalgadaki id başına bir Agent çağrısı, aynı mesajda (subagent_type: video-tarayici, model sonnet;
   yoksa general-purpose + sapma notu). Dalga bitmeden sonrakini başlatma → aynı anda en fazla 3 alt ajan.
5. video toplu <rapor.md...>            # tekille · sözlük eşleşmesi · jev tarama (≤2 batch) · işaret · <tarih>-toplu.md · kayit.jsonl
6. Sohbete: toplu'nun çıktısı (≤25 satır: video başına 1 satır + adaylar işaretiyle) + "atlandı: N" + tahmini maliyet.
```

Ana ajan `video oku`, altyazı dosyası ya da segmentler.jsonl açmaz; alt ajan dönüşü dışında rapor gövdesi okumaz.

## Alt ajan görevi (sabit metin; `<id>`, `<tarih>` doldurulur)

> Video `<id>` için tarama raporu yaz. Adımlar:
> 1. `video oku <id>` → künye, chapter başlıkları, linkler (linkler.json) ve segmentler (varsayılan tam; `--suzgecli` yalnız okunacaklar).
> 2. `video kare <id> --suzgecten --en-fazla 6` → çıkan her kare yolunu Read ile gör.
> 3. `docs/video-tarama/<tarih>-<id>.md` yaz (şablon aşağıda). Adayları ELEME: videoda anılan her skill, plugin, MCP, CLI, teknik, iş akışı bir satır.
>    Sözlük sütunu için `video adlar --eslestir "<ad>" …` (tek çağrıda hepsi); eşleşme yoksa "yok".
> 4. `video rapor-denetle <rapor>` GEÇTİ diyene kadar düzelt (en fazla 2 düzeltme denemesi; geçmezse hataları dönüşe yaz).
> 5. Yalnız şunu dön: `rapor: <yol> · aday: <n> · <1 satır özet>` (≤5 satır). Altyazı alıntılama, rapor gövdesini dönme.

## Rapor şablonu

```markdown
# <başlık>
## Künye
başlık · kanal · süre: m:ss · dil · url
## Özet
5-10 satır, Türkçe.
## Bölümler
- m:ss <bölüm> — ne anlatılıyor (zaman damgalı)
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| <ad> | <eşleşen ad (kaynak, skor)> ya da yok | skill/plugin/MCP/CLI/teknik/iş akışı (yerleşik komut → CLI) | açıklamadan ya da kareden; yoksa "yok" | … | m:ss | kendi cümlenle; alıntı “…” ≤15 kelime |
## Kareden okunanlar
- m:ss ekranda okunan komut/ayar/ad
## Belirsizlikler
- ASR'den şüpheli adlar, doğrulanamayan iddialar
## Atlanan segment oranı
atlanan/toplam (video oku ilk satırı)
```

## Süzgeç varsayılanı: kapalı (12b ölçümü)

2 videoda süzgeçli okuma, tam okumanın adaylarının %74'ünü buldu (gevşek ad eşleşmesiyle; katı eşleşmeyle %55). Kabul eşiği %90 olduğu için
`video oku` varsayılan olarak tüm segmentleri okur. Süzgeç yalnız segmentlerin ~%10'unu atlıyordu, yani kazancı da küçüktü. Tekrar ölçmeden varsayılanı değiştirme.

## Denetim ve tavanlar

- `video rapor-denetle`: zorunlu bölümler · zaman damgaları video süresi içinde · 7 aday alanı dolu, tür listeden · tırnak içi alıntı ≤15 kelime.
- Jev: video başına ≤ segment+14 istek; `jev tarama` ≤2 batch (toplu içinde); kare ≤6/video. Tahmini toplam maliyeti rapora yaz.
- İşaret: sözlükte skill/plugin/MCP/yerleşik eşleşmesi ya da Jev çift p≥0.5 → ÇİFT · kayıt/ELE eşleşmesi → ÖNCEDEN-GÖRÜLDÜ · izin riski ≥2 ya da Jev yanıtı yok → BEKLE · kalan → UYGULA.
- Eski raporlar bir kez `video kayit --ice-al` ile kayda alındı; aynı id yeniden taranmaz (`--yeniden` zorlar).
