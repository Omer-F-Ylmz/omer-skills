# TOKEN-1 — arka plan profili (L1 + L10) · 2 Eki 2026 · DURUM: TOKEN-1b kısmi — K3 prob + K4 kapı bekliyor (tur tavanı)

## 1. Envanter — `claude -p` çağrı yerleri (14 gün, 244 sdk-cli oturumu, observer hariç, message.id tekil)
oturum · MCP · skill · tur medyanı · 1h/5m cache yazma · ağırlıklı
- tools/cc-kopru/sunucu.mjs:177 ajan (sonnet-5): 15 · — · — · 1 · 534k/0 · 1.17 M
- tools/cc-kopru/tasarim.mjs:36 + araclar/sema-yakala.mjs:54 tasarım aktarıcı (haiku, zaten `--setting-sources ""`): 6 · claude-design 4 · — · 1 · 37k/0 · 0.11 M
- tools/video/video/hafif.py:29 motor: `--no-session-persistence` → 0 oturum görünür (K5: usage sayıları olcum/motor-usage.jsonl)
- tools/video/video/kur.py:618 deney A/B (sonnet-5): 99 · — · — · 2 · 7.75 M/0 · 17.30 M
- Desktop/blender-kum/olcum/betik/kos.py:128 Blender (opus-5-5, repo dışı): 10 · blender 171, headroom 14 · blender-oturum 10, blender-uretim 6 · 45.5 · 2.88 M/0 · 19.30 M
- Eşlenemeyen kısa opus istemleri (skill tetik testi olası): 48 · — · blender-oturum/uretim, mod-atolyesi… · 2 · 4.14 M/0 · 8.84 M
- Ölçüm probları (ok/OK, haiku ok): 54 · — · — · 1 · 2.83 M/0 · 5.96 M
Bütün gruplarda 5m yazma ≈ 0: kısa çağrılar 1h TTL ödüyor (L10).

## 2. Profiller (profiller/cc-arka.json · tools/cc_profil.py)
- tam: ek argüman yok. CC_PROFIL_ZORLA=tam her profili buna çevirir.
- ttl: yalnız `--settings {"promptCacheTtl":"5m"}`; MCP/skill/plugin/hook aynı, CC_PROFIL yok (deney koşulu aynı). Bağlı: kur.py deney (kol env'i aynı --settings'te birleşir) · hafif.py motor.
- blender: `--strict-mcp-config` + blender, headroom (~/.claude.json girdisi olduğu gibi) · `--disable-slash-commands` + blender-oturum/uretim SKILL.md tek `--append-system-prompt-file` · enabledPlugins false: claude-mem, superpowers, ponytail, everything-claude-code · 5m · CC_PROFIL=blender (jev-skill.ps1 erken çıkar). Henüz bağlı değil (K4 kapısı bekliyor).

## 3. Açık
- K3 prob (≤4), K4 B-fincan kapısı (tavan taban ile aynı: kos.py `--max-turns 100`; taban num_turns 115 aynı tavanla), cc-kopru ajan ttl (medyan 1 ≤ 3), token_olc $ sütunu + motor kaynağı, tam suit, arşiv.
- Ek A fiyat eksikleri: sonnet-5.5 yazma fiyatı, opus-5 · sonnet-5 · haiku-4-5 → resmi sayfa.
- omer-kurallar.md madde 24 "tasarruf ayrıştırma"; "kalite takası tablosu" yok (satır 23 "takas" okunmadı) → karar ölçütü netleşmeli.
- claude-mem-cowork@thedotmack etkin görünüyor (hafıza "kapalı" diyor); blender profiline eklenmeli mi, kanıtla.

