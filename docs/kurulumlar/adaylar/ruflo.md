# Ruflo
ad: Ruflo
tur: plugin
video: L2JKgj7WzU4
repo: ruvnet/ruflo
lisans: MIT
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/ruvnet/ruflo
telemetri: bilinmiyor. README'nin gösterilen kısmında telemetri açıklaması yok; git klon/indirme sayıları GitHub/npm istatistiğine dayanıyor gibi görünüyor. Kurulum öncesi kaynak kodda (bin/cli.js, daemon, hook'lar) ağ çağrıları ve analytics elle denetlenmeli. Federasyon özelliği makineler arası iletişim açtığı için ağ trafiği var.
yildiz: bilinmiyor (README rozeti eski claude-flow reposuna bağlı; sayı doğrulanamadı)
alt_tur: araç
skillspector: atlandı (repo 561 MB, ön tarama yapılmadı)
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-7)
## Ne
Claude Code ve Codex için "ajan meta-harness" (eski adı Claude Flow). 100'e yakın uzman ajan (README: 98–100+), sürü (swarm) koordinasyonu, oturumlar arası kalıcı/öğrenen bellek, makineler arası federasyon ve güvenlik korkulukları ekler. İki yolla kurulur: hafif Claude Code plugin marketplace'i (35 plugin) veya tam CLI kurulumu (npx ruflo init).
## Mekanizma
Mimari (README diyagramı): Kullanıcı → Ruflo (CLI/MCP) → Router → Swarm → Ajanlar → Bellek → LLM sağlayıcıları, bir öğrenme döngüsüyle geri besleme. CLI kurulumu (`npx ruflo init`) çalışma alanına .claude/, .claude-flow/, CLAUDE.md, yardımcı betikler ve settings yazar; hooks sistemi görevleri otomatik yönlendirir, başarılı kalıpları öğrenir, ajanları arka planda koordine eder; MCP sunucusu (README: 314 MCP aracı, 26 CLI komutu, 60+ komut, 30 skill) ve daemon içerir. Plugin yolu (/plugin marketplace add ruvnet/ruflo) yalnızca slash komutları ve ajan tanımları ekler; yalnız ruflo-core kendi .mcp.json ile MCP sunucusu kaydeder, hook kurmaz. Bellek katmanı: agentdb/RuVector (vektör DB, hibrit arama, graf hop, RVF ile kaydet/yükle). Altta Rust tabanlı motor (Cargo.toml, crates/) ve Cognitum.One mimarisi var. Kodun kendisini incelemedim; bu özet README'ye dayanıyor.
## Kanıt
- MIT lisanslı → doğrulandı · README rozeti MIT; ağaçta LICENSE dosyası var (içeriğini okumadım).
- ~100 ajan kendini sürüler halinde organize ediyor, oturumlar arası paylaşılan bellek var (video) → sınanamadı · README bu iddiayı yineliyor (98 ajan, swarm, bellek) ama çalıştırıp sınamadım.
- 35 plugin → sınanamadı · README 'All 35 plugins' diyor; video 32 diyor. İkisi tutarsız, marketplace.json'ı saymadım.
- 8.1M+ ekosistem indirmesi, 106k git klonu → sınanamadı · Sadece README rozetleri ve data/clone-data.* dosyalarına bağlantı; bağımsız doğrulama yapılmadı.
- güvenlik ön taraması: atlandı (repo 561 MB)
## Kurulum
- Hafif yol (Claude Code içinde): /plugin marketplace add ruvnet/ruflo
- /plugin install ruflo-core@ruflo (ardından ihtiyaca göre ruflo-swarm@ruflo, ruflo-rag-memory@ruflo vb.)
- Tam yol: proje dizininde `npx ruflo init` (çalışma alanına .claude/, .claude-flow/, CLAUDE.md, hook ve settings yazar, MCP sunucusu + daemon kurar)
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Büyük, çok adımlı işleri paralel ajanlarla yürütmek, oturumlar arası bellek, otomatik görev yönlendirme, test üretimi, federasyon. Video de bunu ileri seviye kullanıcılar için olarak tanımlıyor.
## Maliyet/risk
Yüksek yüzey alanı: 314 MCP aracı, 98+ ajan, hook'lar, daemon, çalışma alanına çok sayıda dosya yazan init. Repo 561 MB; güvenlik ön taraması yapılamadı. Federasyon ve özerk döngü (autopilot) veri sızıntısı ve kontrolsüz maliyet riski taşır. README büyük iddialar içeriyor (8.1M indirme, öğrenen ajanlar) ve hiçbirini doğrulamadım. Repo içinde CLAUDE.local.md, settings.json.bak gibi geliştirici artıkları var. Mevcut CLAUDE.md ve ayarlarımızla çakışabilir. Önce izole bir projede, yalnızca ruflo-core plugin yoluyla denenmeli.
## Tasarruf
Token aracısı olarak konumlanmıyor; asıl amaç koordinasyon. README'de sayısal token tasarruf iddiası yok (gösterilen kısımda). Dolaylı etkiler: yönlendirici (router) görevi uygun ajana/modele gönderir, ruflo-ruvllm ile yerel LLM'e yönlendirme, kalıcı bellekle bağlamı yeniden anlatma ihtiyacının azalması. Çoklu ajan sürüsü genelde token tüketimini artırır; tasarruf doğrulanmadı.
## Üretilebilir
hedef_tur: skill
tarif: Tamamını kopyalamak mantıksız. Değerli ve küçük parça: görev türüne göre ajan/model yönlendirme ve oturumlar arası bellek. Yapım: (1) SKILL.md ile görev sınıflandırma tablosu (görev türü → alt ajan tanımı + model); (2) .claude/agents altında 5–8 odaklı alt ajan; (3) bellek için basit bir hook (SessionEnd'de özet yazar, SessionStart'ta ilgili notları bağlama ekler) veya mevcut bir bellek MCP'si. Sürü/federasyon gerekmez; Claude Code'un yerleşik alt ajan paralelliği yeter.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-7/panel.md → Ömer sütunu
## Özellikler
### Plugin marketplace: 35 plugin (core, swarm, autopilot, loop-workers, workflows, federation, agentdb, rag-memory, rvf, ruvector, knowledge-graph, intelligence, testgen vb.)
kaynak: https://github.com/ruvnet/ruflo
### Tam CLI kurulumu: 98 ajan, 60+ komut, 30 skill, MCP sunucusu, hooks, daemon
kaynak: https://github.com/ruvnet/ruflo
### Hook tabanlı otomatik görev yönlendirme ve başarılı kalıplardan öğrenme
kaynak: https://github.com/ruvnet/ruflo
### Federasyon: farklı makinelerdeki ajanlar güvenli iş birliği
kaynak: https://github.com/ruvnet/ruflo
### Bellek: vektör DB, hibrit arama, graf hop, çeşitlilik sıralaması, oturumlar arası kaydet/yükle
kaynak: https://github.com/ruvnet/ruflo
## Destek
- L2JKgj7WzU4 · 8:40 · Sürüler halinde kendini organize eden ~100 ajan, paylaşılan bellek, federe iletişim, 32 plugin; ileri seviye kullanıcılar için. · kanıt: 100 specialized agents that self-organize into swarms, shared memory across all the sessions
