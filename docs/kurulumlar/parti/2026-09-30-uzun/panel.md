# Karar paneli — 2026-09-30-uzun

Ömer sütununa AL / RED / ERTELE ya da karar (DENE · ÖĞREN · UYARLA · ZATEN VAR) yaz; boş satır dokunulmaz → `video panel uygula <bu dosya>`.

| aday | tür | video | lisans | güvenlik | önerilen | gerekçe | Ömer |
|---|---|---|---|---|---|---|---|
| prompt-caching | teknik | 1 | — | koşmadı: servis | ÖĞREN | teknik: kurulabilir araç değil | ÖĞREN |
| clear | ipucu | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) | ZATEN VAR |
| compact | ipucu | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) | ZATEN VAR |
| handoff-skill | skill | 1 | bilinmiyor | koşmadı: repo yok | SOR | eksik: lisans, son_commit | UYARLA |
| advisor-modu | iş akışı | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) | ZATEN VAR |
| codex-plugin-for-claude-code | plugin | 1 | bilinmiyor (repoda LICENSE ve NOTICE dosyası var, metni okunamadı; büyük olasılıkla Apache-2.0 ama doğrulanmadı) | SkillSpector --no-llm HIGH/CRITICAL 4 | SOR | eksik: son_commit | ERTELE |
| fable-advisor | skill | 1 | bilinmiyor (repoda LICENSE dosyası var, ancak README çıktısında lisans türü kesildi; SPDX doğrulanmadı) | SkillSpector --no-llm HIGH/CRITICAL 1 | SOR | eksik: son_commit | ÖĞREN |
| doctor | CLI | 1 | bilinmiyor | koşmadı: ürün | SOR | ürün: kurulum gereği · bizde karşılığı | ZATEN VAR |
| context | CLI | 1 | — | koşmadı: kurulu | SOR | araştırılmadı (kurulu) · alt tür çakışması (kurulu > servis) | ZATEN VAR |
| ponytail | skill | 1 | MIT | koşmadı: kurulu | ZATEN VAR | kurulu: ponytail · alt tür çakışması (kurulu > ürün) | ZATEN VAR |
| caveman | skill | 1 | MIT + BSL-1.1 | koşmadı: ürün | SOR | ürün: kurulum gereği · bizde karşılığı · eksik: bizde_karsilik | ZATEN VAR |
| codrops-noise-transition-alev-gurultu-ef | teknik | 1 | — | koşmadı | ÖĞREN | teknik: kurulabilir araç değil | ÖĞREN |
| sketchfab-ile-hazir-3d-model-bulma | iş akışı | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) | ÖĞREN |
| referans-siteyi-vererek-awwwards-seviyes | prompt | 1 | — | koşmadı: ürün | ÖĞREN | prompt: kurulabilir araç değil | ÖĞREN |
| modelin-tarayicida-kendi-ciktisini-test- | iş akışı | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) | ZATEN VAR |
| emil-kowalski-skills | skill | 1 | bilinmiyor | SkillSpector --no-llm HIGH/CRITICAL 8 | SOR | eksik: lisans, son_commit | UYARLA |
| garden-skills-web-design-engineer | skill | 1 | MIT | koşmadı: SkillSpector raporu yok | SOR | eksik: son_commit | UYARLA |
| ai-design-skills-elia-design | skill | 1 | MIT | SkillSpector --no-llm HIGH/CRITICAL 2 | SOR | eksik: son_commit | ÖĞREN |
| meng-to-skills-awards-quality-sites | skill | 1 | bilinmiyor | koşmadı: SkillSpector raporu yok | SOR | eksik: lisans, son_commit | UYARLA |
| jakub-krehel-skills-review-better-layout | skill | 1 | bilinmiyor | SkillSpector --no-llm HIGH/CRITICAL 6 | SOR | eksik: lisans, son_commit | UYARLA |
| tastemaker | skill | 1 | MIT | SkillSpector --no-llm HIGH/CRITICAL 11 | SOR | eksik: son_commit | UYARLA |
| designer-skills-screen-critique-percepti | skill | 1 | — | koşmadı: kurulu | SOR | araştırılmadı (kurulu) | ZATEN VAR |
| animate-skill-ini-cagirip-mevcut-sitenin | prompt | 1 | — | koşmadı: servis | ÖĞREN | prompt: kurulabilir araç değil | ÖĞREN |
| ponytail-gelistirme | skill | 1 | — | — | ÖĞREN | Kendi görevlerimizde ponytail açık ve kapalı iki koşulda aynı iş için üretilen satır sayısı ve token maliyetini karşılaştıran küçük bir ölçüm yap. Sonucu kayda al. Etki anlamlı değilse ponytail'in surec-inceleme'deki yerini yeniden değerlendir. (kanıt: 17:33 — 'It reduces the amount of code Claude writes while maintaining its effectiveness.' (video iddiası); bizdeki kayıtta ölçüm alanı yok.) | DENE |

