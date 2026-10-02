# TOKEN-0 — token haritası + ölçüm tabanı
KARAR: yalnız ölçüm. settings.json, ~/.claude.json, hooks, skill, plugin, MCP, Headroom ayarı DEĞİŞMEZ; hiçbir şey SİLİNMEZ.
Birim: ağırlıklı token = girdi×1 + cache okuma×0.1 + cache yazma (5m×1.25, 1h×2) + çıktı×5.

Kabul
- token_olc testleri yeşil; kırmızı-önce commit görünür; iki mutasyon kırmızı.
- K2 ≤8 claude -p; her varyant tabloda; atlanan gerekçeli.
- Mühür eşit: settings.json · ~/.claude.json mcpServers · ~/.claude/hooks; skill/plugin/MCP sayıları aynı.
- `git diff --diff-filter=D <baş>..HEAD` boş; env değeri yok; gitleaks (docs+olcum) temiz.
- Tam suit yeşil (183 main · 497 video · 81 jev + yeni).
- Rapor ≤15 satır.
Düzeltmeler (kullanıcı): K2 7 varyant `--output-format stream-json --verbose`, usage son result satırı, etki init satırından kanıt (b mcp 0 · c slash/skill 0 · d hook yok · e sonnet-5-5), kanıtsız varyant "etkisiz"; JSON argüman Bash/geçici dosya. K3+K4 tek sonnet subagent, workflow/doğrulayıcı yok. Kapanış: dalga.md → .claude/dalga-arsiv/TOKEN-0.md (silinmez).

Durum
- [x] 1 açılış mührü (scratchpad/muhur-bas.json, HEAD 1a41264)
- [x] 2 K1 kırmızı commit f55b67e
- [x] 3 K1 yeşil bef27ea + 2 mutasyon kırmızı
- [x] 4 K1 koşu: 475.88 M/14g · olcum/token-0.json
- [x] 5 K2 7 çağrı $4.10 · olcum/token-0-k2.json · hepsi init kanıtlı
- [x] 6 K3+K4 tek sonnet subagent
- [x] 7 K5 docs/token-0.md (148 satır)
- [x] 8 suit 497/81/195/176/40/22 yeşil · gitleaks temiz · silinen yok · mühür: settings/mcpServers/sayılar eşit; hooks/ farkı yalnız .headroom-guard-verdict.json (SessionStart guard çalışma durumu, K2 çağrıları yazdı)
