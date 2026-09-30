# write-a-prd
ad: write-a-prd
tur: skill
video: EJyuu6zlQCg
repo: mattpocock/skills
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/mattpocock/skills
telemetri: Bilinmiyor; README'de telemetri belirtilmiyor. Skill'ler düz markdown istem dosyaları; kurulum aracı (npx skills) için ayrıca sınanmadı.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-4)
## Ne
Matt Pocock'un agent skill setindeki (mattpocock/skills) bir skill: kullanıcıyla sorgulama oturumu yapıp ayrıntılı bir PRD (ürün gereksinim belgesi) üretir ve GitHub issue olarak yazar. Güncel repoda bu skill'in yerini "to-prd" almış görünüyor (skills.sh'te to-prd sayfası var); write-a-prd eski ad olabilir.
## Mekanizma
SKILL.md tabanlı istem akışı: (1) kullanıcıdan sorunun ve olası çözümlerin ayrıntılı tanımını ister, (2) kod tabanını keşfeder, (3) planın her yönü hakkında kullanıcıyı sorgular, tasarım ağacının her dalını bağımlılıklarıyla çözer, (4) uygulama için gereken ana modülleri çizer, (5) şablonla PRD yazar: kullanıcı bakışıyla problem, çözüm, numaralı kullanıcı hikâyeleri listesi, uygulama kararları, test kararları; sonra GitHub issue olarak gönderir. Video (EJyuu6zlQCg) terminalde /write-a-prd-user çalıştırıldığını ve 'step 4 — sketching out the major modules' yanıtını gösteriyor. Skill dosyasının kendisini doğrudan okuyamadım; akış arama özetlerine dayanıyor.
## Kanıt
- Skill ayrıntılı açıklama alır, repoyu inceler, kullanıcıyı sorgular, modülleri çizer ve PRD'yi şablonla GitHub issue olarak yazar. → doğrulandı · Web arama özeti (mateuszmidor kopyası, lobehub, explainx) aynı adımları listeliyor; videoda 'step 4 — sketching out the major modules' görüldüğü bildirildi.
- Skill güncel mattpocock/skills reposunda write-a-prd adıyla duruyor. → sınanamadı · Repo ağacı derinlik 2'de skills/engineering, productivity, deprecated vb. klasörler var; içeriği listelenmedi. Arama sonuçlarında skills.sh/to-prd de çıktı, yeniden adlandırılmış olabilir.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Claude Code: claude plugins install mattpocock-skills (veya oturumda /plugin install mattpocock-skills)
- Diğer ajanlar/düzenlenebilir kopya: npx skills@latest add mattpocock/skills (istenen skill'leri seç)
- Repo başına bir kez /setup-matt-pocock-skills çalıştır (issue tracker, etiketler, doküman konumu)
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Belirsiz özellik isteğini koda geçmeden önce sorgulayarak netleştirir ve izlenebilir bir PRD/issue çıktısı verir; yanlış anlaşılma kaynaklı yeniden işi azaltır. Token tasarrufu aracı değil.
## Maliyet/risk
Düşük: salt istem dosyası. Dikkat: lisans doğrulanmadı (repoda LICENSE dosyası var, türü okunamadı); skill adı repoda değişmiş/kullanımdan kalkmış olabilir (to-prd); GitHub issue oluşturduğu için yazma yetkili gh/token kullanır, gereksiz issue açma riski; uzun sorgulama oturumu token harcar.
## Üretilebilir
hedef_tur: skill
tarif: Kendi SKILL.md'mizi yaz: 1) kullanıcıdan problem ve olası çözüm tanımını iste; 2) repoyu Glob/Grep ile keşfet; 3) karar ağacındaki her dalı tek tek sor, bağımlılıkları çöz; 4) ana modülleri ve test edilecek yüzeyleri çiz; 5) PRD şablonunu doldur (problem, çözüm, numaralı kullanıcı hikâyeleri, uygulama kararları, test kararları); 6) gh issue create ile yayımla (önce kullanıcıdan onay al). Mevcut skill'i doğrudan kurmak da mümkün; lisansı önce doğrula.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-4/panel.md → Ömer sütunu
## Özellikler
### Kullanıcıyı tasarım ağacı boyunca sorgulama (grilling) ile gereksinim netleştirme
kaynak: https://github.com/mattpocock/skills
### Kod tabanını keşfedip ana modülleri çizme
kaynak: https://explainx.ai/skills/mattpocock/skills/write-a-prd
### Şablonlu PRD: problem, çözüm, numaralı kullanıcı hikâyeleri, uygulama ve test kararları; GitHub issue olarak çıktı
kaynak: https://claudemarketplaces.com/skills/mattpocock/skills/write-a-prd
## Destek
- EJyuu6zlQCg · 3:55 · Ayrıntılı açıklama alır, repoyu inceler, kullanıcıyı sorgular, modülleri çizer ve PRD'yi şablonla GitHub issue olarak yazar. · kanıt: Terminalde /write-a-prd-user çalıştırılıyor; 'step 4 — sketching out the major modules' yanıtı. (karede: EKSİK: karede_gorulen (kare gönderildi, karede görülen boş olamaz))