## form_red
- yok
## Eksik alanlar
- Ysr7oNDajJI · Animate · karede_gorulen (kare gönderildi, karede görülen boş olamaz)
## Belirsiz birleşmeler (ad benzer, repo farklı)
- yok
## ÜRETİLEBİLİR / yapım tarifleri
- handoff-skill: hedef_tur: skill tarif: SKILL.md yaz: çağrıldığında oturumdan hedef, yapılanlar, kararlar, açık işler, ilgili dosya yolları ve sonraki adımları çıkar; bunu proje içinde HANDOFF.md (ya da .handoff/tarih.md) olarak yaz. Yeni oturumda başta bu dosyayı oku talimatı ekle (CLAUDE.md satırı veya ikinci bir 'resume' komutu). Sırlar yazılmasın kuralı ekle.
- codex-plugin-for-claude-code: hedef_tur: plugin tarif: Zaten hazır plugin var, yeniden yazmaya gerek yok; doğrudan kurulabilir. Kendi sürümümüz istenirse: .claude-plugin/marketplace.json ile bir plugin oluşturulur. İçine slash komutları (review, rescue, status) konur. Bunlar Bash ile `codex exec` / `codex review` çağırır, çıktıyı dosyaya yazar, arka plan işleri için PID/iş kaydı tutar. İnceleme için ayrıca bir alt ajan tanımı eklenir.
- fable-advisor: hedef_tur: skill tarif: Kendi skill'imizi yaz: (1) agents/advisor.md: model'i pinlenmiş, yalnızca Read/Grep/Glob araçlı, temiz bağlamda çalışan salt-okunur inceleme ajanı; çıktı ship/fix-first/rethink. (2) skills/orchestration/SKILL.md: hangi işin hangi lane'e gideceği tablosu, altı satırlık spec şablonu (hedef, dosyalar, kısıtlar, doğrulama, REASONING vb.), 'iş bitmeden advisor incelemesi' kuralı. (3) İsteğe bağlı implementer ajanı: `codex exec` çağıran, çıktıyı yapılandırılmış STATUS ile döndüren sarmalayıcı. (4) CLAUDE.md'ye tek satırlık zorunlu-danışma kuralı. Önce yalnızca (1)+(4) ile başla; Codex bağımlılığını sonra ekle.
- doctor: hedef_tur: skill tarif: 'bağlam-diyeti' adında bir skill yazılabilir. Adımlar: (1) CLAUDE.md ve ~/.claude/CLAUDE.md boyutunu ölç. (2) settings ve .mcp.json içindeki MCP sunucularını ile skill klasörlerini listele. (3) Son oturumlarda kullanılmayanları işaretle. (4) Kaldırma ve kısaltma önerilerini onay isteyerek sun. /doctor çıktısı ek girdi olarak kullanılabilir.
- ponytail: hedef_tur: skill tarif: Bir SKILL.md yaz. Ajana kod yazmadan önce 7 basamaklı merdiveni (gerekli mi, kod tabanında var mı, stdlib, native özellik, mevcut bağımlılık, tek satır, minimum) uygulamasını söyle. Önce ilgili kodu okumayı ve doğrulama, hata yönetimi, güvenlik ve erişilebilirliği asla kesmemeyi şart koş. Önce/sonra örnekleri ekle. Etkiyi kendi ortamımızda 5-10 görevle git diff satırı ve token ölçerek sına. Kopyalamak yerine MIT lisansına atıf vererek sıfırdan yazmak daha temiz.
- emil-kowalski-skills: hedef_tur: skill tarif: Kendi arayüz skill'imizi aynı yapıda yazabiliriz: skills/<ad>/SKILL.md içinde 'ajanın sık yaptığı hata → doğru yaklaşım' çiftleri. Örnekler: giriş için ease-out, çıkış için ease-in, transform ve opacity dışı özellikleri animasyonlamama, süre aralıkları, prefers-reduced-motion. Ayrıca bir inceleme skill'i (kuralları kod tabanında tarayıp öncelikli plan çıkarır) ve bir animasyon sözlüğü skill'i eklenebilir. Doğrudan kopyalamak yerine, lisans doğrulanana kadar kuralları kendi ifademizle yazmak daha güvenli.
- garden-skills-web-design-engineer: hedef_tur: skill tarif: Kendi 'design-engineer' skill'imizi yazın. (1) SKILL.md: Design Read adımı olarak brief'i beş kadrana (varyans, hareket, yoğunluk, varlık, marka) çevirsin. Ardından tasarım sistemi beyanı, erken v0, tam yapım ve doğrulama sırası gelsin. (2) references/style-recipes/ altında her stil için palet, tipografi, imza hareketler ve anti-pattern içeren kısa bir dosya olsun. Yalnızca seçilen tarif yüklensin. (3) anti-cliché kara listesi ayrı bir dosyada tutulsun. (4) İsteğe bağlı kabul adımı için mevcut tarayıcı/Playwright aracımızı çağırsın. Kod kopyalamak yerine yapıyı örnek alıp içeriği kendimiz yazalım. MIT lisansı atıf gerektirir. Önce SKILL.md ve references dosyalarını okuyup tarifi netleştirmek gerekir.
- ai-design-skills-elia-design: hedef_tur: skill tarif: Kendi landing-page skill'imizi SKILL.md olarak yaz. Bölümler: (1) giriş soruları (hedef eylem, kitle, teklif), (2) sayfa iskeleti (hero, kanıt, fayda, SSS, CTA) ve tek eylem kuralı, (3) dönüşüm metni yönergeleri, (4) SEO kontrol listesi (başlık, meta, başlık hiyerarşisi), (5) en altta değiştirilebilir 'tasarım değerleri' bölümü (font, renk, boşluk ölçeği, radius, hareket). Doğrudan kopyalamak yerine MIT lisansıyla forklayıp Türkçe ve kendi marka değerlerimizle uyarlamak daha hızlı. Önce SKILL.md'yi okuyup SkillSpector'ın 2 bulgusunu incele.
- meng-to-skills-awards-quality-sites: hedef_tur: skill tarif: Kendi 'awards-site-principles' skill'imizi yaz: SKILL.md içinde ne zaman kullanılacağı (landing page, scroll hikayesi), varsayılanlar (tipografi, boşluk, hareket zamanlaması, scroll tetikli bölüm geçişleri, GSAP/ScrollTrigger ya da CSS scroll-timeline) ve tuzaklar (performans, reduced-motion, mobil) yer alsın. references/ altında efekt tarifleri (parallax, pin, mask reveal) tut. Depodaki web-design skill'lerini okuyup fikirleri kendi sözlerimizle yeniden yaz, kopyalama. Önce lisansı doğrula.
- jakub-krehel-skills-review-better-layout: hedef_tur: skill tarif: Kendi tasarım skill'imizi yazmak kolay. Alan başına bir SKILL.md hazırlanır: layout (gruplama, hizalama, boşluk ölçeği, okuma sırası) ve tipografi gibi. Her birine kontrol listesi ve çıktı biçimi eklenir. Bir interface-review skill'i, alt skill'leri sırayla çağırıp kategori başına puan ve bulgu tablosu üretir. Önce/sonra karşılaştırması için git diff veya ekran görüntüsü adımı eklenir. Orijinal içerik kopyalanmaz. Lisansı doğrulayıp kendi kurallarımızla yeniden yazarız.
- tastemaker: hedef_tur: skill tarif: Kendi skill'imizi yazabiliriz. Yapı: (1) SKILL.md, arayüz işlerinde tetiklenir ve önce spec okunup tasarım gereken ekranlar çıkarılır. (2) scripts/extract_palette.py: Pillow ile görseli küçültüp k-means veya median-cut ile baskın renkleri, sRGB'den luminans ve kontrast oranlarını çıkarır. (3) scripts/check_contrast.py --matrix: paletteki her çift için WCAG oranını hesaplar. 4.5 ve üzeri metin, 3 ve üzeri kenarlık/UI, altı ise yasak olarak etiketlenir. (4) Stil kararlarını .style-lock.md dosyasına yazıp sonraki ekranlarda okuma kuralı. (5) references/ altında anti-slop kontrol listesi: indigo-mor gradyan, emoji ikon, harf kutulu logo gibi kalıpları yasakla. Kodu doğrudan kopyalamak yerine bu tarife göre sıfırdan yazmak daha güvenli. Önce upstream betikleri okunmalı.
## Kural önerileri (T0)
- clear: Cache kaybolunca konuşma geçmişini silip sıfırdan başlama; proje dosyaları bağlamı taşır.
- compact: Konuşmayı özetleyip yeni konuşmanın mesaj geçmişine koyar; otomatik compact'ı beklemeden çalıştırmak önerilir.
- advisor-modu: Büyük model plan yapar, küçük model (Sonnet) uygular; her ikisinin ayrı cache'i vardır.
- sketchfab-ile-hazir-3d-model-bulma: Ücretsiz 3D modelleri Sketchfab'da İngilizce arama ('energy drink') ile bulup projeye vermek.
- modelin-tarayicida-kendi-ciktisini-test-: Opus 5.5 tarayıcıyı kullanıp modeli döndürme, hızlı kaydırma gibi adım adım animasyon testi yapıyor ve hatalarını düzeltiyor.
## OLASI EŞDEĞER (Jev p 0.5–0.75)
- yok
## OLASI TEKRAR
- yok
## Araştırılmadı
- context: kurulu 
- designer-skills-screen-critique-percepti: kurulu 
## Site/UI teknikleri
- 3D karusel / vitrin · ptGXxk1-Uj4 · 5:46 (kare) → docs/departmanlar/frontend.md
- Arka planda alev/gürültü efekti + renk değişimi · ptGXxk1-Uj4 · 0:30 (kare) → docs/departmanlar/frontend.md
- Referans site (Ciao Energy) vitrin düzeni · ptGXxk1-Uj4 · 4:44 (kare) → docs/departmanlar/frontend.md
- Özellik seçimi ve modelin döndürülmesiyle senkron içerik · ptGXxk1-Uj4 · 11:26 (altyazı) → docs/departmanlar/frontend.md
- Yükleme animasyonu ve rüzgarda eğilen modeller · ptGXxk1-Uj4 · 10:24 (altyazı) → docs/departmanlar/frontend.md
- Mobil düzen · ptGXxk1-Uj4 · 12:57 (altyazı) → docs/departmanlar/frontend.md
- BLAZING ENERGY sitesi, turuncu 'BLAZING MANGO' ekranı, turuncu gürültü/alev dokusu, ortada turuncu kutu, sağ üstte Contact ve Menu. · ptGXxk1-Uj4 · 0:30 (kare) → docs/departmanlar/frontend.md
- İki dilli 'HATA BULUNDU / BUG FOUND' slaytı: st.from.p Vector3 ama from.p[i] gibi indekslenmiş, NaN dönüşümleri; 'DÜZELTİYORUM / FIXING'. · ptGXxk1-Uj4 · 1:32 (kare) → docs/departmanlar/frontend.md
- Ciao Energy sitesi: ortada mor kutu, altta 'DOUBLE LITCHI', 'SCROLLER POUR DÉCOUVRIR'. · ptGXxk1-Uj4 · 4:44 (kare) → docs/departmanlar/frontend.md
- Blazing Energy sitesi: 'BERRY', 'Zero sugar — 140 mg caffeine', 'After-hours fuel.', sayaç 05/05, 'BLACKCURRANT · VIOLET · AÇAÍ'. · ptGXxk1-Uj4 · 5:46 (kare) → docs/departmanlar/frontend.md
- Landing page için tek eyleme odaklı görsel sistem (renk, tipografi, boşluk) · Ysr7oNDajJI · 5:24 (altyazı) → docs/departmanlar/frontend.md
- Scroll tabanlı hikaye anlatımı ve ince animasyonlu arka plan · Ysr7oNDajJI · 8:27 (altyazı) → docs/departmanlar/frontend.md
- Koyu yeşil hero, serif başlık, yuvarlak CTA butonları, dekoratif çatal-bıçak illüstrasyonları · Ysr7oNDajJI · 3:30 (kare) → docs/departmanlar/frontend.md
- Küçük etkileşim animasyonları (form gönderimi, hover'da grafikler) · Ysr7oNDajJI · 3:12 (altyazı) → docs/departmanlar/frontend.md
- Ortada açık renkli bir landing page kartı, altta soluk dört benzer kart; şablon/kalıp vurgusu. · Ysr7oNDajJI · 0:30 (kare) → docs/departmanlar/frontend.md
- Koyu zeminde 'skill' etiketli küçük bir açılır kutu. · Ysr7oNDajJI · 1:05 (kare) → docs/departmanlar/frontend.md
- Solda site taslağı, sağda 'Animate' paneli; 5 adımlı liste, ilk dördü tamamlanmış, 5. sırada. · Ysr7oNDajJI · 1:40 (kare) → docs/departmanlar/frontend.md
- Salt & Ember restoran sitesi hero bölümü: 'Twelve seats. One fire. No gas line.' · Ysr7oNDajJI · 3:30 (kare) → docs/departmanlar/frontend.md
## Anatomi bekliyor
- yok
## Geliştirme önerileri
- ponytail · video: Claude'un yazdığı kod miktarını azaltıp etkinliği korumak için kullanılan popüler skill; 17:33'te Fable ile benchmark sayıları tutuldu (sayıların kendisi bilinmiyor). · bizde: ponytail plugin olarak kurulu (surec-inceleme departmanı, p=1.0): 'Lazy senior dev mode' — YAGNI, önce stdlib, istenmemiş soyutlama yok. Bizde kullanımını ya da etkisini ölçen kayıt görünmüyor. · fark: Videodaki tek somut ek yan, benchmark ile kod miktarı/maliyet düşüşünün sayısal ölçülmesi. Bizde kurulu ama kod hacmi veya maliyet etkisi ölçülmüyor. Skill içeriği açısından fark bilinmiyor; video ayrıntısı alınmadı. · ÖĞREN: Kendi görevlerimizde ponytail açık ve kapalı iki koşulda aynı iş için üretilen satır sayısı ve token maliyetini karşılaştıran küçük bir ölçüm yap. Sonucu kayda al. Etki anlamlı değilse ponytail'in surec-inceleme'deki yerini yeniden değerlendir. · kanıt: 17:33 — 'It reduces the amount of code Claude writes while maintaining its effectiveness.' (video iddiası); bizdeki kayıtta ölçüm alanı yok.
## Defter
19 çağrı · $1.2375 · 329171 jeton
