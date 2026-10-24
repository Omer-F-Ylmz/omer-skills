---
type: rapor
status: kismi
tags: [arac-ajan-ozellik-1, envanter]
relatedTo: [docs/envanter/arac-ajan-ozellik.tsv, tools/arac_ajan_envanter.py]
---
# ARAC-AJAN-OZELLIK-1, KISMİ (kalite kapısı ≥%98 tutmadı)

- Envanter: `docs/envanter/arac-ajan-ozellik.tsv` 560 satır (15 elle yazılmış çekirdek + 545 otomatik; kaynak `envanter.tsv`). Üretici: `tools/arac_ajan_envanter.py` (yeniden koşulabilir).
- Durum sütunu: 527 kurulu · 5 KUR (UYARLA/DENE kararlı) · 10 zaten var · 4 RED/ATLANDI · 14 ÖĞREN (konu kartı, araç değil).
- Doğruluk örneklemi (okuyucu ajan, 12 satır): bizde_karşılığı eşlemesi 7/12 uyumlu (~%58). 202 satır `ajan_sira (genel)` yer tutucu; `ne_yapar` otomatik satırlarda `ozellik` kopyası. Kapı (%98) GEÇMEDİ.
- Yapılmadı: (2) her özelliğin headless deneme koşusu (`_deneme/arac-ajan/`), (3) zincirli kombin, (4) ajan-özellik etiketi/katalog + görev şablonu satırı, (5) 3 gerçek görevde transkript kanıtı. Neden: bütçe ($1.1 harcandı; hedef $0.50) ve otomatik eşlemenin önce düzeltilmesi gerekiyor.
- Gerçek kullanım kanıtı: ruflo `hooks_intelligence_pattern-search` (başta), Agent `okuyucu` (örnekleme). Diğer zorunlu araçlar (dispatching-parallel-agents, executing-plans, pair-agent, oh-my-issues, idea-refine, brainstorming, interview-me, doubt-driven-development, gstack-plan-ceo-review, gstack-office-hours, design-ops:design-critique) çağrılmadı, tek kanıtlı iş envanter üretimi; `arac_eksik`.
- Devam: `.kos/kopru/gorev-arac-ajan-ozellik-1-devam.md`.
- ÖMER: claude.ai tarafı için dist zip yeniden üretimi/yüklemesi (envanter + üretici betik zip içine), henüz yapılmadı.
- Push yok. Test: üretici betik koştu (exit 0); birim testi yok.
