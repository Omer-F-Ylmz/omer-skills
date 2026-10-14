# Otomasyon satışı ve prototip — birleşim tarifi
Ne zaman: Müşteriye n8n/webhook otomasyonu teklif edip hızlı çalışan prototip göstermek.

## Fazlar
1. Kapsam: `pln-kapsam-kesici` — planı en küçük teslim edilebilir dilime indirir · birlikte: `octo:skill-prototype` tek riskli varsayımı sabit bütçeyle dener.
2. Teklif ve fiyat: `dok-teknik-teklif` — kapsam, takvim, fiyat varsayımlı teklif · birlikte: `urn-fiyatlandirma` değer metriği ve paketler.
3. Akış tasarımı: `otm-n8n-akis-tasarimi` — tetikleyici, dallanma, net düğüm adları · birlikte: `n8n-workflow-patterns` akış yapısı ve webhook işleme kalıbı.
4. Uygulama: `n8n-mcp` — n8n düğüm belgesi ve iş akışı oluşturma/doğrulama · birlikte: `using-n8n-mcp-skills` MCP üzerinden kurma ve hata ayıklama; webhook alıcısı `otm-webhook-tasarimci`.
5. Hata ve test: `n8n-error-handling` — sessiz hatayı önler · birlikte: `otm-n8n-hata-yonetimi` hata akışı, yeniden deneme ve uyarı ekler.
6. İzleme ve teslim: `otm-otomasyon-izleme` — çalışma hatası, süre ve maliyet · birlikte: `superpowers:verification-before-completion` demo öncesi kanıt.

## İnceleme ajanları
- `otm-webhook-tasarimci`: imza kontrolü ve idempotency.
- `ponytail-review`: prototipte gereksiz karmaşıklık.

## Güvenlik ve kalite kapıları
- Webhook imzalı ve idempotent.
- Kimlik bilgileri depoda değil: `gitleaks`.
- Müşteri verisi geçiyorsa KVKK: `sec-kvkk-gdpr-kontrol`.
- Her akışta hata yolu tanımlı.

## Tartışma konseyi
- Karar: kapsam sınırı ve fiyat modeli.
- `ecc:dev-team` — PM/Mimar/Geliştirici/QA personaları paralel alt ajan; ya da daha hafif `ecc:council`. Varsayılan Claude personaları.

## Jeton bütçesi
- Kapsam: küçük (~6k, tahmini). Teklif: orta (~10k). Akış: orta (~10k). Uygulama: büyük (~30k). Hata/test: orta (~10k). Teslim: küçük (~4k). Hepsi tahmini.
- Uzun n8n çalışma logları `okuyucu` alt ajanına.

## Kaçınılacaklar
- `ecc:dev-team` 4 paralel alt ajanla plan limitini hızlı tüketir; küçük işte kullanma.
- n8n sunucusu varsaymak; `n8n-mcp` sunucunun kendisi değildir.
- Teklifte ölçülmemiş tasarruf iddiası.

## Aday (kurulu değil)
yok
