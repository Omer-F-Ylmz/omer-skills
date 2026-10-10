# Kurulum turu 6 (2026-10-10 akşam)

Kaynak: `kacan-adaylar.md` "Tur 6 adayları" (91 aday). Ayrıntı: `tur6-sonuc.tsv`. Betik: `tools/kurulum-turu-6.sh` (log `.kos/kurulum-6/`, geri-al `.kos/kurulum-6/geri-al.sh`, SHA `kurtarma.json`).

## Sayılar
KUR 4 (eşlemeyle) · ZATEN 2 · HESAP 25 · AYRI-UYGULAMA 21 (i web 12 · ii 9) · RED 43 (gürültü 20 · kapsam 11 · bulunamadı 8 · lisans 4) · ÖNERİLMEZ 0 · KUR-duzeltmeli 0. 91 aday; 4 kurulum satırı OCR eşlemesinden eklendi (kaynak adaylar avanderlee.com ve hackingwithswift.com).

## Kurulan (skill, MIT, SKILL.md var, ad çakışması 0, hesap istemez)
- AvdLee/Swift-Concurrency-Agent-Skill · d5770817d262 · swift-concurrency
- AvdLee/SwiftUI-Agent-Skill · 204dba7c6725 · swiftui-expert-skill
- twostraws/SwiftUI-Agent-Skill · f9800713b245 · swiftui-pro
- twostraws/Swift-Concurrency-Agent-Skill · bee3f69ba171 · swift-concurrency-pro
`~/.claude/skills/<ad>`; iç içe kopyalar ADI çakışması diye atlandı (aynı ad).

## Kurulmayan, önemliler
- mrdainami/kie-mcp (MIT): KIE_API_KEY ister → HESAP; hesaplar.md satırı eklendi.
- hetpatel-11/Adobe_Premiere_Pro_MCP (MIT): AYRI-UYGULAMA ii; `npx …@latest` (pin yok) ve Adobe Premiere Pro gerekir.
- mrdainami/nami (Apache-2.0): masaüstü çok-ajan uygulaması → AYRI-UYGULAMA ii.
- bilawalsidhu/gods-eye-view: web 3B küre uygulaması, lisans NOASSERTION → AYRI i; üç çatalı RED lisans.
- cocktailpeanut/minijam: lisanssız → RED lisans (lisans kapısı).
- composio-mcp (ComposioHQ/composio, MIT): hesap ister → HESAP.
- OCR eşlemeleri: iktof/iktok/tiktof/tikt∂k → tiktok.com; aps.aple.com → apps.apple.com; hyperframe.ai → HyperFrames (ZATEN); platform.claude.com/docs → ZATEN.
- Saldırı/red-team repo yok; klon silinecek bir şey yok.

## Doğrulama
4/4 yeni skill'de SKILL.md var, `~/.claude/skills` yinelenen ad 0. `claude plugin list` 195 giriş, hata 0 (plugin eklenmedi). `claude mcp list`: MCP eklenmedi; 25 mevcut sunucu bağlı değil (önceden var: open-design, azure-cost, adobe, expo, fal, intercom, 21st, github vb.).
