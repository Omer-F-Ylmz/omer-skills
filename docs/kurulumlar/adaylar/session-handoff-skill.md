# Session handoff skill
ad: Session handoff skill
tur: skill
video: 6cEQEba0i2A
repo: yok
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: yok
telemetri: bilinmiyor (kaynak kod yok; salt talimat içeren bir skill için telemetri beklenmez ama doğrulanamadı)
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-29-uzun)
## Ne
Oturum sonunda yapılanları, önemli dosyaları, açık kararları ve nereden devam edileceğini özetleyen bir skill. Özet kopyalanıp /clear sonrası yeni oturuma yapıştırılır; /compact yerine kullanılır.
## Mekanizma
Videoda anlatıldığı kadarıyla skill, modele oturumu dört başlıkta (yapılanlar, önemli dosyalar, açık kararlar, sonraki adım) özetletiyor. Çıktı elle kopyalanıp /clear sonrası yapıştırılıyor. Skill'in gerçek içeriği yayımlanmamış; video sayfası çekildiğinde transkript gelmedi, bu yüzden iç işleyişi doğrulanamadı.
## Kanıt
- Skill oturum özetini (yapılanlar, önemli dosyalar, açık kararlar, devam noktası) üretir ve /compact yerine kullanılır. → sınanamadı · Video sayfası getirildi ama yalnızca YouTube altbilgisi geldi, transkript yoktu. İddia aday bulgusundaki alıntıya dayanıyor; skill'in kendisi bulunamadı.
- Skill ücretsiz olarak paylaşılacak. → sınanamadı · Yalnızca 'Session handoff skill'imi de ücretsiz ekleyeceğim' alıntısı var; bağlantı ya da repo doğrulanmadı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Repo/paket yok; videoda 'ücretsiz ekleyeceğim' deniyor, henüz erişilebilir bir bağlantı doğrulanmadı.
- Kendi SKILL.md dosyanı yazarak benzerini kurabilirsin (aşağıdaki tarife bak).
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Uzun oturumlarda bağlam şişmesini önler, kararların ve devam noktasının kaybolmasını engeller. Oturumlar arası süreklilik sağlar.
## Maliyet/risk
Düşük. Kaynak yok, bu yüzden içerik denetlenemez. Özet eksik olursa bağlam kaybı olur. Elle kopyala-yapıştır adımı gerekir. Özetin gizli bilgi (anahtar vb.) taşımamasına dikkat edilmeli.
## Tasarruf
Mekanizma: /compact'in modelle özet üretme maliyeti ve kalıntı bağlamı yerine, bağlam /clear ile sıfırlanır ve yalnızca kısa bir özet yeni oturuma taşınır. Böylece sonraki her turda taşınan bağlam küçük kalır. Video başlığındaki 'milyonlarca token' iddiası ölçülmedi.
## Üretilebilir
hedef_tur: skill
tarif: ~/.claude/skills/session-handoff/SKILL.md oluştur. Frontmatter: name: session-handoff, description: 'Oturumu /clear öncesi devretmek için özet üret'. Gövde: modele şu başlıklarla kısa bir Markdown üretmesini söyle: 1) Hedef, 2) Yapılanlar, 3) Değişen/önemli dosyalar (yol + tek satır neden), 4) Açık kararlar ve engeller, 5) Sonraki adım (ilk yapılacak komut). Kurallar: en fazla ~300 kelime, sır/anahtar yazma, git status/diff'e bakarak dosya listesini doğrula, çıktıyı tek kod bloğunda ver ki kopyalanabilsin. İsteğe bağlı: özeti HANDOFF.md dosyasına yaz ve yeni oturumda okut.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-29-uzun/panel.md → Ömer sütunu
## Özellikler
### Oturum özeti: yapılanlar, önemli dosyalar, açık kararlar, nereden devam edileceği
kaynak: https://www.youtube.com/watch?v=6cEQEba0i2A
### /clear sonrası yapıştırılabilir devir özeti (/compact alternatifi)
kaynak: https://www.youtube.com/watch?v=6cEQEba0i2A
## Destek
- 6cEQEba0i2A · 6:14 · Oturumda yapılanları, önemli dosyaları, açık kararları ve nereden devam edileceğini özetler; özet kopyalanıp /clear sonrası yapıştırılır. /compact yerine kullanılıyor. · kanıt: Session handoff skill'imi de ücretsiz ekleyeceğim.
