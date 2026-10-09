# Skills CLI (npx skills)
ad: Skills CLI (npx skills)
tur: CLI
video: vfLtsYbtJf0
repo: vercel-labs/skills
lisans: MIT
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/vercel-labs/skills
telemetri: Kaynakta src/telemetry.ts var, yani anonim kullanım telemetrisi muhtemelen gönderiliyor. Gönderilen alanları ve kapatma yöntemini doğrulayamadım. README'nin görebildiğim kısmında bu bilgi yok. Kullanmadan önce telemetry.ts incelenmeli.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-10-03-short)
## Ne
Açık ajan skill ekosistemi için paket yöneticisi CLI'ı (Vercel Labs). Skill arar, kurar, günceller ve kaldırır. OpenCode, Claude Code, Codex, Cursor ve 75 ek ajanı destekler.
## Mekanizma
`npx skills add <kaynak>` kaynağı çözümler. Kaynak GitHub kısayolu, GitHub/GitLab/Azure Repos URL'si, herhangi bir git URL'si veya yerel yol olabilir. Skill dosyalarını indirir ya da klonlar, SKILL.md frontmatter'ını okur ve dosyaları seçilen ajanların skill dizinine yerleştirir. Varsayılan olarak sembolik bağ kurar, `--copy` ile kopyalar. `-g` kullanıcı dizinine, aksi halde projeye kurar. Kurulumları lock dosyalarında (skill-lock, local-lock) izler. Diğer komutlar: update, remove, list, find, init, sync. `skills use` bir skill'i kurmadan geçici dizine yazıp prompt üretir. Özel repolarda git kimlik bilgileri, gh CLI veya SSH kullanılır. GITHUB_TOKEN ve GH_TOKEN isteğe bağlıdır.
## Kanıt
- Skills CLI, açık ajan skill ekosisteminin paket yöneticisidir; skill arar, kurar, günceller. → doğrulandı · Repo README'si 'The CLI for the open agent skills ecosystem' diyor. add, update, remove, list ve find komutlarına karşılık gelen kaynak dosyaları (add.ts, update.ts, remove.ts, list.ts, find.ts) ağaçta var.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- npx skills add vercel-labs/agent-skills
- npx skills add <owner/repo> --skill <ad> -a claude-code -g -y
- npx skills add <owner/repo> --list
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Tek komutla skill'leri onlarca ajana kurmak, güncellemek ve yönetmek mümkün olur. Ajanlar arası taşınabilirlik sağlar. Özel repo desteği ve CI uyumlu `-y` modu vardır. Kendi skill deposumuzu başka ajanlara dağıtmak için de kullanılabilir.
## Maliyet/risk
Üçüncü taraf repolardan skill kurmak, ajanın talimatlarına yetkisiz içerik sokabilir (prompt injection). Kurmadan önce `--list` ile ve içeriği okuyarak denetlemek gerekir. Telemetri ayrıntıları doğrulanmadı. Sembolik bağlar Windows'ta sorun çıkarabilir, bu durumda `--copy` kullanılabilir.
## Tasarruf
Token aracı değil. Dolaylı etkisi: yalnızca gereken skill'leri kurmaya izin verir ve `skills use` ile kurmadan tek skill kullanılabilir. Bu bağlam şişmesini azaltabilir.
## Üretilebilir
hedef_tur: yok
tarif: yok
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-10-03-short/panel.md → Ömer sütunu
## Özellikler
### Çok kaynaklı kurulum: GitHub kısayolu, GitLab, Azure Repos, git URL'si ve yerel yol
kaynak: https://github.com/vercel-labs/skills
### Yaklaşık 79 ajan desteği; -a ile hedef ajan seçimi, -g ile global kurulum
kaynak: https://github.com/vercel-labs/skills
### `skills use` ile kurmadan tek skill'den prompt üretme veya ajanı başlatma
kaynak: https://github.com/vercel-labs/skills
### Özel repo desteği (git kimlik bilgileri, gh CLI, SSH)
kaynak: https://github.com/vercel-labs/skills
## Destek
- vfLtsYbtJf0 · 0:38 · Açık ajan skill ekosisteminin paket yöneticisi: skill arar, kurar, günceller. · kanıt: Karede 'Skills CLI (npx skills) is the package manager for the open agent skills ecosystem'. (karede: Aynı Find Skills sayfasındaki 'Key commands' listesi.)
