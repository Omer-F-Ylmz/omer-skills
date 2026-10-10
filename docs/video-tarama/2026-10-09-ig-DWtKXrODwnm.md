# Yoruma "claude" yaz, eğitim videosunu DM'den göndereyim ⚡️
## Künye
Yoruma "claude" yaz, eğitim videosunu DM'den göndereyim ⚡️ · isanurdogdu · süre: 1:02 · ? · https://www.instagram.com/reel/DWtKXrODwnm/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-30 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 51692 tk · claude-haiku-5-5: claude-haiku-5-5 · 44800 tk
## Özet
Kısa reel: Claude Code, bilgisayarda yaşayan dijital bir çalışan olarak anlatılıyor. İki örnek var: toplantı notlarından teklif hazırlama (Fireflies, Gmail ile gönderme) ve Dallas sigorta ajanslarını bulup e-posta toplama, araştırma ve kişiselleştirilmiş mesaj yazma. Sonda pr-description skill'i, git komutları ve 6 seviyeli eğitim müfredatı görünüyor. Yoruma 'claude' yazana eğitim DM ile gönderiliyor.
## Bölümler
- 0:00 Claude Code dijital çalışan benzetmesi
- 0:21 Toplantı notlarından teklif hazırlama
- 0:37 Sigorta ajanslarını bulma ve kişisel mesaj yazma
- 0:47 Skill örneği: pr-description
- 0:56 6 seviyeli eğitim müfredatı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Code | yok | CLI | yok | Terminalde çalışan, sade dille verilen görevleri baştan sona yapan yapay zekâ ajanı; videonun ana aracı. | 0:00 | İşte Cloud Code tam olarak bu. İhtiyacın olanı sade Türkçe ile söylüyorsun |
| Fireflies | yok | MCP | yok | Toplantı özet ve transkriptlerini Claude'a getiren bağlayıcı; teklif hazırlamada kullanıldı. | 0:27 | Ekran metni: Claude Al Fireflies [fireflies_get_summary], [fireflies_get_transcript] (karede: kanıttan) Ekran metni: Claude Al Fireflies [fireflies_get_summary], [fireflies_get_transcript] |
| Gmail | yok | MCP | yok | Hazırlanan teklifi e-posta olarak göndermek için gösterilen seçenek. | 0:29 | Ekran metni 'Send via Gmall'; konuşmada 'hatta gönderiyor' |
| Web Fetch | yok | teknik | yok | Claude Code'un web sayfası çekme aracı; ajans bilgisi toplamada kullanıldı. | 0:40 | Karede Web Fetch voyagedallas.com satırı görünüyor (karede: Web Fetch voyagedallas.com/interview/meet-susana-gibb-of-gibb-insurance-services/ satırı ve 'Fetched from' çıktısı) |
| AskUserQuestion | yok | teknik | yok | Claude Code'un görev sırasında kullanıcıya soru sorma aracı. | 0:40 | Karede AskUserQuestion başlığı ve yanıtlanan soru görünüyor (karede: AskUserQuestion başlığı, altında 'User has answered your questions: what product or service...' satırı) |
| pr-description | yok | skill | yok | Pull request açıklaması yazan, /pr-description ile çağrılan skill örneği. | 0:47 | Ekran metni: SKILL.md, pr-description, Skill: /pr-description (karede: kanıttan) Ekran metni: SKILL.md, pr-description, Skill: /pr-description |
| Git | yok | CLI | yok | PR açıklaması için git diff ve git log komutları çalıştırıldı. | 0:55 | Ekran metni: Bash(git diff master...HEAD), Bash(git branch -a && git log --oneline -10) (karede: kanıttan) Ekran metni: Bash(git diff master...HEAD), Bash(git branch -a && git log --oneline -10) |
| Lucide | yok | teknik | yok | Prompt metninde geçen ikon kütüphanesi; videoda yalnız prompt içinde anılıyor. | 0:17 | Use Lucide (karede: OCR (ekran metni): prompt satırında 'Use Lucide' ifadesi) |
| Bash | yok | teknik | yok | Claude Code'un kabuk komutu çalıştıran aracı; git komutları bu araçla çalıştırılıyor. | 0:55 | Bash(git branch -a && git log --oneline -10) (karede: OCR (ekran metni): 'Bash(git branch -a && git log --oneline -10)' çağrı satırı) |
| Toplantı notlarından teklif hazırlama | yok | prompt | yok | Son toplantı notlarımı al ve bir teklif hazırla; keşif aşaması ayrıntıları ve fiyatlandırmayı içersin, abonelik uygulaması özelliklerini ve teknik kapsamı özetlesin. | 0:21 | kaynak: kare |
| Potansiyel müşteri bulma ve kişiselleştirilmiş mesaj yazma | yok | prompt | yok | Dallas'taki sigorta acentelerini bul, e-postalarını topla, her biri hakkında araştır ve her birine kişiselleştirilmiş mesaj yaz. | 0:37 | kaynak: kare |
## Açıklama bağlantıları
- https://www.gibbagencydallas.com — Susana Gibb'in sigorta acentesi sitesi · aday: hayır · Referans sayfa; izleyicinin kullanacağı bir araç değil. · sınıf: diğer
- https://www.youtube.com/@SusanaGibbShow — Susana Gibb'in YouTube kanalı · aday: hayır · Referans kanal; araç değil. · sınıf: diğer
- https://www.susanagibb.com — Susana Gibb'in kişisel sitesi · aday: hayır · Referans sayfa; araç değil. · sınıf: diğer
- https://voyagedallas.com/interview/meet-susana-gibb-of-gibb-insurance-services — Röportaj sayfası; Web Fetch ile çekilen veri kaynağı. · aday: hayır · Veri kaynağı sayfa; izleyicinin kullanacağı araç değil. · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| /pr-description | PR açıklaması yazan skill'i çalıştırır. (karede: (karede OCR) auth.py — fastapi-project :del * Available Skills The following skills are available for invocation: Skill: /documentation Description: Writes documentation - READMEs, API docs, code cep documentation) | 0:53 | kare |
| git diff master...HEAD | Dal değişikliklerini gösterir. (karede: (karede OCR) auth.py — fastapi-project del PR Description Writing to separate paths from revisions, like this: Use'-' 'git <command> [<revision>...] - [<file>...] Bash(git branch -a && git log --oneline -10) cep m) | 0:55 | kare |
| git branch -a && git log --oneline -10 | Dalları ve son 10 commit'i listeler. (karede: (karede OCR) auth.py — fastapi-project del PR Description Writing to separate paths from revisions, like this: Use'-' 'git <command> [<revision>...] - [<file>...] Bash(git branch -a && git log --oneline -10) cep m) | 0:55 | kare |
| /model | Model seçimi için ipucu olarak gösterilir. (karede: (karede OCR) *Claude Code Type /model to pick the right tool for the job. > take my latest meeting notes and make a proposal / Ask before edits Mesela bir) | 0:21 | kare |
| /mobile | Claude'u telefonda kullanma ipucu. (karede: (karede OCR) auth.py — fastapi-project del PR Description Writing to separate paths from revisions, like this: Use'-' 'git <command> [<revision>...] - [<file>...] Bash(git branch -a && git log --oneline -10) cep m) | 0:55 | kare |
| git diff main...HEAD | Ana dal ile mevcut dal arasındaki değişiklikleri gösterir. (karede: OCR (ekran metni): pr-description yönergesinde komut satırı) | 0:50 | kare |
| /commit | Commit mesajı yazan skill'in sohbetteki komutu; ekranda örnek olarak anılıyor. (karede: OCR (ekran metni): 'type the command (e.g., /commit)' ifadesi) | 0:53 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Claude Code, süreç adımları verilince işi baştan sona otomatik yapar; teknik bilgi gerekmez. | 0:00 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Claude Code | Claude Code | Ana araç olarak anlatılıyor |
| kare 0:27 | Fireflies | Fireflies | fireflies_get_summary araçları |
| kare 0:29 | Gmail | Gmail | Send via Gmall |
| kare 0:40 | Web Fetch | Web Fetch | Web Fetch satırı |
| kare 0:40 | AskUserQuestion | AskUserQuestion | Soru-cevap bloğu |
| kare 0:40 | voyagedallas.com sayfası | aday değil: başka adayın parçası (Web Fetch) | Web Fetch ile çekilen kaynak |
| kare 0:41 | brookscannon.com | aday değil: konu dışı | Örnek ajans e-postası |
| kare 0:43 | vanguardinsgroup.com | aday değil: konu dışı | Örnek ajans e-postası |
| bağlantılı sayfa | gibbagencydallas.com, susanagibb.com, youtube.com/@SusanaGibbShow | aday değil: konu dışı | Voyage Dallas röportaj sayfasındaki bağlantılar |
| kare 0:47 | pr-description skill | pr-description | SKILL.md içeriği |
| kare 0:55 | Git | Git | git diff ve git log komutları |
| açıklama | Yoruma 'claude' yaz DM eğitim | aday değil: sponsor/reklam | Eğitim videosu tanıtımı |
| kare 0:56 | 6 seviye müfredat (Kurulum, Bağlam, MCP, Agent Teams) | aday değil: konu dışı | Eğitim içerik listesi |
## Kareden okunanlar
- 0:40: Claude Code çıktısı: Web Fetch, Update Todos, AskUserQuestion, Write dallas_insurance_agents_outreach.md (161 lines); üstte 'Veri' yazısı.
- 0:41: Markdown dosyası: Brooks Cannon için e-posta, telefon, adres ve kişiselleştirilmiş mesaj; üstte 'zenginleştirme' yazısı.
- 0:43: Vanguard Insurance Group bölümü ve mesaj taslağı, Summary Table başlığı; üstte 'yapıyor' yazısı.
## Belirsizlikler
- Altyazıda 'Cloud Code' geçiyor, ekranda Claude Code; Claude Code kabul edildi.
- Sözlük eşleşmeleri (Codex, Veo, Exa, Make, Inter, Hermes Agent, Descript, Astro vb.) videoda kullanılmıyor, OCR gürültüsü; aday yapılmadı.
- Gmail'in MCP mi başka yol mu olduğu belirsiz.
- Dil alanı belirsiz; konuşma Türkçe.
- Yorumlar girişsiz alınamadı.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://voyagedallas.com/interview/meet-susana-gibb-of-gibb-insurance-services/ | 0:40 | ekran | hayır |
| brookscannon.com | 0:41 | ekran | hayır |
| vanguardinsgroup.com | 0:43 | ekran | hayır |
| https://www.gibbagencydallas.com | açıklama | açıklama | hayır |
| https://www.youtube.com/@SusanaGibbShow | açıklama | açıklama | hayır |
| https://www.susanagibb.com | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — Claude Code'a toplantı notlarından teklif hazırlama görevi verilir — araçlar: Claude Code
- 2. adım — Fireflies'tan toplantı özeti ve transkript çekilir — araçlar: Fireflies
- 3. adım — Teklif hazırlanır ve Gmail ile gönderme gösterilir — araçlar: Claude Code, Gmail
- 4. adım — Dallas sigorta acentelerini bulma görevi yazılır — araçlar: Claude Code
- 5. adım — Web sayfaları çekilir ve ajans bilgileri toplanır — araçlar: Web Fetch
- 6. adım — Claude kullanıcıya teklif edilen ürünü sorar — araçlar: AskUserQuestion
- 7. adım — Kişiselleştirilmiş mesajlar markdown dosyasına yazılır — araçlar: Claude Code
- 8. adım — pr-description skill'i gösterilir ve çağrılır — araçlar: Claude Code, pr-description
- 9. adım — Skill git diff ve git log çalıştırır — araçlar: Git
## Promptlar
- Toplantı notlarından teklif hazırlama — Son toplantı notlarımı al ve bir teklif hazırla; keşif aşaması ayrıntıları ve fiyatlandırmayı içersin, abonelik uygulaması özelliklerini ve teknik kapsamı özetlesin.
- Potansiyel müşteri bulma ve kişiselleştirilmiş mesaj yazma — Dallas'taki sigorta acentelerini bul, e-postalarını topla, her biri hakkında araştır ve her birine kişiselleştirilmiş mesaj yaz.
