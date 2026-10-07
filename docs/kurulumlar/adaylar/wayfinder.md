# wayfinder
ad: wayfinder
tur: skill
video: l_WQx_XUsRY
repo: mattpocock/skills
lisans: MIT
son_commit: 2026-10-07
arsiv: hayır
kaynak: C:/Projeler/.video-cache/repo/mattpocock__skills/skills/engineering/wayfinder
telemetri: yok
arastirma: yarım: tur tavanı: bağımsız kanıt (web araması) araştırılamadı
## Ne
Büyük, tek oturuma sığmayan işi issue tracker'da paylaşılan harita + karar biletleri olarak planlar; biletleri tek tek çözer. Önce hedef adlandırılır; bilet türleri research/prototype/grilling/task. disable-model-invocation: true (yalnız elle çağrılır).
## Kanıt
- 278867 yıldız · son commit 2026-10-07 · MIT (LICENSE var) · arşiv değil
- SkillSpector --no-llm HIGH/CRITICAL 15 (tüm repo taraması, on.md; wayfinder'a özgü dağılım doğrulanmadı)
- skills/engineering/wayfinder/SKILL.md + agents/openai.yaml + docs/engineering/wayfinder.md
## Kurulum
- plugin: mattpocock-skills@claude-plugins-official
## İzinler
Yalnız .md skill + openai.yaml; betik yok. Tracker işlemleri için gh/issue tracker erişimi (setup-matt-pocock-skills ile seçilir). Paket tümü kurulur (çok skill).
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
T1 (yalnız .md skill; plugin paketi tüm repoyu getirir, HIGH/CRITICAL 15 incelenmeli)
## Özellikler
### harita-ve-bilet-planlama
ne: Hedef/Notlar/Kararlar/Sis bölümlü harita issue'su ve ~100K tokenlık karar biletleri.
kurulum: plugin ile gelir; /wayfinder elle çağrılır, önce /setup-matt-pocock-skills.
lisans: MIT
etiket: -
karar: DENE
gerekce: güvenlik: SkillSpector HIGH/CRITICAL 15 (repo geneli) incelenecek; lisans MIT
## Bağımsız kanıt
- doğrulanamadı: tur tavanı, web araması yapılmadı
## İddia sınama
| iddia | kaynak | sonuç | not | kart |
|---|---|---|---|---|
| Karar haritasını kullanıcıyı sorgulayarak kurar | skills/engineering/wayfinder/SKILL.md | doğru | grilling/research/prototype bilet türleri var | - |
## Kötü yan + onarım + güçlendirme
- token · plugin tüm skill'leri listeler (skill listesi payı) · neden: README kurulum bölümü · tahmin · onarım: skills CLI ile yalnız wayfinder seç (npx skills add) ya da TOKEN-3 profili · kaynak: https://github.com/mattpocock/skills
- kalite · issue tracker kurulumu gerektirir, grill-with-docs/domain-modeling ile çakışabilir · neden: SKILL.md tracker bölümü · tahmin · onarım: yerel-markdown tracker varsayılanı · kaynak: SKILL.md
güçlendirme: graphify haritasıyla bilet kapsamı çıkarılır; departman skill'leri HITL biletlerde.
## Bizde durum
- kurulum: yok (katalog ve settings'te yok)
- jev skill (Act): agent-skills:planning-and-task-breakdown 0.90
