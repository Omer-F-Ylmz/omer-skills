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

## İkinci bölüm — BLENDER-REHBER (2026-10-02)

SKILL.md zorunlu akıştan rehbere (78 → 58 satır): 8 aşama, ≤3 eleştiri turu, aşama başı dogrula, zorunlu kanıt sayfası çıktı; durma kuralı (v1 + kapı → ≤1 iyileştirme turu) ve görüntü disiplini (≤512 px, ≤3 Read) girdi. skill_denetim 0 hata · tetik olumlu 5/5, olumsuz 0/3 (mod-atolyesi · threejs-bloom · gorsel-uret) · senkron sha eşleşti (26 dk).

| Koşu | Teslim | Tur | Süre | Maliyet | Kapı | GLB | Puan ort (5) | Uygunluk |
|---|---|---|---|---|---|---|---|---|
| A-fincan-v3 | evet (msg 17) | 60 | 22.5 dk | $4.98 | geçti | 111.5 KB | 3.6 | 2 |
| B-fincan-v3 tekrar | evet (msg 38) | 101 | 33.6 dk | $12.26 | tablo.json: geçmedi (1 glb bulgusu) | 156 KB | 4.0 | 4 |
| B-fincan-rehber | evet (msg 46) | 115 | 28.0 dk | $9.60 | geçti, 0 bulgu | 83.6 KB | 3.6 | 3 |

Kör puan: üç render tek sonnet çağrısında, rastgele ad; 5 ölçüt + uygunluk 0-5 (Türk kahvesi fincanı: konik/ince gövde, ayak halkası, küçük hacim; tabak çukurlu). Aynı A render'ı ilk bölümde 3.4, burada 3.6: puanlayıcı oynaklığı ±0.2.

K5: teslim ✓ · kapı ✓ · maliyet $9.60 > $6.5 ✗ · puan 3.6 ≥ A 3.6 ✓ · uygunluk 3 > A 2 ✓ → **DUR** (maliyet).

Maliyet dağılımı (B-fincan-rehber, 83 asistan mesajı; ağırlık = girdi + 1.25×önbellek yazma + 0.1×önbellek okuma + 5×çıktı): execute_blender_code %30.4 · Bash %24.0 · Read %10.4 · Edit %8.6 · get_objects_summary %7.4 · Grep %5.3.
En pahalı 5 adım: #32 get_objects_summary (tek çağrı) %7.4 · #14 Grep (blender_pisir argümanları/GPU) %3.7 · #1 Skill yükleme (oturum + üretim) %3.5 · #20 headroom_retrieve + `rtk proxy python` araç %2.5 · #24 headroom_retrieve %2.2.

Gözlem: durma kuralı tuttu (bitiş success; B tekrar max_turns'te bitmişti), maliyet B tekrara göre −%22. v1 teslimi geç kaldı (msg 46 / 83; A'da 17). Pahalı tekil adımlar teslim öncesi keşif: sahne özeti dökümü, araç argümanı Grep, headroom retrieve.

Çelişki: ilk bölüm B tekrar için "kapı geçti" diyor, tablo.json (kor.py) aynı koşu için kapi=False + 1 glb bulgusu veriyor; bu dalgada çözülmedi.

Karar: DUR. Rehber hâli repoda ve claude.ai'de duruyor (geri alınmadı); KABUL maliyet koşulunda tutmadı. Ek koşu yok.
