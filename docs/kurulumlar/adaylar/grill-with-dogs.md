# grill-with-dogs
ad: grill-with-dogs
tur: skill
video: l_WQx_XUsRY
repo: mattpocock/skills
lisans: MIT
son_commit: 2026-10-07
arsiv: hayır
kaynak: C:/Projeler/.video-cache/repo/mattpocock__skills/skills/engineering/grill-with-docs
telemetri: yok
arastirma: tam
## Ne
Videodaki "grill-with-dogs" büyük olasılıkla "grill-with-docs" ses hatası (repoda dogs yok). Plan/tasarımı tek soru + önerilen cevapla sorgular, GLOSSARY/CONTEXT.md ve ADR'leri yazar. Gövde 1 satır: "grilling" ve "domain-modeling" skill'lerini çağırır.
## Kanıt
- 278867 yıldız · son commit 2026-10-07 · MIT · arşiv değil
- SkillSpector --no-llm HIGH/CRITICAL 15 (LLM'siz tarama, yanlış pozitif olası; skill gövdesi 7 satır, hook/süreç/ağ yok: on.md Mekanizma incelemesi)
- sınırlama: issue #341 (cevaplar PRD/issue'lara izlenemiyor, açık), #831 (eski grill-me istendi), #483 (/code-review ad çakışması, kapalı), #1164 (plugin güncellenmiyor, açık)
## Kurulum
- plugin: mattpocock-skills@claude-plugins-official
## İzinler
Yalnız .md; çalıştırılabilir, ağ, hook yok. Çalışırken repoya CONTEXT.md/GLOSSARY.md ve docs/adr/ yazar. disable-model-invocation: true (yalnız elle çağrılır).
## Duman testi
- komut: claude plugin list
- cikis: 0
- desen: mattpocock-skills
## Geri alma
- plugin: mattpocock-skills@claude-plugins-official
## Köprü izni
- arac: claude
- altIzin: list
## Önerilen katman
T1 (yalnız .md skill)
## Telemetri kapatma
Telemetri yok.
## Özellikler
### grill-with-docs
ne: grilling + domain-modeling'i birlikte çalıştırır; terimleri GLOSSARY'ye, kararları ADR'ye anında yazar.
kurulum: plugin ile gelir; /grill-with-docs.
lisans: MIT
etiket: -
karar: KUR
gerekce: zaten var: katalogta domain-modeling.md ve grill-me benzeri adaylar var; çakışma kontrolü kurulumda
### grilling
ne: tek soru + önerilen cevap, tur tur görüşme.
kurulum: plugin ile gelir.
lisans: MIT
etiket: -
karar: KUR
gerekce: grill-with-docs bağımlılığı
### domain-modeling
ne: alan modeli geçişi; ADR-FORMAT ve GLOSSARY-FORMAT şablonlarıyla belge yazar.
kurulum: plugin ile gelir.
lisans: MIT
etiket: -
karar: KUR
gerekce: grill-with-docs bağımlılığı
### grill-me
ne: belgesiz, yalnız sohbette görüşme (kod dışı kullanım).
kurulum: plugin ile gelir.
lisans: MIT
etiket: -
karar: ÖĞREN
gerekce: grill-with-docs'un belgesiz hali; ayrıca kurmaya gerek yok
## Bağımsız kanıt
- https://www.aihero.dev/skills-grill-with-docs — grill-me ile aynı görüşme, ama diske GLOSSARY.md ve ADR yazan durumlu sürüm.
- https://claudeskills.info/skills/mattpocock/skills/grill-with-docs/ — gövde tek talimat; grilling ve domain-modeling'e bağımlı, grill-me'den ağır.
- https://pablodelarco.com/claude-skills/grill-with-docs — rastgele brief verilince kod yazmadan önce sorgular, CONTEXT.md üretir.
## İddia sınama
| iddia | kaynak | sonuç | not | kart |
|---|---|---|---|---|
| Alternatif görüşme skill'i boşlukları kapatır | https://www.aihero.dev/skills-grill-with-docs | doğru | Terim ve kararları kalıcı dosyaya yazar | - |
| Skill adı "grill-with-dogs" | repo ağacı | yanlış | Repoda yalnız grill-with-docs var | - |
## Kötü yan + onarım + güçlendirme
- token · plugin tüm skill'leri getirir, liste payı oluşur · neden: README plugin tümünü kurar · tahmin · onarım: grill-with-docs/grilling/domain-modeling dışını tembel/devre dışı bırakmak (TOKEN-3 profili) · kaynak: https://github.com/mattpocock/skills
- kalite · /code-review ad çakışması · neden: issue #483 (kapalı) · tahmin · onarım: yalnız 3 skill'i kullanmak, çakışan adı çağırmamak · kaynak: https://github.com/mattpocock/skills/issues/483
- güvenlik · SkillSpector HIGH/CRITICAL 15 · neden: on.md Güvenlik ön taraması · ölçülen (LLM'siz) · onarım: skill klasörü elle gözden geçirilir (gövde 7 satır) · kaynak: on.md
- kalite · plugin güncellenmiyor · neden: issue #1164 · ölçülen · onarım: mattpocock marketplace'ini doğrudan ekle · kaynak: README
güçlendirme: CONTEXT/GLOSSARY çıktısı graphify ile grafiğe bağlanır; departman skill'leriyle ADR'ler yazılır.
## Bizde durum
- kurulum: yok (katalog ve settings'te yok)
- jev skill (Act): yok
