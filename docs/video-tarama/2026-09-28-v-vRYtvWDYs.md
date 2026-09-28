# v-vRYtvWDYs · Claude Code Token İsrafına Son Verdim
## Künye
Claude Code Token İsrafına Son Verdim · Muzaffer Kadir | mkdir dev · süre: 7:02 · dil: tr-orig · https://youtu.be/v-vRYtvWDYs

## Özet
Video, Claude Code'da token/maliyet israfını azaltmak için üç ana taktik anlatıyor: `settings.json` içinde `MAX_THINKING_TOKENS`, `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` ve `CLAUDE_CODE_SUBAGENT_MODEL` ayarları; iş türüne göre model seçimi (hafif işler Haiku, kritik/mimari kararlar Opus/Codex, orta işler Sonnet); ve context-mode adlı MCP ile araç çağrısı çıktılarının izole subprocess'lerde özetlenip ana context'e sadece özün taşınması. Bonus olarak kullanılmayan MCP'lerin kapatılması ve "alakalıysa compact, sıfırdan işse clear/yeni terminal" karar kuralı veriliyor. İddia: bu üç yöntemle bazı projelerde token kullanımı %70-88 azaltılmış. Context Rot grafiğiyle uzun session'larda maliyetin katlanarak arttığı gösteriliyor (50. mesajda ilk 10 mesajın maliyeti 40 kat). İçerik bir geliştirici araç/ayar rehberidir, görsel tasarım konusu yoktur.

## Bölümler
- 0:00 Giriş — token maliyeti farkındalığı, %88 azaltma iddiası
- 0:45 1- Claude Code settings.json — max thinking tokens, autocompact override, subagent model
- 2:18 2- Doğru Model Seçimi — Haiku/Sonnet/Opus iş türüne göre
- 3:37 3- context-mode mcp — izole subprocess ile özetlenmiş tool call sonuçları
- 5:02 Bonus Taktik — kullanılmayan MCP'leri kapatma
- 6:10 Bonus Taktik 2 — compact mı clear mı kararı
- 6:50 Sonuç — kapanış

## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| MAX_THINKING_TOKENS ayarı | yok | ipucu | settings.json env | modelin düşünme token bütçesini 32-35k'dan 10.000'e düşürerek limit tasarrufu sağlar | 0:45 | "Bunu ben 10.000'e düşürmemde herhangi bir zarar görmedim" |
| CLAUDE_AUTOCOMPACT_PCT_OVERRIDE ayarı | yok | ipucu | settings.json env | context'in %90 yerine %50'de özetlenmesini (compact) tetikler, şişmeyi erken önler | 1:47 | "%50'ye çekmemin herhangi bir dezavantajını görmedim" |
| CLAUDE_CODE_SUBAGENT_MODEL ayarı | yok | ipucu | settings.json env | sub agent'ların varsayılan modelini Haiku'ya sabitler (dosya arama/düzenleme gibi hafif işler için) | 1:47 | "Sub agent modelini Hiko olarak belirlemek" |
| iş türüne göre model seçimi | yok | iş akışı | anlatımdan | hafif işlerde Haiku, kritik bug/mimari kararda Opus/Codex, orta işlerde Sonnet kullanarak maliyeti düşürür | 2:18 | "Hafif işlerde Hayiku'yu kullanırken, kritik bug'da Opus gibi modelleri seçmek" |
| context-mode | yok | MCP | https://github.com/mksglu/context-mode | uzun dosya/log/tool call çıktılarını izole subprocess'te özetleyip ana context'e sadece özet döner, lokalde çalışır | 3:37 | "araç çağrılarını izole süreçlere hapseder, sadece ihtiyaç duyulan özet döner" |
| plugin marketplace add / plugin install (context-mode kurulumu) | yok | CLI | context-mode README'den, ekranda kurulum anlatılıyor | context-mode MCP'sini Claude Code'a marketplace üzerinden eklemek için kullanılan yerleşik komut akışı | 3:37 | "marketplace kuruluyor... plugin install diyerek bu plugin de ekleyelim" |
| claude mcp list | yok | CLI | yerleşik komut → CLI | bağlı/bağlanmamış MCP sunucularını ve pluginleri listeler | 5:32 | kare k00332_0.jpg'de "Manage MCP servers" çıktısı görülüyor |
| kullanılmayan MCP'leri kapatma | yok | ipucu | anlatımdan | her MCP'nin description/usage bilgisi context'e eklendiği için açık kalan MCP sayısı azaltılarak token tasarrufu sağlanır | 5:02 | "kullanmadığınız MCP'leri kapatabilirsiniz... sadece notebook MCP açıkmış" |
| compact/clear karar kuralı | yok | iş akışı | anlatımdan | devam eden iş alakalıysa compact, sıfırdan iş için clear/yeni terminal açılması önerilir | 6:10 | "alakalı bir şey de geliştiriyorsanız... compact deyip devam edin... sıfırdan bir şey geliştiriyorsanız... clear demek" |
| context rot (bağlam çürümesi) kavramı | yok | teknik | anlatımdan + grafik | uzun session'larda geçmiş mesajların tekrar tekrar işlenmesi nedeniyle token maliyetinin katlanarak arttığını açıklayan kavram | 6:06 | "50. mesajda, ilk 10 mesajın maliyetini 40 kez daha ödüyorsunuz" |
| everything-claude-code (repo) | yok | iş akışı | https://github.com/affaan-m/everything-claude-code | Linkler bölümünde paylaşılan ek kaynak repo; videoda içerik anlatılmıyor, yalnız linklendi | 0:00 | Linkler listesinde geçiyor, transkriptte açıklama yok |

