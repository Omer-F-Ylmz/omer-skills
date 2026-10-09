# Comment “AUDIT” and I’ll DM you the command and the guide: how to clean up your 
## Künye
Comment “AUDIT” and I’ll DM you the command and the guide: how to clean up your  · nocodealex · süre: 0:42 · ? · https://www.instagram.com/reel/Dd15NcHvlNl/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-26 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
tek kol: claude-sonnet-5-5 error_max_structured_output_retries:  · claude-haiku-5-5: claude-haiku-5-5 · 37124 tk
## Özet
42 saniyelik Instagram reel'i, Opus 5.5 için CLAUDE.md dosyasını temizlemeyi anlatıyor. Videoya göre eski modeller için yazılmış talimatlar (çift kontrol, BÜYÜK HARF, adım adım scriptler) Opus 5.5'i yavaşlatıp cevap kalitesini düşürüyor. Anthropic'in resmi claude-api skill'indeki prompt-audit komutu bu alışkanlıkları tarıyor, değişiklik önermeden önce rapor ve diff sunuyor, onay verilmeden hiçbir şey değişmiyor. Video maliyette ~%9 düşüş ve ~2 puan doğruluk artışı iddia ediyor, ancak bu sayılar doğrulanmış değil. Açıklama 'AUDIT' yorumu ve DM takibi istiyor.
## Bölümler
- yok
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| prompt-audit | yok | skill | yok | Anthropic'in claude-api skill'i içindeki prompt denetim aracı. CLAUDE.md, skill ve promptları tarar; üç alışkanlığı (çift kontrol, BÜYÜK HARF, adım adım scriptler) arar; önce rapor ve önerilen diff gösterir, kullanıcı onaylamadan değişiklik yapmaz. | 0:13 | prompt-audit (karede: Anthropic logosunun altındaki beyaz kartta 'prompt-audit' yazısı; kartın üstünde bulanık 'claude-api' etiketi.) |
| claude-api | yok | skill | yok | Anthropic'in resmi Claude API skill'i. Videoya göre prompt-audit komutu bu skill'in içinde yer alıyor. Kare 0:13'te ad bulanık görünüyor. | açıklama | Anthropic's own Claude API skill has a prompt audit built in |
| Claude Code | yok | CLI | yok | Anthropic'in terminal tabanlı kodlama aracı. Komut 'claude' ile başlatılıyor; /help ve /status gibi slash komutları ve y/n onay istemi gösteriliyor. | açıklama | Run it in Claude Code and it scans your CLAUDE.md |
| Opus 5.5 | yok | teknik | yok | Videonun ana hedefi olan Claude modeli. Videoya göre talimatları kelimesi kelimesine izliyor ve eski tarz talimatlar onu yavaşlatıyor. | 0:00 | But on Opus 5.5, those old instructions just slow it down |
| CLAUDE.md | yok | teknik | yok | Claude Code'un proje talimatlarını tuttuğu dosya. Videonun temizlenmesini önerdiği ana dosya. | 0:00 | their Claude.md is now making the new Opus model worse |
| AGENTS.md | yok | teknik | yok | Videoda bir geliştiricinin düzeltme bulduğu dosyalardan biri olarak geçiyor (skills, CLAUDE.md ile birlikte). | açıklama | his skills, CLAUDE.md and AGENTS.md |
| Eski modeller için yazılmış çift kontrol talimatı örneği; videoda kaçınılması gereken alışkanlık olarak gösteriliyor. | yok | prompt | yok | Her zaman çıktını iki kez kontrol et (Türkçe özet: 'Always double-check your work' tarzı talimat, eski model için yazılmış çift kontrol zorunluluğu). | 0:00 | kaynak: altyazı |
| Eski model (Opus etiketli, RETIRED damgalı) için yazılmış tekrar kontrol talimatı örneği. | yok | prompt | yok | Her şeyi iki kez kontrol et (Türkçe özet: 'DOUBLE-CHECK EVERYTHING' yapışkan notu). | 0:06 | kaynak: kare |
| Claude 3.5 Sonnet dönemine ait adım adım talimat örneği; videoda eski tarz olarak gösteriliyor. | yok | prompt | yok | Adım adım düşün (Türkçe özet: 'THINK STEP BY STEP' yapışkan notu). | 0:06 | kaynak: kare |
| Claude 2.1 dönemine ait doğrulama talimatı örneği; eski tarz olarak gösteriliyor. | yok | prompt | yok | Önce iki kez doğrula (Türkçe özet: 'VERIFY TWICE' yapışkan notu). | 0:05 | kaynak: kare |
| BÜYÜK HARFLE bağırılan talimat örneği; prompt-audit'in tespit ettiği alışkanlıklardan biri. | yok | prompt | yok | Her zaman şunu yapmak zorundasın (Türkçe özet: 'YOU MUST ALWAYS...' yarım kalmış, BÜYÜK HARF zorunluluk talimatı). | 0:05 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| claude | Terminalde Claude Code'u başlatır; ekranda 'Welcome to Claude Code!' karşılama mesajı çıkar. (karede: Terminal penceresinde 'claude— [yol]' satırı ve 'enter' yazısı görünüyor; altında 'Welcome to Claude Code!' mesajı (OCR).) | 0:16 | kare |
| /help | Claude Code içinde yardım bilgisini gösterir. (karede: Ekranda '/help for help, /status for your current setup' satırı görünüyor (OCR).) | 0:16 | kare |
| /status | Claude Code içinde mevcut kurulum durumunu gösterir. (karede: Ekranda '/help for help, /status for your current setup' satırı görünüyor (OCR).) | 0:16 | kare |
| prompt-audit | Claude Code'da çalıştırılan denetim komutu; CLAUDE.md, skill ve promptları tarar, düzeltmeleri önce rapor ve diff olarak gösterir. Tam çağırma sözdizimi videoda görünmüyor. | 0:00 | altyazı |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Opus 5.5 talimatları kelimesi kelimesine uyguluyor; eski talimatlar onu yavaşlatıyor ve cevap kalitesini düşürüyor. | 0:00 | özellik |
| Prompt-audit ile yapılan testte, aynı model üzerinde maliyet yaklaşık %9 düştü ve doğruluk yaklaşık 2 puan arttı. | 0:00 | sayısal |
| Bir geliştiricinin kurulumunda prompt-audit yaklaşık 70 düzeltme buldu. | 0:00 | sayısal |
| Prompt-audit önce ne kesmek istediğini gösterir; kullanıcı onaylamadan hiçbir değişiklik yapılmaz. | 0:00 | özellik |
| Prompt-audit CLAUDE.md, skill ve promptları tarayıp çift kontrol, BÜYÜK HARF ve adım adım scriptleri arıyor. | 0:00 | özellik |
| Prompt-audit, Anthropic'in resmi skill'lerinden geliyor ve GitHub'da 178 bin yıldız almış. | 0:13 | sayısal |
| Lance Martin prompt-audit'i Opus 5.5 için güncelledi, CJ Avilla prompt-audit'i ekledi, Boris Cherny Claude Code'u yarattı. | 0:13 | özellik |
| Opus 5.5 için CLAUDE.md temizliği tek komutla otomatik yapılabilir. | 0:00 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| açıklama | Claude Code, açıklamada komutun çalıştırılacağı araç olarak geçiyor | Claude Code | Run it in Claude Code and it scans your CLAUDE.md |
| ekran metni 0:16 | Terminalde 'claude' komutu ve 'Welcome to Claude Code!' ekranı | Claude Code | Welcome to Claude Code! |
| ekran metni 0:16 | Slash komutları /help ve /status | Claude Code | /help for help, /status for your current setup |
| ekran metni 0:27 | Onay istemi 'Apply? y/n' | Claude Code | Apply? y/n |
| açıklama | Anthropic'in resmi Claude API skill'i, prompt-audit'i içinde barındırıyor | claude-api | Anthropic's own Claude API skill has a prompt audit built in |
| kare 0:13 | Bulanık 'claude-api' etiketi kartın üstünde | claude-api | bulanık 'claude-api' etiketi |
| altyazı 0:00 | Komut adı 'Prompt Audit' | prompt-audit | It's called Prompt Audit |
| kare 0:13 | Kartta 'prompt-audit' adı ve 'added prompt-audit' notu | prompt-audit | prompt-audit |
| altyazı 0:00 | Eski tarz talimatların zarar verdiği model | Opus 5.5 | new Opus model worse |
| kare 0:13 | 'updated it for Opus 5.5' notu, Lance Martin | aday değil: başka adayın parçası (prompt-audit) | Lance Martin updated it for Opus 5.5 |
| kare 0:13 | 'added prompt-audit' notu, CJ Avilla | aday değil: başka adayın parçası (prompt-audit) | CJ Avilla added prompt-audit |
| kare 0:13 | 'created Claude Code' notu, Boris Cherny | aday değil: başka adayın parçası (Claude Code) | Boris Cherny created Claude Code |
| altyazı 0:00 | Claude.md dosyası | CLAUDE.md | their Claude.md is now making the new Opus model worse |
| açıklama | AGENTS.md dosyası, düzeltme bulunan dosyalardan biri | AGENTS.md | his skills, CLAUDE.md and AGENTS.md |
| kare 0:13 | Anthropic şirketi, 'FROM ANTHROPIC'S OFFICIAL SKILLS' başlığı | aday değil: genel kavram | FROM ANTHROPIC'S OFFICIAL SKILLS |
| kare 0:13 | GitHub, yıldız sayısı etiketi '178K stars on GitHub' | aday değil: genel kavram | 178K stars on GitHub |
| açıklama | 'skills' genel kavramı | aday değil: genel kavram | CLAUDE.md, skills and prompts |
| kare 0:06 | Eski model etiketi 'for CLAUDE 3.5 SONNET' (örnek) | aday değil: genel kavram | for CLAUDE 3.5 SONNET |
| kare 0:05 | Eski model etiketi 'for CLAUDE 2.1' (örnek) | aday değil: genel kavram | for CLAUDE 2.1 |
| kare 0:05 | Eski model etiketi 'for CLAUDE 3 HAIKU' (bulanık, örnek) | aday değil: genel kavram | for CLAUDE 3 HAIKU |
| kare 0:06 | Eski Opus etiketi 'for CLAUDE OPUS' ve RETIRED damgası (örnek) | aday değil: genel kavram | for CLAUDE OPUS RETIRED |
| kare 0:05 | Çift kontrol ve doğrulama talimatları, eski alışkanlık örneği | aday değil: genel kavram | VERIFY TWICE |
| ekran metni 0:00 | Başlıkta geçen 'MAKE' kelimesi (başlık metni) | aday değil: genel kavram | MAKE OPUS 5.5 SMARTER AND CHEAPER |
| ekran metni 0:34 | 'Claude Platform' ifadesi | aday değil: genel kavram | with Claude Platform |
| ekran metni 0:36 | 'Token Vault' ifadesi, görsel metin | aday değil: genel kavram | TOKEN VAULT |
| ekran metni 0:30 | Geliştirici adı 'DAN McATEER' ve '@daniel' etiketi | aday değil: konu dışı | @daniel DAN McATEER |
| ekran metni 0:41 | Hesap adı 'devon.builds' | aday değil: konu dışı | devon.builds |
| ekran metni 0:00 | Başlıkta görünen 'CLAUDE GYM' ifadesi | aday değil: konu dışı | CLAUDE GYM |
| kare 0:05 | Dekor tabelaları 'RECORDS 2023-2024' ve 'DO NOT THROW OUT' | aday değil: konu dışı | RECORDS 2023-2024 |
| sözlük eşleşmesi (ses 0:00) | Three.js eşleşmesi, konuşmada ve ekranda bağlam bulunamadı | aday değil: konu dışı | Three.js eşleşmesi bağlamsız |
| sözlük eşleşmesi (ses 0:00) | claude-mem eşleşmesi (bulanık claudemd), videoda anlatılmıyor | aday değil: konu dışı | claude-mem bulanık eşleşme |
| açıklama | Instagram yorum ve DM çağrısı ('Comment AUDIT', 'Follow') | aday değil: sponsor/reklam | Comment "AUDIT" and I'll DM you the command |
| ekran metni 0:41 | 'FREE GUIDE' ve 'GET THE COMMAND AND THE GUIDE' tanıtımı | aday değil: sponsor/reklam | GET THE COMMAND AND THE GUIDE |
| açıklama | Çift kontrol, BÜYÜK HARF ve adım adım talimatlar, eski alışkanlık kavramı | aday değil: genel kavram | Double-check your work rituals, instructions shouting in ALL CAPS |
## Kareden okunanlar
- 0:05: Başlık: 'WORKAROUNDS FOR RETIRED MODELS'; tabela 'RECORDS 2023-2024' ve 'DO NOT THROW OUT'; yapışkan notlar: 'CRITICAL!!', 'NEVER EVER...', 'YOU MUST ALWAYS...', 'VERIFY TWICE', 'for CLAUDE 3 HAIKU' (bulanık); alt yazı kutusu 'full of'.
- 0:06: Başlık: 'WORKAROUNDS FOR RETIRED MODELS'; notlar: 'THINK STEP BY STEP' (for CLAUDE 3.5 SONNET), 'NEVER EVER...', 'DOUBLE-CHECK EVERYTHING' (for CLAUDE OPUS, RETIRED damgası), 'VERIFY TWICE' (for CLAUDE 2.1), 'YOU MUST ALWAYS'; alt yazı kutusu 'written for older'.
- 0:13: Başlık: 'FROM ANTHROPIC'S OFFICIAL SKILLS'; kişi kartları: Lance Martin 'updated it for Opus 5.5', CJ Avilla 'added prompt-audit', Boris Cherny 'created Claude Code'; 'ANTHROPIC' logosu; kart: 'claude-api' (bulanık) ve 'prompt-audit'; '178K stars on GitHub'; alt yazı 'just built one'.
## Belirsizlikler
- Prompt-audit'i çağıran tam komut sözdizimi videoda okunabilir biçimde görünmüyor; yalnızca 'ONE COMMAND IN CLAUDE CODE' yazısı var.
- prompt-audit ve claude-api için GitHub repo bağlantısı videoda, açıklamada ya da ekranda yer almıyor; repo_url boş bırakıldı.
- Kare 0:13'teki 'claude-api' etiketi bulanık; adı yalnızca açıklamadaki 'Claude API skill' ifadesine dayanarak yazıldı.
- Maliyet %9 ve doğruluk 2 puan iddiaları bağımsız olarak doğrulanamadı; testi kimin yaptığı ve hangi koşullarda yapıldığı belirtilmiyor.
- Ekranda 'DAN McATEER' ve '@daniel' geçiyor; 70 düzeltmeyi bulan geliştiricinin bu kişi olup olmadığı kesin değil.
- Altyazının tamamı tek bir [0:00] segmenti olarak verilmiş; altyazıya dayanan kanıt zamanları 0:00 olarak yazıldı.
- Kurulum ve /help /status komutları ile 'Apply? y/n' istemi 0:16 ve 0:27 OCR metninden alındı; bu kareler gönderilmedi, yalnızca OCR okuması var.
- Sözlük eşleşmeleri Three.js ve claude-mem ile 'Make' ve 'Claude Sonnet' ekranda/seste bağlamsız geçiyor; Three.js ve claude-mem videoda anlatılmıyor, aday yapılmadı.
- Ekranda 'CLAUDE GYM' (0:00) ve açıklamada 'devon.builds' geçiyor; bunların marka/hesap adı olup olmadığı belirsiz.
- 'Claude Platform' (0:34) ve 'Token Vault' (0:36) ekran metinleri ne araç olduğu netleşmeden genel ifade olarak bırakıldı.
- Opus 5.5 model adı ve sürüm bilgisi videonun iddiası olarak kaldı; resmi bir kaynakla doğrulanmadı.
- Kare 0:05 ve 0:06'daki eski model etiketleri (Claude 3 Haiku, 3.5 Sonnet, 2.1, Opus) yalnızca örnek olarak gösteriliyor; videoda kullanılmıyor, aday yapılmadı.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
- yok
## İş akışı
- 1. adım — Terminalde Claude Code'u 'claude' komutuyla başlat — araçlar: Claude Code
- 2. adım — Kurulum durumunu ve yardımı /status ile /help üzerinden kontrol et — araçlar: Claude Code
- 3. adım — prompt-audit komutunu Claude Code içinde çalıştır — araçlar: Claude Code, prompt-audit
- 4. adım — CLAUDE.md, skill ve prompt dosyalarını tara — araçlar: prompt-audit, claude-api
- 5. adım — Üç alışkanlığı tespit et: çift kontrol ritüelleri, BÜYÜK HARF talimatlar, adım adım scriptler — araçlar: prompt-audit
- 6. adım — Rapor ve önerilen diff üret; hiçbir değişikliği henüz uygulama — araçlar: prompt-audit
- 7. adım — Kullanıcıdan onay iste (Apply? y/n) — araçlar: Claude Code
- 8. adım — Onaylanan kesimleri CLAUDE.md, skill ve promptlara uygula — araçlar: Claude Code, prompt-audit
- 9. adım — Maliyet ve doğruluk sonuçlarını (~%9 maliyet, ~2 puan doğruluk) iddia olarak değerlendir — araçlar: Opus 5.5
## Promptlar
- Eski modeller için yazılmış çift kontrol talimatı örneği; videoda kaçınılması gereken alışkanlık olarak gösteriliyor. — Her zaman çıktını iki kez kontrol et (Türkçe özet: 'Always double-check your work' tarzı talimat, eski model için yazılmış çift kontrol zorunluluğu).
- Eski model (Opus etiketli, RETIRED damgalı) için yazılmış tekrar kontrol talimatı örneği. — Her şeyi iki kez kontrol et (Türkçe özet: 'DOUBLE-CHECK EVERYTHING' yapışkan notu).
- Claude 3.5 Sonnet dönemine ait adım adım talimat örneği; videoda eski tarz olarak gösteriliyor. — Adım adım düşün (Türkçe özet: 'THINK STEP BY STEP' yapışkan notu).
- Claude 2.1 dönemine ait doğrulama talimatı örneği; eski tarz olarak gösteriliyor. — Önce iki kez doğrula (Türkçe özet: 'VERIFY TWICE' yapışkan notu).
- BÜYÜK HARFLE bağırılan talimat örneği; prompt-audit'in tespit ettiği alışkanlıklardan biri. — Her zaman şunu yapmak zorundasın (Türkçe özet: 'YOU MUST ALWAYS...' yarım kalmış, BÜYÜK HARF zorunluluk talimatı).
ikinci göz KAPALI: --ikinci-goz yok
