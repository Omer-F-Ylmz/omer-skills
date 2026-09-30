# Septem Agents Pack
ad: Septem Agents Pack
tur: skill
video: cAeQjck1jHs
repo: yok
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: bilinmiyor (kaynak kodu incelenemedi)
yildiz: bilinmiyor
alt_tur: ürün
bizde_karsilik: Kendi alt ajan dosyalarımızı .claude/agents altında yazarak aynı işi yapabiliriz. Ücretli paket gerekmez.
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-7)
## Ne
Projeye 10 adlı uzman alt ajan ekleyen paket (Atlas, Luca, Cannon, Ember, Telly, Nova, Ward, Mira, Juno, Pip). Video bulgusuna göre orijinali yaklaşık 49 dolarlık ücretli paket. Sunucu, ücretsiz kendi sürümünü toplulukta paylaştığını söylüyor. Bu bilgi yalnızca video bulgusundan geliyor.
## Mekanizma
Doğrulanamadı. Büyük olasılıkla her ajan için bir alt ajan tanım dosyası (markdown, .claude/agents) var. Bu bir varsayım. Repo ve içerik incelenemedi. Video sayfası getirildi ama transkript gelmedi.
## Kanıt
- Paket 10 isimli uzman alt ajan ekliyor → sınanamadı · Video sayfası getirildi ama yalnızca YouTube altbilgisi geldi. Transkript ve repo yok.
- Orijinal paket yaklaşık 49 dolar, sunucu ücretsiz sürüm paylaşıyor → sınanamadı · Yalnızca verilen video bulgusunda geçiyor. Bağımsız kaynak doğrulanmadı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Repo veya indirme bağlantısı bilinmiyor; kurulum adımı doğrulanamadı.
- Topluluk sürümü bulunursa, ajan .md dosyaları projedeki .claude/agents/ klasörüne kopyalanır (varsayım).
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Görev türüne göre uzmanlaşmış alt ajanlar sağlayabilir. Kanıtlanmış bir fayda yok.
## Maliyet/risk
Repo yok, lisans ve kaynak belirsiz. Ücretli paketin "ücretsiz kopyası" telif veya lisans ihlali olabilir. Kaynağı doğrulanamayan ajan istemleri komut çalıştırma yetkisiyle gelirse güvenlik riski taşır. Kurmadan önce içerik elle okunmalı.
## Üretilebilir
hedef_tur: skill
tarif: Paketin kendisi kopyalanmamalı. Ajan adları ve rolleri kendi ihtiyacımıza göre yeniden tasarlanabilir: her rol için .claude/agents/<ad>.md dosyası yazılır. Dosyada frontmatter (name, description, tools) ve kısa bir rol istemi bulunur. Örnek roller: kod inceleme, test, güvenlik, dokümantasyon, araştırma. Orijinal içerik kullanılmaz, sıfırdan yazılır.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-7/panel.md → Ömer sütunu
## Özellikler
### 10 isimli uzman alt ajan (Atlas, Luca, Cannon, Ember, Telly, Nova, Ward, Mira, Juno, Pip). Her birinin görevi bilinmiyor.
kaynak: https://www.youtube.com/watch?v=cAeQjck1jHs
## Destek
- cAeQjck1jHs · 9:56 · Projeye 10 isimli uzman alt ajan ekler (Atlas, Luca, Cannon, Ember, Telly, Nova, Ward, Mira, Juno, Pip). · kanıt: Orijinal paket yaklaşık 49 dolar; sunucu ücretsiz kendi sürümünü topluluğa koyduğunu söylüyor.