## İddialar
| iddia | zaman | tür |
|---|---|---|
| Bazı senaryolarda token kullanımı ~%88 düşürüldü | 0:00 | sayısal |
| Max thinking tokens normalde 32-35k civarı; 10.000'e düşürmenin zararı görülmedi, limit süresi arttı | 0:45 | özellik |
| Autocompact varsayılan %90'da tetiklenir; %50'ye çekmenin dezavantajı görülmedi | 1:47 | özellik |
| 50. mesajda, ilk 10 mesajın maliyeti 40 kat fazla ödenir (context rot grafiği) | 6:06 | sayısal |
| İlk iki ayar (thinking tokens + model seçimi) tek başına ~%70, bazı projelerde %88'e varan düşüş sağladı | 3:19 | sayısal |
| context-mode en fazla Claude Code, Gemini CLI ve OpenCode ile uyumlu | 3:37 | karşılaştırma |

## Site/UI teknikleri
İçerik frontend/site yapımı değil (Claude Code ayarları/CLI/MCP konulu geliştirici rehberi); bu bölüm uygulanamaz.

## Kareden okunanlar
- 1:16 terminalde `nano .claude/settings.json` komutu
- 2:02 settings.json içinde `"MAX_THINKING_TOKENS": "10000"`, `"CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "50"`, `"CLAUDE_CODE_SUBAGENT_MODEL": "claude-haiku-4-5-20251001"`
- 4:07 context-mode GitHub README "Platform Compatibility" tablosu: Claude Code, Gemini CLI, VS Code Copilot, Cursor, OpenCode, OpenClaw, Codex CLI, Antigravity sütunları (MCP Server, Hook'lar, Slash Commands vb. satırlar)
- 4:50 "Mimari Kırılım" slaytı: Öncesi (Monolithic Context, ana process'e onlarca Tool Call) vs Sonrası (context-mode mimarisi: izole sandbox subprocess'ler, ana process'e yalnız "Özet Veri" akışı)
- 5:32 `/mcp` çıktısı: `notebooklm-mcp · connected`, `plugin:context-mode:context-mode · connected`, çeşitli `claude.ai` bağlantıları "needs authentication"
- 6:06 "Gizli Maliyet Tuzağı: Bağlam Çürümesi (Context Rot)" grafiği, x ekseni session mesaj 1-50, y ekseni işlenen token miktarı (log ölçek), "50. mesajda, ilk 10 mesajın maliyetini 40 kez daha ödüyorsunuz"

## Belirsizlikler
- everything-claude-code reposu yalnız "Linkler" bölümünde geçiyor, transkriptte hiç anlatılmadı; içeriği doğrulanmadı
- "CLAUDE_CODE_SUBAGENT_MODEL" değeri karede `claude-haiku-4-5-20251001` olarak okunuyor; bu değerin resmi/güncel model adı olup olmadığı doğrulanmadı
- Context Mod'un "Türk arkadaş Mert Köseoğlu yapmış" iddiası ASR'den; repo sahibi GitHub kullanıcı adı `mksglu`, isim eşleşmesi doğrulanmadı

## Atlanan segment oranı
0/11 (paket tam okuma)
