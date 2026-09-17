# Prompt cache notları · 2026-09-17
Kaynak: code.claude.com/docs/en/prompt-caching · statusline "Prompt cache fields" · errors "Unable to resize image". Ölçümler: CACHE-1 (Claude Code 2.1.273–274, transcript'ler 09-10 → 09-17).
## Bozan
- Model değişimi: `/model` ya da frontmatter'ında oturumdan farklı `model:` olan skill/komut/agent → sonraki istek tüm geçmişi cache'siz okur.
- Effort değişimi (Opus 5 dahil; istisna Fable 5.1 abonelik/API anahtarı) · fast mode'u açmak (sonraki turun ilk isteği).
- Prefix'teki araç tanımı değişimi: MCP bağla/kes, MCP sunuculu plugin aç/kapa, `alwaysLoad` sunucu. Tool search'le ertelenen araçlar bozmaz.
- Bare tool deny (`Bash`, `Bash(*)`, `"*"`) yalnız tool search kapalıyken bozar; kapsamlı kurallar (`Read(./bin/**)`) ve allow/ask kuralları bozmaz.
- Compaction (konuşma katmanı yeniden yazılır, sistem katmanı kalır) · çok görüntü birikince en eski grup atılır, o mesajdan sonrası yeniden işlenir.
- TTL aşımı: ana oturum abonelikte 1 saat, subagent/workflow/fork 5 dk · Claude Code güncellemesi (yeniden başlatma sonrası ilk tur).
## Koruyan
- Repo dosyası düzenleme · oturum içinde CLAUDE.md düzenleme (bozmaz; yeni içerik /clear, /compact ya da yeniden başlatmada yüklenir) · izin modu · output style.
- Skill/komut çağırmak (mesaj olarak eklenir) · plugin'in skill/komut/agent/hook'ları · `/recap` · `/rewind` (önceden cache'lenmiş prefix'e döner, bedava).
## Bizim düzen
- Dalga başı /clear = yeni oturum: son 7 günde 60 Opus 5 oturumunun ilk isteği medyan 19.4k token yazıyor (proje katmanı + oturuma özgü), 32.2k okuyor (sistem prompt + araçlar, önceki oturumlardan). Dalga içinde yanlış yola girildiyse /clear değil /rewind.
- /model ve /effort dalga başında, ilk istekten önce: en düşük hit'li 5 oturumda hep ilk istekten önce yazılmış, bozmamış. Oturum ortasında değiştirmek tüm geçmişi yeniden yazar.
- Ana oturumda 1 saatten uzun ara cache'i soğutur: dacfce6b'de 69.5 dk → 105k token yeniden yazım. "Uzun aradan sonra yeni oturum" kuralı bununla uyumlu.
- 7 günlük ana oturum hit oranı %99.05 (medyan %98.45); en düşükler %93.8–96.8, sebep kısa oturumda sabit başlangıç yazımı + büyük araç çıktıları ve TTL aşımı, bozan ayar değil.
- Subagent'ler 5 dk TTL'de: 2.723 istekte okuma/yazma 16.8:1, tamamen soğuk istek %3.1, >5 dk boşluk 6 kez. Uzun video taramaları cache'i soğutmadı; istekler sık.
- Denetim: deny kuralları kapsamlı (bare yok) · MCP'lerde `alwaysLoad` yok · açık plugin'lerde farklı `model:` yok (impeccable 4 agent `inherit`; `model: sonnet` yalnız kapalı plugin-dev agent-creator).
- Screenshot: Claude Code görüntüyü uzun kenar ≤2000 px'e küçültür, maliyet ⌈w/28⌉×⌈h/28⌉ (ölçümle +125–245 token araç metni). 1440 tam sayfa 1.7k–3.7k (tepe ~2000 px yükseklikte, daha uzun sayfa küçülür), 768 ≤2k, 390 ≤1k. Tur ≈5.4k (medyan)–6.8k (en kötü), 4 tur 21–27k, yön keşfi 8.5–11k; bir çalışma 15 görüntü. Tek oturumda en çok 68 görüntü okunmuş (8 oturumda >20).
- İzleme: statusline `~/.claude/statusline.ps1` (model | ctx % | cache % | miss sebebi; komut `-ExecutionPolicy Bypass` ister) · `/usage` "Prompt cache (main)" aynı istatistik, `claude -p`'de satır çıkmaz.
