# ORDU-1 d3 (21 Eki) — kapı koşulmadı, bayrak kapalı
Hazır: `ordu.kapi3` (Claude alt iş ≤%50 · ağırlıklı token ≤%60 · kalite ≥ A; ağırlık Haiku 1/3 · Sonnet 1 · Opus 5/3 = liste fiyat oranı varsayımı), `tools/olcum/ordu_olc3.py` (zor/imkansız işler ücretsizden başlar, Sonnet/Opus çekirdeği taslakla; orta işte iki aile çapraz; Claude çağrısı iş başı ayrı oturum, tavan 12), T1 zincirinde `gemini/gemini-3.1-flash-lite` (2.5-flash OmniRoute'ta 404; 3.8/3.5/flash-latest 400).
Çelişki: 20 iş × ayrı oturum A kolunda tek başına 20 çağrı > tavan 12 → A, d2 toplu yanıtlarından + bir kalibrasyon çağrısıyla ölçülen oturum yüküyle modellenir (ölçüm değil model; raporda belirt).
Koşmak: `.claude/ordu3/cikti` (d2 önbelleği kopyalı) → `python tools/olcum/ordu_olc3.py .claude/ordu3/cikti` (ayrıntı: dosya başlığı). Koşulmadığı için ★ d4'te.
Ölçüm aracı düzeltmesi: I1 yarış testi (`SINIRLI_TEST`) kilitsiz yanlış çözümü bazen kabul ediyordu → 30 tur + switchinterval 1e-6; hâlâ ~1/6 koşuda kaçırıyor.
