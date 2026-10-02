# blender-uretim ölçümü (BLENDER-OLCUM · 2 Eki 2026)

Soru: senkron blender-uretim skill'i, skill'siz koşuya göre fincan üretimini iyileştiriyor mu?
Düzenek: `claude -p` varsayılan model (opus-5-5), aynı brief (Türk kahvesi fincanı + tabak). Tek fark A = blender-uretim kapalı (hook ile engel, içerik erişimi 0) / B = açık; blender-oturum ikisinde açık. Kör puan: sonnet, rastgele dosya adı, 5 ölçüt 0-5. Kanıt: `Desktop\blender-kum\olcum\`.

| Koşu | Teslim (asistan msj) | Tur | Süre | Maliyet | Kapı | GLB hat | Kör puan |
|---|---|---|---|---|---|---|---|
| A-fincan-v3 | evet (17) | 60 | 22.5 dk | $4.98 | geçti, 0 bulgu | 105 KB | 3.4 (ilk puanlama 3.6) |
| B-fincan-v3 ilk | yok (GLB msj 84, `--glb` döngüsü) | 101 (sınır) | 55.9 dk | $9.74 | geçti, 0 bulgu | — | 0 (kural: teslim yok) |
| B-fincan-v3 tekrar | evet (38) | 101 (sınır) | 33.6 dk | $12.26 | geçti, 0 bulgu | 131 KB | 3.4 |

B tekrar öncesi düzeltmeler: "önce teslim" sırası (ilk render → hemen GLB → `dogrula --glb`) + bekçi `bpy.data.libraries.write` reddi (B ilk koşunun çökme izi).

## Dört ölçüt (B tekrar)
- Teslim var — geçti
- Kapı (`blender_dogrula`) geçti — geçti
- Kör puan ≥ A + 0.3 (≥ 3.9) — **tutmadı** (3.4 = A)
- Maliyet ≤ 1.5 × A (≤ $6) — **tutmadı** ($12.26 = 2.5 × A)

## Turu/maliyeti yiyen ilk 5 adım (B tekrar, 100 asistan mesajı; maliyetin %60'ı teslimden sonra)
1. Sahne kodu (bpy düzeltmeleri) — maliyetin %29'u, 25 çağrı (13'ü teslim sonrası)
2. Render — %26, 22 çağrı (21'i teslim sonrası; "ikinci render yok" kuralına rağmen)
3. Bash yardımcıları (dosya/süreç) — %12, 16 çağrı
4. Render görselini okuma (Read .png) — %11, 17 çağrı (16'sı teslim sonrası)
5. `blender_dogrula` tekrarları — %9, 14 çağrı
B ilk koşuda teslimden önceki sahne kurma baskındı (%45, 39 çağrı). Ölçer: transkript kullanım alanı, mesaj başına ağırlık (girdi + önbellek + 5 × çıktı), çağrılara eşit bölünmüş.

## Görsel not (Desktop Claude)
B biçimde brief'e daha sadık: konik gövde, ayak halkası, çukurlu tabak. A kupa + düz tabak görünümünde. Kör puanlayıcının genel ölçütleri bunu ayırt etmedi (biçim 3 vs 2, ortalama eşit 3.4) → sonraki ölçümde brief'e özel biçim ölçütü (ör. "konik gövde · ayak halkası · tabak çukuru" maddeleri).

## Karar
Zorunlu akış (8 aşama + ≤3 eleştiri turu + aşama başı doğrulama + kanıt paketi) turu bitiriyor ve maliyeti 2.5 katına çıkarıyor; kaliteyi genel ölçütle artırmıyor. blender-uretim **"kısa rehber"** moduna geçecek (ayrı dalga). Bu dalgada skill yalnız libraries.write ve önce-teslim satırlarıyla kalır.
