# Mekanizma: caveman 1.3.4

Kaynak: kurulu npm paketi (README, dist/index.js, dist/learn-tui.js), `~/.caveman/bin/*.exe` dizgileri (koşulmadan), github.com/JuliusBrussee/caveman (README, LICENSING.md, docs/technical/{architecture,engine,proxy-and-providers,deploy,configuration,local-tools,stats-accounting,proxy-reliability}.md, skills/cavecrew/SKILL.md). Ölçümler: docs/denemeler/caveman-*-sonuc.md.

Lisans (LICENSING.md): npm CLI, skills/ (cavecrew dahil), SDK'lar MIT. Sıkıştırmayı yapan Go ikilileri (proxy, engine, mcp, shrink, browse, cavemem) BSL-1.1 (sürüm başına 4 yıl sonra Apache-2.0; üçüncü kişiye hizmet olarak sunmak ticari lisans ister). Bizde: fikir alınır, kod kopyalanmaz.

## proxy (`caveman start` / `caveman wrap <ajan>`)
- Ne: 127.0.0.1'de (varsayılan 8787; `CAVEMAN_LISTEN`) Anthropic/OpenAI uyumlu yerel vekil; `wrap` ajanın `ANTHROPIC_BASE_URL`'sini ona çevirir. Kip `record` (yalnız ölçüm, bayt korunur) ya da `compress` (`CAVEMAN_MODE`).
- Nasıl: istek gövdesindeki büyük araç sonuçlarını/blokları engine'e verir (aşağıda compress) → küçülen blok yerine kısa özet + kurtarma işaretçisi konur, aslı önce yerel CCR deposuna (`~/.caveman/ccr.db`) yazılır. Model gerekirse işaretçiyle aslını ister: akışsız API-anahtarlı istekte vekil kendi döngüsünde çözer; akışlı ve abonelik (Pro/Max OAuth) oturumunda aslını ajan tarafındaki caveman-mcp `Retrieve` aracıyla çeker. Ayrıca istem önbelleği kırılma noktalarını planlar ("cache-breakpoint planner", frontier). Dokunulmaz: sistem istemi, kullanıcı metni, küçülmeyen ya da ayrıştırılamayan her blok (özgün bayt geçer).
- Neden kazandırır: tekrarlı/hacimli araç çıktısı (log, JSON, arama sonucu) her turda yeniden gönderilir; bir kez sıkıştırılıp işaretçiyle taşınınca sonraki tüm turlarda girdi küçülür.
- Kazandırmadığı koşul: abonelik (Max/OAuth) oturumu, caveman-mcp ajanın KALICI MCP kaydında yoksa bayt bayt geçer — açılışta karar verilir; o çağrıya özel `--mcp-config` + `CAVEMAN_SUBSCRIPTION_COMPRESS=true` yetmedi (stats: saved 0; bilgi/caveman-max-gecis.md); paylaşımlı vekil OAuth taşıyamaz; kısa/tek atışlık oturum (sıkıştırılacak birikmiş araç çıktısı yok); zaten yoğun/küçük girdi; Headroom ile aynı işi yapar, zincirlenemez (yukarı akış adresi ayarlanamıyor). Ölçüm: docs/denemeler/caveman-proxy-sonuc.md.
- Bizde: Headroom (6767) aynı tekniği uyguluyor (sıkıştır + `headroom_retrieve` hash) → ZATEN VAR. Yeni fikir yok.

## compress (`caveman compress` · engine `Compress`)
- Ne: stdin'deki içeriği sıkıştırıp stdout'a yazar; sonunda `{content_type, tokens_before, tokens_after, ratio}` satırı.
- Nasıl: tür algıla → 15 kayıtlı sıkıştırıcıdan uygun olanı seç (JSON, log, kod, diff, arama sonucu, metin, HTML, tablo, yapılandırma, araç şeması, şema açıklamaları, TOON, erişilebilirlik ağacı, tekrar, terminal çıktısı) → dönüştür → "daha küçük ve geçerli mi" doğrula → kayıplıysa aslını CCR'a yaz, sonra değiştir. Ayrıştırma hatası, belirsizlik ya da küçülmeme → özgün bayt. Token sayımı çevrimdışı o200k_base (`basis: inferred`).
- Neden kazandırır: yapısal içerikte (JSON anahtar tekrarı, log satır tekrarı) anlamı koruyup biçim fazlasını atar; kayıp geri çağrılabilir kaldığı için agresif olabilir.
- Kazandırmadığı koşul: düz yazı/markdown. Divisima CLAUDE.md: 10981 → 10981 token, çıktı girdiyle bayt bayt aynı (docs/denemeler/caveman-compress-sonuc.md).
- Bizde: "küçülmüyorsa özgün bayt" + "önce aslını sakla" ilkesi Headroom/RTK'da var → ZATEN VAR. CLAUDE.md küçültme için bu araç uygun değil.

