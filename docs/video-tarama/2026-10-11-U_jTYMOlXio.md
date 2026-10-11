# Somebody Vibe Coded Microsoft Office, and I tried it (so you don't have to)
## Künye
Somebody Vibe Coded Microsoft Office, and I tried it (so you don't have to) · FUTC · süre: 22:11 · en-orig · https://youtu.be/U_jTYMOlXio · şema 2
motor: parti 2026-10-11-uzun · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (57)
kareler: girdi ≤40000 jeton için 60→57
claude-sonnet-5-5: claude-sonnet-5-5 · 73063 tk · claude-haiku-5-5: claude-haiku-5-5 · 121646 tk
## Özet
FUTC, ArtCraft ekibinin saf Rust ile yazdığı açık kaynaklı Microsoft Office klonlarını dener: WordCraft (Word), GridCraft (Excel), DeckCraft (PowerPoint). Linux/Arch üzerinde kaynaktan derler (cargo), arayüzleri dener ve GridCraft ile DeckCraft'ı MCP üzerinden Claude Code ile sürer. Word klonu en zayıfı (italik hatası, metin kaydırma), Excel klonu daha iyi (grafikler, otomatik güncelleme), PowerPoint klonu MCP ile eğlenceli ama animasyonlar takılıyor. Sonuç: çok erken aşamada, olgun bir alternatif için LibreOffice öneriliyor.
## Bölümler
- 0:00 Bu nedir?
- 2:53 Nasıl kurulur
- 3:42 WordCraft (Word alternatifi)
- 8:31 GridCraft (Excel alternatifi)
- 12:41 DeckCraft (PowerPoint alternatifi)
- 20:27 Sonuç
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| WordCraft | yok | CLI | https://github.com/storytold/wordcraft | Saf Rust ile yazılmış açık kaynaklı Word klonu; .docx okur/yazar, MCP ve CLI sunar | 3:42 | Word benzeri şerit arayüzü açılıyor, örnek belge gösteriliyor (karede: 'The Open Studio Handbook — Word...' başlıklı, Home/Insert/Draw/Design şeritli Word benzeri pencere) |
| GridCraft | yok | CLI | https://github.com/storytold/gridcraft | Saf Rust Excel klonu; grafikler, pivot tablolar, MCP sunucusu | 8:44 | cargo run --release -p gridcraft -- --sample sales komutu ve Quarterly Sales Dashboard (karede: Terminalde cargo run --release -p gridcraft -- --sample sales yazılı; sağda README Quick start) |
| DeckCraft | yok | CLI | https://github.com/storytold/deckcraft | Saf Rust PowerPoint klonu; geçişler, animasyonlar, MCP ile sürülebilir | 12:41 | Deckcraft the PowerPoint alternative. Get clone that. Open that. |
| ArtCraft | yok | teknik | https://github.com/storytold/artcraft | Üç Office klonunu ve Adobe klonlarını yapan ekip/proje | 0:34 | Crafting Apps sayfası: Seven apps. One craft. (karede: getartcraft.com Crafting Apps sayfası, PhotoCraft/VectorCraft/FilmCraft/LightCraft simgeleri) |
| Rust | yok | teknik | yok | Tüm klonların yazıldığı dil; hızlı ve her platformda çalışır | 1:00 | these are built completely in 100% pure Rust |
| Claude Code | yok | CLI | yok | GridCraft ve DeckCraft MCP sunucularını sürmek ve içerik üretmek için kullanıldı | 10:48 | Terminalde claude mcp add gridcraft komutu ve Claude Code oturumu (karede: Terminal: '[yol] claude - claude', 'Claude Code'll be able to read, edit,') |
| MCP | yok | MCP | yok | Uygulamaları yapay zekâya bağlayan bağlantı noktası; GridCraft ve DeckCraft içinde yerleşik | 10:00 | all of these have an MCP server built in |
| gridcraft-cli | yok | CLI | yok | GridCraft başsız MCP sunucusu/CLI; PATH'e eklenmesi gerekti | 10:52 | claude mcp add gridcraft -- gridcraft-cli mcp (karede: Terminalde 'claude mcp add gridcraft -- gridcraft-cli mcp' satırı) |
| deckcraft-cli | yok | CLI | yok | DeckCraft komut satırı ve MCP sunucusu (--connect 7990 ile çalışan uygulamayı sürer) | 13:00 | deckcraft-cli run --sample --cmd 'slide.new=...' komutu (karede: README'de 'deckcraft-cli run --sample --cmd slide.new=... --save hell') |
| Cargo | yok | CLI | yok | Rust derleme aracı; klonlar kaynaktan derlenip çalıştırıldı | 8:44 | cargo run --release -p gridcraft (karede: Terminal komutu cargo run --release -p gridcraft -- --sample sales) |
| Git | yok | CLI | yok | Depoları klonlamak için kullanıldı | 8:32 | git clone git@github.com:storytold/gridcraft.git (karede: Terminalde git clone git@github.com:storytold/gridcraft.git ve Receiving objects 100%) |
| GitHub | yok | teknik | yok | Depolar ve release indirmeleri burada | 2:54 | WordCraft v0.3.0 release sayfası (karede: github.com/storytold/wordcraft/releases/tag/v0.3.0, WordCraft v0.3.0 Latest) |
| LibreOffice | yok | teknik | yok | Olgun, ücretsiz açık kaynak ofis paketi; videonun önerisi | 21:02 | LibreOffice 26.8 sitesi gösteriliyor, indirmeyi öneriyor (karede: LibreOffice ana sayfası: 'LibreOffice is an open source office suite created by you, for you.') |
| Poppins | yok | teknik | yok | DeckCraft örnek destesinde kullanılan yazı tipi | 15:06 | Claude çıktısı: deck has the Poppins and Nunito Sans fonts (karede: Claude çıktısında 'the window. That deck has the Poppins and Nunito Sans fonts') |
| Nunito Sans | yok | teknik | yok | DeckCraft destesinde kullanılan yazı tipi | 15:06 | Poppins ve Nunito Sans fontları geçiyor (karede: Claude çıktısında Poppins and Nunito Sans fonts) |
| Aptos Display | yok | teknik | yok | WordCraft örnek belgesinde stil yazı tipi alanında görünen font | 3:42 | Font kutusunda Aptos Display, 28 · kanıt: kare (karede: Font alanında 'Aptos Display' ve 28 yazıyor) |
| egui | yok | teknik | yok | Klonların arayüz kütüphanesi (eframe/egui derleme günlüğünde) | 13:30 | Compiling egui v0.36.2, eframe v0.36.2 (karede: Derleme günlüğünde eframe v0.36.2, egui v0.36.2, egui-wgpu v0.36.2) |
| wgpu | yok | teknik | yok | GPU çizim katmanı; derleme günlüğünde | 13:30 | egui-wgpu, wgpu-core-deps ve gpu-allocator derleniyor (karede: egui-wgpu v0.36.2, wgpu-naga-bridge v30.0.1 satırları) |
| Vello | yok | teknik | yok | Vektör çizim motoru; DeckCraft render bağımlılığı | 12:52 | vello_cpu v0.2.0 derleniyor (karede: Derleme günlüğünde vello_cpu v0.2.0, krilla v0.8.2) |
| Krilla | yok | teknik | yok | PDF dışa aktarma kütüphanesi (DeckCraft bağımlılığı) | 12:52 | krilla v0.8.2 derleme satırı (karede: deckcraft-render, krilla v0.8.2, vello_cpu v0.2.0) |
| Symphonia | yok | teknik | yok | Ses çözme kütüphanesi (DeckCraft medya desteği) | 12:48 | symphonia-codec-aac vb. derleniyor (karede: symphonia v0.5.5 ve codec/format paketleri derleme günlüğünde) |
| Trunk | yok | CLI | yok | GridCraft web sürümünü derlemek için README komutu | 8:46 | cd apps/gridcraft-web && trunk build --relea.. (karede: Terminalde 'cd apps/gridcraft-web && trunk build --relea..') |
| WebAssembly | yok | teknik | yok | Klonların tarayıcıda çalışması için hedef | 1:10 | README: in the browser via WebAssembly (karede: WordCraft README: 'runs natively on macOS, Windows, Linux and BSD, and in the browser via WebAssembly') |
| PhotoCraft | yok | teknik | https://github.com/storytold/photocraft | Photoshop benzeri açık kaynak görüntü editörü; önceki videoda anlatıldı. | açıklama | PhotoCraft (Photoshop alternative), LightCraft (Lightroom alternative) |
| LightCraft | yok | teknik | https://github.com/storytold/lightcraft | Lightroom benzeri fotoğraf kütüphanesi ve RAW geliştirici; önceki videoda anlatıldı. | açıklama | LightCraft (Lightroom alternative) |
| FilmCraft | yok | teknik | https://github.com/storytold/filmcraft | Premiere Pro benzeri video düzenleyici; önceki videoda anlatıldı. | açıklama | FilmCraft (Premiere Pro alternative) |
| VectorCraft | yok | teknik | yok | Illustrator benzeri vektör çizim uygulaması; önceki videoda anlatıldı. | açıklama | VectorCraft (Adobe Illustrator alternative) |
| EffectCraft | yok | teknik | yok | After Effects benzeri hareketli grafik uygulaması; önceki videoda anlatıldı. | açıklama | EffectCraft (After Effects alternative) |
| GridCraft MCP bağlantısını doğrulama | yok | prompt | yok | Claude'a GridCraft MCP sunucusunu görüp görmediği ve kullanıp kullanamayacağı soruldu. | 10:31 | kaynak: altyazı |
| GridCraft'ta sahte satış verisi üretme | yok | prompt | yok | Yeni bir belge oluşturup içine rastgele veri eklemesi istendi. | 10:31 | kaynak: altyazı |
| MCP ile grafik üretme | yok | prompt | yok | Tablodan grafik yapıp ekran görüntüsü alması istendi. | 11:12 | kaynak: kare |
| Ek grafik ve veri üretme | yok | prompt | yok | Tabloya kurumsal jargonlu bir 'sinerji hattı' grafiği daha eklemesi istendi. | 11:32 | kaynak: altyazı |
| DeckCraft MCP kurulumu | yok | prompt | yok | DeckCraft'ın MCP'sini kurup erişmeye çalışması istendi. | 14:41 | kaynak: altyazı |
| MCP bağlantı testi | yok | prompt | yok | Çalışıp çalışmadığını test etmek için bir şey eklemesi istendi. | 14:41 | kaynak: altyazı |
| Eğlenceli sunum içeriği üretme | yok | prompt | yok | Sunuma kurumsal jargon ve komik kurumsal suçlar eklemesi istendi. | 15:41 | kaynak: altyazı |
| Animasyon ekleme | yok | prompt | yok | Tüm slaytlara bol animasyon eklemesi istendi. | 17:44 | kaynak: kare |
## Açıklama bağlantıları
- https://github.com/storytold/wordcraft — WordCraft deposu · aday: evet (WordCraft) · Videoda denenen araç; izleyici indirebilir · sınıf: diğer
- https://github.com/storytold/gridcraft — GridCraft deposu · aday: evet (GridCraft) · Videoda denenen araç · sınıf: diğer
- https://github.com/storytold/deckcraft — DeckCraft deposu · aday: evet (DeckCraft) · Videoda denenen araç · sınıf: diğer
- https://futc.gumroad.com/l/analogvibes2/n1b2iu0 — Yaratıcının Gumroad ürünü · aday: hayır · Videoda kullanılmayan kendi ürün sayfası; içerik doğrulanamadı · sınıf: diğer
- https://apps.apple.com/app/apple-store/id6739345616?pt=127502132&ct=youtubelaunch&mt=8 — App Store uygulaması (Polychrome) · aday: hayır · Videoda kullanılmayan, yaratıcının tanıttığı uygulama; izleme parametreli · sınıf: affiliate
- https://share.epidemicsound.com/vi9i60 — Epidemic Sound müzik bağlantısı · aday: hayır · Yalnız müzik kaynağı; videoda anlatılan araç değil · sınıf: affiliate
- https://geni.us/D2c4 — Ekipman bağlantısı · aday: hayır · Gear listesi, videoda kullanılan yazılım değil · sınıf: affiliate
- https://prf.hn/l/JzY20PN — Ekipman bağlantısı · aday: hayır · Gear listesi affiliate · sınıf: affiliate
- https://prf.hn/l/1MVRO4X — Ekipman bağlantısı · aday: hayır · Gear listesi affiliate · sınıf: affiliate
- https://prf.hn/l/ZYo9NLW — Ekipman bağlantısı · aday: hayır · Gear listesi affiliate · sınıf: affiliate
- https://prf.hn/l/3YVDvvY — Ekipman bağlantısı · aday: hayır · Gear listesi affiliate · sınıf: affiliate
- https://prf.hn/l/QxY2ood — Ekipman bağlantısı · aday: hayır · Gear listesi affiliate · sınıf: affiliate
- https://prf.hn/l/vybM3OM — Ekipman bağlantısı · aday: hayır · Gear listesi affiliate · sınıf: affiliate
- https://prf.hn/l/GlRaeYQ — Ekipman bağlantısı · aday: hayır · Gear listesi affiliate · sınıf: affiliate
- https://geni.us/FfmyXd — Ekipman bağlantısı · aday: hayır · Gear listesi affiliate · sınıf: affiliate
- https://prf.hn/l/5NLajnm — Ekipman bağlantısı · aday: hayır · Gear listesi affiliate · sınıf: affiliate
- https://geni.us/eAw9 — Ekipman bağlantısı · aday: hayır · Gear listesi affiliate · sınıf: affiliate
- https://geni.us/KBJo6r — Ekipman bağlantısı · aday: hayır · Gear listesi affiliate · sınıf: affiliate
- https://geni.us/rI8A — Ekipman bağlantısı · aday: hayır · Gear listesi affiliate · sınıf: affiliate
- https://geni.us/EzdqdA — Ekipman bağlantısı · aday: hayır · Gear listesi affiliate · sınıf: affiliate
- https://geni.us/ySx4kC — Ekipman bağlantısı · aday: hayır · Gear listesi affiliate · sınıf: affiliate
- https://geni.us/k2g8N — Ekipman bağlantısı · aday: hayır · Gear listesi affiliate · sınıf: affiliate
- https://geni.us/ZwkBEC3 — Ekipman bağlantısı · aday: hayır · Gear listesi affiliate · sınıf: affiliate
- https://geni.us/Fai9kNo — Ekipman bağlantısı · aday: hayır · Gear listesi affiliate · sınıf: affiliate
- https://strapnstyles.de/en — Aksesuar mağazası · aday: hayır · Videoyla ilgisiz mağaza sayfası · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Üst gezinme çubuğu (navigation bar) | Üst gezinme çubuğu (HOME, IMAGE, VIDEO, RESOURCES, LAUNCH APP) ve sağda uygulama başlatma düğmesi. (karede: getartcraft.com sayfasının üstünde HOME/IMAGE/VIDEO menüsü ve LAUNCH APP düğmesi) | 0:34 | kare |
| Simge ızgarası (icon grid) | Yedi uygulama simgesi (PhotoCraft, VectorCraft, FilmCraft, LightCraft, PdfCraft, EffectCraft, DesignCraft) yan yana dizili. (karede: 'Seven apps. One craft.' başlığı altında yedi renkli uygulama simgesi) | 0:34 | kare |
| Sekmeli içerik geçişi (tabbed content) | Lineup bölümünde numaralı sekmeler (01 IMAGE EDITOR, 02 VECTOR ILLUSTRATION...) ile uygulama kartları değişiyor. (karede: 'PICK A CRAFT TO EXPLORE' yazısı altında 01-04 numaralı sekmeler ve kartlar) | 0:44 | kare |
| Yatay kaydırma (horizontal scroll) | Uygulama kartları üst üste ve yatay bölümler halinde kayarak açılıyor. (karede: PhotoCraft, VectorCraft, FilmCraft kartlarının yan yana kayan bölümü) | 1:00 | kare |
| Üzerine gelince büyüme (hover scale) | Kartlarda hover ile büyüyen önizleme görselleri. (karede: Fare kartın üzerinde iken PhotoCraft önizleme görseli büyük açılıyor) | 0:44 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| git clone git@github.com:storytold/wordcraft.git | WordCraft deposunu klonlar (karede: Terminalde git clone git@github.com:storytold/wordcraft ... ve Cloning into wordcraft) | 3:26 | kare |
| cargo run --release -p wordcraft -- report.docx | WordCraft'ı release modunda derleyip belgeyle açar (karede: README'de cargo run --release -p wordcraft -- report.docx) | 3:31 | kare |
| git clone git@github.com:storytold/gridcraft.git | GridCraft deposunu klonlar (karede: Terminalde git clone git@github.com:storytold/gridcraft.git) | 8:32 | kare |
| cd gridcraft/ | Klonlanan dizine girer (karede: Terminalde 'cd gridcraft/' ve ~/gridcraft main) | 8:34 | kare |
| cargo run --release -p gridcraft -- --sample sales | GridCraft'ı örnek satış belgesiyle derleyip açar (karede: Terminalde komut yazılı) | 8:44 | kare |
| cd apps/gridcraft-web && trunk build --release | GridCraft web sürümünü derler (README) (karede: 'cd apps/gridcraft-web && trunk build --relea..') | 8:46 | kare |
| gridcraft --control 7979 | GridCraft'ı JSON-lines kontrol kanalıyla başlatır (karede: Belgede 'gridcraft --control 7979') | 10:16 | kare |
| gridcraft-cli mcp --connect 7979 | Çalışan GridCraft penceresine MCP köprüsü kurar (karede: Belgede 'gridcraft-cli mcp --connect 7979') | 10:16 | kare |
| claude | Claude Code oturumunu başlatır | 10:31 | altyazı |
| claude mcp add gridcraft -- gridcraft-cli mcp | GridCraft MCP sunucusunu Claude Code'a ekler (karede: Terminalde komut satırı) | 10:52 | kare |
| /mcp | Claude Code'da MCP bağlantılarını yeniler/gösterir (karede: Claude yanıtı: 'restart Claude Code or run /mcp') | 11:02 | kare |
| cargo run --release -p deckcraft | DeckCraft arayüzünü derleyip açar (karede: Terminalde cargo run --release -p deckcraft) | 14:42 | kare |
| deckcraft-cli run --sample --cmd 'slide.new={"layout":"titleOnly","title":"Hello"}' --save hello | Örnek desteye yeni slayt ekleyip kaydeder (karede: README satırı deckcraft-cli run --sample --cmd 'slide.new=...') | 13:00 | kare |
| deckcraft-cli mcp | DeckCraft'ı başsız MCP sunucusu olarak çalıştırır (karede: README: '# MCP server over stdio (headless)') | 12:56 | kare |
| deckcraft-cli mcp --connect 7990 | Çalışan DeckCraft uygulamasını MCP ile sürer (karede: Claude: 'deckcraft-cli mcp --connect 7990') | 15:08 | kare |
| target/release/deckcraft --control 7990 | DeckCraft GUI'yi 7990 kontrol portuyla başlatır (karede: Terminalde target/release/deckcraft --control 7990) | 15:06 | kare |
| cd wordcraft/ | Klonlanan WordCraft klasörüne girer. (karede: Terminalde 'cd wordcraft/' satırı, prompt ~/wordcraft main) | 3:26 | kare |
| cargo run --release -p wordcraft | WordCraft'ı release modunda derler ve çalıştırır (README). (karede: README'de 'cargo run --release -p wordcraft' satırı (OCR bozuk okuma)) | 3:30 | kare |
| cargo run -p wordcraft-ui-egui --example ui_shot | README'deki UI test harness'ini çalıştırıp arayüz ekran görüntüsü alır. (karede: README'de 'UI test harness' başlığı altında komut) | 3:28 | kare |
| wordcraft-cli run --template sample | CLI ile örnek şablondan belge çalıştırır (README). (karede: README'de 'wordcraft-cli run --template sample \' satırı) | 3:30 | kare |
| cargo xtask ci | GridCraft README hızlı başlangıç listesinde geçen CI görevini çalıştırır. (karede: README 'Quick start' listesinde 'cargo xtask ci') | 8:46 | kare |
| git clone https://github.com/storytold/deckcraft | DeckCraft deposunu HTTPS ile klonlar (komutun sonu ekranda kesik). (karede: Terminalde 'git clone https://github.com/stor...' satırı (kesik)) | 12:44 | kare |
| deckcraft-cli run --sample --cmd 'slide.new={"layout":"titleOnly","title":"Hello"}' --save hell | CLI ile örnek sunuma yeni slayt ekleyip kaydeder (kayıt adı kesik). (karede: README/terminalde deckcraft-cli run --sample --cmd komutu) | 13:02 | kare |
| cargo run --release -p deckcraft-cli -- render --sample --all --scale 1 out/ | Yerleşik örnek destenin tüm slaytlarını görüntüye çevirir (README). (karede: README'de render komutu (OCR 'peckcraft-cli' bozuk)) | 13:28 | kare |
| claude mcp get deckcraft | DeckCraft MCP sunucusunun bağlantı durumunu gösterir (Connected). (karede: Claude Code yanıtında 'claude mcp get deckcraft shows Connected' metni) | 15:08 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| DeckCraft PowerPoint özelliklerinin genişlik olarak yaklaşık %79'unu, çekirdek olanların %93'ünü kapsıyor | 12:41 | sayısal |
| GridCraft, WordCraft'tan belirgin şekilde daha iyi çalıştı | 8:31 | karşılaştırma |
| GridCraft'ta 313 motor komutu ajanlara açık | 10:16 | sayısal |
| Olgun alternatif için LibreOffice indirilmeli, klonlar çok yeni | 20:27 | öneri |
| Adobe klonları Office klonlarından daha sağlamdı | 20:27 | karşılaştırma |
| DeckCraft'ta animasyonlar ve sunum modu birkaç saniye gecikmeli | 15:41 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Adobe uygulamaları (Photoshop, Illustrator, Premiere Pro, Lightroom, After Effects) | aday değil: konu dışı | Önceki videolarda incelenen Adobe klonları |
| konuşma 0:00 | Rust | Rust | everything in pure rust |
| kare 0:34 | ArtCraft Crafting Apps sayfası | ArtCraft | Seven apps. One craft. |
| kare 0:34 | PhotoCraft | aday değil: başka adayın parçası (ArtCraft) | Crafting Apps listesinde simge |
| kare 0:34 | VectorCraft | aday değil: başka adayın parçası (ArtCraft) | Crafting Apps listesinde simge |
| kare 0:34 | FilmCraft | aday değil: başka adayın parçası (ArtCraft) | Crafting Apps listesinde simge |
| kare 0:44 | LightCraft | aday değil: başka adayın parçası (ArtCraft) | getartcraft.com/apps/lightcraft |
| kare 0:34 | PdfCraft, EffectCraft, DesignCraft | aday değil: başka adayın parçası (ArtCraft) | Crafting Apps simgeleri |
| kare 0:34 | Discord | aday değil: konu dışı | JOIN THE DISCORD düğmesi |
| konuşma 1:00 | WordCraft | WordCraft | they have Wordcraft |
| konuşma 1:00 | GridCraft | GridCraft | Gridcraft, which is Excel |
| konuşma 1:00 | DeckCraft | DeckCraft | Deckcraft, which is PowerPoint |
| konuşma 1:00 | Temiz oda yeniden uygulama | aday değil: genel kavram | clean room reimplementations |
| kare 1:00 | PowerShell, Python, Dockerfile dil yüzdeleri | aday değil: konu dışı | GitHub dil çubuğu |
| konuşma 2:01 | macOS, Windows, Linux | aday değil: genel kavram | runs everywhere |
| kare 2:54 | GitHub | GitHub | wordcraft deposu sayfası |
| kare 3:00 | WordCraft v0.3.0 release | WordCraft | Releases / v0.3.0 |
| konuşma 2:53 | MSI ve Universal DMG kurulum paketleri | WordCraft | download the MSI if you're on Windows |
| konuşma 2:53 | Arch Linux | aday değil: konu dışı | because I'm on Arch |
| kare 3:26 | git clone wordcraft | Git | git@github.com:storytold/wordcraft.git |
| kare 3:26 | Terminal: kitty, NotoSansM font | aday değil: konu dışı | neofetch çıktısı |
| kare 3:31 | cargo run --release -p wordcraft | Cargo | README komutu |
| kare 3:42 | Aptos Display yazı tipi | Aptos Display | Font alanı |
| konuşma 3:42 | Markdown ve LaTeX | aday değil: konu dışı | real men use markdown or latex |
| kare 6:52 | Nextcloud | aday değil: konu dışı | Dosya seçicide Nextcloud klasörü |
| kare 8:32 | git clone gridcraft | Git | git@github.com:storytold/gridcraft.git |
| kare 8:44 | cargo run gridcraft | Cargo | --sample sales |
| kare 8:46 | trunk build | Trunk | cd apps/gridcraft-web && trunk build |
| kare 8:46 | winit, glow, kurbo vb. crate'ler | aday değil: başka adayın parçası (Cargo) | Derleme günlüğü |
| kare 13:30 | eframe, egui, egui-wgpu | egui | Derleme günlüğü |
| kare 13:30 | wgpu-core-deps, wgpu-naga-bridge | wgpu | Derleme günlüğü |
| kare 12:52 | vello_cpu, vello_common | Vello | Derleme günlüğü |
| kare 12:52 | krilla | Krilla | krilla v0.8.2 |
| kare 12:48 | symphonia paketleri | Symphonia | symphonia v0.5.5 |
| konuşma 8:31 | Pasta ve çubuk grafikler, trend çizgisi | GridCraft | bar chart seems to work |
| kare 10:14 | Command Palette / Agent Control | GridCraft | Automate sekmesi |
| konuşma 10:00 | MCP sunucusu | MCP | all of these have an MCP server built in |
| kare 10:16 | gridcraft --control 7979 | GridCraft | JSON-lines control channel |
| kare 10:16 | gridcraft-cli mcp --connect | gridcraft-cli | MCP bridged to this window |
| kare 10:48 | Claude Code | Claude Code | Claude Code'll be able to read, edit |
| kare 10:52 | claude mcp add gridcraft | gridcraft-cli | claude mcp add gridcraft -- gridcraft-cli mcp |
| kare 11:18 | BlackmagicDesign klasörü | aday değil: konu dışı | Dolphin Documents klasöründe |
| kare 12:48 | Dolphin dosya yöneticisi | aday değil: konu dışı | fake-sales.xlsx klasörü |
| kare 12:46 | deckcraft-cli | deckcraft-cli | deckcraft-cli run --sample |
| kare 15:06 | Poppins ve Nunito Sans | Poppins | deck has the Poppins and Nunito Sans fonts |
| kare 15:08 | deckcraft-cli mcp --connect 7990 | deckcraft-cli | Claude çıktısı |
| konuşma 17:44 | Microsoft Copilot | aday değil: konu dışı | who the hell has Microsoft Copilot |
| kare 17:34 | DuckDuckGo | aday değil: konu dışı | accretive kelimesi aranıyor |
| konuşma 20:27 | LibreOffice | LibreOffice | just use Libra Office |
| açıklama | Epidemic Sound müziği | aday değil: sponsor/reklam | Music is from Epidemic Sound*, affiliate bağlantı |
| açıklama | MY GEAR bağlantıları (geni.us, prf.hn) | aday değil: sponsor/reklam | AFFILIATE LINKS notu |
| açıklama | Polychrome uygulaması (App Store) | aday değil: sponsor/reklam | pt/ct parametreli App Store bağlantısı |
| yorum | SoundCraft, CADCraft, PDFCraft | aday değil: başka adayın parçası (ArtCraft) | Yorum: They also made SoundCraft, CADCraft and PDFCraft |
| yorum | ChatGPT | aday değil: konu dışı | Yorumda geçiyor, videoda kullanılmadı |
## Kareden okunanlar
- 0:34: getartcraft.com Crafting Apps: 'Seven apps. One craft.'; PhotoCraft, VectorCraft, FilmCraft, LightCraft, PdfCraft, EffectCraft, DesignCraft
- 2:54: WordCraft deposu: Releases 2, WordCraft v0.3.0 Latest, Deployments 45
- 3:26: git clone git@github.com:storytold/wordcraft.git; neofetch: Arch, kitty, AMD Ryzen Threadripper PRO 5975WX
- 8:44: cargo run --release -p gridcraft -- --sample sales
- 9:20: Grafik paneli: Column, Stacked, Bar, Line, Area, Pie, Doughnut, Scatter, Radar; Colors & Layout: colorful/monochrome
- 10:14: Search Commands paleti, Automate sekmesi: Command Palette, Agent Control, Action Journal
- 11:44: Claude: 'Q4 Synergy Realization Funnel' grafiği eklendi; Blue-sky ideation 480, Circled back 310
- 14:12: DeckCraft Animations sekmesi: Appear, Fade, Fly In, Float In, Split, Wipe, Zoom, Pulse, Spin
- 17:34: DuckDuckGo: 'what does accretive mean' — adjective, increasing by growth
- 21:02: LibreOffice 26.8 ana sayfası, WG262-WriterGuide.odt — LibreOffice Writer
## Belirsizlikler
- Sunucuda çalışan ana yapay zekâ modeli adı videoda açıkça söylenmiyor; yalnız 'Claude Code'/'Claude' deniyor.
- Altyazı 'Wordcraft v0.3.0' diyor, kare de v0.3.0 gösteriyor; açıklama bağlantılarında lightcraft/filmcraft v0.4.0 indirme bağlantıları bağlı sayfadan geliyor ve burada tek tek URL olarak listelenmedi.
- Gear (geni.us / prf.hn) bağlantılarının hedefleri doğrulanamadı; açıklamada affiliate olarak belirtildi.
- Gumroad ve Polychrome bağlantılarının içeriği erişilemedi; amaçları tahmin.
- Yalnız sözlük eşleşmeleri (Next.js, Framer Motion, Linear, Vercel vb.) videoda kullanılmayan, OCR/ses yanlış eşleşmesi olabilir; adaylara alınmadı.
- Microsoft Word/Excel/PowerPoint ve Copilot yalnızca karşılaştırma olarak anıldı, kullanılmadı.
- Kare 17:04 ve 20:18 için ekli görsel içeriği ayrıca doğrulanmadı.
## Atlanan segment oranı
0/24 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://github.com/storytold/wordcraft | açıklama | açıklama | evet |
| https://github.com/storytold/gridcraft | açıklama | açıklama | evet |
| https://github.com/storytold/deckcraft | açıklama | açıklama | evet |
| https://futc.gumroad.com/l/analogvibes2/n1b2iu0 | açıklama | açıklama | hayır |
| https://apps.apple.com/app/apple-store/id6739345616?pt=127502132&ct=youtubelaunch&mt=8 | açıklama | açıklama | hayır |
| https://share.epidemicsound.com/vi9i60 | açıklama | açıklama | hayır |
| https://geni.us/D2c4 | açıklama | açıklama | hayır |
| https://prf.hn/l/JzY20PN | açıklama | açıklama | hayır |
| https://prf.hn/l/1MVRO4X | açıklama | açıklama | hayır |
| https://prf.hn/l/ZYo9NLW | açıklama | açıklama | hayır |
| https://prf.hn/l/3YVDvvY | açıklama | açıklama | hayır |
| https://prf.hn/l/QxY2ood | açıklama | açıklama | hayır |
| https://prf.hn/l/vybM3OM | açıklama | açıklama | hayır |
| https://prf.hn/l/GlRaeYQ | açıklama | açıklama | hayır |
| https://geni.us/FfmyXd | açıklama | açıklama | hayır |
| https://prf.hn/l/5NLajnm | açıklama | açıklama | hayır |
| https://geni.us/eAw9 | açıklama | açıklama | hayır |
| https://geni.us/KBJo6r | açıklama | açıklama | hayır |
| https://geni.us/rI8A | açıklama | açıklama | hayır |
| https://geni.us/EzdqdA | açıklama | açıklama | hayır |
| https://geni.us/ySx4kC | açıklama | açıklama | hayır |
| https://geni.us/k2g8N | açıklama | açıklama | hayır |
| https://geni.us/ZwkBEC3 | açıklama | açıklama | hayır |
| https://geni.us/Fai9kNo | açıklama | açıklama | hayır |
| https://strapnstyles.de/en | açıklama | açıklama | hayır |
| https://polychrome.dev | açıklama | açıklama | hayır |
| https://github.com/storytold/lightcraft | açıklama | açıklama | hayır |
| https://github.com/storytold/filmcraft | açıklama | açıklama | hayır |
| https://github.com/storytold/craft-launcher | açıklama | açıklama | hayır |
| https://app.getartcraft.com | açıklama | açıklama | hayır |
| https://github.com/storytold/artcraft | açıklama | açıklama | evet |
| getartcraft.com/apps/lightcraft | 0:44 | ekran | hayır |
| getartcraft.com/apps/filmcraft | 0:58 | ekran | hayır |
| getartcraft.com | 1:00 | ekran | evet |
| github.com/storytold/photocraft/blob/main/docs/images/photocraft-demo.jpg | 1:04 | ekran | hayır |
| github.com/storytold/deckcraft/blob/main/docs/images/editor.png | 1:16 | ekran | hayır |
| github.com/storytold/wordcraft/deployments | 2:54 | ekran | hayır |
| github.com/storytold/wordcraft/releases/tag/v0.3.0 | 2:56 | ekran | evet |
| github.com/storytold/wordcraft/releases/download/v0.3.0/wordcraft-0.3.0-windows-x64.msi | 3:04 | ekran | evet |
| github.com/storytold/wordcraft/releases/download/v0.3.0/wordcraft-0.3.0-windows-x64-portable.zip | 3:06 | ekran | evet |
| github.com/storytold/wordcraft/releases/download/v0.3.0/wordcraft-0.3.0-macos-universal.dmg | 3:08 | ekran | evet |
| getartcraft.com/apps/wordc | 3:26 | ekran | evet |
| https://github.com/storytold/wordcraft | 3:30 | ekran | evet |
| portfolio.example.com | 4:58 | ekran | hayır |
| github.com/storytold/gridcraft/blob/main/docs/images/format-chart.pry | 8:42 | ekran | hayır |
| https://github.com/storytold/deckcraft | 12:44 | ekran | evet |
| https://getartcraft.com/apps/wordcraft | 3:26 | ekran | hayır |
| https://github.com | 3:26 | ekran | hayır |
| https://example.com | 4:58 | ekran | hayır |
| https://github.com/storytold/gridcraft/blob/main/docs/images/format-chart.png | 8:42 | ekran | hayır |
| https://github.com/sto… | 14:52 | ekran | hayır |
## İş akışı
- 1. adım — Kaynak depoyu ve sürüm sayfasını bulma (GitHub Releases/Deployments). — araçlar: GitHub
- 2. adım — WordCraft deposunu SSH ile klonlama. — araçlar: Git, WordCraft
- 3. adım — WordCraft'ı release modunda derleme ve açma. — araçlar: Cargo, WordCraft
- 4. adım — Örnek belgeyi açıp WordCraft arayüzünü inceleme. — araçlar: WordCraft
- 5. adım — Yeni resume belgesi oluşturup italik ve metin düzenlemelerini test etme. — araçlar: WordCraft
- 6. adım — Tablo, resim, denklem ve metin sarma (wrap text) testleri. — araçlar: WordCraft
- 7. adım — GridCraft deposunu klonlama ve örnek satış dosyasıyla derleme. — araçlar: Git, Cargo, GridCraft
- 8. adım — Grafik türü, renk ve toplam (AutoSum) testleri ile tablo tasarımı denemesi. — araçlar: GridCraft
- 9. adım — GridCraft MCP sunucusunu Claude Code'a ekleme ve bağlantıyı kontrol etme. — araçlar: Claude Code, GridCraft, MCP
- 10. adım — Claude ile rastgele satış verisi ve yeni grafik ürettirme; yıldız testi. — araçlar: Claude Code, GridCraft, MCP
- 11. adım — DeckCraft deposunu klonlama ve derleme. — araçlar: Git, Cargo, DeckCraft
- 12. adım — DeckCraft'ta slayt, başlık, madde ve geçiş (transition) ayarlarını deneme. — araçlar: DeckCraft
- 13. adım — DeckCraft'ı kontrol portuyla açıp Claude Code'a MCP olarak bağlama. — araçlar: Claude Code, DeckCraft, MCP
- 14. adım — Claude ile kurumsal şaka slaytlarını ve animasyonları ürettirme. — araçlar: Claude Code, DeckCraft, MCP
- 15. adım — Sunum modunda (Present) çalıştırma ve gecikmeyi gözlemleme. — araçlar: DeckCraft
- 16. adım — Uygulamanın çökmesi ve log kontrolü (Rust panic, çıkış kodu 101). — araçlar: Claude Code, DeckCraft
- 17. adım — Karar: LibreOffice'in MS Office alternatifi olarak önerilmesi. — araçlar: LibreOffice
## Promptlar
- GridCraft MCP bağlantısını doğrulama — Claude'a GridCraft MCP sunucusunu görüp görmediği ve kullanıp kullanamayacağı soruldu.
- GridCraft'ta sahte satış verisi üretme — Yeni bir belge oluşturup içine rastgele veri eklemesi istendi.
- MCP ile grafik üretme — Tablodan grafik yapıp ekran görüntüsü alması istendi.
- Ek grafik ve veri üretme — Tabloya kurumsal jargonlu bir 'sinerji hattı' grafiği daha eklemesi istendi.
- DeckCraft MCP kurulumu — DeckCraft'ın MCP'sini kurup erişmeye çalışması istendi.
- MCP bağlantı testi — Çalışıp çalışmadığını test etmek için bir şey eklemesi istendi.
- Eğlenceli sunum içeriği üretme — Sunuma kurumsal jargon ve komik kurumsal suçlar eklemesi istendi.
- Animasyon ekleme — Tüm slaytlara bol animasyon eklemesi istendi.
ikinci göz KAPALI: --ikinci-goz yok
