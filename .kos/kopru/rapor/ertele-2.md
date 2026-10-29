---
type: rapor
status: tur-bitti
tags: [ertele-2, token, skill, ajan]
relatedTo: [ertele-1]
---
# ERTELE-2 — TUR 1 (kanıt tmp/ertele5/)
- /context A (mevcut global): 121,7k başlangıç; Skills 52,3k · özel ajan 32,1k · MCP talimat 13,2k · bellek 9,1k.
- Aday C (`ayar-C.json`: 5136 skill `skillOverrides: user-invocable-only`, 28 çekirdek `name-only`, 285 ajan reddi): /context 108,2k; Skills 36,2k (3500 satır kaldı: 471 claude.ai sync, 376 ecc plugin — skillOverrides bunları kapsamıyor); ajan reddi Custom agents 32,1k'yı DÜŞÜRMEDİ (286 satır aynı).
- Kancalı tek tur (`bas.py`, haiku, toplam girdi): A 182,3k $0,177 · C 143,3k $0,138 (−39k); paralel koşuda süre 630/747 sn.
- D/E (`env.SLASH_COMMAND_TOOL_CHAR_BUDGET=6000` --settings içinde): boş stdout, neden ÖLÇÜLEMEDİ (bağlam tükendi).
- KAPI TUTMADI (≤60k uzak; 6 görev kalite/bulma/slash canlı testi yapılmadı). ~/.claude'a HİÇBİR şey uygulanmadı.
- Sonraki: claude.ai senkron skill'leri kapatma (disableClaudeAiConnectors/sync ayarı), ecc plugin skill'lerini plugin adıyla override, ajan listesini deny yerine agent frontmatter/plugin disable ile düşürme, D hatasını stderr ile ayıkla.
- Harcama ≈ $0,32 ölçüm + ana oturum.
