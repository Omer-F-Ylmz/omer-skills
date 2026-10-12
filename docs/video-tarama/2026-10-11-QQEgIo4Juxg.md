# you need to use Hermes RIGHT NOW!! (goodbye OpenClaw!!)
## Künye
you need to use Hermes RIGHT NOW!! (goodbye OpenClaw!!) · NetworkChuck · süre: 32:39 · en · https://youtu.be/QQEgIo4Juxg · şema 2
motor: parti 2026-10-11-uzun-2 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (45)
kareler: girdi ≤40000 jeton için 60→45
claude-sonnet-5-5: claude-sonnet-5-5 · 79677 tk · claude-haiku-5-5: claude-haiku-5-5 · 123716 tk
## Özet
NetworkChuck, bir aydır kullandığı Nous Research'ün açık kaynak ajanı Hermes Agent'a OpenClaw'dan neden geçtiğini beş gerekçeyle anlatıyor: hava (vibe), bellek, ekip, kendi skill'ini yazan kendini geliştirme döngüsü ve bozulmaması. Hostinger sponsorluğunda 5 dolarlık sınıfta bir VPS'e (KVM 2, Ubuntu) tek satırlık komutla Hermes kuruyor; modeli OpenAI Codex ile ChatGPT aboneliği üzerinden bağlıyor, Telegram bot'unu BotFather ile kuruyor. Ajana 'Ron Weasley' IT büyücüsü kişiliğini veriyor, USER.md / MEMORY.md boyut sınırlarını ve 10 turluk bellek dürtmesini gösteriyor, Honcho ile uzun vadeli belleği anlatıyor. Twingate ile stüdyo ağına bağlanan Ron'un kendi skill'ini yazması, Curator, Home Assistant ile lamba/panjur kontrolü, UniFi erişimi, dashboard, Kanban ve computer use da gösteriliyor. Video sonunda dua var.
## Bölümler
- 0:00 OpenClaw'dan Hermes'e neden geçiyorum
- 2:22 Hermes'i Hostinger VPS'e kurmak
- 5:36 Yapay zekâ modeli seçimi + Telegram kurulumu
- 9:46 Hermes belleği gerçekte nasıl çalışıyor
- 12:51 Bellek boyut sınırları ve 10 turluk dürtme
- 14:43 Honcho: ajan için uzun vadeli bellek
- 17:01 Hermes, OpenClaw'dan önce de vardı
- 19:20 Kendi skill'ini yazan ajanlar
- 22:20 Curator ve kendini geliştirme döngüsü
- 24:03 Canlı demo: Home Assistant + UniFi
- 26:16 Hermes neden OpenClaw gibi bozulmuyor
- 29:23 Kanban, dashboard ve computer use
- 30:57 Size bir dua
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Hermes Agent | yok | CLI | https://github.com/NousResearch/hermes-agent | Nous Research'ün açık kaynak, kendini geliştiren yapay zekâ ajanı (harness) | 0:14 | GitHub kartı: NousResearch / hermes-agent, 'The agent that grows with you' (karede: kanıttan) GitHub kartı: NousResearch / hermes-agent, 'The agent that grows with you' |
| OpenClaw | yok | CLI | yok | Karşılaştırılan ve bırakılan rakip ajan çerçevesi; Hermes'e geçiş yolu var | 0:00 | Tired of fixing my OpenClaw agents |
| Hostinger | yok | teknik | yok | Hermes'in kurulduğu bulut VPS sağlayıcısı (sponsor) | 2:22 | They are the sponsor of this video |
| KVM 2 | yok | teknik | yok | Seçilen Hostinger VPS planı (2 vCPU, 8 GB RAM) | 3:16 | Fiyat kartında KVM 2 işaretli, 'Homelab in the cloud' notu · kanıt: kare (karede: Fiyat kartında KVM 2 işaretli, 'Homelab in the cloud' notu) |
| Ubuntu | yok | teknik | yok | VPS işletim sistemi (Ubuntu 24.04 LTS) | 3:38 | Overview'da Ubuntu 24.04 LTS KVM 2 Running (karede: kanıttan) Overview'da Ubuntu 24.04 LTS KVM 2 Running |
| SSH | yok | CLI | yok | VPS'e kök erişimle uzaktan bağlanma | 3:38 | Root access: ssh root@ ... komutu (karede: kanıttan) Root access: ssh root@ ... komutu |
| uv | yok | CLI | yok | Kurulum betiğinin kurduğu hızlı Python paket yöneticisi | 4:18 | Installing uv (fast Python package manager) (karede: kanıttan) Installing uv (fast Python package manager) |
| Python 3.11 | yok | teknik | yok | Hermes'in çalıştığı Python sürümü, uv ile kuruldu | 4:50 | Creating virtual environment with Python 3.11 (karede: kanıttan) Creating virtual environment with Python 3.11 |
| Node.js | yok | teknik | yok | Tarayıcı araçları için kurulan Node.js 22 LTS | 4:22 | Installing Node.js 22 LTS (browser tools) metni (karede: kanıttan) Installing Node.js 22 LTS (browser tools) metni |
| ripgrep | yok | CLI | yok | Kurulum sırasında yüklenen arama aracı | 4:44 | ripgrep installed, ffmpeg installed satırları · kanıt: kare (karede: ripgrep installed, ffmpeg installed satırları) |
| ffmpeg | yok | CLI | yok | Kurulum sırasında yüklenen medya aracı | 4:44 | ripgrep installed, ffmpeg installed satırları · kanıt: kare (karede: ripgrep installed, ffmpeg installed satırları) |
| OpenAI Codex | yok | teknik | yok | ChatGPT aboneliğiyle Hermes'e beyin olarak bağlanan sağlayıcı | 5:36 | My favorite one to start with is the OpenAI Codex |
| GPT-5.5 | yok | teknik | yok | Seçilen ana model | 6:30 | Then we'll choose our model. GPT-5.5. |
| ChatGPT | yok | teknik | yok | Mevcut abonelik Hermes'e giriş için kullanıldı | 6:02 | ChatGPT fiyatlandırma sayfası Free, Go, Plus, Pro planları (karede: kanıttan) ChatGPT fiyatlandırma sayfası Free, Go, Plus, Pro planları |
| xAI Grok OAuth | yok | teknik | yok | SuperGrok aboneliğiyle Hermes'i kullanma seçeneği | 6:10 | Listede 'xAI Grok OAuth (SuperGrok Subscription)' daire içine alınmış (karede: kanıttan) Listede 'xAI Grok OAuth (SuperGrok Subscription)' daire içine alınmış |
| LM Studio | yok | teknik | yok | Yerel model seçeneği; Hermes ile iyi çalıştığı söylendi | 5:36 | If you wanna go local with LM Studio, do it |
| OpenRouter | yok | teknik | yok | Frontier model erişimi için seçenek | 5:36 | Wanna go Frontier? OpenRouter's good |
| Qwen | yok | teknik | yok | Yerel modellerde Hermes ile iyi çalışan model | 5:36 | Hermes is really good with it, especially the Qwen model |
| Telegram | yok | teknik | yok | Ajanla konuşulan mesajlaşma ağ geçidi | 6:36 | We're gonna go with Telegram because it's the easiest |
| BotFather | yok | teknik | yok | Telegram bot oluşturma ve token alma botu | 6:36 | Search for the bot father. He's gonna help us create a new bot |
| userinfobot | yok | teknik | yok | Telegram kullanıcı kimliğini öğrenme botu (izin listesi için) | 8:02 | Telegram'da 'User Info • Get ID • idbot' sohbeti (karede: kanıttan) Telegram'da 'User Info • Get ID • idbot' sohbeti |
| systemd | yok | teknik | yok | Ağ geçidini arka plan sistem servisi olarak çalıştırma | 7:36 | We'll install the gateways a SystemD service |
| SOUL.md | yok | teknik | yok | Ajanın kişiliğini tutan dosya; Ron kimliği buraya yazıldı | 10:46 | Hermes edited his SOUL.md file |
| USER.md | yok | teknik | yok | Ajanın kullanıcı hakkında yazdığı bellek dosyası (1.375 karakter sınırı) | 10:46 | it added it to my user file... USER.md |
| MEMORY.md | yok | teknik | yok | Ortam ve teknik bilgi belleği (2.200 karakter sınırı) | 11:46 | there's a new file there, MEMORY.md |
| hermes memory setup | yok | CLI | yok | Bellek eklentilerini yapılandıran Hermes komutu | 13:52 | We'll do Hermes memory setup |
| Honcho | yok | plugin | https://github.com/plastic-labs/honcho | Eş (peer) kartı ve sonuç çıkarımıyla uzun vadeli bellek servisi | 14:43 | I added this thing called Honcho |
| Hermes 4 | yok | teknik | yok | Nous Research'ün ayrı Hermes model ailesi (70B ve 405B) | 18:46 | Hermes-4-70B ve Hermes-4-405B model kartları, Llama-3.1 tabanlı (karede: kanıttan) Hermes-4-70B ve Hermes-4-405B model kartları, Llama-3.1 tabanlı |
| Twingate | yok | teknik | yok | Ron'un stüdyo ağına bağlanması için VPN / sıfır güven erişim | 19:20 | We're gonna use Twingate. It's a VPN |
| Kendi skill'ini yazma | yok | skill | yok | Ajan deneyimden yeniden kullanılabilir skill üretiyor (Twingate client skill'i) | 20:24 | Ron just made his own skill. That's the power of Hermes · kanıt: yok |
| GitHub PR review | yok | skill | yok | Hermes ile gelen hazır PR inceleme skill'i | 21:26 | prepackaged skills... GitHub PR review, that is in there |
| ClawHub | yok | teknik | yok | OpenClaw topluluk skill pazarı; kötü amaçlı içerik eleştirisi | 21:54 | ClawHub sayfası: 'Equip Install Ship', öne çıkan skill'ler · kanıt: kare (karede: ClawHub sayfası: 'Equip Install Ship', öne çıkan skill'ler) |
| Curator | yok | skill | yok | Ajanın yazdığı skill'leri active/stale/archived durumlarıyla temizleyen arka plan ajanı | 22:20 | Hermes just came out with this, a thing called the Curator |
| agentskills.io | yok | teknik | yok | Curator belgesinde anılan hub skill standardı | 22:28 | Curator belgesinde 'hub-installed skills (from agentskills.io)' bağlantısı (karede: kanıttan) Curator belgesinde 'hub-installed skills (from agentskills.io)' bağlantısı |
| Home Assistant | yok | skill | yok | Hermes'in yerleşik Home Assistant skill'i; stüdyo lambası ve panjurlar kontrol edildi | 24:03 | Built into Hermes is a Home Assistant skill |
| UniFi | yok | teknik | yok | Ağ yönetimi için Ron'a verilen erişim; UniFi network operation skill'i üretildi | 25:03 | Ron is wanting some UniFi access |
| Alt ajanlar (delegate) | yok | teknik | yok | Görev devri ve alt ajan desteği | 26:16 | it can delegate tasks. It can do sub agents · kanıt: yok |
| interrupt / steer / queue | yok | ipucu | yok | Mesajı kesme, yönlendirme veya sıraya alma | 26:16 | you can interrupt, steer, or queue messages · kanıt: yok |
| Hermes dashboard | yok | teknik | yok | Skill, eklenti, profil, model, başarım yönetimi arayüzü | 29:23 | now, there's a Hermes dashboard |
| Kanban | yok | teknik | yok | Dashboard'da ajana görev atama panosu (Pokemon kartı örneği) | 29:23 | one of the most powerful things they released recently is Kanban |
| Computer use | yok | teknik | yok | Hermes'in bilgisayarı kontrol etme özelliği (önizleme) | 30:24 | just came out their own computer use |
| Windows PowerShell | yok | CLI | yok | Yerel bilgisayarda sunucuya SSH ile bağlanmak için kullanılan terminal | 3:48 | Terminal açılıyor ve Windows PowerShell başlatılıyor (karede: Windows PowerShell açılış metni ve pwsh prompt'u) |
| xAI Grok (SuperGrok) | yok | teknik | yok | Grok aboneliğiyle Hermes'e bağlanabilen sağlayıcı seçeneği (anlatıldı, kurulmadı) | 5:36 | Grok'un Hermes ile ortaklık yaptığı ve abonelikle kullanılabileceği anlatılıyor · kanıt: yok |
| Claude Opus | yok | teknik | yok | Sağlayıcı ekranında görünen varsayılan Anthropic modeli | 6:20 | Terminalde mevcut model olarak anthropic/claude-opus-4.6 görünüyor (karede: Terminal satırı: 'Current model: anthropic/claude-opus-4.6' ve 'Active provider: none') |
| Discord | yok | teknik | yok | Ekipte ajanların çalıştığı sohbet platformu; Hermes'in desteklediği platformlardan biri | 4:24 | Nous Research ekibinin ajanlarla Discord kanallarında konuştuğu anlatılıyor |
| Ajana IT büyücüsü Ron Weasley kimliği vermek | yok | prompt | yok | Ajana Ron Weasley kişiliğini verir: Muggle IT'ye merak saran yetişkin Ron, İngiliz ve sıcak üslup, büyü sözlüğü, güvenlik kuralları. SOUL.md dahil dosyaları güncelleyip bundan sonra bu kimlikle davranmasını ister. | 9:46 | kaynak: altyazı |
| Ron'un sistem prompt'undaki sert kurallar | yok | prompt | yok | Ron'un kimlik kartındaki kısıtlar: cihazlarda açık yetki yoksa salt okunur çalış, işlemden önce teşhis, yıkıcı adımları onayla, önce sade dille başarı/başarısızlık raporu ver. | 10:22 | kaynak: kare |
| Ajanı kullanıcı ve ortam bilgisiyle beslemek (USER.md/MEMORY.md) | yok | prompt | yok | Kullanıcı NetworkChuck, adı Chuck; ekip üyeleriyle de konuşulacak, ajan Hostinger VPS'te çalışıyor, ağı anlatılıyor. | 10:46 | kaynak: altyazı |
| Stüdyo ağına Twingate erişimi kurdurmak | yok | prompt | yok | Ron'dan Hostinger bulutunda başsız (headless) Twingate istemcisini kurup stüdyo ağına erişim sağlaması istendi; servis anahtarı verildi. | 19:20 | kaynak: altyazı |
| Home Assistant ile stüdyo cihazlarını kontrol etmek | yok | prompt | yok | Home Assistant skill'ini etkinleştirmesi, IP ve anahtarla bağlanması, sonra lambayı kapatıp mavi açması, panjurları denemesi istendi. | 24:03 | kaynak: altyazı |
| Ron'a UniFi ağ yönetimi erişimi vermek | yok | prompt | yok | UniFi hakkında olabildiğince araştırma yapması, API anahtarı ve kullanıcı hesabı verilerek erişimin kurulması. | 26:16 | kaynak: altyazı |
| Kanban görevi olarak Pokemon kartı oluşturtmak | yok | prompt | yok | NetworkChuck için Pokemon kartı yapılması, benim görüntümü kullan, HTML sayfası olsun ve etkileyici görünsün; default profile atanıyor. | 29:23 | kaynak: altyazı |
## Açıklama bağlantıları
- https://hostinger.com/networkchuckhermes — Hostinger VPS sponsor bağlantısı (kod NETWORKCHUCK) · aday: evet (Hostinger) · Videoda kullanılan VPS servisi; açıklamada 'Sponsored by Hostinger' yazıyor ve indirim kodu var · sınıf: sponsor
- https://ntck.co/hermes — NetworkChuck Academy Hermes kursu (mağaza) · aday: hayır · Ücretli kurs sayfası, araç değil · sınıf: diğer · erişilemez: ücretli kurs, giriş gerekli
- https://hermes-agent.nousresearch.com/ — Hermes Agent resmî sitesi · aday: evet (Hermes Agent) · Videoda kurulan ve kullanılan araç · sınıf: diğer
- https://github.com/NousResearch/hermes-agent — Hermes Agent GitHub deposu · aday: evet (Hermes Agent) · Kurulan aracın deposu · sınıf: diğer
- https://nousresearch.com/ — Nous Research şirket sitesi · aday: hayır · Şirket tanıtımı, referans sayfa · sınıf: diğer
- https://honcho.dev/ — Honcho bellek servisi · aday: evet (Honcho) · Videoda denenen bellek eklentisi · sınıf: diğer
- https://www.twingate.com/ — Twingate erişim servisi · aday: evet (Twingate) · Ron'un ağa bağlanmak için kullandığı servis · sınıf: diğer
- https://www.home-assistant.io/ — Home Assistant akıllı ev platformu · aday: evet (Home Assistant) · Demoda kullanılan platform · sınıf: diğer
- https://ui.com/ — UniFi üreticisi Ubiquiti · aday: evet (UniFi) · Alan adı videoda kullanılan UniFi aracını adlandırıyor · sınıf: diğer
- https://youtu.be/G3jvn7n-68Y — Başka NetworkChuck videosu (systemd videosu olduğu tahmin) · aday: hayır · Videonun içeriği doğrulanamadı, YouTube referansı · sınıf: diğer
- https://youtu.be/wOWhfNB_r-0 — Başka NetworkChuck videosu (Perplexity Computer olabilir) · aday: hayır · Videonun içeriği doğrulanamadı, YouTube referansı · sınıf: diğer
- https://x.com/theemozilla — Nous Research kurucu hesabı · aday: hayır · Sosyal medya profili · sınıf: diğer
- https://x.com/NousResearch — Nous Research X hesabı · aday: hayır · Sosyal medya profili · sınıf: diğer
- https://x.com/Teknium1 — Teknium X hesabı · aday: hayır · Sosyal medya profili · sınıf: diğer
- https://x.com/karan4d — Karan X hesabı · aday: hayır · Sosyal medya profili · sınıf: diğer
- https://x.com/bloc97_ — bloc97 X hesabı · aday: hayır · Sosyal medya profili · sınıf: diğer
- https://ntck.co/coffee — NetworkChuck kahve mağazası · aday: hayır · Destek/mağaza bağlantısı, araç değil · sınıf: diğer
- https://ntck.co/NCAcademy — NetworkChuck Academy · aday: hayır · Eğitim platformu tanıtımı, ücretli üyelik · sınıf: diğer · erişilemez: ücretli topluluk, giriş gerekli
- https://ntck.co/ccna — CCNA kursu · aday: hayır · Konu dışı kurs reklamı · sınıf: diğer
- https://www.instagram.com/networkchuck/ — Instagram profili · aday: hayır · Sosyal medya · sınıf: diğer
- https://x.com/networkchuck — NetworkChuck X hesabı · aday: hayır · Sosyal medya · sınıf: diğer
- https://www.facebook.com/NetworkChuck/ — Facebook sayfası · aday: hayır · Sosyal medya · sınıf: diğer
- https://ntck.co/discord — NetworkChuck Discord topluluğu · aday: hayır · Topluluk daveti, araç değil · sınıf: diğer · erişilemez: giriş gerekli topluluk
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Parlayan neon başlık (neon glow text) ve GitHub depo kartı | Turuncu parlayan 'HERMES-AGENT' başlığı, altında koyu cam görünümlü kart: izleyici, fork, yıldız sayaçları ve etiket rozetleri (karede: Parlayan turuncu HERMES-AGENT başlığı; kartta 327 watching, 17.2K forks, 131.8K stars, MIT License rozeti) | 0:14 | kare |
| Koyu yeşil tek sütun açılış sayfası (hero section) ve terminal demosu | Ortalanmış 'The agent that grows with you.' başlığı, kurulum komutu kutusu, terminal penceresi demosu ve sağda görselli panel (karede: Hermes Agent sitesi: üstte DOCS/PORTAL/SOCIALS/THEME menüsü, 1 INSTALL ve 2 CONFIGURE kutuları, 'See it in action' terminal kutusu) | 1:46 | kare |
| Özellik ızgarası (feature grid) ve sekmeli açılır liste (tabs / accordion) | Üç sütunlu özellik kartları; 'LESS' ile açılan TOOLS/PLATFORMS/ENVIRONMENTS/SKILLS/RESEARCH satırları, seçili satır vurgulu (karede: Hermes Agent v0.13.0 sayfasında SKILLS satırı vurgulu: '40+ bundled skills covering MLOps, GitHub workflows') | 21:24 | kare |
| Fiyat kartları (pricing cards) ve 'en popüler' rozeti | Üç plan kartı yan yana, ortadaki mor çerçeveli ve rozetli; sağda sohbet yardımcı paneli (chat widget) (karede: Hostinger KVM 1, KVM 2 (MOST POPULAR, $8.99/mo), KVM 4 kartları; sağda Kodee sohbet paneli) | 3:16 | kare |
| Kenar çubuklu yönetim paneli (sidebar dashboard) ve kullanım kartları | Sol menü, sunucu özeti, CPU/bellek/disk/trafik metrik kartları (karede: Hostinger hPanel Overview: Ubuntu 24.04 LTS KVM 2 Running, CPU 1%, Memory 5%, Disk 2 GB/100 GB) | 3:38 | kare |
| Honcho bulut paneli: sekmeli eş kartı (tabbed peer card) | Sol gezinme çubuğu, Peer Card/Chat/Message Search/Sessions/Config sekmeleri, bulanıklaştırılmış kişi kartı (karede: app.honcho.dev Explore: Workspaces > hermes_james > Peers > Chuck, Peer Card sekmesi) | 16:02 | kare |
| Kanban panosu ve dashboard sekmeleri (Kanban board) | Hermes dashboard'unda skill, eklenti, profil, model, başarım ve görev panosu | 29:23 | altyazı |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| curl -fsSL https://hermes-agent.nousresearch.com/install.sh / bash | Hermes Agent'ı sunucuya kurar; uv, Python 3.11, Git ve Node.js bağımlılıklarını ve Hermes deposunu indirir (karede: Installer ekranı: 'Hermes Agent Installer', 'Detected: linux (ubuntu)', 'Installing uv') | 4:18 | kare |
| ssh root@<sunucu-IP> | Hostinger VPS'e root kullanıcısıyla SSH bağlantısı açar (IP değeri yazılmadı) (karede: VPS overview ekranında 'Root access' altında ssh root komutu) | 3:38 | kare |
| hermes claw --help | OpenClaw'dan Hermes'e geçiş alt komutlarını (migrate, cleanup, clean) listeler (karede: Terminalde 'hermes claw [-h] {migrate,cleanup,clean}' yardım çıktısı) | 1:26 | kare |
| hermes setup agent | Ajan ayarlarını sonradan özelleştirmek için kurulum sihirbazını açar (karede: Kurulum ekranında 'Run hermes setup agent later to customize' satırı) | 7:04 | kare |
| hermes model | Ana modeli ve sağlayıcıyı seçmek için açılır (karede: Uyarı satırı: 'Run hermes model to choose a provider and model') | 6:20 | kare |
| hermes | Hermes sohbet arayüzünü terminalde başlatır ('Launch hermes chat now?' sorusu) (karede: 'Launch hermes chat now? [Y/n]' istemi) | 8:50 | kare |
| hermes doctor | Kurulum ve yapılandırma sorunlarını teşhis eder (ipucu olarak gösterildi) (karede: Kurulum sonrası ipuçları listesinde 'hermes doctor' satırı) | 8:50 | kare |
| hermes config edit | Yapılandırma dosyasını düzenleyici ile açar (karede: İpuçları listesinde 'hermes config edit' satırı) | 8:50 | kare |
| nano /root/.hermes/config.yaml | Hermes yapılandırma dosyasını nano ile açar (karede: İpuçları listesinde 'nano /root/.hermes/config.yaml' satırı) | 8:50 | kare |
| sudo hermes gateway start --system | Telegram gateway'ini sistem servisi olarak başlatır (karede: Kurulum çıktısında 'Next steps' altında bu komut) | 8:48 | kare |
| sudo hermes gateway status --system | Gateway servisinin durumunu gösterir (karede: Kurulum çıktısında 'Next steps' altında bu komut) | 8:48 | kare |
| journalctl -u hermes-gateway -f | Gateway servis loglarını canlı izler (karede: Kurulum çıktısında '# View logs' açıklamalı komut) | 8:48 | kare |
| hermes memory setup | Hafıza sağlayıcısını (yerleşik ya da Honcho gibi eklenti) yapılandırır | 13:52 | altyazı |
| cat USER.md ve cat MEMORY.md (memories klasöründe) | Hermes'in kullanıcı ve ortam hafıza dosyalarının içeriğini gösterir (karede: Terminalde memories klasöründe 'cat USER.md' ve 'cat MEMORY.md' komutları) | 13:02 | kare |
| hermes tools enable homeassistant | Home Assistant araç setini etkinleştirir (ajanın terminalde çalıştırdığı komut) (karede: Terminal satırı: 'hermes tools enable homeassistant && ...') | 24:10 | kare |
| hermes tools list | Etkin ve kullanılabilir araçları listeler (Home Assistant doğrulaması için) (karede: Terminal satırı: 'hermes tools list / sed -n ...') | 24:10 | kare |
| /new | Yeni bir sohbet oturumu başlatır (videoda 'new' olarak söylendi) | 10:46 | altyazı |
| /reset | Araç değişikliklerinin yeni oturumda etkili olması için oturumu sıfırlar (karede: Hermes mesajı: 'use /reset here after' yönlendirmesi) | 24:10 | kare |
| /restart | Telegram gateway'inin yeni ortam değişkenlerini ve araçları yeniden yüklemesini sağlar (karede: Hermes mesajı: 'send /restart here so the Telegram owl reloads') | 24:28 | kare |
| /busy | Çalışan görev sırasında gelen mesajların nasıl ele alınacağını gösterir (karede: Mesaj: 'First-time tip — ... Send /busy') | 1:24 | kare |
| /queue | Gelen mesajı çalışan göreve kesmeden sıraya alır (karede: Alt satır: 'msg=interrupt · /queue · /bg · /steer · Ctrl+C cancel') | 26:34 | kare |
| /bg | Görevi arka planda çalıştırır (karede: Alt satır: '/bg' seçeneği) | 26:34 | kare |
| /steer | Çalışan görevin yönünü mesajla değiştirir (karede: Alt satır: '/steer' seçeneği) | 26:34 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Hermes GitHub deposu 131.8K yıldız, 17.2K fork gösteriyor | 0:14 | sayısal |
| Hermes en hızlı büyüyen GitHub projesi ve OpenRouter token kullanımında OpenClaw'ı geçti | 0:00 | karşılaştırma |
| KVM 2 planı 2 vCPU, 8 GB RAM, 100 GB disk, ayda 8,99 dolar (24 ay) | 3:16 | sayısal |
| ChatGPT aboneliği ek ücret ödemeden Hermes'e beyin olabilir | 5:36 | özellik |
| USER.md en fazla 1.375, MEMORY.md en fazla 2.200 karakter | 12:51 | sayısal |
| Hermes bellek güncellemesi için oturum içinde yaklaşık her 10 turda arka plan ajanı çalıştırır; OpenClaw yalnızca sıkıştırmada | 13:52 | karşılaştırma |
| Honcho OpenClaw'a da bağlanabilir ama Hermes'te birinci sınıf vatandaş | 15:43 | karşılaştırma |
| Hermes, OpenClaw'dan önce yaklaşık 6-7 ay önce dahili araç olarak başladı | 17:01 | özellik |
| OpenClaw skill'leri pazardan bulunur, Hermes ise skill'i kullanıma göre kendisi üretir | 20:24 | karşılaştırma |
| Curator skill'leri active, stale, archived durumlarına taşır | 22:20 | özellik |
| Konuşmacıya göre Hermes'e henüz ajanla ilgili CVE gelmedi; OpenClaw'ın çok CVE'si vardı | 21:26 | karşılaştırma |
| Hermes bir proje değil ürün gibi hissettiriyor; bir aydır sorun yaşamamış | 27:16 | öneri |
| Hermes ve OpenClaw aynı sunucuda yan yana çalışabilir | 2:22 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | OpenClaw | OpenClaw | Tired of fixing my OpenClaw agents |
| kare 0:14 | Hermes Agent GitHub kartı | Hermes Agent | NousResearch / hermes-agent, 131.8K stars |
| kare 1:38 | NetworkChuck tweeti ve Nous yanıtı | aday değil: konu dışı | Tweet yanıtı 'Hermes Agent' |
| konuşma 1:00 | OpenClaw migration yolu | OpenClaw | They even have an OpenClaw migration path |
| konuşma 2:22 | Hostinger VPS | Hostinger | They are the sponsor of this video |
| açıklama | NETWORKCHUCK indirim kodu | aday değil: sponsor/reklam | Use code NETWORKCHUCK at checkout for a discount |
| kare 3:16 | KVM 2 planı | KVM 2 | MOST POPULAR, $8.99/mo |
| konuşma 3:22 | Ubuntu işletim sistemi | Ubuntu | Choose Ubuntu as your OS |
| konuşma 2:22 | Docker | aday değil: genel kavram | Run Docker. I don't care. |
| kare 3:38 | SSH kök erişimi | SSH | Root access ssh root@... |
| kare 3:48 | Windows PowerShell | aday değil: konu dışı | PowerShell güncelleme uyarısı, bağlantı yalnızca terminal penceresi |
| kare 4:18 | uv paket yöneticisi | uv | Installing uv (fast Python package manager) |
| kare 4:50 | Python 3.11 | Python 3.11 | Creating virtual environment with Python 3.11 |
| kare 4:22 | Node.js 22 LTS | Node.js | Node.js 22 LTS kurulum satırı |
| kare 4:44 | ripgrep ve ffmpeg | ripgrep | ripgrep installed, ffmpeg installed |
| konuşma 4:24 | Discord'da Hermes ajanı | aday değil: genel kavram | we actually have our agents in our Discord channels |
| konuşma 5:36 | LM Studio | LM Studio | If you wanna go local with LM Studio, do it |
| konuşma 5:36 | OpenRouter | OpenRouter | OpenRouter's good |
| konuşma 5:36 | Qwen modeli | Qwen | especially the Qwen model |
| konuşma 5:36 | OpenAI Codex | OpenAI Codex | my favorite one to start with is the OpenAI Codex |
| kare 6:02 | ChatGPT fiyat sayfası | ChatGPT | Free, Go, Plus, Pro planları |
| kare 6:10 | xAI Grok OAuth | xAI Grok OAuth | SuperGrok Subscription satırı daire içinde |
| konuşma 6:30 | GPT-5.5 | GPT-5.5 | Then we'll choose our model. GPT-5.5. |
| konuşma 6:36 | Telegram | Telegram | We're gonna go with Telegram |
| konuşma 7:36 | BotFather | BotFather | Search for the bot father |
| kare 8:02 | userinfobot | userinfobot | User Info • Get ID • idbot sohbeti |
| konuşma 7:36 | systemd servisi | systemd | We'll install the gateways a SystemD service |
| konuşma 10:46 | SOUL.md | SOUL.md | Hermes edited his SOUL.md file |
| konuşma 11:00 | USER.md | USER.md | USER.md. Let's cat that |
| konuşma 11:46 | MEMORY.md | MEMORY.md | there's a new file there, MEMORY.md |
| konuşma 13:52 | hermes memory setup | hermes memory setup | We'll do Hermes memory setup |
| konuşma 14:43 | Honcho | Honcho | I added this thing called Honcho |
| konuşma 16:44 | Jeff Quesnelle röportajı | aday değil: konu dışı | I asked Jeff about this |
| kare 18:46 | Hermes-4-405B ve 70B | Hermes 4 | Hermes-4-70B ve Hermes-4-405B model kartları |
| konuşma 19:20 | Twingate | Twingate | We're gonna use Twingate. It's a VPN |
| konuşma 20:24 | Ron'un kendi yazdığı skill | Kendi skill'ini yazma | Ron just made his own skill |
| konuşma 21:26 | GitHub PR review skill | GitHub PR review | GitHub PR review, that is in there |
| kare 21:54 | ClawHub | ClawHub | Equip Install Ship. ClawHub sayfası |
| konuşma 22:20 | Curator | Curator | a thing called the Curator |
| kare 22:28 | agentskills.io | agentskills.io | hub-installed skills (from agentskills.io) |
| konuşma 22:20 | Perplexity Computer videosu | aday değil: konu dışı | callback to that video I made on Perplexity Computer |
| konuşma 24:03 | Home Assistant | Home Assistant | Built into Hermes is a Home Assistant skill |
| konuşma 25:03 | UniFi | UniFi | Ron is wanting some UniFi access |
| konuşma 26:16 | Alt ajanlar | Alt ajanlar (delegate) | It can do sub agents |
| konuşma 26:16 | interrupt, steer, queue | interrupt / steer / queue | you can interrupt, steer, or queue messages |
| konuşma 28:18 | Opus 4.7 | aday değil: konu dışı | Opus 4.7, GPT 5.5, I mean, things are good |
| konuşma 29:23 | Hermes dashboard | Hermes dashboard | there's a Hermes dashboard |
| konuşma 29:50 | Kanban | Kanban | One of the most powerful things they released recently is Kanban |
| konuşma 30:24 | Computer use | Computer use | just came out their own computer use |
| konuşma 30:57 | Dua bölümü | aday değil: konu dışı | I believe in the power of prayer |
| yorum | Hindsight | aday değil: konu dışı | Yorumda 'I swapped out Honcho for Hindsight' |
| linkli sayfa https://minimax.io | MiniMax | aday değil: konu dışı | Yalnızca bağlantılı sayfada ve sağlayıcı menüsünde |
## Kareden okunanlar
- 0:14: NousResearch / hermes-agent, MIT License, 327 watching, 17.2K forks, 131.8K stars
- 0:44: Hostinger sipariş özeti: KVM 2 plan, NETWORKCHUCK kuponu uygulanmış, 'COMING UP...'
- 1:38: NetworkChuck tweet: frontier OpenClaw alternatifleri; Nous Research yanıtı 'Hermes Agent'
- 1:46: Hermes Agent sitesi: 'THE AGENT THAT GROWS WITH YOU', 1 INSTALL curl komutu, 2 CONFIGURE hermes setup, 'Requires WSL2 on Windows'
- 2:44: Tarayıcı adresi hostinger.com/networkchuckhermes; altta 'hostinger.com/networkchuckhermes' yazısı
- 2:46: Hostinger Hermes Agent sayfası: VPS plan KVM 2, 2 vCPU, 8 GB RAM, 100 GB NVMe, 8 TB bant, $8.99/mo
- 3:04: Hostinger: 'Up to 70% off AI-managed VPS hosting', AMD EPYC, NVMe, Free weekly backups, AI Web terminal
- 3:16: KVM 1 $6.49, KVM 2 $8.99 (MOST POPULAR), KVM 4 $12.99; el yazısı 'Homelab in the cloud'
- 3:24: Hostinger sepeti: KVM 2, 24 ay, ABD-Phoenix, 'Have a coupon code?' bağlantısı
- 3:38: hPanel Overview: srv732018.hstgr.cloud, Ubuntu 24.04 LTS KVM 2 Running, ssh root@ komutu
- 3:46: Windows arama kutusuna 'terminal' yazılmış, en iyi eşleşme Terminal uygulaması
- 3:48: Windows PowerShell açılışı, 'https://aka.ms/PSWindows' güncelleme uyarısı
- 4:18: curl -fsSL https://hermes-agent.nousresearch.com/install.sh / sh/bash; 'Hermes Agent Installer', Ubuntu algılandı, uv kuruluyor
- 4:44: ripgrep ve ffmpeg kuruldu; /usr/local/lib/hermes-agent'a Git klonlama
- 4:50: Python 3.11.15 ile sanal ortam oluşturuluyor, bağımlılıklar kuruluyor
- 5:40: Sağlayıcı listesi: Nous Portal, OpenRouter, LM Studio, Anthropic, OpenAI Codex, Qwen Cloud, Xiaomi MiMo, NVIDIA NIM, GitHub Copilot, xAI, DeepSeek, Kimi vb.
- 6:02: ChatGPT fiyatları: Free $0, Go $8, Plus $20, Pro $100/ay
- 6:10: 'xAI Grok OAuth (SuperGrok Subscription)' satırı daire içinde
- 6:20: OpenAI Codex girişi: auth.openai.com/codex/device adresi ve bulanık kod, 'Waiting for sign-in...'
- 6:44: Platform listesi: Telegram, Discord, Slack, Matrix, WhatsApp, Signal, Email vb. (hepsi not configured)
- 7:04: Terminal Backend 'Skipped (keeping current)', local; 'Telegram bot token:' isteği
- 8:02: Telegram 'User Info • Get ID • idbot' sohbeti, /start yanıtı (isim bulanık)
- 10:22: 'RON WEASLEY AI AGENT SKILL' kartı; kurallar ve büyü sözlüğü
- 13:02: Terminalde ~/.hermes/memories, cat USER.md, cat MEMORY.md; el yazısı 'hard limits'
- 16:02: Honcho: workspace hermes_james, Peer Card 'Chuck' sekmeleri
- 18:10: Nous Research ekibi: Jeffrey Quesnelle (Co-Founder, CEO, CTO), Teknium, Karan Malhotra, Shivani Mitra
- 18:46: Hermes-4-70B ve Hermes-4-405B model kartları, Llama-3.1 tabanlı, 128k bağlam
- 21:04: Ağ taraması özeti: UniFi OS 10.77.14.3, Ceph, Proxmox düğümleri, çeşitli SSH ana bilgisayarları
- 21:54: ClawHub: 'Equip Install Ship.', öne çıkan skill'ler (Slack, Caldav Calendar, X Search, Trello)
- 22:22: Curator belgesi: 'background maintenance pass for agent-created skills', active → stale → archived
## Belirsizlikler
- Kurulum komutunun sonu karede 'sh' olarak sarılmış görünüyor; OCR 'bash' okuyor, kesin değil.
- Nous Portal, NVIDIA NIM, Xiaomi MiMo gibi sağlayıcılar yalnızca menüde görünüyor, kullanılmadı; aday yapılmadı.
- Mem0 yalnızca memory setup ekranında geçen OCR metninde göründü, anlatılmadı; aday yapılmadı.
- Playwright, Chrome Headless Shell kurulumu yalnızca OCR'da var, karede doğrulanamadı.
- hermes claw migrate/--help, /reset, /restart ve hermes tools enable homeassistant yalnızca OCR'da geçti, kare/altyazı kanıtı yok; kurulum komutlarına eklenmedi.
- Hindsight yalnızca yorumda anılıyor, videoda gösterilmedi.
- Açıklamadaki iki YouTube videosunun içeriği doğrulanamadı.
- Web sitesinin font aileleri karelerden belirlenemedi.
- Dashboard (29:23-30:26) kareleri gönderilmedi; yalnızca altyazı kanıtı var.
- Bazı zamanlar segment içi tahmindir (örn. GPT-5.5 6:30).
## Atlanan segment oranı
0/40 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://hostinger.com/networkchuckhermes | 2:22 | ses | evet |
| hostinger.com | 2:42 | ekran | evet |
| hostinger.com/ncopenclaw | 2:42 | ekran | hayır |
| hostinger.com/vps/docker/hermes-agent?utm_medium=influencer&utm | 2:42 | ekran | hayır |
| hpanel.hostinger.com/vps | 2:42 | ekran | evet |
| hostinger.com/vps-hosting | 3:10 | ekran | evet |
| cart.hostinger.com/pay/<sipariş-id> | 3:24 | ekran | evet |
| hpanel.hostinger.com/vps/732018/overview | 3:38 | ekran | evet |
| github.com/NousResearch/hermes-agent | 0:14 | ekran | evet |
| https://hermes-agent.nousresearch.com/install.sh | 1:44 | ekran | evet |
| hermes-agent.nousresearch.com | 4:16 | ekran | evet |
| archive.ubuntu.com/ubuntu | 4:24 | ekran | hayır |
| https://cdn.playwright.dev/builds/cft/147.0.7727.15/linux64/chrom | 5:32 | ekran | hayır |
| build.nvidia.com | 5:40 | ekran | hayır |
| api.kimi.com | 5:40 | ekran | hayır |
| minimax.io | 6:08 | ekran | hayır |
| ollama.com | 6:08 | ekran | hayır |
| networkchuck.com | 6:24 | ekran | hayır |
| auth.openai.com/codex/device | 6:20 | ekran | evet |
| auth.openai.com/deviceauth/callback (sorgu parametreleri kırpıldı) | 6:42 | ekran | evet |
| hermes-agent.nousresearch.com/docs/developer-guide/environments | 7:04 | ekran | hayır |
| t.me/username_bot | 7:20 | ekran | hayır |
| app.honcho.dev | 16:02 | ekran | evet |
| agentskills.io | 22:24 | ekran | evet |
| hermes-agent.nousresearch.com/docs/user-guide/features/curator | 22:38 | ekran | hayır |
| hermes-agent.nousresearch.com/docs/user-guide/features/skills#agent-managed-skills-skill_manage-tool | 22:46 | ekran | hayır |
| duckduckgo.com/html/?q= | 26:34 | ekran | hayır |
| academy.networkchuck.com | 29:22 | ekran | hayır |
| chatgpt.com/backend-api/codex | 30:18 | ekran | evet |
| https://hostinger.com/networkchuckhermes | açıklama | açıklama | evet |
| https://ntck.co/hermes | açıklama | açıklama | hayır |
| https://hermes-agent.nousresearch.com/ | açıklama | açıklama | evet |
| https://github.com/NousResearch/hermes-agent | açıklama | açıklama | evet |
| https://nousresearch.com/ | açıklama | açıklama | hayır |
| https://honcho.dev/ | açıklama | açıklama | evet |
| https://www.twingate.com/ | açıklama | açıklama | evet |
| https://www.home-assistant.io/ | açıklama | açıklama | evet |
| https://ui.com/ | açıklama | açıklama | evet |
| https://youtu.be/G3jvn7n-68Y | açıklama | açıklama | hayır |
| https://youtu.be/wOWhfNB_r-0 | açıklama | açıklama | hayır |
| https://x.com/theemozilla | açıklama | açıklama | hayır |
| https://x.com/NousResearch | açıklama | açıklama | hayır |
| https://x.com/Teknium1 | açıklama | açıklama | hayır |
| https://x.com/karan4d | açıklama | açıklama | hayır |
| https://x.com/bloc97_ | açıklama | açıklama | hayır |
| https://ntck.co/coffee | açıklama | açıklama | hayır |
| https://ntck.co/NCAcademy | açıklama | açıklama | hayır |
| https://ntck.co/ccna | açıklama | açıklama | hayır |
| https://www.instagram.com/networkchuck/ | açıklama | açıklama | hayır |
| https://x.com/networkchuck | açıklama | açıklama | hayır |
| https://www.facebook.com/NetworkChuck/ | açıklama | açıklama | hayır |
| https://ntck.co/discord | açıklama | açıklama | hayır |
| https://hostinger.com/networkchuckhermes | açıklama | yorum | evet |
| https://ntck.co/hermes | açıklama | yorum | hayır |
## İş akışı
- 1. adım — Hostinger'da KVM 2 VPS planını seç ve indirim kodunu uygula — araçlar: Hostinger VPS, Hostinger hPanel
- 2. adım — Sunucu konumunu ve işletim sistemi olarak Ubuntu 24.04'ü seç, VPS kurulumunu bekle — araçlar: Hostinger VPS, Ubuntu 24.04
- 3. adım — Yerel terminali aç ve sunucuya root kullanıcısıyla SSH ile bağlan — araçlar: Windows PowerShell, SSH
- 4. adım — Hermes kurulum betiğini tek satır komutla çalıştır ve kurulumu izle — araçlar: Hermes Agent, curl, bash, uv
- 5. adım — Kurulum sihirbazında model sağlayıcısını seç ve OpenAI Codex ile cihaz kodu üzerinden giriş yap — araçlar: Hermes Agent, OpenAI Codex
- 6. adım — Modeli GPT-5.5 olarak seç ve terminal backend'ini yerel bırak — araçlar: Hermes Agent, GPT-5.5
- 7. adım — Telegram'da BotFather ile yeni bot oluştur ve token'ı al — araçlar: Telegram, BotFather
- 8. adım — Telegram token'ını Hermes kurulumuna yapıştır ve kullanıcı ID'sini userinfobot ile al — araçlar: Hermes Agent, Telegram, userinfobot
- 9. adım — Gateway'i systemd sistem servisi olarak kur ve başlat — araçlar: Hermes Agent, systemd
- 10. adım — Hermes'i terminalden ve Telegram'dan test et — araçlar: Hermes Agent, Telegram
- 11. adım — Ron Weasley kimliğini SOUL dosyasına yazdır — araçlar: Hermes Agent
- 12. adım — Kullanıcı ve ortam bilgilerini USER.md ve MEMORY.md hafıza dosyalarına kaydettir ve dosyaları incele — araçlar: Hermes Agent
- 13. adım — Honcho bulut bellek eklentisini bağla ve peer kartını incele — araçlar: Honcho, Hermes Agent
- 14. adım — Twingate headless istemciyi sunucuya kurdur ve stüdyo ağına bağlan — araçlar: Twingate, Hermes Agent
- 15. adım — Ajanın ağ üzerinde keşif yapmasını iste ve kendi skill'ini oluşturmasını izle — araçlar: Hermes Agent
- 16. adım — Home Assistant skill'ini etkinleştir, bağlan ve lamba ile perdeleri kontrol et — araçlar: Home Assistant, Hermes Agent
- 17. adım — UniFi erişimi ver ve ajanın ağ envanteri çıkarmasını bekle — araçlar: UniFi, Hermes Agent
- 18. adım — Kanban üzerinden HTML Pokémon kart görevi oluştur ve ilerlemeyi izle — araçlar: Hermes Agent, Kanban
## Promptlar
- Ajana IT büyücüsü Ron Weasley kimliği vermek — Ajana Ron Weasley kişiliğini verir: Muggle IT'ye merak saran yetişkin Ron, İngiliz ve sıcak üslup, büyü sözlüğü, güvenlik kuralları. SOUL.md dahil dosyaları güncelleyip bundan sonra bu kimlikle davranmasını ister.
- Ron'un sistem prompt'undaki sert kurallar — Ron'un kimlik kartındaki kısıtlar: cihazlarda açık yetki yoksa salt okunur çalış, işlemden önce teşhis, yıkıcı adımları onayla, önce sade dille başarı/başarısızlık raporu ver.
- Ajanı kullanıcı ve ortam bilgisiyle beslemek (USER.md/MEMORY.md) — Kullanıcı NetworkChuck, adı Chuck; ekip üyeleriyle de konuşulacak, ajan Hostinger VPS'te çalışıyor, ağı anlatılıyor.
- Stüdyo ağına Twingate erişimi kurdurmak — Ron'dan Hostinger bulutunda başsız (headless) Twingate istemcisini kurup stüdyo ağına erişim sağlaması istendi; servis anahtarı verildi.
- Home Assistant ile stüdyo cihazlarını kontrol etmek — Home Assistant skill'ini etkinleştirmesi, IP ve anahtarla bağlanması, sonra lambayı kapatıp mavi açması, panjurları denemesi istendi.
- Ron'a UniFi ağ yönetimi erişimi vermek — UniFi hakkında olabildiğince araştırma yapması, API anahtarı ve kullanıcı hesabı verilerek erişimin kurulması.
- Kanban görevi olarak Pokemon kartı oluşturtmak — NetworkChuck için Pokemon kartı yapılması, benim görüntümü kullan, HTML sayfası olsun ve etkileyici görünsün; default profile atanıyor.
ikinci göz KAPALI: --ikinci-goz yok
