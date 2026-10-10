# Yorumlara SES yaz, seninle de rehberi paylaşayım 🤝
## Künye
Yorumlara SES yaz, seninle de rehberi paylaşayım 🤝 · yasin.arsal · süre: 0:36 · ? · https://www.instagram.com/reel/DcgPETIMIhq/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-10-short · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 31008 tk · claude-haiku-5-5: claude-haiku-5-5 · 35880 tk
## Özet
Kısa reel: ElevenLabs ve Wispr Flow gibi ücretli ses araçlarının yerine geçen, açık kaynaklı ve yerelde çalışan Voicebox GitHub reposu tanıtılıyor. Ses klonlama, yapay zekâ ile seslendirme ve sistem geneli dikte kısayolu sunuyor. API key, abonelik ve kullanım limiti yok. Repo 33 bin yıldızı geçmiş, kurulum tek komut diye anlatılıyor. Rehber için yorumlara SES yazılması isteniyor.
## Bölümler
- 0:00 Ücretli araçlara alternatif girişi (ElevenLabs, Wispr Flow)
- 0:08 Voicebox GitHub reposu tanıtımı
- 0:10 Birkaç saniyelik kayıtla ses klonlama
- 0:13 Sistem geneli dikte kısayolu (push to talk)
- 0:21 Yerel API ve MCP sunucusu
- 0:23 Açık kaynak lisansı ve 33 bin yıldız
- 0:27 Tek komutla kurulum
- 0:30 Voicebox ana sayfası: ElevenLabs ve WisprFlow alternatifi
- 0:35 Yorumlara SES yaz çağrısı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Voicebox | yok | CLI | yok | Açık kaynaklı, yerelde çalışan yapay zekâ ses stüdyosu: ses klonlama, konuşma üretimi, sistem geneli dikte. | 0:08 | README başlığı Voicebox; 'The open-source AI voice studio.' yazıyor. (karede: Mikrofon simgesi, 'Voicebox' başlığı, 'The open-source AI voice studio. Clone any voice. Generate speech. Dictate into any app.' metni, rozetler ve uygulama ekran görüntüsü.) |
| ElevenLabs | yok | CLI | yok | Ücretli ses üretimi/klonlama servisi; Voicebox'ın yerini aldığı araç olarak anılıyor. | 0:00 | Altyazı 'Eleven Labs ve Whisper Flow'u artık tamamen ücretsiz kullanabilirsiniz'. |
| Wispr Flow | yok | CLI | yok | Ücretli dikte aracı; Voicebox'ın yerini aldığı araç olarak anılıyor. | 0:00 | Ekran metni 'ElevenLabs ve WisprFlow'u'; açıklamada Wispr Flow geçiyor. |
| GitHub | yok | teknik | yok | Reponun barındığı açık kaynak platform; GitHub Trending rozeti gösteriliyor. | 0:08 | Altyazı 'bunu sağlayan şey ise bi Github reposu'; karede GitHub Trending rozeti. (karede: 'GITHUB TRENDING #1 Repository Of The Day' rozeti ve alt yazı 'bunu sağlayan şey ise bi Github reposu'.) |
| Whisper | yok | teknik | yok | Yerel konuşmadan yazıya çeviri modeli (whisper-turbo); transcribe isteğinde kullanılıyor. | 0:21 | Ekran metni 'model=whisper-turbo' ve '/transcribe' isteği. (karede: README'deki curl örneği: '# Transcribe an audio file', '-F "audio=@recording.wav"', '-F "model=whisper-turbo"'.) |
| MCP server | yok | MCP | yok | Voicebox'ın yerleşik Model Context Protocol sunucusu; ajanlar konuşabilir, yazıya çevirebilir. | 0:21 | Ekran metni 'Voicebox ships a built-in Model Context Protocol server'. (karede: 'MCP server' başlığı ve altında 'Voicebox ships a built-in Model Context Protocol server so any MCP-aware agent...' paragrafı.) |
| Claude Code | yok | CLI | yok | Anthropic'in terminal tabanlı yapay zekâ kodlama aracı; npm ile global olarak kurulur ve Voicebox MCP sunucusu buna eklenir. | 0:21 | 'Claude Code one-liner' ve 'claude mcp' komut satırı. (karede: Kod ekranının alt kısmında 'Claude Code one-liner' başlığı ve 'claude mcp' ile başlayan kesik bir komut.) |
| npm | yok | CLI | yok | Node.js paket yöneticisi; Claude Code'u global olarak kurmak için kullanılır. | 0:27 | 'npm install -g @anthropic-ai/claude-code' komutu. (karede: kanıttan) 'npm install -g @anthropic-ai/claude-code' komutu. |
| curl | yok | CLI | yok | Komut satırından HTTP istekleri gönderen araç; Voicebox'ın yerel API'sini çağırmak için örneklerde kullanılır. | 0:21 | 'curl -X POST http://127.0.0.1:17493/generate' komut örnekleri. (karede: Kod bloğunda üst üste curl komutları: /generate, /speak, /transcribe ve /profiles.) |
| Cursor | yok | teknik | yok | Yapay zekâ destekli kod editörü; Voicebox MCP sunucusunu kullanabileceği belirtiliyor. | 0:21 | 'Claude Code, Cursor, Windsurf, Cline, VS Code MCP extensions' metni. (karede: MCP açıklama metninde 'Claude Code, Cursor, Windsurf' sıralaması.) |
| Windsurf | yok | teknik | yok | Yapay zekâ destekli kod editörü; Voicebox MCP sunucusunu kullanabileceği belirtiliyor. | 0:21 | 'Claude Code, Cursor, Windsurf, Cline, VS Code MCP extensions' metni. (karede: MCP açıklama metninde 'Windsurf' adı.) |
| Cline | yok | teknik | yok | VS Code tabanlı yapay zekâ kodlama eklentisi; Voicebox MCP sunucusunu kullanabileceği belirtiliyor. | 0:21 | 'Claude Code, Cursor, Windsurf, Cline, VS Code MCP extensions' metni. (karede: MCP açıklama metninde 'Cline' adı.) |
| VS Code | yok | teknik | yok | Microsoft'un kod editörü; MCP eklentileriyle Voicebox MCP sunucusunu kullanabileceği belirtiliyor. | 0:21 | 'Cline, VS Code MCP extensions' metni. (karede: MCP açıklama metninde 'VS Code MCP extensions' ifadesi.) |
## Açıklama bağlantıları
- yok
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Kahraman bölümü (hero section) | Sayfanın üstünde büyük 'Clone, dictate and create.' başlığı, kısa açıklama metni ve ürün tanıtımı. (karede: Ana sayfa üst kısmında büyük beyaz 'Clone, dictate and create.' başlığı, altında açıklama ve 'DOWNLOAD' düğmesi.) | 0:30 | kare |
| Çağrı düğmesi (call-to-action button) | Sarı 'DOWNLOAD' düğmesi ve yanındaki 'View on GitHub' bağlantısı ile indirmeye yönlendirme. (karede: Ortada koyu sarı 'DOWNLOAD' düğmesi, altında küçük 'View on GitHub' bağlantısı.) | 0:30 | kare |
| Kart ızgarası yerleşimi (card grid layout) | Ses profillerinin kart ızgarası; her kartta profil adı, kısa açıklama ve önizleme. (karede: Koyu arka plan üzerinde Jarvis, Samuel L. Jackson, Bob Ross, Morgan Freeman, Linus Tech Tips gibi profil kartları.) | 0:30 | kare |
| Rozet satırı (badge row) | README üstündeki indirme sayısı, sürüm, yıldız, lisans ve 'Ask DeepWiki' rozetleri. (karede: Başlık altında 'downloads 1.5M', 'release v0.5.0', 'stars 38k', 'license MIT', 'Ask DeepWiki' rozetleri.) | 0:08 | kare |
| Sekme gezintisi (tab navigation) | Üst kısımda README, Contributing, MIT license ve Security sekmeleri. (karede: Ekranın üstünde 'README', 'Contributing', 'MIT license', 'Security' sekme bağlantıları.) | 0:08 | kare |
| Ses dalga formu görseli (waveform visualization) | Uygulama ekran görüntüsünün altında ses dalgası çizgisi ve ana büyük başlık 'Clone Voi...'. (karede: Uygulama ekran görüntüsünün sol alt kısmında yatay ses dalgası; üstünde büyük 'Clone Voi' başlığı.) | 0:08 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| curl -X POST http://127.0.0.1:17493/generate -H "Content-Type: application/json" -d '{"text": "Hello world", "profile_id": "abc123", "language": "en"}' | Yerel Voicebox API'siyle metinden konuşma üretir. (karede: '# Generate speech' altında curl -X POST .../generate komutu.) | 0:21 | kare |
| curl -X POST http://127.0.0.1:17493/speak -H "X-Voicebox-Client-Id: my-script" -d '{"text": "Deploy complete.", "profile": "Morgan"}' | Bir uygulama ya da betiğin klonlanmış sesle konuşmasını sağlar. (karede: '# Agent voice output' altında curl .../speak komutu.) | 0:21 | kare |
| curl -X POST http://127.0.0.1:17493/transcribe -F "audio=@recording.wav" -F "model=whisper-turbo" | Ses dosyasını yazıya çevirir. (karede: '# Transcribe an audio file' altında curl .../transcribe komutu.) | 0:21 | kare |
| curl http://127.0.0.1:17493/profiles | Ses profillerini listeler. (karede: '# List voice profiles' altında curl komutu.) | 0:21 | kare |
| claude mcp add ... --url http://... | Voicebox MCP sunucusunu Claude Code'a ekler (komut kısmen okunuyor). (karede: 'Claude Code one-liner' altında 'claude mcp' ve '--url htt' parçaları.) | 0:22 | kare |
| npm install -g @anthropic-ai/claude-code | Claude Code'u global kurar; kurulum bölümü sırasında ekranda görünüyor. (karede: '1. Install the latest version of Claude Code' altında npm install komutu.) | 0:27 | kare |
| claude mcp … (kesik komut, tam hali okunamadı) | Voicebox MCP sunucusunu Claude Code'a ekler; 'Claude Code one-liner' bölümünde gösterilir. (karede: Kod ekranının altında 'Claude Code one-liner' başlığı ve 'claude mcp' ile başlayan kesik komut satırı.) | 0:21 | kare |
| curl -X POST http://127.0.0.1:17493/speak -H "Content-Type: application/json" -H "X-Voicebox-Client-Id: my-script" -d '{"text": "Deploy complete.", "profile": "Morgan"}' | Bir betik ya da ajanın ses profiliyle konuşmasını sağlar. (karede: Kod bloğunda 'Agent voice output' yorumunun altında /speak örneği.) | 0:21 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Voicebox, ElevenLabs ve Wispr Flow'un işini yerelde ücretsiz yapıyor. | 0:30 | karşılaştırma |
| API key, aylık abonelik ve kullanım limiti yok. | 0:00 | özellik |
| Birkaç saniyelik ses kaydıyla ses klonlama yapılabiliyor. | 0:10 | özellik |
| Sistem geneli dikte kısayoluyla konuşulan metin açık uygulamaya yazılıyor. | 0:14 | özellik |
| Repo 33 bin yıldızı geçti. | 0:23 | sayısal |
| Kurulum bir dakikadan kısa sürüyor, tek komut. | 0:25 | sayısal |
| Veriler dışarı çıkmıyor, her şey yerelde çalışıyor. | açıklama | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma/ekran 0:00 | ElevenLabs | ElevenLabs | Ekran 'ElevenLabs ve WisprFlow'u' |
| konuşma/ekran 0:00 | Wispr Flow | Wispr Flow | Ekran 'WisprFlow' |
| kare 0:04 | API key generated ekranı | aday değil: konu dışı | 'API key generated', 'NO API KEYS' |
| kare 0:05 | Monthly Subscription ve usage bar | aday değil: genel kavram | 'Monthly Subscription', 'UNLIMITED USAGE' |
| konuşma 0:08 | GitHub reposu | GitHub | 'Github reposu' |
| kare 0:08 | Voicebox | Voicebox | README başlığı Voicebox |
| kare 0:08 | GitHub Trending rozeti | aday değil: başka adayın parçası (GitHub) | '#1 Repository Of The Day' |
| kare 0:08 | Ask DeepWiki rozeti | aday değil: başka adayın parçası (Voicebox) | 'Ask DeepWiki' |
| kare 0:08 | MIT license | aday değil: genel kavram | 'MIT license' |
| kare 0:10 | Ses klonlama | aday değil: başka adayın parçası (Voicebox) | 'Clone voice' |
| kare 0:12 | Linus Sebastian profili | aday değil: başka adayın parçası (Voicebox) | 'Linus Sebastian' |
| kare 0:13 | Push to talk | aday değil: başka adayın parçası (Voicebox) | 'PUSH TO TALK' |
| kare 0:21 | Whisper | Whisper | 'model=whisper-turbo' |
| kare 0:21 | curl | aday değil: başka adayın parçası (Voicebox) | curl istekleri |
| kare 0:21 | MCP server | MCP server | 'MCP server' |
| kare 0:21 | Claude Code | aday değil: başka adayın parçası (MCP server) | 'Claude Code one-liner' |
| kare 0:22 | Cursor, Windsurf, Cline, VS Code | aday değil: başka adayın parçası (MCP server) | MCP-aware agent listesi |
| kare 0:27 | npm ve Claude Code kurulumu | aday değil: konu dışı | 'npm install -g @anthropic-ai/claude-code' |
| kare 0:27 | NVIDIA NIM | aday değil: konu dışı | 'NVIDIA NIM.' |
| kare 0:30 | Voicebox ses profilleri | aday değil: başka adayın parçası (Voicebox) | 'Jarvis', 'Morgan Freeman' |
| açıklama | Rehber ve SES yorum çağrısı | aday değil: konu dışı | 'Yorumlara SES yaz' |
| yorum | Yorumlar | aday değil: konu dışı | Girişsiz alınamadı |
## Kareden okunanlar
- 0:08: Voicebox README: 'Clone any voice. Generate speech. Dictate into any app'; rozetler downloads 1.5M, release v0.5.0, stars 38k, license MIT, Ask DeepWiki; '#1 Repository Of The Day'; ekranda 'Clone Vo i'.
- 0:21: README: localhost:17493 üzerinde generate, speak, transcribe, profiles curl örnekleri; 'MCP server' bölümü; konuşmacı kamerada, altyazı 'bu proje tamamen açık kaynak'.
- 0:30: Voicebox sayfası: 'Clone, dictate and create.'; 'ElevenLabs and WisprFlow, running entirely on your machine'; DOWNLOAD ve View on GitHub düğmeleri; Jarvis, Morgan Freeman, Bob Ross gibi ses profilleri.
## Belirsizlikler
- Kurulum komutu videoda net gösterilmiyor; 0:27'deki npm komutu Claude Code'a ait ve başka bir README'den olabilir.
- Cursor, Windsurf, Cline, VS Code ve Claude Code README'de MCP uyumlu istemci listesinde görünüyor; videoda kullanılmıyor.
- Ask DeepWiki rozeti yalnızca README'de görünüyor, kullanılmıyor.
- Karedeki yıldız rozeti 38k, konuşmada 33 bin deniyor; fark var.
- Yorumlar girişsiz alınamadı; rehber bağlantısı ve repo URL'si videoda verilmiyor.
- Dil bilgisi belirtilmemiş; altyazı Türkçe.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.instagram.com/reel/DcgPETIMIhq/ | açıklama | açıklama | hayır |
| http://127.0.0.1:17493/generate | 0:21 | ekran | hayır |
| http://127.0.0.1:17493/speak | 0:21 | ekran | hayır |
| http://127.0.0.1:17493/transcribe | 0:21 | ekran | hayır |
| http://127.0.0.1:17493/profiles | 0:21 | ekran | hayır |
## İş akışı
- 1. adım — ElevenLabs ve Wispr Flow'un ücretli abonelik ve API key sorunu gösteriliyor. — araçlar: ElevenLabs, Wispr Flow
- 2. adım — Açık kaynak Voicebox GitHub reposu README'siyle tanıtılıyor. — araçlar: Voicebox, GitHub
- 3. adım — Birkaç saniyelik kayıtla ses klonlama arayüzü gösteriliyor. — araçlar: Voicebox
- 4. adım — Sistem geneli push-to-talk dikte kısayolu anlatılıyor. — araçlar: Voicebox
- 5. adım — Yerel API örnekleri ve MCP sunucusu gösteriliyor. — araçlar: Voicebox, MCP server, Whisper
- 6. adım — Lisans ve yıldız sayısı gösteriliyor. — araçlar: GitHub
- 7. adım — Tek komutlu kurulum anlatılıyor. — araçlar: Voicebox
- 8. adım — Voicebox ana sayfası ve ses profilleri gösteriliyor. — araçlar: Voicebox
- 9. adım — İzleyiciye yorumlara SES yazması için çağrı yapılıyor. — araçlar: Instagram
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
