# Meng To Skills (Awards quality sites)
ad: Meng To Skills (Awards quality sites)
tur: skill
video: Ysr7oNDajJI
repo: mengto/skills
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/mengto/skills
telemetri: Kanıt yok: README'de telemetri belirtilmiyor. Skill'ler düz Markdown. Betikleri (scripts/*.mjs) ve skill'lerin harici servis çağrılarını (Aura asset, Unsplash) incelemedim. Ağ erişimi olabilir, bilinmiyor.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı: SkillSpector raporu yok
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun)
## Ne
Meng To'nun (Aura Build) derlediği taşınabilir agent skill koleksiyonu: web tasarımı, 3D (Three.js), oyun geliştirme, medya ve iş akışı klasörleri. Öne çıkanlar: Video to Super Prompt, HTML to Interaction Prompts, Stitched Full Page Capture, Daily UI Inspiration. Videoda Awards seviyesi site ilkeleri, efektler ve scroll tabanlı hikaye anlatımı işleniyor.
## Mekanizma
Kod çalıştıran bir araç değil; klasör tabanlı SKILL.md oyun kitapları (isteğe bağlı references, ARTICLE.md, script, asset). Ajan ilgili SKILL.md'yi okuyup adımları, varsayılanları ve tuzakları izler. Codex, Claude Code (CLAUDE.md'den referans ya da skills klasörüne kopya), Cursor ve diğer ajanlarda kullanılabilir. Depoda ayrıca demo/ekran görüntüsü galerisi üreten ve doğrulayan yardımcı Node betikleri (scripts/*.mjs) var. Bu betikleri okumadım.
## Kanıt
- Video: Awards seviyesi site ilkeleri, efektler ve scroll tabanlı hikaye anlatımı içeriyor → sınanamadı · video getir yalnızca başlığı döndürdü (Insane Claude Design Skills You Need To Actually Build Beautiful Sites). Döküm alınamadı.
- Video to Super Prompt skill'i depoda var → doğrulandı · README, agent-skills/codex/video-to-superprompt/SKILL.md bağlantısını listeliyor.
- Depo Codex, Claude, Cursor ile taşınabilir skill klasörleri sunuyor → doğrulandı · README'deki 'Agent support' bölümü.
- Fable 5 tek seferde HTML üretiyor → sınanamadı · Yalnızca README'de iddia olarak geçiyor, denenmedi.
- güvenlik ön taraması: koşmadı: SkillSpector raporu yok
## Kurulum
- git clone https://github.com/mengto/skills
- İstediğin skill klasörünü (ör. agent-skills/codex/video-to-superprompt) ~/.claude/skills/ altına kopyala
- Ya da CLAUDE.md içinden ilgili SKILL.md'ye referans ver
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Tasarım yönünü ve efekt/scroll anlatımı ilkelerini tekrar kullanılabilir dosyalara çevirir. Video, referans ya da HTML'den ayrıntılı prompt üretir. Site inşa sürecinde tutarlılık sağlar.
## Maliyet/risk
Lisans türü doğrulanamadı: LICENSE dosyası var ama içeriğine bakmadım. Skill içeriği ve scriptleri çalıştırmadan önce gözden geçirilmeli. Bazı skill'ler Aura Build gibi ticari servislere yönlendiriyor olabilir. Awards seviyesi skill'in kendisini görmedim: ağaçta agent-skills/web-design var ama içeriği kesildi. Video sayfası da yalnızca başlık verdi, dökümü alınamadı.
## Üretilebilir
hedef_tur: skill
tarif: Kendi 'awards-site-principles' skill'imizi yaz: SKILL.md içinde ne zaman kullanılacağı (landing page, scroll hikayesi), varsayılanlar (tipografi, boşluk, hareket zamanlaması, scroll tetikli bölüm geçişleri, GSAP/ScrollTrigger ya da CSS scroll-timeline) ve tuzaklar (performans, reduced-motion, mobil) yer alsın. references/ altında efekt tarifleri (parallax, pin, mask reveal) tut. Depodaki web-design skill'lerini okuyup fikirleri kendi sözlerimizle yeniden yaz, kopyalama. Önce lisansı doğrula.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun/panel.md → Ömer sütunu
## Özellikler
### Video to Super Prompt: ekran kaydından ayrıntılı prompt üretir
kaynak: https://github.com/mengto/skills
### HTML to Interaction Prompts: mevcut HTML'den bölüm, animasyon, hover ya da WebGL efekti için prompt çıkarır
kaynak: https://github.com/mengto/skills
### Stitched Full Page Capture: sayfanın tamamını referans olarak yakalar
kaynak: https://github.com/mengto/skills
### Daily UI Inspiration: gezinme, yakalama ve prompt paketi üretimi döngüsü
kaynak: https://github.com/mengto/skills
### 3D skill'leri: su, gökyüzü ışınları, yaprak, mevsimler, Retina çözünürlük
kaynak: https://github.com/mengto/skills
### Oyun geliştirme skill'leri: izometrik ARPG, düşman sistemleri, oyun testi
kaynak: https://github.com/mengto/skills
## Destek
- Ysr7oNDajJI · 7:27 · Awards seviyesi site ilkeleri ve efektleri; scroll tabanlı hikaye anlatımı. Video to super prompt da içinde. · kanıt: Awards quality sites
