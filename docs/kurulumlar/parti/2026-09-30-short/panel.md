# Karar paneli — 2026-09-30-short

Ömer sütununa AL / RED / ERTELE ya da karar (DENE · ÖĞREN · UYARLA · ZATEN VAR) yaz; boş satır dokunulmaz → `video panel uygula <bu dosya>`.

| aday | tür | video | lisans | güvenlik | önerilen | gerekçe | Ömer |
|---|---|---|---|---|---|---|---|
| claude-code | CLI | 1 | bilinmiyor | koşmadı: kurulu | ZATEN VAR | kurulu: kendi aracımız | ZATEN VAR |
| framer-motion | teknik | 1 | — | koşmadı | ÖĞREN | teknik: kurulabilir araç değil | ÖĞREN |
| ui-ux-pro-max-skill | skill | 1 | — | koşmadı: kurulu | SOR | araştırılmadı (kurulu) | ZATEN VAR |
| 21st-dev-komutu | iş akışı | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) | ZATEN VAR |
| emil-kowalski-skill | skill | 2 | bilinmiyor | SkillSpector --no-llm HIGH/CRITICAL 8 | SOR | eksik: lisans, son_commit | UYARLA |
| impeccable | skill | 3 | — | koşmadı: kurulu | ZATEN VAR | kurulu: impeccable · alt tür çakışması (kurulu > ürün) | ZATEN VAR |
| taste-skill | skill | 3 | — | koşmadı: kurulu | ZATEN VAR | kurulu: taste-skill · alt tür çakışması (kurulu > ürün) | ZATEN VAR |
| emil-kowalski-motion-skill | skill | 1 | bilinmiyor (repoda LICENSE dosyası var ama içeriği okunamadı) | koşmadı: ürün | SOR | ürün: kurulum gereği · bizde karşılığı · eksik: bizde_karsilik | UYARLA |
| open-design | iş akışı | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) | ÖĞREN |
| google-stitch | MCP | 1 | bilinmiyor | koşmadı: servis | SOR | servis: koşullar · ücretsiz katman · gizlilik | ZATEN VAR |
| dribbble-referans-gorseli | iş akışı | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) | ZATEN VAR |
| stitch-mcp-disa-aktarimi | MCP | 1 | bilinmiyor | koşmadı: servis | SOR | servis: koşullar · ücretsiz katman · gizlilik | ZATEN VAR |
| cell-fracture-eklentisi | plugin | 1 | GPL-3.0-or-later | koşmadı: repo yok | SOR | eksik: son_commit | ÖĞREN |
| geometry-nodes-ile-kure-animasyonu | teknik | 1 | — | koşmadı: ürün | ÖĞREN | teknik: kurulabilir araç değil | ÖĞREN |
| figma-maskeli-baslik-sayilari | teknik | 1 | — | koşmadı: ürün | ÖĞREN | teknik: kurulabilir araç değil | ÖĞREN |
| solidify-modifier | teknik | 1 | — | koşmadı: ürün | ÖĞREN | teknik: kurulabilir araç değil | ÖĞREN |
| hair-modunda-parcacik-sistemi | teknik | 1 | — | koşmadı: ürün | ÖĞREN | teknik: kurulabilir araç değil | ÖĞREN |
| blenderkit-eklentisi | plugin | 1 | GPL-2.0-or-later (eklenti kodu, doğrulanmadı; varlıklar ayrı lisanslı: Royalty Free / CC0) | koşmadı: servis | SOR | servis: koşullar · ücretsiz katman · gizlilik | ERTELE |
| origin-i-3d-cursor-a-alma | ipucu | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) | ÖĞREN |

