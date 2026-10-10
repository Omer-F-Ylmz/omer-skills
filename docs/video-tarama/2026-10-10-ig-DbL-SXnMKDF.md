# Reponun linkini yorumlara sabitledim 👇
## Künye
Reponun linkini yorumlara sabitledim 👇 · talhaunuvai · süre: 0:52 · ? · https://www.instagram.com/reel/DbL-SXnMKDF/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-10-short-8 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 15535 tk · claude-haiku-5-5: claude-haiku-5-5 · 92286 tk
## Özet
Kısa video, Claude Code'un her yeni oturumda aynı dosyaları baştan okuyarak token harcadığını anlatıyor. Çözüm olarak DeusData/codebase-memory-mcp reposu tanıtılıyor: kod tabanını tree-sitter ile tarayıp fonksiyon, dosya ve bağlantılardan kalıcı bir bilgi grafı çıkaran MCP sunucusu. Anlatıcıya göre 31 gerçek repoda dosya keşfine göre yaklaşık 10 kat daha az token harcıyor. Kurulum, install.sh betiğinin linkini Claude Code'a yapıştırıp kurdurma ve indeksletme şeklinde gösteriliyor. Repo linki yorumlara sabitlenmiş (yorumlar girişsiz alınamadı).
## Bölümler
- 0:00 Sorun: her oturumda tekrar okunan dosyalar ve token maliyeti
- 0:06 Codebase Memory reposunun tanıtımı (GitHub)
- 0:27 Özellikler ve 31 repo üzerindeki benchmark
- 0:35 Kurulum: linki kopyala, Claude Code'a yapıştır, indeksle
- 0:42 Sonuç: Claude kodun yerini önceden biliyor
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| codebase-memory-mcp | yok | MCP | https://github.com/DeusData/codebase-memory-mcp | Kod tabanını indeksleyip kalıcı bilgi grafı çıkaran, Claude Code'a kalıcı hafıza veren MCP sunucusu | 0:06 | Bu sorunu çözen reponun adı Codebase Memory. (karede: GitHub sayfası DeusData/codebase-memory-mcp (Public), About: High-performance code intelligence MCP server, 12.7k yıldız) |
| Claude Code | yok | CLI | yok | Videoda kurulumun yapıldığı ve repoyu sorgulayan ana yapay zekâ kodlama aracı | 0:00 | Cloud kodunu resmen para yakıyor. |
| GitHub | yok | teknik | yok | Reponun barındırıldığı ve tanıtımda gösterilen servis | 0:06 | GitHub Trend listesinde bir numaraya kadar çıktı (karede: GitHub üst menüsü, repo sayfası, Sign in/Sign up, Star 12.7k) |
| tree-sitter | yok | teknik | yok | 158 dilde AST analiziyle yüksek kaliteli ayrıştırma yapan kütüphane | 0:27 | High-quality parsing through tree-sitter AST analysis across all 158 languages (karede: README paragrafı: tree-sitter AST analysis across all 158 languages, Hybrid LSP) |
| Hybrid LSP | yok | teknik | yok | 10 dilde anlamsal tip çözümlemesi sağlayan katman | 0:27 | enhanced with Hybrid LSP semantic type resolution (karede: README: Hybrid LSP semantic type resolution; rozet Hybrid LSP 10 languages) |
| Remotion | yok | teknik | yok | Anlatıcının kendi projesinde Claude'a sorduğu örnek sorguda geçen video kütüphanesi (node_modules/remotion) | 0:15 | node_modules/remotion/index.js (karede: kanıttan) node_modules/remotion/index.js |
| VirusTotal | yok | teknik | yok | Sürüm ikililerini tarayan güvenlik servisi (rozet) | 0:27 | VirusTotal scanned every release (karede: README rozeti: VirusTotal scanned every release) |
| install.sh | yok | CLI | yok | Tek komutla kurulum yapan betik; curl ile indirilip bash'e verilir | 0:35 | codebase-memory-mcp/main/install.sh (karede: kanıttan) codebase-memory-mcp/main/install.sh |
| codebase-memory-mcp'yi kurdurma ve indeksletme | yok | prompt | yok | Claude Code'a repo linkinin yapıştırılıp aracı kurması ve projeyi indekslemesi isteniyor. | 0:36 | kaynak: altyazı |
| Kod konumunu hafıza aracıyla bulma örneği | yok | prompt | yok | Terminal-inserts skill'inin projede nerede tutulduğu soruluyor. | 0:13 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh / bash -s -- … index (tam bayraklar ekranda okunamadı) | codebase-memory-mcp'yi indirip kurar ve kurulumun ardından indeksleme başlatılır; tam bayraklar doğrulanamadı (karede: Ekran metni (OCR): '/ bash -s ---Ui index' ve 'install.sh' parçaları; kare gönderilmedi, komutun tamamı okunamadı.) | 0:37 | kare |
| claude ./promptible (OCR: 'claude -/promptible') | Demo projesinin klasöründe Claude Code oturumunu başlatır (karede: Terminalde '* claude -/promptible' satırı (OCR; kare gönderilmedi, tam yol okunamadı).) | 0:22 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Claude Code her yeni oturumda aynı dosyaları baştan okuyor ve maliyeti kullanıcı ödüyor | 0:00 | özellik |
| Repo GitHub Trend listesinde bir numaraya kadar çıktı | 0:06 | sayısal |
| Ortalama bir reponun haritasını milisaniyeler içinde çıkarıyor | 0:09 | sayısal |
| 31 gerçek repoda dosya keşfine göre yaklaşık 10 kat daha az token harcıyor | 0:27 | karşılaştırma |
| README'ye göre 83% cevap kalitesi, 10× daha az token, 2.1× daha az araç çağrısı | 0:29 | sayısal |
| Bir kez indekslenince sonrasını kendisi güncel tutuyor | 0:37 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| altyazı 0:00 | Claude Code | Claude Code | Cloud kodunu resmen para yakıyor. |
| altyazı 0:00 | GitHub Trend | GitHub | GitHub Trend listesinde bir numaraya kadar çıktı |
| kare 0:06 | DeusData/codebase-memory-mcp | codebase-memory-mcp | Repo sayfası başlığı |
| kare 0:06 | Martin Vogel LinkedIn profili | aday değil: konu dışı | Hover kartında linkedin.com/in/martin-vogel- URL'si |
| kare 0:27 | tree-sitter | tree-sitter | tree-sitter AST analysis |
| kare 0:27 | Hybrid LSP | Hybrid LSP | Hybrid LSP 10 languages |
| kare 0:27 | VirusTotal rozeti | VirusTotal | VirusTotal scanned every release |
| kare 0:27 | arXiv:2603.27277 makalesi | aday değil: başka adayın parçası (codebase-memory-mcp) | Codebase-Memory preprint |
| kare 0:27 | OpenSSF Scorecard, SLSA, MIT license rozetleri | aday değil: başka adayın parçası (codebase-memory-mcp) | README rozetleri |
| kare 0:15 | Remotion | Remotion | node_modules/remotion/index.js |
| kare 0:35 | install.sh | install.sh | codebase-memory-mcp/main/install.sh Copied! |
| kare 0:42 | Google Sheets, Instantly, NeverBounce, AmpleLeads | aday değil: konu dışı | Claude'un örnek projedeki yanıt metninde geçiyor |
| kare 0:00 | Token sayacı animasyonu | aday değil: genel kavram | TOPLAM MALIYET, OTURUM #1-#3 |
| açıklama | Repo linki yorumlara sabitlendi | codebase-memory-mcp | Reponun linkini yorumlara sabitledim |
## Kareden okunanlar
- 0:06: GitHub: DeusData/codebase-memory-mcp (Public), hover kartında DeusData Martin Vogel, Berlin; klasörler graph-ui vb.
- 0:09: Fork 924, Star 12.7k, 888 Commits; About: High-performance code intelligence MCP server, 158 languages, 99% fewer tokens, single static binary
- 0:27: README: rozetler release v0.9.0, MIT, 158 languages, VirusTotal, arXiv 2603.27277; 15 MCP tools, 43 agent surfaces; benchmark 83% answer quality, 10× fewer tokens
## Belirsizlikler
- Yorumlar girişsiz alınamadı; sabitlenen repo linki görülemedi, repo_url ekran görüntüsündeki ad üzerinden çıkarıldı.
- OCR'da Framer Motion, Emotion, Syne, v0 eşleşmeleri görünür ama videoda kullanıldığı doğrulanamadı; bunlar OCR gürültüsü olabilir.
- 0:15 civarındaki Remotion/skill yolları anlatıcının kendi projesinden; aracın kendisi değil.
- Kurulum komutunun tam metni ekranda kısmen okunabildi (curl ... / bash -s -- --ui index).
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.linkedin.com/in/martin-vogel-ab5b66174/ | 0:06 | ekran | hayır |
| https://github.com/DeusData/codebase-memory-mcp | 0:06 | ekran | evet |
| https://deusdata.github.io/codebase-memory-mcp | 0:09 | ekran | hayır |
| https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | 0:35 | ekran | evet |
## İş akışı
- 1. adım — Sorunu tanımlama: Claude Code'un her oturumda aynı dosyaları baştan okuduğu ve token maliyeti gösterilir — araçlar: Claude Code
- 2. adım — GitHub'da codebase-memory-mcp repo sayfasını açıp README, yıldız ve About bölümünü gösterme — araçlar: GitHub
- 3. adım — Repo linkini kopyalama ve Claude Code'a yapıştırma — araçlar: GitHub, Claude Code
- 4. adım — Kurulum betiğini terminalde çalıştırma (curl ile install.sh'ı indirip bash'e verme) — araçlar: curl, bash, install.sh
- 5. adım — Claude Code'u kapatıp yeniden açarak MCP sunucusunu etkinleştirme — araçlar: Claude Code
- 6. adım — Claude Code'da MCP araçlarını ToolSearch ile bulma — araçlar: Claude Code, ToolSearch
- 7. adım — codebase-memory-mcp ile projeleri listeleme ve repoyu indeksleme — araçlar: codebase-memory-mcp
- 8. adım — Demo projede skill'in konumunu Claude Code'a sorma; yanıtta dosya yollarının bulunması — araçlar: Claude Code, codebase-memory-mcp
- 9. adım — Çağrı zinciri ve bağlantılı fonksiyonları grafikten bulma (anlatım) — araçlar: codebase-memory-mcp
- 10. adım — İndeksin bir kez kurulup sonrasında otomatik güncel tutulması (anlatım) — araçlar: codebase-memory-mcp
- 11. adım — Repo linkinin Instagram yorumlarına sabitlenmesi — araçlar: Instagram
## Promptlar
- codebase-memory-mcp'yi kurdurma ve indeksletme — Claude Code'a repo linkinin yapıştırılıp aracı kurması ve projeyi indekslemesi isteniyor.
- Kod konumunu hafıza aracıyla bulma örneği — Terminal-inserts skill'inin projede nerede tutulduğu soruluyor.
ikinci göz KAPALI: --ikinci-goz yok
