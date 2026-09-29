# Graphify
ad: Graphify
tur: CLI
video: oHKt0FUbR58
repo: graphify-labs/graphify
lisans: Apache-2.0 (README rozeti; depoda ayrıca LICENSE-MIT dosyası var, bir web sonucu MIT diyor. Çift lisans olabilir, doğrulanmadı)
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/Graphify-Labs/graphify
telemetri: Kod ayrıştırma tamamen yerel, kod makineden çıkmaz (README beyanı). Yalnızca doküman/medya için anlamsal geçişte yapılandırılan LLM backend'ine çağrı gider. Ayrı bir telemetri/analitik toplaması kodda doğrulanmadı, bilinmiyor. Ücretli bulut platformu (app.graphify.com) ayrı ve isteğe bağlı.
yildiz: bilinmiyor
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-29-short)
## Ne
Kod tabanını, dokümanları, SQL şemalarını, PDF/görsel/videoyu bilgi grafiğine (graph.json, graph.html, GRAPH_REPORT.md) çeviren Python CLI'ı. Claude Code, Cursor, Codex, Gemini CLI gibi 15'ten fazla asistana /graphify skill'i olarak kurulur. Y Combinator S26 şirketi Graphify Labs'ın ürünüdür.
## Mekanizma
Kod tree-sitter AST ile yerelde, LLM kullanmadan ve deterministik olarak ayrıştırılır (~40 dil). calls/imports/inherits gibi dosyalar arası bağlar çözülür. Graf üzerinde Leiden ile topluluk çıkarılır, en çok bağlı 'god node'lar belirlenir. Her kenar EXTRACTED (kaynakta açık) ya da INFERRED (çözümlenmiş) diye etiketlenir. Vektör deposu ve embedding yoktur. Doküman, PDF, görsel ve video için asistanın modeli ya da yapılandırılmış bir API anahtarıyla anlamsal geçiş yapılır. Sorgulama `graphify query`, `graphify path A B` ve `graphify explain` komutlarıyla graph.json üzerinden yapılır. Claude Code'da 'strict mode' var: oturumdaki ilk ham kaynak okumasını engelleyip grafiğe yönlendirir. Ayrıca hooks, MCP ingest ve pre-commit desteği var.
## Kanıt
- Kod bir kez okunup bilgi grafiğine çevrilir, Claude her oturumda baştan okumaz → doğrulandı · README: /graphify projeyi graph.json'a çıkarır, dosyaları grep'lemek yerine sorgulanır (graphify query/path/explain).
- Araç ücretsiz → doğrulandı · README: kod haritalama ücretsiz ve tamamen yerel. Ücretli bulut platformu ayrı.
- 70 kata kadar token tasarrufu → sınanamadı · Yalnızca MindStudio blogunda geçiyor. Kendi ölçümüm yok, BENCHMARKS.md incelenmedi.
- Kod hiçbir LLM'e gitmez → doğrulandı · README: tree-sitter AST, LLM yok, makineden çıkmaz. Kaynak kodu denetlenmedi, beyana dayanıyor.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- uv tool install graphifyy (veya: pipx install graphifyy)
- graphify install
- Asistanda: /graphify .
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Büyük kod tabanlarında yeniden keşif maliyetini ve token tüketimini azaltır, mimariyi (god node, topluluk, yol) görünür kılar. Kod kısmı ücretsiz ve yerel. Ek olarak docs/PDF/video de aynı grafa girer.
## Maliyet/risk
Orta-düşük. Doküman/medya semantik geçişi verileri LLM sağlayıcısına gönderir. `graphify install` asistan yapılandırmasına skill/hook yazar. Strict mode ham dosya okumasını engelleyerek beklenmedik davranışa yol açabilir. Lisans belirsizliği (Apache-2.0 vs MIT). Proje ticari bulut ürününe yönleniyor. Paket adı 'graphifyy' (çift y), yazım hatası kaynaklı sahte paket riski var. Yıldız ve commit tarihi doğrulanmadı.
## Tasarruf
Claude her oturumda dosyaları baştan okumak yerine graph.json üzerinde query/path/explain ile gezinir, yalnızca ilgili alt grafiği bağlama alır. Üçüncü taraf bir blog 500+ dosyalı projelerde 70 kata kadar token düşüşü iddia ediyor. Depoda BENCHMARKS.md var ama rakamlar doğrulanmadı.
## Üretilebilir
hedef_tur: CLI
tarif: Graphify zaten kurulabilir bir CLI+skill olduğundan kopyalamak yerine doğrudan kullanmak daha mantıklı. Hafif bir sürüm için: Python CLI yaz, tree-sitter ile dosyalardan sembol, import ve call kenarlarını çıkar, networkx ile graph.json üret, query/path/explain alt komutları ekle. Ardından bir SKILL.md ile Claude'a 'önce graph.json'ı sorgula' talimatı ver ve isteğe bağlı bir PreToolUse hook'u ile ilk ham Read'i grafiğe yönlendir.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-29-short/panel.md → Ömer sütunu
## Özellikler
### tree-sitter ile yerel, deterministik AST çıkarımı (~40 dil), LLM'siz
kaynak: https://github.com/Graphify-Labs/graphify
### Kenar güvenilirlik etiketleri EXTRACTED/INFERRED
kaynak: https://github.com/Graphify-Labs/graphify
### query, path, explain komutları ile graph.json sorgulama
kaynak: https://github.com/Graphify-Labs/graphify
### God node ve Leiden topluluk analizi, GRAPH_REPORT.md
kaynak: https://github.com/Graphify-Labs/graphify
### Claude Code strict mode: ilk ham okumayı grafiğe yönlendirir
kaynak: https://www.mindstudio.ai/blog/graphify-claude-code-knowledge-graph-large-codebase-70x
### Doküman, PDF, görsel, video/audio aynı grafa girer
kaynak: https://github.com/Graphify-Labs/graphify
### Kod haritasıyla (graph.json) grep gidiş-gelişlerini azaltıp token ve zaman tasarrufu
video: g89FJiNAlEs · iddia: Graphify kod haritasıyla grep gidiş-gelişlerini azaltıp token ve zaman tasarrufu sağlıyor.
sonuc: sınanamadı
arastirma: Mekanizma README'de doğrulandı: /graphify projeyi (kod, doküman, PDF, görsel, video) graph.json, graph.html ve GRAPH_REPORT.md dosyalarına çevirir. README'nin ilk cümlesi bunu "dosyaları grep'lemek yerine sorgulayabileceğin bilgi grafiği" diye anlatır. Kod tree-sitter AST ile yerelde ayrıştırılır (LLM yok, deterministik, ~40 dil). calls/imports/inherits bağları dosyalar arası çözülür. Sorgulama graph.json üzerinden `graphify query "<soru>"` (kapsamlı alt graf), `graphify path A B` (en kısa yol) ve `graphify explain X` (bağlantılar) ile yapılır. README'deki FastAPI örneği: `path FastAPI ModelField` 3 sıçramada sonuç veriyor. Her kenar EXTRACTED ya da INFERRED etiketi taşır. Vektör deposu ve embedding yoktur. Grafik bir kez üretilir, sonra dosyalar yeniden okunmadan sorgulanır. Bu yüzden grep/oku döngüsü azalır. Bu, iddianın mekanizma kısmını destekler. Sayısal token ve zaman tasarrufu doğrulanmadı. README'nin gösterdiği bölümde ölçüm yok. Depoda BENCHMARKS.md ve graphify/benchmark.py var ama içeriklerini incelemedim. "70 kata kadar" rakamı yalnızca üçüncü taraf MindStudio blogunda geçiyor. Videodaki iddia da anlatıcının beyanı, ölçüm yok. Zaman tasarrufu için kanıt bulamadım, bilinmiyor.
kaynak: https://github.com/Graphify-Labs/graphify
## Destek
- oHKt0FUbR58 · 0:00 · Kod tabanını bir kez okuyup bilgi grafiği çıkaran ücretsiz araç. Claude oturumlarda dosyaları yeniden okumak yerine grafikte gezinir. · kanıt: So, this tool called Graphify just fixes it. You run it once
- klDiYMzW0o0 · 0:13 · Kod tabanını bilgi grafiğine dönüştürür; Claude her oturumda her şeyi baştan okumaz. · kanıt: Kod tabanını bir bilgi grafiğine dönüştürüyor.
- g89FJiNAlEs · 11:50 · Kod tabanını ve dokümanları sorgulanabilir bilgi grafiğine/haritaya çevirir. Ajan grep ile gidip gelmek yerine haritadan bulur. · kanıt: Anlatıcı Graphify'ı ikinci beyin olarak sorgulanabilir bilgi grafiği yapan araç diye anlatıyor. · iddia: Graphify kod haritasıyla grep gidiş-gelişlerini azaltıp token ve zaman tasarrufu sağlıyor.
