# TOKEN-10 — ajan açıklamaları sıkışır, tüm ajanlar listede kalır

## Ara rapor 1 (13 Eki, d1)
- Dağılım (tools/olcum/ajan_aciklama.py, çağrısız; docs/token-10/aciklama.tsv): kendi (repo kaynaklı) 493 ajan · 75 983 kr · ort 154 · medyan 149 · p90 205 · max 282 · >120: 382 · ≤90: 3. Kaynaksız (~/.claude/agents'ta repo dışı, agency-agents kopyaları) 87 · 19 237 kr · ort 221 — dokunulmadı (repo kaynağı yok, zip tutarlılığı sağlanamaz).
- Katkı: `<example>` blok 0; "Use when" 482 kez (kalıp), "including …"/"with or without files" ekleri 49. Büyük katkı tek tek uzun cümleler, blok değil.
- Üretim: tools/olcum/ajan_sikistir.py uret (4 parti = 4 claude -p sonnet, arka plan, günlük .kos/kopru/token-10-uret.log) → denetle (≤120 kr, tek satır, aile içi Jaccard ≥0.6 yok) → docs/token-10/esleme.tsv.
- Ara rapor 2 (d1 sonu): üretim parti 0–1 bitti (112+114, eksik 0), 2–3 arka planda. onay/token_10_uygula.py (--kuru/uygula/--geri; yalnız description satırı, CRLF/gövde bayt korunur, ':' JSON tırnaklı, yedek ~/.claude/agents-yedek-token10, ajan-getir katalog yenilenir) + tests/test_token_10_uygula.py 1/1 yeşil. aciklama_degistir ortak: tools/olcum/ajan_aciklama.py.
- Kapı: tools/olcum/kapi10.py (onek 2 çağrı; kapi 2 opus çağrısı, 30 görev = f2b 10 + f2c 10 + ek 10; kor/sonuc). claude -p sayacı: 4/14.
