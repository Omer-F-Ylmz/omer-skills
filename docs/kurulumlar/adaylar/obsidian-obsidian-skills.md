# Obsidian + Obsidian skills
ad: Obsidian + Obsidian skills
tur: skill
video: V2RIVnGCy74
repo: kepano/obsidian-skills
lisans: bilinmiyor (repoda LICENSE dosyası var ama türü okunamadı)
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/kepano/obsidian-skills
telemetri: Repoda telemetri yok; skill'ler yalnızca Markdown talimat dosyaları. Ön taramada SKILL dosyalarının tamamı okunmadı. defuddle ve obsidian-cli gibi harici araçların kendi davranışı ayrıca doğrulanmadı.
yildiz: bilinmiyor
alt_tur: araç
skillspector: SkillSpector --no-llm: HIGH/CRITICAL bulgu 0 (LLM'siz tarama)
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-5)
## Ne
Obsidian (Markdown tabanlı not uygulaması) kasalarıyla çalışan ajanlar için Agent Skills standardına uygun 6 skill paketi: obsidian-markdown, obsidian-bases, json-canvas, obsidian-cli, defuddle, knap. Claude Code, Codex ve OpenCode ile kullanılabilir.
## Mekanizma
Her skill, skills/<ad>/SKILL.md dosyasıdır. Ajan, görev ilgili olduğunda skill'i yükler ve içindeki talimatlarla Obsidian'a özgü biçimleri doğru üretir. obsidian-markdown: wikilink, gömme, callout ve özellik (properties) sözdizimi. obsidian-bases: .base dosyaları (görünüm, filtre, formül, özet). json-canvas: .canvas dosyaları (düğüm, kenar, grup). obsidian-cli: Obsidian CLI ile kasayı yönetme, eklenti/tema geliştirme. defuddle: web sayfasından temiz markdown çıkarır, gürültüyü atarak token tasarrufu sağlar. knap: JSON/CSV verisinden Markdown şablonu üretir, toplu dosya oluşturabilir. Kasa klasörü Claude Code'un çalışma dizini olduğunda klasörler ve bağlantılar ajana bilgi grafiği/hafıza gibi hizmet eder. Bu, videonun yorumu; repo kendisi hafıza mekanizması sunmaz.
## Kanıt
- Repo Obsidian'ın kurucusu tarafından oluşturuldu. → sınanamadı · Repo sahibi kepano; README'de obsidianmd/knap ve kepano/defuddle bağlantıları var. Sahibin Obsidian kurucusu olduğuna dair kanıt bu çıktıda yok.
- Vault klasörleriyle Claude Code'a bilgi grafiği/hafıza sağlar. → sınanamadı · README skill'lerin biçim ve araç bilgisi verdiğini söylüyor, hafıza özelliğinden söz etmiyor. Hafıza etkisi kasayı çalışma dizini yapmaktan geliyor ve sınanmadı.
- Skills reposu en iyi uygulamaları öğretir. → sınanamadı · SKILL.md içerikleri okunmadı, yalnızca README tablosu görüldü. README'ye göre skill'ler Obsidian biçimlerini ve araçlarını anlatıyor.
- güvenlik ön taraması: SkillSpector --no-llm HIGH/CRITICAL 0
## Kurulum
- /plugin marketplace add kepano/obsidian-skills
- /plugin install obsidian@obsidian-skills
- Alternatif: npx skills add https://github.com/kepano/obsidian-skills
- Elle: repo içeriğini kasa kökündeki .claude klasörüne kopyala (Claude Code); Codex için skills/ dizinini ~/.codex/skills'e kopyala
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Ajan, Obsidian'a özgü biçimleri (wikilink, callout, Bases, Canvas) sözdizimi hatası yapmadan üretir. Kasa, ajan için kalıcı not/hafıza deposu olarak kullanılabilir. Web sayfalarını temiz markdown olarak kasaya almak kolaylaşır.
## Maliyet/risk
Düşük. SkillSpector --no-llm taramasında HIGH/CRITICAL bulgu 0. Yine de obsidian-cli ve defuddle harici araç çalıştırır. Ajan kasadaki notları okuyup yazabilir, bu yüzden kasanın yedeği önemli. Lisans türü doğrulanmadı.
## Tasarruf
Tasarruf ana amaç değil. Tek istisna defuddle: web sayfasındaki gereksiz öğeleri çıkarıp temiz markdown verir, böylece bağlama giren token azalır. Oran ölçülmedi.
## Üretilebilir
hedef_tur: skill
tarif: Zaten skill formatında, doğrudan kurulabilir. Kendi sürümümüz için: skills/<ad>/SKILL.md yapısıyla, bizim kasa düzenimize özel (klasör adları, frontmatter alanları, wikilink kuralları) kısa bir obsidian-vault skill'i yazılabilir. defuddle benzeri temiz markdown çıkarma için ayrı bir CLI sarmalayıcı skill eklenebilir.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-5/panel.md → Ömer sütunu
## Özellikler
### obsidian-markdown: wikilink, gömme, callout ve properties dahil Obsidian Flavored Markdown üretimi/düzenleme
kaynak: https://github.com/kepano/obsidian-skills
### obsidian-bases: .base dosyaları için görünüm, filtre, formül ve özet
kaynak: https://github.com/kepano/obsidian-skills
### json-canvas: .canvas dosyaları için düğüm, kenar ve grup
kaynak: https://github.com/kepano/obsidian-skills
### obsidian-cli: Obsidian CLI ile kasa etkileşimi, eklenti ve tema geliştirme
kaynak: https://github.com/kepano/obsidian-skills
### defuddle: web sayfasından temiz markdown çıkarma (token tasarrufu)
kaynak: https://github.com/kepano/obsidian-skills
### knap: JSON/CSV verisinden Markdown şablonu ve toplu dosya üretimi
kaynak: https://github.com/kepano/obsidian-skills
### Agent Skills standardı: Claude Code, Codex, OpenCode ile uyumlu; marketplace ve npx skills ile kurulum
kaynak: https://github.com/kepano/obsidian-skills
## Destek
- V2RIVnGCy74 · 15:10 · Vault klasörleriyle Claude Code'a bilgi grafiği/hafıza sağlar; Obsidian kurucusunun skills reposu en iyi uygulamaları öğretir. · kanıt: Repo Obsidian'ın kurucusu tarafından oluşturuldu. (karede: İlgili kare yok; altyazıdan.)
