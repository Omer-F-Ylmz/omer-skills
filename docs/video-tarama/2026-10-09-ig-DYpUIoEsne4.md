# Yorumlara "Gönder" yaz, sana da rehberi ileteyim.🤝
## Künye
Yorumlara "Gönder" yaz, sana da rehberi ileteyim.🤝 · yasin.arsal · süre: 0:52 · ? · https://www.instagram.com/reel/DYpUIoEsne4/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-32 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 26591 tk · claude-haiku-5-5: claude-haiku-5-5 · 28361 tk
## Özet
Kısa reel: Claude Code her yeni oturumda kod tabanını yeniden okuyup token harcıyor. Anlatıcı, Graphify adlı aracın kod tabanından bir bilgi grafiği (knowledge graph) çıkardığını, sonraki oturumlarda Claude'un dosyaları okumak yerine grafiği kullandığını ve token kullanımının yaklaşık 70 kat (açıklamada 71,5 kat) azaldığını söylüyor. Açıklamada ayrıca CLAUDE.md'ye talimat eklemek ve grafiği Obsidian'da 3B görselleştirmek öneriliyor. Rehber için yorumlara 'Gönder' yazılması isteniyor.
## Bölümler
- 0:00 Giriş: token sorunu ve Pro/Max plan iddiası
- 0:10 Yeni oturumda kod tabanının yeniden okunması
- 0:25 Graphify tanıtımı
- 0:38 Bilgi grafiği ve sonraki oturumlar
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Graphify | yok | skill | yok | Kod tabanını bir kez tarayıp knowledge graph oluşturan Claude Code skill'i; sonraki oturumlarda Claude grafiği sorguluyor. | 0:25 | OCR 0:25'te 'Graphify' yazıyor; açıklamada Graphify skill'i anlatılıyor. |
| Claude Code | yok | CLI | yok | Her oturumda kod tabanını yeniden okuyan, sorunun kaynağı olan kodlama aracı. | 0:11 | Kare 0:11'de altyazı 'yeni bi Claude Code oturumu başlattığınızda'; OCR'da Claude Code arayüzü görülüyor. (karede: Claude uygulaması arayüzü: Chats, Projects, Ask Claude, Artifacts menüsü ve 'Here's the thing' yazısı.) |
| CLAUDE.md | yok | ipucu | yok | Claude'a önce knowledge graph'ı sorgulamasını söyleyen talimatların eklendiği dosya. | açıklama | Açıklamada CLAUDE.md dosyasına birkaç satır eklemek öneriliyor. |
| Obsidian | yok | CLI | yok | Graph'ı 3B görselleştirmek için bonus olarak önerilen not uygulaması. | açıklama | Açıklamada graph'ı Obsidian'da 3D görselleştirme bonusu geçiyor. |
| Claude Pro planı | yok | ipucu | yok | 20 dolarlık plan; anlatıcıya göre Graphify ile Max plan kadar iş yapılabilir. | 0:05 | Kare 0:05'te Pro planı fiyat kartı ve altyazı görülüyor. · kanıt: kare (karede: Pro planı kartı: $20 USD/month, Get Pro plan düğmesi; altyazı '20$'lık Pro planınızla 100$'lık Max planın'.) |
| Git | yok | CLI | yok | Sürüm kontrol aracı; Claude Code ekranında 'git add' komutu görüldü. | 0:19 | git add src/rgutes/a (karede: OCR ekran metni: terminalde 'git add src/...' komutu (kare görseli gönderilmedi).) |
| sharp | yok | teknik | yok | Node.js görüntü işleme kütüphanesi; Claude Code değişiklik özetinde avatar için WebP dönüşümü yapıldığı görüldü. | 0:18 | imported sharp. made the avatar handler async, added webP conversion (karede: OCR ekran metni: Claude Code değişiklik özetinde '3. src/routes/auth.ts - imported sharp' satırı.) |
| Graphify sonrası Claude'ı graph'ı önce kullanmaya yönlendirmek (CLAUDE.md talimatı) | yok | prompt | yok | Claude'a önce knowledge graph'ı sorgulamasını, ham dosyaları ise yalnızca kullanıcı açıkça isterse okumasını söyleyen birkaç satırlık talimat. | açıklama | kaynak: açıklama |
| Claude Code oturumunda belirli bir dizini hariç tutma isteği | yok | prompt | yok | web/ dizininin hariç tutulmasını isteyen kısa bir talimat (OCR ile kısmen okundu). | 0:18 | kaynak: kare |
## Açıklama bağlantıları
- yok
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Graphify ile token kullanımı yaklaşık 70 kat azalıyor (açıklamada 71,5 kat). | 0:43 | sayısal |
| Pro plan ile Max planın yaptıkları yapılabilir. | 0:00 | karşılaştırma |
| Her oturum başında 15-20 bin token kod tabanını okumaya gidiyor. | açıklama | sayısal |
| CLAUDE.md'ye talimat eklenmezse Claude eski alışkanlığına dönüyor. | açıklama | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Claude Code | Claude Code | Token sorunu anlatılıyor. |
| kare 0:05 | Pro plan fiyat kartı | Claude Pro planı | $20 USD/month Pro kartı görülüyor. |
| kare 0:05 | Max planı | aday değil: genel kavram | Altyazıda 100$'lık Max plan geçiyor, gösterilmiyor. |
| kare 0:17 | Claude Code terminal (Bash, Explore, /effort) | Claude Code | OCR'da Bash ve Explore satırları var. |
| kare 0:17 | JavaScript | aday değil: konu dışı | Sadece ekran görüntüsünde dosya deseni olarak geçiyor. |
| kare 0:18 | TypeScript | aday değil: konu dışı | Ekrandaki dosya adında src/routes/auth.ts geçiyor. |
| kare 0:19 | Git | aday değil: konu dışı | Ekranda git add komutu geçiyor, anlatılmıyor. |
| kare 0:25 | Graphify | Graphify | Ekranda Graphify yazıyor. |
| kare 0:38 | Bilgi grafiği çıkarma (EXTRACT) | Graphify | OCR'da [EXTRACT ve calls geçiyor. |
| açıklama | CLAUDE.md | CLAUDE.md | Talimat ekleme önerisi. |
| açıklama | Obsidian | Obsidian | 3B görselleştirme bonusu. |
| açıklama | Andrej Karpathy / vibe coding | aday değil: konu dışı | Sorunu paylaşan kişi olarak anılıyor. |
| konuşma 0:00 | GitHub | aday değil: konu dışı | GitHub linki yorumlara isteniyor. |
## Kareden okunanlar
- 0:05: Pro planı kartı: $20 USD/month, altyazı '20$'lık Pro planınızla 100$'lık Max planın'.
- 0:10: Claude ana ekranı 'Hey there, Elliot', altyazı 'bakın şöyle bi durum var'.
- 0:11: Claude menüsü (Chats, Projects, Ask Claude, Artifacts), altyazı 'yeni bi Claude Code oturumu başlattığınızda'.
## Belirsizlikler
- Graphify'ın kurulum komutu ve repo adresi videoda verilmiyor; GitHub linki yorumla isteniyor.
- Videoda 70 kat, açıklamada 71,5 kat deniyor.
- Yorumlar girişsiz alınamadı.
- Altyazıda 'Graphifier'ındaki' ve 'CloudArt' gibi hatalı transkripsiyonlar var; Graphify ve Claude kastediliyor olabilir.
- Ses sözlüğündeki Codex ve Hermes Agent eşleşmeleri bulanık, videoda anlatılmıyor.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
- yok
## İş akışı
- 1. adım — Graphify'ı Claude Code'a kur — araçlar: Graphify, Claude Code
- 2. adım — Graphify'ı bir kez çalıştırıp kod tabanını tara ve bilgi grafiği oluştur — araçlar: Graphify
- 3. adım — CLAUDE.md'ye önce grafiği sorgulama talimatı ekle — araçlar: CLAUDE.md, Claude Code
- 4. adım — Sonraki oturumlarda Claude grafiği sorgulasın — araçlar: Claude Code, Graphify
- 5. adım — İsteğe bağlı: grafiği Obsidian'da 3B görselleştir — araçlar: Obsidian
## Promptlar
- Graphify sonrası Claude'ı graph'ı önce kullanmaya yönlendirmek (CLAUDE.md talimatı) — Claude'a önce knowledge graph'ı sorgulamasını, ham dosyaları ise yalnızca kullanıcı açıkça isterse okumasını söyleyen birkaç satırlık talimat.
- Claude Code oturumunda belirli bir dizini hariç tutma isteği — web/ dizininin hariç tutulmasını isteyen kısa bir talimat (OCR ile kısmen okundu).
ikinci göz KAPALI: --ikinci-goz yok
