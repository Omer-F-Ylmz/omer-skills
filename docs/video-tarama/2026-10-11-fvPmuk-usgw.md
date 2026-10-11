# Vibe Coding a Full Game with PixelLab MCP + API
## Künye
Vibe Coding a Full Game with PixelLab MCP + API · PixelLab · süre: 6:57 · en-orig · https://youtu.be/fvPmuk-usgw · şema 2
motor: parti 2026-10-11-short-2 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 36162 tk · claude-haiku-5-5: claude-haiku-5-5 · 358462 tk
## Özet
PixelLab ekibi, PixelLab MCP ve API'sini OpenAI Codex ile birlikte kullanarak Phaser 4 üzerinde müze temalı izometrik bir oyunu 'vibe coding' ile nasıl yaptığını gösteriyor. Karakter, tile set, nesne, animasyon, portre ve kaplı nesne varyantları basit promptlarla üretiliyor. Sonda ajanın model seçmesine bırakmak yerine hangi aracın kullanılacağını açıkça belirtmek öneriliyor ve önerilen araç listesi veriliyor.
## Bölümler
- 0:00 Giriş ve kavramlar
- 0:54 Pixel Lab kurulumu
- 1:25 İlk proje iskeleti
- 2:17 Oyunu oluşturma ve iyileştirme
- 3:37 Nesne etkileşimi ve genişletme
- 4:45 Gelişmiş oda geçişleri
- 5:38 Önerilen araçların özeti
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| PixelLab MCP | yok | MCP | yok | PixelLab'ın MCP sunucusu; kodlama ajanından piksel sanat varlığı üretmeyi sağlar | 0:54 | Vibe coding sekmesinde 'claude mcp add pixellab https://api.pixellab.ai/mcp' komutu görünüyor (karede: PixelLab sitesinde Vibe coding sekmesi, Claude Code seçili, MCP ekleme komutu ve kurulum adımları) |
| PixelLab API | yok | teknik | yok | MCP'nin sunmadığı uç noktaları da kapsayan doğrudan API | 0:00 | API provides everything that the MCP doesn't, all the endpoints that might be missing |
| OpenAI Codex | yok | CLI | yok | Videoda ana kodlama ajanı | 0:00 | For coding, I'll be using OpenAI's Codex |
| Phaser 4 | yok | teknik | yok | Oyun çatısı | 0:00 | I'll be using Phaser 4 |
| TypeScript | yok | teknik | yok | Proje dili | 2:13 | Ajan Phaser + TypeScript + Vite rotasını seçiyor (karede: Codex sohbetinde 'Phaser + TypeScript + Vite' yazan metin) |
| Vite | yok | CLI | yok | Geliştirme sunucusu ve derleme aracı | 2:13 | Phaser + TypeScript + Vite; npm run dev çalışıyor (karede: Codex sohbetinde 'Phaser + TypeScript + Vite' ifadesi) |
| Claude Code | yok | CLI | yok | Alternatif kodlama ajanı; kurulum komutu bunun için gösteriliyor | 0:56 | Claude Code sekmesi seçili (karede: Claude Code sekmesi vurgulu, claude mcp add komutu) |
| Create Character | yok | MCP | yok | Karakter oluşturma aracı | 5:38 | For characters, use the create character tool |
| Character States | yok | MCP | yok | Karakter durumları (ör. mid-walk) aracı | 5:38 | create character tool and the character states one |
| Animate with Text V3 | yok | MCP | yok | Metinle animasyon üretimi | 5:38 | use animate with text V3 and interpolation V3 |
| Custom Animation V3 | yok | MCP | yok | Idle animasyonu için kullanılan animasyon aracı | 2:17 | Idle should be using custom animation V3 |
| Interpolation V3 | yok | MCP | yok | Kareler arası ara değerleme animasyonu | 5:38 | animate with text V3 and interpolation V3 |
| Create Building Kit | yok | MCP | yok | Duvar/zemin sistemi tile seti aracı | 6:05 | Ekranda 'Create Building Kit - wall/floor systems for interiors & exteriors' (karede: Araç özeti slaytında Create Building Kit satırı (OCR: 6:05)) |
| Create Tiles Pro | yok | MCP | yok | İzometrik, altıgen, oblique, kare tile setleri | 5:38 | create tiles pro for isometric, hexagonal, oblique, or square |
| Create Top-Down Tileset | yok | MCP | yok | Yukarıdan görünüm tile seti | 5:38 | create top-down tile set, create side-scroller tile set |
| Create Side-Scroller Tileset | yok | MCP | yok | Yandan kaydırmalı tile seti | 5:38 | create side-scroller tile set |
| Create Object | yok | MCP | yok | Tek yönlü veya sekiz yönlü nesne üretimi | 5:38 | create one direction or eight direction object · kanıt: yok |
| Animate Object | yok | MCP | yok | Nesne animasyonu | 6:19 | Ekranda 'Animate Object' yazıyor (karede: Özet slaytında Animate Object satırı (OCR: 6:19)) |
| Object States | yok | MCP | yok | Nesne durumları | 5:38 | animate object, and object states |
| UI Template Pro | yok | MCP | yok | Oyun arayüzü üretimi | 5:38 | I'd recommend using the UI template pro tool |
| Create Font | yok | MCP | yok | Font üretimi | 5:38 | Use create font tool for fonts |
| Create Portrait Character | yok | MCP | yok | Diyalog portreleri (character to portrait) | 5:38 | create portrait character and create vocal animation |
| Create Vocal Animation | yok | MCP | yok | Konuşma animasyonu | 6:30 | Ekranda 'Create Vocal Animation' yazıyor (karede: Özet slaytında Create Vocal Animation satırı (OCR: 6:30)) |
| Create Image Pixen | yok | MCP | yok | Ham görsel üretimi | 5:38 | use create image pixen or create image pro |
| Create Image Pro | yok | MCP | yok | Ham görsel üretimi (pro model) | 5:38 | create image pixen or create image pro |
| Edit Image Pro | yok | MCP | yok | Görsel düzenleme | 6:38 | to edit images, use edit image pro |
| Edit Image (new/pixen) | yok | MCP | yok | Nesnelere beyaz battaniye örtüsü eklemek için kullanılan düzenleme | 3:37 | edit each of the objects from the museum using edit image new |
| Building Tiles | yok | teknik | yok | Müze duvar/zemin için bina tile tipi | 2:17 | make a tile set using the buildings tiles type |
| Gemini CLI | yok | CLI | yok | Alternatif kodlama ajanı, MCP kurulum listesinde | 1:24 | Menüde Gemini CLI (karede: Other açılır menüsünde Gemini CLI ve Codex CLI) |
| Cursor | yok | CLI | yok | Alternatif kodlama ortamı | 1:30 | Uyumlu ajanlar slaytında Cursor Composer (karede: 'Compatible with every AI agent' slaytında Cursor Composer kutusu) |
| Gölgelendirici | yok | teknik | yok | Duvarların arkasındaki karakterleri görünür yapan shader | 4:30 | add a shader to make the characters visible through the walls · kanıt: yok |
| Gün-gece sistemi | yok | teknik | yok | Oyuna eklenen gün-gece döngüsü | 3:18 | add a day-night system · kanıt: yok |
| Grok 4.6 | yok | teknik | yok | xAI'nin modeli; konuşmada ve uyumluluk slaytında geçiyor. | 0:00 | Claude, Gemini, Grok, Kimmy |
| Kimi 3.0 | yok | teknik | yok | Moonshot/Kimi model; konuşmada 'Kimmy' olarak, slaytta Kimi 3.0 olarak geçiyor. | 0:00 | Claude, Gemini, Grok, Kimmy, etc. |
| Claude Opus 5 / Fable | yok | teknik | yok | Uyumlu ajan slaytında listelenen Anthropic modeli. | 1:31 | Uyumluluk slaytı: Claude Opus 5 / Fable (karede: 'Compatible with every AI agent' slaytında Claude Opus 5 / Fable kartı.) |
| Gemini 3.7 Flash | yok | teknik | yok | Uyumlu ajan slaytında listelenen Google modeli. | 1:31 | Uyumluluk slaytı: Gemini 3.7 Flash (karede: 'Compatible with every AI agent' slaytında Gemini 3.7 Flash kartı.) |
| Windsurf | yok | teknik | yok | AI kodlama IDE'si; Cascade ajanı uyumluluk slaytında listelenmiş. | 1:31 | Uyumluluk slaytı: Windsurf Cascade (karede: 'Compatible with every AI agent' slaytında Windsurf Cascade kartı.) |
| Shader | yok | teknik | yok | GPU gölgelendirici; karakterin duvar arkasından görünmesi için eklendiği anlatılıyor. | 3:37 | add a shader to make the characters visible through the walls |
| mcp-remote | yok | MCP | yok | Codex config'inde npx ile çalıştırılan, uzak MCP sunucusunu stdio'ya bağlayan köprü paketi. | 1:38 | mcp-remote@latest (karede: Codex config.toml örneğinde command = "npx" ve mcp-remote@latest satırı (OCR).) |
| npm | yok | CLI | yok | Node paket yöneticisi; npm run dev, npm run build ve npm audit komutları çalıştırıldı. | 2:35 | npm run dev -- --host 127.0.0.1 (karede: Codex terminal çıktısında npm run dev komutu (OCR).) |
| npx | yok | CLI | yok | npm paketlerini indirmeden çalıştırır; MCP köprüsünü başlatmak için kullanılıyor. | 1:40 | command = "npx" (karede: Codex config.toml örneğinde command = "npx" satırı (OCR).) |
| Git | yok | CLI | yok | Sürüm kontrol aracı; Codex derleme sonrası git status --short ile değişiklikleri kontrol etti. | 2:30 | npm run build && git status --short (karede: Codex komut çıktısında git status --short komutu (OCR).) |
| curl | yok | CLI | yok | Komut satırı indirme aracı; PixelLab dosyasını Backblaze üzerinden indirmek için kullanıldı. | 2:24 | Running curl -fsSL 'https://backblaze.pixellab.ai/file/... (karede: Codex komut kaydında curl -fsSL ile PixelLab dosya indirme satırı (OCR).) |
| ffmpeg | yok | CLI | yok | Video/kare dizisi işleme aracı; sprite karelerini birleştirmek için kullanıldı. | 4:32 | Ran ffmpeg -hide_banner -loglevel error -framerate 1 (karede: Codex komut kaydında ffmpeg komutu (OCR).) |
| İlk oyun iskeleti | yok | prompt | yok | İzometrik oyun yapılacak; müze temalı özet verildi. 48x48 müze bekçisi karakteri, building tiles ile müze tile seti ve haritaya yerleştirilecek izometrik nesneler isteniyor. | 1:25 | kaynak: altyazı |
| Düzeltme ve animasyon | yok | prompt | yok | Kamera konumunu düzelt, duvarları sütun yerine tam kullan; idle için custom animation V3, yürüme ara durumu için ayrı state ve animasyon. | 2:17 | kaynak: altyazı |
| Oyun genişletme | yok | prompt | yok | Çarpışmaları düzelt, gün-gece sistemi, UI template aracıyla arayüz ve daha fazla nesne ekle. | 3:18 | kaynak: altyazı |
| Kaplı nesne varyantları | yok | prompt | yok | Müzedeki her nesneyi edit image ile beyaz battaniyeyle kapla; oyuncu açarak kilidi açsın. | 3:37 | kaynak: altyazı |
| Eşlikçi karakter ve harita | yok | prompt | yok | Aynı stilde yeni eşlikçi karakter, idle ve mid-walk animasyonları, portre aracıyla portreler; müzeyi daha büyük ve farklı düzenli yap. | 3:37 | kaynak: altyazı |
| Oda geçişi | yok | prompt | yok | Yeni izometrik oda ekle; oyuncu kapıdan geçince fade out/in ile yeni odaya geçsin, yeni nesneler ve kaplı varyantları olsun. | 4:45 | kaynak: altyazı |
## Açıklama bağlantıları
- https://www.pixellab.ai?utm_source=youtube&utm_medium=description&utm_campaign=fvPmuk-usgw — PixelLab ana sayfası (UTM izlemeli) · aday: evet (PixelLab MCP) · PixelLab, videoda kullanılan servis; yalnızca izleme parametresi var, sponsor ifadesi yok · sınıf: diğer
- https://discord.gg/kCnDAD6hYc — PixelLab Discord topluluğu · aday: hayır · Topluluk daveti; araç değil · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| HUD paneli (HUD panel) ve ilerleme çubuğu (progress bar) | Sol üstte 'CURRENT CASE' vaka kartı; başlık ve 'attribution confidence' yüzdeli çubuk. (karede: Sol üstte 'CURRENT CASE · The Salt-Fired Vessel' kartı, '32%' attribution çubuğu ve 'Inspect the broken amphora' görevi.) | 2:37 | kare |
| Görev listesi paneli (task list panel) | Sol altta 'Tonight's work' görev kutusu. (karede: Sol altta 'TONIGHT'S WORK' kutusu ve 'Inspect the broken amphora' satırı.) | 2:37 | kare |
| Bağlama duyarlı etkileşim istemi (contextual prompt) | Yakın bir nesnede sağ altta 'Inspect exhibit' istemi çıkıyor. (karede: Sağ altta 'Inspect exhibit' yazılı etkileşim kutusu.) | 2:37 | kare |
| İzometrik 2.5D oda (isometric tile floor) | Duvarlı, karo zeminli izometrik müze odası; sergi objeleri sahnede yerleşik. (karede: İzometrik karo zeminli oda, duvarlar ve yerleştirilmiş sergi vitrinleri.) | 3:27 | kare |
| Örtülü sergi objeleri (covered sprite overlay) | Müze objeleri beyaz örtüyle kapalı başlıyor; açılınca örtü kalkıyor. (karede: Beyaz örtü/konik şekilli objeler ve '0/3 CLEANED' göstergesi.) | 3:51 | kare |
| Örtü kaldırma animasyonu (reveal animation) | Nesne yanında E tuşuna basınca örtünün açılması; Codex bunu uygulamış. (karede: Codex özet metni: 'Pressing E near an object uncovers only that placement with a reveal animation' (OCR).) | 3:59 | kare |
| Diyalog penceresi ve karakter portreleri (dialogue box, portrait) | Ekranın altında çerçeveli diyalog kutusu; iki karakter portresi yan yana. (karede: 'RECOVERY · A FAMILIAR KNOT' diyalog kutusu, iki portre ve 'Continue' düğmesi.) | 4:40 | kare |
| Karartma ve açılma geçişi (fade-out / fade-in transition) | Kapıdan geçince ekran kararıp yeni odada açılıyor. | 4:45 | altyazı |
| Duvar arkası karakter görünürlüğü (shader overlay) | Karakterin duvar arkasından görünmesi için gölgelendirici eklendi. | 3:37 | altyazı |
| Sprite kare animasyonu (sprite animation) | Boşta (idle) ve yürüme (walk) animasyonları farklı kare hızlarında oynuyor. (karede: Codex özet metni: 'Idle at 4 FPS and Walk at 10 FPS' (OCR).) | 3:15 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| claude mcp add pixellab https://api.pixellab.ai/mcp -t http -H "Authorization: Bearer <anahtar>" | PixelLab MCP sunucusunu Claude Code'a ekler (karede: Vibe coding sekmesinde Claude Code için claude mcp add pixellab komutu) | 0:56 | kare |
| npm run dev -- --host 127.0.0.1 | Oyunun geliştirme sunucusunu başlatır (karede: Codex çıktısında npm run dev -- --host 127.0.0.1 satırı) | 2:35 | kare |
| npm run build | Üretim derlemesi alır (karede: Codex'in 'Running npm run build && git status' satırı) | 2:30 | kare |
| npx tsc --noEmit | TypeScript tip denetimi yapar (karede: 'Running npx tsc --noEmit && printf placed props' satırı) | 4:16 | kare |
| claude mcp add pixellab https://api.pixellab.ai/mcp -t http -H "Authorization: Bearer <anahtar gizlendi>" | Claude Code'a PixelLab MCP sunucusunu HTTP olarak ekler. (karede: Vibe Coding AI Toolkit'te Claude Code sekmesindeki kurulum komutu; anahtar kısmı gizli.) | 1:18 | kare |
| config.toml: command = "npx"; args içinde "mcp-remote@latest", "--transport", "--header" (PixelLab MCP adresi) | Codex CLI'a PixelLab MCP'yi npx ve mcp-remote köprüsüyle tanıtır. (karede: Codex config.toml örneğinde command = "npx" ve mcp-remote@latest satırları (OCR; tam argüman listesi okunamadı).) | 1:38 | kare |
| npm run build && git status --short 2>/dev/null | Üretim derlemesi alır, ardından değişen dosyaları listeler (OCR'da sonunda '/ true' okundu). (karede: Codex komut kaydında npm run build && git status --short satırı (OCR).) | 2:30 | kare |
| /bin/zsh -Ic 'npm audit --omit=dev' | Üretim bağımlılıklarındaki güvenlik açıklarını denetler. (karede: Codex komut kaydında npm audit --omit=dev satırı (OCR).) | 2:32 | kare |
| npx tsc --noEmit && printf 'placed props: ' && rg -c "id: " src/game/content/museum.ts | TypeScript tip denetimi yapar, sonra museum.ts içindeki yerleştirilmiş prop sayısını sayar. (karede: Codex komut kaydında npx tsc --noEmit ve rg -c satırı (OCR).) | 4:16 | kare |
| curl -fsSL 'https://backblaze.pixellab.ai/file/pixellab-characters/...' (kırpılmış) | PixelLab'ın ürettiği karakter dosyasını indirir. (karede: Codex komut kaydında curl ile PixelLab dosya indirme satırı (OCR, kırpılmış).) | 2:24 | kare |
| ffmpeg -hide_banner -loglevel error -framerate 1 -start_number 0 -i public/assets/environment/build... (kırpılmış) | Ortam (environment) kare dizisini işler ve birleştirir. (karede: Codex komut kaydında ffmpeg satırı (OCR, kırpılmış).) | 4:32 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| API, MCP'de eksik olan tüm uç noktaları sağlar | 0:00 | özellik |
| Araçları bilmek ajanı yönlendirmeyi kolaylaştırır; building tiles tipi bilinmezse kaçırılır | 2:17 | öneri |
| Model belirtilmezse ajan pro modelleri seçti ve ilk/ikinci harita nesneleri arasında stil farkı oluştu | 4:45 | karşılaştırma |
| Idle 4 FPS, yürüme 10 FPS ile oynatılıyor; 112 kare 48x48'e normalize edildi | 3:15 | sayısal |
| Genel olarak 'oyun yap ve PixelLab kullan' demek yerine belirli şeyler istenmeli | 4:45 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | PixelLab MCP | PixelLab MCP | We already have an MCP video in our channel |
| konuşma 0:00 | Phaser 4 | Phaser 4 | I'll be using Phaser 4 |
| konuşma 0:00 | OpenAI Codex | OpenAI Codex | I'll be using OpenAI's Codex |
| konuşma 0:00 | Claude, Gemini, Grok, Kimi | aday değil: konu dışı | alternatif ajan örnekleri sayıldı |
| kare 0:56 | Claude Code sekmesi | Claude Code | Claude Code sekmesi seçili |
| kare 1:24 | Gemini CLI, Codex CLI menüsü | Gemini CLI | Other menüsünde listelendi |
| kare 1:24 | Zed, Continue, BoltAI, LM Studio, Perplexity Desktop, Kiro, Junie, Warp | aday değil: konu dışı | yalnız menüde görünür |
| kare 1:30 | Uyumlu ajan slaytı | aday değil: konu dışı | Yalnız slayt |
| kare 2:13 | TypeScript, Vite | TypeScript | Phaser + TypeScript + Vite |
| açıklama | Discord daveti | aday değil: konu dışı | discord.gg bağlantısı |
| açıklama | pixellab.ai doküman sayfaları | PixelLab API | docs/tools bağlantıları |
| açıklama | youtu.be video bağlantıları | aday değil: konu dışı | Diğer PixelLab videoları |
| konuşma 3:18 | Gün-gece sistemi | Gün-gece sistemi | add a day-night system |
| konuşma 4:30 | Gölgelendirici | Gölgelendirici | add a shader |
| konuşma 5:38 | Önerilen araç listesi | Create Character | For characters, use the create character tool |
| yorum | RPG Maker MCP sorusu | aday değil: konu dışı | Is there an mcp for rpg maker |
| kare 4:32 | ffmpeg | aday değil: konu dışı | Codex'in çalıştırdığı komut, anlatılmıyor |
## Kareden okunanlar
- 0:01: PixelLab.ai, 'NEW MCP SERVER & API', 'VIBE CODING 2.0'
- 1:09: PixelLab API sayfası: Tier 2 Pixel Artisan, 5.000 üretim/ay, eşzamanlı iş limiti 10
- 1:22: Pro tip: @https://api.pixellab.ai/mcp/docs bağlantısı istemlere eklenmeli
- 3:29: Oyun: The Museum Restorer, 'Current Case' paneli, E ile inceleme
- 4:16: Codex: 'Created 16 unique white-blanket variants ... Pixen /edit-image endpoint'; 0/17 unlock ilerlemesi
## Belirsizlikler
- Yorumlarda sorulan Codex modeli (Luna?) videoda belirtilmiyor.
- Kare/OCR'da görünen API anahtarı ve Bearer değeri yazılmadı.
- Uyumlu ajan slaytındaki model adları (Claude Opus 5 / Fable, Gemini 3.7 Flash, Grok 4.6, Kimi 3.0) yalnızca slaytta; kullanılmıyor.
- Açıklama sayfalarındaki doküman bağlantıları (animate-with-text-pro, rotate vb.) videoda anlatılmıyor.
- Sözlük eşleşmeleri (Next.js, Framer, Three.js, React vb.) videoda kullanıldığına dair kanıt yok.
## Atlanan segment oranı
0/10 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.pixellab.ai?utm_source=youtube&utm_medium=description&utm_campaign=fvPmuk-usgw | açıklama | açıklama | evet |
| https://discord.gg/kCnDAD6hYc | açıklama | açıklama | hayır |
| https://api.pixellab.ai/mcp | 1:18 | ekran | evet |
| https://api.pixellab.ai/mcp/docs | 1:22 | ekran | evet |
| api.pixellab.ai/v2/llms.txt | 2:17 | ekran | evet |
| http://127.0.0.1:5173/ | 2:35 | ekran | hayır |
| http://127.0.0.1:52475 | 4:35 | ekran | hayır |
| api.pixellab.ai/v2/lms.txt | 2:17 | ekran | hayır |
| https://backblaze.pixellab.ai/file/pixellab-characters/67fef9e8-3a50-4bff-a4cd-0ee8b | 2:24 | ekran | hayır |
| https://www.pixellab.ai/docs/tools/animate-with-text-pro | açıklama | açıklama | hayır |
| https://www.pixellab.ai/docs/tools/rotate | açıklama | açıklama | hayır |
| https://www.pixellab.ai/docs/tools/consistent-style | açıklama | açıklama | hayır |
| https://www.pixellab.ai/docs/getting-started | açıklama | açıklama | hayır |
| https://www.pixellab.ai/docs/tools/create-image-flux | açıklama | açıklama | hayır |
| https://www.pixellab.ai/docs/tools/create-map | açıklama | açıklama | hayır |
| https://www.pixellab.ai/docs/tools/create-ui-elements-pro | açıklama | açıklama | hayır |
| https://youtu.be/Iaxk_8ftJ5s | açıklama | açıklama | hayır |
| https://youtu.be/r8ySiSRRvz4 | açıklama | açıklama | hayır |
| https://youtu.be/9eAlZlQmZBg | açıklama | açıklama | hayır |
| https://youtu.be/oCJWxfEwX-o | açıklama | açıklama | hayır |
| https://youtu.be/sE1s5ZYfxqk | açıklama | açıklama | hayır |
| https://youtu.be/fvPmuk-usgw | açıklama | açıklama | hayır |
| https://youtu.be/BdoUMKhZ1Ys | açıklama | açıklama | hayır |
| https://youtu.be/Hhx9QZwYoZY | açıklama | açıklama | hayır |
| https://youtu.be/moCpjMOOBGk | açıklama | açıklama | hayır |
| https://youtu.be/j2bE9gq914U | açıklama | açıklama | hayır |
| https://youtu.be/zghUW8fGqsM | açıklama | açıklama | hayır |
| https://youtu.be/qVDkp1baJkU | açıklama | açıklama | hayır |
| https://PixelLab.ai/docs/tools/animate-with-text-pro | açıklama | açıklama | hayır |
| https://PixelLab.ai/docs/tools/rotate | açıklama | açıklama | hayır |
| https://PixelLab.ai/docs/tools/consistent-style | açıklama | açıklama | hayır |
| https://PixelLab.ai/docs/getting-started | açıklama | açıklama | hayır |
| https://PixelLab.ai/docs/tools/create-image-flux | açıklama | açıklama | hayır |
| https://PixelLab.ai/docs/tools/create-map | açıklama | açıklama | hayır |
| https://PixelLab.ai/docs/tools/create-ui-elements-pro | açıklama | açıklama | hayır |
| https://Pixellab.ai/docs/tools/animate-with-text-pro | açıklama | açıklama | hayır |
| https://Pixellab.ai/docs/tools/rotate | açıklama | açıklama | hayır |
| https://Pixellab.ai/docs/tools/consistent-style | açıklama | açıklama | hayır |
| https://Pixellab.ai/docs/getting-started | açıklama | açıklama | hayır |
| https://Pixellab.ai/docs/tools/create-image-flux | açıklama | açıklama | hayır |
| https://Pixellab.ai/docs/tools/create-map | açıklama | açıklama | hayır |
| https://Pixellab.ai/docs/tools/create-ui-elements-pro | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — Oyun konseptini (müze restorasyonu, izometrik) belirle ve konsept belgesi hazırla — araçlar: Phaser 4, OpenAI Codex
- 2. adım — PixelLab API sayfasında API anahtarı ve abonelik durumunu kontrol et — araçlar: PixelLab API
- 3. adım — Vibe Coding sekmesinden Claude Code için MCP kurulum komutunu kopyala — araçlar: PixelLab MCP, Claude Code
- 4. adım — Codex'e MCP ve API kurulumunu yaptır; config.toml içine MCP sunucusu ekle — araçlar: OpenAI Codex, PixelLab MCP, mcp-remote, npx
- 5. adım — PixelLab AI asistan dokümanını (lms.txt) Codex'e okut — araçlar: OpenAI Codex, PixelLab API
- 6. adım — Karakter, buildings tile seti ve izometrik objeleri üret — araçlar: PixelLab MCP
- 7. adım — Phaser + TypeScript + Vite proje iskeletini kur ve geliştirme sunucusunu başlat — araçlar: Phaser 4, TypeScript, Vite, npm
- 8. adım — Karakter boşta ve yürüme animasyonlarını üret; sprite karelerini ffmpeg ile işle — araçlar: PixelLab MCP, Custom Animation V3, ffmpeg
- 9. adım — Derleme ve git ile değişiklik kontrolü yap; üretilen dosyaları indir — araçlar: npm, Git, curl
- 10. adım — Tarayıcıda oyunu oynatıp görsel kontrol ve etkileşim testi yap — araçlar: OpenAI Codex
- 11. adım — Sergi objelerini Edit Image ile beyaz örtülü varyantlara çevir — araçlar: PixelLab MCP, Pixen
- 12. adım — Yeni karakter ekle ve portre oluştur — araçlar: PixelLab MCP, OpenAI Codex
- 13. adım — Müzeyi büyüt, koridorlar ekle, duvarları birleştir, karakter görünürlüğü için shader ekle — araçlar: OpenAI Codex, Shader
- 14. adım — Yeni odayı ve geçişi ekle; yeni objelerin örtülü varyantlarını üret — araçlar: OpenAI Codex, PixelLab MCP
- 15. adım — TypeScript tip denetimi ve güvenlik kontrolü (npm audit) yap — araçlar: npx tsc, npm
## Promptlar
- İlk oyun iskeleti — İzometrik oyun yapılacak; müze temalı özet verildi. 48x48 müze bekçisi karakteri, building tiles ile müze tile seti ve haritaya yerleştirilecek izometrik nesneler isteniyor.
- Düzeltme ve animasyon — Kamera konumunu düzelt, duvarları sütun yerine tam kullan; idle için custom animation V3, yürüme ara durumu için ayrı state ve animasyon.
- Oyun genişletme — Çarpışmaları düzelt, gün-gece sistemi, UI template aracıyla arayüz ve daha fazla nesne ekle.
- Kaplı nesne varyantları — Müzedeki her nesneyi edit image ile beyaz battaniyeyle kapla; oyuncu açarak kilidi açsın.
- Eşlikçi karakter ve harita — Aynı stilde yeni eşlikçi karakter, idle ve mid-walk animasyonları, portre aracıyla portreler; müzeyi daha büyük ve farklı düzenli yap.
- Oda geçişi — Yeni izometrik oda ekle; oyuncu kapıdan geçince fade out/in ile yeni odaya geçsin, yeni nesneler ve kaplı varyantları olsun.
ikinci göz KAPALI: --ikinci-goz yok
