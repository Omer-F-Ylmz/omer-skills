# prompt-hilesi (DXb0NNTj8g1)

**Amaç:** Claude'a canlı web tarama yeteneği kazandırmak
**Araçlar:** Tinyfish (MCP entegrasyonu), Claude custom connector, Tinyfish Search API, Tinyfish Fetch API, Tinyfish Browser API

**Adımlar**
1. [0:13-0:21] Claude ayarlarında 'connectors' sekmesine gir, yeni bir custom connector ekle ve Tinyfish MCP URL'sini yapıştır.
2. [0:21-0:24] Connector'ı ekle ve Tinyfish'e yönlendirilen sayfada giriş yaparak entegrasyonu tamamla.
3. [0:24-0:28] Claude'a canlı web verilerini işlemesi için prompt ver (örn: 'Amazon'da $1000 altındaki en iyi laptopları araştır ve özetle').
4. [0:30-0:33] Tinyfish'in canlı tarama ve veri analizi sonucu, Claude'a yapısal bir çıktı döndürülür.

**Prompt/kod/ayar:** Claude'a Tinyfish MCP URL'si ve custom connector adı ile entegrasyon yapıldıktan sonra, 'go to [URL] and [action]' formatında prompt verilir.
**Sonuç:** Claude, Tinyfish'in web tarama ve veri işleme yetenekleriyle desteklenerek canlı verilerden mantıksal özetler üretebilir.
**Bizde (öneri, modelden):** kurulu araçlarla nasıl yapılır: Claude'a Tinyfish gibi bir entegrasyon aracı kurularak MCP protokolü üzerinden web tarama yeteneği sağlanır. Ardından, Claude'a yapısal prompt'lar vererek canlı verilerden analizler elde edilir.
**Daha iyi (öneri):** Tinyfish'in API'leri doğrudan kod içinde kullanılabilir, böylece web işlemleri tamamen otomatikleştirilebilir.
