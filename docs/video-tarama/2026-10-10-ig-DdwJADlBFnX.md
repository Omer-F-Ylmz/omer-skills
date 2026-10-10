# Comment “AI” and I’ll send you the repo.
## Künye
Comment “AI” and I’ll send you the repo. · ericdoestech · süre: 0:21 · ? · https://www.instagram.com/reel/DdwJADlBFnX/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-10-short-17 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 45936 tk · claude-haiku-5-5: claude-haiku-5-5 · 171944 tk
## Özet
21 saniyelik reel: ericdoestech, Anthropic hackathon kazananının oluşturduğunu söylediği ve 262 bin GitHub yıldızını geçen ECC (Everything Claude Code) deposunu tanıtıyor. Depo 64 uzman ajan, 261 skill ve 84 komut/hook içeriyor ve tek komutla kuruluyor. Ekranda GitHub deposu, geliştirici profili, skill/komut listeleri, kurulum komutları ve Plan Canvas arayüzü gösteriliyor. Sonda izleyiciden 'AI' yorumu yazması isteniyor.
## Bölümler
- 0:00 ECC deposu ve 262 bin yıldız
- 0:04 Oluşturucu Affaan Mustafa profili
- 0:06 Ajan, skill ve komut listeleri
- 0:12 Harness audit ve model yönlendirme
- 0:14 Tek komutla kurulum
- 0:15 Plan Canvas arayüzü
- 0:20 Yorum çağrısı: 'AI'
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| ECC | yok | plugin | https://github.com/affaan-m/ECC | Claude Code için ajan, skill, komut ve hook içeren harness performans optimizasyon sistemi | 0:00 | Depo affaan-m / ECC, agent harness performance optimization system (karede: GitHub sayfası affaan-m/ECC Public, 263.0k stars, 39.4k forks, ecc.tools bağlantısı, v2.2.1 Latest) |
| Claude Code | yok | CLI | yok | ECC'nin üzerinde çalıştığı ana yapay zekâ aracı | 0:14 | /plugin install ecc@ecc komutu Claude Code içinde çalıştırılıyor (karede: README 'Claude Code details' bölümü ve /plugin komutları) |
| Claude | yok | CLI | yok | Konuşmada 'Clawd' diye geçen asistan; tek asistandan ekibe dönüşüyor | 0:00 | Clawd leaps from being one assistant to an entire AI development team |
| Plan Canvas | yok | skill | https://github.com/affaan-m/ECC/tree/main/skills/plan-canvas | /plan onay kapısını tarayıcıda açıp not düşme ve onaylama imkânı veren skill | 0:15 | Plan Canvas plan-canvas-demo.plan.md, Approve plan, annotate (karede: Koyu tema Plan Canvas sayfası: OpenCode, ECC, 279 skills, 67 agents, Annotate kutusu, sıra diyagramı) |
| AgentShield | yok | CLI | https://github.com/affaan-m/agentshield | ECC güvenlik tarama aracı | 0:06 | OCR: AGENTSHIELD rozeti; 0:15 diyagramda AgentShield kutusu (karede: 0:15 karede diyagramda AgentShield kutusu; 0:06 OCR AGENTSHIELD) |
| ecc-universal | yok | CLI | yok | ECC'nin npm paketi | 0:06 | OCR: NPM: ECC-UNIVERSAL (karede: NPM: ECC-UNIVERSAL rozeti (OCR metni)) |
| OpenCode | yok | CLI | yok | Plan Canvas diyagramında ajan ortamı olarak görünen araç | 0:15 | Diyagramda OpenCode kutusu içinde Your agent (karede: Diyagramın üstünde OpenCode ve Your agent kutuları) |
| Codex CLI | yok | CLI | yok | ECC'nin desteklediği diğer ajan aracı | 0:12 | OCR: Codex CLI ve codex app ifadesi (karede: Codex CLI yazılı harness bölümü (OCR metni)) |
| /harness-audit | yok | skill | yok | Harness'i ölçüp zayıf kapıları bulan komut | 0:12 | OCR: /harness-audit . -format text (karede: Harness Positioning bölümünde komut (OCR metni)) |
| /quality-gate | yok | skill | yok | Kalite kapısı komutu | 0:13 | OCR: /quality-gate . -strict (karede: Komut satırı (OCR metni)) |
| GitHub | yok | teknik | yok | Deponun barındığı platform ve klonlama kaynağı | 0:14 | git clone https://github.com/affaan-m/ECc.git (karede: README kurulum bölümünde git clone ve cd ECC) |
| Git | yok | CLI | yok | Manuel kurulum adımında repoyu yerel klasöre klonlamak için kullanılan sürüm kontrol aracı. | 0:14 | git clone https://github.com/affaan-m/ECC.git (karede: 0:14 ekran metninde 'git clone' komutu (kare görseli ekte değil, OCR).) |
| Plan Canvas'ta plan bölümüne açıklama (annotation) yazma | yok | prompt | yok | Plan başlığının bir bölümüne 'Add install and...' notu yazılıp kuyruğa alınır; amaç kurulum ve yükseltme komutlarının plana eklenmesini istemek. | 0:15 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Plan onay arayüzü (Plan Canvas) | Plan tarayıcıda açılıyor; Annotate kutusu, Send to agent, Approve plan ve Cancel/Queue düğmeleri ile sohbet paneli var (karede: Koyu sayfada Annotate <H2> kutusu 'Add install and', Cancel/Queue düğmeleri, sıra diyagramı) | 0:15 | kare |
| Mimari akış diyagramı (architecture diagram) | Your agent, 279 skills, Rules, Memory + instincts, 67 agents, Hooks, AgentShield kutuları oklarla bağlı (karede: OpenCode ve ECC çerçeveli kutular ve oklar) | 0:15 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| /plugin marketplace add https://github.com/affaan-m/ECC | ECC marketplace'ini Claude Code'a ekler (karede: README kurulum bölümünde komut satırı (OCR: .../affaan-m/Ecc)) | 0:14 | kare |
| /plugin install ecc@ecc | ECC eklentisini Claude Code'a kurar (karede: README kurulum bölümünde komut satırı) | 0:14 | kare |
| git clone https://github.com/affaan-m/ECC.git | ECC deposunu yerel olarak klonlar (manuel kurulum) (karede: README kod bloğu) | 0:14 | kare |
| cd ECC | Klonlanan klasöre girer (karede: README kod bloğu) | 0:14 | kare |
| cp -R rules/common [yol] | Ortak kural paketini hedef klasöre kopyalar (karede: README kod bloğu) | 0:14 | kare |
| /harness-audit . -format text | Harness'i denetler ve metin raporu verir (karede: Harness Positioning bölümü) | 0:12 | kare |
| /quality-gate . -strict | Katı kalite kapısı çalıştırır (karede: Komut satırı (OCR metni)) | 0:13 | kare |
| /ecc:configure-ecc | ECC kurulduktan sonra Claude içinden yeniden yapılandırma skill'ini çalıştırır. (karede: 0:14 ekran metninde 'After ECC is installed, /ecc:configure-ecc' yazısı (kare görseli ekte değil, OCR).) | 0:14 | kare |
| ECC_HOOK_PROFILE=strict ECC_DISABLED_HOOKS=... | Hook profilini sıkı moda alır ve belirtilen hook'ları devre dışı bırakır (ortam değişkenleri). (karede: 0:13 ekran metninde ortam değişkeni satırı (kare görseli ekte değil, OCR).) | 0:13 | kare |
| /plan | Plan onay kapısını başlatır; Plan Canvas tarayıcı sayfasında açılır. (karede: 0:15 ekran metninde '/plan ends with a hard confirmation gate' ifadesi (kare 3 ile uyumlu).) | 0:15 | kare |
| mkdir -p [yol] | Kural paketlerinin kopyalanacağı hedef klasörü oluşturur. (karede: 0:14 ekran metninde 'mkdir -p [yol]' satırı (kare görseli ekte değil, OCR).) | 0:14 | kare |
| cp -R rules/typescript [yol] | TypeScript kural paketini kopyalar; belgede 'kendi stack'inizle değiştirin' notu var. (karede: 0:14 ekran metninde 'cp -R rules/typescript' satırı (kare görseli ekte değil, OCR).) | 0:14 | kare |
| ./install.sh --profile full | Tam manuel kurulumu çalıştırır; plugin kurulduysa çalıştırılmaması uyarısı var. (karede: 0:14 ekran metninde './install.sh --profile full' ifadesi (kare görseli ekte değil, OCR).) | 0:14 | kare |
| ecc feedback | Kurulum veya çalışma sorunlarını raporlamak için tanı çıktısı üretir. (karede: 0:14 ekran metninde 'run ecc feedback' ifadesi (kare görseli ekte değil, OCR).) | 0:14 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Depo 262.000'den fazla GitHub yıldızına ulaştı | 0:00 | sayısal |
| 64 uzman ajan, 261 skill, 84 komut ve hook içeriyor | 0:00 | sayısal |
| Tek komutla tüm kurulum yapılıyor | 0:00 | özellik |
| Depo bir Anthropic Hackathon kazananı tarafından oluşturuldu | 0:00 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| altyazı 0:00 | Clawd/Claude | Claude | Clawd repo already crossed 262,000 GitHub stars |
| kare 0:00 | affaan-m/ECC deposu | ECC | affaan-m / ECC Public |
| altyazı 0:00 | Anthropic Hackathon | aday değil: genel kavram | created by an Anthropic Hackathon winner |
| kare 0:00 | GitHub | GitHub | GitHub depo arayüzü |
| kare 0:04 | Affaan Mustafa profili | aday değil: başka adayın parçası (ECC) | Profil sayfası affaan-m |
| kare 0:06 | AgentShield | AgentShield | OCR AGENTSHIELD |
| kare 0:06 | ECC-UNIVERSAL | ecc-universal | NPM: ECC-UNIVERSAL |
| kare 0:06 | skill ve komut listeleri | aday değil: başka adayın parçası (ECC) | code-reviewer, /santa-loop, gan-planner |
| kare 0:12 | Codex CLI | Codex CLI | OCR Codex CLI |
| kare 0:12 | /harness-audit | /harness-audit | /harness-audit . -format text |
| kare 0:13 | /quality-gate | /quality-gate | /quality-gate . -strict |
| kare 0:14 | /plugin komutları | Claude Code | /plugin install ecc@ecc |
| kare 0:14 | git clone | GitHub | git clone https://github.com/affaan-m/ECc.git |
| kare 0:15 | Plan Canvas | Plan Canvas | Plan Canvas plan-canvas-demo.plan.md |
| kare 0:15 | OpenCode | OpenCode | OpenCode kutusu diyagramda |
| kare 0:15 | 279 skills, 67 agents | aday değil: başka adayın parçası (ECC) | diyagram kutuları |
| kare 0:19 | Dreamina | aday değil: konu dışı | OCR 'Dreamina' tek satır, kullanım belirsiz |
| altyazı 0:00 | Yorum çağrısı 'AI' | aday değil: konu dışı | Comment AI and I'll send it over |
| bağlantılı sayfa ecc.tools | ecc.tools sayfası | ECC | Bağlantılı sayfalar listesi |
| bağlantılı sayfa affaanmustafa.com | Kişisel site ve proje bağlantıları | aday değil: konu dışı | itomarkets.com, pmx.trade gibi bağlantılar videoda anlatılmıyor |
## Kareden okunanlar
- 0:00: affaan-m/ECC Public, 263.0k stars, 39.4k forks, v2.2.1 Latest, MIT license, ecc.tools
- 0:04: Affaan Mustafa (affaan-m), 11.1k followers, affaanmustafa.com, Ito-Markets, ECC-Tools
- 0:15: Plan Canvas: OpenCode, ECC, 279 skills, 67 agents, Approve plan, annotate 'Split phase 2'
## Belirsizlikler
- Konuşmada 'Clawd' geçiyor; Claude kastedildiği varsayıldı.
- Konuşma 64 ajan/261 skill derken ekranda 67 ajan/279 skill görünüyor; sürüm farkı olabilir.
- Yorumlar girişsiz alınamadı.
- Dreamina 0:19'da OCR'da görünüyor ama videoda kullanıldığı belli değil.
- Depo dosya listesindeki .codex-plugin, .kimi, .openclaw, .hermes gibi klasörler yalnız listede göründü, adaya alınmadı.
- Bağlantılı sayfalardaki ürün/depo adları (ito-compute, pmx.trade vb.) videoda gösterilmedi, aday alınmadı.
- OCR sözlük eşleşmeleri (Inter, Canva, Bun, Cursor) gürültü veya yalnız liste öğesi olabilir.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://github.com/affaan-m/ECC | 0:00 | ekran | evet |
| https://affaanmustafa.com | 0:04 | ekran | hayır |
| https://orcid.org/0009-0009-9408-5570 | 0:04 | ekran | hayır |
| https://github.com/affaan-m/ECC.git | 0:14 | ekran | evet |
| ecc.tools | 0:00 | ekran | evet |
## İş akışı
- 1. adım — ECC GitHub deposunu ve yıldız sayısını gösterme — araçlar: GitHub, ECC
- 2. adım — Oluşturucu Affaan Mustafa profilini gösterme — araçlar: GitHub
- 3. adım — Ajan, skill ve komut listelerini gezme — araçlar: ECC, Claude Code
- 4. adım — Harness audit ve model yönlendirme bölümlerini gösterme — araçlar: ECC, Codex CLI
- 5. adım — Tek komutlu kurulum adımlarını gösterme — araçlar: Claude Code, ECC, GitHub
- 6. adım — Plan Canvas ile plan onay arayüzünü gösterme — araçlar: Plan Canvas, OpenCode
- 7. adım — İzleyiciyi 'AI' yorumu yazmaya çağırma — araçlar: Instagram
## Promptlar
- Plan Canvas'ta plan bölümüne açıklama (annotation) yazma — Plan başlığının bir bölümüne 'Add install and...' notu yazılıp kuyruğa alınır; amaç kurulum ve yükseltme komutlarının plana eklenmesini istemek.
ikinci göz KAPALI: --ikinci-goz yok
