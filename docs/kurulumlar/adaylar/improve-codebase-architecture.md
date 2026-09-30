# improve-codebase-architecture
ad: improve-codebase-architecture
tur: skill
video: EJyuu6zlQCg
repo: mattpocock/skills
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/mattpocock/skills
telemetri: Bulgu yok. README'de telemetri ya da veri toplama anlatılmıyor. Skill düz Markdown dosyalarından oluşuyor. İlgili install betiği (npx skills) ve skills.sh kullanım istatistiği tutabilir, bunu doğrulamadım.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-4)
## Ne
Matt Pocock'un "skills" deposundaki (skills/engineering/improve-codebase-architecture) bir ajan skill'i. Kod tabanını tarayıp sığ modülleri (arayüzü, gizlediği işin neredeyse kadar karmaşık olduğu modüller) derin modüllere dönüştürme fırsatlarını listeler. Arayüz alternatifleri tasarlatır ve sonucu refactor RFC'si olarak GitHub issue'ya yazar. Periyodik bakım için tasarlanmış: birkaç günde bir, başka zincirlerin dışında çalıştırılıp iş kuyruğu üretir.
## Mekanizma
Ajan kod tabanını gezer ve "deepening" adaylarını çıkarır. Belirli bir sözlük kullanır: module, interface, depth, seam, adapter, leverage, locality. Ayrıca "silme testi" ve "arayüz test yüzeyidir" ilkelerini uygular. Yakın zamanda değişen bölgelere daha çok ağırlık verir, çünkü derinleştirme gelecekteki değişiklikleri kolaylaştırır. Proje belgelerini okur: CONTEXT.md (repo README'sinde GLOSSARY olarak yeniden adlandırılmış görünüyor) iyi seam'lere ad verir, docs/adr/ altındaki ADR'ler yeniden tartışılmayacak kararları tutar. Video bulgusuna göre bir aday seçilince 3 alt ajan paralel çalışır ve her biri kökten farklı bir arayüz tasarlar. Sonra karşılaştırılır ve refactor RFC'si GitHub issue olarak açılır. Not: SKILL.md içeriğini doğrudan okuyamadım. Alt ajan ve issue akışı yalnızca video özetine dayanıyor.
## Kanıt
- Skill 3 paralel alt ajanla kökten farklı arayüzler tasarlatır. → sınanamadı · Yalnızca verilen video bulgusunda geçiyor. Video sayfası getirilemedi (yalnızca YouTube alt bilgisi geldi) ve SKILL.md okunamadı.
- Refactor RFC'yi GitHub issue olarak açar. → sınanamadı · Yalnızca video bulgusunda geçiyor. Arama özeti bunu doğrulamıyor.
- Skill kod tabanında sığ modülleri derinleştirme adayları olarak bulur. → doğrulandı · Arama sonucu özeti (github.com/mattpocock/skills, tessl, skills.sh) skill'i tam bu şekilde tanımlıyor.
- Skill, mattpocock/skills deposunda ve skills/engineering altında bulunur. → doğrulandı · Arama sonucu URL'si: github.com/mattpocock/skills/blob/main/skills/engineering/improve-codebase-architecture/SKILL.md. Depo ağacında skills/engineering var.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Claude Code eklentisi: claude plugins install mattpocock-skills (ya da oturum içinde /plugin install mattpocock-skills)
- Düzenlenebilir dosyalar için: npx skills@latest add mattpocock/skills (istenen skill'ler seçilir, setup-matt-pocock-skills de seçilmeli)
- Her repoda bir kez /setup-matt-pocock-skills çalıştır: issue tracker (GitHub/Linear/yerel dosya), etiketler ve doküman konumu sorulur
- İkisini birden kurma: her skill iki kez yüklenir
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Mimari borcu düzenli ve yapılandırılmış biçimde görünür kılar. Ortak bir sözlük kullanır. Alternatif arayüzleri karşılaştırarak ilk akla gelen tasarıma takılmayı önler. Çıktı issue olarak kuyruğa girdiği için iş sonradan yapılabilir.
## Maliyet/risk
Lisans doğrulanamadı: depoda LICENSE dosyası var ama türünü okumadım. Yeniden kullanmadan önce kontrol et. Paralel alt ajanlar token ve maliyeti artırır. Skill, GitHub issue açtığı için yazma izni gerektirir. Repo README'si sık değişiyor (changeset'ler, yeniden adlandırmalar). Claude Code eklentisi salt okunur ve otomatik güncellenir, bu da sürüm kayması riski taşır. Skill içeriğini ve video transkriptini doğrudan doğrulayamadım.
## Tasarruf
Token aracı değil. Tersine, 3 paralel alt ajan token harcamasını artırır.
## Üretilebilir
hedef_tur: skill
tarif: Zaten skill. Kendi sürümümüz için önce SKILL.md'yi ve LICENSE'ı oku. Sonra kendi skill'imizi yaz: (1) kodu tara, sığ modülleri ve silme testini geçemeyenleri listele, son commit'lerde çok değişen dosyalara ağırlık ver; (2) CONTEXT/glossary ve docs/adr dosyalarını oku, ADR'lerle çelişme; (3) kullanıcı bir aday seçince Task ile 3 alt ajanı paralel başlat ve her birine farklı kısıt ver (en az arayüz, en çok esneklik, ortak durum vb.); (4) sonuçları karşılaştırıp gh issue create ile RFC aç. Lisans uygunsa kopyalamak yerine kendi kelimelerimizle yeniden yaz.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-4/panel.md → Ömer sütunu
## Özellikler
### Derinleştirme adaylarını tarar (sığ modül → derin modül), yakın zamanda değişen kodu öne çıkarır
kaynak: https://github.com/mattpocock/skills/blob/main/skills/engineering/improve-codebase-architecture/SKILL.md
### Sabit mimari sözlük kullanır (module, interface, depth, seam, adapter, leverage, locality) ve silme testini uygular
kaynak: https://github.com/mattpocock/skills/blob/main/skills/engineering/improve-codebase-architecture/SKILL.md
### CONTEXT/sözlük ve docs/adr kararlarını okuyup bunlarla çelişmez
kaynak: https://github.com/mattpocock/skills/blob/main/docs/engineering/improve-codebase-architecture.md
### 3 paralel alt ajanla alternatif arayüzler tasarlatır, RFC'yi GitHub issue yapar (video iddiası)
kaynak: https://www.youtube.com/watch?v=EJyuu6zlQCg
### Claude Code eklentisi ya da npx skills ile kurulur
kaynak: https://github.com/mattpocock/skills
## Destek
- EJyuu6zlQCg · 12:04 · Kod tabanını keşfeder, derinleştirme adaylarını listeler, 3 paralel alt ajanla farklı arayüzler tasarlatır ve refactor RFC'yi GitHub issue olarak açar. · kanıt: spawn three subagents in parallel, each of which must produce a radically different interface
