# excalidraw-diagram skill
ad: excalidraw-diagram skill
tur: skill
video: zKBPwDpBfhs
repo: coleam00/excalidraw-diagram-skill
lisans: yok
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/coleam00/excalidraw-diagram-skill
telemetri: Skill kendi içinde telemetri kodu içermiyor görünüyor (dosya ağacında yalnızca markdown, şablon, Python render betiği ve pyproject var); render yerel Chromium ile yapılıyor. Render şablonunun Excalidraw kütüphanesini CDN'den çekip çekmediği doğrulanmadı: bilinmiyor.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-5)
## Ne
Kodlama ajanına (Claude Code, OpenCode vb.) doğal dil tarifinden düzenlenebilir Excalidraw diyagramı (.excalidraw native JSON) üretme yeteneği veren skill. Amaç sadece kutu-ok değil, kavramı görsel olarak 'savunan' diyagramlar üretmek.
## Mekanizma
SKILL.md tasarım metodolojisi ve iş akışını tanımlar (Workflow: Step 1 kavramı anla → kavram-şekil eşleme → yerleşim → JSON üretimi → render → görsel doğrulama). Ajan Excalidraw JSON'unu doğrudan yazar (references/json-schema.md ve element-templates.md şablonlarıyla), bu yüzden metinler hatasız ve dosya düzenlenebilir çıkar. Render hattı: render_excalidraw.py + render_template.html Playwright (Chromium) ile .excalidraw dosyasını PNG'ye çevirir; ajan çıktıyı görüp çakışan metin, hizasız ok, dengesiz boşluk gibi sorunları döngüyle düzeltir. Renkler tek dosyada (references/color-palette.md) olduğundan marka paleti değiştirilebilir. Fan-out, zaman çizgisi, yakınsama gibi yapısal desenler ve gerçek kod/JSON kanıt parçaları önerilir.
## Kanıt
- Düzenlenebilir Excalidraw diyagramı (native JSON) üretir. → doğrulandı · README: 'generates ... Excalidraw diagrams'; dosya ağacında references/json-schema.md ve element-templates.md (Excalidraw JSON formatı) var.
- Kelimeler hep doğru çıkar. → sınanamadı · JSON doğrudan yazıldığı için metin bozulması beklenmez ve render ile doğrulama hattı var; ancak 'hep' iddiası çalıştırılarak sınanmadı.
- SKILL.md içinde name: excalidraw-diagram, Workflow ve Step 1: Understand the concept var. → sınanamadı · SKILL.md dosyası mevcut (ağaçta), ancak içeriği okunamadı; video kare bulgusu ve README iş akışı tarifiyle tutarlı. Kurulum dizini adı excalidraw-diagram.
- Ajan kendi çıktısını görüp düzeltir (görsel doğrulama). → doğrulandı · README: Playwright tabanlı render hattı; render_excalidraw.py ve render_template.html dosyaları ağaçta.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- git clone https://github.com/coleam00/excalidraw-diagram-skill.git
- cp -r excalidraw-diagram-skill .claude/skills/excalidraw-diagram
- cd .claude/skills/excalidraw-diagram/references && uv sync
- uv run playwright install chromium (render/doğrulama hattı için; isteğe bağlı ama önerilir)
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Düzenlenebilir, doğru yazımlı mimari/akış diyagramları; görsel öz-doğrulama ile daha az elle düzeltme; tek dosyadan marka renk özelleştirmesi; mevcut .claude/skills yapısına doğrudan uyum.
## Maliyet/risk
Lisans dosyası depo ağacında görünmüyor (lisans belirsiz/yok) → yeniden dağıtım ve türetme hukuken belirsiz. Kurulum Playwright + Chromium indirir (disk, ağ); Python/uv gerekir. Skill ajana kabuk komutu çalıştırtıyor (uv sync, playwright install). Çok sayıda fork var, kaynak güvenilirliği için orijinal repo tercih edilmeli. Yıldız/commit tarihi doğrulanamadı.
## Tasarruf
Token aracı değil; tasarruf mekanizması yok. Aksine render-düzeltme döngüsü ek token harcar.
## Üretilebilir
hedef_tur: skill
tarif: Lisans belirsiz olduğundan kopyalamak yerine kendi skill'imizi yaz: skills/excalidraw-diagram/SKILL.md (front matter name/description; iş akışı: kavramı anla → şekil eşleme → yerleşim → JSON yaz → render → doğrula). references/ altında Excalidraw JSON şema özeti, element şablonları ve renk paleti dosyası olsun. Render için küçük bir Python+Playwright betiği (.excalidraw → PNG, @excalidraw/excalidraw ile yerel HTML) ekle; ajan PNG'yi okuyup çakışma/hizasızlık kontrol etsin. Paleti tek dosyada tut.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-5/panel.md → Ömer sütunu
## Özellikler
### Kavramı yansıtan yerleşim (fan-out, zaman çizgisi, yakınsama); tek tip kart ızgarası yok
kaynak: https://github.com/coleam00/excalidraw-diagram-skill
### Kanıt öğeleri: gerçek kod parçaları ve JSON payload'ları diyagramda
kaynak: https://github.com/coleam00/excalidraw-diagram-skill
### Playwright ile PNG render edip görsel doğrulama ve düzeltme döngüsü
kaynak: https://github.com/coleam00/excalidraw-diagram-skill
### Tek dosyadan (color-palette.md) marka renk özelleştirme
kaynak: https://github.com/coleam00/excalidraw-diagram-skill
### Claude Code ve OpenCode dahil .claude/skills okuyan ajanlarla uyumlu
kaynak: https://github.com/coleam00/excalidraw-diagram-skill
## Destek
- zKBPwDpBfhs · 6:35 · Düzenlenebilir Excalidraw diyagramı (native JSON) üretir; kelimeler hep doğru çıkar. · kanıt: SKILL.md: name excalidraw-diagram, Workflow, Step 1 Understand the concept. (karede: SKILL.md front matter'ında name: excalidraw-diagram ve description; altında '## Workflow' ve '### Step 1: Understand the concept'.)
