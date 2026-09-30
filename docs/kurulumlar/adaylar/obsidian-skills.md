# Obsidian skills
ad: Obsidian skills
tur: skill
video: L2JKgj7WzU4
repo: pablo-mano/obsidian-cli-skill
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/pablo-mano/obsidian-cli-skill
telemetri: Skill kendi başına telemetri göndermez (yalnızca talimat metni ve yerel CLI çağrıları). README'de telemetri beyanı yok; kodun tamamı incelenmedi. Obsidian Sync komutları kullanılırsa Obsidian'ın kendi hizmeti devreye girer.
yildiz: bilinmiyor
alt_tur: araç
skillspector: SkillSpector --no-llm: 2 HIGH/CRITICAL bulgu (ön tarama; ayrıntı incelenmedi)
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-7)
## Ne
Resmi Obsidian CLI (v1.12+) ile Obsidian kasalarını (vault) terminalden yönetmeyi ajana öğreten bir Claude Code skill'i/plugin'i. 130+ komutu kapsar: not okuma/oluşturma/ekleme, günlük notlar, arama, özellikler, etiketler, görevler, bağlantılar, şablonlar, eklentiler, sync, bases, geçmiş, geliştirici araçları.
## Mekanizma
SKILL.md, ajana komut sözdizimini ve kullanım kalıplarını öğretir. Ajan Bash ile `obsidian` ikilisini çalıştırır; CLI, çalışan Obsidian masaüstü uygulamasıyla IPC üzerinden konuşur. Obsidian'ın açık olması ve Ayarlar'dan CLI'nin etkinleştirilmesi gerekir. Skill, istek Obsidian ile ilgili olduğunda otomatik devreye girer; olmazsa `$obsidian-cli` öneki veya "use obsidian-cli" ile çağrılır. Repoda .claude-plugin/marketplace.json ve plugin.json bulunur, ayrıca eval/eval_set.json ile bir değerlendirme kümesi vardır. Cursor gibi diğer ajanlar için de SKILL.md uyumu var. Not: videodaki "Obsidian skills" adı (markdown, bases, JSON Canvas, defuddle) bu repodan farklı bir pakete (muhtemelen kepano/obsidian-skills) işaret edebilir; bu repo yalnızca CLI'yi kapsar.
## Kanıt
- Video: Obsidian markdown, bases, JSON Canvas, Obsidian CLI ve defuddle için yerel skill'ler sunuyor → sınanamadı · İncelenen repo yalnızca obsidian-cli skill'i içeriyor (README ve ağaç). Markdown, Canvas ve defuddle skill'leri bu repoda görünmüyor; muhtemelen başka bir repo (kepano/obsidian-skills), ama bu doğrulanmadı.
- Obsidian CLI komutlarını kapsıyor (130+ komut) → doğrulandı · README komut tablosunda Files, Daily, Search, Properties, Tags, Tasks, Links, Bases, Sync, Dev vb. alanlar listeli; 130+ sayısı yalnızca README beyanı, tek tek sayılmadı.
- güvenlik ön taraması: SkillSpector --no-llm HIGH/CRITICAL 2
## Kurulum
- Obsidian Desktop v1.12+ kur; Ayarlar → Command line interface → AÇIK yap; Obsidian'ı çalışır tut
- Claude Code içinde: /plugin marketplace add https://github.com/pablo-mano/Obsidian-CLI-skill
- /plugin install obsidian-cli
- Alternatif: git clone sonra `claude --plugin-dir ./Obsidian-CLI-skill`
- Windows'ta normal yetkili terminal kullan; Obsidian.exe yanına Obsidian.com yönlendirici dosyası gerekir
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Claude'un ikinci beyin (Obsidian) kasasını güvenilir komutlarla okuyup yazmasını sağlar. Ajan sözdizimini tahmin etmez; sürekli kullanılan not, günlük not ve arama işleri hızlanır.
## Maliyet/risk
Lisans belirsiz: README'den görülemedi, repo LICENSE dosyası ağaçta görünmüyor, bu yüzden yeniden dağıtım hakkı net değil. Ön tarama SkillSpector --no-llm ile 2 HIGH/CRITICAL bulgu verdi; ayrıntılar incelenmedi. Komutlar yıkıcı olabilir (delete, plugin:install, eval, sync:restore, plugins ve tema kurulumu); `eval` ile Obsidian içinde keyfi JS çalışır. Obsidian masaüstü uygulamasına bağımlıdır, headless kullanım kırılgandır. Videodaki adla repo uyuşmayabilir.
## Tasarruf
Token aracı değil. Dolaylı fayda: ajan dosyaları toptan okumak yerine `search`, `backlinks`, `outline`, `base:query` gibi hedefli komutlarla yalnızca gereken veriyi çeker; bu ölçülmedi.
## Üretilebilir
hedef_tur: skill
tarif: Kendi SKILL.md'mizi yaz: frontmatter'da name=obsidian-cli ve Obsidian kasası işlerini tetikleyecek bir description ver. Gövdede en sık kullanılan komutları (read, create, append, daily:append, search, backlinks, property:set, tasks, base:query) örnek sözdizimiyle ve bir güvenlik bölümüyle (delete/eval/plugin:install için onay iste) ekle. Önkoşul kontrolü olarak `obsidian version` çalıştır. Lisans net olmadığından metni kopyalama; resmi Obsidian CLI belgelerinden kendimiz yazalım.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-7/panel.md → Ömer sütunu
## Özellikler
### Not işlemleri: read, create, append, prepend, move, rename, delete
kaynak: https://github.com/pablo-mano/obsidian-cli-skill
### Günlük not, arama (JSON çıktı dahil), özellik, etiket, görev ve bağlantı sorguları
kaynak: https://github.com/pablo-mano/obsidian-cli-skill
### Bases (base:query/create), history, sync ve diff komutları
kaynak: https://github.com/pablo-mano/obsidian-cli-skill
### Geliştirici araçları: eval, dev:screenshot, dev:console, dev:dom
kaynak: https://github.com/pablo-mano/obsidian-cli-skill
### Claude Code marketplace/plugin desteği, Cursor SKILL.md uyumu, eval seti
kaynak: https://github.com/pablo-mano/obsidian-cli-skill
## Destek
- L2JKgj7WzU4 · 16:08 · Obsidian markdown, bases, JSON Canvas, Obsidian CLI ve defuddle için yerel skill'ler; ikinci beyni Claude'a bağlar. · kanıt: native skills for Obsidian flavored markdown, JSON Canvas, the Obsidian CLI, defuddle
