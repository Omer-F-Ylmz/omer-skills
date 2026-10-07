# domain-modeling
ad: domain-modeling
tur: skill
video: l_WQx_XUsRY
repo: mattpocock/skills
lisans: MIT
son_commit: 2026-09-29
arsiv: hayır
kaynak: C:/Projeler/.video-cache/repo/mattpocock__skills/skills/engineering/domain-modeling
telemetri: yok
arastirma: tam
## Ne
Aktif alan modeli disiplini: oturumda terim çatışmasını GLOSSARY.md'ye karşı yakalar, belirsiz terimi keskinleştirir, kenar senaryolarla sınar, kodla çelişkiyi gösterir, çözülen terimi anında GLOSSARY.md'ye yazar; yalnız zor-geri-alınır/şaşırtıcı/gerçek ödünleşimli kararlar için ADR önerir.
## Kanıt
- 278867 yıldız (repo, tüm set) · son push 2026-10-07, son commit (klon) 2026-09-29 · MIT · arşiv değil
- SkillSpector --no-llm HIGH/CRITICAL 15 (on.md; tüm repo klonu için, skill klasörüne özel döküm yok: SKILL.md + 2 .md + agents/openai.yaml, çalıştırılabilir kod yok)
- on.md Mekanizma incelemesi: oturum başı enjeksiyon/hook/süreç yok
- SKILL.md okundu (satır 1-74): yalnız talimat metni, ağ/komut yok
## Kurulum
- plugin: mattpocock-skills@claude-plugins-official
## İzinler
Yalnız dosya yazma: GLOSSARY.md ve docs/adr/ (tembel oluşturur). Plugin tüm seti (grill-me, triage vb.) getirir; yalnız bu skill için `npx skills add` yolu var ama Kurulum türü dışı (elle).
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
T1 (yalnız .md skill; plugin paketi ise tüm set gelir, bkz. kötü yan)
## Özellikler
### sozluk-catisma-denetimi
ne: kullanıcının terimi GLOSSARY.md ile çelişince hemen uyarır, belirsiz terime kanonik terim önerir
kurulum: plugin ile gelir, "terminoloji/GLOSSARY/ADR" konuşulunca tetiklenir
lisans: MIT
etiket: -
karar: UYARLA
gerekce: zaten var: araştırılmadı (katalog taraması yapılmadı); fikir departman skill'ine uyarlanabilir
### adr-teklifi
ne: ADR'yi yalnız üç koşul (zor geri alma, bağlamsız şaşırtıcı, gerçek ödünleşim) birlikte doğruysa önerir
kurulum: aynı skill, ADR-FORMAT.md şablonu
lisans: MIT
etiket: -
karar: DENE
gerekce: lisans: MIT; güvenlik: SkillSpector 15 HIGH/CRITICAL tüm repo için, skill klasörü kod içermez
## Bağımsız kanıt
- https://www.aihero.dev/skills-domain-modeling — yazarın kendi sayfası: terim çatışmasını sorar, çözülen terimi anında yazar (bağımsız değil)
- https://tessl.io/registry/skills/github/mattpocock/skills/domain-modeling — Tessl incelemesi bu skill için "No findings" raporluyor
## İddia sınama
| iddia | kaynak | sonuç | not | kart |
|---|---|---|---|---|
| Skill ortak dili (ubiquitous language) oturum içinde canlı tutar | https://github.com/mattpocock/skills (SKILL.md 1-74) | doğru | SKILL.md bunu açıkça tarif ediyor; etkisi ölçülmedi | - |
## Kötü yan + onarım + güçlendirme
- token · plugin tüm seti ekler, skill listesi payı artar · neden: README kurulum bölümü · tahmin · onarım: yalnız bu skill'i kendi klasörümüze uyarlı kopyasız yazmak (fikir) ya da Skill aracıyla tembel yükleme · kaynak: https://github.com/mattpocock/skills
- kalite · GLOSSARY.md/CONTEXT.md adı sürümler arası değişmiş (skillsmp kopyası CONTEXT.md diyor) · neden: on.md kaynak listesi · tahmin · onarım: GLOSSARY.md adını sabitleyip sürüm pinlemek · kaynak: https://skillsmp.com/creators/mattpocock/skills/skills-engineering-domain-modeling
- güvenlik · SkillSpector 15 HIGH/CRITICAL (tüm repo) · neden: on.md Güvenlik ön taraması · ölçülen · onarım: yalnız taranmış domain-modeling klasörü ile sınırlamak; skill'e özel döküm alınmadı
güçlendirme: graphify çıktısı (kod-terim eşlemesi) kod-ile-çelişki adımını besler; departman skill'leri GLOSSARY.md'yi okuyarak aynı sözlüğü kullanır.
## Bizde durum
- kurulum: yok (katalog ve settings'te yok)
- jev skill (Act): yok
