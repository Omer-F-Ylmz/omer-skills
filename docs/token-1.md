# TOKEN-1 — arka plan profili (L1 + L10) · 2 Eki 2026 · DURUM: K3–K5 bekliyor (tur tavanı 40 doldu)

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
