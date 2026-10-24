---
type: doc
status: active
tags: [hermes, nous-research, mcp, hermes-kur-1]
relatedTo: [hermes-kur-1, ajan-sira]
---

# Hermes Agent, öğrenme notu (HERMES-KUR-1, 24 Eki 2026)

Kaynak: github.com/NousResearch/hermes-agent (MIT, `4dcef215`, sürüm 2026.9.24), README + pyproject + plugin-catalog. "Hermes 2" adlı ayrı bir ürün bulunamadı; kurulan Hermes Agent.

- **Kurulum:** Windows yerel destekli (WSL2 gerekmez). Resmi betik `install.ps1` LOCALAPPDATA'ya Python 3.14/Node/FFmpeg indirir → kullanılmadı. Burada: `UV_PROJECT_ENVIRONMENT=araclar/hermes uv sync --project <repo> --frozen --extra mcp --python 3.14`. `pip install -e` çözümsüz (browser-harness↔pillow pin çakışması), Python 3.12'de çekirdek bağımlılıklar koşullu (`python_version >= '3.14'`) → boş kurulur. `bdist_wheel` bilerek engelli; yalnız editable.
- **Veri dizini:** `HERMES_HOME` (burada `araclar/hermes-home`); varsayılan `%LOCALAPPDATA%\hermes`.
- **Sağlayıcılar (yerleşik):** nous, openrouter, nvidia, gemini, anthropic, openai-codex, xai, deepseek, ollama-cloud, huggingface … Groq/Mistral/SambaNova yerleşik değil (custom endpoint gerekir). OpenRouter `:free` slug'ları sık değişir (404 "unavailable for free"); güncel liste `openrouter.ai/api/v1/models` fiyat 0.
- **Tek atış:** `hermes chat -Q -q "<istem>" --provider openrouter -m <model> --max-turns N` (stdout = yalnız son yanıt).
- **MCP:** istemci olarak `hermes mcp add/list/test`. Sunucu olarak çekirdekte yok; resmî plugin `mcp-serve` (`hermes plugins install mcp-serve --enable --yes-deps`, sonra `hermes mcp-serve`, stdio): 10 araç (conversations_list, messages_read, events_poll, messages_send, channels_list, permissions_* …), mesajlaşma ağ geçidi oturumlarını açar; `--tools` ile web/vision/skills; terminal/dosya/kanban asla. Hermes'in model ile iş yapması (delegasyon) bu MCP'den değil `hermes chat -q`'dan (bkz. `tools/hermes_motor.py`).
- **Skill sistemi:** agentskills.io uyumlu; ajan karmaşık işten sonra kendi skill'ini üretir, kullanırken geliştirir; `skills/.bundled_manifest` hazır olanları listeler → bundled olmayanlar aday (bkz. `tools/hermes_ogrenme.py`).
- **Bellek/arama:** ajan-küratörlü bellek + FTS5 oturum araması + Honcho kullanıcı modeli. **Delegasyon:** izole alt ajanlar, RPC ile Python betiği. **Cron:** yerleşik zamanlayıcı. **Gateway:** Telegram/Discord/Slack/WhatsApp/Signal tek süreç. **Plugin:** `hermes plugins`, katalog `plugin-catalog/*.yaml`.
- **Güvenlik (bu kurulum):** gitleaks 928 bulgu = OAuth client-id sabitleri + test fixture (gerçek sır yok); semgrep p/secrets=0, p/python 19 ERROR = `subprocess shell=True`/tainted env (ajanın kabuk aracı, tasarım gereği); 10 dosya semgrep Timeout = TARANMADI. Claude aboneliği/anahtarı Hermes'e verilmez (`ANTHROPIC_*` alt süreçten çıkarılır); OpenRouter anahtarı yalnız mevcut ortam değişkeninden.
