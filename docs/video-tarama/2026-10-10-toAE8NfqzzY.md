# Bu GitHub Reposu Ajansları Bitirebilir: Claude Code ile Sıfırdan AI Video Uygulaması Yap
## Künye
Bu GitHub Reposu Ajansları Bitirebilir: Claude Code ile Sıfırdan AI Video Uygulaması Yap · Burhan KOCABIYIK · süre: 15:51 · tr-orig · https://youtu.be/toAE8NfqzzY · şema 2
motor: parti 2026-10-10-short-16 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 72535 tk · claude-haiku-5-5: claude-haiku-5-5 · 127155 tk
## Özet
Burhan Kocabıyık, Anil-matcha'nın açık kaynaklı Open-Generative-AI reposunu (Higgsfield alternatifi) temel alıp Claude Code (Opus 4.7) ile SaaS ve ajanslara yönelik bir AI içerik/video uygulaması (GOAT UGC AI) kuruyor. Uygulama GitHub'a yüklenip Vercel'e deploy ediliyor, fal.ai ile görsel/video üretiyor. Ardından Remotion tabanlı video oluşturucu, sahne editörü, Nano Banana 2, Seedance 2.0 ve text-to-video modu ekleniyor; LTX-2 ile lokal ücretsiz üretim anlatılıyor ve canlı testte altyazılı bir B2B faturalama teaser videosu üretiliyor.
## Bölümler
- 0:00 Giriş: Yeni AI Video Reposu ve SaaS Vizyonu
- 1:32 VS Code Hazırlığı ve Claude Code Otonom Mod Aktivasyonu
- 4:39 Vercel Deployment ve Çoklu Ajan Mimarisi İncelemesi
- 6:25 Prototipal Gelir Analizi ve SaaS Fiyatlandırma Stratejileri
- 7:42 Stüdyo Arayüzü ve ReMotion Video Üretim Pipeline'ı
- 9:39 Fal.ai (Nano Banana 2 & Kling V3) Modellerini Entegre Etmek
- 12:16 LTX 2 ile Lokal Bilgisayarda Ücretsiz Video Üretme Yöntemi
- 13:48 Canlı Test: Text-to-Video ve Otomatik Altyazı Jenerasyonu
- 15:44 Kapanış ve Open-Source Klonlama Detayları
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Open-Generative-AI | yok | iş akışı | https://github.com/Anil-matcha/Open-Generative-AI | Higgsfield benzeri, 200+ modelli açık kaynak görsel/video stüdyo reposu; proje temeli olarak klonlanıyor | 0:10 | Repo sayfası: Open-Generative-AI, 'Uncensored, open-source alternative to Higgsfield AI' (karede: GitHub'da Anil-matcha/Open-Generative-AI repo sayfası, About'ta 200+ models, klasör listesi) |
| Claude Code | yok | CLI | yok | Uygulamayı baştan sona kodlayan, deploy eden ana yapay zekâ kodlama aracı | 1:38 | Claude Code v2.1.119 karşılama ekranı terminalde (karede: VS Code terminalinde Claude Code v2.1.119 başlık kutusu, Opus 4.7 (1M context) · Claude Max) |
| Claude Opus 4.7 | yok | prompt | yok | Sunucunun içinde çalıştığı ana model (Opus 4.7, 1M context) | 1:38 | Opus 4.7 (1M context) · Claude Max (karede: Claude Code karşılama kutusunda 'Opus 4.7 (1M context) · Claude Max') |
| VS Code | yok | iş akışı | yok | Yeni pencere/klasör açılıp terminalde Claude çalıştırılan editör | 1:24 | Visual Studio Code karşılama ekranı (karede: Visual Studio Code 'Editing evolved' karşılama sayfası, Clone Git Repository seçeneği) |
| Vercel | yok | CLI | yok | Uygulamanın deploy edildiği platform; vercel deploy --prod komutu | 4:44 | vercel deploy --prod --yes ve vercel inspect çıktıları (karede: Terminalde Bash(vercel deploy --prod --yes 2>&1 / tail -15), Vercel CLI 50.22.1) |
| fal.ai | yok | MCP | yok | Görsel ve video üretimi için kullanılan bulut model sağlayıcısı (FAL_KEY ile) | 6:40 | Provider: fal.ai (FAL_KEY env'de set, AI_PROVIDER=fal) (karede: Terminalde 'Provider: fal.ai', model: flux-schnell, fal.media görsel URL'si) |
| Remotion | yok | teknik | yok | Sahneleri tarayıcıda önizleyen ve birleştiren video çerçevesi (Remotion Player) | 9:40 | Remotion Player tarayıcıda önizleme, Ken Burns + fade + altyazı (karede: Terminal özetinde 'Remotion Player tarayicida önizleme — Ken Burns + fade + altyazı') |
| Flux Schnell | yok | teknik | yok | Ankraj görsel üretimi için varsayılan hızlı görsel modeli | 6:56 | Create sayfasında model: Flux Schnell (fast) (karede: Create sayfası model açılır listesinde 'Flux Schnell (fast)') |
| Nano Banana 2 | yok | teknik | yok | Görsel modeli olarak eklenen Google modeli (fal.ai üzerinden) | 10:52 | Nano Banana 2 (Google, fast) model listesinde (karede: Video builder'da Image model olarak 'Nano Banana 2 (Google, fast)' seçili) |
| Nano Banana Pro | yok | teknik | yok | Premium Google görsel modeli seçeneği | 10:36 | fal-ai/nano-banana-pro (Google, premium) ekleneni listesinde (karede: Terminal özetinde 'fal-ai/nano-banana-pro (Google, premium)') |
| Seedance 2.0 | yok | teknik | yok | Text-to-video ve motion klipleri için kullanılan video modeli | 10:36 | endpoint: bytedance/seedance-2.0/text-to-video (karede: Terminalde model: seedance-2-t2v, endpoint bytedance/seedance-2.0/text-to-video) |
| Kling v3 | yok | teknik | yok | Video modeli olarak istenen/ kullanılması önerilen Kling modeli | 9:39 | Cdream 2'yi veya clink V3'ü kullan diyelim |
| Kling v1 | yok | teknik | yok | İsteğe bağlı motion clip için başlangıçta kullanılan Kling modeli | 9:38 | isteğe bağlı Kling v1 motion clip (karede: Terminal özetinde 'flux-schnell ile 1280x720 görsel + isteğe bağlı Kling v1 motion clip') |
| GPT-4o mini | yok | teknik | yok | Sahne planlayıcıda fal-ai/any-llm üzerinden kullanılan LLM | 10:02 | Scene planner (fal-ai/any-llm - gpt-4o-mini) (karede: Terminalde 'Scene planner (fal-ai/any-llm - gpt-4o-mini) bir konudan 3-8 sahneli çekim listesi') |
| LTX-2 | yok | teknik | https://github.com/Lightricks/LTX-2 | Lokalde ücretsiz video üretmek için açık kaynak Lightricks modeli | 11:50 | git clone https://github.com/Lightricks/LTx-2.git, uv sync --frozen (karede: Lightricks/LTX-2 GitHub sayfası, 'Official Python inference and LoRA trainer package') |
| uv | yok | CLI | yok | LTX-2 bağımlılıklarını kuran Python paket yöneticisi | 11:50 | uv sync --frozen (karede: LTX-2 README'sinde kurulum komutu uv sync --frozen, repoda uv.lock) |
| frontend-design | yok | plugin | yok | Claude Code HTML/CSS çalışması için önerilen eklenti | 10:32 | /plugin install frontend-design@claude-plugins-official (karede: Claude Code ipucu: 'Tip: Working with HTML/CSS? Install the frontend-design plugin') |
| GitHub CLI | yok | CLI | yok | gh ile kimlik kontrolü ve repo oluşturma/push işlemleri | 3:58 | Bash(which gh node npm git; gh auth status) (karede: Terminalde Bash(which gh node npm git 2>&1; gh auth status 2>&1)) |
| Git | yok | CLI | yok | Repo klonlama, commit, push ve amend işlemleri | 3:22 | git clone https://github.com/Anil-matcha/Open-Generative-AI.git source-repo (karede: Terminalde git clone ... source-repo && ls -la source-repo/) |
| Next.js | yok | teknik | yok | Uygulamanın web çatısı (Next.js 15.5.4) | 1:22 | Next.js 15.5.4'e yükseltildi (güvenlik patch) (karede: Terminal commit mesajında Next.js 15.5.4 ve React 19 stable) |
| React | yok | teknik | yok | Arayüz kütüphanesi (React 19) | 1:22 | React 19 stable (karede: Terminal commit mesajı satırlarında 'React 19 stable') |
| Tailwind CSS | yok | teknik | yok | Repo dosyalarında bulunan stil çerçevesi (tailwind.config.js) | 5:34 | Dosya ağacında tailwind.config.js, postcss.config.js (karede: VS Code gezgininde tailwind.config.js ve postcss.config.js dosyaları) |
| Inter | yok | teknik | yok | Webfont ailesi (Inter + JetBrains Mono) | 1:22 | Inter + JetBrains Mono webfonts (karede: Terminalde '- Inter + JetBrains Mono webfonts' satırı) |
| JetBrains Mono | yok | teknik | yok | Monospace webfont ailesi | 1:22 | Inter + JetBrains Mono webfonts (karede: Terminalde '- Inter + JetBrains Mono webfonts' satırı) |
| Muapi.ai | yok | CLI | yok | Orijinal repoda bağlı olan API sağlayıcı; videoda kaldırılması istendi | 7:42 | Muapi API'ını da kullanmayacağız. Oradaki API'yi hiçbir şekilde |
| Higgsfield | yok | teknik | yok | Reponun birebir benzerini yaptığı referans ürün | 0:00 | Hixfield'ın birebir aynısını oluşturmuşlar |
| Sora 2 | yok | teknik | yok | Video üretimi için örnek model olarak anıldı | 0:00 | Sora 2 ile çok mükemmel videolar oluşturabilirsiniz |
| goat-youtube | yok | iş akışı | yok | Yazarın açık kaynak YouTube otomasyon projesi; Scene bileşeni ve pipeline buradan alındı | 8:42 | Starter God YouTube projesini Gitup'tan çek |
| Vercel CLI | yok | CLI | yok | Terminalden deploy, inspect ve list için kullanılan araç | 4:46 | Vercel CLI 50.22.1 inspect çıktısı (karede: Terminalde 'Vercel CLI 50.22.1' ve vercel inspect çıktısı) |
| Prototipal | yok | iş akışı | yok | Yazarın önceki SaaS ürünü; gelir örneği olarak gösterildi (TrustMRR sayfası) | 6:12 | Prototipal all-time revenue $99,320 (karede: Prototipal startup sayfası, All-time revenue $99,320, Stripe API ile doğrulanmış gelir) |
| GOAT UGC AI | yok | teknik | yok | Videoda Claude Code ile geliştirilen SaaS AI stüdyo uygulaması (Next.js, fal.ai, Remotion). | 6:40 | Canlı URL: goat-ugc-ai.vercel.app; Provider: fal.ai (karede: Terminal çıktısında canlı URL, sağlayıcı ve repo bilgisi) |
| Node.js | yok | teknik | yok | Open Generative AI'ın yerel build ve çalıştırma gereksinimi; yerel kurulum için anılıyor. | 1:01 | One-click installers — no Node.js or terminal required. (karede: Repo README kurulum bölümü) |
| Açık kaynak repodan SaaS içerik üretim uygulaması kurmak | yok | prompt | yok | GitHub reposunu klonla, SaaS ve ajanslar için içerik üreten bir uygulamaya çevir; fal.ai kullan, private repo olarak GitHub'a yükle ve Vercel'e deploy et; yerelde de çalışabilsin, açık kaynak ve bulut sürümü olsun. | 1:32 | kaynak: altyazı |
| Claude Code'u otomatik modda uzun işe bırakmak | yok | prompt | yok | Otonom modda çalış, her şeyi bitir, sonunda tek seferde onaylayacağım. | 3:34 | kaynak: altyazı |
| Remotion tabanlı sahne planlayıcılı video pipeline'ı kurmak | yok | prompt | yok | Ürün videoları üretecek sistemi kur, Remotion kullanabilirsin; Muapi API'yi ve sayfasını kaldır, yalnız fal.ai kullan; konuyu ben vereyim, sahne ve promptları sen yaz; goat-youtube projesini GitHub'dan çekip işe yarayanı al. | 7:26 | kaynak: altyazı |
| Görsel slayt yerine yapay zekâ video klipleri üretmek | yok | prompt | yok | Görsel değil videolar eklensin; görselleri ve videoları yapay zekayla üret; görsel modeli Seedream 2 ya da video için Kling v3, fal.ai üzerinden. | 9:39 | kaynak: kare |
## Açıklama bağlantıları
- https://benburhan.gumroad.com/l/bsrxgi — Yazarın Gumroad sayfası (dosyalar/kaynaklar) · aday: hayır · Yazarın kendi dosya/ürün satış sayfası; izleyicinin kullanacağı araç değil, referans/kaynak bağlantısı · sınıf: diğer
- https://youtu.be/oGI1YmC2L00 — Yazarın diğer YouTube videosu · aday: hayır · Başka video bağlantısı, araç/servis değil · sınıf: diğer
- https://youtu.be/nXvWTR88sfU — Yazarın diğer YouTube videosu · aday: hayır · Başka video bağlantısı, araç/servis değil · sınıf: diğer
- https://youtu.be/qm0ZlYezt1Q — Yazarın diğer YouTube videosu · aday: hayır · Başka video bağlantısı, araç/servis değil · sınıf: diğer
- https://github.com/anil-matcha/open-generative-ai — Videoda kullanılan açık kaynak repo · aday: evet (Open-Generative-AI) · Videoda klonlanıp temel alınan, izleyicinin kullanabileceği repo · sınıf: diğer
- skool.com/doa/about — DOA topluluk sayfası (Skool) · aday: hayır · Topluluk tanıtım sayfası; kullanılan bir araç değil. · sınıf: diğer · erişilemez: ücretli topluluk olabilir; giriş gerekli
- skool.com/doa-zero/about — Ücretsiz kaynaklar sayfası (Skool) · aday: hayır · Kaynak/topluluk tanıtım sayfası; araç değil. · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Koyu temalı hero bölümü (hero section) ve büyük başlık, vurgu rengi neon yeşil/sarı | Ana sayfada 'Creative AI studio for apps and agencies' başlığı, iki CTA düğmesi ve açık kaynak rozeti (karede: (karede OCR) Startpagina 8 Home / ARspar 3D NFT Generator... in LinkedIn Mijn Drive - Devel... ARspar Dashboard.. ARspar - 2022 - V... ARspar Dashboard > DeepL Translator L Slack / arspar-tbf /.. All Bookmarks « G) | 7:02 | kare |
| Üst gezinme çubuğu (navbar) | GOAT UGC AI logosu, Features / How it works / Self-host / GitHub bağlantıları, Dashboard ve Start creating düğmeleri (karede: (karede OCR) Startpagina 8 Home / ARspar 3D NFT Generator... in LinkedIn Mijn Drive - Devel... ARspar Dashboard.. ARspar - 2022 - V... ARspar Dashboard > DeepL Translator L Slack / arspar-tbf /.. All Bookmarks « G) | 7:02 | kare |
| Özellik kartları ızgarası (feature card grid) | Image Studio, Video Studio, Lip Sync & Cinema, Agents & Workflows kartları (karede: (karede OCR) Startpagina 8 Home / ARspar 3D NFT Generator... in LinkedIn Mijn Drive - Devel... ARspar Dashboard.. ARspar - 2022 - V... ARspar Dashboard > DeepL Translator L Slack / arspar-tbf /.. All Bookmarks « G) | 7:02 | kare |
| Üç adımlı nasıl çalışır bölümü (steps section) | Pick a model, Brief the studio, Ship the asset kartları (karede: (karede OCR) 8 Startpagina Slack / arspar-tbf ... ARspar Dashboard... ARspar - 2022 - V... LinkedIn 3D NFT Generator... All Bookmarks DeepL Translator Mijn Drive - Devel... ARspar Dashboard Home / ARspar in > « □) | 6:50 | kare |
| İki sütunlu dağıtım kartları (deployment cards) | Cloud: Deploy to Vercel in 2 minutes; Local: Run on your own GPU (karede: (karede OCR) 8 Home / ARspar Mijn Drive - Devel... ARspar Dashboard... Startpagina Slack / arspar-tbf /.. ARspar - 2022 - V... 3D NFT Generator... in LinkedIn DeepL Translator ARspar Dashboard All Bookmarks > « GO) | 6:52 | kare |
| Gösterge paneli kart ızgarası (dashboard cards) | Provider, Image Gen, Video Gen, Agents durum kartları ve Quick create/Generate/Workspaces/Hosting kartları (karede: (karede OCR) Startpagina 8 in LinkedIn Mijn Drive - Devel... ARspar Dashboard... Home / ARspar Slack / arspar-tbf /... ARspar - 2022 - V... 3D NFT Generator... DeepL Translator ARspar Dashboard All Bookmarks > « G) | 6:54 | kare |
| Basit üretim formu (generator form) | Create sayfasında prompt kutusu, model açılır listesi, en-boy oranı düğmeleri ve Generate düğmesi (karede: (karede OCR) 8 Startpagina Home / ARspar 3D NFT Generator... Slack / arspar-tbf .. in LinkedIn ARspar Dashboard... ARspar - 2022 - V... < DeepL Translator Mijn Drive - Devel... ARspar Dashboard All Bookmarks < Das) | 6:56 | kare |
| Proje yönetimi formu (project form) | Projects sayfasında proje adı, marka alanı ve Create project düğmesi (karede: (karede OCR) Startpagina 8 Home / ARspar 3D NFT Generator... in LinkedIn Mijn Drive - Devel... ARspar Dashboard.. ARspar - 2022 - V... ARspar Dashboard > DeepL Translator L Slack / arspar-tbf /.. All Bookmarks « G) | 7:02 | kare |
| İki sütunlu video oluşturucu (video builder layout) ve video oynatıcı (video player) | Sol brief formu, sağda Remotion Player ve sahne çekim listesi (karede: (karede OCR) % goat-ugc-ai.vercel.app/video @ ≡ Finish update C : * → 8 ARspar - 2022 - V... ARspar DashboardHome / ARspar in Linkedln DeeplL Translator Startpagina Mijn Drive - Devel.. ARspar Dashboard... Slack /) | 9:14 | kare |
| Sahne çekim listesi (scene shot list) ve küçük resimler (thumbnails) | Her sahne için süre, animasyon etiketi, altyazı ve Regenerate/Open düğmeleri (karede: (karede OCR) % goat-ugc-ai.vercel.app/video ≡ Finish update C * : → 8 DeepL Translator Mijn Drive - Devel... ARspar Dashboard... ARspar DashboardHome / ARspar Slack / arspar-tbf /..ARspar - 2022 - V... in LinkedIn) | 9:18 | kare |
| Zaman çizelgeli sahne editörü (scene editor / timeline) | Sahne başına 5s/10s seçimi, animasyon açılır listesi, altyazı alanı, yukarı/aşağı/sil düğmeleri, açılır Prompt details (karede: (karede OCR) 8 Home / ARspar in Linkedln DeepL. Translator Mijn Drive - Devel... ARspar Dashboard... ARspar Dashboard Slack / arspar-tbf l... ARspar - 2022 - V... Startpagina 3D NFT Generator... All Bookmarks □ >) | 12:34 | kare |
| Yükleme iskeleti (loading placeholder) | Render edilmemiş sahnelerde 'Rendering...' yer tutucusu (karede: (karede OCR) 8 Mijn Drive - Devel... Home / ARspar ARspar Dashboard.. ARspar - 2022 - V... Startpagina in LinkedIn DeepL Translator ARspar Dashboard 3D NFT Generator... Slack / arspar-tbf /... All Bookmarks « □ *) | 12:48 | kare |
| Video üzerine altyazı bindirmesi (subtitle overlay) | Üretilen videoda alt kısımda yeşil çizgili altyazı kutusu (karede: (karede OCR) C Invoiera Due tas Sru4 pumoqmo INV-2024-001 $1,080.00 Desttard Invoxa Daete 1006/2124 pquão b Adtrs: 123 Street New York, NY 10001 a Enftumates invssuices $1,000.00 Olent Jom Smith ©Peymarts © Paymen) | 14:08 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| claude | VS Code terminalinde Claude Code'u başlatır (karede: Terminalde 'arspar@MacBook-Pro-5 goat-ugc-ai % claude') | 3:30 | kare |
| git clone https://github.com/Anil-matcha/Open-Generative-AI.git source-repo && ls -la source-repo/ | Kaynak repoyu klonlar ve içeriğini listeler (karede: Terminal satırında git clone ... source-repo && ls -la source-repo/) | 3:22 | kare |
| which gh node npm git; gh auth status | Gerekli araçların kurulu ve GitHub girişinin yapılı olduğunu kontrol eder (karede: Bash(which gh node npm git 2>&1; gh auth status 2>&1)) | 3:58 | kare |
| which vercel; vercel --version | Vercel CLI kurulumunu ve sürümünü kontrol eder (karede: Satır: which vercel 2>&1; vercel -version 2>&1) | 4:07 | kare |
| vercel deploy --prod --yes | Projeyi Vercel'e production olarak yayınlar (karede: Bash(vercel deploy --prod --yes 2>&1 / tail -15)) | 4:46 | kare |
| vercel inspect <deployment-url> | Deploy durumunu ve loglarını inceler (karede: Bash(sleep 15 && vercel inspect https://goat-ugc-...vercel.app 2>&1 / head -15)) | 4:44 | kare |
| vercel list goat-ugc-ai | Projenin deploy listesini getirir (karede: Satır: vercel list goat-ugc-ai 2>&1 / head -20) | 4:56 | kare |
| curl -s https://vercel-status.com/api/v2/status.json | Vercel servis durumunu kontrol eder (karede: Bash(curl -s https://vercel-status.com/api/v2/status.json 2>&1 / head -5)) | 5:02 | kare |
| git commit --amend --no-edit --reset-author && git push --force-with-lease | Commit yazarını Vercel hesabının e-postasıyla düzeltip yeniden gönderir (karede: Satır: git -c user.email=... commit --amend --no-edit --reset-author ... git push --force-with-lease) | 5:30 | kare |
| curl -s -X POST https://goat-ugc-ai.vercel.app/api/generate/image -H "Content-Type: application/json" -d '{...}' | Canlı sitedeki fal.ai görsel üretim API'sini test eder (karede: Bash(curl -s -X POST https://goat-ugc-ai.vercel.app/api/generate/image -H ...)) | 6:40 | kare |
| curl -s -X POST https://goat-ugc-ai.vercel.app/api/video/plan -H "Content-Type: application/json" -d '{...}' | Sahne planlayıcı API'sini test eder (karede: Bash(curl -s -X POST https://goat-ugc-ai.vercel.app/api/video/plan ...)) | 9:38 | kare |
| /plugin install frontend-design@claude-plugins-official | Claude Code için frontend-design eklentisini kurar (ipucu olarak gösterildi) (karede: Claude Code ipucu satırı '/plugin install frontend-design@claude-plugins-official') | 10:32 | kare |
| curl -s -X POST https://goat-ugc-ai.vercel.app/api/generate/video | Seedance 2.0 text-to-video canlı testini yapar (karede: Bash(echo "--- Seedance 2.0 text-to-video live test ---"; time curl -s -X POST .../api/generate/video ...)) | 10:36 | kare |
| git clone https://github.com/Lightricks/LTx-2.git | LTX-2 modelini lokal kurulum için klonlar (karede: LTX-2 sayfasında kurulum satırı git clone https://github.com/Lightricks/LTx-2.git) | 11:50 | kare |
| uv sync --frozen | LTX-2 Python bağımlılıklarını kilit dosyasından kurar (karede: LTX-2 sayfasında kurulum satırı uv sync --frozen) | 11:50 | kare |
| npm run electron:build:linux | Linux masaüstü uygulamasını yerelde derler (README'de) (karede: README'de Linux (Ubuntu x64): Build locally with npm run electron:build:linux) | 1:01 | kare |
| git add -A && git -c user.email=<e-posta> -c user.name=<ad> commit -q -m "feat: make fal.ai the default landing experience" | Değişiklikleri hazırlayıp fal.ai varsayılan olacak şekilde commit eder. (karede: Terminalde git add ve commit komutu) | 4:44 | kare |
| git push origin main (goatstarter/goat-ugc-ai.git) | Commit'i özel GitHub reposuna gönderir. (karede: Terminalde git push çıktısı ve GitHub adresi) | 4:52 | kare |
| sleep 15 && vercel inspect <deployment-url> 2>&1 / head -15 | Deploy bekler ve deployment durumunu özetler. (karede: Terminalde sleep ve vercel inspect komutu) | 4:44 | kare |
| vercel list goat-ugc-ai 2>&1 / head -20 | goat-ugc-ai projesinin son deployment listesini getirir. (karede: Terminalde deployment listesi) | 4:56 | kare |
| curl -s https://vercel-status.com/api/v2/status.json / head -5 | Vercel durum API'sini sorgular. (karede: Terminalde curl komutu, çıktı boş) | 5:02 | kare |
| vercel inspect --logs <deployment-url> / tail -40 | Başarısız deployment'ın loglarını son 40 satır gösterir. (karede: Terminalde vercel inspect --logs komutu) | 5:28 | kare |
| curl -s -H "Authorization: Bearer <TOKEN>" (Vercel API; token Vercel CLI kimlik dosyasından okunur, değer yazılmaz) | Vercel hesap bilgisini doğrulamak için kimlik sorgusu yapar. (karede: Terminalde Authorization başlıklı curl komutu (token gizli)) | 5:30 | kare |
| curl -s -o /dev/null -w "%{http_code}\n" https://goat-ugc-ai.vercel.app/ (ve /create, /studio, /api/config) | Canlı sayfa ve API uç noktalarının HTTP durum kodunu kontrol eder. (karede: Terminalde http_code kontrol çıktısı) | 6:28 | kare |
| curl -s -X POST https://goat-ugc-ai.vercel.app/api/generate/image -H "Content-Type: application/json" -d '{"prompt":"cinematic portrait of a female startup founder..."}' | Canlıda fal.ai üzerinden görsel üretim isteği gönderir. (karede: Terminalde curl POST komutu ve JSON yanıt) | 6:40 | kare |
| curl -s -X POST https://goat-ugc-ai.vercel.app/api/video/plan -H "Content-Type: application/json" -d '{"topic":"30-second launch teaser for a B2B invoicing SaaS..."}' | Konudan sahne planı (plan.json) üretir. (karede: Terminalde video/plan curl komutu) | 9:38 | kare |
| curl -s -X POST https://goat-ugc-ai.vercel.app/api/generate/image -d '{"prompt":"A dimly lit office with a stressed professional..."}' | Sahne için görsel üretir (flux-schnell, 1280×720). (karede: Terminalde görsel üretim curl komutu) | 9:38 | kare |
| curl -s -X POST https://goat-ugc-ai.vercel.app/api/video/plan -d '{"topic":"30-second launch teaser..."}' (yeniden çalıştırma) | Scene planner'ı yeniden çalıştırıp sahne listesini doğrular. (karede: Terminalde ikinci video/plan çağrısı) | 10:02 | kare |
| time curl -s -X POST https://goat-ugc-ai.vercel.app/api/generate/video -H "Content-Type: application/json" -d '...' | Seedance 2.0 text-to-video canlı testi; süreyi ölçer. (karede: Terminalde time curl video üretim komutu) | 10:36 | kare |
| /init | Claude Code'da CLAUDE.md dosyası oluşturur. (karede: Claude Code ipucu: 'Run /init to create a CLAUDE.md file') | 3:30 | kare |
| rm -rf /tmp/goat-youtube && gh repo clone goatstarter/goat-youtube -- --depth 1 | goat-youtube reposunu sığ klon (depth 1) olarak indirir. (karede: Claude Code Bash komut satırı) | 8:18 | kare |
| sleep 8 && vercel deploy --prod --yes 2>&1 / tail -8 | Başka projede 8 sn bekleyip Vercel production deploy çıktısını son 8 satırla gösterir. (karede: Başka proje terminalinde vercel deploy komutu) | 1:22 | kare |
| git commit -m "..." && git push | Başka proje için değişiklikleri commit edip GitHub'a gönderir. (karede: Başka proje terminalinde commit ve push komutları) | 1:22 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Repo 200'den fazla yapay zekâ modeli içeriyor ve kendi bilgisayarınızda çalıştırılabiliyor. | 0:00 | özellik |
| Otomatik modda planlama çok hızlı geçiliyor, istenmeyen işler yapıp ekstra token masrafı çıkarabiliyor. | 3:34 | karşılaştırma |
| Prototipal'ın bir yıllık toplam geliri 99.320 dolar. | 6:12 | sayısal |
| SaaS için aylık abonelik artı kredi mantığı fiyatlandırmada daha iyi çalışıyor. | 5:39 | öneri |
| Sahne sayısı 30'a kadar çıkabiliyor, 5 veya 10 saniyelik klipler üretilebiliyor. | 10:39 | sayısal |
| Her Seedance/Kling klibi 60-180 saniyede hazır oluyor. | 10:54 | sayısal |
| LTX-2 açık kaynak, lokalde çalışır ama daha uzun sürer. | 11:41 | karşılaştırma |
| Sahneler paralel render edildiği için Vercel'in 300 sn fonksiyon penceresini aşmıyor. | 10:36 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Higgsfield | Higgsfield | Hixfield'ın birebir aynısını oluşturmuşlar |
| konuşma 0:00 | Sora 2 | Sora 2 | Sora 2 ile çok mükemmel videolar oluşturabilirsiniz |
| kare 0:10 | Open-Generative-AI repo | Open-Generative-AI | GitHub repo sayfası |
| kare 0:10 | Flux, Midjourney, Kling, Sora, Veo listesi | aday değil: başka adayın parçası (Open-Generative-AI) | Reponun About metninde model listesi |
| kare 0:10 | Freepik, Krea, Openart AI | aday değil: başka adayın parçası (Open-Generative-AI) | About metni alternatif ürün adları |
| kare 0:10 | dev.muapi.ai | Muapi.ai | Repo bağlantısı dev.muapi.ai/open-generative-ai |
| kare 0:12 | MiniMax image-01 | aday değil: başka adayın parçası (Open-Generative-AI) | Commit mesajı: add MiniMax image-01 T2I model |
| kare 0:22 | Next.js monorepo, vite.config | Next.js | Convert to Next.js monorepo; next.config.mjs |
| kare 0:22 | Tailwind CSS, PostCSS | Tailwind CSS | tailwind.config.js, postcss.config.js |
| kare 1:01 | Discord, Node.js, npm | aday değil: başka adayın parçası (Open-Generative-AI) | Reponun README bölümlerinde |
| kare 1:22 | Linear (linear.app) | aday değil: konu dışı | Arka plandaki başka terminal çıktısı, videoda kullanılmıyor |
| kare 1:22 | Inter + JetBrains Mono | Inter | Webfonts satırı (JetBrains Mono ayrı aday) |
| kare 1:24 | Tripo P1, Excalidraw | aday değil: konu dışı | Arka plandaki başka proje çıktılarında |
| kare 1:38 | Claude Code | Claude Code | Claude Code v2.1.119 |
| kare 1:44 | MCP server needs auth | aday değil: genel kavram | Claude Code durum satırı |
| kare 3:22 | git clone | Git | git clone komutu |
| kare 3:58 | gh auth status | GitHub CLI | Bash(which gh ...; gh auth status) |
| kare 4:44 | Vercel deploy | Vercel | vercel deploy --prod |
| kare 4:46 | Vercel CLI 50.22.1 | Vercel CLI | Vercel CLI 50.22.1 |
| kare 4:50 | Stable Diffusion/SDXL | aday değil: başka adayın parçası (Open-Generative-AI) | Dashboard kartında 'Flux, SDXL, Nano Banana' metni |
| konuşma 4:08 | skool canlı yayın | aday değil: konu dışı | Ekranda yazarın canlı yayın sayfası |
| kare 6:12 | Prototipal / Stripe | Prototipal | Gelir sayfası; Stripe yalnız doğrulama notu |
| kare 6:50 | Runway, Canva | aday değil: konu dışı | Landing metninde 'Runway-class generation'; Canva OCR kalıntısı |
| kare 6:52 | Ollama, ComfyUI, sd.cpp, Llama | aday değil: konu dışı | Landing metninde yerel çalışma seçenekleri, videoda kullanılmıyor |
| kare 6:56 | Flux Schnell | Flux Schnell | Model açılır listesi |
| konuşma 7:42 | Remotion | Remotion | belki remotion'ı kullanabiliriz |
| konuşma 8:42 | goat-youtube | goat-youtube | Starter God YouTube projesini çek |
| kare 10:02 | fal-ai/any-llm gpt-4o-mini | GPT-4o mini | Scene planner satırı |
| konuşma 9:39 | Kling V3 | Kling v3 | clink V3'ü kullan |
| kare 9:38 | Kling v1 | Kling v1 | Kling v1 motion clip |
| kare 10:32 | frontend-design | frontend-design | /plugin install frontend-design@claude-plugins-official |
| kare 10:36 | Seedance 2.0 / Nano Banana Pro | Seedance 2.0 | endpoint bytedance/seedance-2.0/text-to-video; Nano Banana Pro ayrı aday |
| kare 10:52 | Kling v2.1 Master/Pro/Standard | aday değil: başka adayın parçası (Kling v3) | Model açılır listesindeki seçenekler, videoda seçilmedi |
| kare 11:46 | LTX-2 / Hugging Face | LTX-2 | Lightricks/LTX-2 sayfası; Hugging Face rozeti yalnız sayfada |
| kare 11:50 | uv sync --frozen | uv | LTX-2 kurulum komutu |
| kare 14:12 | Descript | aday değil: konu dışı | Üretilen video içindeki sahte arayüz metni, araç değil |
| açıklama | Gumroad bağlantısı | aday değil: konu dışı | benburhan.gumroad.com/l/bsrxgi |
| açıklama | YouTube bağlantıları (3 adet) | aday değil: konu dışı | youtu.be bağlantıları |
| açıklama | skool.com/doa ve doa-zero | aday değil: sponsor/reklam | Yazarın kendi topluluk tanıtımı |
| açıklama | Muapi.ai docs bağlantısı | Muapi.ai | muapi.ai/docs/introduction bağlantısı |
| açıklama | fal.ai docs bağlantıları | fal.ai | fal.ai/docs/documentation |
| yorum | Codex, Antigravity | aday değil: konu dışı | Sabit yorumda 'codex, antigravity veya claude code' |
| yorum | Cursor, ChatGPT, Gemini, Obsidian | aday değil: konu dışı | İzleyici yorumlarında anılıyor, videoda gösterilmiyor |
| yorum | Opus 4.8 | aday değil: konu dışı | Yorumda 'Opus 4.8 çıkmışken' sorusu |
| kare 14:08 | Altyazı bindirmesi | aday değil: başka adayın parçası (Remotion) | Remotion Player ile eklenen altyazı |
## Kareden okunanlar
- 0:10: GitHub'da Anil-matcha/Open-Generative-AI: 'Uncensored, open-source alternative to Higgsfield AI, Freepik, Krea, Openart AI', 200+ models, MIT licensed.
- 1:01: README: Try it Online (dev.muapi.ai/open-generative-ai), Download Desktop App tablosu (macOS, Windows, Linux), Discord bağlantısı.
- 1:38: Claude Code v2.1.119, Opus 4.7 (1M context) · Claude Max, VS Code terminali.
- 4:44: Commit 'feat: make fal.ai the default landing experience' ve Vercel deploy komutları.
- 5:22: Hata: Vercel commit author'ı tanımıyor; commit yazarı burhan-3576 e-postasıyla değiştirilip yeniden deploy ediliyor.
- 6:12: Prototipal sayfası: All-time revenue $99,320, MRR tahmini $6,623, kuruluş March 2025, Stripe ile doğrulanmış.
- 6:40: Terminal: canlı URL goat-ugc-ai.vercel.app, provider fal.ai, model flux-schnell, repo goatstarter/goat-ugc-ai (private).
- 6:52: Landing: Deploy to Vercel in 2 minutes (FAL_KEY), Run on your own GPU (AI_PROVIDER=local, Ollama, ComfyUI, sd.cpp).
- 9:14: Video builder: topic alanı, tone, duration, motion clip (fal.ai kling) onay kutusu, sahne sayısı 0/6.
- 10:36: Terminal özeti: Nano Banana 2 + Pro, text-to-video modu, Seedance 2.0 endpoint, 5 dakikalık video, sahne editörü.
- 11:50: LTX-2 GitHub: Official Python inference and LoRA trainer; git clone ve uv sync --frozen.
- 14:08: Üretilen video karelerinde altyazı: 'Simplify Your Billing Process', 'User-Friendly Design', 'Real-Time Payment Tracking'.
## Belirsizlikler
- Video 'Kling V3' ve 'Cdream/Seedream 2' diyor; ekranda Kling v2.1 ve Kling v1 görünüyor, hangisinin gerçekte kullanıldığı net değil.
- Konuşmadaki 'Hixfield' Higgsfield olarak yorumlandı (otomatik altyazı bulanık).
- Muapi.ai kaldırılması istendi; arayüzde hâlâ 'enable Muapi' ibaresi görünüyor.
- Altyazı 'Cdream 2' ile ekran 'seedream 2' tutarsız; Seedance 2.0 ile karışmış olabilir.
- Kare listesinde 'Descript', 'Linear', 'Tripo', 'Excalidraw' gibi adlar yalnız OCR'da/terminal kalıntısında geçiyor, videoda kullanılmıyor.
- API anahtarı değerleri görünmüyor; yalnızca FAL_KEY/ANTHROPIC_API_KEY adları geçiyor.
- Yorumlardaki Codex, Antigravity, Cursor, Gemini, ChatGPT, Obsidian yalnız izleyici yorumunda anılıyor.
## Atlanan segment oranı
0/20 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://github.com/Anil-matcha/Open-Generative-AI | 0:11 | ekran | evet |
| dev.muapi.ai/open-generative-ai | 0:10 | ekran | hayır |
| github.com/Anil-matcha/Open-Generative-AI/releases | 1:01 | ekran | hayır |
| https://github.com/Anil-matcha/Open-Generative-AI.git | 1:44 | ekran | evet |
| http://localhost:3000 | 1:22 | ekran | hayır |
| http://localhost:3333 | 1:22 | ekran | hayır |
| https://linear.app | 1:22 | ekran | hayır |
| skool.com/live/BPKyklgfzsw | 4:08 | ekran | hayır |
| https://github.com/goatstarter/goat-ugc-ai.git | 4:50 | ekran | hayır |
| https://vercel-status.com/api/v2/status.json | 5:00 | ekran | hayır |
| https://goat-ugc-ai.vercel.app/ | 6:28 | ekran | hayır |
| https://goat-ugc-ai.vercel.app/api/generate/image | 6:40 | ekran | hayır |
| https://github.com/goatstarter/goat-ugc-ai | 6:40 | ekran | hayır |
| goat-ugc-ai.vercel.app/video | 9:14 | ekran | hayır |
| https://goat-ugc-ai.vercel.app/api/video/plan | 9:38 | ekran | hayır |
| https://goat-ugc-ai.vercel.app/api/generate/video | 10:36 | ekran | hayır |
| Itx.io/model/ltx-2 | 11:46 | ekran | evet |
| https://github.com/Lightricks/LTx-2.git | 11:50 | ekran | evet |
| https://v3b.fal.media/files/b/0a978bd9/kvBDvsz-rwg7kfsfhtob.Jpg | 6:42 | ekran | hayır |
| https://benburhan.gumroad.com/l/bsrxgi | açıklama | açıklama | hayır |
| https://youtu.be/oGI1YmC2L00 | açıklama | açıklama | hayır |
| https://youtu.be/nXvWTR88sfU | açıklama | açıklama | hayır |
| https://youtu.be/qm0ZlYezt1Q | açıklama | açıklama | hayır |
| https://github.com/anil-matcha/open-generative-ai | açıklama | yorum | evet |
| skool.com/doa/about | açıklama | açıklama | hayır |
| skool.com/doa-zero/about | açıklama | açıklama | hayır |
| https://fal.ai/docs/documentation | açıklama | açıklama | evet |
| https://muapi.ai/docs/introduction | açıklama | açıklama | evet |
| https://github.com/burhankocabiyik/videomaker#local-models | açıklama | açıklama | hayır |
| https://github.com/Anil-matcha/0pen-Generative-AI.git | 1:40 | ekran | evet |
| https://anthropic.com | 1:22 | ekran | hayır |
| http://localhost:3300 | 1:22 | ekran | hayır |
| https://arspar.com | 1:38 | ekran | hayır |
| https://goat-ugc-gi51h1ng-burhan-3576s-projects.vercel.app | 4:44 | ekran | evet |
| https://fal.ai | 4:46 | ekran | evet |
| https://users.noreply.github.com | 4:50 | ekran | hayır |
| https://muapi.ai | 5:52 | ekran | evet |
| https://ltx.io/model/ltx-2 | 11:46 | ekran | evet |
| https://fal.ai/docs/documentation/compute | açıklama | açıklama | evet |
| https://fal.ai/docs/documentation/serverless | açıklama | açıklama | evet |
| https://vercel.com | açıklama | açıklama | evet |
## İş akışı
- 1. adım — Open-Generative-AI reposu incelenip proje temeli olarak seçildi — araçlar: Open-Generative-AI, GitHub
- 2. adım — VS Code'da yeni pencere ve goat-ugc-ai klasörü açıldı — araçlar: VS Code
- 3. adım — Terminalde Claude Code başlatılıp kurulum promptu yazıldı — araçlar: Claude Code, Claude Opus 4.7
- 4. adım — Repo klonlama, araç kontrolü ve GitHub'a private repo yükleme otonom modda yürütüldü — araçlar: Claude Code, Git, GitHub CLI
- 5. adım — Uygulama Vercel'e deploy edildi, fal.ai varsayılan sağlayıcı yapıldı — araçlar: Vercel CLI, Vercel, fal.ai
- 6. adım — Commit yazar hatası bulunup düzeltildi, yeniden deploy edildi — araçlar: Git, Vercel CLI
- 7. adım — Canlı API ve landing/dashboard/create sayfaları test edildi — araçlar: fal.ai, Flux Schnell, Next.js
- 8. adım — Prototipal geliri gösterilip fiyatlandırma stratejisi (abonelik + kredi) anlatıldı — araçlar: Prototipal
- 9. adım — İkinci prompt: Muapi kaldırılıp Remotion pipeline ve goat-youtube eklendi — araçlar: Claude Code, Remotion, goat-youtube
- 10. adım — Video builder açılıp sahne planı ve görselleri üretildi — araçlar: fal.ai, GPT-4o mini, Flux Schnell, Remotion
- 11. adım — Videolu üretim için üçüncü prompt verilip Seedance 2.0, Nano Banana 2 ve sahne editörü eklendi — araçlar: Claude Code, Seedance 2.0, Nano Banana 2, fal.ai
- 12. adım — B2B faturalama teaser'ı ile canlı test yapıldı — araçlar: Seedance 2.0, Nano Banana 2, Remotion
- 13. adım — LTX-2 ile lokal ücretsiz video üretme seçeneği gösterildi — araçlar: LTX-2, uv
- 14. adım — Text-to-video modu ile sahneler render edilip birleştirilen video izlendi — araçlar: Seedance 2.0, Remotion, fal.ai
## Promptlar
- Açık kaynak repodan SaaS içerik üretim uygulaması kurmak — GitHub reposunu klonla, SaaS ve ajanslar için içerik üreten bir uygulamaya çevir; fal.ai kullan, private repo olarak GitHub'a yükle ve Vercel'e deploy et; yerelde de çalışabilsin, açık kaynak ve bulut sürümü olsun.
- Claude Code'u otomatik modda uzun işe bırakmak — Otonom modda çalış, her şeyi bitir, sonunda tek seferde onaylayacağım.
- Remotion tabanlı sahne planlayıcılı video pipeline'ı kurmak — Ürün videoları üretecek sistemi kur, Remotion kullanabilirsin; Muapi API'yi ve sayfasını kaldır, yalnız fal.ai kullan; konuyu ben vereyim, sahne ve promptları sen yaz; goat-youtube projesini GitHub'dan çekip işe yarayanı al.
- Görsel slayt yerine yapay zekâ video klipleri üretmek — Görsel değil videolar eklensin; görselleri ve videoları yapay zekayla üret; görsel modeli Seedream 2 ya da video için Kling v3, fal.ai üzerinden.
ikinci göz KAPALI: --ikinci-goz yok
