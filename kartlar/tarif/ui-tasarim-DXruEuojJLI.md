# ui-tasarim (DXruEuojJLI)

**Amaç:** Uygulama ön yüz tasarımını otomatik olarak oluşturmak ve koda dönüştürmek.
**Araçlar:** Stitch (yapay zeka tabanlı UI tasarım aracı), Claude Code (UI tasarımını koda dönüştüren yapay zeka aracı)

**Adımlar**
1. [0:08-0:13] Stitch'e giriş yap ve uygulamayı basit bir dille açıklayarak UI tasarımını oluştur.
2. [0:13-0:23] Stitch'in oluşturduğu tasarımı inceleyip onayla.
3. [0:23-0:28] Tasarımı export et ve MCP'yi kurarak Claude Code'a entegre et.
4. [0:28-0:32] Claude Code'a export edilen tasarım kodunu terminalde yapıştır.
5. [0:34-0:43] Son prompt'u kullanarak tasarımı yayına hazır koda dönüştür.

**Prompt/kod/ayar:** claude mcp addstitch --transport=http --url`https://stitch.googleapis.com/mcp` --header"X-Goog-Api-Key:REDACTED"
**Sonuç:** Tasarımın koda otomatik dönüşümü ve yayına hazır hale getirilmesi.
**Bizde (öneri, modelden):** Stitch ve Claude Code gibi araçlarla UI tasarımını otomatikleştirmek için kurulu araçları kullanarak benzer bir entegrasyon yapabilirsiniz.
**Daha iyi (öneri):** Kullanılan yapay zeka araçlarının API entegrasyonlarını daha esnek hale getirmek ve daha fazla özelleştirme imkanı sunmak.
