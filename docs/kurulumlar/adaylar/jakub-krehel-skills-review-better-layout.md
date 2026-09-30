# Jakub Krehel skills (review, better layout)
ad: Jakub Krehel skills (review, better layout)
tur: skill
video: Ysr7oNDajJI
repo: jakubkrehel/skills
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/jakubkrehel/skills
telemetri: Bilinmiyor. README telemetriden söz etmiyor. Skill'ler salt metin talimatıdır. Yine de npx skills kurulum aracı ve skills.sh rozeti kendi istatistiklerini toplayabilir, bunu doğrulamadım.
yildiz: bilinmiyor
alt_tur: araç
skillspector: SkillSpector --no-llm: 6 HIGH/CRITICAL bulgu. Ayrıntı incelenmedi.
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun)
## Ne
Jakub Krehel'in arayüz tasarımı odaklı ajan skill koleksiyonu. Alan başına ayrı skill içerir: better-ui, better-typography, better-colors, better-accessibility, better-layout, better-writing, hepsini birleştiren better-interface ve kullanıcının çağırdığı interface-review, explain-interface, break, variant.
## Mekanizma
Her skill, klasöründeki bir SKILL.md dosyasıdır. Bu dosya ajana ilgili alanın kurallarını ve kontrol listesini verir. Kurallara örnekler: eş merkezli border-radius, optik hizalama, tip ölçeği, gruplama, hizalama, okuma sırası. Ajan projedeki kodu bu kurallara göre inceler ve düzeltir. interface-review birden fazla kategoriyi (UI, tipografi, layout, renk, yazı, erişilebilirlik) tek raporda toplar. break, bir bileşeni geçici bir sayfada tüm durumlarıyla render edip zorlar. variant, bir bileşenin birden fazla varyantını üretir. SKILL.md içeriklerini okumadım. Yukarıdaki ayrıntılar README'ye dayanıyor. Videodaki "puanlama ve GitHub ile önce/sonra karşılaştırma" iddiası README'de geçmiyor.
## Kanıt
- Alan başına ayrı skill var. → doğrulandı · README ve ağaçta better-ui, better-typography, better-colors, better-accessibility, better-layout, better-writing ayrı klasörler olarak görünüyor.
- Review skill puanlar ve GitHub ile önce/sonra karşılaştırır. → sınanamadı · README interface-review'u çok kategorili ayrıntılı analiz olarak tanımlıyor. Puanlama veya GitHub karşılaştırmasından söz etmiyor. SKILL.md okunmadı.
- Layout skill boşluk ve hizayı denetler. → doğrulandı · README: better-layout gruplama, hizalama ve okuma sırasını kapsıyor. Boşluk doğrudan geçmiyor, gruplamayla ilişkili.
- güvenlik ön taraması: SkillSpector --no-llm HIGH/CRITICAL 6
## Kurulum
- npx skills add jakubkrehel/skills
- Claude Code plugin olarak: /plugin marketplace add jakubkrehel/skills
- Ardından: /plugin install interfaces@interfaces
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Arayüz kalitesi için hazır, alan bazlı kontrol listeleri sağlar: layout boşluk ve hizası, tipografi, renk kontrastı, erişilebilirlik. Ayrıca çok kategorili inceleme ve bileşen stres testi sunar.
## Maliyet/risk
Ön taramada SkillSpector --no-llm 6 HIGH/CRITICAL bulgu verdi. Ayrıntıları incelemedim ve yanlış pozitif olabilir. Kurmadan önce SKILL.md dosyaları elle gözden geçirilmeli. Lisans dosyası var ama türünü okuyamadım. break ve variant skill'leri kod yazıp geçici sayfa oluşturabilir, bu yüzden çalıştırılan komutlara dikkat edilmeli. Yıldız sayısı ve son commit doğrulanamadı.
## Tasarruf
Token tasarrufu aracı değil. Skill'ler bağlama yüklendiğinde token tüketir. Alan başına ayrı skill olması, yalnızca gereken alanı yüklemeyi mümkün kılar.
## Üretilebilir
hedef_tur: skill
tarif: Kendi tasarım skill'imizi yazmak kolay. Alan başına bir SKILL.md hazırlanır: layout (gruplama, hizalama, boşluk ölçeği, okuma sırası) ve tipografi gibi. Her birine kontrol listesi ve çıktı biçimi eklenir. Bir interface-review skill'i, alt skill'leri sırayla çağırıp kategori başına puan ve bulgu tablosu üretir. Önce/sonra karşılaştırması için git diff veya ekran görüntüsü adımı eklenir. Orijinal içerik kopyalanmaz. Lisansı doğrulayıp kendi kurallarımızla yeniden yazarız.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun/panel.md → Ömer sütunu
## Özellikler
### better-layout: gruplama, hizalama, okuma sırası denetimi
kaynak: https://github.com/jakubkrehel/skills/blob/main/skills/better-layout/SKILL.md
### interface-review: UI, tipografi, layout, renk, yazı ve erişilebilirlik için çok kategorili inceleme raporu
kaynak: https://github.com/jakubkrehel/skills/blob/main/skills/interface-review/SKILL.md
### break: bileşeni geçici sayfada tüm durumlarıyla render edip stres testi yapar
kaynak: https://github.com/jakubkrehel/skills/blob/main/skills/break/SKILL.md
### variant: bir bileşenin birden fazla varyantını üretir
kaynak: https://github.com/jakubkrehel/skills/blob/main/skills/variant/SKILL.md
### Claude Code plugin marketplace desteği
kaynak: https://github.com/jakubkrehel/skills
## Destek
- Ysr7oNDajJI · 8:55 · Alan başına ayrı skill; review skill puanlar ve GitHub ile önce/sonra karşılaştırır, layout skill boşluk/hizayı denetler. · kanıt: each area gets its own skill
