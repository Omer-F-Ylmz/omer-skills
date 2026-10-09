# Neden Her Şeyi Terminalde Yapıyorum? (Claude Code + Modlar)
## Künye
Neden Her Şeyi Terminalde Yapıyorum? (Claude Code + Modlar) · Selma Kocabıyık · süre: 11:23 · tr-orig · https://youtu.be/kBWqtBu4hEI · şema 2
motor: parti 2026-10-09-uzun-5 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 141792 tk · claude-haiku-5-5: claude-haiku-5-5 · 286936 tk
## Özet
Selma Kocabıyık, Claude Code'u neden terminalde kullandığını anlatmak yerine gösteriyor. Web'deki Claude dosyaları göremezken terminaldeki Claude Code dosyaları okuyup düzenler, komut çalıştırır ve kullanıcıyı hatırlar. Masaüstü uygulamasıyla karşılaştırma, Mac terminali ve VS Code terminaliyle kurulum, üç örnek (Hepsi klasör düzenleme, CSV birleştirme, PDF faturadan tablo), en kullanışlı 5 özellik ve yeni 'mod' özelliği anlatılıyor. Kendi modları (Proje Paneli, Clawd Madenci, Clawd Labirent) ve başkalarının modları gösteriliyor; mod kurulumu ve Claude'a mod yazdırma canlı denenip 2 dakikada tamamlanıyor.
## Bölümler
- 0:00 Neden terminal?
- 0:18 Terminalde neler yaptım
- 0:52 Web'deki Claude neden yetmiyor
- 1:28 Yazılımcı olmayanlar için
- 2:03 Masaüstü mü, terminal mi?
- 3:01 Terminale giriş ve kurulum
- 4:53 Üç basit örnek
- 6:34 En kullanışlı 5 özellik
- 7:39 Mod nedir, nasıl kurulur?
- 9:40 Benim modlarım
- 10:54 Başkalarının modları
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Code | yok | CLI | yok | Terminalde çalışan, dosya okuyup düzenleyen, komut çalıştıran yapay zekâ aracı; videonun ana aracı. | 0:18 | Bunların hepsini terminalde cloud kod ile yaptım. (karede: Karede 'Hepsi terminalde · Claude Code ile' etiketi ve sabah brifingi paneli.) |
| Fable 5.1 | yok | teknik | yok | Claude Code oturumunun ana modeli (high effort, Claude Max). | 1:56 | Claude Code v2.1.287, Fable 5.1 with high effort (karede: Terminal başlığında 'Claude Code v2.1.287 · Fable 5.1 with high effort · Claude Max'.) |
| Opus 5.5 | yok | teknik | yok | Web Claude arayüzünde ve başkalarının oturumlarında görünen model. | 1:00 | Opus 5.5 Medium (karede: Web Claude giriş kutusunun altında 'Opus 5.5 Medium Manual'.) |
| Claude (web) | yok | teknik | yok | Dosya yapısını göremeyen web sohbet arayüzü; karşılaştırma için. | 0:52 | web'deki cloud çok akıllı ama dosya yapınızı okuyup göremiyor · kanıt: yok |
| Claude Desktop | yok | teknik | yok | Masaüstü uygulaması; görsel arayüz ve ekran kontrolü için, /desktop ile sohbet taşınır. | 2:03 | masaüstü appi bu konuda daha iyi performans gösterecek (karede: Karede 'Ekran ve uygulama kontrolü: masaüstü' ve Kaynak: Anthropic ile masaüstü uygulaması.) |
| Codex | yok | CLI | yok | OpenAI'ın terminal ajanı; karşılaştırma görselinde. | 2:54 | Codex Cloud Code hangisi olduğu için önemli değil (karede: 'OpenAI Codex (v0.0.0)' terminali, gpt-5.2-codex medium, Kaynak: OpenAI.) |
| Hermes Agent | yok | CLI | yok | Terminalde kullanılan başka bir ajan; karşılaştırmada gösterilir. | 2:56 | Hermis Agent kesinlikle terminalizin içerisinde (karede: 'Welcome to Hermes Agent!' ve 'claude-sonnet-5 · Nous Research' terminal paneli.) |
| Terminal | yok | CLI | yok | Mac'in yerleşik terminali; Spotlight ile açılır. | 3:46 | normalde Macinizi arama yerine gelirseniz terminal yazdığınız zaman (karede: '1. yol · Mac Terminal' etiketi ve Spotlight Search penceresi.) |
| Ghostty | yok | CLI | yok | Özelleştirilmiş terminal uygulaması (arka plan görseli). | 3:01 | Ghostly diye bir uygulama var |
| VS Code | yok | CLI | yok | İçindeki terminalden claude çağrılan editör; proje klasörü video-demo. | 3:50 | Visual Studio Code içerisindeki terminali kullanabilirsiniz (karede: '2. yol · VS Code terminali' etiketi, terminalde 'claud' yazılıyor, Claude Code for VS Code eklentisi.) |
| Claude Code for VS Code | yok | plugin | yok | Anthropic'in VS Code eklentisi sayfası gösterilir. | 3:58 | Claude Code for VS Code: Harness the power of Claude Code (karede: Eklenti sayfası, Anthropic, 26,892,899 indirme, Restart Extensions düğmesi.) |
| Plan modu | yok | ipucu | yok | Shift+Tab ile geçilen, eylem almadan plan yapan mod. | 4:53 | Shift tab yaparak istediğim şekilde değiştirebiliyorum |
| AskUserQuestion | yok | teknik | yok | Claude'un klasör düzenlerken seçenek sorduğu araç. | 5:24 | AskUserQuestion ile uğr... · kanıt: kare (karede: Altta 'AskUserQuestion ile uğr' etiketi, 'Nebulizing… 51 blok'.) |
| anthropic-skills:pdf | yok | skill | yok | PDF faturalardan firma, tarih, tutar çıkarmada yüklenen skill. | 5:52 | Skill(anthropic-skills:pdf) Successfully loaded skill (karede: Terminalde 'Skill(anthropic-skills:pdf) Successfully loaded skill'.) |
| Python | yok | teknik | yok | CSV birleştirme ve PDF ayıklama için Claude'un çalıştırdığı python3 betikleri. | 5:46 | $ ls -A . && python3 - <<'EOF' (karede: Terminalde python3 - <<'EOF' ile csv, glob, unicodedata içe aktarımı.) |
| Remote Control | yok | ipucu | yok | /remote-control ile oturuma telefondan bağlanma. | 6:34 | direkt remote kontrol açıyorum (karede: Terminalde '/remote-control is active' ve telefonda 'Claude Code · Remote Control aktif' bildirimi.) |
| Alt ajanlar | yok | ipucu | yok | İşi birden çok ajana bölüp aynı anda çalıştırma. | 6:34 | birçok farklı ajana bölmesini sağlıyor (karede: 'Running 2 Explore agents…' ve '3 background agents launched'.) |
| superpowers:dispatching-parallel-agents | yok | skill | yok | Paralel alt ajan başlatan skill. | 2:48 | skill(superpowers:dispatching-parallel-agents) (karede: Alt ajanlar karesinde 'Skill(superpowers:dispatching-parallel-agents) Successfully loaded skill'.) |
| Skills | yok | skill | yok | Bir işi bir kez öğretip tekrar kullanma özelliği. | 6:34 | Sadece bir işi bir kere öğretirsiniz ve gerisini o halleder |
| MCP | yok | MCP | yok | MCP ve API bağlantıları; /mcp ile yönetilir. | 7:14 | MCP ve API bağlantılarını güvenli bağlayabiliyorsunuz (karede: 'Manage MCP servers' listesi: higgsfield, mobai, notebooklm-mcp, claude.ai Gmail, Google Drive, computer-use.) |
| notebooklm-mcp | yok | MCP | yok | Kullanıcı MCP'si; 32 araç. | 7:14 | notebooklm-mcp 32 tools (karede: User MCPs altında '✓ notebooklm-mcp 32 tools'.) |
| higgsfield | yok | MCP | yok | Listede görünen MCP; kimlik doğrulaması gerekiyor. | 7:14 | higgsfield needs authentication (karede: User MCPs altında '⚠ higgsfield needs authentication' ve claude.ai higgsfield 133 tools.) |
| Zamanlanmış görevler | yok | ipucu | yok | Zamanlanmış görev oluşturma; masaüstü uygulamasından da yapılır. | 7:35 | zamanlanmış görevler oluşturabilme imkanımız var |
| Mods | yok | plugin | yok | Claude Code'a panel, komut ve araç kuralı ekleyen JavaScript/TypeScript plugin türü. | 7:39 | mod cloud kodunuzun içerisine kendi ekranınızı eklemek demek (karede: 'Mods overview' dokümanı: 'A mod is a plugin that changes how Claude Code looks and behaves'.) |
| /plugin install | yok | plugin | yok | Modu plugin olarak kuran komut. | 8:44 | /plugin install clawd-madenci@clawd-madenci (karede: Üstte '/plugin install clawd-madenci@clawd-madenci', altında 'Install for you (user scope)' seçenekleri.) |
| plugin-authoring | yok | skill | yok | Claude'un mod yazarken yüklediği skill. | 8:02 | Skill(plugin-authoring) Successfully loaded skill (karede: 'Skill(plugin-authoring) Successfully loaded skill' ve 'Bana küçük bir Claude Code modu yaz' istemi.) |
| Clawd Madenci | yok | plugin | https://github.com/selmakcby/clawd-madenci | Claude çalışırken Clawd'ın madende blok kırdığı, TNT patlattığı mod. | 8:20 | cloud'da maden kazmasını sağlayan bir mod (karede: GitHub sayfası selmakcby/clawd-madenci, 'Claude çalışırken Clawd madene iniyor' README.) |
| Proje Paneli | yok | plugin | yok | Prompt üstünde 3 sekmeli panel: çıktılar, siteler, klasör. | 9:40 | prompt verdiğim yerin tam üstünde bir tane proje işareti var (karede: '1 Proje Paneli' kutusu: proje, çıktılar, siteler, klasör; X, Instagram, ManyChat, YouTube Stud.) |
| Clawd Labirent | yok | plugin | yok | Claude çalışırken sağda çok oyunculu Pacman benzeri labirent açan mod. | 10:40 | sağ tarafta bir labirent açılıyor (karede: 'Clawd Labirent · bekleyen herkes aynı labirentte' ekranı, 3 kişi oynuyor.) |
| claude-image-view | yok | plugin | https://github.com/jarrodwatts/claude-image-view | Jarrod Watts'ın yapıştırılan görseller için küçük resim gösteren modu. | 10:54 | başka birisi de oyun yapmış (karede: GitHub jarrodwatts/claude-image-view sayfası; terminalde [Image #1] küçük resmi.) |
| GitHub CLI | yok | CLI | yok | Modu indirmeden önce incelemek için gh api kullanılıyor. | 8:36 | gh api repos/selmakcby/clawd-madenci/contents · kanıt: kare (karede: Terminalde 'for f in plugin/hooks/sahne.js ... gh api "repos/selmakcby/clawd-madenci/contents/$f?ref=..."'.) |
| claude plugin validate | yok | CLI | yok | Mod doğrulama ve test komutları. | 8:06 | claude plugin validate (karede: Terminalde 'M=[yol] claude plugin validate "$M"' ve 'claude plugin test "$M"'.) |
| touched-files modu | yok | plugin | yok | Videoda Claude'a yazdırılan, her turda dokunulan dosya sayısını gösteren mod. | 10:44 | Bana küçük bir Claude Code modu yaz · kanıt: kare (karede: 'Bana küçük bir Claude Code modu yaz: her tur' istemi ve touched-files klasörü.) |
| Remotion | yok | CLI | yok | Kurgu için kullanılan araç (açıklamada). | açıklama | Kullandıklarım: ... Remotion |
| mlx-whisper | yok | CLI | yok | Açıklamada kullanılan araçlar arasında. | açıklama | Kullandıklarım: ... mlx-whisper |
| CapCut | yok | CLI | yok | Kurgu uygulaması; ekranda İndirilenler klasöründeki bağlı medya olarak da geçer. | 5:18 | CapCut/selma-content'e bağlı 49 video (karede: Seçenek metni 'CapCut/selma-content'e bağlı 49 video yerinde kalır'.) |
| Google | yok | CLI | yok | Kurulum sayfasını bulmak için arama. | 4:24 | claude code mac terminal install (karede: Google arama sonuçları; sponsorlu Bing sonucu ve code.claude.com belgeleri.) |
| Claude.ai | yok | teknik | yok | Web'deki Claude sohbet arayüzü; videoda terminal Claude Code ile karşılaştırılıyor. | 0:52 | web'deki cloud çok akıllı ama sizin dosya yapınızı okuyup göremiyor |
| PowerShell | yok | teknik | yok | Windows komut kabuğu; Windows kurulum komutu bu kabukta çalıştırılıyor. | 9:04 | Windows (PowerShell'i aç, yapıştır, Enter) yazısı gösteriliyor. (karede: kanıttan) Windows (PowerShell'i aç, yapıştır, Enter) yazısı gösteriliyor. |
| WSL | yok | teknik | yok | Windows Subsystem for Linux; Linux kurulumu için belirtiliyor. | 9:04 | Mac / Linux / WSL (Terminal'i aç, yapıştır, Enter) yazısı. (karede: kanıttan) Mac / Linux / WSL (Terminal'i aç, yapıştır, Enter) yazısı. |
| pandas | yok | teknik | yok | Veri analizi kütüphanesi; pip ile kurulması gösteriliyor. | 1:10 | $ [yol] -m pip install pandas matplotlib (karede: kanıttan) $ [yol] -m pip install pandas matplotlib |
| matplotlib | yok | teknik | yok | Grafik kütüphanesi; pandas ile birlikte kuruluyor. | 1:10 | $ [yol] -m pip install pandas matplotlib (karede: kanıttan) $ [yol] -m pip install pandas matplotlib |
| İndirilenler klasörünü düzenleme | yok | prompt | yok | Bu bilgisayarın İndirilenler klasörünü dosya türüne göre belgeler, görseller, tablolar, diğer alt klasörlerine ayır; hiçbir şeyi silme. Plan modunda olduğu için eylem almadan plan çıkarır. | 4:53 | kaynak: kare |
| CSV birleştirme ve analiz | yok | prompt | yok | harcamalar klasöründeki üç aylık CSV'yi birleştir, kategori bazında aylık toplamları çıkar, ozet.csv olarak kaydet ve en çok harcanan 3 kategoriyi söyle. | 5:50 | kaynak: kare |
| PDF faturalardan tablo | yok | prompt | yok | faturalar klasöründeki PDF'lerden firma adı, tarih ve tutarı çıkar, faturalar.csv tablosu yap. | 5:54 | kaynak: kare |
| Hafıza gösterimi | yok | prompt | yok | En son ne üzerine çalışıyorduk? İki cümleyle hatırlat. | 1:18 | kaynak: kare |
| Öğretmen örneği | yok | prompt | yok | ders-notları klasöründeki notlarımı incele, toparla ve öğrencilerim için bir sunum hazırla. | 1:50 | kaynak: kare |
| Güvenli mod incelemesi | yok | prompt | yok | Modu bilgisayara indirmeden önce içine gir, analizini yap; güvenliyse indir. | 8:32 | kaynak: kare |
| Claude'a mod yazdırma | yok | prompt | yok | Bana küçük bir Claude Code modu yaz: her tur bittiğinde kısa bir bildirim çıksın ve bu turda kaç dosyaya dokunduğunu söylesin; plugin-authoring skill'ini kullan. | 10:54 | kaynak: altyazı |
| Yazılan modu test | yok | prompt | yok | faturalar.csv dosyasını oku ve toplam tutarı söyle. | 11:15 | kaynak: kare |
## Açıklama bağlantıları
- https://drive.google.com/file/d/1Z9ATJpNEUDpGih2mq3EG7vf1gTqd8Z1V/view — Kurulum ve mod rehberi (PDF) · aday: hayır · Referans doküman; araç değil. · sınıf: diğer
- https://github.com/selmakcby/clawd-madenci — Clawd Madenci mod deposu · aday: evet (Clawd Madenci) · Videoda kurulan ve gösterilen mod. · sınıf: diğer
- https://youtube.com/@selma.builds — Kanal sayfası · aday: hayır · Sosyal profil; araç değil. · sınıf: diğer
- https://instagram.com/selma.builds — Instagram profili · aday: hayır · Sosyal profil; araç değil. · sınıf: diğer
- https://x.com/selmaaii — X profili · aday: hayır · Sosyal profil; araç değil. · sınıf: diğer
- https://selma.codes — Kişisel site · aday: hayır · Portfolyo/kişisel site. · sınıf: diğer
## Site/UI teknikleri
- EKSİK: formda site/UI tekniği yok (kısmi kabul)
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| curl -fsSL https://claude.ai/install.sh / bash | Mac/Linux/WSL'de Claude Code'u kurar. (karede: Terminalde '(base) mac:~ selma$ curl -fsSL https://claude.ai/install.sh / bash'.) | 4:38 | kare |
| claude | Seçili proje klasöründe Claude Code'u başlatır. (karede: VS Code terminalinde 'claud' yazılıyor.) | 3:50 | kare |
| irm https://claude.ai/install.ps1 / iex | Windows PowerShell'de Claude Code'u kurar. (karede: Rehberde 'Windows (PowerShell'i aç...)' altında komut.) | 9:04 | kare |
| curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd | Windows CMD'de Claude Code'u kurar. (karede: Rehberde 'Windows (CMD kullanıyorsan)' komutu.) | 9:04 | kare |
| claude --version | Kurulumu doğrular. (karede: Terminalde 'mac:video-demo selma$ claude --version'.) | 8:56 | kare |
| /plugin marketplace add selmakcby/clawd-madenci | Mod pazaryerini Claude Code'a tanıtır. | açıklama | açıklama |
| /plugin install clawd-madenci@clawd-madenci | Clawd Madenci modunu kurar. (karede: Üstte '/plugin install clawd-madenci@clawd-madenci' ve kapsam seçenekleri.) | 8:44 | kare |
| claude update | Claude Code'u günceller; plugin hata verirse. (karede: Rehberde 'güncellemek için: claude update'.) | 9:08 | kare |
| /desktop | Terminaldeki sohbeti Claude Desktop'a taşır. (karede: Girişte '/desktop' ve 'Continue the current session in Claude Desktop'.) | 2:38 | kare |
| /remote-control | Oturumu telefondan sürdürmek için uzaktan kontrolü açar. (karede: Terminalde '/remote-control is active'.) | 6:36 | kare |
| /mcp | MCP sunucularını yönetir. (karede: Girişte '/mcp' ve 'Manage MCP servers'.) | 7:12 | kare |
| claude plugin list | Kurulu plugin'leri listeler. (karede: 'claude plugin list → clawd-madenci@clawd-madenci 0.1.0, etkin.') | 2:38 | kare |
| python3 - <<'EOF' (ls -A . ile birlikte) | Klasördeki CSV'leri Python ile okuyup birleştiren betiği çalıştırır. (karede: Claude Code'da '$ ls -A . && python3 - <<'EOF'' komutu çalışıyor.) | 5:46 | kare |
| [yol] -m pip install pandas matplotlib | pandas ve matplotlib kütüphanelerini Python ortamına kurar. (karede: Claude Code'da pip install pandas matplotlib komutu yazılı.) | 1:10 | kare |
| gh api "repos/selmakcby/clawd-madenci/contents/$f?ref=8413933a" -H "Accept: application/vnd.github.raw" | Mod dosyalarını GitHub'dan indirmeden içeriğini okuyarak inceler. (karede: Claude Code'da gh api ile mod dosyası okuma komutu yazılı.) | 8:36 | kare |
| claude plugin validate "$M" ve claude plugin test "$M" 2>&1 / tail -60 | Yazılan modu doğrular ve test eder. (karede: Claude Code'da plugin validate ve plugin test komutları yazılı.) | 8:06 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Terminaldeki Claude Code dosyaları okuyup anında değiştirir, paket indirir ve kullanıcıyı hatırlar. | 0:52 | özellik |
| Geliştirme, paketler ve script işleri için terminal daha sorunsuz; ekran/uygulama kontrolü için masaüstü uygulaması daha iyi. | 2:03 | karşılaştırma |
| Mod, kurulumdan sonra yeniden başlatma gerektirmeden bir sonraki işte ekranda belirir. | 8:39 | özellik |
| Mod yazdırma yaklaşık 2 dakika sürdü ve tek satır kod yazılmadı. | 10:54 | sayısal |
| Hazır modu indirmeden önce Claude'a incelettirmek öneriliyor. | 8:39 | öneri |
| Claude'u doğru proje klasöründe çalıştırmak gerekir; önce klasörü aç, sonra claude yaz. | 6:22 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Claude Code | Claude Code | Neden her şeyi terminalle yapıyorum |
| kare 0:20 | Fable 5.1 | Fable 5.1 | Fable 5.1 [high+think] |
| kare 1:00 | Opus 5.5 | Opus 5.5 | Opus 5.5 Medium |
| konuşma 0:52 | Web Claude | Claude (web) | web'deki cloud çok akıllı |
| kare 0:50 | CLAUDE.md | aday değil: başka adayın parçası (Claude Code) | CLAUDE.md Hafıza etiketi |
| kare 0:34 | stripe | aday değil: konu dışı | Web siteleri görselinde geçer |
| kare 1:24 | hooks | Mods | Claude Code calls both kinds hooks |
| konuşma 2:03 | Masaüstü appi | Claude Desktop | masaüstü appi de var |
| kare 2:54 | OpenAI Codex | Codex | OpenAI Codex (v0.0.0) |
| kare 2:56 | Hermes Agent | Hermes Agent | Welcome to Hermes Agent! |
| kare 2:56 | claude-sonnet-5 | aday değil: başka adayın parçası (Hermes Agent) | Hermes içinde model |
| kare 3:20 | Terminal | Terminal | Last login: Sat Oct 3 |
| konuşma 3:01 | Ghostty | Ghostty | Ghostly diye bir uygulama |
| kare 3:46 | VS Code | VS Code | VS Code terminali |
| kare 3:46 | GitHub Copilot, MSSQL | aday değil: konu dışı | VS Code karşılama ekranında |
| kare 3:58 | Claude Code for VS Code | Claude Code for VS Code | eklenti sayfası |
| kare 4:24 | Google arama | Google | claude code mac terminal install |
| kare 4:24 | Bing sponsorlu sonuç | aday değil: sponsor/reklam | Sponsorlu Sonuç |
| kare 4:30 | Cursor | aday değil: konu dışı | sözlük eşleşmesi, belge sayfasında |
| konuşma 4:53 | Plan modu | Plan modu | plan modunu alıyorum |
| kare 5:24 | CapCut | CapCut | CapCut/selma-content'e bağlı |
| kare 5:24 | AskUserQuestion | AskUserQuestion | AskUserQuestion ile uğr |
| kare 5:52 | anthropic-skills:pdf | anthropic-skills:pdf | Skill(anthropic-skills:pdf) |
| kare 5:46 | python3 | Python | python3 - <<'EOF' |
| konuşma 6:34 | Remote Control | Remote Control | remote control |
| konuşma 6:34 | Alt ajanlar | Alt ajanlar | alt ajanlar |
| kare 2:48 | superpowers | superpowers:dispatching-parallel-agents | skill(superpowers:dispatching-parallel-agents) |
| konuşma 6:34 | Skills | Skills | yeteneklerimiz |
| kare 7:14 | MCP listesi | MCP | Manage MCP servers |
| kare 7:14 | notebooklm-mcp | notebooklm-mcp | notebooklm-mcp 32 tools |
| kare 7:12 | higgsfield | higgsfield | higgsfield needs authentication |
| kare 7:14 | claude.ai Gmail, Calendar, Drive, Docs | aday değil: başka adayın parçası (MCP) | claude.ai bağlayıcıları listede |
| konuşma 7:35 | Zamanlanmış görevler | Zamanlanmış görevler | zamanlanmış görevler |
| kare 7:36 | Mods dokümanı | Mods | Mods overview |
| kare 7:36 | React | aday değil: konu dışı | dokümanda geçen örnek |
| kare 8:44 | /plugin install | /plugin install | /plugin install clawd-madenci@clawd-madenci |
| kare 8:02 | plugin-authoring | plugin-authoring | Skill(plugin-authoring) |
| kare 8:06 | claude plugin validate/test | claude plugin validate | claude plugin validate |
| kare 8:20 | Clawd Madenci | Clawd Madenci | selmakcby/clawd-madenci |
| kare 8:36 | gh api | GitHub CLI | gh api repos/... |
| kare 9:04 | PowerShell, WSL | aday değil: konu dışı | Windows/WSL kurulum rehberi, videoda kullanılmadı |
| kare 9:04 | install.ps1 / install.cmd | aday değil: başka adayın parçası (Claude Code) | Windows kurulum komutları |
| kare 9:40 | Proje Paneli | Proje Paneli | Proje Paneli |
| kare 9:40 | remotion/ klasörü | Remotion | remotion/ dosya |
| konuşma 10:40 | Clawd Labirent | Clawd Labirent | labirent açılıyor |
| kare 10:30 | Ask Gemini | aday değil: konu dışı | Chrome'da menü düğmesi |
| kare 10:32 | claude-image-view | claude-image-view | Claude mod for image rendering |
| kare 10:52 | touched-files modu | touched-files modu | touched-files klasörü |
| kare 10:52 | code-reviewer agent | aday değil: konu dışı | çalıştırılmadı |
| açıklama | Remotion, mlx-whisper, CapCut, Ghostty, VS Code | Remotion | Kullandıklarım listesi |
| açıklama | mlx-whisper | mlx-whisper | Kullandıklarım listesi |
| açıklama | Cowork, @alexchristou_, @jarrodwatts, @ClaudeDevs | aday değil: konu dışı | Anthropic görselleri ve başka modlar; videoda ayrıca anlatılmadı |
| açıklama | PDF rehberi | aday değil: konu dışı | Referans doküman |
| yorum | Jev guard modu, Herdr, antigravity, WrongStack | aday değil: konu dışı | Yorumlarda anılıyor, videoda yok |
| linkli sayfa code.claude.com | Claude Code belgeleri | aday değil: başka adayın parçası (Claude Code) | Belge sayfaları |
| linkli sayfa anthropic.com | Anthropic | aday değil: konu dışı | Şirket sayfası |
## Kareden okunanlar
- 0:00: Kullanıcı yorumları ekranı; 'Claude code'u neden vscode da değil de terminalde kullanıyorsun?' gibi yorumlar.
- 1:18: Resume session listesi: 'Harcamalar klasörü CSV birleştirme' 9 hours ago, 413.9KB; Fable 5.1 [high+think].
- 3:50: Terminalde '(base) mac:~ selma$ claud' yazılıyor; Claude Code for VS Code, Anthropic.
- 4:30: Dokümanda 'curl -fsSL https://claude.ai/install.sh / bash' kurulum satırı.
- 7:14: /mcp: 9 sunucu; higgsfield, mobai (✗), notebooklm-mcp 32 tools, claude.ai Gmail/Google Calendar/Drive.
- 8:44: '2 mods active · clawd-madenci, proje-paneli' ve plugin güvenlik uyarısı.
- 9:04: Rehber: Mac için curl -fsSL https://claude.ai/install.sh / bash; Windows için irm https://claude.ai/install.ps1 / iex; CMD için install.cmd; sonra claude --version.
## Belirsizlikler
- Ana modelde 'Fable 5.1' ekranda görünüyor; Opus 5.5 farklı oturumlarda geçiyor, hangisinin hangi işte kullanıldığı net değil.
- Remotion, mlx-whisper ve CapCut yalnız açıklamada; videoda kullanıldıkları doğrulanmadı (CapCut karede yalnız İndirilenler bağlamında geçiyor).
- Hermes Agent sesi bulanık ('hermisagent'); karede doğrulandı.
- Cowork, Alex Christou ve @ClaudeDevs modları açıklamada geçiyor; videoda adlarıyla gösterilmedi.
- Yorumlardaki jev, Herdr, antigravity, WrongStack, Descript, gstack videoda gösterilmediği için aday değil.
- Bing/'Claude Code for MacOS' sponsorlu arama sonucu reklam; araç değil.
- Mod güvenliği ile ilgili 'Claude Code 2.1.287 ve üstü' gereksinimi açıklamadan; video süresi 11:23 ve bazı kare zamanları OCR'dan yaklaşık.
- EKSİK: rapor (bölüm eksik: ## Site/UI teknikleri)
## Atlanan segment oranı
0/17 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://claude.ai/install.sh | 0:08 | ekran | hayır |
| https://www.bing.com/ | 4:24 | ekran | hayır |
| https://code.claude.com | 4:24 | ekran | hayır |
| https://code.claude.com/docs/en/mcp | 7:14 | ekran | hayır |
| code.claude.com/docs/en/plugins/mods/overview | 7:32 | ekran | hayır |
| github.com/selmakcby/clawd-madenci | 8:20 | ekran | evet |
| github.com/jarrodwatts/claude-image-view | 8:24 | ekran | evet |
| https://claude.ai/install.ps1 | 9:04 | ekran | hayır |
| https://claude.ai/install.cmd | 9:04 | ekran | hayır |
| https://drive.google.com/file/d/1Z9ATJpNEUDpGih2mq3EG7vf1gTqd8Z1V/view | açıklama | açıklama | hayır |
| https://github.com/selmakcby/clawd-madenci | açıklama | açıklama | evet |
| https://youtube.com/@selma.builds | açıklama | açıklama | hayır |
| https://instagram.com/selma.builds | açıklama | açıklama | hayır |
| https://x.com/selmaaii | açıklama | açıklama | hayır |
| https://selma.codes | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — Claude Code'un ne yaptığı ve web Claude farkı anlatılır — araçlar: Claude Code, Claude (web)
- 2. adım — Masaüstü uygulaması ile terminal karşılaştırılır, /desktop gösterilir — araçlar: Claude Desktop, Claude Code, Codex, Hermes Agent
- 3. adım — Mac Terminali ve Ghostty ile terminal açılır — araçlar: Terminal, Ghostty
- 4. adım — VS Code terminali açılır, video-demo klasöründe claude çağrılır — araçlar: VS Code, Claude Code
- 5. adım — Kurulum sayfası aranır ve install.sh komutu çalıştırılır — araçlar: Google, Terminal
- 6. adım — Plan moduna geçilip İndirilenler düzenleme planlanır — araçlar: Claude Code, Plan modu, AskUserQuestion
- 7. adım — Harcama CSV'leri birleştirilip ozet.csv üretilir — araçlar: Claude Code, VS Code, Python
- 8. adım — PDF faturalardan faturalar.csv çıkarılır — araçlar: Claude Code, anthropic-skills:pdf, Python
- 9. adım — Remote Control telefondan açılır — araçlar: Remote Control
- 10. adım — Alt ajanlar paralel klasör incelemesi yapar — araçlar: Alt ajanlar, superpowers:dispatching-parallel-agents
- 11. adım — MCP bağlantıları /mcp ile gösterilir — araçlar: MCP, notebooklm-mcp, higgsfield
- 12. adım — Mod belgesi gösterilir; Claude'a mod yazdırma anlatılır — araçlar: Mods, plugin-authoring
- 13. adım — Clawd Madenci GitHub'dan incelenip kurulur — araçlar: GitHub CLI, /plugin install, Clawd Madenci
- 14. adım — Kendi modları ve başkalarının modları gösterilir — araçlar: Proje Paneli, Clawd Labirent, claude-image-view
- 15. adım — Claude'a küçük mod yazdırılır, doğrulanır ve test edilir — araçlar: Claude Code, plugin-authoring, claude plugin validate
## Promptlar
- İndirilenler klasörünü düzenleme — Bu bilgisayarın İndirilenler klasörünü dosya türüne göre belgeler, görseller, tablolar, diğer alt klasörlerine ayır; hiçbir şeyi silme. Plan modunda olduğu için eylem almadan plan çıkarır.
- CSV birleştirme ve analiz — harcamalar klasöründeki üç aylık CSV'yi birleştir, kategori bazında aylık toplamları çıkar, ozet.csv olarak kaydet ve en çok harcanan 3 kategoriyi söyle.
- PDF faturalardan tablo — faturalar klasöründeki PDF'lerden firma adı, tarih ve tutarı çıkar, faturalar.csv tablosu yap.
- Hafıza gösterimi — En son ne üzerine çalışıyorduk? İki cümleyle hatırlat.
- Öğretmen örneği — ders-notları klasöründeki notlarımı incele, toparla ve öğrencilerim için bir sunum hazırla.
- Güvenli mod incelemesi — Modu bilgisayara indirmeden önce içine gir, analizini yap; güvenliyse indir.
- Claude'a mod yazdırma — Bana küçük bir Claude Code modu yaz: her tur bittiğinde kısa bir bildirim çıksın ve bu turda kaç dosyaya dokunduğunu söylesin; plugin-authoring skill'ini kullan.
- Yazılan modu test — faturalar.csv dosyasını oku ve toplam tutarı söyle.
