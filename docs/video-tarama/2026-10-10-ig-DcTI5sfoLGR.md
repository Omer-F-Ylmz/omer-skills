# “PROJE” yaz, detaylı bilgilendirmeyi DM üzerinden paylaşayım
## Künye
“PROJE” yaz, detaylı bilgilendirmeyi DM üzerinden paylaşayım · esadcom · süre: 1:03 · ? · https://www.instagram.com/reel/DcTI5sfoLGR/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-10-short-9 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 31173 tk · claude-haiku-5-5: claude-haiku-5-5 · 114095 tk
## Özet
Kısa videoda Claude'a PDF'i doğrudan yüklemenin token israfı olduğu söyleniyor. Konuşmacıya göre tek PDF sayfası 1500-3000 token yakıyor. Çözüm olarak Microsoft'un ücretsiz aracı MarkItDown öneriliyor. Araç PDF, Word, Excel, PowerPoint ve YouTube içeriğini temiz markdown'a çeviriyor ve yaklaşık %70 daha az token harcatıyor. Aracın markitdown-mcp paketi Claude'a MCP sunucusu olarak bağlanıyor. Videoda GitHub deposu, bir markdown çıktısı örneği ve pip ile kurulum ekranı gösteriliyor. Video yoruma 'proje' yazma çağrısıyla bitiyor.
## Bölümler
- 0:00 Sorun: PDF'i doğrudan yüklemek token yakıyor
- 0:24 Çözüm: Microsoft MarkItDown GitHub deposu
- 0:32 Desteklenen dosya türleri ve markdown çıktısı
- 0:44 markitdown-mcp ile MCP kurulumu
- 0:51 Claude'da kullanım ve yoruma 'proje' çağrısı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| MarkItDown | yok | CLI | yok | Microsoft'un PDF, Office ve YouTube içeriğini markdown'a çeviren Python aracı | 0:24 | Depo sayfasında markitdown adı ve altyazıda 'çözüm basit adı Markitdown' görünüyor. (karede: GitHub depo sayfası: Microsoft logosu, 'markitdown' Public, dosya listesi, altyazı 'çözüm basit adı Markitdown') |
| markitdown-mcp | yok | MCP | yok | MarkItDown'u Claude'a bağlayan STDIO MCP sunucusu; convert_to_markdown(uri) aracını sunar | 0:44 | Ekran metni 'MarkItDown-MCP', 'install markitdown-mcp' ve convert_to_markdown(uri) aracını gösteriyor. (karede: Bu an kare listesinde yok; yalnız OCR metni var: 'MarkItDown-MCP', 'To install the package, use pip', 'install markitdown-mcp') |
| Claude | yok | CLI | yok | PDF'in yüklendiği ve MCP'nin bağlandığı ana yapay zekâ asistanı | 0:00 | Konuşmada 'Cloud'a direkt PDF yükleyen herkes' geçiyor; ekranda 'Claude'a direkt pdf' yazıyor. |
| Sonnet 4.6 | yok | teknik | yok | Claude arayüzünde seçili görünen model | 0:01 | Ekran metninde 'Sonnet 4.6' yazıyor; Claude sohbet arayüzü görünüyor. (karede: Bu an kare listesinde yok; yalnız OCR metni: 'How can I help you today?' ve 'Sonnet 4.6') |
| GitHub | yok | teknik | yok | MarkItDown deposunun barındığı ve yıldız sayısının gösterildiği servis | 0:24 | Depo sayfası gösteriliyor; konuşmada 'GitHub'da 110 binden fazla yıldızı var' deniyor. (karede: GitHub depo sayfası: 9 Branches, 20 Tags, .github klasörü, commit listesi) |
| pip | yok | CLI | yok | markitdown-mcp paketini kurmak için kullanılan Python paket yöneticisi | 0:44 | Ekran metni 'To install the package, use pip' ve 'install markitdown-mcp' diyor. (karede: Bu an kare listesinde yok; yalnız OCR metni: 'To install the package, use pip' ve 'install markitdown-mcp') |
| Sublime Text | yok | teknik | yok | Dönüştürülecek HTML kaynağının gösterildiği metin editörü | 0:35 | Alt çubukta SUBLIME, Spaces: 4 ve Line 27 yazıyor; HTML kaynağı görünüyor. · kanıt: kare (karede: Koyu editörde HTML span ve href kodu; alt çubukta 'SUBLIME', 'Spaces: 4', 'Line 27, Columns 1 — 281 Lines') |
| convert_to_markdown | yok | MCP | yok | markitdown-mcp'nin dışa açtığı tek araç; uri parametresiyle dosyayı Markdown'a çevirir. | 0:44 | It exposes one tool: convert_to_markdown(uri), where uri (karede: kanıttan) It exposes one tool: convert_to_markdown(uri), where uri |
| Claude'u PDF'leri işlemeden önce markdown'a çevirmeye yönlendirmek | yok | prompt | yok | Claude'a PDF'leri her zaman önce MarkItDown MCP'ye göndermesi, sonra işlemesi söyleniyor. Böylece varsayılan olarak daha az token kullanması isteniyor. | 0:49 | kaynak: altyazı |
## Açıklama bağlantıları
- yok
## Site/UI teknikleri
- EKSİK: formda site/UI tekniği yok (kısmi kabul)
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| pip install markitdown-mcp | markitdown-mcp paketini kurar (karede: Bu an kare listesinde yok; yalnız OCR metni: 'To install the package, use pip' ve 'install markitdown-mcp') | 0:45 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Claude'a doğrudan PDF yüklemek token israfıdır; dosyanın tamamı işlenmek zorundadır. | 0:00 | özellik |
| Tek bir PDF sayfası 1500 ile 3000 token yakabilir. | 0:19 | sayısal |
| MarkItDown ile dosyalar yaklaşık %70 daha az token harcanarak işlenir. | 0:36 | sayısal |
| MarkItDown'ın GitHub'da 110 binden fazla yıldızı var. | 0:27 | sayısal |
| MarkItDown, Microsoft'un ücretsiz aracıdır. | 0:00 | özellik |
| MarkItDown PDF, Word, Excel, PowerPoint ve YouTube videolarını markdown'a çevirir. | 0:33 | özellik |
| markitdown-mcp tek araç sunar: convert_to_markdown(uri). | 0:44 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 · kare 0:36 | Claude | Claude | 'Cloud'a direkt PDF yükleyen herkes' ve ekranda 'Claude'a direkt pdf'. |
| ekran 0:01 | Sonnet 4.6 | Sonnet 4.6 | Claude arayüzünde model seçici metni. |
| konuşma 0:00 | Microsoft | aday değil: başka adayın parçası (MarkItDown) | 'Microsoft'un aylardır buna ücretsiz bir çözümü var'; MarkItDown'ın geliştiricisi. |
| konuşma 0:24 · kare 0:24 | MarkItDown | MarkItDown | Depo sayfası ve altyazı 'çözüm basit adı Markitdown'. |
| konuşma 0:27 | GitHub | GitHub | 'GitHub'da 110 binden fazla yıldızı var'; depo sayfası gösteriliyor. |
| konuşma 0:00 | PDF | aday değil: genel kavram | Yüklenen dosya türü; Claude'a PDF yükleme anlatılıyor. |
| konuşma 0:32 | Word, Excel, PowerPoint | aday değil: genel kavram | MarkItDown'ın desteklediği dosya türleri sayılıyor; ekranda 'Excel sheets'. |
| konuşma 0:33 · ekran 0:33 | YouTube videoları | aday değil: başka adayın parçası (MarkItDown) | MarkItDown'ın dönüştürebildiği girdi türü; ekranda 'YouTube videos'. |
| konuşma 0:00 | token | aday değil: genel kavram | PDF yüklemenin token harcaması anlatılıyor. |
| konuşma 0:00 | markdown | aday değil: genel kavram | MarkItDown'ın çıktı formatı. |
| konuşma 0:44 · kare 0:44 | MCP sunucusu (markitdown-mcp) | markitdown-mcp | 'MarkItDown-MCP' ve 'install markitdown-mcp' ekran metni. |
| ekran 0:44 | pip | pip | 'To install the package, use pip:' |
| ekran 0:44 | convert_to_markdown(uri) | aday değil: başka adayın parçası (markitdown-mcp) | MCP paketinin sunduğu tek araç. |
| ekran 0:44 | AutoGen Team | aday değil: başka adayın parçası (markitdown-mcp) | 'Built by AutoGen Team' paket sayfasında yazıyor. |
| ekran 0:24 | Git, Docker, .devcontainer, pre-commit, Dockerfile | aday değil: başka adayın parçası (MarkItDown) | Depo dosya listesinde görünen dosyalar. |
| ekran 0:27 | Python, LangChain, autogen-extension, openai, microsoft-office | aday değil: başka adayın parçası (MarkItDown) | Depo açıklaması ve konu etiketleri; videoda kullanılmıyor. |
| ekran 0:24 | Azure Content Understanding converter | aday değil: başka adayın parçası (MarkItDown) | Depodaki commit mesajı. |
| kare 0:35 | Sublime Text | Sublime Text | Alt çubukta SUBLIME ve HTML kaynağı. |
| kare 0:35 | https://en.wikipedia.org/wiki/Philip_Kotler | aday değil: konu dışı | Dönüştürülen örnek HTML içindeki bağlantı; araç değil. |
| linkli sayfa | http://pkotler.org | aday değil: konu dışı | Philip Kotler sayfası; videoda araç olarak anlatılmıyor. |
| kare 0:36 | Özgeçmiş yanıtı (resume bölümleri) | aday değil: konu dışı | Claude yanıtındaki örnek içerik; konuşma konusu değil. |
| açıklama · ekran 0:01 | 'proje' yorum çağrısı ve DM | aday değil: sponsor/reklam | 'PROJE yaz, detaylı bilgilendirmeyi DM üzerinden paylaşayım'. |
| yorum | Yorumlar | aday değil: konu dışı | Girişsiz alınamadı. |
## Kareden okunanlar
- 0:24: GitHub'da markitdown deposu (Public), 9 Branches, 20 Tags; .devcontainer, .github, packages, Dockerfile, SECURITY.md; altyazı 'çözüm basit adı Markitdown'.
- 0:35: Editörde HTML kodu: 'According to' ve Philip Kotler Wikipedia bağlantısı; alt çubukta Line 27, Spaces: 4, SUBLIME, Length: 282; altyazı 'Markdown dosyasına çeviriyor'.
- 0:36: Claude yanıtı: özgeçmiş bölümleri (Contact Info, Summary, Work Experience, Skills, Education, Projects, Certifications, Awards); altta konuşmacı; altyazı 'yani yapay zekanın'.
## Belirsizlikler
- Sublime Text'in videoda gerçekten kullanıldığı net değil; yalnız HTML kaynağını gösteren editör olarak görünüyor.
- Yorumlar girişsiz alınamadı; 'proje' çağrısının DM ile paylaşılan içeriği bilinmiyor.
- http://pkotler.org bağlantılı sayfa olarak geçiyor ama ekranda görünmüyor; videodaki Kotler bağlantısı Wikipedia'ya gidiyor.
- '%70 daha az token' ve '110 binden fazla yıldız' konuşmacının iddiası; ekranda doğrulanmadı (karede yalnız 8.5k forks okunuyor).
- markitdown-mcp kurulum karesi kare listesinde yok; komut yalnız OCR metninden okundu ('pip' + 'install markitdown-mcp').
- Claude'a MCP bağlama komutu veya yapılandırması gösterilmedi; konuşmada 'tek satır' deniyor.
- EKSİK: rapor (bölüm eksik: ## Site/UI teknikleri)
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://en.wikipedia.org/wiki/Philip_Kotler | 0:35 | ekran | hayır |
| http://pkotler.org | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — PDF'i doğrudan Claude'a yüklemenin token israfı olduğunu anlatma — araçlar: Claude
- 2. adım — Microsoft'un ücretsiz MarkItDown deposunu GitHub'da açıp dosya yapısını gösterme — araçlar: GitHub, MarkItDown
- 3. adım — MarkItDown'un PDF, Word, Excel, PowerPoint ve YouTube girdilerini Markdown'a çevirdiğini anlatma — araçlar: MarkItDown
- 4. adım — Wikipedia sayfasının dönüştürülmüş Markdown çıktısını Sublime Text'te açıp inceleme — araçlar: Sublime Text, MarkItDown
- 5. adım — markitdown-mcp paketini pip ile kurma — araçlar: pip, markitdown-mcp
- 6. adım — MCP sunucusunun dışa açtığı convert_to_markdown(uri) aracını tanıtma — araçlar: markitdown-mcp, convert_to_markdown
- 7. adım — Claude sohbet arayüzünde Sonnet 4.6 modeliyle PDF yükleme ekranını gösterme — araçlar: Claude, Claude Sonnet 4.6
- 8. adım — MCP bağlantısıyla dosyaları önce Markdown'a çevirip token tasarrufu sağlama önerisini anlatma — araçlar: Claude, markitdown-mcp
- 9. adım — Özgeçmiş hazırlama örneğini Claude yanıtı üzerinden gösterme — araçlar: Claude
## Promptlar
- Claude'u PDF'leri işlemeden önce markdown'a çevirmeye yönlendirmek — Claude'a PDF'leri her zaman önce MarkItDown MCP'ye göndermesi, sonra işlemesi söyleniyor. Böylece varsayılan olarak daha az token kullanması isteniyor.
