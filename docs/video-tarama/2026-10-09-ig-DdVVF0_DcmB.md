# Turn your coding agents into research agents
## Künye
Turn your coding agents into research agents · git.radar · süre: 1:02 · ? · https://www.instagram.com/reel/DdVVF0_DcmB/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-27 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 39243 tk · claude-haiku-5-5: claude-haiku-5-5 · 90996 tk
## Özet
git.radar reeli, alphaXiv'in açık kaynak OpenResearch aracını tanıtıyor. Araç Claude Code, Codex, OpenCode veya Cursor gibi kodlama ajanlarını araştırma ajanlarına çeviriyor: deneyleri kendi başına çalıştırıyor, sonuçları kaydediyor, git tabanlı deney ağacında sürümleri tutuyor. Veri yerelde (SQLite) kalıyor. Reel GitHub'da 3.495 yıldız ve günün 1 numaralı deposu rozetini gösteriyor.
## Bölümler
- 0:00 OpenResearch tanıtımı ve GitHub günün deposu rozeti
- 0:03 Kurulum komutu ve yerel model bağlantısı
- 0:10 Araştırma ajanları için özellik tablosu
- 0:26 Autoresearch ve her yerde çalıştırma
- 0:33 Uzak GPU üzerinde çalıştırma (orx up --remote)
- 0:40 CLI komutları ve skill kurulumu
- 0:47 Yerel çalışma, SQLite ve telemetri
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| OpenResearch | yok | CLI | https://github.com/alphaXiv/OpenResearch | Kodlama ajanlarını araştırma ajanlarına çeviren, yerel öncelikli çalışma alanı; deney çalıştırır, sonuçları saklar. | 0:00 | README başlığı OpenResearch; yerel öncelikli çalışma alanı (karede: kanıttan) README başlığı OpenResearch; yerel öncelikli çalışma alanı |
| Claude Code | yok | CLI | yok | OpenResearch'ün araştırma ajanına çevirdiği kodlama ajanlarından biri. | 0:00 | Turn Claude Code, Codex, OpenCode, or Cursor (karede: kanıttan) Turn Claude Code, Codex, OpenCode, or Cursor |
| Codex | yok | CLI | yok | Desteklenen kodlama ajanı. | 0:00 | README satırında Codex (karede: kanıttan) README satırında Codex |
| OpenCode | yok | CLI | yok | Desteklenen kodlama ajanı; özel uç noktayla yerel model bağlamada da geçiyor. | 0:00 | README satırında OpenCode (karede: kanıttan) README satırında OpenCode |
| Cursor | yok | CLI | yok | Desteklenen kodlama ajanı. | 0:00 | README satırında Cursor (karede: kanıttan) README satırında Cursor |
| GitHub | yok | teknik | yok | Projenin barındırıldığı platform; trend rozeti burada. | 0:00 | GITHUB TRENDING #1 Repository Of The Day rozeti (karede: kanıttan) GITHUB TRENDING #1 Repository Of The Day rozeti |
| Rust | yok | teknik | yok | Açıklamada projenin dili olarak belirtilen programlama dili. | açıklama | Açıklamada Rust etiketi ve mavi daire |
| orx | yok | CLI | https://github.com/alphaXiv/OpenResearch | OpenResearch komut satırı aracı: up, projects, runs, exp run, logs, paper, discover. | 0:33 | orx up --remote user@host komut bloğu (karede: kanıttan) orx up --remote user@host komut bloğu |
| orx install-skills | yok | skill | yok | OpenResearch skill'ini desteklenen kodlama ajanlarına kurar. | 0:41 | OCR: orx install-skills; Install the OpenResearch skill (karede: kanıttan) OCR: orx install-skills; Install the OpenResearch skill |
| Autoresearch | yok | teknik | yok | Fikir öner, kodu değiştir, deney başlat, kanıtı incele döngüsünü otonom çalıştırma. | 0:29 | Autoresearch bölümü: can run the full loop autonomously (karede: kanıttan) Autoresearch bölümü: can run the full loop autonomously |
| Git worktree | yok | teknik | yok | Her araştırma yönü için izole git çalışma ağacı. | 0:33 | Parallel exploration: independent agent session and isolated git worktree (karede: kanıttan) Parallel exploration: independent agent session and isolated git worktree |
| SQLite | yok | teknik | yok | Yerel depolama; OpenResearch 127.0.0.1 üzerinde SQLite ile çalışır. | 0:48 | OCR: runs on 127.0.0.1 with a local SQLite store (karede: kanıttan) OCR: runs on 127.0.0.1 with a local SQLite store |
| LM Studio | yok | CLI | yok | Yerel model bağlamak için desteklenen seçenek. | 0:06 | OCR: Connect a local model to use LM Studio (karede: kanıttan) OCR: Connect a local model to use LM Studio |
| oMLX | yok | CLI | yok | Yerel model bağlamak için desteklenen seçenek. | 0:06 | OCR: LM Studio, oMLX, Ollama (karede: kanıttan) OCR: LM Studio, oMLX, Ollama |
| Ollama | yok | CLI | yok | Yerel model bağlamak için desteklenen seçenek. | 0:06 | OCR: Ollama, or a custom endpoint (karede: kanıttan) OCR: Ollama, or a custom endpoint |
| SSH | yok | teknik | yok | Deneyleri uzak makinede çalıştırma yolu. | 0:29 | can run locally, over SSH, or on Slurm (karede: kanıttan) can run locally, over SSH, or on Slurm |
| Slurm | yok | teknik | yok | Deneylerin çalıştırılabildiği küme zamanlayıcısı. | 0:29 | over SSH, or on Slurm, Kubernetes, Ray (karede: kanıttan) over SSH, or on Slurm, Kubernetes, Ray |
| Kubernetes | yok | teknik | yok | Deney çalıştırma hedefi. | 0:29 | Slurm, Kubernetes, Ray, Hugging Face Jobs (karede: kanıttan) Slurm, Kubernetes, Ray, Hugging Face Jobs |
| Ray | yok | teknik | yok | Deney çalıştırma hedefi. | 0:29 | Kubernetes, Ray, Hugging Face Jobs (karede: kanıttan) Kubernetes, Ray, Hugging Face Jobs |
| Hugging Face Jobs | yok | teknik | yok | Deney çalıştırma hedefi. | 0:29 | Ray, Hugging Face Jobs satırı (karede: kanıttan) Ray, Hugging Face Jobs satırı |
| Modal | yok | teknik | yok | Deney çalıştırma hedefi. | 0:30 | OCR: Modal, Tinker, and managed OpenResearch compute (karede: kanıttan) OCR: Modal, Tinker, and managed OpenResearch compute |
| Tinker | yok | teknik | yok | Deney çalıştırma hedefi. | 0:30 | OCR: Modal, Tinker, and managed OpenResearch compute (karede: kanıttan) OCR: Modal, Tinker, and managed OpenResearch compute |
| curl | yok | CLI | yok | Kurulum betiğini indirip çalıştırmak için kullanılan komut. | 0:03 | OCR: curl -LsSf https://openresearch.sh/install.sh / sh (karede: kanıttan) OCR: curl -LsSf https://openresearch.sh/install.sh / sh |
| Git for Windows | yok | teknik | yok | Windows beta sürümü için gerekli Git kurulumu. | 0:00 | README'de 'macOS 11+ · Windows beta requires Git for Windows' yazısı. (karede: README altındaki satırda 'macOS 11+ · Windows beta requires Git for Windows' bağlantısı.) |
## Açıklama bağlantıları
- https://github.com/alphaXiv/OpenResearch — OpenResearch GitHub deposu · aday: evet (OpenResearch) · Videoda anlatılan ve izleyicinin kullanabileceği aracın deposu. · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| curl -LsSf https://openresearch.sh/install.sh / sh | macOS/Linux'ta OpenResearch CLI'ı kurar. | 0:03 | kare |
| orx up | Yerel paneli http://127.0.0.1:4791 adresinde açar. | 0:06 | kare |
| orx up --remote user@host | Çalışma alanını uzak GPU makinesinin yanında çalıştırır. | 0:33 | kare |
| orx install-skills | OpenResearch skill'ini desteklenen kodlama ajanlarına kurar. | 0:41 | kare |
| orx projects | Projeleri listeler. | 0:42 | kare |
| orx runs <project-id> | Projenin çalıştırmalarını listeler. | 0:42 | kare |
| orx exp run <experiment-id> | Bir deneyi çalıştırır. | 0:43 | kare |
| orx logs <run-id> | Çalıştırma günlüklerini gösterir. | 0:43 | kare |
| orx discover keyword <query> | Anahtar kelimeyle keşif yapar. | 0:44 | kare |
| orx paper <arxiv-id-or-doi> | arXiv kimliği veya DOI ile makale getirir. | 0:44 | kare |
| orx --help | Tüm komutların yardımını gösterir. | 0:45 | kare |
| orx telemetry status | Telemetri durumunu gösterir. | 0:55 | kare |
| orx <command> --no-telemetry | Tek komutta telemetriyi kapatır. | 0:56 | kare |
| orx project view <p…> | Bir projenin ayrıntılarını gösterir (komut ekranda kesik). | 0:43 | kare |
| orx --help / orx <command> --help | Tüm komutların ve komut yardımının listesini gösterir. | 0:45 | kare |
| orx telemetry off | Telemetriyi kalıcı olarak kapatır. | 0:59 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Open Research 3.495 yıldız almış. | 0:00 | sayısal |
| Deneyleri kendi başına çalıştırır, sonuçları kaydeder, sürümleri tek yerde tutar. | 0:00 | özellik |
| Veriler kendi makinende kalır, buluta gönderilmez. | 0:00 | özellik |
| Mevcut kodlama araçlarıyla çalışır, iş akışı değişmez. | 0:00 | özellik |
| Günün 1 numaralı deposu rozeti (GitHub Trending). | 0:00 | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Open Research | OpenResearch | This new tool, called Open Research |
| kare 0:00 | Claude Code, Codex, OpenCode, Cursor | Claude Code | README satırı desteklenen ajanları sıralıyor |
| kare 0:00 | GitHub Trending rozeti | GitHub | #1 Repository Of The Day |
| açıklama | Rust | Rust | Açıklamada Rust etiketi |
| açıklama | Hashtag'ler (#opensource, #devtools vb.) | aday değil: genel kavram | Açıklama etiketleri |
| açıklama | GitHub deposu bağlantısı | OpenResearch | github.com/alphaXiv/OpenResearch |
| kare 0:03 | curl kurulum komutu | curl | curl -LsSf openresearch.sh/install.sh / sh |
| kare 0:06 | LM Studio, oMLX, Ollama | LM Studio | Connect a local model satırı |
| kare 0:06 | orx up paneli 127.0.0.1:4791 | orx | orx up opens the local dashboard |
| kare 0:08 | openresearch.sh hesabı | OpenResearch | Create an account at openresearch.sh |
| kare 0:11 | Git worktree, deney ağacı | Git worktree | isolated git worktree |
| kare 0:29 | Autoresearch | Autoresearch | Autoresearch bölümü |
| kare 0:29 | SSH, Slurm, Kubernetes, Ray, Hugging Face Jobs | SSH | Run anywhere paragrafı |
| kare 0:30 | Modal, Tinker | Modal | Modal, Tinker, and managed OpenResearch compute |
| kare 0:33 | orx up --remote | orx | orx up --remote user@host |
| kare 0:41 | orx install-skills | orx install-skills | Install the OpenResearch skill |
| kare 0:44 | orx paper, orx discover | orx | Common commands listesi |
| kare 0:48 | SQLite | SQLite | local SQLite store |
| kare 0:55 | orx telemetry | orx | orx telemetry status |
| kare 0:06 | Windows beta / Git for Windows | aday değil: konu dışı | Windows beta requires Git for Windows notu |
| yorum | Yorumlar | aday değil: konu dışı | Girişsiz alınamadı |
## Kareden okunanlar
- 0:00: alphaXiv/OpenResearch Public, MIT license, #1 Repository Of The Day, macOS/Windows/Linux indirme düğmeleri
- 0:29: Built for research agents tablosu: Parallel exploration, Reproducible experiments, Evidence in context, Local ownership; Autoresearch bölümü
- 0:33: Run anywhere bölümü, orx up --remote user@host komut bloğu
## Belirsizlikler
- Dil alanı '?'; altyazı İngilizce.
- OCR'deki Next.js, Llama, Inter, Meshy sözlük eşleşmeleri yanlış pozitif; adaya alınmadı.
- Yalnız 0:00, 0:29, 0:33 kareleri görüldü; diğer zamanların kanıtı OCR metnine dayanıyor, kaynak 'kare' olarak işaretlendi.
- Reel görsellerinde yorumlar alınamadı (girişsiz).
- Windows betası ve Git for Windows ekranda geçiyor; ayrı araç olarak adaylaştırılmadı.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://github.com/alphaXiv/OpenResearch | açıklama | açıklama | evet |
| https://www.instagram.com/reel/DdVVF0_DcmB/ | açıklama | açıklama | hayır |
| https://openresearch.sh/install.sh | 0:06 | ekran | evet |
| openresearch.sh | 0:08 | ekran | evet |
| http://127.0.0.1:4791 | 0:06 | ekran | hayır |
## İş akışı
- 1. adım — GitHub'da OpenResearch deposunu ve trend rozetini gösterme — araçlar: GitHub, OpenResearch
- 2. adım — CLI'ı curl betiğiyle kurma — araçlar: curl, orx
- 3. adım — Yerel paneli orx up ile açma — araçlar: orx
- 4. adım — İsteğe bağlı yerel model bağlama — araçlar: LM Studio, oMLX, Ollama, OpenCode
- 5. adım — Araştırma yönü başına izole ajan oturumu ve git worktree açma — araçlar: Git worktree, Claude Code, Codex, OpenCode, Cursor
- 6. adım — Autoresearch döngüsünü çalıştırma: fikir, kod değişikliği, deney, kanıt — araçlar: Autoresearch, OpenResearch
- 7. adım — Deneyi yerelde, SSH'ta veya bulut hedeflerinde çalıştırma — araçlar: SSH, Slurm, Kubernetes, Ray, Hugging Face Jobs, Modal, Tinker
- 8. adım — Uzak GPU'da orx up --remote ile çalıştırma — araçlar: orx, SSH
- 9. adım — CLI komutlarıyla proje, çalıştırma, günlük ve makale sorgulama — araçlar: orx
- 10. adım — Skill'i ajanlara kurma — araçlar: orx install-skills
- 11. adım — Yerel SQLite depolamayı ve telemetri kapatmayı gösterme — araçlar: SQLite, orx
## Promptlar
- yok
