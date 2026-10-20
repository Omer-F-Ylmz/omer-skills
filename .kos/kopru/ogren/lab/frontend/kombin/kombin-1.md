# kombin-1 — tasarım yığını zinciri (ÖĞREN-2 d3, G1; d3'te yeniden koşuldu)
- İş türü: referans siteden yeni sayfa tasarımı → kod. Dosyalar: lab\frontend\kombin\k1\
- Zincir: (1) ref.mjs playwright headless referans ölçümü (linear.app: bg rgb(8,9,10) · h1 64px/510 · gövde 16px; yalnız stil, varlık yok) → (2) yon.mjs üç yön PNG (yon-a/b/c) → (3) seçilen yön A → DESIGN.md (token + yerleşim 1440x900) → (4) hero.p1.html (pass 1) → (5) diff.mjs: pixelmatch + h1/p/cta ölçüsü + en kötü 100px şeridi → (6) düzelt → yeniden diff (≤4 tur).
- Devir noktaları: ölçüm → DESIGN.md (metin/sayı, görüntü yok); DESIGN.md → kod; her tur çıktısı tek JSON satırı (diffPct, metrics, worstBand), PNG'ye bakılmaz.
- Token-verimli sürüm: kod turu başına yalnız diff JSON okunur (~200 bayt); PNG Read ile açılmaz.
- Desktop/CC: ölçüm + kod + diff = CC (yerel, headless); yön seçimi (3 PNG'ye bakış) ve son estetik yargı = Desktop (tek ekran görüntüsü).
- KOŞU KANITI (d3, `node dd-tmp.mjs`, yon-a.png'ye karşı pixelmatch 1440x900 eşik 0,1): ref 0 % · t1 7,51 % · t2 0 % · t3 0,03 % · t4 0,05 %. `diff.mjs hero.p1.html t1` → h1 [top 220, h 134, w 712] · p [378,54,520] · cta [472,47,712] · worstBand 100 px. 1. turda %7,51 → 2. turda %0 (sayıyla diff yöntemi çalıştı; t3/t4'teki 0,03–0,05 % kaymanın nedeni kayıtlı değil).
- Görsel yargı adımı (pixeljury claude-code + ollama qwen3.5:4b + kendi bakış): d3'te DENENMEDİ — pixeljury puanı bu kartta yok; yalnız piksel diff ölçüldü.
- Tuzak: diff yalnız yön-A PNG'sine yakınlığı ölçer, tasarım kalitesini değil; yon-b/c ile karşılaştırma yapılmadı. Font Inter yerine system-ui yedek (DESIGN.md) → harf genişliği farkı beklenir.
