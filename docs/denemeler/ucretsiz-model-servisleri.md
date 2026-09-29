# Ücretsiz model servisleri denemesi — groq · nvidia-nim
durum: plan (koşulmaz) · karar: Ömer DENE (panel 2026-09-29-short, 2026-09-29)

## Amaç
Token tasarrufu: basit işleri ücretsiz katmanlı model servisine yönlendirmek.

## Ölçüt (servis — OSS lisans kapısı uygulanmaz)
- kullanım koşulları (ticari kullanım, çıktı hakları)
- ücretsiz katman (istek/dk, günlük jeton)
- veri gizliliği (eğitimde kullanım, saklama süresi)

## Adaylar
- groq — docs/kurulumlar/adaylar/groq.md
- nvidia-nim — docs/kurulumlar/adaylar/nvidia-nim.md

## Deneme tasarımı (koşulmaz; koşulduğunda tavan: servis başına en fazla 10 istek)
- aynı 3 basit görev iki serviste; anahtar env'de, değeri hiçbir çıktıya yazılmaz
- ölçüm: kalite (elle), gecikme, jeton; koşullar/gizlilik notu
- ilgili: kuyruktaki markitdown denemesi ayrı dosya
