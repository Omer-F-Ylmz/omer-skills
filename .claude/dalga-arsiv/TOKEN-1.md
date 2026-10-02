# TOKEN-1 — arka plan profili (L1 + L10)
KARAR
- Profil yalnız `claude -p` başlatma argümanını değiştirir; kurulu hiçbir şey silinmez, etkileşimli oturum aynı.
- Kapsam: MCP alt kümesi · skill listesi · SessionStart/UserPromptSubmit enjeksiyonu · promptCacheTtl 5m. Model/effort değişmez.
- Güvenlik hook'ları her profilde açık; disableAllHooks yok. Plugin enjeksiyonu `--settings` enabledPlugins false; jev-skill.ps1 CC_PROFIL'de erken çıkar.
- Profiller: tam (ek yok) · ttl (yalnız 5m; deney koşulu aynı, CC_PROFIL yok) · blender (MCP alt kümesi + skill'ler tek dosyada `--append-system-prompt-file` + 4 plugin kapalı + 5m).
- Bağlama: kur.py deney → ttl · hafif.py motor → ttl (+ usage sayıları olcum/motor-usage.jsonl) · tur medyanı ≤3 çağrı yerleri en az ttl (cc-kopru veriyle) · Blender kos.py → blender (kapıyı geçerse). CC_PROFIL_ZORLA=tam geri alır.
- Motor kapı koşusu yok (yalnız TTL); prob yeter. B-fincan kapısı taban koşusunun tur tavanıyla; kos.py.bakT1 yedeği, diff docs/token-1.md'ye.
Kabul
- ≥12 test yeşil, kırmızı-önce commit; mutasyon: disableAllHooks · ${VAR} açılır · ttl atlanır → kırmızı.
- Prob ≤4: init (MCP · skills 0 · plugin) + usage ephemeral_1h 0 / 5m>0; ilk ctx ≤50k.
- B-fincan kapı 1 koşu: kör ≥3.6 · uygunluk ≥3 · $ · tur (taban 115 · $9.60); karar omer-kurallar 24.
- settings.json + ~/.claude.json mcpServers hash eşit; hooks klasörü jev-skill.ps1 dışında eşit; skill/plugin/MCP sayıları eşit; diff-filter=D boş.
- Tam suit: 195 main · 497 video · 81 jev · 176 cc-kopru · 40 mcp-jev · 22 dotnet + yeni; gitleaks temiz; env değeri yok.
Durum
- [x] K1 · [x] K2 · [x] K5 kur.py+hafif ttl · [x] K0 video 500/500 · [x] cc-kopru ttl · [x] token_olc $ + motor · [x] cowork profilde · [x] kos.py --profil (bakT1) · [x] mühür + D-boş + gitleaks · [ ] K3 prob (betik: scratchpad 7ca267ef…/prob_t1.py) · [ ] K4 B-fincan · [ ] arşiv — DUR: TOKEN-1b tur tavanı (~59 > 40) · TOKEN-1c tur 21/25: KAPANDI · prob 4/4 · kapı SOR → blender tam · gitleaks ağaç 20/20 yanlış alarm
