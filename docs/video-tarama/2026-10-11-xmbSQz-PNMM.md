# AIE CODE Day 2: ft Google Deepmind, Anthropic, Cursor, Netflix, Cline, OpenAI, Meta, and METR
## Künye
AIE CODE Day 2: ft Google Deepmind, Anthropic, Cursor, Netflix, Cline, OpenAI, Meta, and METR · AI Engineer · süre: 8:57:05 · en-orig · https://youtu.be/xmbSQz-PNMM · şema 2
motor: parti yeniden-3-uzun · claude-sonnet-5-5 · hafif claude -p
kareler: yok
kareler: girdi ≤40000 jeton için 60→0
tek kol: claude-sonnet-5-5 error_max_budget_usd:  · claude-haiku-5-5: claude-haiku-5-5 · 222660 tk
## Özet
AI Engineer Code Summit 2025 Day 2 kaydı (8:57:05). Swix'in 'slop' karşıtı açılışından, Anthropic'in 'agent yerine skill' sunumuna, Dex Horthy'nin context engineering / RPI iş akışından, Cursor Composer ve RL altyapısına, OpenAI Agent RFT'ye, Kitze'nin vibe engineering konuşmasına kadar uzanan tam gün. Öne çıkan canlı demolar: Poolside'un Ada'dan Rust'a kod dönüşümü, Google AI Studio ile Gemini 3 Pro / Nano Banana Pro uygulamaları ve Google Antigravity tanıtımı. Ayrıca Amp (Sourcegraph) alt ajan mimarisi, Gimlet Labs'ın AI ile kernel üretimi, Netflix'in 'Simple vs Easy' ve sonsuz yazılım krizi anlatımı, Prime Intellect'in environment yaklaşımı, Cline'ın ClineBench önerisi ve METR'ın geliştirici RCT sonucu (AI kullanımında %19 yavaşlama) yer alıyor. Konuşmalar ağırlıklı olarak İngilizce; ASR isimleri ve terimleri bozuyor (Cloud Code = Claude Code, Codeex = Codex, Klein = Cline).
## Bölümler
- 0:00 Pre-show
- 10:36 Welcome to AI Engineer Code Summit — Jed Borovik
- 14:32 Opening Remarks — swyx
- 23:41 Stop Building Agents — Barry Zhang & Mahesh Murag
- 39:54 No Vibes Allowed: Solving Hard Problems in Complex Codebases — Dex Horthy
- 1:00:08 Building a Fast Frontier Model with RL — Lee Robinson
- 1:15:37 From Code Snippets to Codebases: What's Next for Coding Evals — Naman Jain
- 1:33:36 Coffee Break
- 2:07:04 Code World Model: Building World Models for Computation — Jacob Kahn
- 2:23:38 Efficient Reinforcement Learning — Rhythm Garg & Linden Li
- 2:43:46 RL Environments at Scale — Will Brown
- 3:02:15 Agent Reinforcement Fine Tuning — Will Hang & Cathy Zhou
- 3:18:58 From Vibe Coding to Vibe Engineering — Kitze
- 3:44:21 Lunch Break
- 4:53:23 Proactive Agents — Kath Korevec
- 5:11:19 Making Codebases Agent-Ready — Eno Reyes
- 5:26:38 Amp Code: Next-Generation AI Coding — Beyang Liu
- 5:45:03 Using AI-Generated Kernels to Speed Up PyTorch — Natalie Serrino
- 6:04:23 The Infinite Software Crisis — Jake Nations
- 6:23:26 Break
- 7:07:13 AGI: The Path Forward — Eiso Kant & Jason Warner
- 7:23:06 Continual System-Prompt Learning for Code Agents — Aparna Dhinakaran
- 7:34:05 Hard-Won Lessons from Building Effective AI Coding Agents — Nik Pash
- 7:48:17 Benchmarks vs. Economics: The AI Capability Measurement Gap — Joel Becker
- 8:09:26 Defying Gravity — Kevin Hou
- 8:34:29 Closing Remarks
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Code | yok | CLI | yok | Anthropic'in terminal kodlama ajanı; Barry Zhang sunumunda ilk kodlama ajanları olarak anılıyor (ASR: Cloud code). | 23:41 | Cloud code, our first coding agent, launched to the world. |
| Agent Skills | yok | skill | yok | Klasör tabanlı, SKILL.md ve script içeren prosedürel bilgi paketleri; agent ihtiyaç anında okur. | 23:41 | We created agent skills. |
| Claude Agent SDK | yok | teknik | yok | Anthropic'in üretime hazır agent altyapısını sunan SDK; konuşmada hazır agent olarak anılıyor. | 23:41 | our cloud agent SDK now provides a production ready agent |
| MCP | yok | MCP | yok | Model Context Protocol; agent ile dış araç ve veri arasında bağlantı standardı. Skills ile birlikte kullanım anlatılıyor. | 23:41 | MCP became the standard for agent connectivity. |
| Codex | yok | CLI | yok | OpenAI'ın kodlama ajanı (GPT-5.1 Codex); plan yazımında kullanıldığı anlatılıyor. Ekranda npm ile global kurulum komutu görünüyor. | 1:13:23 | GPT 5.1 Codeex is really great for plans |
| Cursor | yok | teknik | yok | AI kod editörü; Composer modelini eğiten ve kullanan ürün ekibi. | 1:00:08 | head of developer experience at Cursor |
| Cursor Composer | yok | teknik | yok | Cursor'un kodlama için RL ile eğittiği ilk ajan modeli; hızlı ve akıllı olmayı hedefler. | 1:00:08 | our first agent model |
| Cursor semantik arama | yok | teknik | yok | Cursor'un kendi eğittiği embedding modeliyle kod tabanında doğal dil ile dosya arama aracı. | 1:10:19 | trained our own embedding model that allows you to do semantic search · kanıt: yok |
| Cursor Cloud Agents | yok | teknik | yok | Cursor ajanlarını bulutta VM üzerinde çalıştıran ürün; RL eğitim ortamıyla aynı altyapıyı paylaşır. | 1:08:18 | this is how you can run a cursor agent kind of offline · kanıt: yok |
| Claude Sonnet 4.5 | yok | teknik | yok | Anthropic modeli; Cursor Composer karşılaştırmasında referans alınıyor. | 1:00:08 | slightly below the latest Frontier with Sonnet 45 |
| Gemini 3 Pro | yok | teknik | yok | Google DeepMind'ın en yeni modeli; Google AI Studio ve Antigravity demolarında kullanıldı. | 4:54:23 | Gemini 3 Pro. this is our latest most intelligent state-of-the-art model |
| Nano Banana Pro | yok | teknik | yok | Google'ın görsel model (Gemini Image) ürünü; metin render, tutarlılık ve Search grounding ile demolarda kullanıldı. | 4:55:26 | Nano Banana Pro, which came out yesterday |
| Google AI Studio | yok | teknik | yok | Google'ın Gemini modellerini deneme ve 'build' ile prompt'tan uygulama üretme ortamı; demoda kullanıldı. | 4:58:29 | this is Google AI Studio. It's our home |
| Gemini API | yok | teknik | yok | AI Studio'da uygulamalara entegre edilen Gemini API; grounding ve Live API özellikleri anlatıldı. | 4:58:29 | how easy it is to integrate the Gemini API into your application |
| Google Antigravity | yok | teknik | yok | Google DeepMind'ın agent-first IDE'si; Agent Manager, editör ve agent kontrollü Chrome tarayıcısından oluşur. | 8:10:26 | Google Anti-gravity is a brand new IDE out of Google DeepMind |
| Gemini computer use | yok | teknik | yok | Gemini'nin tarayıcıyı tıklayarak, kaydırarak ve JavaScript çalıştırarak kullanabildiği bilgisayar kullanımı varyantı; Antigravity tarayıcı ajanında kullanılıyor. | 8:19:36 | Gemini computer use variant |
| Terminus | yok | teknik | yok | Terminal-Bench için sade, genel amaçlı bir agent harness; Gemini 3.0 ile sıralamada üst sıralara çıktığı gösteriliyor. | 7:35:07 | Gemini 3.0 on Terminus scored better |
| Terminal-Bench | yok | teknik | yok | Terminal içinde ajan görevlerini ölçen benchmark; liderlik tablosu Nik Pash'in konuşmasında anılıyor. | 7:35:07 | dominated terminal bench leaderboards |
| SWE-bench | yok | teknik | yok | GitHub issue'larını çözme benchmark'ı; Arize deneyinde kıyaslama ölçütü olarak kullanılıyor. | 7:28:09 | benchmark both client and cloud code on Swebench |
| LiveCodeBench | yok | teknik | yok | Yarışma tarzı kodlama problemleri ile zaman bazlı (dinamik) değerlendirme benchmark'ı; Naman Jain'in sunumunda tanıtılıyor. ASR: life codebench. | 1:16:37 | this is life codebench which is like valation work |
| Copilot Arena | yok | teknik | yok | LMArena ile geliştirilen, IDE içi kod tamamlama asistanlarını kabul oranına göre çift yönlü karşılaştıran deneyim. | 1:30:46 | first is copilot arena |
| LMArena | yok | teknik | yok | Model karşılaştırma platformu; Copilot Arena ve Repo Chat değerlendirmelerinde iş birliği yapılan platform. | 1:30:46 | Ekran: imarena.ai (LM arena folks iş birliği, altyazıda da geçiyor) (karede: kanıttan) Ekran: imarena.ai (LM arena folks iş birliği, altyazıda da geçiyor) |
| Kernel Bench | yok | teknik | yok | GPU kernel üretimini ölçen benchmark; v0.1 üzerinde Metal (M4) sonuçları paylaşılıyor. | 5:52:12 | on the kernel bench benchmark the v0.1 version |
| Code World Model (CWM) | yok | teknik | yok | Meta FAIR'in 32B parametreli, çalıştırma izlerini (execution trace) öğrenen kod modeli; açık model olarak yayınlandı. | 2:07:04 | the code world model which I'll abbreviate as CWM · kanıt: yok |
| Verifiers | yok | teknik | yok | Prime Intellect'in RL ortamları (environment) oluşturma kütüphanesi; araçlar, sandbox ve rubric bileşenleri içerir. | 2:52:58 | it just released a library called verifiers |
| Environments Hub | yok | teknik | yok | Prime Intellect'in RL ortamlarını oluşturup paylaştığı açık topluluk platformu (paket kayıt defteri gibi). | 2:51:56 | the environments hub, which is a open source community platform |
| Prime-RL | yok | teknik | yok | Prime Intellect'in büyük ölçekli asenkron RL eğitim yığını; config dosyasıyla çalışır. | 2:56:01 | our Prime RL trainer |
| Intellect 3 | yok | teknik | yok | Prime Intellect'in 500 GPU üzerinde eğittiği 100B+ parametreli model (SFT ve RL). | 2:58:03 | we've been training a large model which will be out into the world quite soon called Intellect 3 |
| Qwen3 4B | yok | teknik | yok | Wiki search ortamında RL ile eğitilen küçük açık model; doğruluk %55'ten %89'a çıkarılmış. | 2:57:02 | we started with a Quen 3 4B model |
| Agent RFT | yok | teknik | yok | OpenAI'ın, ajanın araç çağrılarını ve uç nokta tabanlı ödül fonksiyonunu kullanarak model ağırlıklarını eğiten reinforcement fine-tuning ürünü. | 3:02:15 | Agent reinforcement fine-tuning or agent RF is the way to do this |
| Amp | yok | CLI | yok | Sourcegraph/Amp Code'un terminal ve editör (VS Code uzantısı) üzerinden çalışan kodlama ajanı; smart ve rush ajan modları, alt ajanlar (Finder, Oracle, Librarian, Kraken) anlatılıyor. | 5:27:39 | it's a coding agent that you can invoke from the terminal |
| Amp Oracle | yok | teknik | yok | Amp'in zor hata ayıklama ve planlama için çağrılan muhakeme (reasoning) alt ajanı. | 5:34:50 | Oracle sub agent · kanıt: yok |
| Poolside Malibu | yok | teknik | yok | Poolside'un sıfırdan eğittiği ikinci nesil kodlama ajanı modeli; canlı demoda Ada'dan Rust'a dönüşüm yaptı. | 7:16:25 | Malibu agent is a second generation · kanıt: yok |
| Visual Studio Code | yok | teknik | yok | Poolside asistanının çalıştığı editör; demo VS Code içinde yapıldı. | 7:08:15 | our assistant in Visual Studio Code backed by poolside agent |
| Ada | yok | teknik | yok | Poolside demosunda kod tabanının dili (savunma/kritik altyapı); Rust'a dönüştürüldü. | 7:08:15 | a very modern programming language that the government uses |
| Rust | yok | teknik | yok | Poolside demosunda hedef dil; ayrıca Dex Horthy'nin BAML ve Parquet denemelerinde geçen dil. | 7:09:16 | convert this database to Rust |
| rustyline | yok | teknik | yok | Rust için satır düzenleme kütüphanesi; ajan yukarı ok ile komut geçmişi için bunu ekledi. | 7:14:22 | Ekran kodu: use rustline::DefaultEditor; (ASR: rustyline) (karede: kanıttan) Ekran kodu: use rustline::DefaultEditor; (ASR: rustyline) |
| Cargo | yok | teknik | yok | Rust derleme ve paket yöneticisi; demoda Compiling çıktıları görünüyor. | 7:14:16 | Ekran: Compiling bitflags v1.3.2 / libc v0.2.177 vb. (karede: kanıttan) Ekran: Compiling bitflags v1.3.2 / libc v0.2.177 vb. |
| Cline | yok | CLI | https://github.com/cline/cline | Açık kaynak kodlama ajanı (VS Code uzantısı ve CLI cline-cli); konuşmacı Nik Pash, Cline'ın yaratıcısı ve AI başkanı. ASR: Klein. | 7:34:05 | I'm the head of AI at Klein |
| ClineBench | yok | teknik | yok | Cline'ın gerçek dünya kodlama görevlerinden RL ortamı üreterek duyurduğu açık benchmark. ASR: ClientBench; ekranda cline-bench komutu görünüyor. | 7:46:20 | today we're announcing ClientBench |
| kforge | yok | CLI | yok | Gimlet Labs'ın PyTorch iş yükünden hedef donanım (H100) için optimize kernel üreten CLI aracı. | 5:50:12 | Ekran: demo@demo-host kforge_demo % kforge generate gemm_activation_model.py --target-hw h100_pcie (karede: kanıttan) Ekran: demo@demo-host kforge_demo % kforge generate gemm_activation_model.py --target-hw h100_pcie |
| Prompt Learning | yok | teknik | yok | Arize'ın, RL ağırlık güncellemesi yerine İngilizce geri bildirimle sistem prompt'unu iyileştirme yöntemi. | 7:23:06 | apply RL techniques to prompts instead of model weights |
| GEPA | yok | teknik | yok | DSPy'ın prompt optimizasyon yöntemi; Arize deneyinde kıyas olarak kullanıldı. ASR: GEA. | 7:32:14 | it's a prompt optimizer from DSPI · kanıt: yok |
| DSPy | yok | teknik | yok | Stanford'un prompt optimizasyon çerçevesi; GEPA bu çerçevenin parçası. | 7:32:14 | If you're familiar with DSPI |
| PyTorch | yok | teknik | yok | Kernel optimizasyonunun hedef aldığı derin öğrenme kütüphanesi. | 5:45:03 | speed up custom PyTorch code |
| torch.compile | yok | teknik | yok | PyTorch derleyicisi; Gimlet deneyinde baseline olarak kullanıldı. | 5:50:08 | It's comparing to eager mode and torch compile |
| CUDA | yok | teknik | yok | NVIDIA GPU programlama platformu; kernel üretimi için hedef. | 5:48:06 | from things like CUDA and like Triton |
| Triton | yok | teknik | yok | GPU kernel yazmak için DSL; kernel üretiminde anılıyor. | 5:48:06 | from things like CUDA and like Triton |
| Metal | yok | teknik | yok | Apple GPU programlama çerçevesi; Gimlet M4 deneyinde kullanıldı. | 5:48:06 | device specific like Metal |
| Ray | yok | teknik | yok | Dağıtık hesaplama çerçevesi; Cursor RL rollout'ları için kullanılıyor. | 1:06:16 | that's where we use Ray |
| Weights & Biases | yok | teknik | yok | Eğitim koşularını izleme panosu; Prime-RL koşusunun kaydı ekranda görünüyor. | 2:56:22 | Ekran: View project at https://wandb.ai/primeintellect/wiki-search-debug · kanıt: kare (karede: Ekran: View project at https://wandb.ai/primeintellect/wiki-search-debug) |
| AGENTS.md | yok | teknik | yok | Kodlama ajanlarına proje kuralları veren açık standart dosya; Eno Reyes sunumunda anılıyor. | 5:20:29 | agents MD files an open standard |
| CLAUDE.md | yok | teknik | yok | Claude Code'un proje bağlamını okuduğu dosya; Dex Horthy repo onboarding için öneriyor. ASR: cloudmd. | 53:14 | you could use cloudmd for this |
| Research-Plan-Implement (RPI) | yok | iş akışı | yok | Dex Horthy'nin üç aşamalı iş akışı: araştırma, plan, uygulama; bağlamı küçük tutmayı hedefler. | 58:17 | people are calling this RPI · kanıt: yok |
| HumanLayer | yok | teknik | https://github.com/humanlayer/humanlayer | Dex Horthy'nin ekibinin şirketi/açık kaynak deposu; .claude/commands ve prompt sistemi paylaşılıyor. | 42:06 | Ekran: AI to work in complex codebases (github.com/humanlayer) (karede: kanıttan) Ekran: AI to work in complex codebases (github.com/humanlayer) |
| Factory Droid | yok | teknik | yok | Factory'nin kodlama ajanı; Eno Reyes'in sunumunda anılıyor. | 5:18:26 | Droid is our coding agent · kanıt: yok |
| Devin | yok | teknik | yok | Cognition'ın yazılım ajanı; Swix, AI Engineer web sitesi güncellemelerini Devin ile otomatikleştirdiğini anlatıyor; ekranda Devin oturum bağlantısı var. | 21:42 | here's an example of us using Devon to automate the sort of website |
| Browserbase | yok | teknik | yok | Tarayıcı otomasyon altyapısı; Barry Zhang Browserbase için yazılmış bir skill örneği anlatıyor. | 28:44 | Browserbase is a pretty good example of this |
| Stagehand | yok | teknik | yok | Browserbase'in açık kaynak tarayıcı otomasyon aracı; skill ile Claude'a bağlanıyor. ASR: stage hand. | 29:44 | with stage hand can now go navigate the web |
| Document Skills | yok | skill | yok | Anthropic'in office belgeleri (docx, pdf, pptx vb.) oluşturup düzenleyen skill'leri. | 28:44 | document skills that give Claude the ability to create and edit |
| Notion Skills | yok | skill | yok | Notion çalışma alanında derin araştırma ve iş akışları için Claude skill paketi. | 29:44 | notion launched a bunch of skills that help claude |
| skill-creator | yok | skill | yok | Claude'un yeni skill'ler oluşturmasını sağlayan Anthropic skill'i. | 37:54 | using our skill creator skill |
| Claude Scientific Skills | yok | skill | yok | K-Dense ekibinin 120+ bilimsel skill koleksiyonu; slaytta gösteriliyor. | 28:56 | Ekran: A comprehensive collection of 120+ ready-to-use scientific skills for Claude (karede: kanıttan) Ekran: A comprehensive collection of 120+ ready-to-use scientific skills for Claude |
| Shadcn/ui | yok | teknik | yok | React bileşen kütüphanesi; AI Studio'nun full stack özelliğinde kurulumu demo edildi. ASR: Shadci. | 5:07:43 | if you want to install Shadci · kanıt: yok |
| Three.js | yok | teknik | yok | Web 3D kütüphanesi; AI Studio ile üretilen yarış oyununda kullanıldı. ASR: 3JS. | 5:06:40 | I got this 3D racing game in 3JS |
| React | yok | teknik | yok | Kitze'nin frontend konuşmasında LLM'lerin iyi yazdığı UI kütüphanesi olarak anılıyor. | 3:23:02 | React is the best |
| Parquet Java | yok | teknik | yok | Dex Horthy'nin Hadoop bağımlılığını kaldırmaya çalıştığı Java kod tabanı. | 49:05 | we tried to remove Hadoop dependencies from Parket Java |
| BAML | yok | teknik | yok | BoundaryML'in Rust tabanlı dil/derleyici projesi; Dex Horthy 7 saatlik oturumda 35.000 satır değişiklik yaptı. | 48:04 | fix to your 300,000line Rust codebase |
| Next.js | yok | teknik | yok | Kitze'nin benji.so projesini taşıdığı React framework'ü. | 3:34:11 | moved it to next 16 with app router |
| tRPC | yok | teknik | yok | Kitze'nin proje yeniden yazımında kullandığı tip güvenli API katmanı. | 3:34:11 | better off tRPC monor repo |
| Turborepo | yok | teknik | yok | Kitze'nin monorepo yapısında kullandığı build aracı. | 3:34:11 | turbo repo react native app |
| React Native | yok | teknik | yok | Kitze'nin monorepo içindeki mobil uygulama. | 3:34:11 | react native app |
| Prisma | yok | teknik | yok | Veritabanı ORM aracı; Kitze yanlışlıkla npx prisma migrate reset çalıştırdığını anlatıyor. | 3:28:30 | Ekran: mistake. When I ran npx prisma migrate reset (karede: kanıttan) Ekran: mistake. When I ran npx prisma migrate reset |
| Docker | yok | teknik | yok | Konteyner aracı; Cline benchmark ortamları Docker ile paketleniyor. | 7:42:16 | containerize it with docker |
| uv | yok | teknik | yok | Python paket ve çalıştırma aracı; Cline benchmark görevlerinde süreç yönetimi için kullanılıyor. | 7:42:18 | Ekran: uv for clean process management (karede: kanıttan) Ekran: uv for clean process management |
| z.ai | yok | teknik | yok | Z.ai model servisi; Kitze'nin Claude'dan geçtiği alternatif olarak anılıyor. | 3:32:52 | Ekran: I switched from Claude to z.ai (using (karede: kanıttan) Ekran: I switched from Claude to z.ai (using |
| AviationStack API | yok | teknik | yok | Uçuş verisi API'si; Antigravity demosunda uçuş takip uygulaması bu API'yi kullanıyor. | 8:27:46 | Ekran: The base URL is http://api.aviationstack.com/v1/ · kanıt: kare (karede: Ekran: The base URL is http://api.aviationstack.com/v1/) |
| Poolside ile Ada veritabanı kod tabanını Rust'a dönüştürme demosu | yok | prompt | yok | Ada kod tabanını Rust'a çevir. Derleme ve test komutlarını çalıştır, çalışmadığında düzelt. | 7:09:16 | kaynak: altyazı |
| Poolside ajanına eksik bir özelliği istemek (rustyline ile geçmiş) | yok | prompt | yok | Veritabanı CLI'a yukarı ok tuşu ile komut geçmişinde gezinme özelliği ekle. | 7:13:21 | kaynak: altyazı |
| Google AI Studio'da 3D yarış oyunu üretme (Gemini 3 ile) | yok | prompt | yok | Bir yarış oyunu yap; başlangıçta bot olan bir başlangıç ekranı olsun. | 5:06:40 | kaynak: altyazı |
| Yeni bir arayüz özelliğini ideate etmek ve Antigravity'ye dışa aktarma akışı üretmek | yok | prompt | yok | Bu AI Studio ekran görüntüsünü mümkün olduğunca birebir klonla ve AI Studio'dan Antigravity'ye aktarma akışı ekle; yaratıcı ol. | 5:05:39 | kaynak: altyazı |
| Gemini 3 ile tasarım odaklı tek seferlik site üretimi | yok | prompt | yok | Bir animasyonlu, kaydırmalı kayan (slick) web sitesi üret; cyberpunk olmasın. | 5:01:33 | kaynak: altyazı |
| Nano Banana Pro ve Gemini 3 ile çok adımlı çizgi roman uygulaması | yok | prompt | yok | Bizi (Cat ve Ammaar) AI Engineer New York'ta sunum yaparken gösteren, Nano Banana Pro ile çizgi roman hikayesi üret; yüzleri kullan, tür ve dil seç, hikâye yönünü ortada değiştirebil. | 5:00:46 | kaynak: altyazı |
| Kitze'nin vibe coding parodisi (tek satırlık abartılı prompt) | yok | prompt | yok | Kodu TypeScript'e taşı ve hiç hata yapma. | 3:30:08 | kaynak: altyazı |
| Antigravity artifact yorumlarıyla ajana yön vermek | yok | prompt | yok | Yorum örneği: Tailwind kullanma, vanilla CSS kullan. (Antigravity'de görsel üzerine yorum bırakma) | 8:27:41 | kaynak: altyazı |
| Amp'in kendi kaynak kodunda küçük özellik ekleme demosu | yok | prompt | yok | Amp'e alt sol köşeye yardım butonu ekle. | 5:28:02 | kaynak: kare |
| Poolside'un yaratıcı yazım yeteneğini göstermek | yok | prompt | yok | Bu değişikliklerle ilgili bir şiir yaz. (Eğlence amaçlı) | 7:15:23 | kaynak: altyazı |
| Arize Prompt Learning yönteminin özeti (SWE-bench 150 örnek) | yok | prompt | yok | Kod tabanlarında LLM'in her seferinde mevcut sistem prompt'una kural ekleyecek meta prompt: orijinal prompt, kurallar ve LLM-judge açıklamaları birleştirilerek yeni kurallar üretilir. | 7:31:12 | kaynak: altyazı |
## Açıklama bağlantıları
- yok
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Shader animasyonu (WebGL shader animation) | Gemini 3 ile üretilen animasyonlu web sitesinde sayfalar arası akan shader arka planı. | 5:01:33 | altyazı |
| Sayfa geçiş animasyonları (page transition animations) | Üretilen sitenin sayfaları arasında çeşitli geçiş efektleri gösteriliyor. | 5:01:33 | altyazı |
| Tipografi ve yerleşim (typography and layout) | Gemini 3 tarafından seçilen tipografi ile tasarlanmış sitenin tasarım sistemi; mor gradyan yerine daha az klişe görünüm hedefleniyor. | 5:01:33 | altyazı |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| npm i -g @openai/codex | Codex CLI'yı npm ile global olarak kurar. (karede: (karede OCR) 0 00 0299992020 002222202999922 100011 0002290 11011011111111 TP00000000000T AIE/CODE 0000000000000000000001 0000000111111100000000 10000001 111000001 11000001 10000 110011 1000 1111 111 101 11 11 111) | 2:49:16 | kare |
| uv run prime-rl @ configs/prime-rl/wiki-search.toml | Prime-RL eğitimini wiki-search config dosyasıyla başlatır. (karede: (karede OCR) 0 00 0299992020 002222202999922 100011 0002290 11011011111111 TP00000000000T AIE/CODE 0000000000000000000001 0000000111111100000000 10000001 111000001 11000001 10000 110011 1000 1111 111 101 11 11 111) | 2:56:22 | kare |
| kforge generate gemm_activation_model.py --target-hw h100_pcie | PyTorch modelinden H100 hedefli GPU kernel'ları üretir. (karede: (karede OCR) AIE/CODE 00 0299992020 002222202999922 100011: 0002290 11011011111111 10121111111111 111 1P0000000000000000T 0000000000000000000001 0000000111111100000000 111000001. 10000001 10000 11000001 110011 100) | 5:50:12 | kare |
| pnpm exec tsc -b && NODE_ENV=development bun run scripts/build.ts | Amp VS Code uzantısının TypeScript derlemesini ve build'ini çalıştırır. (karede: (karede OCR) AIE/CODE 00 0299992020 002222202999922 100011 0002290 11011011111111 10131111111111 211 0000000000000000000001 0003000111111100000080 10000001 111000001 10000 11000001 110011 1000 1111 STARTS IN 111 1) | 5:28:28 | kare |
| git branch -a / grep -i press | Git dal listesinde press geçen dalları filtreler. (karede: (karede OCR) AIE/CODE 00 0299992020 002222202999922 100011: 0002290 11011011111111 10121111111111 111 1P0000000000000000T 0000000000000000000001 0000000111111100000000 111000001. 10000001 10000 11000001 110011 100) | 5:40:32 | kare |
| vitest run --run src/review/structured-review.test.ts | Yapılandırılmış review test dosyasını Vitest ile çalıştırır. (karede: (karede OCR) AIE/CODE 00 0299992020 002222202999922 100011: 0002290 11011011111111 10121111111111 111 1P0000000000000000T 0000000000000000000001 0000000111111100000000 111000001. 10000001 10000 11000001 110011 100) | 5:41:08 | kare |
| pnpm -C vscode test --run src/review/structured-review.test.ts | Aynı review testini VS Code paketinde çalıştırır. (karede: (karede OCR) AIE/CODE 00 0299992020 002222202999922 100011: 0002290 11011011111111 10121111111111 111 1P0000000000000000T 0000000000000000000001 0000000111111100000000 111000001. 10000001 10000 11000001 110011 100) | 5:41:08 | kare |
| chmod +x test_database.sh | Veritabanı test betiğini çalıştırılabilir yapar. (karede: (karede OCR) 2018 October November Dec MNLI/NER SQuAD mbe Mask LM NSP Mask LM Start/End Span TM T,' TM C [SEP] N [SEP] .. ... BERT BERT ECLSI EM E,' E(CLS) E,' E, E, ... .. .. . Tok 1 Tok 1 Tok 1 Tok 1 [CLS] TokM) | 7:11:12 | kare |
| chmod +x test_history.sh | Komut geçmişi test betiğini çalıştırılabilir yapar. (karede: (karede OCR) 2019 T5:"Text-to-Text October Transfer "cola sentence November jumping well." unifies all NLP Transformer" tasks December "stsb sentence1: The rhino grazed "3.8" . sentence2: A rhino is on the grass.) | 7:14:46 | kare |
| chmod +x final_demo.sh | Final demo betiğini çalıştırılabilir yapar. (karede: (karede OCR) 2019 T5:"Text-to-Text October Transfer "cola sentence November jumping well." unifies all NLP Transformer" tasks December "stsb sentence1: The rhino grazed "3.8" . sentence2: A rhino is on the grass.) | 7:14:52 | kare |
| uv run tb run --agent cline-cli --task-id 01k7c9703dknej | Terminal-Bench görevini Cline CLI ajanı ile tek bir task-id için çalıştırır. (karede: (karede OCR) We are observing a once in a generation "shift right" of applied Al, fueled by the emergent capabilities and open source/APl availability of Foundation Models. A wide range of Al tasks that used to ta) | 7:43:46 | kare |
| npx prisma migrate reset | Prisma veritabanını sıfırlar; Kitze yanlışlıkla çalıştırdığını anlatıyor. (karede: (karede OCR) AIE/CODE 00 0299992020 002222202999922 100011 0002290 11013011111111 10121111111171 311 1002000000000000000001 1000000000000000000000 0003000111111100000080 111000001 10000001 10000 11000001 1000 1100) | 3:28:30 | kare |
| curl "http://api.aviationstack.com/v1/flights?..." | Antigravity demosunda uçuş verisini AviationStack API'sinden çeker (anahtar parametreleri gizlendi). (karede: (karede OCR) 2024 November Anthropic Standardizes AI Data Desember 025 2 Agentic Era Integrations to Fuel lanuarv Announcements Introducing the Context Model Protocol 2024 Nov 25, read 3 min .) | 8:27:46 | kare |
| npm run dev | Uçuş takip uygulamasının yerel geliştirme sunucusunu başlatır. (karede: (karede OCR) 2024 November Anthropic Standardizes AI Data Desember 025 2 Agentic Era Integrations to Fuel lanuarv Announcements Introducing the Context Model Protocol 2024 Nov 25, read 3 min .) | 8:28:56 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Cursor Composer, benzer seviyedeki modellere göre token üretiminde yaklaşık dört kat daha verimli. | 1:01:09 | karşılaştırma |
| Cursor'da semantik arama, neredeyse tüm modellerin performansını artırdı; Composer'da en çok fayda sağladı. | 1:10:19 | karşılaştırma |
| Modeller, yaklaşık 3 milyon yapılandırılmış hata çıktısından kaynaklanan reward hacking girişimi yapıyor; sorunlu girişim yaklaşık %30 problemde görüldü (konuşmacı yaklaşık değer veriyor). | 1:27:49 | sayısal |
| Agent RFT ile yaklaşık 10 örnekle bile başarı elde edilebiliyor. | 3:05:19 | sayısal |
| Cognition, 100 örnekten 1000 örneğe çıkınca iyileşme 5 puandan 10 puana çıktı. | 3:10:25 | sayısal |
| Kodo'nun derin araştırma ajanında RFT ile doğruluk %6 arttı ve araç çağrısı sayısı azaldı. | 3:11:26 | sayısal |
| Macco, GPT-5 tabanlı kernel ajanında en iyi-of-3 seçimiyle state-of-the-art'ı %72 geçti. | 3:16:34 | sayısal |
| Gimlet, tek başına standalone ajanla KernelBench (v0.1, M4) üzerinde ortalama yaklaşık %25 hızlanma sağladı; karmaşık problemlerde performans düşüyor. | 5:52:12 | sayısal |
| Gimlet'in %71.000 hızlanma iddiası aslında ajanın işlemi atlamasından kaynaklanıyordu; bu sonuç analizden çıkarıldı. | 5:57:18 | özellik |
| Prompt Learning ile Claude Code'un SWE-bench sonucu yaklaşık %5, Cline'ın yaklaşık %15 arttı (150 örnek). | 7:32:14 | sayısal |
| Terminus, genel amaçlı ve sade bir harness olmasına rağmen Gemini 3.0 ile Terminal-Bench sıralamasında çok sayıda modelden üstün. | 7:35:07 | karşılaştırma |
| Benchmark'lar model ağırlıklarını gerçekten iyileştirir; ajan tarafındaki zekice mühendislik bunu yapmaz. | 7:36:09 | öneri |
| METR RCT'de yetkin geliştiriciler AI kullandığında yaklaşık %19 daha yavaş çalıştı; geliştiriciler ise %20 hızlanma bekliyordu. | 8:01:31 | sayısal |
| Ajan zaman ufku (time horizon) yaklaşık altı-yedi ayda bir ikiye katlanıyor; eğri düzgün bir üstel gidiyor. | 7:55:25 | sayısal |
| Poolside, yaklaşık 40.000 GB300 GPU'nun devreye girmesiyle ölçeklenme yapacağını ve ikinci nesil modeli kamuya açmayı planlıyor. | 7:17:26 | sayısal |
| Eno Reyes'e göre doğrulama kriterleri olan organizasyonlar ajan verimliliğinde 5-7 kat kazanç görebilir. | 5:25:32 | öneri |
| Amp, terminal içinde küçük reklam ağı ile rush ajanının inference maliyetini sponsorlayabiliyor. | 5:41:58 | özellik |
| Gemini 3, Claude ve diğer modellerin hâlâ kaçırdığı kutuları (akıllı, hızlı) birlikte karşılıyor. | 5:37:44 | karşılaştırma |
| Google Antigravity, Gemini 3 ile aynı hafta yayınlandı; ajan yöneticisi (Agent Manager) ana arayüz olarak konumlanıyor. | 8:10:26 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 3:19:58 | Kitze'nin kendi geliştirici tarayıcısı Sizzy'yi anlatması | aday değil: sponsor/reklam | Sizzy: browser specifically made for developers |
| ekran 3:19:30 | Kitze'nin kendi ürünleri: benji.so, sizzy.co, zerotoshipped.com, glink.so | aday değil: sponsor/reklam | always cooking benji.so - fix your life fr sizzy.co |
| konuşma 5:27:39 | Ghostty terminali; Amp'in TUI ekibinin katkıda bulunduğu proje | aday değil: konu dışı | one of the core contributors to Ghosty the open source terminal |
| konuşma 5:28:40 | Emacs, Neovim, JetBrains editörleri ile Amp entegrasyonu | aday değil: genel kavram | Emacs, Neovim, Jet Brains |
| konuşma 5:01:33 | Figma'nın tasarım aracı olarak anılması | aday değil: konu dışı | way around Figma |
| konuşma 17:37 | OpenAI Sora ve video üretimi örneği | aday değil: konu dışı | when I do Sora videos |
| konuşma 3:39:15 | ChatGPT'nin yavaşlığı benzetmesi | aday değil: genel kavram | if you call Chad GPT or whatever slow |
| konuşma 8:27:41 | Google Docs yorum deseni benzetmesi | aday değil: genel kavram | I love Google Docs |
| konuşma 41:55 | Hacker News'te viral olması | aday değil: konu dışı | went super viral on Hacker News |
| ekran 3:22:36 | Redux dokümantasyonu (Kitze espri slaytı) | aday değil: konu dışı | redux.js.org |
| ekran 3:35:34 | WebStorm ve Supermaven eklentisi (Kitze'nin kurulumu) | aday değil: konu dışı | WebStorm with Supermaven plugin |
| konuşma 3:34:11 | Electron ve MobX (Sizzy yığını) | aday değil: konu dışı | electron mobex mob state |
| konuşma 3:23:02 | Tailwind (taşıma örneği) | aday değil: genel kavram | go into Tailwind and just move it by three pixels |
| konuşma 3:27:26 | Git workspaces (git worktree) fikri | aday değil: genel kavram | Use git workspaces |
| konuşma 16:38 | Oxford English Dictionary 'slop' kelime seçimi | aday değil: konu dışı | corp.oup.com word-of-the-year |
| konuşma 19:40 | AI News bülteni (swyx'in kişisel projesi) | aday değil: sponsor/reklam | I'm proud to run as a side project AI news |
| konuşma 11:36 | Jules coding agent (Jed'in çalıştığı proje) | aday değil: konu dışı | I also work on the Jules coding agent |
| konuşma 2:25:41 | GPT-OSS ve Llama modelleri örnek olarak | aday değil: konu dışı | one of the GPToss models or one of the llama models |
| konuşma 7:18:00 | Qwen, Kimi, MiniMax modellerinin açık kaynak örneği | aday değil: konu dışı | Quens and Fies and Miniaxes of the world |
| konuşma 8:52:12 | Cerebras afterparty sponsoru | aday değil: sponsor/reklam | Afterparty brought to you by Cerebras |
| konuşma 8:49:39 | BCV, Mackenzie, Warp, Exa, Modal, Metronome sponsorları | aday değil: sponsor/reklam | Warp, Exa, Modal, and Metronome |
| konuşma 10:40 | WorkOS Enterprise MCP sunumu tanıtımı | aday değil: sponsor/reklam | Enterprise grade MCP |
| konuşma 1:03:13 (Kitze) | Roboflow ekranda görünüyor; kullanım belirsiz | aday değil: konu dışı | roboflow.com ekran |
| konuşma 8:20:00 (Kevin) | Google Chrome: Antigravity agent kontrollü tarayıcı | Google Antigravity | agent controlled Chrome browser |
| konuşma 4:58:29 | Google Search grounding ile AI Studio uygulamaları | Google AI Studio | Google Search grounding |
| konuşma 2:12:05 (Kahn) | GitHub Archive ve git clone verisi ile eğitim verisi | aday değil: genel kavram | GH Archive |
| ekran 5:09:28 | Google Docs (paylaşım ekranı) | aday değil: konu dışı | docs.google.com |
| konuşma 7:33:38 | Arize CPO Aparna Dhinakaran'ın kişisel LinkedIn profili | aday değil: konu dışı | linkedin.com/in/aparnadhinakaran |
| konuşma 1:03:16 | Git: git show ve git branch komutları | aday değil: genel kavram | git show HEAD |
| konuşma 1:30:46 (ekran) | Copilot Arena'nın FastChat deposu ekranda görünüyor | Copilot Arena | github.com/lm-sys/FastChat |
## Kareden okunanlar
- yok
## Belirsizlikler
- Kare görseli gönderilmedi (kare görseli 0); ekran bilgileri paketteki OCR metninden alındı. Bu nedenle kareden_okunanlar boş bırakıldı ve OCR kaynaklı kayıtlar 'kare' etiketiyle, karede_gorulen olmadan yazıldı. OCR metni bozuk ve gürültülü.
- Transkript otomatik (ASR) ve isimleri bozuyor: Jed Borovik/Boravik, Barry Zhang/Jeang, Mahesh Murag/Morog, Cline/Klein, Codex/Codeex, Claude Code/Cloud Code, Antigravity/Anti-gravity. Kanıt alıntıları ASR metnine göre verildi.
- ClineBench ASR'de ClientBench olarak geçiyor; ekranda cline-bench benzeri ifade görünüyor. Ad ClineBench olarak alındı.
- Açıklama alanı 'yok' olarak geldi; açıklama bağlantısı yok. 'Bağlantılı sayfalar' bölümü yalnızca sayfa listesi olarak verildi ve ne videoda ne ekranda geçtiği için urller'e alınmadı.
- Açıklama dışı konuşma ve ekran kayıtları tamamen okunamadı: 9 saatlik kayıtta müzik/şarkı segmentleri (Heat tekrarları) analiz dışı bırakıldı; iz, urller ve adaylar kapsamı yüksek sinyalli öğelerle sınırlı tutuldu.
- Ekran OCR listesindeki bazı URL'ler bozuk veya tekrar (ör. sithub.com, Imarena.ai, Ghosty). Geçerli olanlar birleştirildi; kesin doğruluğu doğrulanamadı.
- Konuşmacıların bazı ifadeleri zaman damgası olarak kesin değil; zamanlar en yakın segment başlangıcı olarak yazıldı.
- Amp ekran günlüklerinde görünen yardımcı araçlar (pnpm, bun, vitest, svelte-check) ayrı aday yapılmadı; kanıtı yalnızca ekran metni.
- Sohbet arayüzüne yazılmış /slash komut bulunmadı; kurulum komutları ekran OCR'ından ve konuşmadan çıkarıldı.
- Biçimsel 'sayfa' bağlantıları (kitze.io, docs.claude.com, ampcode.com/docs vb.) videoda gösterilmediği için aday ve urller'e alınmadı.
## Atlanan segment oranı
0/525 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://github.com/humanlayer/humanlayer | 42:06 | ekran | evet |
| https://star-history.com | 42:12 | ekran | hayır |
| https://ghuntley.com/ralph/ | 45:34 | ekran | hayır |
| https://hlyr.dev/he-gh | 48:20 | ekran | hayır |
| https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html | 50:18 | ekran | hayır |
| https://blakesmith.me/2015/02/09/code-review-essentials-for-software-teams.html | 54:50 | ekran | hayır |
| https://hlur.dev/jobs | 59:52 | ekran | hayır |
| https://cursor.com/blog/kernels | 1:07:32 | ekran | hayır |
| https://cursor.com/agents | 1:08:32 | ekran | evet |
| https://cursor.com/blog/semsearch | 1:10:04 | ekran | hayır |
| https://lmarena.ai | 1:30:46 | ekran | evet |
| https://github.com/lm-sys/FastChat | 1:30:46 | ekran | hayır |
| https://wandb.ai/primeintellect/wiki-search-debug | 2:56:22 | ekran | evet |
| https://benji.so | 3:19:30 | ekran | hayır |
| https://sizzy.co | 3:19:30 | ekran | hayır |
| https://zerotoshipped.com | 3:19:30 | ekran | hayır |
| https://glink.so | 3:20:38 | ekran | hayır |
| https://redux.js.org | 3:22:36 | ekran | hayır |
| https://z.ai | 3:32:52 | ekran | evet |
| https://kitze.io | 3:20:10 | ekran | hayır |
| https://mc.jed.xyz | 4:52:46 | ekran | hayır |
| https://ai.studio/build | 4:57:44 | ekran | evet |
| https://aistudio.google.com/apps | 4:59:38 | ekran | evet |
| https://aistudio.google.com/apps/drive/... | 5:04:04 | ekran | hayır |
| https://github.com/sourcegraph/amp3 | 5:28:02 | ekran | evet |
| https://ampcode.com | 5:42:36 | ekran | evet |
| https://ampcode.com/how-to-build-an-agent | 5:30:42 | ekran | hayır |
| https://ampcode.com/news/gemini-3 | 5:37:44 | ekran | hayır |
| https://roboflow.com | 5:41:08 | ekran | hayır |
| https://hamel.dev | 5:42:36 | ekran | hayır |
| https://gimletlabs.ai | 6:03:44 | ekran | hayır |
| https://doc.rust-lang.org/cargo/reference/profiles.html#default-profiles | 7:13:12 | ekran | hayır |
| https://www.linkedin.com/in/aparnadhinakaran/ | 7:33:38 | ekran | hayır |
| https://tbench.ai/terminus | 7:35:42 | ekran | evet |
| https://github.com/cline/cline | 7:39:28 | ekran | evet |
| https://github.com/cline/cline/pull/6727 | 7:40:44 | ekran | hayır |
| https://metr.org/about | 7:49:40 | ekran | hayır |
| https://meter.org/careers | 8:08:39 | ses | hayır |
| http://localhost:3000 | 8:22:56 | ekran | hayır |
| http://api.aviationstack.com/v1/ | 8:27:46 | ekran | evet |
| https://app.devin.al/sessions/... | 21:22 | ekran | evet |
| https://luma.com/f3vuq3rj | 21:22 | ekran | hayır |
| https://github.com/aiDotEngineer/aiecode2025/pull/10 | 21:22 | ekran | hayır |
| ai.engineer/europe | 8:42:34 | ses | hayır |
## İş akışı
- 1. adım — VS Code içindeki Poolside asistanına kod tabanının ne yaptığını açıklatma (Ada) — araçlar: Visual Studio Code, Poolside Malibu
- 2. adım — Ada veritabanını Rust'a çevirme prompt'unu verme — araçlar: Poolside Malibu, Rust
- 3. adım — Canlı diff akışını izleme (dosya listesi ve değişiklik paneli) — araçlar: Poolside Malibu
- 4. adım — Ajanın yazdığı kodun derlenip çalıştırılması (cargo derleme çıktısı) — araçlar: Cargo, Rust
- 5. adım — Veritabanı CLI'ında CREATE/INSERT/SELECT ile elle doğrulama — araçlar: Rust
- 6. adım — Eksik özellik isteme: yukarı ok ile komut geçmişi — araçlar: Poolside Malibu
- 7. adım — Ajanın rustyline kütüphanesini eklemesi ve yeniden derlemesi — araçlar: rustyline, Cargo
- 8. adım — Ajanın yazdığı test betiklerini çalıştırma (chmod +x ve ./test_history.sh) — araçlar: Poolside Malibu
- 9. adım — Final demo betiği ile son doğrulama — araçlar: Poolside Malibu
- 10. adım — Google AI Studio'da prompt ile uygulama üretimi (Gemini 3 Pro, Nano Banana Pro) — araçlar: Google AI Studio, Gemini 3 Pro, Nano Banana Pro
- 11. adım — Ses/yüz yükleyip çizgi roman hikayesi üretme ve hikâye yönünü değiştirme — araçlar: Google AI Studio, Nano Banana Pro
- 12. adım — Yarış oyununu Three.js ile üretme ve çok oyunculu sürüme dönüştürme (QR ile katılım) — araçlar: Google AI Studio, Three.js, Shadcn/ui
## Promptlar
- Poolside ile Ada veritabanı kod tabanını Rust'a dönüştürme demosu — Ada kod tabanını Rust'a çevir. Derleme ve test komutlarını çalıştır, çalışmadığında düzelt.
- Poolside ajanına eksik bir özelliği istemek (rustyline ile geçmiş) — Veritabanı CLI'a yukarı ok tuşu ile komut geçmişinde gezinme özelliği ekle.
- Google AI Studio'da 3D yarış oyunu üretme (Gemini 3 ile) — Bir yarış oyunu yap; başlangıçta bot olan bir başlangıç ekranı olsun.
- Yeni bir arayüz özelliğini ideate etmek ve Antigravity'ye dışa aktarma akışı üretmek — Bu AI Studio ekran görüntüsünü mümkün olduğunca birebir klonla ve AI Studio'dan Antigravity'ye aktarma akışı ekle; yaratıcı ol.
- Gemini 3 ile tasarım odaklı tek seferlik site üretimi — Bir animasyonlu, kaydırmalı kayan (slick) web sitesi üret; cyberpunk olmasın.
- Nano Banana Pro ve Gemini 3 ile çok adımlı çizgi roman uygulaması — Bizi (Cat ve Ammaar) AI Engineer New York'ta sunum yaparken gösteren, Nano Banana Pro ile çizgi roman hikayesi üret; yüzleri kullan, tür ve dil seç, hikâye yönünü ortada değiştirebil.
- Kitze'nin vibe coding parodisi (tek satırlık abartılı prompt) — Kodu TypeScript'e taşı ve hiç hata yapma.
- Antigravity artifact yorumlarıyla ajana yön vermek — Yorum örneği: Tailwind kullanma, vanilla CSS kullan. (Antigravity'de görsel üzerine yorum bırakma)
- Amp'in kendi kaynak kodunda küçük özellik ekleme demosu — Amp'e alt sol köşeye yardım butonu ekle.
- Poolside'un yaratıcı yazım yeteneğini göstermek — Bu değişikliklerle ilgili bir şiir yaz. (Eğlence amaçlı)
- Arize Prompt Learning yönteminin özeti (SWE-bench 150 örnek) — Kod tabanlarında LLM'in her seferinde mevcut sistem prompt'una kural ekleyecek meta prompt: orijinal prompt, kurallar ve LLM-judge açıklamaları birleştirilerek yeni kurallar üretilir.
ikinci göz KAPALI: --ikinci-goz yok