## shrink (`caveman tools shrink -- <komut>` · `tools compress catalog`)
- Ne: (a) komut çıktısını terminal/log sıkıştırıcısından geçirir; (b) MCP/OpenAI araç kataloglarının şemasını sıkıştırır, lint eder, geri çevirir (`caveman-shrink`).
- Nasıl: (a) engine'in terminal-output/log/tekrar sıkıştırıcıları: ilerleme çubukları, tekrarlı satırlar, ANSI, gürültü atılır; hata/özet satırları kalır. (b) şema açıklamaları ve gereksiz annotation alanları budanır; tam şema kurtarma için saklanır.
- Neden kazandırır: komut çıktısı ve araç şemaları her turda bağlama girer; ikisi de büyük ölçüde gürültü.
- Kazandırmadığı koşul: kısa çıktı; araç şemaları zaten ertelenmişse (Claude Code `ENABLE_TOOL_SEARCH` MCP şemalarını yalnız arandığında yükler).
- Bizde: (a) RTK hook'u komut çıktısını aynı biçimde süzüyor → ZATEN VAR (caveman-shrink denemesi hazır, koşulmadı). (b) araç araması açık → ZATEN VAR; skill açıklamaları için bkz. docs/uyarlamalar/skill-kullanim-sayaci.md.

## cavecrew (skills/cavecrew · MIT)
- Ne: vekil/engine değil; 3 alt ajan hazır ayarı (investigator salt-okur · builder 1-2 dosya düzenler · reviewer diff inceler).
- Nasıl: alt ajanın araç sonucu dönüşü caveman sıkıştırmasından geçip kısa haliyle ana ajana verilir; iş tanımı Explore/edit/review varsayılanlarıyla aynı.
- Neden kazandırır: alt ajan dönüşü ana bağlama kalıcı eklenir; her delege bir kez küçülünce ana oturumun geri kalanı boyunca kazanç sürer.
- Kazandırmadığı koşul: alt ajan az kullanılıyorsa; dönüş zaten kısaysa (bizim ajanlar "yalnız yol + ≤3-5 satır" döner).
- Bizde: docs/uyarlamalar/caveman-cavecrew.md (17'de yazıldı) aynı fikri taşıyor; ajanlarımız zaten kısa dönüş kuralında → ek uyarlama yok. learn: ölçülen bağlamın %18'i alt ajanlarda.

## convert (`caveman tools skills add … ` pixel)
- Ne: kurulu skill gövdelerini (SKILL.md) token-yoğun "pixel" biçime çevirir.
- Nasıl: yalnız yeni/değişen skill'ler; aslı `SKILL.orig.md` olarak bayt bayt saklanır (geri alma); dönüşüm kârlı değilse metin kalır (README duman testi: 35 skill'in 27'si çevrildi, 8'i metin kaldı; 32314 → 9537 tahmini token, −%70, inferred).
- Neden kazandırır: skill gövdesi yüklendiğinde büyük statik metin; yoğun gösterim aynı talimatı daha az tokenla taşır.
- Kazandırmadığı koşul: `--no-pixel`; skill az yükleniyorsa (gövde yalnız çağrıda girer, her tur giren yalnız description); talimat uyumu düşerse (bizde 20a caveman-oz terse talimat denemesi kaliteyi 0.21 düşürdü).
- Bizde: caveman-convert denemesi hazır (12 claude -p), bu dalgada koşulmadı. "kârlıysa çevir, aslını bayt bayt sakla" ilkesi `video dene` compress yolunda zaten var (kaynak baytı değişirse geri yazılır).

## learn (ek)
- Nasıl: yerel transkriptleri (`~/.claude`, `~/.codex`) tarar; sabit yük (config vergisi), kullanılmayan skill yükü, oturumlar arası tekrar kurulan bağlam blokları, alt ajan payı gibi "sink"leri tahmini token/gün ile sıralar. Salt-okur, ağsız.
- Bizde: docs/uyarlamalar/skill-kullanim-sayaci.md · docs/uyarlamalar/tekrar-baglam-tespiti.md (docs/denemeler/caveman-learn-sonuc.md).
