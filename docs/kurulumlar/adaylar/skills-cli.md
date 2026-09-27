# skills-cli
ad: skills-cli
tur: CLI
video: Gg35_iQWx7g
repo: vercel-labs/skills
lisans: MIT
son_commit: 2026-09-18
arsiv: hayır
kaynak: yok
telemetri: açık
## Ne
GitHub/GitLab/Azure Repos repolarından tek komutla Agent Skill kurar, 79+ ajana (Claude Code dahil) sembol bağlantı/kopya yazar; kurmadan önizleme (`skills use`) ve kaldırma (`skills remove`) destekler.
## Kanıt
32621 yıldız · son commit 2026-09-18 · MIT · CLI (skillspector yok)
## Kurulum
- npm: skills@1.7.0
## İzinler
Proje/global agent dizinlerine dosya yazar (symlink/copy); kurulumda ve `--list`'te varsayılan olarak add-skill.vercel.sh'e telemetri + Snyk audit isteği gönderir; GITHUB_TOKEN/GH_TOKEN varsa özel repo erişiminde kullanır.
## Duman testi
- komut: npx skills --version
- cikis: 0
- desen: \d+\.\d+
## Geri alma
- npm: skills
## Köprü izni
- arac: skills
- altIzin: --version, list
## Önerilen katman
T2 (çalıştırılabilir her şey) — kurulan skill'lerin kendisi rastgele kod/talimat taşıyabilir, CLI'nin kendisi düşük riskli.
## Telemetri kapatma
- DISABLE_TELEMETRY=1 (veya DO_NOT_TRACK=1) env, hem telemetriyi hem Snyk audit isteğini kapatır
## Özellikler
### skill-kurma
ne: `npx skills add <repo> --skill <ad>` ile tek skill'i seçilen ajana kurar, skills-lock.json ile sürüm izler.
kurulum: npm paketi; ekstra bağımlılık yok, ilk çalıştırmada npx indirir.
lisans: MIT
etiket: -
karar: KUR
gerekce: MIT, Snyk audit'li, mevcut katalogda benzer tek-komut skill kurucu yok.
### gecici-kullan
ne: `npx skills use <repo> --skill <ad> --agent claude-code` kalıcı kurmadan geçici dizinde çalıştırıp prompt üretir.
kurulum: aynı paket, ayrı alt komut; kurulum yapmadan önizleme sağlar.
lisans: MIT
etiket: -
karar: KUR
gerekce: aynı artefakt, ek risk yok; kurulum öncesi inceleme için doğrudan kullanılabilir.
## Bağımsız kanıt
- https://snyk.io/blog/snyk-vercel-securing-agent-skill-ecosystem/ — Snyk, `npx skills add` ile kurulan her skill için kurulumdan önce otomatik güvenlik taraması yaptığını doğruluyor.
## İddia sınama
| iddia | kaynak | sonuç | not | kart |
|---|---|---|---|---|
| npx skills add ile anthropics/skills gibi repolardan tek komutla skill kurulur | README.md (vercel-labs/skills) | doğru | `--skill <ad>` ve `-a <agent>` seçenekleri gösterilen tek-komut akışıyla birebir eşleşiyor | - |
