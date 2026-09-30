# Obsidian skill
ad: Obsidian skill
tur: skill
video: PWRWO749oro
repo: kepano/obsidian-skills
lisans: MIT (arama sonuçlarına göre; LICENSE dosyası repoda var, içeriği doğrudan okunmadı)
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/kepano/obsidian-skills
telemetri: Repoda telemetri koduna rastlanmadı; yalnızca markdown talimatları var. defuddle/knap/Obsidian CLI'nin kendi telemetrisi doğrulanmadı (bilinmiyor).
yildiz: bilinmiyor (bir arama sonucu 40.000+ diyor, doğrulanmadı)
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-10-01-uzun)
## Ne
Obsidian vault'unda çalışan ajana Obsidian dosya türlerini (.md, .base, .canvas), Obsidian CLI'yi ve web sayfasından temiz markdown çıkarmayı öğreten Agent Skills koleksiyonu. Adayda repo belirtilmemişti; video yalnızca "ikinci beyin" diyor. Eşleştirme arama sonucuna dayanıyor, kesin değil. Alternatif olası aday: AgriciDaniel/claude-obsidian (kalıcı wiki/ikinci beyin).
## Mekanizma
Saf talimat dosyaları: skills/ altında 6 skill (obsidian-markdown, obsidian-bases, json-canvas, obsidian-cli, defuddle, knap), her biri SKILL.md. Ajan görev eşleşince ilgili SKILL.md'yi yükler ve sözdizimi kurallarına (wikilink, frontmatter, Bases, Canvas JSON) uyarak dosya üretir. defuddle ve knap dış araçları çağırır. .claude-plugin ile marketplace paketi olarak da dağıtılır.
## Kanıt
- Notları, kararları, proje geçmişini ve kod kalıplarını kalıcı bir bilgi sistemine bağlayan ikinci beyin yaklaşımı → sınanamadı · Video sayfası yalnızca başlık verdi (Top 5 Claude Code Plugins), transkript alınamadı. kepano/obsidian-skills README'si yalnızca dosya biçimi ve CLI skill'lerini listeliyor, kalıcı bellek özelliği yok.
- defuddle web sayfasından temiz markdown çıkarıp token tasarrufu sağlar → sınanamadı · README'de yazıyor; ölçüm yapılmadı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- /plugin marketplace add kepano/obsidian-skills
- /plugin install obsidian@obsidian-skills
- Alternatif: npx skills add https://github.com/kepano/obsidian-skills
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Ajanın Obsidian dosyalarını bozmadan doğru sözdizimiyle üretmesini sağlar. Videodaki "ikinci beyin" iddiasını (kararlar, proje geçmişi, kod kalıpları) tek başına karşılamaz; kalıcı bellek mantığı içermez, yalnızca format/araç bilgisi verir.
## Maliyet/risk
Düşük: talimat dosyaları. Skill'ler ajanın vault'a yazmasına ve CLI/harici komut çalıştırmasına yol açar; vault yedeği önerilir. Aday kimliği belirsiz, yanlış repo olabilir. SKILL.md içerikleri tek tek incelenmedi.
## Tasarruf
Doğrudan token aracı değil. Tek istisna defuddle: web sayfasındaki gürültüyü atıp temiz markdown verir, README "token tasarrufu" diyor; ölçülmedi.
## Üretilebilir
hedef_tur: skill
tarif: Zaten skill; kopyalamaya gerek yok. Videodaki ikinci beyin için ayrı bir skill yazılabilir: proje kararlarını ve kod kalıplarını vault'taki klasörlere (decisions/, patterns/) frontmatter'lı notlar olarak kaydeden, oturum başında ilgili notları okuyan bir SKILL.md; biçim için obsidian-markdown skill'ine dayanır.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-10-01-uzun/panel.md → Ömer sütunu
## Özellikler
### obsidian-markdown: wikilink, embed, callout, properties içeren Obsidian Flavored Markdown üretimi
kaynak: https://github.com/kepano/obsidian-skills
### obsidian-bases: .base dosyaları (view, filtre, formül, özet)
kaynak: https://github.com/kepano/obsidian-skills
### json-canvas: .canvas dosyaları (node, edge, grup)
kaynak: https://github.com/kepano/obsidian-skills
### obsidian-cli: Obsidian CLI ile vault ve eklenti/tema geliştirme
kaynak: https://github.com/kepano/obsidian-skills
### defuddle: web sayfasından temiz markdown çıkarma
kaynak: https://github.com/kepano/obsidian-skills
### knap: JSON/CSV verisinden Markdown şablon render, toplu dosya üretimi
kaynak: https://github.com/kepano/obsidian-skills
## Destek
- PWRWO749oro · 1:03 · Notları, kararları, proje geçmişini ve kod kalıplarını kalıcı bir bilgi sistemine bağlayan ikinci beyin yaklaşımı. · kanıt: Think of this as a structured second brain for your entire workflow.
