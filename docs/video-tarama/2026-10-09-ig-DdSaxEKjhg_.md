# Claude-Red is a free library of hacking skills you drop into Claude so it works 
## Künye
Claude-Red is a free library of hacking skills you drop into Claude so it works  · gittrend.io · süre: 0:35 · ? · https://www.instagram.com/reel/DdSaxEKjhg_/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-8 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 16557 tk · claude-haiku-5-5: claude-haiku-5-5 · 40686 tk
## Özet
Kısa reel, Claude-Red adlı ücretsiz ve açık kaynaklı saldırgan güvenlik skill kütüphanesini tanıtıyor. Her skill tek bir SKILL.md dosyası; Claude, sohbette SQL injection gibi bir konu geçince ilgili skill'i kendiliğinden yüklüyor. Depo bir kez klonlanıyor. Web uygulamaları, Wi-Fi, EDR atlatma gibi kategoriler var. Yetkili sızma testi ve red team işleri için, Cobalt Strike gibi ücretli çatılara ücretsiz alternatif olarak sunuluyor. Ekranda GitHub README'si geziniyor.
## Bölümler
- 0:00 Claude-Red tanıtımı ve README
- 0:07 Kurulum komutları (git clone, sparse-checkout, install.sh)
- 0:13 Kategori tablosu
- 0:24 Skill dizini (offensive-sqli, xss, ssrf vb.)
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude-Red | yok | skill | https://github.com/SnailSploit/Claude-Red | Claude için saldırgan güvenlik SKILL.md dosyalarından oluşan açık kaynaklı kütüphane (78 skill) | 0:00 | README başlığı claude-red, 78 skills, MIT license rozeti (karede: GitHub README: claude-red başlığı, 78 skills, MIT license, Stars 4.5k, Forks 617) |
| Claude | yok | CLI | yok | Skill'lerin yüklendiği ana yapay zekâ asistanı | 0:00 | Each skill is a single file you drop into Claude |
| Claude Skills System | yok | skill | yok | Konuşma tetikleyicilerine göre skill'leri isteğe bağlı yükleyen Claude mekanizması | 0:06 | README: Claude Skills System (Recommended) (karede: Kareler kısmen: README'de 'Claude Skills system' bağlantısı görünüyor) |
| Claude Code | yok | CLI | yok | Skill'leri cat ile system-file olarak vererek kullanma yöntemi | 0:09 | Claude Code başlığı altında cat ... / claude --system-file - (karede: Claude Code başlığı, cat Skills/web/offensive-sqli/SKILL.md / claude --system-file -) |
| Claude.ai | yok | iş akışı | yok | Manuel yöntem: SKILL.md içeriğini Project system prompt'una yapıştırma | 0:10 | Claude.ai (Manual) başlığı (karede: Claude.ai (Manual): SKILL.md içeriğini Project system prompt'una yapıştır) |
| Git | yok | CLI | yok | Depoyu klonlama ve sparse-checkout ile tek kategori kurma | 0:07 | git clone ve git sparse-checkout komutları (karede: git clone --filter=blob:none --sparse ... ; git sparse-checkout set Skills/web Skills/active-dir) |
| install.sh | yok | CLI | yok | Kategori ya da hedef klasör seçerek kurulum betiği | 0:12 | Install Script bölümü (karede: ./install.sh, --target ~/.claude/skills, --category web) |
| GitHub | yok | teknik | yok | Deponun barındırıldığı platform | 0:00 | github.com/SnailSploit/Claude-Red#readme adres çubuğu (karede: Tarayıcıda github.com/SnailSploit/Claude-Red#readme) |
| SKILL.md | yok | teknik | yok | Her skill'in yapılandırılmış tek dosya biçimi | 0:00 | drop-in SKILL.md files (karede: README: Offensive security skills for Claude — drop-in SKILL.md files) |
| Cobalt Strike | yok | teknik | yok | Ücretli red team çatısı; Claude-Red ücretsiz alternatif olarak anıldı | 0:00 | a free alternative to paid frameworks like Cobalt Strike |
| offensive-sqli | yok | skill | https://github.com/SnailSploit/Claude-Red | SQL injection konularında otomatik yüklenen skill dosyası (Skills/web/offensive-sqli/SKILL.md) | 0:07 | mentioning SQL injection loads offensive-sqli (karede: README kurulum bölümünde ekran metni: 'mentioning SQL injection loads offensive-sqli') |
## Açıklama bağlantıları
- gittrend.io — Açıklamadaki 'More like this' bağlantısı; ilgili içerik sitesi · aday: hayır · Tanıtım/yönlendirme sayfası; kullanılan bir araç değil · sınıf: diğer
- https://github.com/snailsploit — Yazar (SnailSploit) GitHub profili; bağlantılı sayfalar bölümünde · aday: hayır · Yazar profili; izleyicinin kullanabileceği araç değil · sınıf: diğer
- https://github.com/advisories/GHSA-x2xq-qhjf-5mvg — GitHub güvenlik danışmanlığı kaydı (GHSA-x2xq-qhjf-5mvg); bağlantılı sayfalar bölümünde · aday: hayır · Referans danışmanlık kaydı; videoda anlatılmıyor ve kullanılmıyor · sınıf: diğer
- https://snailsploit.com — Yazar/proje sitesi; bağlantılı sayfalar bölümünde · aday: hayır · Referans/ilham sayfası; kullanılabilir araç değil · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| git clone https://github.com/SnailSploit/claude-red ~/.claude/skills/ | Tüm kütüphaneyi Claude skills klasörüne klonlar (karede: git clone https://github.com/SnailSploit/claude-red -/.claude/sk1lls/ (OCR'dan)) | 0:07 | kare |
| git clone --filter=blob:none --sparse https://github.com/SnailSploit/... | Depoyu yalnız gerekli kısmı için seyrek klonlar (karede: git clone --filter=blob:none --sparse https://github.com/SnailSploit/) | 0:08 | kare |
| cd claude-red && git sparse-checkout set Skills/web Skills/active-dir | Yalnız seçilen kategorileri çeker (karede: cd claude-red && git sparse-checkout set Skills/web Skills/active-dir) | 0:08 | kare |
| cat Skills/web/offensive-sqli/SKILL.md / claude --system-file - | Tek skill'i sistem prompt'u olarak Claude Code'a verir (karede: cat Skills/web/offensive-sqli/SKILL.md / claude --system-file -) | 0:09 | kare |
| cat Skills/active-directory/**/SKILL.md / claude --system-file - | Active Directory skill'lerini sistem prompt'u olarak verir (karede: cat Skills/active-directory/**/SKILL.md / claude --system-file -) | 0:10 | kare |
| ./install.sh --category web | Yalnız web kategorisini kurar (karede: ./install.sh --category web # single category) | 0:12 | kare |
| ./install.sh --target ~/.claude/skills | Açık hedef klasöre kurar (karede: ./install.sh --target ~/.claude/skills # explicit target) | 0:12 | kare |
| git clone --filter=blob:none --sparse https://github.com/SnailSploit/claude-red | Blob'suz sparse modda klonlar; yalnız seçilen dizinler indirilir (karede: (karede OCR) GitHub - SnailSploit/Claude× + Install % github.com/SnailSploit/Claude-Red#readme © C * : ← Contributing : Security README MIT license snailsploit.com claude-red Offensive security skills for Claude —) | 0:08 | kare |
| ./install.sh | Etkileşimli (interactive) kurulum betiğini çalıştırır (karede: (karede OCR) GitHub - SnailSploit/Claude × + Install github.com/SnailSploit/Claude-Red#readme © C * % : ← Contributing : README MIT license Security system. Each skillis a structured sKILL . md file that primes Cl) | 0:12 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Claude-Red, Cobalt Strike gibi ücretli çatılara ücretsiz alternatiftir | 0:00 | karşılaştırma |
| Depoda 78 skill ve 23 kategori var; 4.5k yıldız, 617 fork | 0:04 | sayısal |
| Skill'ler konuşma tetikleyicilerine göre isteğe bağlı yüklenir, kullanılmayan skill için bağlam harcanmaz | 0:00 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Claude Red skill kütüphanesi | Claude-Red | Claude Red is a free library of hacking skills |
| konuşma 0:00 | Claude | Claude | drop into Claude |
| konuşma 0:00 | SQL injection | aday değil: genel kavram | loads when you mention SQL injection |
| konuşma 0:00 | Cobalt Strike | Cobalt Strike | free alternative to paid frameworks like Cobalt Strike |
| kare 0:00 | GitHub README | GitHub | github.com/SnailSploit/Claude-Red#readme |
| kare 0:07 | git clone | Git | git clone https://github.com/SnailSploit/claude-red |
| kare 0:09 | Claude Code | Claude Code | Claude Code başlığı |
| kare 0:10 | Claude.ai | Claude.ai | Claude.ai (Manual) |
| kare 0:12 | install.sh | install.sh | ./install.sh --category web |
| kare 0:00 | SKILL.md dosyaları | SKILL.md | drop-in SKILL.md files |
| kare 0:06 | Claude Skills System | Claude Skills System | Claude Skills System (Recommended) |
| kare 0:22 | Kubernetes kategori satırı | aday değil: başka adayın parçası (Claude-Red) | Container & Kubernetes kategorisi |
| kare 0:22 | Kategori tablosu (OSINT, fuzzing, AFL++ vb.) | aday değil: başka adayın parçası (Claude-Red) | Fuzzing, libFuzzer, AFL++ kategorileri |
| açıklama | gittrend.io | aday değil: konu dışı | More like this → gittrend.io |
| açıklama | Etiketler (#cybersecurity vb.) | aday değil: genel kavram | #cybersecurity #redteam #claude |
| linkli sayfa | github.com/SnailSploit | aday değil: başka adayın parçası (Claude-Red) | Yazar profili bağlantısı |
| linkli sayfa | GHSA-x2xq-qhjf-5mvg advisory | aday değil: konu dışı | github.com/advisories/GHSA-x2xq-qhjf-5mvg |
| linkli sayfa | snailsploit.com | aday değil: başka adayın parçası (Claude-Red) | Yazarın sitesi, kapakta görünüyor |
| yorum | Yorumlar | aday değil: konu dışı | girişsiz alınamıyor |
## Kareden okunanlar
- 0:00: GitHub SnailSploit/Claude-Red README: 78 skills, MIT, 23 categories, 4.5k yıldız, 617 fork; yazarlar SnailSploit & Mixbanana
- 0:16: Kurulum komutları, Claude Code, Claude.ai (Manual), Install Script ve kategori tablosunun başı
- 0:22: Kategori tablosu: Web Application 16, Wireless 14, Infrastructure & Red Team 7, Exploit Development 6 skill vb.
## Belirsizlikler
- Sözlük eşleşmeleri (Redis, Stripe, strix, claude-mem vb.) videoda kullanılmıyor, bulanık eşleşme sayıldı.
- Yorumlar girişsiz alınamadı; 'red' yorumuyla repo linki gönderildiği belirtiliyor.
- Kare 0:16 ve 0:22 yoluyla kısmen okunabilen metinler OCR hatalı.
- Skill'lerin yetkili kullanım amacı dışında kötüye kullanım riski var; videoda yalnız yetkili çalışma vurgulanıyor.
- Kategori sayısı 23 rozetten okundu (OCR 'categories 23' belirsiz).
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.instagram.com/reel/DdSaxEKjhg_/ | açıklama | açıklama | hayır |
| github.com/SnailSploit/Claude-Red#readme | 0:00 | ekran | evet |
| snailsploit.com | 0:00 | ekran | hayır |
| https://github.com/SnailSploit/ | 0:08 | ekran | hayır |
| gittrend.io | açıklama | açıklama | hayır |
| https://github.com/advisories/GHSA-x2xq-qhjf-5mvg | açıklama | açıklama | hayır |
| https://claude.ai | 0:10 | ekran | evet |
## İş akışı
- 1. adım — Claude-Red deposunu GitHub'dan klonla — araçlar: Git, GitHub
- 2. adım — Yalnız web ve active-directory kategorilerini sparse-checkout ile al — araçlar: Git
- 3. adım — offensive-sqli skill dosyasını Claude Code'a sistem dosyası olarak ver — araçlar: Claude Code
- 4. adım — Active Directory skill dosyalarını birleştirip Claude Code'a ver — araçlar: Claude Code
- 5. adım — Claude.ai'de manuel yöntem: SKILL.md içeriğini proje sistem promptuna yapıştır — araçlar: Claude.ai
- 6. adım — install.sh ile etkileşimli kurulum başlat — araçlar: install.sh
- 7. adım — install.sh --target ile skill'leri hedef dizine kur — araçlar: install.sh
- 8. adım — install.sh --category web ile tek kategori kur — araçlar: install.sh
- 9. adım — Konuşmada SQL injection geçince offensive-sqli skill'inin otomatik yüklendiğini göster — araçlar: Claude Skills System, offensive-sqli
- 10. adım — Kategori tablosunu incele (Web Application, Auth & Identity, Active Directory, Wireless vb.) — araçlar: GitHub
## Promptlar
- yok
