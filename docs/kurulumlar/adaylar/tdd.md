# tdd
ad: tdd
tur: skill
video: EJyuu6zlQCg
repo: mattpocock/skills
lisans: bilinmiyor (repoda LICENSE dosyası var, içeriği okunamadı)
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/mattpocock/skills
telemetri: README'de telemetri belirtilmiyor. Skill'ler düz markdown dosyaları. Kurulum için npx skills installer'ı kullanılıyor, onun telemetrisi denetlenmedi. Bilinmiyor.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-4)
## Ne
Kodlama ajanını kırmızı-yeşil-refactor (TDD) döngüsüne yönlendiren bir agent skill'i. Videoya göre arayüz değişikliklerini kullanıcıya onaylatır, tek seferde tek test yazdırır; refactor, mocking ve derin modül dokümanları da içerir.
## Mekanizma
SKILL.md talimatları ajanın bağlamına girer ve ajanı önce başarısız test (kırmızı), sonra minimum kod (yeşil), sonra refactor adımlarına yönlendirir. Ek referans dosyaları (refactor, mocking, derin modüller) gerektiğinde okunur. Skill'in kendi SKILL.md dosyasını okuyamadım. Mekanizma video anlatımına ve repo yapısına dayanıyor. Aday repo olarak mattpocock/skills varsayıldı. Bunun nedeni adın eşleşmesi ve yazarın bilinen skill seti. Bu eşleşme doğrulanmadı.
## Kanıt
- Ajanı kırmızı-yeşil-refactor döngüsüne yönlendirir → sınanamadı · Yalnızca video alıntısı var (it basically forces the agent... red-green-refactor loop). Video sayfası transkript vermedi, SKILL.md okunamadı.
- mattpocock/skills repo'su tdd skill'inin kaynağıdır → sınanamadı · Repo mevcut ve README skill setini anlatıyor, ama getirilen çıktıda tdd geçmiyor (ağaç derinlik 2, skills/engineering içeriği görünmüyor).
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Claude Code: claude plugins install mattpocock-skills (veya oturum içinde /plugin install mattpocock-skills)
- Diğer ajanlar / düzenlenebilir kopya: npx skills@latest add mattpocock/skills, ardından tdd skill'ini seç
- Repo başına bir kez /setup-matt-pocock-skills çalıştır
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Ajanın testsiz büyük kod yığmasını engeller. Arayüz onayı ve küçük adımlar sayesinde kullanıcı kontrolünü korur.
## Maliyet/risk
Skill içeriği okunmadı. Lisans doğrulanmadı. Repo hızlı değişiyor (changeset dosyaları ve deprecated/in-progress klasörleri var), plugin otomatik güncellenirse davranış değişebilir. Aday "repo yok" diye verilmişti, repo eşleşmesi tahmine dayanıyor.
## Tasarruf
Token aracı değil. Dolaylı etkisi: tek test tek adım yaklaşımı hatalı büyük değişikliklerin yeniden yazılmasını azaltabilir. Bu ölçülmedi.
## Üretilebilir
hedef_tur: skill
tarif: SKILL.md yaz: (1) davranışı ve public arayüzü çıkar, kullanıcıya onaylat; (2) tek başarısız test yaz ve çalıştırıp kırmızıyı doğrula; (3) testi geçirecek en az kodu yaz, yeşili doğrula; (4) test yeşilken refactor yap; (5) sonraki davranış için döngüyü tekrarla. Yan dosyalar: refactor.md, mocking.md (yalnız sistem sınırlarında mock), deep-modules.md.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-4/panel.md → Ömer sütunu
## Özellikler
### Kırmızı-yeşil-refactor döngüsü, tek seferde bir test, arayüz onayı (video anlatımı)
kaynak: https://www.youtube.com/watch?v=EJyuu6zlQCg
### Claude Code plugin olarak veya npx skills ile kurulum
kaynak: https://github.com/mattpocock/skills
## Destek
- EJyuu6zlQCg · 9:30 · Ajanı kırmızı-yeşil-refactor döngüsüne yönlendirir; arayüz değişikliklerini onaylatır, tek seferde bir test yazdırır. Refactor, mocking ve derin modül dokümanları içerir. · kanıt: it basically forces the agent, or encourages the agent rather, to follow a red-green-refactor loop.
