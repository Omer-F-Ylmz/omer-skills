# 🧠 This MCP server cuts your AI agent’s token usage by 99% on your codebase. // c
## Künye
🧠 This MCP server cuts your AI agent’s token usage by 99% on your codebase. // c · fullstackparody · süre: 0:00 · ? · https://www.instagram.com/p/Ddq_d1bDV_Z/ · platform: instagram · tür: görsel gönderi · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-10-short-8 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (7)
altyazı yok: kare-yalnız
claude-sonnet-5-5: claude-sonnet-5-5 · 64829 tk · claude-haiku-5-5: claude-haiku-5-5 · 38966 tk
## Özet
Instagram görsel gönderisi (karusel, 7 kare): codebase-memory-mcp adlı açık kaynak MCP sunucusunu tanıtıyor. Depoyu bilgi grafiğine indeksleyerek ajanın dosyaları yeniden okumadan yapısal sorulara cevap vermesini sağladığı, 412.000 tokenlık aramanın yaklaşık 3.400 tokena indiği, 158 dil desteği, 1 ms altı sorgu, tek satırlık kurulum ve Claude Code/Cursor/Codex uyumu anlatılıyor. Tüm rakamlar gönderinin kendi iddiasıdır, bağımsız doğrulanmadı.
## Bölümler
- 0:00 Kapak: %99 daha az token
- 0:00 Kaynak: GitHub deposu
- 0:00 Nedir: kod belleği ve bilgi grafiği
- 0:00 Sayı: 412k tokendan 3,4k'ya
- 0:00 Hız: sub-1ms ve Linux çekirdeği indeksleme
- 0:00 Kurulum: tek satır
- 0:00 Kapanış: takip çağrısı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| codebase-memory-mcp | yok | MCP | https://github.com/DeusData/codebase-memory-mcp | Depoyu kalıcı bilgi grafiğine indeksleyen, yapı/bağımlılık/çağrı zinciri sorularını yanıtlayan MCP sunucusu | 0:00 | Kapak ve GitHub deposu karesinde adı görünüyor (karede: Kapakta 'CODEBASE-MEMORY-MCP' ve GitHub sayfasında DeusData/codebase-memory-mcp deposu) |
| Claude Code | yok | CLI | yok | Sunucunun bağlanabildiği kodlama ajanı | 0:00 | Kurulum karesinde 'add to Claude Code / Cursor / Codex' (karede: Kurulum terminalinde 'or add to Claude Code / Cursor / Codex' satırı) |
| Cursor | yok | plugin | yok | Sunucunun bağlanabildiği kod editörü/ajan | 0:00 | Kurulum karesinde ve açıklamada geçiyor (karede: Kurulum terminalinde 'Claude Code / Cursor / Codex' satırı) |
| Codex | yok | CLI | yok | Desteklenen ajanlardan biri | 0:00 | Kurulum karesinde 'Claude Code, Cursor, Codex and more than 40 other agents' (karede: Kurulum karesi açıklama kutusunda 'Claude Code, Cursor, Codex and more than 40 other agents') |
| tree-sitter | yok | teknik | yok | 158 dili ayrıştırmak için kullanılan ayrıştırıcı kütüphane | 0:00 | Hız karesinde 'parses 158 languages with tree-sitter' (karede: Hız karesinde açıklama kutusu ve terminalde 'Using tree-sitter parsers') |
| Bilgi grafiği | yok | teknik | yok | Kod yapısını düğüm ve ilişkilerle saklayan kalıcı grafik (knowledge graph) | 0:00 | Nedir karesinde 'indexes your repo into a knowledge graph' · kanıt: kare (karede: 'What it is' karesinde açıklama kutusu metni) |
| curl | yok | CLI | yok | Kurulum betiğini indirmek için kullanılan komut | 0:00 | Kurulum terminalinde curl -fsSL komutu (karede: Terminalde 'curl -fsSL codebase-memory.dev/install.sh / sh') |
| Python | yok | teknik | yok | Örnek query.py ve compare_tokens.py betiklerinde kullanılan dil | 0:00 | Editörde query.py, terminalde python compare_tokens.py (karede: query.py sekmesi ve terminalde '$ python compare_tokens.py') |
| GitHub | yok | teknik | yok | Deponun barındığı ve gösterildiği servis | 0:00 | Tarayıcıda github.com adresi (karede: Tarayıcı adres çubuğunda github.com/DeusData/codebase-memory-mcp) |
| zsh | yok | CLI | yok | Token karşılaştırma karesinde gösterilen terminal kabuğu | 0:00 | Terminal sekmesi 'zsh' (karede: Sayı karesinde terminal sekmesinde 'zsh') |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| curl -fsSL codebase-memory.dev/install.sh / sh | Yerel ikili dosyayı indirip /usr/local/bin altına kurar (karede: Kurulum terminalinde ilk satır) | 0:00 | kare |
| codebase-memory-mcp --version | Kurulu sürümü gösterir (0.6.1) (karede: Terminalde '--version' ve '0.6.1' çıktısı) | 0:00 | kare |
| codebase-memory-mcp --help | Seçenekleri listeler: --index, --query, --server, --help (karede: Terminalde 'Usage: codebase-memory-mcp [options]' ve seçenek listesi) | 0:00 | kare |
| codebase-memory-mcp index ./linux | Linux çekirdeği deposunu bilgi grafiğine indeksler (karede: Hız karesi terminalinde ilk komut) | 0:00 | kare |
| codebase-memory-mcp query "net_init call ch..." | Bilgi grafiğinde çağrı zinciri sorgusu çalıştırır; komut satırı kırpık (karede: Terminalde ikinci komut, sağ tarafı kesik) | 0:00 | kare |
| python compare_tokens.py | Dosya araması ile grafik sorgusunun token tüketimini karşılaştırır (karede: Sayı karesi terminalinde '$ python compare_tokens.py') | 0:00 | kare |
| python query.py | CodebaseMemory ile 'createUser' çağıranlarını sorgular (karede: Editör terminalinde '$ python query.py') | 0:00 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| 412.000 tokenlık dosya araması grafik sorgularıyla yaklaşık 3.400 tokena düşer (%99 azalma) | 0:00 | sayısal |
| 158 dili tree-sitter ile ayrıştırır, sorgular 1 ms altında yanıtlanır | 0:00 | sayısal |
| 28 milyon satırlık Linux çekirdeği yaklaşık 3 dakikada indekslendi | 0:00 | sayısal |
| Tek satırla yerel ikili dosya kurulur; Docker ve API anahtarı gerekmez | 0:00 | özellik |
| Claude Code, Cursor, Codex ve 40'tan fazla ajanla çalışır; MIT lisanslı | 0:00 | özellik |
| Depo 43,3 bin yıldız aldı | 0:00 | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| kare 0:00 | codebase-memory-mcp | codebase-memory-mcp | Kapak etiketi ve depo adı |
| açıklama | MCP | codebase-memory-mcp | MCP sunucusu olarak tanımlanıyor |
| açıklama | Claude Code | Claude Code | Uyumlu ajan olarak anılıyor |
| açıklama | Cursor | Cursor | Uyumlu ajan olarak anılıyor |
| kare 0:00 | Codex | Codex | Kurulum karesinde anılıyor |
| kare 0:00 | tree-sitter | tree-sitter | Ayrıştırıcı olarak anlatılıyor |
| kare 0:00 | Bilgi grafiği | Bilgi grafiği | Temel çalışma yöntemi |
| kare 0:00 | GitHub deposu sayfası | GitHub | Tarayıcı karesinde gösteriliyor |
| kare 0:00 | curl kurulum komutu | curl | Kurulum terminalinde |
| kare 0:00 | Python betikleri (query.py, compare_tokens.py) | Python | Editör ve terminalde |
| kare 0:00 | zsh terminali | zsh | Terminal sekmesi adı |
| kare 0:00 | Docker | aday değil: konu dışı | Yalnızca 'gerekmez' diye anılıyor, kullanılmıyor |
| kare 0:00 | Linux çekirdeği | aday değil: konu dışı | Yalnızca indeksleme örnek verisi |
| kare 0:00 | deusdata.dev | aday değil: konu dışı | Depo sayfasındaki proje web sitesi, kullanılmıyor |
| kare 0:00 | @fullstackparody | aday değil: konu dışı | Hesap tanıtımı |
| açıklama | MIT lisansı | aday değil: konu dışı | Lisans bilgisi |
| açıklama | Hashtag'ler (#mcp #claudecode #cursor #aiagents #devtools) | aday değil: genel kavram | Etiketler |
| yorum | Yorumlar | aday değil: konu dışı | Girişsiz alınamadı |
## Kareden okunanlar
- 1 (0:00): Kapak: 'CODEBASE-MEMORY-MCP', '99% fewer tokens.', madeni para yığınları görseli
- 2 (0:00): GitHub: DeusData/codebase-memory-mcp, Star 43.3k, Fork 2.9k, v0.6.1, MIT, deusdata.dev
- 3 (0:00): 'code memory' başlığı; query.py örneği ve createUser sorgu çıktısı; '15 MCP tools, in-memory'
- 4 (0:00): '99% fewer'; python compare_tokens.py; 412,000 token ve ~3,400 token karşılaştırması
- 5 (0:00): 'sub-1ms'; Linux çekirdeği 28M LOC 3m 04s; sorgu gecikmesi 0.7ms; tree-sitter
- 6 (0:00): 'one line'; curl kurulum komutu; --version 0.6.1; --help seçenekleri; '45 agent surfaces, MIT'
- 7 (0:00): 'follow for more.' ve '@fullstackparody / coding + ai tools'
## Belirsizlikler
- Video değil görsel gönderi; süre 0:00, tüm zamanlar 0:00 olarak yazıldı.
- Yorumlar girişsiz alınamadı.
- Kareler yapay üretim görünümlü; terminal çıktıları ve rakamlar (412k→3,4k, 0,7 ms) gerçek ölçüm olmayabilir.
- Python örneğindeki 'from codebase_memory import CodebaseMemory' API'sinin gerçekte var olduğu doğrulanamadı.
- Kurulum karesinde '/usr/local/bin/codebase-memory' ile komut adı 'codebase-memory-mcp' farklı yazılmış.
- Sorgu komutu karede kırpık; tam metni bilinmiyor.
- Gönderide 15 MCP aracı geçiyor ama araç listesi gösterilmiyor.
- Kurulum karesinde '40+ ajan' ile '45 agent surfaces' ifadeleri birlikte geçiyor.
## Atlanan segment oranı
0/0 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.instagram.com/p/Ddq_d1bDV_Z/ | açıklama | açıklama | hayır |
| github.com/DeusData/codebase-memory-mcp | 0:00 | ekran | evet |
| deusdata.dev | 0:00 | ekran | hayır |
| codebase-memory.dev/install.sh | 0:00 | ekran | evet |
## İş akışı
- 1. adım — GitHub'da DeusData/codebase-memory-mcp deposu sayfasını açıp yıldız, lisans ve sürümü incelemek — araçlar: GitHub
- 2. adım — Örnek query.py dosyasında CodebaseMemory ile depoyu graf olarak oluşturup 'createUser' çağıran yerleri sorgulamak — araçlar: Python, CodebaseMemory (Python), VS Code benzeri editör
- 3. adım — compare_tokens.py ile dosya taraması ve graf sorgusunun token kullanımını karşılaştırmak — araçlar: Python, zsh
- 4. adım — Linux çekirdeği deposunu 'codebase-memory-mcp index ./linux' ile indekslemek (yaklaşık 3 dk) — araçlar: codebase-memory-mcp, tree-sitter
- 5. adım — 'codebase-memory-mcp query' ile net_init çağrı zincirini sorgulayıp gecikmeyi (0,7 ms) ölçmek — araçlar: codebase-memory-mcp
- 6. adım — curl ile install.sh betiğini indirip sh üzerinden tek satırda kurmak — araçlar: curl, codebase-memory-mcp
- 7. adım — Kurulumu 'codebase-memory-mcp --version' ile doğrulamak — araçlar: codebase-memory-mcp
- 8. adım — Kullanılabilir seçenekleri 'codebase-memory-mcp --help' ile listelemek — araçlar: codebase-memory-mcp
- 9. adım — Aracı Claude Code, Cursor veya Codex'e eklemek (gösterilmedi, yalnızca anıldı) — araçlar: Claude Code, Cursor, Codex
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
