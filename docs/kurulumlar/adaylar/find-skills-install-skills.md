# Find Skills (install skills)
ad: Find Skills (install skills)
tur: skill
video: vfLtsYbtJf0
repo: vercel-labs/skills
lisans: MIT
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/vercel-labs/skills
telemetri: Repoda src/telemetry.ts var, yani CLI telemetri gönderiyor. Neyin gönderildiğini ve kapatma yöntemini (DISABLE_TELEMETRY / DO_NOT_TRACK gibi ortam değişkenleri olabilir) doğrulayamadım: bilinmiyor. Kurulmadan önce src/telemetry.ts okunmalı.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-10-03-short)
## Ne
Vercel Labs'in açık "agent skills" ekosistemindeki `skills` CLI'ının (npx skills) yanında gelen `find-skills` skill'i (repoda skills/find-skills). Kullanıcı "şunu yapabilir miyim / bunun için skill var mı" dediğinde ajan skills.sh dizininde arama yapar, uygun skill'i bulur ve kurar. CLI, 80'e yakın ajanı destekler (Claude Code, Codex, Cursor, OpenCode vb.) ve kurulu ajanları algılar.
## Mekanizma
Skill, ajana `npx skills find [sorgu]` komutunu çalıştırmayı öğreten bir SKILL.md talimatıdır. CLI skills.sh dizininde arar, sonuçları listeler. Seçilen skill `npx skills add <owner/repo@skill>` ile kurulur. Kaynak GitHub, GitLab, Azure Repos, herhangi bir git URL'si veya yerel yol olabilir. Dosyalar ajanların skill dizinlerine varsayılan olarak symlink, `--copy` ile kopya olarak yazılır. `-g` küresel kurulum yapar. Ayrıca `check` ve `update` komutları güncellemeleri denetler. Kurulum kaydı için lock dosyaları (skill-lock, local-lock) kullanılır. `skills use` ile kurmadan geçici dizin üzerinden prompt üretilebilir. Özel repolar için Git kimlik bilgileri, gh CLI veya SSH kullanılır.
## Kanıt
- Skill, başka skill'ler arasında arama yapıp uygun olanı kurar → doğrulandı · Repoda skills/find-skills var. README'de `skills add` kurulum akışı ve skills.sh dizini anlatılıyor. Video karesinde `npx skills find [query]` ve `npx skills add <package>` komutları görülüyor.
- Kurulu ajanları otomatik algılar → doğrulandı · Repoda src/detect-agent.ts var. README, 75'ten fazla ajanın desteklendiğini yazıyor. Algılamanın ayrıntısını kodu okuyarak incelemedim.
- Lisans MIT → doğrulandı · README'deki lisans rozeti MIT gösteriyor, repoda LICENSE dosyası var.
- Telemetri yok / kapatılabilir → sınanamadı · src/telemetry.ts mevcut. İçeriği ve kapatma ayarı okunmadı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- npx skills add vercel-labs/skills --skill find-skills -g -a claude-code -y
- Arama: npx skills find <sorgu>
- Güncelleme: npx skills check && npx skills update
- Katalog: https://skills.sh/
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Doğru skill'i elle aramadan bulup tek komutla doğru ajan dizinine kurar. Birden çok ajanı tek kaynaktan yönetir, güncelleme denetimi yapar.
## Maliyet/risk
Üçüncü taraf skill'ler talimat içerdiği için prompt injection ve kötü niyetli skill riski taşır. Kurmadan önce `--list` ile içeriğe bakılmalı, kaynak güvenilir olmalı. skills.sh dizinindeki arama sonuçları bir güvenlik denetiminden geçmiş sayılmaz. Telemetri belirsiz. Ajanın `npx` ile ağdan kod çalıştırması gerekir. Video yalnızca 0:38'lik kısa bir tanıtım.
## Tasarruf
Token aracı değil. Dolaylı etkisi: skill'ler gerektiğinde yüklendiği için bağlama sürekli skill gömmek gerekmez. Ama ölçülmüş bir tasarruf iddiası yok.
## Üretilebilir
hedef_tur: skill
tarif: Zaten hazır olduğu için kendi sürümüne gerek yok. İstenirse kendi SKILL.md'miz şöyle yazılır: (1) description: 'Kullanıcı bir yetenek/skill aradığında kullan'. (2) Gövde: `npx skills find <sorgu>` çalıştır, sonuçları kullanıcıya göster. (3) Kurmadan önce `npx skills add <kaynak> --list` ile içeriği göster ve onay iste. (4) Onaydan sonra `-g -a claude-code` ile kur. Ek olarak SkillSpector benzeri bir tarama adımı eklenebilir.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-10-03-short/panel.md → Ömer sütunu
## Özellikler
### `npx skills find`, `add`, `check`, `update` komutları ve skills.sh dizini
kaynak: https://github.com/vercel-labs/skills
### GitHub, GitLab, Azure Repos, git URL ve yerel yoldan kurulum; özel repo desteği
kaynak: https://github.com/vercel-labs/skills
### Symlink veya --copy ile çoklu ajana kurulum, -g küresel mod, --all, -y (CI uyumlu)
kaynak: https://github.com/vercel-labs/skills
### `skills use` ile kurmadan tek skill için prompt üretme
kaynak: https://github.com/vercel-labs/skills
## Destek
- vfLtsYbtJf0 · 0:38 · Diğer skill'ler arasında arayıp amaca uyanı bulan ve doğru yere kuran skill; kurulu ajanları otomatik algılar. · kanıt: Karede 'Find Skills' README'si ve Skills CLI komutları görülüyor. (karede: 'Find Skills' sayfası: 'When to Use This Skill', 'What is the Skills CLI?' ('npx skills'); komutlar: npx skills find [query], npx skills add <package>, npx skills check, npx skills update; 'Browse skills at: https://skills.sh/'.)
