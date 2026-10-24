---
name: hermes-desktop
description: "Hermes Agent (Nous Research) ücretsiz-model motoru: CC/Desktop'tan nasıl çağrılır (mcp-serve MCP, hermes chat -q, ajan-sira motor=hermes). claude.ai sandbox'ında koşmaz; komut şablonları."
---

# Hermes Agent, kullanım rehberi (Desktop / CC)

Hermes yerelde (Windows) `C:\Projeler\omer-skills\araclar\hermes` venv'inde kurulu; veri `araclar\hermes-home`. Hermes ikilisi Windows'a özgü: claude.ai sandbox'ında koşmaz, bu skill yalnız komutları ve yorumlamayı verir.

## Üç kullanım
1. **MCP (CC + Desktop):** sunucu adı `hermes` (komut `...\araclar\hermes\Scripts\hermes.exe`, arg `mcp-serve`, env `HERMES_HOME`, `PYTHONUTF8=1`). Araçlar: `conversations_list`, `messages_read`, `events_poll`, `channels_list`, `permissions_*`. Bu bir mesajlaşma köprüsüdür (gateway oturumlarını okur/mesaj yollar); terminal/dosya aracı sunmaz. Desktop'ta yeni MCP girdisi için Desktop yeniden başlatılır.
2. **Tek atış ücretsiz model:** `hermes chat -Q -q "<istem>" --provider openrouter -m nvidia/nemotron-3.5-lightning:free --max-turns 20` ($0; OpenRouter anahtarı mevcut `OPENROUTER_API_KEY` ortam değişkeninden). `:free` slug'ı değişirse `openrouter.ai/api/v1/models` listesinden fiyatı 0 olan, `tools` destekleyen birini seç (`HERMES_MODEL` ile ezilir).
3. **Alt ajan motoru:** `.kos/kopru/ajan-sira.tsv` satırına `motor=hermes` → iş `claude -p` yerine `tools/hermes_motor.py` ile Hermes'te koşar ($0). Başarısızsa merdivende bir üst basamağa (haiku medium) düşer. Kolay işlerde merdivenin ücretsiz basamağı Hermes'tir (hazırsa).

## Kurallar
- Claude aboneliği/anahtarı Hermes'e verilmez (`ANTHROPIC_*` alt süreçten çıkarılır). Anahtar dosyaya yazılmaz.
- Boş çıktı başarı değildir: yanıtta görev adı ve `KABUL:`/`DUR:` satırı aranır.
- Hermes'in ürettiği skill'ler `python tools/hermes_ogrenme.py` ile gitleaks kapısından geçip `.kos/kopru/aday-skill/hermes/`'e düşer; omer-skills'e inceleme sonrası girer.
- Varsayılan tarayıcı açılmaz (K2q); Hermes'in tarayıcı araçları headless/Chrome ile sınırlı tutulur.
