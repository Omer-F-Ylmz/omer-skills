# Sosyal medya otomasyonu — birleşim tarifi
Ne zaman: İçerik takvimi, platforma özel gönderi ve zamanlanmış yayın kurulumu.

## Fazlar
1. Araştırma: `last30days:last30days` — son 30 günde Reddit, X, YouTube, TikTok ve HN'de konuşulanlar · birlikte: `marketing-skills:social` dinleme ve içerik fikri.
2. Plan: `marketing-skills:content-strategy` — ne üretileceğine karar · birlikte: takvim için `linkedin-agent:li-plan` ya da `youtube-agent:yt-plan`.
3. Üretim: `ecc:content-engine` — tek kaynaktan platformlara uyarlanmış gönderi, yazar sesi korunur · birlikte: `ecc:crosspost` platform kısıtına uyarlar; görsel boyut `adobe-for-creativity:adobe-create-social-variations`.
4. Yayın ve zamanlama: `ecc:social-publisher` — X, LinkedIn, Instagram, TikTok vb. yayın · birlikte: `socialclaw` zamanlama CLI'ı.
5. İzleme: `otm-otomasyon-izleme` — çalışmaları hata, süre ve maliyet için inceler, uyarı önerir.
6. Ölçüm: `urn-icerik-performans` — etkileşim ve dönüşümle tut/güncelle/kes kararı.

## İnceleme ajanları
- `urn-sosyal-medya-icerik`: platforma özel hook ve format kontrolü.
- `sepia:sepia`: AI tadını temizler.

## Güvenlik ve kalite kapıları
- Hesap anahtarları depoda değil: `gitleaks`.
- Görsellerde alt metin: `accessible-content:alt-text-design`.
- Kişisel veri işleniyorsa KVKK: `sec-kvkk-gdpr-kontrol`.
- Otomatik gönderi önce taslak/onay kipinde denenir.

## Tartışma konseyi
- Karar: kanal seçimi ve ana mesaj.
- `marketing-skills:marketing-council` — simüle danışman kurulu. Varsayılan Claude personaları.

## Jeton bütçesi
- Araştırma: orta (~15k, tahmini); ham gönderi okuması `okuyucu` alt ajanına.
- Plan: küçük (~6k). Üretim: orta (~15k). Yayın: küçük (~5k). İzleme + ölçüm: küçük (~6k). Hepsi tahmini.

## Kaçınılacaklar
- URL ya da başkasının taslağından gelen içeriği denetimsiz yayınlamak; `ecc:crosspost` bunun prompt injection taşıyabileceğini söyler.
- Onaysız toplu gönderi; gönderim hesap erişimi ister.
- Ücretli reklam araçlarını (`claude-ads:ads-meta` vb.) organik işe karıştırmak.

## Aday (kurulu değil)
yok
