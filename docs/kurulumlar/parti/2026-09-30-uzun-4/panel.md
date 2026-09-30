# Karar paneli — 2026-09-30-uzun-4

Ömer sütununa AL / RED / ERTELE ya da karar (DENE · ÖĞREN · UYARLA · ZATEN VAR) yaz; boş satır dokunulmaz → `video panel uygula <bu dosya>`.

| aday | tür | video | lisans | güvenlik | önerilen | gerekçe | Ömer |
|---|---|---|---|---|---|---|---|
| jev-typesafe-ai | CLI | 2 | — | koşmadı: kurulu | SOR | araştırılmadı (kurulu) · alt tür çakışması (kurulu > servis) | ZATEN VAR |
| typesafe-agent-prompt-kurulumu | iş akışı | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) | ZATEN VAR |
| claude-code-terminalde-vs-code-icinde | CLI | 1 | yok (kapalı kaynak; Anthropic ticari şartları geçerli, SPDX kimliği yok) | koşmadı: ürün | SOR | ürün: kurulum gereği · bizde karşılığı | RED |
| browser-use-jev | teknik | 1 | — | koşmadı: servis | ÖĞREN | teknik: kurulabilir araç değil | ÖĞREN |
| jev-ile-model-yonlendirme-router | iş akışı | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) | ÖĞREN |
| 176-topluluk-postunu-jev-ile-analiz-etti | prompt | 1 | — | koşmadı: servis | ÖĞREN | prompt: kurulabilir araç değil | ÖĞREN |
| kurulumdan-sonra-api-anahtarinin-calisti | prompt | 1 | — | koşmadı: servis | ÖĞREN | prompt: kurulabilir araç değil | ÖĞREN |
| claude-skills-yetenek-ekleme | skill | 1 | bilinmiyor | koşmadı: ürün | SOR | ürün: kurulum gereği · bizde karşılığı | ZATEN VAR |
| sentetik-kullanicilarla-uygulama-testi | iş akışı | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) | ÖĞREN |
| grill-me | skill | 1 | bilinmiyor (repoda LICENSE dosyası var, içeriği doğrulanamadı) | SkillSpector --no-llm HIGH/CRITICAL 14 | RED | lisans uygunsuz/yok: bilinmiyor (repoda LICENSE dosyası var, içeriği doğrulanamadı) | ZATEN VAR |
| write-a-prd | skill | 1 | bilinmiyor | SkillSpector --no-llm HIGH/CRITICAL 14 | SOR | eksik: lisans, son_commit | ZATEN VAR |
| prd-to-issues | skill | 1 | bilinmiyor (repoda LICENSE dosyası var ama türü okunamadı; MIT olması muhtemel, doğrulanmadı) | SkillSpector --no-llm HIGH/CRITICAL 14 | SOR | eksik: son_commit | ÖĞREN |
| tdd | skill | 1 | bilinmiyor (repoda LICENSE dosyası var, içeriği okunamadı) | SkillSpector --no-llm HIGH/CRITICAL 14 | SOR | eksik: son_commit | ZATEN VAR |
| improve-codebase-architecture | skill | 1 | bilinmiyor | SkillSpector --no-llm HIGH/CRITICAL 14 | SOR | eksik: lisans, son_commit | ÖĞREN |
| ralph-loop | iş akışı | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) | ÖĞREN |
| arastirma-dosyasiyla-grill-me-skill-ini- | prompt | 1 | — | koşmadı: repo yok | ÖĞREN | prompt: kurulabilir araç değil | ÖĞREN |
| grill-oturumundan-sonra-prd-yazma-skill- | prompt | 1 | — | koşmadı: ürün | ÖĞREN | prompt: kurulabilir araç değil | ÖĞREN |