## 2. TOKEN-1b (2 Eki, 18:10–18:30)
- K0: video 500/500 (pytest exit 0). kur.py deney argv'sinde ttl `--settings` artık `--output-format json`'dan hemen sonra, `*ek`'ten önce; B = A + append yapısı korunur (test_kalite:129 bu sırayla değişmeden yeşil). test_girdi:66 + test_kur:224 beklenen argv'ye ttl eklendi. suite-kosucu komutları `set -o pipefail` + çıkış kodu.
- cc-kopru ajan → ttl: sunucu.mjs argv sonunda tek `--settings {"promptCacheTtl":"5m"}`, CC_PROFIL_ZORLA=tam kaldırır. Kırmızı 4/7 → yeşil 178/178. Mutasyon 1h → 4 kırmızı. Sapma: ajan-argv'deki 3 sabit argv beklentisine TTL eklendi (video ONAY'ıyla aynı desen; ayrı onay alınmadı).
- blender profili: pluginKapat'a claude-mem-cowork@thedotmack eklendi. settings.json:497'de zaten `false`; "etkin görünüyor" gözleminin kaynağı prob olmadan kanıtlanamadı, etkileşimli ayara dokunulmadı.
- token_olc: `FIYAT` ($/MTok girdi · okuma · 5m · 1h · çıktı; kaynak platform.claude.com/docs/en/about-claude/pricing, 2 Eki 2026): opus-5-5 4 · 0.20 · 5 · 8 · 20 · opus-5 5 · 0.50 · 6.25 · 10 · 25 · sonnet-5-5 2 · 0.20 · 2.50 · 4 · 10 · sonnet-5 2 · 0.20 · 2.50 · 4 · 10 (dipnot 3: $2/$10 standart) · haiku-4-5 1 · 0.10 · 1.25 · 2 · 5. En uzun önek; fiyatsız model → `fiyatsiz_istek` sayacı. `--motor olcum/motor-usage.jsonl` ayrı "motor" kaynak satırı (fiyat tablodan; kayıttaki usd kullanılmaz). 5 yeni test, 17/17; tek fiyat mutasyonu ×4 → her biri ≥1 kırmızı.
- kos.py (repo dışı; yedek kos.py.bakT1 yerinde), `--profil <ad>` (varsayılan tam = eski davranış):
```
+sys.path.insert(0, r"C:\Projeler\omer-skills\tools")
+import cc_profil  # TOKEN-1: --profil <ad> → claude -p argv + env eki
+PROFIL = sys.argv.pop(sys.argv.index("--profil") + 1) if "--profil" in sys.argv else "tam"
+if "--profil" in sys.argv:
+    sys.argv.remove("--profil")
+    p_arg, p_env = cc_profil.kur(PROFIL, env=ENV)
+    argv += p_arg
-            rc = subprocess.run(argv, cwd=cwd, env=ENV, ...
+            rc = subprocess.run(argv, cwd=cwd, env={**ENV, **p_env}, ...
```
  Kuru kontrol: `--profil blender` → strict-mcp-config · mcp-config · disable-slash-commands · append-system-prompt-file · settings (enabledPlugins 5 false + promptCacheTtl) · env CC_PROFIL.
- Mühür (TOKEN-1 başı muhur-once.json ile): settings · mcpServers · skill/plugin/MCP sayıları eşit; hooks yalnız jev-skill.ps1 farklı. `git diff --diff-filter=D 095b201..HEAD` boş. gitleaks: TOKEN-1 commit'leri temiz.
- Açık (DUR): K3 4 prob yazıldı ama koşulmadı. İlk denemede boş RAM 0.7 GB'tı (oyun açıktı), RAM boşaldığında tur tavanı aşılmıştı. K4 B-fincan kapısı koşulmadı → blender çağrı yeri "tam"da. Ölçülen tasarruf yok; beklenen: L10 1.0 M ağırlıklı (token-0 kaldıraç tablosu).
- Sonraki: `python <scratchpad>/prob_t1.py` (4 prob, ≤$1/prob) → `python kos.py fincan B rehber-T1 --profil blender` → kor.py → karar (omer-kurallar "kalite takası") → arşiv.
