# TOKEN-6c-R — recap ölçümü

KARAR: onay (2026-10-03 ~19:20), eklerle. Salt okuma: ayar/hook/Headroom değişmez · claude -p 0 · tur ≤8, 5'te sayaç, 7'de DUR.

Kabul:
- Mühür bas/son: settings · hooks · mcp sha, sayımlar, settings anahtar-başı sha (içerik); Headroom 3 alan sha8 ayrı satır, kaynak adıyla (GET /stats → log).
- scratchpad/k6cr.py: pencereler R (10-03 18:49:58 → şimdi), (b) 10-01 04:03 → 10-03 17:33:58 (bakT6c CreationTime), (a) 14 gün bilgi. Bantlar ≤1 · 1–4 · 4–60 · >60 dk. Sınıf: oturum eylemi · Headroom (mat/kmp) · tool_search_deferral · diğer · kanıtsız. frozen_message_count kolonu · runtime-env satırları → olcum/token-6c-r.json.
- Doğrudan recap testi: 4–60 dk çiftleri away_summary var/yok, (a) ve (b), oran + n. Hüküm: iki grup n≥10 & ≥2 kat → recap kırıyor (kapalı kalır, deneme biter) · n≥10 & fark yok → suçsuz (Ömer geri açar; bakT6c geri yüklenmez) · n<10 → yetersiz. R kapısı (<30 çift) beklenen.
- docs/token-6c-r.md · kapanış: mühür eşit · diff-filter=D · gitleaks · arşiv · push.

Durum:
- tur 1/8: mühür scratchpad/muhur-6cr-bas.json — settings d624c65b · hooks f226ffce · mcpServers 23452893 · plugin 47/53 · mcp 19 · skill 2068 (rglob SKILL.md; eski 1054 farklı yöntem) · Headroom: SHAPER yok (stats/log vermiyor) · HOLDOUT 4a8f8adf (log 18:27:07) · VERBOSITY yok.
- ölçüm ✓ b2a10f6: (b) 4–60 n=108 kırık 41 hepsi Headroom; recap testi var %76.7 (43) vs yok %12.3 (65) → recap kırıyor (Headroom üzerinden; Headroom hariç 0/10 vs 0/57). R n=1, kapı kapalı (beklenen).
- Sapma: ek sınıflar ttl_asimi ve arac_listesi şeffaflık için ayrı satır (4–60'ta 0).
- tur 5/8: docs/token-6c-r.md · kapanış.
- tur 6/8 kapanış: mühür son ↔ bas (aşağıda) · diff-filter=D boş · gitleaks · arşiv · push.
  settings d624c65bfad79cee EŞİT
  hooks f226ffce582b5bdc EŞİT
  mcpServers 23452893b846a828 EŞİT
  plugin [47, 53] EŞİT
  mcp 19 EŞİT
  skill 2068 EŞİT
  HEADROOM_OUTPUT_SHAPER {'kaynak': 'yok (stats ve log vermiyor)', 'sha8': None} EŞİT
  HEADROOM_OUTPUT_HOLDOUT {'kaynak': 'proxy-6768.log son runtime-env satırı 2026-10-03 18:27:07', 'sha8': '4a8f8adf'} EŞİT
  HEADROOM_VERBOSITY_LEVEL {'kaynak': 'yok (stats ve log vermiyor)', 'sha8': None} EŞİT
  settings anahtar farkı: []
  runtime-env log satırı 79
