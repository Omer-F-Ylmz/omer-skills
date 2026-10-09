# skill-creator
ad: skill-creator
tur: skill
video: BiEvvC_66AQ
repo: sandiiarov/skill-creator
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/sandiiarov/skill-creator
telemetri: bilinmiyor. README'de telemetriden söz edilmiyor, kaynak kodu da incelenmedi. Araç `npx -y` ile her çalıştığında npm'den paket indiriyor, ayrıca kullanıcının verdiği spec/MCP adreslerine ağ isteği atıyor.
yildiz: bilinmiyor
alt_tur: bilinmiyor
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-10-03-short)
## Ne
OpenAPI spec, GraphQL şeması ya da MCP sunucusu bağlantısından, sarmalayıcı betikleri, referans dosyaları ve kullanım notları olan hazır bir Agent Skill üreten araç. npm paketi @asnd/skill-creator olarak yayımlanıyor. Videoda geçen Anthropic'in resmi skill-creator'ı değil, aynı adı taşıyan üçüncü taraf bir repo.
## Mekanizma
`npx @asnd/skill-creator command install --agent <ajan> --scope global/project` komutu `/skill-creator` prompt komutunu ve `skill-creator-improvement` yardımcı skill'ini kuruyor. Kullanıcı `/skill-creator <spec/MCP/GraphQL bağlantısı>` yazınca ajan kaynağı araştırıyor ve `skill-creator generate` komutunu çalıştırıyor. Çıktı `SKILL.md`, `scripts/<ad>` sarmalayıcısı ve `references/` altında spec kopyasından oluşuyor. Sarmalayıcı içeride `npx -y @asnd/skill-creator` çağırıyor; `commands list`, `commands search`, `commands help` ve `run` alt komutları var. Üretilen skill'ler `~/.skill-creator/lock.json` dosyasında izleniyor. İyileştirme skill'i yalnızca bu dosyadaki skill'lerin `## Gotchas` bölümünü, kullanım sırasında öğrenilenlerle güncelliyor. Kod TypeScript ve Node ile yazılmış (src/openapi, src/graphql, src/mcp). Bunlar README ve dosya ağacından okundu; kaynak kodu satır satır incelenmedi.
## Kanıt
- Anthropic'in kendi skill'i; kendi skill'lerini oluşturup düzenlemeni sağlar. → çürütüldü · Aday repo sandiiarov/skill-creator, üçüncü taraf bir proje. README'ye göre OpenAPI, GraphQL ve MCP kaynaklarından skill üretiyor. Anthropic'e ait olduğuna dair bir işaret yok. Video muhtemelen Anthropic'in resmi skill-creator'ından söz ediyor; bu aday o değil.
- güvenlik ön taraması: koşmadı
## Kurulum
- Node.js ^22.22.2 // ^24.15.0 // >=26 gerekli
- npx @asnd/skill-creator command install --agent claude-code --scope project
- Ajanda şunu çalıştır: /skill-creator https://example.com/openapi.json
- MCP için: /skill-creator --mcp https://mcp.example.com/mcp --name ornek
- Desteklenen ajanlar: pi, claude-code, codex, cursor, opencode, gemini-cli, github-copilot, cline, windsurf
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
API, GraphQL ve MCP entegrasyonlarını tekrar kullanılabilir CLI skill'lerine çeviriyor. Skill'ler kullanım sırasında Gotchas notlarıyla kendini iyileştiriyor. Birçok ajan destekleniyor.
## Maliyet/risk
Lisans türü doğrulanmadı: LICENSE dosyası var ama içeriği okunmadı. Yıldız sayısı ve son commit tarihi alınmadı. Her çalıştırmada `npx -y` ile uzak paket çalıştırılıyor, bu bir tedarik zinciri riski. Ajan, spec ve MCP içeriğini işlerken içindeki talimatlardan etkilenebilir (prompt injection). İyileştirme skill'i skill dosyalarını kendiliğinden değiştiriyor. Video bulgusu bu repoyla eşleşmiyor: "Anthropic'in kendi skill'i" ifadesi Anthropic'in resmi skill-creator'ı için geçerli, bu aday için değil.
## Tasarruf
Token aracı olarak sunulmuyor, ama dolaylı bir tasarruf sağlıyor. API dokümanını her sohbete yapıştırmak yerine ajan `commands search` ve `commands help` ile yalnızca gereken komutu okuyor. Bu tasarrufun ölçümü yok.
## Üretilebilir
hedef_tur: skill
tarif: Ayrı bir araç gerekmez, ama istersek küçük bir skill yazabiliriz. Skill, ajana OpenAPI/MCP kaynağını okutup `SKILL.md`, ince bir `scripts/` sarmalayıcısı ve `references/` içinde spec kopyası olan bir klasör üretmesini söyler. Sarmalayıcıya list/search/help alt komutları ekleriz. Gotchas bölümünü güncelleme kuralını da skill metnine yazarız. Hazır araç yerine kendi sürümümüzü yapmak, `npx -y` ile uzak paket çalıştırma riskini ortadan kaldırır. Resmi Anthropic skill-creator ile karşılaştırmak da yararlı olur.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-10-03-short/panel.md → Ömer sütunu
## Özellikler
### OpenAPI, GraphQL veya MCP (http ve stdio) kaynağından skill üretimi
kaynak: https://github.com/sandiiarov/skill-creator
### Üretilen skill'de commands list/search/help ve run sarmalayıcı betiği
kaynak: https://github.com/sandiiarov/skill-creator
### lock.json ile izlenen skill'ler için skill-creator-improvement ile Gotchas güncelleme döngüsü
kaynak: https://github.com/sandiiarov/skill-creator
### 9 ajan için kurulum: claude-code, codex, cursor, gemini-cli ve diğerleri
kaynak: https://github.com/sandiiarov/skill-creator
## Destek
- BiEvvC_66AQ · 0:06 · Anthropic'in kendi skill'i; kendi skill'lerini oluşturup düzenlemeni sağlar. · kanıt: First is the skill creator from Anthropic itself, so you can build and edit your own.

## Güncellik (2026-10-04)
- kurulu d182ca4 ↔ upstream 2a40fd2 · son commit 2026-04-23
- yeni skill/komut/ajan: yok
