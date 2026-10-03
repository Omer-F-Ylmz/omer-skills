# TOKEN-4a — tur + araç çıktısı: ölçüm ve tasarım (L7 · L8 · L14)
KARAR
- Ayar/hook/skill/plugin/MCP dosyası değişmez; silme yok; yalnız ölçüm + tasarım.
- Rehber okuması (skills/**, plugins/**/skills/**, references/**) hiçbir tasarımda kısıtlanmaz.
- K3'te workflow/doğrulayıcı ajan yok; sayılar testli token_olc çıktısından aktarılır.
- Headroom kalibrasyonu: oturum katsayısı k = (gerçek ctx − taban) / transcript büyümesi (taban transcript'te yok, iki taraftan düşülür); katkı ham + düzeltilmiş yan yana; L8 tasarrufları düzeltilmişle, Headroom örtüşmesi ayrı satır; katsayı testli.
- Tur tavanı 25; her 5 turda sayaç; 21. turda bitmediyse kalan yazılır, DUR. Her madde commit; push en sonda.
Kabul
- K1 ≥8 test (+≥1 katsayı), sentetik jsonl; kırmızı-önce commit ayrı; mutasyon (offset/limit) ≥1 kırmızı.
- K2 olcum/token-4a.json + olcum/token-4a.md: 4 kategori + en büyük 10 kaynak (ağırlıklı katkı, pay).
- K3 docs/token-4a.md: L8a/L8b/L8c/L7/L14/headroom (TOKEN-6 notu) + TOKEN-4b kapısı.
- Mühür dalga başıyla eşit (Headroom 3 alan ayrı satır), kurulum eşit, diff-filter=D boş, gitleaks temiz, tests suite yeşil (pipefail).
- dalga.md → .claude/dalga-arsiv/TOKEN-4a.md; commit + push; rapor ≤8 satır.
Durum
- Tur 5: plan onaylı; mühür .claude/token2/muhur-4a.json; K1 başlıyor.
- Tur 16 kapanış: K1 7b8b8e9 (kırmızı 12) → e99d466 yeşil → 7092f13 k düzeltmesi (pytest 31/31; mutasyon offset/limit hep-yanlış 1 · hep-doğru 3 kırmızı) · K2 51dcd00 (14 gün · 2150 dosya · 508.0 M · k genel 1.37 / medyan 2.04) · K3 08c6f2a.
- İlk 3 kaynak (düz katkı payı): Bash sed %0.90 · cat %0.82 · python %0.50. Kaldıraç düz M/gün: L14 0.501 · L8a(300) 0.165 · L7 0.074 · L8b 0.030 · L8c 0.004 (uygulanmaz).
- Mühür EŞİT (env.ANTHROPIC_BASE_URL · env.ENABLE_TOOL_SEARCH · hooks.SessionStart var, settings özeti eşit) · kurulum skill 1054 · mcp 19 · plugin 47/53 eşit · diff-filter=D 0 · gitleaks staged+log 0 · suite video 500 · jev 81 · tests 270 · cc-kopru 178 · mcp-jev 40 · jev-dotnet 22 (pipefail, kırmızı yok).
