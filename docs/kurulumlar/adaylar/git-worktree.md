# Git worktree
ad: Git worktree
tur: CLI
video: jqoFP9QapXI
repo: git/git
lisans: GPL-2.0-only
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/git/git
telemetri: Yok. Git yerel çalışır ve kendiliğinden ağa veri göndermez. Claude Code'un kendi telemetrisi ayrı bir konudur ve burada incelenmedi.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-7)
## Ne
Git'in yerleşik alt komutu. Tek bir depoya bağlı birden fazla çalışma dizini oluşturur. Her dizinde farklı bir dal çıkış yapılmış olur. Video, Claude Code'da her özellik için izole dal ve çalışma alanıyla paralel oturum açmak için bunu kullanıyor.
## Mekanizma
`git worktree add <yol> -b <dal>` yeni bir dizin açar. Bu dizin ana deponun .git nesne veritabanını paylaşır. Dizine özel HEAD ve index bilgisi .git/worktrees/ altında tutulur. Her Claude oturumu ayrı bir dizinde çalıştığı için oturumlar birbirinin dosyalarını ezmez. İş bitince `git worktree remove` ile dizin silinir, dal merge edilir. Videodaki `claude --worktree <ad>` kısayolu bu işi Claude Code tarafında otomatikleştiriyor olmalı. Bunu kendim doğrulamadım.
## Kanıt
- Her özellik için izole dal/çalışma alanıyla paralel oturumlar açılabilir. → doğrulandı · Git worktree'nin tasarımı budur: ortak depoda ayrı dizinlerde ayrı dallar. Bu bilgi Git'in belgelenmiş davranışından geliyor, bu oturumda komut çalıştırılmadı.
- Claude Code'da 'claude --worktree <özellik adı>' yazmak yeterli. → sınanamadı · Yalnız videodaki ifade var: 'You just type in Claude dash work tree and then that feature name.' Bayrağı bu oturumda denemedim, Claude Code sürümünde var olduğunu doğrulamadım.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Git kuruluysa ek kurulum gerekmez (git 2.5 ve üstü).
- git worktree add ../ozellik-x -b ozellik-x
- cd ../ozellik-x && claude
- Bitince: git worktree remove ../ozellik-x
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Paralel özellik geliştirmede izolasyon sağlar. Her görev kendi dalında ve dizininde yürür. Klonlamaya göre disk ve süre tasarrufu vardır, çünkü nesne veritabanı paylaşılır. Bir oturumdaki hata diğerlerini etkilemez.
## Maliyet/risk
Aynı dal iki worktree'de aynı anda çıkış yapılamaz. node_modules ve .env gibi izlenmeyen dosyalar her dizine ayrıca kurulmalı veya kopyalanmalıdır. Unutulan worktree'ler birikir (`git worktree prune` gerekir). Dallar arası merge çakışması yine el ile çözülür. Video kaynaklı `claude --worktree` bayrağının ayrıntıları doğrulanmadı.
## Tasarruf
Token aracı değil, doğrudan token tasarrufu sağlamaz. Dolaylı fayda: paralel oturumlar birbirinin değişikliklerini karıştırmadığı için çakışma çözme ve geri alma turları azalır.
## Üretilebilir
hedef_tur: skill
tarif: 'wt' adlı bir skill yazılabilir. Girdi özellik adıdır. Adımlar: 1) `git rev-parse --show-toplevel` ile depoyu bul. 2) `git worktree add ../<repo>-<ad> -b <ad>` çalıştır. 3) Gerekli dosyaları (.env, bağımlılık kurulumu) kopyala veya kur. 4) Yeni dizin yolunu kullanıcıya bildir. 5) Bitiş komutunda `git worktree remove` ve `git worktree prune` ile temizle. Dal adı doğrulaması ve silmeden önce kaydedilmemiş değişiklik kontrolü eklenmeli. Claude Code'da `--worktree` bayrağı zaten varsa skill gereksiz olabilir. Önce bayrak denenmeli.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-7/panel.md → Ömer sütunu
## Özellikler
### Tek depoya bağlı çoklu çalışma dizini (git worktree add/list/remove/prune)
kaynak: https://git-scm.com/docs/git-worktree
### Claude Code ile özellik adına göre izole paralel oturum (videodaki anlatım)
kaynak: https://www.youtube.com/watch?v=jqoFP9QapXI
## Destek
- jqoFP9QapXI · 10:29 · Her özellik için izole dal/çalışma alanıyla paralel oturumlar. · kanıt: You just type in Claude dash work tree and then that feature name.
