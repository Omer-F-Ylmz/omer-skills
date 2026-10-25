---
type: sonuc
status: karar
tags: [mcp-ac-2, onay-toplu-1]
relatedTo: [docs/token/mcp-ac-2.tsv]
---
# MCP-AÇ-2 A/B sonucu (24 koşu, 22 Eki; yeni claude -p koşulmadı)
kol | koşu | ilk_giris ort | top_giris ort | usd toplam | kalite
bos | 6 | 15008 | 27125 | 0.0137 | 4/4
eski | 6 | 15662 | 102212 | 0.2844 | 2/4
yeni (ertele=1) | 6 | 15663 | 34290 | 0.0190 | 3/4
filtre | 6 | 15662 | 29795 | 0.0126 | 4/4
KARAR: CC_MCP_ERTELE=filtre (en düşük toplam girdi/usd, kalite bos tabanıyla eşit). Not: ilk_giris kollar arası eşit (~15,6k); fark toplam girdide (eski tüm MCP araçlarını yükler).
