# TOKEN-6b — ara ölçüm · etkileşimli TTL simülasyonu · HR uyarısı (KAPANDI, tur 21/25)

## KARAR
- K1 `olc --karsilastir`: grup başına dönem başı (claude-p 170eb0a · observer yama 16:36:04Z · omer-skills 265315f · etk·ana diğer effort high ≤23:53:49Z · varsayılan f3bce7f); ölçüm koşuları OLCUM ilk istem kalıbıyla ayrı/hariç; yetersiz örnek Σ'da 0.
- K2 `olc --ttl-sim`: yazma a/b, sebep sırası compact → ara>TTL → model/effort → deferred_tools_delta → diğer; kollar 1h/5m/hibrit (oturum kehaneti).
- K3 statusline.ps1 HR segmenti başta; yedek .bakT6b.

## Sonuç
- Commit'ler: 5b5eed3 K2 kırmızı · 5ae1306 K2 yeşil (mutasyon ara>=300 kırmızı) · 35247db K3 kırmızı · e20b27d K3 yeşil · c680107 K1 kırmızı · 3cbf64b K1 yeşil (mutasyon eşit pay kırmızı) · 49f2dc7 ölçüm çıktıları · K4 docs.
- Testler: pytest tests 290 yeşil (yeni 7+10+3).
- K1 Σ ağırlıklı −%79.2 (artış), temsilî değil; observer −%55/gün. K2 5m −%4.9 · hibrit −%7.7; baştan yazmanın %93'ü "diğer".
- Mühür EŞİT (settings 02372fb94f3e5e29 · mcpServers 23452893b846a828 · hooks a0801fdfd21676e2 · plugin 47/53 · mcp 19 · skill 1054)
- HR: ANTHROPIC_BASE_URL var · ENABLE_TOOL_SEARCH var · SessionStart e0d759be42561ee5 (başla eşit)
- diff-filter=D 0 · gitleaks 73902cc..HEAD temiz · graphify update koştu.

## Sapmalar
- TTL zinciri repoda yoktu; CC 2.1.288 ikilisinden alındı.
- OLCUM kalıbı tetik-seti ve 3a okuyucu istemlerini kapsamıyor; okuyucu: dönemdeki 72 sdk-cli oturumunun tamamı ölçüm → claude-p karşılaştırılamaz (Σ claude-p hariç de verildi).
- K3 test dikişi HR_PORT env.
