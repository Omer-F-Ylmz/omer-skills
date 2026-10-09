# Claude Code ve Codex’e Böyle Başla (Bugün Başlasaydım #2)
## Künye
Claude Code ve Codex’e Böyle Başla (Bugün Başlasaydım #2) · İsa Nurdoğdu · süre: 19:02 · tr-orig · https://youtu.be/oEnVigmlHPA · şema 2
motor: parti 2026-10-09-uzun-4 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (59)
kareler: girdi ≤40000 jeton için 60→59
claude-sonnet-5-5: claude-sonnet-5-5 · 65411 tk · claude-haiku-5-5: claude-haiku-5-5 · 108712 tk
## Özet
İsa Nurdoğdu, Claude Code ve Codex'te ajanın kararları unutmasının nedenini tek CLAUDE.md'ye her şeyi yığmakla açıklıyor. Çözüm olarak evrensel bir proje yapısı kuruyor: CLAUDE.md ana talimat dosyası, AGENTS.md ona yönlendiren ince katman, context/README.md haritası, hedefler/kararlar/kurallar-ve-sınırlar/proje-özeti dosyaları ve kaynaklar sistemi. Hafızayı güncellemek için proje-hafızası skill'i gösteriliyor. Sonda indirilen taslağın ILK-PROMPT.txt ile kişiselleştirilmesi ve İsa Strateji Ofisi örneği anlatılıyor.
## Bölümler
- 0:00 Ajan neden unutuyor?
- 1:10 Yapılan hata: her şeyi tek CLAUDE.md'ye yığmak
- 2:19 Evrensel proje: CLAUDE.md ve AGENTS.md mantığı
- 4:05 Context klasörü: haritalama ile token tasarrufu
- 7:13 İki soru: neden sadece CLAUDE.md yetmez, skill ne olacak?
- 9:03 Context kalıbı: hedefler, kararlar, kurallar dosyaları
- 11:58 Kaynakları ve hafızayı güncelleme alışkanlığı
- 14:27 Taslağı indirip kendine uyarlama: ilk prompt
- 17:02 Canlı örnek: İsa Strateji Ofisi ve kapanış
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Code | yok | CLI | yok | Anthropic'in kodlama ajanı; CLAUDE.md'yi ilk okuyan ana ajan olarak kullanılıyor. | 0:00 | Cloud Code veya Codex'te bir projeye başladığınızda ilk günler her şey iyi gidiyor |
| Codex | yok | CLI | yok | OpenAI'ın ajanı; AGENTS.md'yi okuyup CLAUDE.md'ye yönleniyor. | 0:02 | Codex kenar çubuğu ve proje oluşturma ekranı gösteriliyor (karede: kanıttan) Codex kenar çubuğu ve proje oluşturma ekranı gösteriliyor |
| Antigravity | yok | CLI | yok | Aynı evrensel yapının çalıştığı üçüncü ajan aracı. | 0:24 | Antigravity 2.0 logosu ve New Conversation menüsü (karede: kanıttan) Antigravity 2.0 logosu ve New Conversation menüsü |
| CLAUDE.md | yok | teknik | yok | Ajanın ilk okuduğu ana kalıcı talimat dosyası. | 2:19 | Cloud MD'yi okuyor. O yüzden Cloud MD'yi ana dosya olarak tutuyoruz |
| AGENTS.md | yok | teknik | yok | Codex uyumluluk katmanı; ana talimat dosyasının CLAUDE.md olduğunu söyler. | 3:28 | Codex Uyumluluk Talimatları başlıklı AGENTS.md dosyası VS Code'da açık (karede: kanıttan) Codex Uyumluluk Talimatları başlıklı AGENTS.md dosyası VS Code'da açık |
| context/README.md | yok | teknik | yok | Bağlam dosyalarını ve ne zaman okunacaklarını haritalayan ana harita. | 5:46 | README.md'de Konum/İçeriği/Ne zaman okunmalı tablosu görünüyor (karede: kanıttan) README.md'de Konum/İçeriği/Ne zaman okunmalı tablosu görünüyor |
| proje-hafızası | yok | skill | yok | Hafızayı güncelleme, bağlamı denetleme ve kaynakları denetleme yapan skill. | 13:26 | SKILL.md'de name: proje-hafızası ve üç çalışma biçimi listeleniyor (karede: kanıttan) SKILL.md'de name: proje-hafızası ve üç çalışma biçimi listeleniyor |
| Miro | yok | iş akışı | yok | Mimari şemaların gösterildiği beyaz tahta aracı. | 0:26 | miro.com adresinde Bugün Başlasaydım #2 panosu açık (karede: kanıttan) miro.com adresinde Bugün Başlasaydım #2 panosu açık |
| Visual Studio Code | yok | CLI | yok | CLAUDE.md, AGENTS.md ve README dosyalarını göstermek için editör. | 3:06 | VS Code'da CLAUDE.md açık, File Edit Selection menüsü görünüyor (karede: kanıttan) VS Code'da CLAUDE.md açık, File Edit Selection menüsü görünüyor |
| ILK-PROMPT.txt | yok | prompt | yok | Taslağı kişiselleştiren ilk prompt dosyası. | 14:27 | ilk prompt diye bir txt dosyası var. Bunu açıyorsunuz |
| Fable 5.1 | yok | CLI | yok | Claude uygulamasında favori model olarak görünüyor. | 0:30 | Favorite model: Fable 5.1 istatistik kartında (karede: kanıttan) Favorite model: Fable 5.1 istatistik kartında |
| Opus 5 Fast | yok | CLI | yok | Claude uygulamasında prompt verirken seçili model. | 13:38 | Alt çubukta Opus 5 Fast Medium yazıyor (karede: kanıttan) Alt çubukta Opus 5 Fast Medium yazıyor |
| GPT-5.6 Sol | yok | CLI | yok | Codex uygulamasında seçili model. | 16:24 | Codex giriş çubuğunda GPT-5.6 Sol Yüksek yazıyor (karede: kanıttan) Codex giriş çubuğunda GPT-5.6 Sol Yüksek yazıyor |
| Notion | yok | iş akışı | yok | Taslak dosyasının paylaşıldığı sayfa. | açıklama | app.notion.com bağlantısı açıklamada taslak için veriliyor |
| .claude/ klasörü | yok | teknik | yok | Claude Code'un ayar ve skill klasörü; içinde skills/ alt klasörü bulunur. | 8:44 | benim projem> .claude> skills (karede: Dosya gezgininde benim projem > .claude > skills yolu açık; proje-hafızası klasörü görünüyor.) |
| Not Defteri | yok | teknik | yok | ILK-PROMPT.txt dosyasını açıp promptu kopyalamak için kullanılan metin editörü. | 15:38 | Bu projeyi inceleyerek ana proje talimatlarını yapılandırmanı istiyorum. (karede: Not Defteri penceresinde ilk prompt metni açık; 'Bu projeyi inceleyerek ana proje talimatlarını yapılandırmanı istiyorum' yazıyor.) |
| Windows Dosya Gezgini | yok | teknik | yok | Proje klasörünü ve dosyalarını (agents, claude, context, AGENTS.md, CLAUDE.md) gezmek için kullanılan dosya yöneticisi. | 2:18 | benim projem klasöründe ara · kanıt: kare (karede: Windows Gezgini'nde benim projem klasörü; agents, claude, context klasörleri ve AGENTS.md, CLAUDE.md dosyaları listeleniyor.) |
| Taslak projeyi kullanıcının kendi projesine uyarlatmak | yok | prompt | yok | Projeyi incele; CLAUDE.md, AGENTS.md ve context/README.md dosyalarını oku, yönlendirilen bağlam dosyalarını incele. Evrensel kuralları ve bölüm sırasını koru, yalnızca projeye özel kalıcı talimatlar bölümünü güncelle, AGENTS.md ve skill dosyalarını değiştirme. Yalnızca doğrulanabilir bilgi yaz, hedef/kural/komut tahmin etme, eksik kritik bilgileri kısa sorularla sor, cevaplardan sonra değişiklikleri kısaca açıkla. | 15:38 | kaynak: kare |
| Oturum sonunda proje hafızasını güncellemek | yok | prompt | yok | /proje-hafızası komutuyla hafızayı güncelle, bağlamı denetle veya kaynakları denetle. | 13:42 | kaynak: kare |
## Açıklama bağlantıları
- https://www.youtube.com/playlist?list=PLNRUkhedZiRQ — Bugün Başlasaydım oynatma listesi · aday: hayır · Video serisi listesi; izleyicinin kullanacağı araç değil. · sınıf: diğer
- https://www.isanurdogdu.com/bugun-baslasaydim/2-claude-code-ve-codex — Taslak dosyanın indirileceği sayfa · aday: hayır · Kişisel site sayfası; kaynak sayfa, araç değil. · sınıf: diğer
- https://app.notion.com/p/bug-n-ba-lasayd-m-2-3e2eed8342d980ffa13ec58d7e211b67?source=copy_link — Notion taslak sayfası · aday: evet (Notion) · Alan adı Notion'ı adlandırıyor; taslak indirmek için kullanılan servis. · sınıf: diğer
- https://www.youtube.com/watch?v=oEnVigmlHPA&list=PLNRUkhedZiRQ — Bu videonun YouTube bağlantısı (oynatma listesiyle) · aday: hayır · Videonun kendisi; referans bağlantı. · sınıf: diğer
- https://www.youtube.com/watch?v=oEnVigmlHPA&list=PLNRUkhedZiRQ&t=0s — Bölüm zaman damgası 0:00 · aday: hayır · Videonun kendi bölüm bağlantısı; referans. · sınıf: diğer
- https://www.youtube.com/watch?v=oEnVigmlHPA&list=PLNRUkhedZiRQ&t=70s — Bölüm zaman damgası 1:10 · aday: hayır · Videonun kendi bölüm bağlantısı; referans. · sınıf: diğer
- https://www.youtube.com/watch?v=oEnVigmlHPA&list=PLNRUkhedZiRQ&t=139s — Bölüm zaman damgası 2:19 · aday: hayır · Videonun kendi bölüm bağlantısı; referans. · sınıf: diğer
- https://www.youtube.com/watch?v=oEnVigmlHPA&list=PLNRUkhedZiRQ&t=245s — Bölüm zaman damgası 4:05 · aday: hayır · Videonun kendi bölüm bağlantısı; referans. · sınıf: diğer
- https://www.youtube.com/watch?v=oEnVigmlHPA&list=PLNRUkhedZiRQ&t=433s — Bölüm zaman damgası 7:13 · aday: hayır · Videonun kendi bölüm bağlantısı; referans. · sınıf: diğer
- https://www.youtube.com/watch?v=oEnVigmlHPA&list=PLNRUkhedZiRQ&t=543s — Bölüm zaman damgası 9:03 · aday: hayır · Videonun kendi bölüm bağlantısı; referans. · sınıf: diğer
- https://www.youtube.com/watch?v=oEnVigmlHPA&list=PLNRUkhedZiRQ&t=718s — Bölüm zaman damgası 11:58 · aday: hayır · Videonun kendi bölüm bağlantısı; referans. · sınıf: diğer
- https://www.youtube.com/watch?v=oEnVigmlHPA&list=PLNRUkhedZiRQ&t=867s — Bölüm zaman damgası 14:27 · aday: hayır · Videonun kendi bölüm bağlantısı; referans. · sınıf: diğer
- https://www.youtube.com/watch?v=oEnVigmlHPA&list=PLNRUkhedZiRQ&t=1022s — Bölüm zaman damgası 17:02 · aday: hayır · Videonun kendi bölüm bağlantısı; referans. · sınıf: diğer
- https://www.isanurdogdu.com — Yayıncının ana sitesi · aday: hayır · Kişisel site; referans bağlantı. · sınıf: diğer
- https://www.isanurdogdu.com/#kur — Sitedeki 'kur' bölümü bağlantısı · aday: hayır · Sayfa içi referans bağlantı. · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| /proje-hafızası | Claude Code'da proje-hafızası skill'ini çalıştırır; hafızayı güncelleme, bağlamı denetleme veya kaynakları denetleme yapar. | 14:00 | altyazı |
| /project:fix-issue | Slaytta özel slash komut örneği olarak gösteriliyor; bu videoda çalıştırılmıyor. (karede: Slaytta '/project:fix-issue' komut örneği ve .claude/commands/ klasörü görünüyor.) | 0:12 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Sorun modelde değil, projenin temel dosyalarının yanlış kurulmasındadır. | 0:00 | özellik |
| Ajan açıldığında ilk CLAUDE.md'yi (Codex'te AGENTS.md'yi) okur; ek klasörler talimat olmadan okunmaz. | 3:20 | özellik |
| README haritası ile yalnızca gereken dosyalar okunur, bu da token israfını önler. | 6:07 | öneri |
| Her oturum sonunda 'hafızayı güncelle' demek, ertesi gün kaldığı yerden devam etmeyi sağlar. | 12:59 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Claude Code | Claude Code | Cloud Code veya Codex'te bir projeye başladığınızda |
| konuşma 0:00 | Codex | Codex | Cloud Code veya Codex'te bir projeye başladığınızda |
| konuşma 0:00 | Antigravity | Antigravity | İster cloud code ister Codex ister antigravity kullanıyor olun |
| konuşma 2:19 | CLAUDE.md | CLAUDE.md | Cloud MD'yi okuyor |
| konuşma 2:19 | AGENTS.md | AGENTS.md | Hem Agents var hem cloud MD var |
| konuşma 4:05 | context klasörü | context/README.md | Contexte bizim hafızamız, bağlamımız |
| konuşma 8:13 | Skill kavramı | proje-hafızası | ihtiyaç duyduğumuzda tetiklenen çok adımlı iş akışları |
| kare 13:26 | proje-hafızası skill | proje-hafızası | SKILL.md name: proje-hafızası |
| konuşma 8:13 | MCP | aday değil: genel kavram | MCP, ajan, plan, output gibi dosyalar açmalı mıyım? Şu anlık açmayacağız |
| konuşma 7:13 | OpenAI / Anthropic | aday değil: genel kavram | Open A'in Antropy'in yayınladığı resmi kaynaklara |
| kare 0:26 | Miro | Miro | miro.com/app/board adres çubuğunda |
| kare 3:06 | Visual Studio Code | Visual Studio Code | File Edit Selection View Go Run Terminal Help |
| kare 0:30 | Fable 5.1 | Fable 5.1 | Favorite model Fable 5.1 |
| kare 13:38 | Opus 5 Fast | Opus 5 Fast | Opus 5 Fast Medium |
| kare 16:24 | GPT-5.6 Sol | GPT-5.6 Sol | GPT-5.6 Sol Yüksek |
| kare 0:12 | .claude klasör anatomisi şeması | aday değil: konu dışı | Anatomy of the .claude/ folder görseli |
| kare 13:42 | vercel, humanizer, cold-email, design-consent skill listesi | aday değil: konu dışı | Slash menüsünde yalnız listelendi, kullanılmadı |
| kare 14:22 | Photoshop, Not Defteri, Antigravity IDE uygulama seçici | aday değil: konu dışı | Bu uygulama dosyasını açmak için .txt seçin |
| kare 14:22 | Not Defteri | aday değil: konu dışı | ILK-PROMPT.txt açma penceresinde listelendi |
| kare 16:08 | Bun, Cursor klasörleri | aday değil: konu dışı | Klasör seçim penceresinde .bun, .cursor görünüyor |
| açıklama | Notion taslak sayfası | Notion | app.notion.com bağlantısı |
| açıklama | YouTube oynatma listesi | aday değil: konu dışı | youtube.com/playlist bağlantısı |
| açıklama | isanurdogdu.com taslak sayfası | aday değil: konu dışı | Taslak indirme sayfası, referans |
| yorum | Obsidian, Hermes Agent, DeepSeek, CRM | aday değil: konu dışı | İzleyici yorumlarında geçiyor, videoda anlatılmıyor |
| konuşma 16:28 | ILK-PROMPT.txt | ILK-PROMPT.txt | ilk prompt diye bir txt dosyası var |
## Kareden okunanlar
- 0:12: Anatomy of the .claude/ folder şeması: CLAUDE.md, CLAUDE.local.md, settings.json, commands/, rules/
- 0:26: Miro şeması: Prompt → Claude Code / Codex → CLAUDE.md ← AGENTS.md → context/README.md → ilgili bağlam dosyaları → kaynak indeksi ve görev
- 1:59: Her dosyanın farklı bir işi var: CLAUDE.md, AGENTS.md, context/, skill
- 2:18: benim projem klasörü: .agents, .claude, context, AGENTS.md, CLAUDE.md, ILK-PROMPT.txt
- 5:46: README tablosu: proje-ozeti.md, hedefler.md, kurallar-ve-sinirlar.md, kararlar.md, kaynaklar dosyaları
- 6:44: Kaynak sistemi: belgeler/, veriler/, gorseller/, ses-ve-video/, baglantilar.md, kaynak-indeksi.md
- 13:26: SKILL.md: proje-hafızası; Hafızayı güncelleme, Bağlamı denetleme, Kaynakları denetleme
- 16:24: Codex Proje oluştur penceresi; GPT-5.6 Sol Yüksek modeli
## Belirsizlikler
- Altyazıdaki 'Tastak' ifadesi büyük olasılıkla 'taslak'; sözlükteki TanStack Query eşleşmesi yanlış, aday yapılmadı.
- 'Cloud MD / Cloud Code' ifadeleri otomatik altyazı hatası; Claude olarak yorumlandı.
- Kare listesinde 'Fable 5.1', 'Opus 5 Fast' model adları ekran OCR'ından alındı; gerçek sürüm adları doğrulanamadı.
- Ekranda yalnızca görünen Next.js, Descript, Vercel, humanizer, cold-email, Cursor, Bun, Kimi, Photoshop gibi öğeler menü/listede göründü, videoda kullanılmadı.
- Yorumlardaki Obsidian, Hermes Agent, DeepSeek, CRM sistemi izleyici yorumu; videoda anlatılmadı.
- Notion bağlantısı erişilmedi; içeriği doğrulanamadı.
## Atlanan segment oranı
0/23 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.youtube.com/playlist?list=PLNRUkhedZiRQ | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=oEnVigmlHPA&list=PLNRUkhedZiRQ | açıklama | açıklama | hayır |
| https://www.isanurdogdu.com/bugun-baslasaydim/2-claude-code-ve-codex | açıklama | açıklama | hayır |
| https://app.notion.com/p/bug-n-ba-lasayd-m-2-3e2eed8342d980ffa13ec58d7e211b67?source=copy_link | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=oEnVigmlHPA&list=PLNRUkhedZiRQ&t=0s | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=oEnVigmlHPA&list=PLNRUkhedZiRQ&t=70s | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=oEnVigmlHPA&list=PLNRUkhedZiRQ&t=139s | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=oEnVigmlHPA&list=PLNRUkhedZiRQ&t=245s | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=oEnVigmlHPA&list=PLNRUkhedZiRQ&t=433s | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=oEnVigmlHPA&list=PLNRUkhedZiRQ&t=543s | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=oEnVigmlHPA&list=PLNRUkhedZiRQ&t=718s | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=oEnVigmlHPA&list=PLNRUkhedZiRQ&t=867s | açıklama | açıklama | hayır |
| https://www.youtube.com/watch?v=oEnVigmlHPA&list=PLNRUkhedZiRQ&t=1022s | açıklama | açıklama | hayır |
| https://www.isanurdogdu.com | açıklama | açıklama | hayır |
| https://www.isanurdogdu.com/#kur | açıklama | açıklama | hayır |
| https://miro.com/app/board/uXjVHkvX9UM=/ | 0:26 | ekran | hayır |
| https://www.isanurdogdu.com/bugun-baslasaydim/2-claude-code-ve-codex | - | yorum | hayır |
| https://app.notion.com/p/bug-n-ba-lasayd-m-2-3e2eed8342d980ffa13ec58d7e211b67?source=copy_link | - | yorum | hayır |
## İş akışı
- 1. adım — Tek CLAUDE.md'ye her şeyi yığmanın sorununu göstermek — araçlar: Claude Code
- 2. adım — Ana talimat dosyası CLAUDE.md'yi incelemek — araçlar: Visual Studio Code, CLAUDE.md
- 3. adım — Codex için AGENTS.md dosyasını CLAUDE.md'ye yönlendirecek şekilde hazırlamak — araçlar: Codex, AGENTS.md
- 4. adım — context/ klasörünü ve README.md ana haritasını incelemek — araçlar: context/README.md, Visual Studio Code
- 5. adım — Hedefler, kararlar, kurallar ve proje özeti dosyalarını haritaya göre incelemek — araçlar: context/README.md, Visual Studio Code
- 6. adım — Kaynak sistemini (kaynaklar/ klasörü, kaynak indeksi) açıklamak — araçlar: Windows Dosya Gezgini, Visual Studio Code
- 7. adım — proje-hafızası skill'ini .claude/skills altına yerleştirmek — araçlar: .claude/ klasörü, proje-hafızası, Windows Dosya Gezgini
- 8. adım — Şablon klasörü indirip ILK-PROMPT.txt dosyasını Not Defteri'nde açmak — araçlar: Windows Dosya Gezgini, Not Defteri
- 9. adım — Claude Code'da proje klasörünü seçip ilk promptu vermek; ajanın keşif sorularını yanıtlamak — araçlar: Claude Code, Opus 5 Fast
- 10. adım — Codex'te proje oluşturup aynı klasörü bağlamak — araçlar: Codex, GPT-5.6
- 11. adım — CLAUDE.md'nin projeye özel bölümünü güncelleyip değişiklikleri kontrol etmek — araçlar: Claude Code, CLAUDE.md
- 12. adım — context/ dosyalarını projeye özel içerikle doldurmak ve README haritasını güncellemek — araçlar: Claude Code, context/README.md
- 13. adım — Sohbet sonunda /proje-hafızası ile hafızayı güncellemek — araçlar: Claude Code, proje-hafızası
- 14. adım — Bağlamı ve kaynakları denetleyip projeyi kapatıp yarın kaldığın yerden devam etmek — araçlar: Claude Code, proje-hafızası
## Promptlar
- Taslak projeyi kullanıcının kendi projesine uyarlatmak — Projeyi incele; CLAUDE.md, AGENTS.md ve context/README.md dosyalarını oku, yönlendirilen bağlam dosyalarını incele. Evrensel kuralları ve bölüm sırasını koru, yalnızca projeye özel kalıcı talimatlar bölümünü güncelle, AGENTS.md ve skill dosyalarını değiştirme. Yalnızca doğrulanabilir bilgi yaz, hedef/kural/komut tahmin etme, eksik kritik bilgileri kısa sorularla sor, cevaplardan sonra değişiklikleri kısaca açıkla.
- Oturum sonunda proje hafızasını güncellemek — /proje-hafızası komutuyla hafızayı güncelle, bağlamı denetle veya kaynakları denetle.
ikinci göz KAPALI: --ikinci-goz yok
