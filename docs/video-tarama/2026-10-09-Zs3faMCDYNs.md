# Turn Claude Code Into Your AI Operating System (4 Layers)
## Künye
Turn Claude Code Into Your AI Operating System (4 Layers) · Pav Rusovs | Automation Orbit · süre: 14:56 · en-orig · https://youtu.be/Zs3faMCDYNs · şema 2
motor: parti 2026-10-09-short-11 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 79813 tk · claude-haiku-5-5: claude-haiku-5-5 · 130263 tk
## Özet
Pav Rusovs, Claude Code üzerinde kurduğu kişisel yapay zekâ işletim sistemini MAPS çerçevesiyle (Memory, Agent, Pulse, Screen) anlatıyor. Önce 646 dosyalık canlı dashboard'u altı görünümüyle gezdiriyor. Sonra dört katmanı kuruluş sırasıyla işliyor. Memory: 40 satırlık CLAUDE.md haritası. Agent: aynı Claude aboneliğinin dizüstü ve Hostinger VPS'te çalışması; Tailscale ile özel ağ, Telegram'dan sesli not, taslak-yalnız kısıtlı ayarlar. Pulse: routines.yaml ile zamanlanmış rutinler. Screen: dosyaları okuyup hiçbir şey saklamayan dashboard. Haritalı ve haritasız aynı soru karşılaştırılıyor: 62 sn'ye karşı 30 sn, yaklaşık %40 daha az token. Aradaki sponsor bölümü kendi AI arama görünürlüğü denetimi (GEO, 47→62). Hermes Agent'ın neden kullanılmadığı da anlatılıyor. Sonuç: dashboard değerin yaklaşık %20'si, harita ve rutinler gerisi.
## Bölümler
- 0:00 AI işletim sistemim, canlı
- 0:49 Dashboard: tek beynin altı görünümü
- 3:12 MAPS çerçevesi ve 3 soru
- 4:32 Memory: Claude'a harita ver
- 6:55 Agent: tek abonelik, iki makine
- 9:03 Günün sponsoru: ben (GEO denetimi)
- 9:42 Pulse: ben uyurken çalışan rutinler
- 11:32 Screen: göster, saklama
- 12:35 Kanıt: haritalı ve haritasız
- 13:55 Tatil testi ve yorumum
- 14:41 Ücretsiz rehber ve sonraki video
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Code | yok | CLI | yok | Tüm sistemin çalıştığı ana ajan; hem dizüstünde hem VPS'te aynı abonelikle çalışıyor. | 6:55 | Diyagramda MacBook ve Hostinger VPS kutularında 'Claude Code' yazıyor (karede: Excalidraw diyagramı 'One subscription, 2 machines': MacBook ve Hostinger VPS içinde Claude Code kutuları) |
| MAPS | yok | iş akışı | https://github.com/pavrus117/ai-os-maps-guide | Memory, Agent, Pulse, Screen dört katmanlı çerçeve. | 3:00 | Slayt başlığı 'MAPS Memory · Agent · Pulse · Screen' (karede: Excalidraw'da dört kutu: Memory, Agent, Pulse, Screen ve altında üç soru) |
| CLAUDE.md | yok | teknik | yok | 40 satırlık ana yönlendirici dosya; olgu tutmaz, her alanın dosyasına işaret eder. | 5:34 | It's a very short file, just 40 lines, and it holds no facts (karede: Ekranda 'CLAUDE.md - the master router' dosya ağacı; sonraki karelerde dosya içeriği (Who, Areas, Rules, Model routing)) |
| Hostinger VPS | yok | CLI | yok | Hiç uyumayan kutu; ikinci Claude Code makinesi ve rutinlerin sunucusu. | 6:55 | In this case, it's Hostinger VPS (karede: Diyagramda 'Hostinger VPS · the box that never sleeps' kutusu) |
| Tailscale | yok | CLI | yok | Laptop, telefon ve sunucuyu özel ağa alan ücretsiz araç; sunucuyu internete kapatır. | 7:58 | Diyagramda 'Tailscale private network only my devices get in' (karede: Diyagramın ortasında Tailscale kutusu, kilit simgesi, 'only my devices get in') |
| Telegram | yok | CLI | yok | Sesli not ve sohbet botu arayüzü; sunucudaki Claude'a ulaşır. | 7:30 | Telegram penceresinde @pav_infobot ve sesli mesaj (karede: Telegram sohbeti: routines yanıtı, ses mesajı 'listening', 'What's on today?' cevabı) |
| GitHub | yok | CLI | yok | İki makine arasında klasör senkronu için özel depo. | 6:55 | Diyagram üstünde 'GitHub private repo', iki yana 'syncs every 5 min' (karede: Diyagramın tepesinde GitHub kutusu 'private repo') |
| Excalidraw | yok | CLI | yok | MAPS ve iki makine diyagramlarını çizdiği çizim aracı. | 3:00 | Ekranda Excalidraw+ ve 'Share' düğmesi (karede: Koyu temalı Excalidraw tuvali, araç çubuğu, MAPS slaytı) |
| Hermes Agent | yok | CLI | yok | Sunucuda denemeyi planladığı açık kaynak ajan; Anthropic kuralları yüzünden kullanmadı. | 9:42 | Hermes Agent açılış sayfası ve curl kurulum komutu (karede: Mavi 'THE AGENT THAT GROWS WITH YOU' sayfası, 'INSTALL VIA TERMINAL' kutusu) |
| OpenAI | yok | ipucu | yok | Aboneliğin üçüncü taraf ajanlarda kullanımına izin verebilir; yazar kontrol etmeyi öneriyor. | 9:46 | Konuşmacı karesinde OpenAI logosu (karede: Sol üstte OpenAI logosu, konuşmacı stüdyoda) |
| DeepSeek | yok | ipucu | yok | Dosyaların okunabileceği ucuz açık kaynak model örneği. | 13:56 | a cheaper open-source one like Deep Seek (karede: Ekranda 'deepseek' yazısı (OCR 13:56); konuşmacı karesi) |
| fal.ai | yok | MCP | yok | studio skill'inin kullandığı ödemeli görsel/video üretim toplayıcısı. | 2:06 | Links görünümünde fal.ai düğümü studio skill'ine bağlı (karede: fal.ai altıgen düğümü, altında studio skill düğümü, sağ altta studio kartı) |
| Kie.ai | yok | teknik | yok | studio skill'inde fal.ai'ye alternatif olarak anılan toplayıcı. | 2:16 | SKILL.md: 'The same recipe works on WaveSpeed or Kie.ai' (karede: studio SKILL.md içeriği açık, Providers bölümü) |
| WaveSpeed | yok | teknik | yok | studio skill'inde alternatif sağlayıcı olarak anılır. | 2:16 | SKILL.md: 'works on WaveSpeed or Kie.ai' (karede: studio SKILL.md Providers paragrafı) |
| studio | yok | skill | yok | Ödeme sınırı ve makbuzla görsel/video üreten kişisel skill. | 2:16 | '# studio — my image & video skill (pay-as-you-go...)' (karede: ~/.claude/skills/studio/SKILL.md modal penceresi) |
| routines.yaml | yok | teknik | yok | Tüm rutinlerin amaç, zaman ve makine bilgisini tutan liste; her 5 dakikada zamanlayıcı okur. | 9:52 | Editörde '# routines.yaml · every routine in the system' (karede: VS Code'da routines.yaml: heartbeat, morning-digest, outreach-pack, tracker-row, mail-scan) |
| VS Code | yok | CLI | yok | routines.yaml dosyasını açtığı editör; dashboard kartında da 'VS CODE' düğmesi var. | 9:52 | Restricted Mode uyarısı olan editör penceresi (karede: VS Code penceresi, 'Restricted Mode is intended for safe code browsing') |
| D3.js | yok | teknik | yok | Dashboard görselleştirmesi HTML, CSS, JavaScript ve D3 ile yapıldı (yazar yorumu). | açıklama | Yorumda: 'custom dashboard using HTML, CSS, JavaScript and D3' (karede: Karede doğrudan yok; dashboard'un 3D orbit ve links görünümleri) |
| AI Search Visibility Audit | yok | iş akışı | yok | Kendi sitesinde GEO skoru 47'den 62'ye çıkaran, yazarın sunduğu denetim hizmeti. | 9:03 | Sayfada 'AI Search Visibility Audit', skor 62/100 (karede: Automation Orbit denetim raporu, radar grafik, Overall GEO score 62) |
| Claude Opus 5 | yok | CLI | yok | Test oturumlarında kullanılan model (1M bağlam). | 12:16 | Başlıkta 'Opus 5 (1M context) · Claude Max' (karede: İki terminal bölmesi, Claude Code v2.1.276, Opus 5 (1M context)) |
| Fable 5.1 | yok | CLI | yok | Model yönlendirmesinde pahalı kararlar için (xhigh) ve karşılama mesajında anılan model. | 6:12 | Model routing tablosunda 'Fable · xhigh' (karede: CLAUDE.md model routing tablosu; 12:16 karesinde 'Fable 5.1 writes better code') |
| Claude Sonnet | yok | CLI | yok | Uygulama ve araştırma için alt ajan modeli (medium-high); dashboard'da SONNET · MEDIUM. | 6:12 | Tabloda 'Sonnet subagents · medium-high' (karede: CLAUDE.md Model routing tablosu satırı Sonnet subagents) |
| Claude Haiku | yok | CLI | yok | Sınıflandırma, özet ve cron işleri için düşük maliyetli model. | 6:14 | Tabloda 'Haiku · low (API key)' (karede: CLAUDE.md Model routing: Classification, digests, cron) |
| Claude Max | yok | ipucu | yok | Kullanılan abonelik planı; iki makinede aynı abonelik. | 12:16 | Başlıkta 'Opus 5 (1M context) · Claude Max' (karede: Claude Code başlık alanı, Claude Max yazısı) |
| /context | yok | ipucu | yok | Harcanan token'ı kategori bazında gösteren Claude Code komutu; karşılaştırmada kullanıldı. | 12:18 | Terminalde '/context' ve Context Usage tablosu (karede: İki bölmede Context Usage: Messages 27.7k ve 16.8k token) |
| Auto mode | yok | ipucu | https://code.claude.com/docs/en/permission-modes | Claude Code'un varsayılan izin modu; araç çağrılarını riske göre otomatik onaylar. | 12:16 | 'Auto mode is now Claude Code's default permission mode.' (karede: Karşılama mesajı ve alt çubukta 'auto mode on (shift+tab to cycle)') |
| brain-build | yok | skill | yok | Merkezdeki beyin grafiğini her gece yeniden üreten skill/rutin. | 10:43 | Brain build rebuilds the brain you saw in the center every night (karede: Skills deck'te '/brain-build' kartı (SCRIPT)) |
| vault-lint | yok | skill | yok | Bozuk notları denetleyen skill/rutin. | 10:43 | vault lint checks my notes for broken ones (karede: Skills deck'te '/vault-lint' kartı) |
| clean-up | yok | skill | yok | Mac'te belleği boşaltıp artık süreçleri kapatan skill. | 10:43 | frees up the memory on my Mac and closes the leftover processes (karede: Skills deck'te '/clean-up' kartı (SCRIPT)) |
| morning-digest | yok | iş akışı | yok | Gece olanları ve günün işlerini Telegram'a/takvime gönderen sabah özeti rutini. | 10:43 | the one I use the most is the morning digest (karede: routines.yaml'da morning-digest, host: vps) |
| Git | yok | teknik | yok | Makineler arası senkron için pull --rebase --autostash komutunun kullanıldığı sürüm kontrol aracı. | 6:12 | git pull —rebase --autostash origin main (karede: kanıttan) git pull —rebase --autostash origin main |
| Gmail | yok | teknik | yok | mail-scan rutininin salt okunur taradığı e-posta servisi; yanıt taslakları üretiyor, göndermiyor. | 7:30 | read-only Gmail/Calendar scan vs pipeline.md (karede: kanıttan) read-only Gmail/Calendar scan vs pipeline.md |
| Google Calendar | yok | teknik | yok | Sabah özetinin düşmesi anlatılan takvim servisi; mail-scan rutini de taranıyor. | 10:43 | It lands in my calendar before I'm awake · kanıt: yok |
| Apple Notes | yok | teknik | yok | notes-ingest rutininin vault/notes klasörüne aktardığı not kaynağı. | 7:30 | ingests up to 20 Apple notes into vault/notes (karede: kanıttan) ingests up to 20 Apple notes into vault/notes |
| Hafıza haritası için röportaj promptu (5:35'te anılan) | yok | prompt | yok | Yapay zekâ önce kullanıcıyı röportaj yapsın: tek soru, yanıt bekle. Sıra: işletme, haftalık beş iş, borçlu olunanlar, dosyaların yeri, unutulanlar. Belirsiz yanıta itiraz et, kayıtları interviews/ klasörüne yaz, 'stop' deyince hafıza haritası taslağı ve bilinmeyenleri çıkar. | açıklama | kaynak: açıklama |
| Harita testi: süre ve token karşılaştırması | yok | prompt | yok | LinkedIn gönderisinde hangi kelimeleri kullanamayacağım ve bu liste nerede yazılı? Aynı soru haritasız ve haritalı oturumda soruldu. | 12:16 | kaynak: kare |
| VPS botu canlı sesli not testi | yok | prompt | yok | Sesli mesajla Telegram botuna 'bugün ne var?' soruldu; ses metne çevrilip Claude'a gitti. | 7:58 | kaynak: kare |
| MAPS rehber promptları (içerik gösterilmedi) | yok | prompt | yok | Her katman için rehberde hazır prompt var; Claude Code'a yapıştırınca o katmanı kurmaya yönlendirir. | 4:13 | kaynak: altyazı |
## Açıklama bağlantıları
- https://www.patreon.com/pavrus/membership — Ücretli Patreon Builder üyeliği (hazır V1/V2 dashboard). · aday: hayır · Yazarın ücretli topluluğu; araç değil, erişim kısıtlı. · sınıf: diğer · erişilemez: ücretli topluluk
- https://github.com/pavrus117/ai-os-maps-guide — Ücretsiz MAPS rehberi ve katman promptları. · aday: evet (MAPS) · Videoda anlatılan, izleyicinin kullanacağı rehber; MAPS çerçevesi adayı. · sınıf: diğer
- https://ko-fi.com/pavrus — Yazarın bağış sayfası. · aday: hayır · Bağış sayfası; videoda kullanılan araç değil. · sınıf: diğer
- https://www.hostinger.com/cart?product=vps%3Avps_kvm_1&period=24&referral_type=cart_link&REFERRALCODE=KYMHOSTIN3D1&referral_id=01a0c876-08f0-73c3-bce5-9309427ddc26 — Hostinger VPS KVM 1 sepet bağlantısı. · aday: evet (Hostinger VPS) · Alan adı videoda kullanılan Hostinger VPS'i adlandırıyor; referral kodu var. · sınıf: affiliate
- https://www.hostinger.com/cart?product=vps%3Avps_kvm_2&period=24&referral_type=cart_link&REFERRALCODE=KYMHOSTIN3D1&referral_id=01a0c876-3bd1-71db-a95c-413e34c5f843 — Hostinger VPS KVM 2 sepet bağlantısı. · aday: evet (Hostinger VPS) · Hostinger VPS'i adlandırıyor; referral kodu var. · sınıf: affiliate
- https://www.hostinger.com/cart?product=vps%3Avps_kvm_4&period=24&referral_type=cart_link&REFERRALCODE=KYMHOSTIN3D1&referral_id=01a0c876-5834-705d-bd87-2676ab5186c2 — Hostinger VPS KVM 4 sepet bağlantısı. · aday: evet (Hostinger VPS) · Hostinger VPS'i adlandırıyor; referral kodu var. · sınıf: affiliate
- https://www.hostinger.com/cart?product=vps%3Avps_kvm_8&period=24&referral_type=cart_link&REFERRALCODE=KYMHOSTIN3D1&referral_id=01a0c876-741d-7284-a934-17abfadddcc1 — Hostinger VPS KVM 8 sepet bağlantısı. · aday: evet (Hostinger VPS) · Hostinger VPS'i adlandırıyor; referral kodu var. · sınıf: affiliate
- https://tailscale.com — Tailscale resmi sitesi. · aday: evet (Tailscale) · Videoda kullanılan özel ağ aracı. · sınıf: diğer
- https://audit.automationorbit.com/?utm_source=youtube&utm_medium=video&utm_campaign=020-ai-os — Yazarın AI Search Visibility Audit hizmeti. · aday: evet (AI Search Visibility Audit) · Videoda gösterilen ve anlatılan denetim hizmeti; yalnızca utm izleme parametresi var. · sınıf: diğer
- https://calendly.com/rusovs-p/30min — 30 dakikalık görüşme rezervasyonu. · aday: hayır · Randevu bağlantısı; videoda anlatılan araç değil. · sınıf: diğer
- https://www.linkedin.com/in/pav-rusovs — Yazarın LinkedIn profili. · aday: hayır · Sosyal profil. · sınıf: diğer
- https://www.youtube.com/@pavrusovs — Yazarın YouTube kanalı. · aday: hayır · Kanal sayfası. · sınıf: diğer
- https://www.youtube.com/watch?v=8NSyI-npJCU&t=981s — Açıklamada ilham olarak verilen başka video. · aday: hayır · İlham/referans videosu. · sınıf: diğer
- https://ko-fi.com (sayfa https://ko-fi.com/pavrus) — Ko-fi ana sayfası. · aday: hayır · Bağış platformu; videoda kullanılmıyor. · sınıf: diğer
- https://fal.ai/docs/documentation/compute — fal.ai compute dokümanı. · aday: evet (fal.ai) · Alan adı videoda kullanılan fal.ai'yi adlandırıyor. · sınıf: diğer
- https://fal.ai/docs/documentation/serverless — fal.ai serverless dokümanı. · aday: evet (fal.ai) · fal.ai aracını adlandırıyor. · sınıf: diğer
- https://fal.ai/docs/documentation — fal.ai dokümantasyonu. · aday: evet (fal.ai) · fal.ai aracını adlandırıyor. · sınıf: diğer
- https://docs.kie.ai/ai-agent/overview — Kie.ai ajan genel bakış dokümanı. · aday: evet (Kie.ai) · Videoda SKILL.md'de anılan Kie.ai'yi adlandırıyor. · sınıf: diğer
- https://docs.kie.ai — Kie.ai dokümanları. · aday: evet (Kie.ai) · Kie.ai aracını adlandırıyor. · sınıf: diğer
- https://www.youtube.com/watch?v=Zs3faMCDYNs — Videonun kendisi. · aday: hayır · Aynı videonun sayfası; araç değil. · sınıf: diğer
- https://audit.automationorbit.com — Denetim hizmeti ana sayfası. · aday: evet (AI Search Visibility Audit) · AI Search Visibility Audit hizmeti. · sınıf: diğer
- https://www.youtube.com/watch?v=Zs3faMCDYNs&t=546s — Aynı videonun 9:06 zaman damgalı bağlantısı. · aday: hayır · Videonun kendisi. · sınıf: diğer
- https://tavaduri-preview.netlify.app — Önizleme demo sitesi. · aday: hayır · Demo/referans site. · sınıf: diğer
- https://recombatumi.com — Örnek müşteri/demo sitesi. · aday: hayır · Demo/referans site. · sınıf: diğer
- https://ajara-palace-preview.netlify.app — Önizleme demo sitesi. · aday: hayır · Demo/referans site. · sınıf: diğer
- https://code.claude.com/docs/llms.txt — Claude Code doküman indeksi. · aday: evet (Claude Code) · Alan adı videoda kullanılan Claude Code'u adlandırıyor. · sınıf: diğer
- https://code.claude.com/docs/en/permissions#manage-permissions — Claude Code izinler dokümanı. · aday: evet (Claude Code) · Claude Code dokümanı. · sınıf: diğer
- https://code.claude.com/docs/en/tools-reference#endconversation-tool-behavior — Araç referansı. · aday: evet (Claude Code) · Claude Code dokümanı. · sınıf: diğer
- https://code.claude.com/docs/en/mcp#organization-controls-on-connector-tools — MCP kurumsal kontroller. · aday: evet (Claude Code) · Claude Code dokümanı. · sınıf: diğer
- https://code.claude.com/docs/en/mcp#require-approval-for-a-specific-tool — MCP araç onayı. · aday: evet (Claude Code) · Claude Code dokümanı. · sınıf: diğer
- https://code.claude.com/docs/en/settings-reference#permissions-blockreadsoutsideworkingdirectories — Ayar referansı. · aday: evet (Claude Code) · Claude Code dokümanı. · sınıf: diğer
- https://code.claude.com/docs/en/sandboxing#the-unsandboxed-retry-escape-hatch — Sandbox dışı yeniden deneme. · aday: evet (Claude Code) · Claude Code dokümanı. · sınıf: diğer
- https://code.claude.com/docs/en/sandboxing — Sandbox dokümanı. · aday: evet (Claude Code) · Claude Code dokümanı. · sınıf: diğer
- https://code.claude.com/docs/en/sandbox-environments — Sandbox ortamları. · aday: evet (Claude Code) · Claude Code dokümanı. · sınıf: diğer
- https://code.claude.com/docs/en/sandboxing#sandbox-modes — Sandbox modları. · aday: evet (Claude Code) · Claude Code dokümanı. · sınıf: diğer
- https://code.claude.com/docs/en/settings-reference#sandbox-enabled — sandbox.enabled ayarı. · aday: evet (Claude Code) · Claude Code dokümanı. · sınıf: diğer
- https://code.claude.com/docs/en/claude-code-on-the-web — Web üzerinde Claude Code. · aday: evet (Claude Code) · Claude Code dokümanı. · sınıf: diğer
- https://code.claude.com/docs/en/sandbox-environments#sandbox-runtime — Sandbox runtime. · aday: evet (Claude Code) · Claude Code dokümanı. · sınıf: diğer
- https://code.claude.com/docs/en/sandboxing#how-sandboxing-relates-to-permissions-and-permission-modes — Sandbox ve izin modları ilişkisi. · aday: evet (Claude Code) · Claude Code dokümanı. · sınıf: diğer
- https://code.claude.com/docs/en/sandbox-environments#how-isolation-relates-to-permission-modes — İzolasyon ve izin modları. · aday: evet (Claude Code) · Claude Code dokümanı. · sınıf: diğer
- https://code.claude.com/docs/en/settings#where-settings-live — Ayarların yeri. · aday: evet (Claude Code) · Claude Code dokümanı. · sınıf: diğer
- https://code.claude.com/docs/en/sessions#permission-mode-on-resume — Oturum devamında izin modu. · aday: evet (Claude Code) · Claude Code dokümanı. · sınıf: diğer
- https://code.claude.com/docs/en/agent-sdk/permissions#permission-modes — Agent SDK izin modları. · aday: evet (Claude Code) · Claude Code dokümanı; alan adı Claude Code'u adlandırıyor. · sınıf: diğer
- https://code.claude.com/docs/en/env-vars#features-that-need-feature-flag-fetching — Ortam değişkenleri. · aday: evet (Claude Code) · Claude Code dokümanı. · sınıf: diğer
- https://code.claude.com/docs/en/hipaa-setup#check-how-developers-sign-in-and-connect — HIPAA kurulumu. · aday: evet (Claude Code) · Claude Code dokümanı. · sınıf: diğer
- https://code.claude.com/docs/en/vs-code — VS Code eklentisi dokümanı. · aday: evet (Claude Code) · Claude Code ve VS Code'u adlandırıyor. · sınıf: diğer
- https://code.claude.com/docs/en/env-vars#first-session-after-an-install-or-upgrade — Kurulum sonrası ilk oturum. · aday: evet (Claude Code) · Claude Code dokümanı. · sınıf: diğer
- https://code.claude.com/docs/en/settings#settings-precedence — Ayar önceliği. · aday: evet (Claude Code) · Claude Code dokümanı. · sınıf: diğer
- https://code.claude.com/docs/en/managed-settings — Yönetilen ayarlar. · aday: evet (Claude Code) · Claude Code dokümanı. · sınıf: diğer
- https://code.claude.com/docs/en/hipaa-setup — HIPAA kurulum ana sayfası. · aday: evet (Claude Code) · Claude Code dokümanı. · sınıf: diğer
- https://code.claude.com/docs/en/settings-reference#disableautomode — disableAutoMode ayarı. · aday: evet (Auto mode) · Claude Code dokümanı; Auto mode ile ilgili. · sınıf: diğer
- https://code.claude.com/docs/en/settings-reference#permissions-disablebypasspermissionsmode — disableBypassPermissionsMode ayarı. · aday: evet (Claude Code) · Claude Code dokümanı. · sınıf: diğer
- https://code.claude.com/docs/en/hipaa-setup#update-claude-code-and-claude-desktop — Claude Code güncelleme. · aday: evet (Claude Code) · Claude Code dokümanı. · sınıf: diğer
- https://code.claude.com/docs/en/settings-reference#permissions-defaultmode — defaultMode ayarı. · aday: evet (Claude Code) · Claude Code dokümanı. · sınıf: diğer
- https://code.claude.com/docs/en/tools-reference#powershell-tool — PowerShell aracı referansı. · aday: evet (Claude Code) · Claude Code dokümanı. · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Halkalı radyal düzen (Rings view / radial layout) | Ortada CLAUDE.md altıgeni, çevresinde Skills, Memory, Routines, Applications halkaları ve alan renkli noktalar. (karede: Koyu arka planda PAV OS dashboard'u, ortada CLAUDE.MD altıgeni ve eşmerkezli halkalar) | 0:48 | kare |
| Altı görünüm sekmesi (Tab navigation / view switcher) | RINGS, CIRCLE, AREAS, LINKS, TIMELINE, 3D ORBIT sekmeleri; aktif sekme turuncu. (karede: Üstte VIEW etiketi ve altı sekme, LINKS turuncu vurgulu) | 1:42 | kare |
| Kuvvet yönlendirmeli ağ grafiği (Force-directed graph) | Links görünümünde dosya, skill ve rutinler arası bağlantılar. (karede: Kümelenmiş noktalar, çizgilerle bağlı düğümler, merkezde CLAUDE.MD) | 1:42 | kare |
| 3B yörünge animasyonu (3D orbit / perspective projection) | Dosyalar ve ilişkiler 3B uzayda dönen küre olarak. (karede: Elips yörüngeli nokta bulutu, merkezde CLAUDE.MD, '3D ORBIT' sekmesi aktif) | 1:48 | kare |
| Alan filtre çipleri (Filter chips) | all areas, business, clients, career, content, youtube, personal, system çipleri; seçilen alan vurgulanır, gerisi kararır. (karede: Business çipi seçili; diğer alanlar soluk, sayılar çiplerin yanında) | 1:58 | kare |
| Odak karartma ve vurgulama (Dim and highlight / focus mode) | Seçilmeyen düğümler solar, seçili alan öne çıkar. (karede: Business düğümü büyük ve mavi, dosya adları etrafında dizili) | 1:58 | kare |
| Yan detay kartı (Side detail card) | OPEN, COPY PATH, VS CODE, FLY TO düğmeli kart; yol ve bağlı dosyalar. (karede: Sağ altta 'studio skill' kartı, yol ~/.claude/skills/studio/SKILL.md) | 2:06 | kare |
| Arama kutusu (Search / command palette) | Yazarak dosya, skill ve rutin arama; 'studio' örneği. (karede: Üstte 'Search' düğmesi; OCR'da 'TYPE TO' arama ipucu) | 2:04 | kare |
| Modal dosya görüntüleyici (Modal overlay) | SKILL.md içeriğini sayfa içinde açan pencere. (karede: Dashboard üstünde kapatma 'x' düğmeli SKILL.md metin penceresi) | 2:16 | kare |
| Tam ekran düğmesi (Fullscreen toggle) | Beyni tam ekran açar; 'full' düğmesi. (karede: 'Open the second brain full screen' ipucu, 'full' düğmesi) | 2:40 | kare |
| Üç sütunlu kontrol paneli (Three-column dashboard layout) | Sol Today, ortada beyin, sağda Needs Pav ve Routines. (karede: Sol: saat ve sonraki 14 gün; orta: grafik; sağ: Needs Pav 3 ve Routines) | 0:48 | kare |
| Canlı saat ve 90 günlük ızgara (Live clock / heatmap grid) | Londra saati ve gate review geri sayımı. (karede: Sol üstte 12:56 saat, 'Gate review Tue 06.10 · in 18 d') | 0:48 | kare |
| Durum rozetli rutin tablosu (Status badges table) | Rutin adı, MAC/VPS etiketi, süre ve yeşil FIRED/NEXT durumu. (karede: ROUTINES listesi, outreach-pack MAC 95 s FIRED, 5/12 fired today) | 0:18 | kare |
| Skills deck kart ızgarası (Card grid with run buttons) | Turuncu oynat düğmeli /outreach-pack, /vault-lint, /brain-build kartları. (karede: SKILLS DECK başlığı altında altı kart, SCRIPT/SONNET etiketleri) | 3:28 | kare |
| İlerleme çubukları (Progress bars) | Business pulse: invites, posts, apps, video. (karede: BUSINESS PULSE altında dört turuncu çubuk ve sayılar) | 3:28 | kare |
| Koyu tema, turuncu vurgu (Dark theme / accent color) | Mono yazı, koyu zemin, turuncu aktif öğeler. (karede: PAV OS Agentic OS başlığı, turuncu 'Agentic OS') | 0:32 | kare |
| Radar grafiği ve skor kartları (Radar chart / score cards) | GEO denetim sayfasında önce-sonra radar ve metrik kartları. (karede: AI-VISIBILITY PROFILE radar, Overall GEO score 62/100, alt kartlar) | 9:00 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| curl -fsSL https://hermes-agent.nousresearch.com/install.sh / bash | Hermes Agent'ı macOS/Linux'a kurar (yalnızca gösterildi, yazar kullanmadı). (karede: Hermes sayfasında INSTALL VIA TERMINAL kutusu, macOS sekmesi, curl komutu) | 9:26 | kare |
| /context | Claude Code oturumunda token kullanımını kategori bazında gösterir. (karede: İki bölmede '/context' ve Context Usage tablosu) | 12:18 | kare |
| /model | Claude Code'da modeli değiştirir. (karede: Karşılama metni 'Switch anytime with /model.') | 12:16 | kare |
| /status | Claude Code durumunu gösterir. (karede: Karşılama mesajında '+2 more · /status') | 12:16 | kare |
| /calibrate | Dersleri hafızaya, CLAUDE.md'ye veya skill'e tek yere işler. (karede: CLAUDE.md kurallarında 'Lessons go through /calibrate into memory') | 6:12 | kare |
| git pull --rebase --autostash origin main | Her commit'ten önce depoyu çekip yerel değişiklikleri korur (VPS sync). (karede: CLAUDE.md kuralı: 'git pull --rebase --autostash origin main' before every commit) | 6:12 | kare |
| /mcp | Bağlı MCP araçlarını listeler; araçlar isteğe bağlı yüklenir. (karede: Bağlam çıktısında 'MCP tools · /mcp (loaded on-demand)' satırı görünüyor.) | 12:18 | kare |
| /skills | Yüklü skill'leri listeler. (karede: Sağ oturumda 'Skills · /skills' satırı ve skill sayısı görünüyor.) | 12:24 | kare |
| /memory | Yüklü bellek dosyalarını gösterir. (karede: Sağ oturumun bağlam çıktısında 'Memory files · /memory' satırı görünüyor.) | 13:04 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Haritasız oturum 1 dk 2 sn, haritalı 30 sn sürdü; yaklaşık yarı süre. | 12:16 | sayısal |
| Mesaj token'ı 28k'ya karşı 17k; yaklaşık %40 daha az okuma. | 12:35 | sayısal |
| Anthropic kuralları kendi Claude aboneliğini üçüncü taraf ajanda kullanmaya izin vermiyor; Claude Code sunucuda çalışır. | 9:42 | özellik |
| CLAUDE.md yalnızca 40 satır; her dosyaya iki adımda ulaşılır. | 5:34 | sayısal |
| Klasör iki makine arasında her 5 dakikada iki yönlü senkronlanır. | 6:55 | özellik |
| Sunucudaki Claude tek ayar dosyasıyla kısıtlı; e-posta taslağı yazar ama gönderemez. | 7:58 | özellik |
| Kendi sitesinde GEO skoru 47'den aynı gün 62'ye çıktı. | 9:03 | sayısal |
| Dashboard değerin yaklaşık %20'si; önce harita, ekran sonra. | 13:55 | öneri |
| Dosyalar düz metin olduğu için Claude, OpenAI veya DeepSeek gibi her model okuyabilir. | 13:55 | özellik |
| Sistem 646 dosya, 869 bağlantı, 246 çalıştırma gösteriyor. | 0:00 | sayısal |
| Rutin zamanlayıcı her makinede 5 dakikada bir listeyi kontrol eder; hata sınırı vardır. | 9:42 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Claude Code | Claude Code | Tüm sistem Claude Code üzerinde çalışıyor |
| kare 0:59 | CLAUDE.md | CLAUDE.md | CLAUDE.md - the master router |
| konuşma 3:12 | MAPS çerçevesi | MAPS | I call it maps: memory, agent, pulse, screen |
| kare 3:00 | Excalidraw | Excalidraw | Excalidraw+ ve Share düğmesi |
| konuşma 6:55 | Hostinger VPS | Hostinger VPS | In this case, it's Hostinger VPS |
| konuşma 7:58 | Tailscale | Tailscale | I use a free tool called Tailscale |
| kare 0:18 | Telegram | Telegram | voice note → text → Claude → reply |
| kare 6:55 | GitHub private repo | GitHub | Diyagramda GitHub private repo |
| konuşma 9:42 | Hermes Agent | Hermes Agent | my first plan was to run Hermes on that server |
| konuşma 9:46 | OpenAI | OpenAI | If you are using OpenAI, for example |
| konuşma 13:55 | DeepSeek | DeepSeek | a cheaper open-source one like Deep Seek |
| kare 2:06 | fal.ai | fal.ai | fal.ai düğümü studio skill'e bağlı |
| kare 2:16 | Kie.ai | Kie.ai | works on WaveSpeed or Kie.ai |
| kare 2:16 | WaveSpeed | WaveSpeed | SKILL.md Providers satırı |
| kare 2:16 | studio skill | studio | studio — my image & video skill |
| kare 9:52 | routines.yaml | routines.yaml | routines.yaml · every routine in the system |
| kare 9:52 | VS Code | VS Code | Restricted Mode uyarılı editör |
| yorum | D3.js, HTML, CSS, JavaScript | D3.js | custom dashboard using HTML, CSS, JavaScript and D3 |
| konuşma 9:03 | AI Search Visibility Audit | AI Search Visibility Audit | one of the things we build for businesses |
| konuşma 9:03 | ChatGPT, Perplexity, Gemini | aday değil: başka adayın parçası (AI Search Visibility Audit) | Denetimin ölçtüğü AI arama platformları olarak sayıldı |
| kare 8:48 | Google AI Overviews | aday değil: başka adayın parçası (AI Search Visibility Audit) | Denetim sayfası metninde geçiyor |
| kare 12:16 | Claude Opus 5 | Claude Opus 5 | Opus 5 (1M context) · Claude Max |
| kare 6:12 | Fable 5.1 | Fable 5.1 | Fable · xhigh |
| kare 6:12 | Claude Sonnet | Claude Sonnet | Sonnet subagents · medium-high |
| kare 6:14 | Claude Haiku | Claude Haiku | Haiku · low (API key) |
| kare 12:16 | Claude Max | Claude Max | Opus 5 (1M context) · Claude Max |
| kare 12:18 | /context | /context | Context Usage tablosu |
| kare 12:16 | Auto mode | Auto mode | Auto mode is now Claude Code's default permission mode |
| konuşma 10:43 | brain-build | brain-build | Brain build rebuilds the brain you saw |
| konuşma 10:43 | vault-lint | vault-lint | vault lint checks my notes for broken ones |
| konuşma 10:43 | cleanup skill | clean-up | frees up the memory on my Mac |
| konuşma 10:43 | morning digest | morning-digest | the one I use the most is the morning digest |
| kare 0:10 | heartbeat, outreach-pack, mail-scan rutinleri | aday değil: başka adayın parçası (routines.yaml) | routines.yaml içindeki girdiler |
| kare 1:00 | claude-mem-port-guard.sh, map-pending.sh, calibrate-pending.sh | aday değil: başka adayın parçası (routines.yaml) | Rings görünümündeki rutin/dosya adları |
| kare 7:30 | Gmail, Calendar, Apple Notes | aday değil: başka adayın parçası (routines.yaml) | Bot yanıtında mail-scan ve notes-ingest açıklamaları |
| konuşma 0:49 | Altı görünüm (rings, circle, areas, links, timeline, 3D orbit) | aday değil: başka adayın parçası (D3.js) | Dashboard sekmeleri; site_ui'de ayrıntılı |
| konuşma 4:32 | J E ve Agnostic OS videosu | aday değil: konu dışı | Seviye 2 fikrini aldığı başka yaratıcı |
| konuşma 5:00 | Astra 6 | aday değil: konu dışı | LLM örneği olarak anıldı, gösterilmedi; transkript şüpheli |
| kare 9:32 | Tech With Tim, Samin Yasar videoları | aday değil: konu dışı | YouTube'da 'hermes agent setup' arama sonuçları |
| kare 9:32 | skool.com, hostg.xyz bağlantıları | aday değil: konu dışı | Başka yaratıcıların video açıklamaları |
| açıklama | Patreon üyeliği | aday değil: konu dışı | Ücretli topluluk, erişilemez |
| açıklama | Ko-fi, Calendly, LinkedIn, YouTube kanalı | aday değil: konu dışı | Destek ve iletişim bağlantıları |
| açıklama | MAPS rehberi (GitHub) | MAPS | Ücretsiz rehber ve promptlar |
| açıklama | Hostinger referral bağlantıları (4) | Hostinger VPS | REFERRALCODE parametreli sepet bağlantıları |
| açıklama | Demo siteler (tavaduri, recombatumi, ajara-palace) | aday değil: konu dışı | Önizleme/referans siteleri |
| açıklama | code.claude.com doküman sayfaları | Claude Code | İzin ve sandbox dokümanları |
| yorum | Obsidian, OpenRouter, Descript, gstack, Nate Herk, Jev, ChatGPT | aday değil: konu dışı | İzleyici yorumlarında geçiyor, videoda gösterilmedi |
| konuşma 0:00 | MacBook, iPhone | aday değil: konu dışı | Donanım olarak anılıyor |
| kare 12:46 | Opus 5 /context kutu ızgarası | aday değil: başka adayın parçası (/context) | Context Usage çıktısının parçası |
## Kareden okunanlar
- 0:00: Üstte '646 files · 869 links · 246 runs'; 3D orbit görünümü, merkezde CLAUDE.MD, alan çipleri business 126, clients 34, career 16, content 48, youtube 19, personal 9, system 380.
- 0:10: ROUTINES tablosu '5/12 fired today': outreach-pack MAC 95 s, heartbeat VPS 8 s, morning-digest VPS 1 s 'digest sent', mail-scan MAC 48 s; hepsi FIRED.
- 0:18: Excalidraw 'One subscription, 2 machines': GitHub private repo, MacBook, Hostinger VPS, Tailscale 'only my devices get in', 'locked: drafts only, never sends', Telegram 'voice note → text → Claude → reply'.
- 0:32: PAV OS Agentic OS: Today, Needs Pav (3 overdue: Rob M., Kartick S., Demo pipeline seed), Routines 5/12; Gate review Tue 06.10 in 18 d.
- 2:16: studio SKILL.md: pay-as-you-go, hard spending gate, aggregator fal.ai, 'FAL_KEY in the environment', WaveSpeed veya Kie.ai alternatif. Anahtar değeri yok.
- 3:00: MAPS slaytı: Memory (one map of everything I work on), Agent (same Claude Code on 2 machines), Pulse (runs while my laptop is closed), Screen (shows, never stores); üç soru.
- 6:12: CLAUDE.md: Who, Areas tablosu, Rules (append-only, show don't store), Model routing: Fable xhigh, Opus high varsayılan, Sonnet medium-high, Haiku low, retrieval no model.
- 9:00: Automation Orbit GEO denetimi: Overall GEO score 62/100, 'Before 47 / After 62', alt skorlar citability 70, authority 34, E-E-A-T 67, technical 90.
- 9:52: routines.yaml: heartbeat 30 7 (vps), morning-digest 30 7 (vps), outreach-pack 0 7 (mac), tracker-row 30 23 (mac), mail-scan 0 8 (mac); '(Demo copy for video #020)'.
- 12:16: İki Claude Code v2.1.276 bölmesi (Opus 5 1M context, Claude Max); sol ~/Claude, sağ ~/Claude/AI OS; Auto mode varsayılan; soru metni.
- 12:18: /context: sol 'Baked for 1m 2s', Messages 27.7k; sağ 'Worked for 30s', Messages 16.8k, Memory files 1.3k, 27 skills.
- 13:02: Bindirme infografiği: 'Tokens used on one question' 23.9k (haritasız) vs 14.5k (haritalı), 'about 40% less'.
## Belirsizlikler
- Infografikteki 23.9k/14.5k, konuşulan 28k/17k ve /context'teki 27.7k/16.8k aynı değil; oran yine yaklaşık %40.
- Altyazıdaki 'Astra 6' modeli belirsiz; ekranda doğrulanmadı.
- Sesli notu metne çeviren araç adı verilmedi.
- Altyazıda 'Cloud' diye geçen ifade Claude olarak yorumlandı.
- 'J E' ve 'Agnostic OS' videosu (4:32) ile yorumdaki 'Jev' kimliği belirsiz; muhtemelen 8NSyI-npJCU videosu.
- Sponsor bölümü ('Today's sponsor: me') yazarın kendi hizmeti; utm parametresi var ama ortaklık yok, bağlantı 'diğer' sınıflandı.
- Yorumda anılan Obsidian, OpenRouter, Descript, gstack, Nate Herk videoda gösterilmedi; aday yapılmadı.
- Sözlük eşleşmeleri Three.js, Next.js, Framer Motion, Matter.js, Astro, Bun, Make, Notion, Canva, context7, Antigravity ekranda/konuşmada doğrulanmadı; 'notion' OCR'ı 'motion' düğmesi olabilir.
- 3B yörünge için Three.js kullanıldığı söylenmedi; yazar yalnızca HTML, CSS, JavaScript ve D3 dedi.
- Ekrandaki Gmail, Calendar, Apple Notes rutin açıklamalarında geçiyor; ayrı araç olarak gösterilmedi.
## Atlanan segment oranı
0/21 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://hermes-agent.nousresearch.com/install.sh | 9:26 | ekran | evet |
| https://www.skool.com/claude | 9:32 | ekran | hayır |
| https://www.skool.com/aianswers | 9:32 | ekran | hayır |
| https://www.hostg.xyz/SHJWj | 9:32 | ekran | hayır |
| https://code.claude.com/docs/en/permission-modes | 12:16 | ekran | evet |
| fal.ai | 2:06 | ekran | evet |
| Kie.ai | 2:16 | ekran | evet |
| automationorbit.com | 8:48 | ekran | hayır |
| map-pending.sh | 1:00 | ekran | hayır |
| claude-mem-port-guard.sh | 1:00 | ekran | hayır |
| calibrate-pending.sh | 1:00 | ekran | hayır |
| https://www.patreon.com/pavrus/membership | açıklama | açıklama | hayır |
| https://github.com/pavrus117/ai-os-maps-guide | açıklama | açıklama | evet |
| https://ko-fi.com/pavrus | açıklama | açıklama | hayır |
| https://www.hostinger.com/cart?product=vps%3Avps_kvm_1 (referral) | açıklama | açıklama | evet |
| https://www.hostinger.com/cart?product=vps%3Avps_kvm_2 (referral) | açıklama | açıklama | evet |
| https://www.hostinger.com/cart?product=vps%3Avps_kvm_4 (referral) | açıklama | açıklama | evet |
| https://www.hostinger.com/cart?product=vps%3Avps_kvm_8 (referral) | açıklama | açıklama | evet |
| https://tailscale.com | açıklama | açıklama | evet |
| https://audit.automationorbit.com/?utm_source=youtube&utm_medium=video&utm_campaign=020-ai-os | açıklama | açıklama | evet |
| https://calendly.com/rusovs-p/30min | açıklama | açıklama | hayır |
| https://www.linkedin.com/in/pav-rusovs | açıklama | açıklama | hayır |
| https://www.youtube.com/@pavrusovs | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=8NSyI-npJCU&t=981s | açıklama | açıklama | hayır |
| https://fal.ai/docs/documentation | açıklama | açıklama | evet |
| https://docs.kie.ai | açıklama | açıklama | evet |
| https://audit.automationorbit.com | açıklama | açıklama | evet |
| https://tavaduri-preview.netlify.app | açıklama | açıklama | hayır |
| https://recombatumi.com | açıklama | açıklama | hayır |
| https://ajara-palace-preview.netlify.app | açıklama | açıklama | hayır |
| https://code.claude.com/docs/llms.txt ve diğer code.claude.com/docs bağlantıları (izinler, sandbox, MCP, ayarlar, HIPAA, VS Code; 30+ sayfa) | açıklama | açıklama | evet |
## İş akışı
- yok
## Promptlar
- Hafıza haritası için röportaj promptu (5:35'te anılan) — Yapay zekâ önce kullanıcıyı röportaj yapsın: tek soru, yanıt bekle. Sıra: işletme, haftalık beş iş, borçlu olunanlar, dosyaların yeri, unutulanlar. Belirsiz yanıta itiraz et, kayıtları interviews/ klasörüne yaz, 'stop' deyince hafıza haritası taslağı ve bilinmeyenleri çıkar.
- Harita testi: süre ve token karşılaştırması — LinkedIn gönderisinde hangi kelimeleri kullanamayacağım ve bu liste nerede yazılı? Aynı soru haritasız ve haritalı oturumda soruldu.
- VPS botu canlı sesli not testi — Sesli mesajla Telegram botuna 'bugün ne var?' soruldu; ses metne çevrilip Claude'a gitti.
- MAPS rehber promptları (içerik gösterilmedi) — Her katman için rehberde hazır prompt var; Claude Code'a yapıştırınca o katmanı kurmaya yönlendirir.
