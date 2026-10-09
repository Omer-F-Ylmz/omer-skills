# Tetikleyici: hangi projede kurulur (kurulum turu 3c)

Bunlar şimdi kurulmadı; ilgili iş çıkınca kurulur.

| Araç | Hangi projede kurulur | Not |
|---|---|---|
| lenis | Smooth-scroll isteyen web projesi | `npm i lenis` proje bağımlılığı |
| remotion | Video üreten proje | `npm i remotion`; skill'leri tur-2'de kurulu |
| pint | PHP/Laravel projesi | `composer require laravel/pint --dev` |
| BlenderKit + blendkit | Blender açıp varlık çekeceğin iş | Blender → Add-ons; login olayı yollar |
| DaVinci Resolve MCP | Resolve açıkken montaj | GUI eklentisi |
| zoetrope | Cargo kurulunca | `cargo install zoetrope@0.2.0 --locked`; bu makinede cargo yok |
| size-limit | Paket boyutu bütçeli JS projesi | proje bağımlılığı, tur-1'de paket adı "None" |
| stripe / @fal-ai/client SDK | Ödeme / fal kullanan proje | `npm i stripe@23.0.0`, `npm i @fal-ai/client@1.10.1` |
| scrapegraph-ai | Kazıma projesi | Python proje bağımlılığı, SGAI_API_KEY |
| googleworkspace/cli (95 skill) | Google Workspace işi | bağlam şişirir; OAuth gerekir |
| Vibe-Trading (91 skill) | Finans araştırması | bağlam şişirir; DEEPSEEK_API_KEY, ALPHAVANTAGE_API_KEY |
| davila7/claude-code-templates | Şablon kataloğu gerekince | telemetri içerir, tam marketplace yüzlerce bileşen |
| git-mcp | Yerel çalıştırma yolu belli olunca | resmi kullanım uzak (gitmcp.io); yerel stdio karşılığı doğrulanamadı |
| excalidraw-mcp | Lisans netleşince | repo lisanssız; npm `excalidraw-mcp@1.0.0` kaynağı doğrulanamadı |
| function-hook mod'ları (claude-toons, davekiss/env, cache-tax) | Açmaya karar verince | klonlar `C:\Projeler\uygulamalar\fn-hook-mods\` altında KAPALI. Açmak için `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1` ve `CLAUDE_CODE_PLUGIN_DIRS`; claude-toons ek Anthropic API maliyeti getirir |
