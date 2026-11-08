---
type: report
status: done
tags: [ret-kur-1b, kurulum]
relatedTo: [ret-denetim]
---

# RET-KUR-1b raporu (28 Eki 2026)

Koşul: `.kos/kopru/ret-kur-1-hesap.txt` HAZIR satırları var (9 anahtar, yalnız varlık kontrolü).

## Sonuç

- KURULDU (resmi paket, global kurulu): Apify (`@apify/actors-mcp-server` 0.19.5), Modal (`modal` 1.6.3 CLI).
- Apify MCP zaten mcptoon gateway üzerinden kayıtlı; yeni kullanıcı kapsamlı kayıt eklenmedi (`claude mcp add` "already exists" dedi, bir şey yazılmadı).
- KURULAMAZ(kaynak): Composio (`@composio/mcp` deprecated), fal.ai, Higgsfield/Kling, Telegram, Meta Ads. Resmi paket bulunamadı; bulunanlar tek bakımcılı topluluk paketleri, kurulmadı.
- KURULAMAZ(hesap): Oxylabs. `OXYLABS_USERNAME` yok, yalnız `OXYLABS_API_KEY` var. Username eklenince yeniden denenir.

## Düzeltme

`ret-denetim.tsv` içinde 13 satır önceden `KURULDU` ve "bkz rapor/ret-kur-1b.md" olarak işaretlenmişti. Bu rapor yoktu ve işaretlerin çoğu doğrulanamadı. Satırlar yukarıdaki sonuçla yeniden yazıldı. Rapor dosyası artık var.

## Güvenlik

- gitleaks: değiştirilen tsv + betik üzerinde 0 bulgu.
- semgrep (p/secrets): 0 bulgu. Ağ kısıtı varsa bu koşu sessiz geçmiş olabilir.
- Env değerleri hiçbir komutta basılmadı; yalnız varlık boolean kontrol edildi.
- Modal canlı token doğrulaması yapılmadı (dış çağrı yok).

## Sapmalar

- Görev "Oxylabs (OXYLABS_USERNAME)" diyordu; hesap dosyası `OXYLABS_API_KEY` veriyor. Kurulum için username gerekiyor.
- "Resmi MCP/CLI" koşulu Meta, fal, Higgsfield, Telegram için sağlanamadı; kanıt tsv kanıt sütununda.
