# Yorumlara “Agent” yaz, bütün kodlama ajanlarını tek terminalde toplayan ücretsiz
## Künye
Yorumlara “Agent” yaz, bütün kodlama ajanlarını tek terminalde toplayan ücretsiz · theakselege · süre: 0:37 · ? · https://www.instagram.com/reel/Dcs5dsxqki8/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-39 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 34281 tk · claude-haiku-5-5: claude-haiku-5-5 · 90568 tk
## Özet
Instagram reel'inde Herder (ekranda herdr) adlı ücretsiz, açık kaynak terminal aracı tanıtılıyor. Birden fazla Claude Code ve Codex ajanı tek terminalde, çalışma alanları ve sekmelerle yan yana yönetiliyor. Hangi ajanın çalıştığı, boşta olduğu ya da girdi beklediği tek bakışta görülüyor. Sonda kurulum komutları gösteriliyor ve yorumlara 'Agent' yazılması isteniyor.
## Bölümler
- 0:00 Herder tanıtımı: tek terminalde birden çok ajan
- 0:11 Yan yana Codex ajanları ve çalışma alanları
- 0:18 Claude Code ajanı örneği
- 0:34 Kurulum komutları ve yorum çağrısı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| herdr | yok | CLI | yok | Birden fazla kodlama ajanını tek terminalde çalışma alanları ve sekmelerle yöneten, ücretsiz açık kaynak araç. | 0:34 | Ekranda 'Installing herdr' ve herdr.dev kurulum adresleri görünüyor; konuşmada 'Herder' deniyor. (karede: Yalnız 0:11-0:13 kareleri gönderildi; kurulum ekranı (0:34) kare olarak yok, OCR metninden okundu. Karelerde panelli ajan terminali görünüyor.) |
| Claude Code | yok | CLI | yok | Herdr içinde çalıştırılan kodlama ajanlarından biri. | 0:18 | Ekran metninde 'Claude Code v2.1.92' var; altyazıda 'bulut kod' ajanı geçiyor. |
| Codex | yok | CLI | yok | Herdr'da yan yana çalışan OpenAI kodlama ajanı. | 0:11 | Panellerde Codex ipuçları görünüyor. (karede: 2x2 ızgara panelleri; 'Try the Codex App' ipucu ve 'gpt-5.6-luna medium' yazısı.) |
| Claude Haiku 4.5 | yok | teknik | yok | Claude Code oturumunda seçili model. | 0:18 | Ekran metninde 'Haiku 4.5 with medium effort - Claude Max' yazıyor. · kanıt: yok |
| gpt-5.6-luna | yok | teknik | yok | Codex panellerinde kullanılan model. | 0:11 | Panel altında 'gpt-5.6-luna medium' yazıyor. (karede: Her panelin altında 'gpt-5.6-luna medium ~/Projects/herdr' satırı.) |
| Git | yok | CLI | yok | Depo durumunu kontrol etmek için ajanın çalıştırdığı sürüm kontrol komutu. | 0:13 | Kare 3: ajan panelinde "git status" komutu ve çıktısı (karede: kanıttan) Kare 3: ajan panelinde "git status" komutu ve çıktısı |
| ripgrep (rg) | yok | CLI | yok | Dosyalarda desen arayan komut; ajan AGENTS.md ve CLAUDE.md dosyalarını bu komutla arıyor. | 0:13 | Kare 3: ajan panelinde "rg 'AGENTS.md/CLAUDE.md' -g ..." komutu · kanıt: kare (karede: Kare 3: ajan panelinde "rg 'AGENTS.md/CLAUDE.md' -g ..." komutu) |
| Claude Code ile proje değerlendirmesi | yok | prompt | yok | Claude Code'a proje hakkında düşüncesi soruluyor ('wdyt on this project?'); ajan projeyi inceleyip yorum yapacak. | 0:18 | kaynak: altyazı |
| Paralel Codex ajanlarıyla kod incelemesi | yok | prompt | yok | Codex ajanlarına salt okunur inceleme: kod tabanı mimarisi, CLI yüzeyi, test boşlukları ve dokümantasyon sapmalarını bulgularla raporlamaları, dosya değiştirmemeleri. | 0:13 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| curl -fsSL https://herdr.dev/install.sh / sh | herdr'i macOS/Linux'ta kurulum betiğiyle kurar. | 0:34 | kare |
| irm https://herdr.dev/install.ps1 / iex | herdr'i Windows PowerShell'de kurar. | 0:34 | kare |
| /fast | Codex'te hızlı çıkarım modunu açar (ipucu olarak görünüyor). (karede: Panelde 'Use /fast to enable our fastest inference' ipucu.) | 0:12 | kare |
| /usage | Codex'te kullanım limiti sıfırlamasını kullanır (ipucu). (karede: Panelde 'Run /usage to use one' yazısı.) | 0:12 | kare |
| codex app | Codex uygulamasını başlatır (ipucu metninde önerilir) (karede: Codex panelindeki ipucu: "Run 'codex app' or visit ...") | 0:11 | kare |
| /btw | Ajana hızlı bir yan soru sormaya yarar (karede: Claude Code panelinde "/btw to ask a quick side question" ipucu) | 0:11 | kare |
| /init | Projede CLAUDE.md dosyası oluşturur (karede: Claude Code karşılama ekranında "Run /init to cre..." ipucu (OCR)) | 0:21 | kare |
| git status | Git deposunun değişen ve izlenmeyen dosyalarını gösterir (karede: Ajan panelinde çalıştırılan "git status" komutu) | 0:13 | kare |
| rg 'AGENTS.md/CLAUDE.md' -g ... | Dosyalarda AGENTS.md ve CLAUDE.md desenini arar (karede: Ajan panelinde "rg 'AGENTS.md/CLAUDE.md' -g ..." komutu) | 0:13 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Araç tamamen ücretsiz ve yüzde 100 açık kaynak. | 0:32 | özellik |
| Hangi ajanın çalıştığı, boşta olduğu veya girdi beklediği tek bakışta görülüyor. | 0:00 | özellik |
| Şu anda tüm büyük kodlama ajanlarıyla çalışıyor. | açıklama | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | herdr/Herder | herdr | Tanıtılan ana araç. |
| konuşma 0:00 | Claude Code | Claude Code | Ajan olarak anılıyor ve 0:18'de gösteriliyor. |
| konuşma 0:00 | Codex | Codex | Yan yana çalışan ajan. |
| kare 0:12 | gpt-5.6-luna | gpt-5.6-luna | Panel model etiketi. |
| ekran 0:18 | Claude Haiku 4.5 | Claude Haiku 4.5 | Claude Code başlığında model yazıyor. |
| ekran 0:18 | Claude Max | aday değil: konu dışı | Yalnız hesap planı etiketi. |
| ekran 0:13 | Git | aday değil: konu dışı | Yalnız ajan çıktısında 'git status' geçiyor. |
| ekran 0:25 | Gemini ve Grok | aday değil: konu dışı | Arka plan animasyon metni. |
| ekran 0:34 | install.sh ve install.ps1 | herdr | herdr kurulum komutları. |
| ekran 0:34 | Homebrew, Nix Flake | aday değil: konu dışı | Yalnız kurulum menüsünde görünüyor. |
| ekran 0:12 | chatgpt.com Codex sayfası | aday değil: konu dışı | Codex panelindeki ipucu bağlantısı. |
| ekran 0:21 | gmail.com | aday değil: konu dışı | Claude Code hesap e-postası. |
| açıklama | Yorumlara 'Agent' yaz çağrısı | aday değil: sponsor/reklam | Etkileşim çağrısı. |
## Kareden okunanlar
- 0:11: Sol tarafta ajan paneli, sağda iki Codex paneli; altyazı 'edebilirsiniz,'.
- 0:12: Turuncu çerçeveli paneller: 'Try the Codex App', 'You have 3 usage limit resets', 'gpt-5.6-luna medium ~/Projects/herdr'.
- 0:13: 2x2 panel ızgarası; 'Working (3m • esc to interrupt)', 'Do not modify any files' talimatları.
## Belirsizlikler
- Yorumlar girişsiz alınamadı.
- Araç adı konuşmada 'Herder', ekranda 'herdr'; kanonik ad herdr alındı.
- Gönderilen kareler yalnız 0:11-0:13; diğer içerik OCR'dan okundu.
- 0:25 animasyonundaki Gemini/Grok adları arka plan görseli; videoda kullanılmıyor.
- Codex ipucu URL'si OCR'da bozuk; yaklaşık yazıldı.
- Kurulum seçeneklerinde Homebrew ve Nix Flake menüde görünüyor, kullanılmıyor.
- Herdr'ın resmi repo bağlantısı verilmedi.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://herdr.dev/install.sh | 0:34 | ekran | evet |
| https://herdr.dev/install.ps1 | 0:34 | ekran | evet |
| chatgpt.com/codex?app-landing-page=true | 0:12 | ekran | hayır |
| gmail.com | 0:21 | ekran | hayır |
| https://chatgpt.com/codex/app-landing-page | 0:11 | ekran | evet |
## İş akışı
- 1. adım — Herdr kurulum betiğini terminalde çalıştırma (Stable install; Windows için PowerShell komutu dahil) — araçlar: Herdr, curl, PowerShell
- 2. adım — Herdr'ı açıp ekranı 2x2 ızgara ve ayrı çalışma alanlarına bölme — araçlar: Herdr
- 3. adım — Codex ajanını ~/Projects/herdr dizininde başlatma — araçlar: Codex, gpt-5.6-luna medium
- 4. adım — Claude Code ajanını aynı dizinde başlatma — araçlar: Claude Code, Claude Haiku 4.5
- 5. adım — Codex App ipucu ve kullanım limiti mesajlarını kontrol etme — araçlar: Codex
- 6. adım — Ajanlara salt okunur kod incelemesi görevi verme (dosya değiştirmeden bulgu raporu) — araçlar: Claude Code, Codex
- 7. adım — Ajanların depo durumunu ve dosyaları kontrol etmesi (git status, rg araması) — araçlar: Git, ripgrep (rg)
- 8. adım — Herdr'da her ajanın durumunu izleme: çalışıyor, boşta, girdi bekliyor — araçlar: Herdr
- 9. adım — Ajan çıktılarını tek ekrandan takip edip sonuçlara geçiş yapma — araçlar: Herdr
## Promptlar
- Claude Code ile proje değerlendirmesi — Claude Code'a proje hakkında düşüncesi soruluyor ('wdyt on this project?'); ajan projeyi inceleyip yorum yapacak.
- Paralel Codex ajanlarıyla kod incelemesi — Codex ajanlarına salt okunur inceleme: kod tabanı mimarisi, CLI yüzeyi, test boşlukları ve dokümantasyon sapmalarını bulgularla raporlamaları, dosya değiştirmemeleri.
ikinci göz KAPALI: --ikinci-goz yok
