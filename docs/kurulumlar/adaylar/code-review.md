# Code Review
ad: Code Review
tur: plugin
video: k0gwr-vC2Z4
repo: anthropics/claude-code
lisans: bilinmiyor
son_commit: 2026-03-12
arsiv: bilinmiyor
kaynak: https://github.com/anthropics/claude-code/tree/main/plugins/code-review
telemetri: Plugin kendi telemetrisini eklemez. Prompt ve `gh` çağrılarından oluşur. Claude Code'un genel veri toplaması geçerlidir: kullanım verisi, kabul/ret bilgisi, konuşma verisi ve `/bug` geri bildirimi. Ayrıntılar Anthropic'in data-usage politikasında.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-10-03-short)
## Ne
Claude Code'un resmî reposundaki plugin. `/code-review [--comment]` komutuyla bir GitHub pull request'ini birden çok alt ajanla inceler. Yalnızca doğrulanmış, yüksek sinyalli bulguları raporlar. Rapor varsayılan olarak terminale yazılır. `--comment` verilirse PR'a yorum olarak gider.
## Mekanizma
Komut dosyası (commands/code-review.md) bir orkestrasyon istemidir. Adımlar şöyle. (1) Haiku ajanı PR'ın kapalı, taslak, önemsiz ya da daha önce Claude tarafından yorumlanmış olup olmadığına bakar. Öyleyse durur. (2) Haiku ajanı ilgili CLAUDE.md dosyalarının yollarını listeler. (3) Sonnet ajanı PR özetini çıkarır. (4) Paralel 4 ajan çalışır: 2 Sonnet ajanı CLAUDE.md uyumunu denetler, 2 Opus ajanı diff içindeki bariz hataları ve güvenlik/mantık sorunlarını arar. (5) Hata bulgularının her biri için ayrı doğrulayıcı alt ajanlar çalışır. Hatalar için Opus, CLAUDE.md ihlalleri için Sonnet kullanılır. (6) Doğrulanamayan bulgular elenir. (7) Özet terminale yazılır. (8–9) `--comment` varsa her sorun için `mcp__github_inline_comment__create_inline_comment` ile satır içi yorum açılır. Yorumda yalnızca sorunu tamamen çözen küçük düzeltmeler için "committable suggestion" bloğu bulunur. GitHub erişimi `gh` CLI üzerinden yapılır. Güncel komutta ayrı bir git blame/geçmiş ajanı yok.
## Kanıt
- Beş ajan kodu paralel inceler: hatalar, kurallar, git geçmişi. → çürütüldü · Güncel commands/code-review.md paralel 4 ajan tanımlıyor: 2 CLAUDE.md uyumu, 2 Opus hata ajanı. Ayrıca ön kontrol ve özet ajanları ile her bulgu için doğrulayıcı ajanlar var. Güncel komutta git geçmişi ajanı yok. README ise hâlâ 4 ajandan biri olarak git blame/geçmiş analizini sayıyor, yani README ile komut dosyası birbirini tutmuyor. Video 'beş ajan' diyor, depo 'dört' diyor. Videonun eski bir sürümü gösteriyor olması muhtemel.
- Hataları ve kuralları (CLAUDE.md) denetler. → doğrulandı · commands/code-review.md: Ajan 1 ve 2 CLAUDE.md uyumunu, Ajan 3 ve 4 hataları inceliyor.
- Güven puanıyla yanlış pozitifleri eler (README: eşik 80). → çürütüldü · README 0–100 puanlama ve 80 eşiğinden söz ediyor. Güncel komut dosyasında puanlama yok, bunun yerine doğrulayıcı alt ajanlar kullanılıyor.
- güvenlik ön taraması: koşmadı
## Kurulum
- Claude Code reposuyla birlikte gelen plugin'dir. README'ye göre komut Claude Code'da otomatik kullanılabilir. Gerekirse `/plugin` ile resmî marketplace'ten kurulabilir; bu yol doğrulanmadı.
- Gereksinimler: GitHub remote'lu git deposu, kurulu ve kimliği doğrulanmış `gh` CLI (`gh auth login`), isteğe bağlı CLAUDE.md dosyaları.
- Kullanım: PR dalındayken `/code-review` ya da `/code-review --comment`.
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Yanlış pozitifi azaltır: bulgular bağımsız doğrulayıcılardan geçer, linter'ın yakalayacağı sorunlar, önceden var olan sorunlar ve üslup tartışmaları dışarıda bırakılır. PR'ı CLAUDE.md kurallarına göre denetler. Yorumlarda tam SHA'lı kod bağlantıları kullanılır. Yerelde ya da CI'da çalıştırılabilir.
## Maliyet/risk
`--comment` ile PR'a herkese görünür yorum yazar. Yalnızca gerekli `gh` komutlarına izin verir (allowed-tools). Opus ajanları pahalıdır. Sonuçlar, yalnızca kesin hataları işaretleyecek şekilde ayarlandığı için gerçek sorunları kaçırabilir. Lisans özeldir, kodu kopyalayıp dağıtmak serbest olmayabilir. Çalışması için `gh` yetkisi gerekir.
## Tasarruf
Token tasarrufu aracı değil. Maliyeti artırır: 4 paralel inceleme ajanı ve her bulgu için ayrı doğrulayıcı çalışır. Ucuz işlerde (ön kontrol, dosya listeleme) Haiku kullanılması maliyeti bir miktar düşürür.
## Üretilebilir
hedef_tur: skill
tarif: Kendi `code-review` skill'imizi ya da slash komutumuzu yazabiliriz; yalnızca fikri ve yapıyı alırız, metni kopyalamayız (lisans özel). Tarif: (1) SKILL.md ön kontrol adımı olarak `gh pr view` ile PR durumunu (kapalı, taslak, daha önce yorumlanmış) denetler. (2) Değişen dosyaların yolundaki CLAUDE.md dosyalarını toplar. (3) Paralel alt ajanlar başlatır: CLAUDE.md uyumu ve diff içi hata/güvenlik. İstersek git blame/geçmiş ajanını da ekleriz, çünkü videonun anlattığı da buydu. (4) Her bulgu için ayrı doğrulayıcı alt ajan çalışır, doğrulanamayanlar elenir. (5) Çıktı varsayılan olarak terminale yazılır, `--comment` ile `gh pr comment` kullanılır. (6) 'Pre-existing, linter, üslup' yanlış-pozitif listesini istemin içine koyarız. `allowed-tools` içinde yalnızca gerekli `gh` komutlarına izin veririz.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-10-03-short/panel.md → Ömer sütunu
## Özellikler
### 4 paralel inceleme ajanı: 2 CLAUDE.md uyumu (Sonnet), 2 hata/mantık/güvenlik (Opus)
kaynak: https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/code-review/commands/code-review.md
### Her bulgu için bağımsız doğrulayıcı alt ajan; doğrulanmayanlar elenir
kaynak: https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/code-review/commands/code-review.md
### Kapalı, taslak, önemsiz ya da zaten yorumlanmış PR'ları atlar
kaynak: https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/code-review/commands/code-review.md
### Varsayılan çıktı terminale; `--comment` ile satır içi PR yorumları ve küçük düzeltmeler için committable suggestion
kaynak: https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/code-review/commands/code-review.md
### Yanlış pozitif listesi: önceden var olan sorunlar, linter konuları, üslup tartışmaları, lint-ignore ile susturulanlar
kaynak: https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/code-review/commands/code-review.md
### README'de güven puanı (0–100, eşik 80) ve git blame ajanı anlatılıyor; komut dosyasıyla uyumsuz
kaynak: https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/code-review/README.md
## Destek
- k0gwr-vC2Z4 · 0:22 · Beş ajan kodu paralel inceler: hatalar, kurallar, git geçmişi. · kanıt: Altyazı: beş ajan kodunuzu paralel kontrol ediyor; hatalar, kurallar, git geçmişi.
