# excalidraw-visuals skill
ad: excalidraw-visuals skill
tur: skill
video: zKBPwDpBfhs
repo: robonuggets/excalidraw-skill
lisans: MIT
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/robonuggets/excalidraw-skill
telemetri: README'de telemetri belirtilmiyor. Her şey yerelde (localhost canvas) çalışıyor. MCP sunucusunun kodu incelenmedi, bu yüzden telemetri yok diyemem: bilinmiyor.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-5)
## Ne
Claude Code için Excalidraw diyagram skill'i: metin tarifini canlı Excalidraw tuvalinde diyagrama çevirir (mimari, akış şeması, karşılaştırma). Videoda (zKBPwDpBfhs, "Master 95% of Claude Code Skills") AI görsellerinde yazımların bozulabildiği, bu yüzden diyagram skill'inin tamamlayıcı olarak kullanıldığı söyleniyor. Not: Video sayfası çekilince yalnız başlık geldi, transkript alınamadı. Aday repo ise web aramasıyla "excalidraw-visuals" adına en yakın eşleşme olarak bulundu ve videodaki skill'le aynı olduğu doğrulanmadı.
## Mekanizma
SKILL.md, ajana 10 görsel teknik ve yerleşim kuralları verir. Teknikler: katmanlı glow, renk bölgeleri, bağlı oklar, çizgi stili anlamları, karar elmasları, yazı hiyerarşisi, anlamsal renk paleti, Mermaid dönüşümü ve ekran görüntüsü döngüsü. Çizimi yapan yer yctimlin/mcp_excalidraw MCP sunucusu ve yerel canvas'tır (localhost:3000). Ajan öğeleri MCP üzerinden oluşturur, tuvalin ekran görüntüsünü alır, taşma, çakışma ve kötü okları görürse düzeltir. Sonra PNG, SVG, .excalidraw veya paylaşım URL'si olarak dışa aktarır. Metin AI görüntü modeliyle değil vektör öğe olarak yazıldığı için yazım bozulması olmaz (bu çıkarım benim, sınanmadı).
## Kanıt
- AI görsellerinde kelimeler yanlış yazılabiliyor; diyagram skill'i bunu tamamlıyor (video) → sınanamadı · Video sayfasından transkript gelmedi, yalnız başlık alındı. İddia adayın bulgu notundan alındı. Repo README'si yazım sorunundan söz etmiyor.
- Skill, ajanın kendi tuvalini ekran görüntüsüyle görüp düzelttiği bir döngü içeriyor → doğrulandı · robonuggets/excalidraw-skill README'si: 'Screenshot Loop: Agent sees and fixes its own work'. Bunu kodu çalıştırarak değil, README'yi okuyarak doğruladım.
- Repo videodaki 'excalidraw-visuals' skill'i ile aynı → sınanamadı · Adı 'excalidraw-visuals' olan bir repo bulunamadı. robonuggets/excalidraw-skill en yakın eşleşme ama bağlantı kanıtlanamadı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- git clone https://github.com/yctimlin/mcp_excalidraw && cd mcp_excalidraw && npm ci && npm run build
- claude mcp add excalidraw -s user -e EXPRESS_SERVER_URL=http://localhost:3000 -- node /mutlak/yol/mcp_excalidraw/dist/index.js
- mcp_excalidraw klasöründe: PORT=3000 npm run canvas (tarayıcıda http://localhost:3000 açılır)
- claude skill add --url https://raw.githubusercontent.com/robonuggets/excalidraw-skill/main/.claude/skills/excalidraw/SKILL.md
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Doğru yazımlı, düzenlenebilir (.excalidraw) diyagramlar üretir. Ekran görüntüsü döngüsü elle düzeltme ihtiyacını azaltır. Tutarlı renk ve yazı hiyerarşisi sağlar. AI resim modelinin yazım hatası sorununu ortadan kaldırır.
## Maliyet/risk
Kurulum için ayrı bir Node MCP sunucusu ve çalışan canvas gerekir (klonla, derle, servisi başlat). Üçüncü taraf kod çalıştırılır. Görsel ve freedraw MCP ile eklenemiyor. Ekran görüntüsü döngüsü token ve süre harcar. Videodaki skill'le eşleşme kesin değil. Yıldız ve son commit değerleri çekilemedi.
## Tasarruf
Token aracı değil. Tasarruf iddiası yok.
## Üretilebilir
hedef_tur: skill
tarif: Kendi SKILL.md'mizi yazarız: (1) yazı hiyerarşisi (28/20/16/14 px), anlamsal renk paleti, boşluk ve ok yönlendirme kuralları; (2) her çizimden sonra ekran görüntüsü alıp taşma ve çakışma kontrol listesiyle düzelt döngüsü; (3) çizim için mevcut yctimlin/mcp_excalidraw MCP'sini kullan (MIT lisanslı olduğu README'ye göre doğrulanmadı, ayrıca bakılmalı) ya da doğrudan .excalidraw JSON üretip dışa aktar. MCP gerektirmeyen sürüm için ajan .excalidraw JSON yazar ve excalidraw CLI veya tarayıcıyla PNG'ye çevrilir.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-5/panel.md → Ömer sütunu
## Özellikler
### 10 görsel teknik: glow, renk bölgeleri, bağlı oklar, çizgi stili anlamı, karar elması, karma şekiller, yazı hiyerarşisi, anlamsal renkler, Mermaid dönüşümü, ekran görüntüsü döngüsü
kaynak: https://github.com/robonuggets/excalidraw-skill
### Kalite kontrol listesi: taşma, çakışma ve kötü okları dışa aktarmadan önce yakalar
kaynak: https://github.com/robonuggets/excalidraw-skill
### PNG, SVG, .excalidraw ve paylaşım URL'si olarak dışa aktarma
kaynak: https://github.com/robonuggets/excalidraw-skill
### Canlı canvas ve ajan araçlarıyla çizim yapan MCP sunucusu (skill'in bağımlılığı)
kaynak: https://github.com/yctimlin/mcp_excalidraw
## Destek
- zKBPwDpBfhs · 2:41 · AI ile görsel üretir ama yazımlar bozuk çıkabilir; diyagram skill'i ile tamamlanır. · kanıt: Excalibraw visuals skill; AI görsellerinde kelimeler yanlış yazılabiliyor.
