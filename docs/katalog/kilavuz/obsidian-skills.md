# obsidian-skills — 7 benzersiz kayıt

**Amaç:** Obsidian kasası dosyaları: Markdown (wikilink, callout, frontmatter), Bases (.base), Canvas (.canvas), CLI ile kasa işlemleri, Defuddle ile HTML'den Markdown, Knap şablonları.

**İç yapı:** obsidian [plugin] + obsidian:<x> alt skill'leri; dosya türü başına skill (markdown, bases, json-canvas) ve araç skill'leri (cli, defuddle, knap).

## En güçlü parçalar
- `obsidian:obsidian-markdown` — Wikilink, callout, frontmatter, etiket, embed içeren .md dosyaları.
- `obsidian:obsidian-bases` — .base dosyaları ve notların tablo/veritabanı görünümleri.
- `obsidian:json-canvas` — .canvas, zihin haritası ve akış şeması.
- `obsidian:obsidian-cli` — Kasada not yönetimi, içerik arama, kasa işlemleri.
- `obsidian:defuddle` — Defuddle CLI ile HTML sayfadan temiz Markdown.

## Birlikte kullanım
- obsidian:defuddle → obsidian:obsidian-markdown: web içeriğini nota çevirmek.
- obsidian:knap ile JSON/CSV'den toplu not, ardından obsidian:obsidian-bases ile tablo görünümü.

## Tuzaklar
- defuddle ve obsidian-cli harici CLI kurulumu gerektirir.
- Kasa yolu/erişimi katalog metninde belirtilmemiş.

## Üyeler
- plugin (1): obsidian
- skill (6): obsidian:defuddle, obsidian:json-canvas, obsidian:knap, obsidian:obsidian-bases, obsidian:obsidian-cli, obsidian:obsidian-markdown
