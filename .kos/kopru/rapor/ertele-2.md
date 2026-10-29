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

# TUR 2 (kanıt tmp/ertele5/: context-F.txt, pte.txt, xgt.txt, uret_f.py)
- D/E boş çıktı: stdout+stderr boş; neden Desktop'un 12:48'de süreci öldürmesi (YÖN notu), ayar hatası yok.
- Kod kanıtı (claude.exe PTe/Xgt/PTo): skillOverrides anahtarı dizin adı (User) / tam ad (claude.ai sync); plugin skill'i (`source==="plugin"`) yalnız synced-skill eşlemesinden (followsSyncedSkillState) override alır — düz plugin adıyla override YOK SAYILIR.
- Aday F (3200 anahtar düzeltildi, 49 çekirdek name-only, 285 ajan reddi): /context 103,8k (A 121,7k, C 108,2k); Skills 30,5k — kalan 2892 satırın tamamı plugin (User 28, sync 21 = çekirdek); Custom agents 33,9k (red yine düşürmedi); MCP 14,7k; bellek 9,1k.
- KAPI TUTMADI (≤60k için plugin skill ~30k + ajan ~34k kalıyor; ikisinin de kaldırmasız resmi yolu bulunamadı: plugin skill'i override almıyor, ajan listesi deny ile düşmüyor). ~/.claude'a hiçbir şey uygulanmadı. 6 görev kalite/bulma/slash canlı testi koşulmadı (bağlam bitti).
- Sonraki: plugin agent/skill için resmi belge (claude-code-guide) — plugin manifest düzeyi gizleme ya da skillListingBudgetFraction ile plugin açıklama kırpma ölçümü; F'yi kalite+slash testine sok. Tek oturum, sırayla.
