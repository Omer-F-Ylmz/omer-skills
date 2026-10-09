# Yorumlara «MIRO» yaz, bütün Miro board’larını Claude’a bağlayan MCP’yi göndereyi
## Künye
Yorumlara «MIRO» yaz, bütün Miro board’larını Claude’a bağlayan MCP’yi göndereyi · theakselege · süre: 0:50 · ? · https://www.instagram.com/reel/DcRLpCbKd7w/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-23 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 14578 tk · claude-haiku-5-5: claude-haiku-5-5 · 30744 tk
## Özet
Video, Miro'nun yayınladığı resmi MCP sunucusunu tanıtıyor. MCP, Miro board'larını Claude'a bağlıyor. Claude board'ları okuyabiliyor, içlerinde arama yapabiliyor, yenilerini oluşturabiliyor, yapışkan notları planlara dönüştürebiliyor ve ekip yorumlarına göre hareket edebiliyor. Anlatıcı 80 yapışkan notlu bir board'u aktarıp sahipli ve zaman çizelgeli öncelik listesini dakikalar içinde almış. Toplantı sonrası özet, aksiyon maddeleri ve proje planı kullanım senaryosu olarak gösteriliyor. Videoda Claude Code terminalinde /miro-mcp:code_explain_on_board komutu çalışıyor.
## Bölümler
- 0:00 Miro MCP'nin tanıtımı ve Miro nedir
- 0:14 Miro MCP Server izin ekranı
- 0:19 Claude Code'da code_explain_on_board komutu
- 0:25 Claude'un yapabilecekleri: okuma, arama, oluşturma, yorumlar
- 0:35 80 notluk board'dan öncelik listesi (OKR tablosu)
- 0:41 Toplantı senaryosu: aksiyon maddeleri ve proje planı
- 0:46 Yorumlara «MIRO» yazma çağrısı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Miro MCP Server | yok | MCP | yok | Miro'nun resmi MCP sunucusu; board'ları Claude'a bağlar, okuma, arama, oluşturma ve düzenleme sağlar. | 0:14 | Ekran metni: Add & allow "Miro MCP Server"; Developed and maintained by Miro. (karede: kanıttan) Ekran metni: Add & allow "Miro MCP Server"; Developed and maintained by Miro. |
| Miro | yok | iş akışı | yok | Görsel işbirliği platformu; board'larda beyin fırtınası, akış şeması ve strateji planlama yapılır. | 0:00 | Miro'yu hiç kullanmadıysan şirketlerin ... görsel işbirliği platformudur. |
| Claude | yok | CLI | yok | Miro MCP'nin bağlandığı ana yapay zekâ aracı; board'ları okur ve planlar üretir. | 0:00 | Miro, sahip olduğun her board'u Claude'a bağlamanın bir yolunu geliştirdi. |
| Claude Code | yok | CLI | yok | Terminalde MCP komutunun çalıştırıldığı Claude komut satırı aracı. | 0:19 | Terminalde ipucu: Run claude --continue or claude --resume. · kanıt: kare (karede: Terminalde ipucu: Run claude --continue or claude --resume.) |
| Miro AI | yok | teknik | yok | Miro MCP'nin diyagram oluşturma gibi eylemlerde kullandığı Miro yapay zekâ kredileri. | 0:14 | Ekran metni: Miro MCP leverages Miro AI; credits to perform certain actions. (karede: kanıttan) Ekran metni: Miro MCP leverages Miro AI; credits to perform certain actions. |
| code_explain_on_board | yok | prompt | yok | Miro MCP'nin kodu board üzerinde görsel diyagramlarla açıklayan slash komutu. | 0:19 | Terminal: /miro-mcp:code_explain_on_board (MCP) is running. (karede: kanıttan) Terminal: /miro-mcp:code_explain_on_board (MCP) is running. |
| Strategy Sidekick | yok | teknik | yok | Miro board'unda OKR tablosu üzerinde görünen Sidekick (yapay zekâ yardımcısı) etiketi. | 0:35 | Tabloda imleç etiketi # Strategy Sidekick görünüyor. (karede: kanıttan) Tabloda imleç etiketi # Strategy Sidekick görünüyor. |
| Yapışkan not kaosunu öncelik listesine dönüştürme | yok | prompt | yok | 80 yapışkan notlu beyin fırtınası board'unu analiz edip sahipleri ve zaman çizelgeleri olan sıralanmış bir öncelik listesi oluşturması istendi. | 0:35 | kaynak: altyazı |
| Kodu Miro board'unda görselleştirme | yok | prompt | yok | Claude'dan, verilen Miro board linkine yerel bilgisayardaki kodu açıklayan görsel diyagramlar oluşturması istendi. | 0:21 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| /miro-mcp:code_explain_on_board | Claude Code sohbetinde miro-mcp eklentisinin kod açıklama komutunu başlatır; kodu analiz edip Miro board'una diyagram çizdirir. (karede: Terminalde '/miro-mcp:code_explain_on_board (MCP) is running' satırı görünüyor.) | 0:19 | kare |
| claude --continue | Son Claude Code oturumunu kaldığı yerden devam ettirir (ekranda ipucu olarak gösteriliyor). (karede: Terminalde 'Tip: Run claude --continue or claude --resume to resume a conversation' ipucu satırı görünüyor.) | 0:19 | kare |
| claude --resume | Önceki Claude Code oturumlarından birini seçerek devam ettirir (ekranda ipucu olarak gösteriliyor). (karede: Terminalde 'claude --resume' ipucu metni görünüyor.) | 0:19 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Miro, sahip olunan tüm board'ları Claude'a bağlayan yeni bir MCP yayınladı. | 0:00 | özellik |
| Claude board'ları okuyabilir, arayabilir, yenilerini oluşturabilir, yapışkan notları planlara dönüştürebilir ve ekip yorumlarına göre hareket edebilir. | 0:25 | özellik |
| 80 yapışkan notlu board'dan sahipli ve zaman çizelgeli öncelik listesi dakikalar içinde alındı. | 0:35 | sayısal |
| Miro oturumu bittikten sonra Claude özet, aksiyon maddeleri ve proje planını hazır eder. | 0:41 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Miro | Miro | Miro'yu hiç kullanmadıysan ... görsel işbirliği platformudur. |
| konuşma 0:00 | Claude | Claude | Board'ları Claude'a bağlamanın bir yolu. |
| konuşma 0:00 | MCP | Miro MCP Server | Bunları doğrudan Claude'a bağlayan bir MCP yayınladılar. |
| kare 0:14 | Miro MCP Server izin ekranı | Miro MCP Server | Add & allow "Miro MCP Server" |
| kare 0:14 | Miro AI | Miro AI | Miro MCP leverages Miro AI. |
| kare 0:19 | /miro-mcp:code_explain_on_board | code_explain_on_board | Terminalde komut çalışıyor. |
| kare 0:19 | claude --continue / --resume ipucu | Claude Code | Tip: Run claude --continue or claude --resume. |
| kare 0:20 | https://miro.com/app/board/ örnek URL | aday değil: konu dışı | Örnek/maskeli board bağlantısı, araç değil. |
| kare 0:07 | Project Brief: Rome in a day belgesi | aday değil: konu dışı | Miro içinde örnek içerik. |
| kare 0:35 | Strategy Sidekick | Strategy Sidekick | Tabloda imleç etiketi görünüyor. |
| kare 0:35 | OKR tablosu | aday değil: konu dışı | Örnek board içeriği (hedefler, anahtar sonuçlar). |
| konuşma 0:00 | Beyin fırtınası, akış şeması, müşteri yolculuğu, strateji planlama | aday değil: genel kavram | Miro kullanım alanları sayılıyor. |
| konuşma 0:35 | Yapışkan notlar (sticky notes) | aday değil: genel kavram | 80 yapışkan notlu board anlatılıyor. |
| kare 0:41 | Action items / Project plan | aday değil: konu dışı | Toplantı çıktısı örnek içerik. |
| açıklama | Yorum ile bağlantı gönderme çağrısı | aday değil: sponsor/reklam | Yorumlara MIRO yaz, linki göndereyim. |
## Kareden okunanlar
- 0:07: Miro board'unda 'Project Brief: Rome in a day' belgesi; Discard, Iterate, Add to canvas düğmeleri; Jerryicus ve Aileen imleç etiketleri.
- 0:19: Terminalde /miro-mcp:code_explain_on_board çalışıyor; Claude board URL'si ve kod yolu istiyor; Infusing durumu ve Claude Code ipucu görünüyor.
- 0:35: Miro'da 'Company Goals, Objectives, Key results, Initiatives' OKR tablosu; Status, Type, Name, Progress, Owner sütunları; Strategy Sidekick ve Markus/Marta imleçleri.
## Belirsizlikler
- Yorumlar girişsiz alınamadığı için yorumlardaki bağlantı veya içerik bilinmiyor.
- Anlatıcının vaat ettiği bağlantı (yorumlara MIRO yazana gönderilecek link) açıklamada yok; hedef URL bilinmiyor.
- Sözlük eşleşmelerindeki Make, Descript, Inter ekranda doğrulanamadı; OCR hatası olabilir, aday yapılmadı.
- OCR'daki board URL'leri kısmen maskeli ve örnek niteliğinde; gerçek board kimliği belli değil.
- 0:14 ekranındaki Select a team ve izin metni yalnızca OCR'dan okundu; tam kurulum adımları gösterilmedi.
- 0:31 civarındaki Backlog, Roadmap, Sprint notes gibi board listesi öğeleri yalnız listede görünüyor, adaya alınmadı.
- Videoda kurulum komutu gösterilmedi, kurulum_komutlar boş.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://miro.com/app/board/xxx= | 0:19 | ekran | hayır |
| https://miro.com/app/board/xx= | 0:20 | ekran | hayır |
| https://miro.com/app/board/uxjV3xxzozA=/ | 0:20 | ekran | hayır |
| https://miro.com/app/board/uxjvIxxzozA-/ | 0:21 | ekran | hayır |
## İş akışı
- 1. adım — Miro'da 'Add & allow Miro MCP Server' ekranında izin verme (board okuma/değiştirme yetkisi) — araçlar: Miro, Miro MCP Server
- 2. adım — Claude Code terminalinde oturumu açık tutma ve ipucundaki 'claude --continue' / '--resume' seçeneklerini gösterme — araçlar: Claude
- 3. adım — Terminalde /miro-mcp:code_explain_on_board komutunu çalıştırma — araçlar: Claude, miro-mcp
- 4. adım — Miro board linkini komut istemine yapıştırma — araçlar: Claude, Miro
- 5. adım — Açıklanacak kodun yerel yolunu ve analiz isteğini yazma — araçlar: Claude
- 6. adım — Claude'un kodu analiz edip diyagram oluşturma kararını alması — araçlar: Claude, miro-mcp
- 7. adım — Mimari, veri akışı ve ana bileşen diyagramlarını Miro board'una çizme — araçlar: Miro MCP Server, Miro
- 8. adım — Miro AI önizlemesinde 'Add to canvas', 'Iterate' veya 'Discard' seçeneğiyle içeriği kabul etme/düzeltme — araçlar: Miro AI, Miro
- 9. adım — (Anlatılan) 80 yapışkan notlu beyin fırtınası board'unu Claude'a aktarıp sahipli, zaman çizelgeli öncelik listesi isteme — araçlar: Miro MCP Server, Claude
- 10. adım — (Anlatılan) Miro'da toplantı oturumunu yürütüp Claude ile özet, aksiyon maddeleri ve proje planı çıkarma — araçlar: Miro, Claude
- 11. adım — (Anlatılan) Claude'un çıktısını (aksiyon maddeleri, proje planı) Miro board'a aktarma ve paylaşma — araçlar: Claude, Miro
## Promptlar
- Yapışkan not kaosunu öncelik listesine dönüştürme — 80 yapışkan notlu beyin fırtınası board'unu analiz edip sahipleri ve zaman çizelgeleri olan sıralanmış bir öncelik listesi oluşturması istendi.
- Kodu Miro board'unda görselleştirme — Claude'dan, verilen Miro board linkine yerel bilgisayardaki kodu açıklayan görsel diyagramlar oluşturması istendi.
ikinci göz KAPALI: --ikinci-goz yok
