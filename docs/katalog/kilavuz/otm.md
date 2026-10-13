# otm — 23 benzersiz kayıt

**Amaç:** Otomasyon ajanları: n8n akışları, API/webhook entegrasyonu, tarayıcı otomasyonu (Playwright, Puppeteer), dosya/CSV/JSON dönüşümü, e-posta ve bildirim, zamanlanmış görev, PowerShell 5.1.

**İç yapı:** Tümü [ajan], otm-<konu>; n8n üçlüsü (akis-tasarimi, hata-yonetimi, ifade-kod), entegrasyon (api, webhook, veri-esleme), tarayıcı, veri dönüşümü (csv, jq, power-query, sema), iletim (mail, bildirim).

## En güçlü parçalar
- `otm-powershell-51` — Stok Windows PowerShell 5.1 için PS7 sözdizimi olmadan, encoding ve JSON derinlik tuzaklarıyla.
- `otm-webhook-tasarimci` — İmza kontrolü, idempotency ve hızlı onaylı webhook alıcıları.
- `otm-n8n-hata-yonetimi` — Sessizce başarısız olan n8n akışlarına hata akışı, retry, alarm.
- `otm-ajan-is-akisi-kur` — İstem, araç ve insan onay kapılı LLM otomasyonları.
- `otm-csv-temizleyici` — Excel'de bozuk görünen CSV'lerde encoding, ayırıcı, bölgesel sayı formatı.
- `otm-tarayici-yardimci-dosya` — Tekrarlanan tarayıcı akışını rol/metin locator'lı, sırsız yardımcı dosyaya çevirir.
- `otm-cli-sarmalayici` — GUI masaüstü uygulamasını makine okunur çıktılı ajan dostu CLI'ya sarar.
- `otm-dosya-isleme-botu` — Çok dosyayı dry run ile yeniden adlandırma, dönüştürme, sıralama.

## Birlikte kullanım
- otm-n8n-akis-tasarimi + otm-n8n-ifade-kod + otm-n8n-hata-yonetimi; n8n ailesi ile.
- otm-api-entegrasyon + otm-veri-esleme + otm-sema-dogrulayici.
- otm-tarayici-otomasyon → otm-tarayici-yardimci-dosya.
- otm-zamanlanmis-gorev + otm-otomasyon-izleme + otm-bildirim-yonlendirme.

## Tuzaklar
- otm-tarayici-otomasyon (Playwright) ile otm-puppeteer alternatif; aynı işte ikisi gereksiz.
- otm-google-sheets-akis Apps Script kota ve izin limitlerine takılır.
- otm-mail-otomasyon toplu gönderimde throttling ve abonelikten çıkma zorunlu.

## Üyeler
- ajan (23): otm-ajan-is-akisi-kur, otm-api-entegrasyon, otm-bildirim-yonlendirme, otm-cli-sarmalayici, otm-csv-temizleyici, otm-dosya-isleme-botu, otm-google-sheets-akis, otm-jq-donusum, otm-mail-otomasyon, otm-n8n-akis-tasarimi, otm-n8n-hata-yonetimi, otm-n8n-ifade-kod, otm-otomasyon-izleme, otm-pazarlama-otomasyonu, otm-power-query, otm-powershell-51, otm-puppeteer, otm-sema-dogrulayici, otm-tarayici-otomasyon, otm-tarayici-yardimci-dosya, otm-veri-esleme, otm-webhook-tasarimci, otm-zamanlanmis-gorev