## form_red
- yok
## Eksik alanlar
- EJyuu6zlQCg · write-a-prd · karede_gorulen (kare gönderildi, karede görülen boş olamaz)
## Belirsiz birleşmeler (ad benzer, repo farklı)
- yok
## ÜRETİLEBİLİR / yapım tarifleri
- grill-me: hedef_tur: skill tarif: Zaten skill olduğu için doğrudan uyarlanabilir. ~/.claude/skills/grill-me/SKILL.md dosyası yaz. Frontmatter'da name ve description olsun, description'a 'planı sına, grill me' gibi tetikleyiciler koy. Gövdeye şu kuralları yaz: (1) planın karar ağacını çıkar; (2) dalları bağımlılık sırasıyla gez; (3) her turda tek soru sor, önerdiğin cevabı da yaz; (4) kod tabanından yanıtlanabilecek soruyu sormadan önce Grep/Glob/Read ile ara; (5) varsayımları ve kaçınılan ödünleşimleri açığa çıkar; (6) ortak anlayışa varınca kararların özetini ver. Kendi dilimizde (Türkçe) yazılabilir, upstream metni birebir kopyalamak yerine lisansı doğruladıktan sonra uyarla.
- write-a-prd: hedef_tur: skill tarif: Kendi SKILL.md'mizi yaz: 1) kullanıcıdan problem ve olası çözüm tanımını iste; 2) repoyu Glob/Grep ile keşfet; 3) karar ağacındaki her dalı tek tek sor, bağımlılıkları çöz; 4) ana modülleri ve test edilecek yüzeyleri çiz; 5) PRD şablonunu doldur (problem, çözüm, numaralı kullanıcı hikâyeleri, uygulama kararları, test kararları); 6) gh issue create ile yayımla (önce kullanıcıdan onay al). Mevcut skill'i doğrudan kurmak da mümkün; lisansı önce doğrula.
- prd-to-issues: hedef_tur: skill tarif: Tek bir SKILL.md yeterli. Adımlar: 1) PRD/planı oku. 2) Katmanları uçtan uca kesen ince dikey dilimlere böl. 3) Her dilim için başlık, kabul ölçütü, blocked-by ve HITL/AFK etiketi yaz. 4) Dökümü kullanıcıya göster ve onay al. 5) `gh issue create` ile bağımlılık sırasına göre aç. Sonraki issue'lara önceki issue numaralarını 'Blocked by #N' olarak yaz. Tracker seçimini repo yapılandırma dosyasından oku. Kod gerekmez. Bir kez yazılınca yukarı akışa bağımlılık kalmaz.
- tdd: hedef_tur: skill tarif: SKILL.md yaz: (1) davranışı ve public arayüzü çıkar, kullanıcıya onaylat; (2) tek başarısız test yaz ve çalıştırıp kırmızıyı doğrula; (3) testi geçirecek en az kodu yaz, yeşili doğrula; (4) test yeşilken refactor yap; (5) sonraki davranış için döngüyü tekrarla. Yan dosyalar: refactor.md, mocking.md (yalnız sistem sınırlarında mock), deep-modules.md.
- improve-codebase-architecture: hedef_tur: skill tarif: Zaten skill. Kendi sürümümüz için önce SKILL.md'yi ve LICENSE'ı oku. Sonra kendi skill'imizi yaz: (1) kodu tara, sığ modülleri ve silme testini geçemeyenleri listele, son commit'lerde çok değişen dosyalara ağırlık ver; (2) CONTEXT/glossary ve docs/adr dosyalarını oku, ADR'lerle çelişme; (3) kullanıcı bir aday seçince Task ile 3 alt ajanı paralel başlat ve her birine farklı kısıt ver (en az arayüz, en çok esneklik, ortak durum vb.); (4) sonuçları karşılaştırıp gh issue create ile RFC aç. Lisans uygunsa kopyalamak yerine kendi kelimelerimizle yeniden yaz.
## Kural önerileri (T0)
- typesafe-agent-prompt-kurulumu: TypeSafe konsolundan 'copy agent prompt' kopyalanıp Claude Code'a yapıştırılır, ardından API anahtarı verilir ve Claude Jev'i kurar.
- jev-ile-model-yonlendirme-router: Gelen istek önce Jev'e gidip yönlendirme/puanlama yapar; zor işler pahalı Claude modeline gider.
- sentetik-kullanicilarla-uygulama-testi: Farklı yaş/profilde kullanıcılar oluşturup ajanın uygulamayı hızlı test etmesi; daha az token, dolmayan context.
- ralph-loop: Her GitHub issue'yu bitene kadar döngüyle uygulayan otonom ajan döngüsü; TDD skill'iyle yönlendirilir.
## OLASI EŞDEĞER (Jev p 0.5–0.75)
- yok
## OLASI TEKRAR
- yok
## Araştırılmadı
- jev-typesafe-ai: kurulu 
## Site/UI teknikleri
- Kurs satış sayfası (landing): koyu tema, sol başlık/alt başlık, sağda fiyat kartı, CTA butonu ve geri sayım · EJyuu6zlQCg · 1:09 (kare) → docs/departmanlar/frontend.md
## Anatomi bekliyor
- yok
## Geliştirme önerileri
- yok
## Defter
14 çağrı · $1.1476 · 333964 jeton
