# jcode hook tarifi (bekleyen, yapım yok)

Kaynak: parti gelistirme-2026-09-29 paneli, jcode satırı (UYARLA · eşdeğer: codex p 0.75 · MIT). Bu dosya yalnız tarif; kurulum ve kod bu dalgada yok (MOTOR-M3a K0d).

## Ne
JCode'un tamamı kurulmaz. Bağlam tasarrufu fikri Claude Code hook'u olarak uyarlanır.

## Tarif
1. **PostToolUse hook (Read/Grep)**: oturumda görülen dosya+satır aralıklarının karmasını tutar (oturum başına geçici dosya, `.claude/` altı, gitignore). Aynı içerik tekrar gelirse çıktı "daha önce görüldü: <yol>:<aralık>" özetiyle kısaltılır.
2. **Grep yapı özeti CLI** (isteğe bağlı): grep sonucuna dosya başına sembol/yapı özeti ekler (ctags ya da tree-sitter). Önce graphify query ile çakışması ölçülür; graphify yeterliyse yapılmaz.
3. **Kapsam dışı**: swarm modu; gömme dizinli oturum hafızası MCP'si (claude-mem zaten var).

## Kabul (yapım dalgası için)
- Önce/sonra: aynı oturum görevinde Read/Grep tool_result baytı (rtk-kapsami.md yöntemi, ~bayt/4 token).
- Bilgi kaybı yok: kısaltılan çıktı yalnız birebir tekrar içerikte; değişmiş dosyada tam çıktı.
- headroom ve rtk ile çakışma testi: aynı çıktı iki kez sıkıştırılmaz.
- Hook hatasında araç çıktısı olduğu gibi geçer (fail-open).
