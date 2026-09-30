# Handoff skill
ad: Handoff skill
tur: skill
video: V0XbuApxlhg
repo: yok
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: bilinmiyor (kaynak kod incelenemedi; yerel dosya yazdığı için ağ çağrısı gerektirmemesi beklenir ama doğrulanmadı)
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun)
## Ne
Bir konuşmanın özetini diskte markdown dosyası olarak saklayan devir (handoff) skill'i; yeni konuşma bu dosyayı okuyarak kaldığı yerden devam eder. Videoda (V0XbuApxlhg, "You're Paying Anthropic 20x MORE Than You Need To") anlatılıyor; skill sunucunun kendi topluluğunda ücretsiz olarak paylaşılıyor.
## Mekanizma
Video bulgusuna göre: skill çağrılınca mevcut oturumun özeti çıkarılıp diske markdown dosyası olarak yazılıyor; yeni oturum başında bu dosya okunuyor. Repo/kaynak kodu görülemedi, ayrıntılar (dosya yolu, şablon) bilinmiyor. Video sayfası getirildiğinde yalnızca başlık geldi, transkript alınamadı.
## Kanıt
- Skill özeti diskte markdown dosyası olarak saklar; yeni konuşma bunu okur. → sınanamadı · Yalnızca video alıntısı: 'It's actually just going to put it on my disk... markdown file with the summary.' Sayfa getirmede transkript gelmedi, skill kodu yok.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- bilinmiyor
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Bağlam şişince temiz oturuma geçişte sürekliliği korur, tekrar açıklama maliyetini azaltır.
## Maliyet/risk
Repo ve lisans yok; skill topluluk üyeliği arkasında olabilir, kaynağı doğrulanamadı. Özet dosyası hassas bilgi içerebilir. Özetleme kayıplı olabilir.
## Tasarruf
Başlığa göre uzun bağlamı taşımak yerine kısa özetle yeni oturum başlatarak token/maliyet tasarrufu amaçlanıyor; ölçülmüş bir oran bilinmiyor.
## Üretilebilir
hedef_tur: skill
tarif: SKILL.md yaz: çağrıldığında oturumdan hedef, yapılanlar, kararlar, açık işler, ilgili dosya yolları ve sonraki adımları çıkar; bunu proje içinde HANDOFF.md (ya da .handoff/tarih.md) olarak yaz. Yeni oturumda başta bu dosyayı oku talimatı ekle (CLAUDE.md satırı veya ikinci bir 'resume' komutu). Sırlar yazılmasın kuralı ekle.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun/panel.md → Ömer sütunu
## Özellikler
### Özeti markdown dosyası olarak diske yazma
kaynak: https://www.youtube.com/watch?v=V0XbuApxlhg
## Destek
- V0XbuApxlhg · 11:39 · Özeti diskte markdown dosyası olarak saklayan devir skill'i; yeni konuşma bu dosyayı okur. Sunucunun kendi skill'i ücretsiz toplulukta. · kanıt: It's actually just going to put it on my disk... markdown file with the summary.