## form_red
- yok
## Eksik alanlar
- Vngbdm2IEXM · Geometry Nodes ile küre animasyonu · karede_gorulen (kare gönderildi, karede görülen boş olamaz)
- Vngbdm2IEXM · Figma maskeli başlık sayıları · karede_gorulen (kare gönderildi, karede görülen boş olamaz)
- q1QQN08ZK6I · Solidify modifier · karede_gorulen (kare gönderildi, karede görülen boş olamaz)
## Belirsiz birleşmeler (ad benzer, repo farklı)
- yok
## ÜRETİLEBİLİR / yapım tarifleri
- emil-kowalski-skill: hedef_tur: skill tarif: Kendi skill'imizi yazabiliriz, kod gerekmez. (1) Lisansı doğrula, izin varsa doğrudan kur, yoksa yeniden yaz. (2) Kendi SKILL.md'mizi oluştur: 4 soruluk karar akışı (animasyon gerekli mi, amaç, easing, süre), varsayılan ease-out, UI'de ease-in yasağı, yalnızca transform/opacity animasyonlama, prefers-reduced-motion saygısı, Before/After tablo şablonu. (3) İsteğe bağlı 'review-animations' alt skill'i ile CSS/JS kodunda transition/animation grep denetimi ekle. Orijinal içeriği kopyalamadan kendi ifademizle yaz.
- emil-kowalski-motion-skill: hedef_tur: skill tarif: Doğrudan kurulabilir, yeniden yazmaya gerek yok. Kendi sürümümüz için: skills/ altına SKILL.md aç. İçine easing kuralları (giriş için ease-out, ekran içi hareket için ease-in-out), süre aralıkları, yalnızca transform ve opacity animasyonu, prefers-reduced-motion desteği ve bir denetim kontrol listesi yaz. Bunları Emil'in yayımlanmış yazılarından (emilkowal.ski/ui/7-practical-animation-tips) kendi cümlelerimizle özetle. Metni kopyalamadan önce lisansı kontrol et.
- google-stitch: hedef_tur: skill tarif: Stitch'in kendisi üretilemez, çünkü tasarım modeli Google'da. Ama bir skill yazılabilir. Skill, Stitch MCP'yi çağırma sırasını tarif eder: markaya uygun istem oluştur, ekranları üret, get_screen_code ile kodu çek, projenin tasarım sistemine (renk, bileşen) uydur. Repoya sabit bir DESIGN.md şablonu ekle. Anahtarı ortam değişkeninden oku.
## Kural önerileri (T0)
- 21st-dev-komutu: Siteden kopyalanan komutun Claude Code'a yapıştırılarak bileşen eklenmesi (sitenin adı altyazıda '20 21 first.dev' diye yanlış geçiyor).
- open-design: Claude Design'a açık kaynak, ücretsiz alternatif; birden fazla model ve 71 hazır tasarım sistemi destekliyor.
- dribbble-referans-gorseli: Beğenilen tasarım referans görsel olarak Stitch'e verilir.
- origin-i-3d-cursor-a-alma: Arka vertex seçilip cursor'a atanır, origin 3D cursor'a taşınır.
## OLASI EŞDEĞER (Jev p 0.5–0.75)
- yok
## OLASI TEKRAR
- emil-kowalski-skill ≈ emil-kowalski-motion-skill (adaylar/emil-kowalski-motion-skill.md)
- emil-kowalski-skill ≈ emil-kowalski-skills (adaylar/emil-kowalski-skills.md)
- emil-kowalski-motion-skill ≈ emil-kowalski-skill (adaylar/emil-kowalski-skill.md)
- emil-kowalski-motion-skill ≈ emil-kowalski-skills (adaylar/emil-kowalski-skills.md)
## Araştırılmadı
- ui-ux-pro-max-skill: kurulu 
## Site/UI teknikleri
- Tipografi, boşluk ve yerleşim düzenlemesi (Impeccable) · BK9P0rYIQY8 · 0:25 (kare) → docs/departmanlar/frontend.md
- Hareket ve easing animasyonları (Emil Kowalski skill) · 0JZtdAtJiyk · 0:30 (kare) → docs/departmanlar/frontend.md
- Boşluk (spacing) düzenlemesi, Impeccable ile · bAhPV1Sl-rg · 0:22 (kare) → docs/departmanlar/frontend.md
- Şablon galerisi kart ızgarası · O1zei0WXHvY · 0:30 (kare) → docs/departmanlar/frontend.md
- Google Stitch ile ekran üretimi · V-CIbnAAhc4 · 0:17 (kare) → docs/departmanlar/frontend.md
- Maske ile gizlenen başlık sayıları · Vngbdm2IEXM · 0:11 (kare) → docs/departmanlar/frontend.md
- Figma hero bölümü düzeni · q1QQN08ZK6I · 0:05 (altyazı) → docs/departmanlar/frontend.md
## Anatomi bekliyor
- yok
## Geliştirme önerileri
- claude-code · video: Terminale komut kopyalanarak kurulan, web sitesi üretiminde kullanılan kodlama aracı (M9qgd_KJkWc 0:00). · bizde: Çekirdek listede kendi aracımız olarak kayıtlı. · fark: Videoda yalnızca kurulum anlatılıyor; bizde zaten kurulu. Bizde olmayan daha iyi bir kullanım yok. · yok: Değişiklik yok. · kanıt: 
- impeccable · video: Tipografi, renk, boşluk ve yerleşim için 20 komutluk tasarım sistemi; /polish ile arayüz toparlanıyor (BK9P0rYIQY8 0:25, 0JZtdAtJiyk 0:38, bAhPV1Sl-rg 0:22). · bizde: Plugin kurulu: 23 komutlu tek skill (/impeccable polish, audit, critique...) ve anti-pattern tespiti. p=1.0, departman frontend. · fark: Bizdeki sürüm videodaki 20 komuttan fazla komut içeriyor. Videonun öne çıkardığı /polish bizde zaten var. Bizde olmayan daha iyi bir yan görünmüyor. · yok: Değişiklik yok. · kanıt: 
- taste-skill · video: Claude'a iyi tasarımın nasıl hissettirdiğini öğretiyor; jenerik gradient ve her yerde Inter fontunu engelliyor (BK9P0rYIQY8 0:36, 0JZtdAtJiyk 0:08, bAhPV1Sl-rg 0:32). · bizde: Plugin kurulu (brutalist, minimalist, soft, redesign, stitch vb. skiller). Ayrıca 39IlNR-P3-Q kaynaklı animasyon düzeyi kararı kaydı var (güven orta, doğrulanamadı, bayatlama 2026-12-27). · fark: Videodaki iddia (aynı font/gradient sorununu kök nedenden çözmesi) bizdeki skill kapsamına giriyor. Bizde olmayan somut bir yan yok. Kanıt yalnızca video altyazı iddiası; bizde bunun ölçülmüş bir doğrulaması yok. · yok: Değişiklik yok. Doğrulanmamış animasyon kaydı bayatlamadan önce gözden geçirilebilir; bu videodan bağımsız. · kanıt: 
## Defter
13 çağrı · $0.9017 · 198622 jeton
