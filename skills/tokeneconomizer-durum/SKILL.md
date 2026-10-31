---
name: tokeneconomizer-durum
description: Use when the user asks what TokenEconomizer (Microsoft Research token saver plugin) is doing, whether it pruned tools, how to restore a hidden MCP/tool, how to turn micro-skills / tool pruning / loop guard on or off, or how much sessions cost. Explains its three mechanisms and gives the exact commands for Claude Code, Codex and a terminal.
---

# TokenEconomizer — durum ve kullanım

TokenEconomizer (github.com/microsoft/TokenEconomizer, Apache-2.0) üç mekanizmayla jeton kısar:

1. **Micro-skills** — repoda öğrenilen kısa gerçekler (ör. "pytest burada çalışmaz, `.venv/Scripts/python -m pytest` çalışır") oturum başında enjekte edilir. Varsayılan KAPALI; Ömer'in makinesinde `--global` açık (`envfacts+distiller`, her 3 oturumda bir model önerisi).
2. **Tool pruning** — hiç kullanılmayan araçlar `.claude/settings.local.json` içine deny kuralı olarak yazılır (git dışı). Varsayılan `auto`: en az 2 oturum ve 60 dk sessizlikten sonra, sonraki oturumdan itibaren. Senin yazdığın deny kurallarına dokunmaz.
3. **Loop guard** — 20+ turluk döngüye giren turda yargıç model takıldı mı diye bakar, takıldıysa bir kez yönlendirir.

## Komutlar

Claude Code içinde (her biri 1 model turu): `/tokeneconomizer:status`, `/tokeneconomizer:toolprune`, `/tokeneconomizer:config`.
Terminalde, repo içinde (bedava): `~/.tokeneconomizer/bin/te --host claude <komut>`. Codex: `$tokeneconomizer:<komut>`.

| İstek | Komut |
|---|---|
| Ne öğrendi, ne budadı, oturum maliyeti | `status` |
| Gizlenen araçlar ve kanıtı | `toolprune` |
| Gizlenen MCP/aracı geri ver (bir daha budanmaz) | `toolprune restore [ARAÇ …]` |
| Budamayı onaylı yap | `config set toolprune=propose`, sonra `toolprune apply` |
| Bir aracı hiç budatma | `config` çıktısındaki `toolprune_protect` listesine ekle (sözdizimini önce `config` ile gör) |
| Mekanizmayı kapat | `config set microskills=off` / `toolprune=off` / `loopguard=off` |
| Araç listesini kaydet (CC güncellenince) | `toolprune refresh-catalog` |
| Sağlık denetimi | `doctor` (yalnız terminal) |

## Bilinen tuzak (Ömer'in makinesi)

`refresh-catalog` `claude -p` açılışını 60 sn bekler; bu makinede açılış ~5,5 dk (1288 araç, çok eklenti). Hata: "could not read the tool list from a `claude -p` init event". Çözüm: `python .kos/kopru/ogren/video-izle-kur-1/te/katalog.py 600` (aynı fonksiyon, uzun süre).

## claude.ai / Desktop

Eklenti yalnız CLI ajanlarında (Claude Code, Codex, Copilot CLI, Pi, opencode) çalışır; claude.ai sohbetinde araç budaması yoktur. Bu skill orada yalnız açıklama ve komut rehberidir: kullanıcıya hangi komutu terminalde koşacağını söyle.
