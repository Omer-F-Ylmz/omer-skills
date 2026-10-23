---
name: code-mode
description: Çok adımlı MCP/araç zincirini TEK çağrıda koş (UTCP Code Mode) — ara sonuçlar bağlama girmez, yalnız özet döner. 2+ ardışık araç çağrısı, büyük çıktı (git diff/status, sayfa snapshot, uzun liste) veya veri süzme gerektiğinde kullan.
---

# Code Mode (UTCP) — token tasarrufu

Neden: normal MCP'de her araç çağrısı modele gidip-gelir ve ham çıktı bağlama girer (ölçüm 23 Eki: omer-skills `git diff` 2.95M karakter, `git status` 138k). Code Mode'da kısa bir JS yazılır, araçlar sandbox'ta (isolated-vm) zincirlenir, yalnız `return` edilen özet döner (~100 karakter).

## CC / köprü ajanı (Bash)
```
python C:/Projeler/omer-skills/tools/cm.py list                 # araçlar (manual.tool)
python C:/Projeler/omer-skills/tools/cm.py search "<görev>"     # ilgili araçlar + arayüz
python C:/Projeler/omer-skills/tools/cm.py info git.git_git_log
python C:/Projeler/omer-skills/tools/cm.py run zincir.js        # dosyadan
python C:/Projeler/omer-skills/tools/cm.py run -c "return gw.time_get_current_time({timezone:'Europe/Istanbul'})"
```

## Desktop
`code-mode` MCP sunucusu (claude_desktop_config.json; @utcp/code-mode-mcp, aynı config) → `call_tool_chain` aracı. Desktop yeniden başlayınca görünür.

## Kod kuralları
- Düz JavaScript (TS tip açıklaması YAZMA). Gövde async fonksiyon; sonuç `return` ile.
- Araç çağrısı senkron: `git.git_git_log({ repo_path: "C:\\Projeler\\omer-skills", max_count: 25 })`.
- Ham çıktıyı DÖNDÜRME; say/süz/özetle, yalnız gereken alanları döndür.
- Tarayıcı (pw.*) oturumu tek `run` içinde yaşar: navigate → snapshot → close aynı dosyada.
- Varsayılan zaman aşımı 60 sn (`--timeout 120000`).

## Bağlı manual'lar (tools/code-mode/.utcp_config.json, 139 araç)
- `gw.*` — time, fetch, memory (graph), brave (web/haber/görsel arama), markitdown, arxiv, context7 (yerel ağ geçidi :47800)
- `git.*` — mcp-server-git (status/log/diff/show/branch/commit...)
- `fs.*` — dosya sistemi (C:/Projeler, Desktop)
- `pw.*` — Playwright (headless)
Yeni MCP: config'e manual ekle → `python tools/cm.py validate`.

## Ne zaman KULLANMA
Tek, küçük araç çağrısı (zaten ucuz) ya da her adımın sonucunu görüp karar vermen gereken etkileşimli iş.
