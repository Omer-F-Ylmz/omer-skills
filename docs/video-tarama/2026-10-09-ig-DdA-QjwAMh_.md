# Automate bug bounty hunting with 50 AI agents. Free, open-source, and works with
## Künye
Automate bug bounty hunting with 50 AI agents. Free, open-source, and works with · gittrend.io · süre: 0:40 · ? · https://www.instagram.com/reel/DdA-QjwAMh_/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-34 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 17312 tk · claude-haiku-5-5: claude-haiku-5-5 · 118923 tk
## Özet
Kısa reel, Pentest Agent Suite (H-mmer/pentest-agents) adlı ücretsiz, açık kaynaklı bug bounty çatısını tanıtıyor. Çatı 50 yapay zekâ ajanı, 26 komut, 19 CLI aracı, 11 skill ve 2 MCP sunucusu içeriyor. Claude Code ve 6 başka kodlama aracıyla çalışıyor. Videoda README, kurulum komutları, kurucu betik, çapraz IDE yükleyici, iş akışı ve MCP sunucuları gösteriliyor.
## Bölümler
- 0:00 Pentest Agent Suite tanıtımı ve hızlı başlangıç
- 0:07 Kurulum: paketler ve yükleyici
- 0:21 Çeviri kuralları ve yükleyici yönetimi
- 0:30 İş akışı ve MCP sunucuları
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Pentest Agent Suite | yok | iş akışı | https://github.com/H-mmer/pentest-agents-suite | 50 ajanlı, açık kaynaklı otonom bug bounty çatısı | 0:00 | README başlığı Pentest Agent Suite for Claude Code; konuşmada 50 ajan geçiyor (karede: kanıttan) README başlığı Pentest Agent Suite for Claude Code; konuşmada 50 ajan geçiyor |
| Claude Code | yok | CLI | yok | Çatının ana çalıştığı yapay zekâ kodlama aracı | 0:00 | README: Autonomous bug-bounty framework for Claude Code (karede: kanıttan) README: Autonomous bug-bounty framework for Claude Code |
| Opus 4.7 [1M] | yok | teknik | yok | Alt ajanların miras aldığı model | 0:00 | Komut bloğunda # Opus 4.7 [1M] - subagents inherit via model (karede: kanıttan) Komut bloğunda # Opus 4.7 [1M] - subagents inherit via model |
| Codex | yok | CLI | yok | Desteklenen diğer kodlama aracı | 0:00 | README: Claude Code, Codex, Gemini, Cursor... (karede: kanıttan) README: Claude Code, Codex, Gemini, Cursor... |
| Gemini | yok | CLI | yok | Desteklenen kodlama aracı (Gemini CLI) | 0:00 | README listesinde Gemini; .gemini/ yolları (karede: kanıttan) README listesinde Gemini; .gemini/ yolları |
| Cursor | yok | plugin | yok | Desteklenen IDE | 0:00 | README listesinde Cursor; .cursor/ yolları (karede: kanıttan) README listesinde Cursor; .cursor/ yolları |
| Windsurf | yok | plugin | yok | Desteklenen IDE | 0:00 | README listesinde Windsurf; .windsurf/ yolları (karede: kanıttan) README listesinde Windsurf; .windsurf/ yolları |
| VS Code Copilot | yok | plugin | yok | Desteklenen GitHub Copilot hedefi | 0:00 | README listesinde VS Code Copilot; .github/ yolları (karede: kanıttan) README listesinde VS Code Copilot; .github/ yolları |
| OpenClaw | yok | CLI | yok | Desteklenen yedinci araç | 0:00 | README listesinde OpenClaw; openclaw/ dizini (karede: kanıttan) README listesinde OpenClaw; openclaw/ dizini |
| MCP | yok | MCP | yok | bounty-platforms ve writeup-search sunucuları | 0:32 | README: MCP Servers (2), bounty-platforms (16 platforms) (karede: kanıttan) README: MCP Servers (2), bounty-platforms (16 platforms) |
| HackerOne | yok | MCP | yok | Tam API ile entegre bug bounty platformu | 0:32 | Altyazıda HackerOne gibi platformlara bağlanan MCP sunucuları anlatılıyor |
| uv | yok | CLI | yok | Python betiklerini ve MCP sunucularını çalıştırır | 0:00 | uv run python3 tools/scaffold.py hackerone tesla (karede: kanıttan) uv run python3 tools/scaffold.py hackerone tesla |
| scaffold.py | yok | CLI | yok | Hedef için çalışma alanı kurar | 0:00 | scaffold.py provisions the workspace metni (karede: kanıttan) scaffold.py provisions the workspace metni |
| tools.installer | yok | CLI | yok | Çapraz IDE yükleyici ve render aracı | 0:11 | python3 -m tools.installer install --targets codex --scope global (karede: kanıttan) python3 -m tools.installer install --targets codex --scope global |
| pentest-agents CLI | yok | CLI | yok | Kurulum, doğrulama, kaldırma ve render komutları | 0:27 | pentest-agents install --dry-run; install --targets claude_code,codex · kanıt: kare (karede: pentest-agents install --dry-run; install --targets claude_code,codex) |
| FAISS | yok | teknik | yok | writeup-search için anlamsal arama | 0:34 | search_writeups — semantic search (FAISS) (karede: kanıttan) search_writeups — semantic search (FAISS) |
| SQLite | yok | teknik | yok | writeup-search için LIKE tabanlı anahtar kelime arama modu | 0:38 | Ekranda LIKE over the text column ve SQLite (karede: kanıttan) Ekranda LIKE over the text column ve SQLite |
| Python | yok | teknik | yok | Çatının çalışma gereksinimi | 0:00 | Rozet python 3.10+ (karede: kanıttan) Rozet python 3.10+ |
| Git | yok | CLI | yok | Repoyu klonlamak için | 0:08 | git clone https://github.com/H-mmer/pentest-agents-suite (karede: kanıttan) git clone https://github.com/H-mmer/pentest-agents-suite |
| GitHub | yok | teknik | yok | Reponun barındırıldığı servis | 0:00 | Tarayıcı sekmesi GitHub - H-mmer/pentest-a (karede: kanıttan) Tarayıcı sekmesi GitHub - H-mmer/pentest-a |
| Claude Opus | yok | teknik | yok | /model opus ile seçilen model; ekranda Opus 4.7 [1M] yazıyor. | 0:00 | /model opus (karede: Kod bloğunda /model opus ve yanında Opus 4.7 [1M] başlığı.) |
| Bugcrowd | yok | MCP | yok | bounty-platforms MCP sunucusunda desteklenen bug bounty platformu. | 0:32 | HackerOne (full API), Bugcrowd, Intigriti, Immunefi (public), YesWeHack (karede: MCP Servers bölümünde platform listesi.) |
| Intigriti | yok | MCP | yok | bounty-platforms MCP sunucusunda desteklenen bug bounty platformu. | 0:32 | HackerOne (full API), Bugcrowd, Intigriti, Immunefi (public), YesWeHack (karede: MCP Servers bölümünde platform listesi.) |
| Immunefi | yok | MCP | yok | bounty-platforms MCP sunucusunda (public) olarak desteklenen platform. | 0:32 | HackerOne (full API), Bugcrowd, Intigriti, Immunefi (public), YesWeHack (karede: MCP Servers bölümünde platform listesi.) |
| YesWeHack | yok | MCP | yok | bounty-platforms MCP sunucusunda desteklenen bug bounty platformu. | 0:32 | HackerOne (full API), Bugcrowd, Intigriti, Immunefi (public), YesWeHack (karede: MCP Servers bölümünde platform listesi.) |
| bounty-platforms | yok | MCP | yok | 16 bug bounty platformuna bağlanan MCP sunucusu; list_platforms, get_program_scope, get_program_policy gibi araçlar sunar. | 0:32 | MCP tools: list_platforms, get_program_scope, get_program_policy (karede: MCP Servers (2) bölümünde bounty-platforms (16 platforms) ve MCP tools listesi.) |
| writeup-search | yok | MCP | yok | Önceki writeup'larda semantik veya anahtar kelime araması yapan MCP sunucusu (kendi indeksinizle). | 0:33 | writeup-search (BYO index) (karede: MCP Servers bölümünde writeup-search (BYO index) başlığı.) |
| /hunt | yok | iş akışı | yok | Pentest Agents'ta bir hedef için otonom avı başlatan komut. | 0:00 | /hunt tesla.com (karede: Kod bloğunda /hunt tesla.com satırı.) |
| 7-Question Gate | yok | iş akışı | yok | Bulguları /triage komutuyla toplu eleyen 7 soruluk doğrulama kapısı. | 0:32 | Batch triage: /triage (7-Question Gate on all findings) (karede: Workflow bölümünde Batch triage satırı.) |
| Otomatik bug bounty avı başlatma | yok | prompt | yok | Hedef tesla.com için otonom bug bounty avı başlatılır (/hunt komutu). | 0:00 | kaynak: kare |
## Açıklama bağlantıları
- https://gittrend.io — Açıklamadaki 'More like this' bağlantısı (gittrend.io). · aday: hayır · Tanıtım/yönlendirme sitesi; videoda anlatılan bir araç değil. · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| uv run python3 tools/scaffold.py hackerone tesla | HackerOne tesla hedefi için çalışma alanı kurar | 0:00 | kare |
| cd ~/bounties/hackerone-tesla && claude | Çalışma alanında Claude Code'u açar | 0:00 | kare |
| export HACKERONE_USERNAME=you HACKERONE_TOKEN=[gizlendi] | HackerOne kimlik bilgilerini ortam değişkeni yapar | 0:00 | kare |
| /hunt tesla.com | Hedefte otonom avı başlatır | 0:00 | kare |
| /model opus | Modeli Opus yapar | 0:00 | kare |
| /sync hackerone tesla | Programı HackerOne'dan eşitler | 0:00 | kare |
| /brain init && /status | Beyni başlatır, durumu gösterir | 0:00 | kare |
| git clone https://github.com/H-mmer/pentest-agents-suite | Repoyu klonlar | 0:08 | kare |
| cd pentest-agents-suite/pentest-agents/providers/codex | Codex paketine geçer | 0:10 | kare |
| python3 -m tools.installer install --targets all --scope project | Tüm hedefleri proje kapsamında kurar | 0:12 | kare |
| python3 -m tools.installer install --targets codex --scope global | Yalnız Codex'i global kurar | 0:11 | kare |
| python3 -m tools.installer render --targets all | providers/ paketlerini yeniden üretir | 0:22 | kare |
| python3 -m tools.installer render --check | Sapma kontrolü yapar, kirliyse çıkış 1 | 0:22 | kare |
| pentest-agents install --dry-run | Dosya ve JSON değişikliklerini önizler | 0:27 | kare |
| pentest-agents install --targets claude_code,codex --scope global | Seçili hedefleri global kurar | 0:27 | kare |
| export HACKERONE_USERNAME=... HACKERONE_TOKEN=[gizlendi] | HackerOne kullanıcı adı ve token'ını ortam değişkeni olarak ayarlar (değerler yazılmadı). (karede: Kod bloğunda export satırı; değerler placeholder.) | 0:00 | kare |
| cd pentest-agents-suite/pentest-agents/providers/codex && codex | Codex için hazır paket klasörüne geçer ve Codex'i başlatır. (karede: Kurulum kod bloğunda cd .../providers/codex ve codex satırları.) | 0:10 | kare |
| cd ../gemini && gemini | Gemini paketi klasörüne geçer ve Gemini CLI'yı başlatır. (karede: Kurulum kod bloğunda '# or: cd ../gemini && gemini, etc.' yorumu.) | 0:09 | kare |
| pentest-agents list | Kurulu hedef araçları tespit eder ve listeler. (karede: Installer management kod bloğunda list satırı.) | 0:32 | kare |
| pentest-agents verify | Kurulum manifest'ini kontrol eder. (karede: Installer management kod bloğunda verify satırı.) | 0:32 | kare |
| pentest-agents uninstall | Yazılan dosyaları siler, yedeklenen .pa-backup dosyalarını geri yükler ve yalnız eklenen MCP/JSON anahtarlarını çıkarır. (karede: Installer management kod bloğunda uninstall satırı.) | 0:32 | kare |
| /new → /sync → /brain init → /analyze → /surface → /hunt → … → /validate → /chain → /report → /bugcheck → /submit | Yeni program için sohbet içi iş akışı sırası; ilk satır okunabiliyor, son kısım kısmen okunuyor. (karede: Workflow bölümünde New program ve After finding satırları.) | 0:32 | kare |
| /triage | Tüm bulgulara 7-Question Gate uygular (toplu eleme). (karede: Workflow bölümünde Batch triage: /triage satırı.) | 0:32 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Çatı 50 ajan, 26 komut, 19 CLI aracı ve 2 MCP sunucusu içeriyor. | 0:00 | sayısal |
| Ajanlar keşif yapar, açık test eder, exploit zinciri kurar ve rapor gönderir. | 0:00 | özellik |
| Claude Code ve 6 başka kodlama aracıyla çalışır. | 0:00 | özellik |
| Writeup indeksi pakete dahil değil, kullanıcı kendi indeksini getirir. | 0:35 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Pentest Agents / 50 ajan | Pentest Agent Suite | Pentest Agents is a free tool that runs 50 AI agents |
| kare 0:00 | Claude Code | Claude Code | README başlığında Claude Code |
| kare 0:00 | Opus 4.7 [1M] | Opus 4.7 [1M] | Komut bloğu yorumu |
| kare 0:00 | Codex, Gemini, Cursor, Windsurf, VS Code Copilot, OpenClaw | Codex | README desteklenen araçlar listesi; diğerleri ayrı adaylar |
| kare 0:00 | uv run scaffold.py | uv | uv run python3 tools/scaffold.py |
| kare 0:00 | HackerOne | HackerOne | HACKERONE_USERNAME ve MCP platform listesi |
| kare 0:00 | tesla.com hedefi | aday değil: konu dışı | Örnek hedef alan adı |
| kare 0:00 | python 3.10+ | Python | Rozet |
| kare 0:32 | MCP sunucuları | MCP | MCP Servers (2) |
| ekran 0:34 | FAISS | FAISS | semantic search (FAISS) |
| ekran 0:38 | SQLite | SQLite | LIKE over the text column, SQLite |
| ekran 0:08 | git clone | Git | git clone komutu |
| ekran 0:13 | OpenAI | aday değil: başka adayın parçası (Codex) | Codex satırında OpenAI etiketi |
| ekran 0:35 | Redis | aday değil: konu dışı | Yalnız OCR eşleşmesi, videoda kullanılmıyor |
| ekran 0:36 | Three.js | aday değil: konu dışı | Yalnız sözlük eşleşmesi, videoda kullanılmıyor |
| ekran 0:39 | Skills CLI | aday değil: başka adayın parçası (Pentest Agent Suite) | skills/ shipped in this metni |
| açıklama | gittrend.io | aday değil: sponsor/reklam | More like this → gittrend.io |
| açıklama | Hashtag'ler | aday değil: konu dışı | #bugbounty #pentesting vb. |
| ekran 0:00 | Bugcrowd, Intigriti, Immunefi, YesWeHack | aday değil: başka adayın parçası (Pentest Agent Suite) | Platform listesi, MCP içinde |
| yorum | Yorumlar | aday değil: konu dışı | Girişsiz alınamadı |
## Kareden okunanlar
- 0:00: GitHub README: Pentest Agent Suite, rozetler, hızlı başlangıç komutları (scaffold.py, /hunt tesla.com)
- 0:15: Install bölümü: git clone, providers/codex, installer komutları, hedef tablosu
- 0:32: Çeviri kuralları, installer yönetimi, Workflow ve MCP Servers (bounty-platforms)
## Belirsizlikler
- Repo adı ekranda pentest-agents ve pentest-agents-suite olarak farklı görünüyor.
- OCR'daki Redis, Three.js, Skills CLI, agent-sdk-dev eşleşmeleri videoda kullanılmıyor, yanlış eşleşme olabilir.
- Yorumlar girişsiz alınamadı.
- gittrend.io açıklamada geçen yönlendirme sitesi; araç değil, aday sayılmadı.
- OCR'daki 'Opus 4.7 [1M]' yorumu Claude modeli olarak okundu.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| github.com/H-mmer/pentest-agents#readme | 0:00 | ekran | evet |
| tesla.com | 0:00 | ekran | hayır |
| slashhunttesla.com | 0:00 | ses | hayır |
| https://github.com/H-mmer/pentest-agents-suite | 0:08 | ekran | evet |
| gittrend.io | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — Pentest Agents deposunu klonla — araçlar: Git, GitHub
- 2. adım — Python 3.10+ ortamında uv ile hedef çalışma alanını oluştur (tesla için HackerOne) — araçlar: uv, Python, scaffold.py
- 3. adım — HackerOne kullanıcı adı ve token'ını ortam değişkeni olarak ayarla — araçlar: HackerOne
- 4. adım — Çalışma klasörüne geçip Claude Code'u başlat — araçlar: Claude Code
- 5. adım — Modeli Opus olarak seç — araçlar: Claude Code, Claude Opus
- 6. adım — Programı senkronize et ve beyin dizinini başlat — araçlar: Pentest Agents
- 7. adım — Hedef için otonom avı başlat (/hunt tesla.com) — araçlar: Pentest Agents, /hunt
- 8. adım — Alternatif kurulum: hazır paket klasörlerini Codex veya Gemini'de aç — araçlar: Codex, Gemini
- 9. adım — Installer ile tüm desteklenen hedeflere proje kapsamında kur — araçlar: pentest-agents CLI, Codex, Gemini, Cursor, Windsurf, VS Code Copilot, OpenClaw
- 10. adım — Kurulumu önizle (dry-run), listele ve manifest'i doğrula — araçlar: pentest-agents CLI
- 11. adım — Üretilen dosyalarda sapma olup olmadığını render --check ile kontrol et — araçlar: pentest-agents CLI
- 12. adım — Bulguları doğrula, zincirle, raporla ve gönder (/validate, /chain, /report, /bugcheck, /submit) — araçlar: Pentest Agents
- 13. adım — Tüm bulguları 7-Question Gate ile toplu ele (/triage) — araçlar: 7-Question Gate
- 14. adım — bounty-platforms MCP ile program kapsamı ve politikasını al — araçlar: bounty-platforms, HackerOne, Bugcrowd, Intigriti, Immunefi, YesWeHack
- 15. adım — writeup-search MCP ile önceki writeup'larda arama yap (FAISS veya SQLite) — araçlar: writeup-search, FAISS, SQLite
- 16. adım — Kurulumu geri al (pentest-agents uninstall) — araçlar: pentest-agents CLI
## Promptlar
- Otomatik bug bounty avı başlatma — Hedef tesla.com için otonom bug bounty avı başlatılır (/hunt komutu).
