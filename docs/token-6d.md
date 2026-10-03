# TOKEN-6d — Headroom çıktı kısaltma (proxy_output_shaper) A/B

**Karar: ölçülebilir tasarruf yok → kalıcı açma yok, çıktı kısaltma kapalı kalır.** İki görevde de çıktı token ve $ farkı gürültü bandının içinde; kör puan farkı da bant içinde.

## Mekanizma kanıtı
- Kol anahtarı: Desktop yalnız süreç ortamında `proxy_output_shaper` süzülerek başlatıldı (`.claude/token6d/hr_deney_baslat.ps1`; User env'e dokunulmadı). Koşu başına `POST /admin/runtime-env` `HEADROOM_OUTPUT_HOLDOUT` 0 = T (shaper), 1 = C (kontrol); koşu sonunda başlangıç değeri geri yazıldı.
- K1 (`olcum/token-6d-k1.json`): T probunda tek opus isteğine `OutputShaper(L2/env)` uygulandı; kontrol kolu kodla (`assign_arm` holdout ≥ 1 → control, shaper yalnız treatment).
- K2 ampirik kol kanıtı (proxy log penceresi): T koşularında 35/36 istek `['output_shaper:verbosity:L2']` etiketli (etiketsiz olan bir sonnet isteği), C koşularında 0/26.

## Kol sonuçları
| görev | başarı T · C | kör puan /9 T · C | çıktı token T−C | $ T−C |
|---|---|---|---|---|
| rtk-ab kısa, 2T+2C (`olcum/token-6d-k2-kisa.json`) | 2/2 · 2/2 | 7.5 (8, 7) · 8.5 (8, 9) | T %2.4 fazla | T %13.4 fazla |
| kur.py orta, 1T+1C (`olcum/token-6d-k2-orta.json`) | 1/1 · 1/1 | 9 · 8 | T %2.3 az | T %2.1 az |

- Orta görev kabul testleri `olcum/token6d/test_orta.py` (ana suite dışı) önce kırmızı (5 failed, 3 passed, `33b2bd5`); iki kol da 8/8 kabul + 500/500 tools/video suite; tavana takılan yok (--max-turns 40).
- Kör puan (`olcum/token-6d-kor.json`): okuyucu (sonnet), kol adları gizli 6 kopya, 0–3 × doğruluk · eksiksizlik · kalite; eşleme puanlama bittikten sonra açıldı. rtk T2 (7): şablon testi kaldı → 5 test (eksiksizlik 2).

## Gürültü bandı
rtk-ab aynı kolun iki koşusu arası fark (büyüğü): çıktı token %31.8 · $ %64.2 · kör puan %13.3. Kollar arası farklar (çıktı −%2.4 / +%2.3 · $ −%13.4 / +%2.1 · kör puan −%11.8 / +%12.5) hepsi bant içinde → "gürültü içinde".

## Karar (omer-kurallar madde 21)
Düşüş = max(kör puan, görev başarısı göreli düşüşü) bant içinde → 0; başarı düşmedi. Tasarruf ölçülemedi (bant içinde, eşik %25'in çok altında) → AL değil. Kalıcı açma yapılmaz; `HEADROOM_DISABLE_FEATURES` User kaydında `proxy_output_shaper` kalır, auto-learning kapalı.

Yeniden denemek gerekirse kalıcı açma yolu: User env `HEADROOM_DISABLE_FEATURES`'tan `proxy_output_shaper`'ı çıkar → Desktop'u tepsiden Quit + yeniden başlat. Geri alma: değeri geri ekle → Desktop'u yeniden başlat. Her ikisi Ömer onayıyla.

## Deney kapatma kanıtı
Desktop Quit + `hr_deney_bitir.ps1` (18:36:02): `/stats` rollout `proxy_output_shaper` disabled=True · enabled=False · decision=disabled; runtime-env `HEADROOM_OUTPUT_SHAPER` · `HEADROOM_OUTPUT_HOLDOUT` · `HEADROOM_VERBOSITY_LEVEL` sha8 başlangıçla EŞİT; restart sonrası 8 istekte OutputShaper 0.
