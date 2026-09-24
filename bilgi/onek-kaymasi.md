---
iddia: CC oturum açılışında önbellek öneki 17.565. token'da (araç bloğu sonu) ayrışır; oturum başına ~76k yeniden yazılır
kaynak: docs/olcumler/onek-kaymasi.md
guven: yüksek
dogrulama: https://github.com/Omer-F-Ylmz/omer-skills/blob/main/docs/olcumler/onek-kaymasi.md
tarih: 2026-09-24
bayatlama: 2026-12-23
etiketler: onbellek, onek, olcum
---
Art arda iki özdeş `claude -p` ikisinde de cache_read 17.565 okudu, ~77k yazdı. 233 oturumun medyan ilk-istek yazımı 76k. Muhtemel sebep: sistem metnindeki oturuma özel scratchpad yolu (güven orta; doğrulama docs/kurulumlar/bekleyen/onek-sabitle.md).
