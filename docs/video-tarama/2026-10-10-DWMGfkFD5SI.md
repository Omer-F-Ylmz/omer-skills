# Claude ile Otomatik Teklif Sistemi Kurdum (Google Docs + Sheets + Gmail)
## Künye
Claude ile Otomatik Teklif Sistemi Kurdum (Google Docs + Sheets + Gmail) · Emrullah Yaprak | AI & Automation · süre: 19:00 · en-orig · https://youtu.be/DWMGfkFD5SI · şema 2
motor: parti 2026-10-10-short-7 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (57)
kareler: girdi ≤40000 jeton için 60→57
claude-sonnet-5-5: claude-sonnet-5-5 · 69337 tk · claude-haiku-5-5: claude-haiku-5-5 · 227510 tk
## Özet
Emrullah Yaprak, Claude Desktop (Claude Code sekmesi, Opus 5 Extra) ve Google Workspace CLI (gws) ile kod yazmadan otomatik teklif sistemi kuruyor. Google Cloud Console'da Gmail, Sheets, Docs ve Drive API'leri açılıp OAuth istemcisi oluşturuluyor, gws auth login ile hesap bağlanıyor. Dolu bir teklif belgesi yeniden kullanılabilir şablona çevriliyor, Excel firma listesi Google Sheets'e dönüştürülüyor. Listedeki ilk firma için teklif Docs olarak dolduruluyor, PDF'e çevriliyor, tabloya link yazılıyor ve PDF ekli Gmail taslağı hazırlanıyor (gönderilmiyor). Sonunda tüm akış /teklif-kutusu skill'ine dönüştürülüp yeni sohbette tek komutla Yıldız Reklam Ajansı için çalıştırılıyor.
## Bölümler
- 0:00 Giriş: Claude ile Otomatik Teklif Sistemi
- 0:28 Sistem Nasıl Çalışıyor? Şablon, Firma Listesi, PDF ve Mail Taslağı
- 2:42 Claude Desktop Kurulumu ve Proje Klasörü
- 4:53 Google Workspace CLI (GWS) ve Google Cloud API Ayarları
- 8:51 Dolu Tekliften Tekrar Kullanılabilir Şablon Oluşturma
- 12:15 İlk Firma İçin Teklif, PDF ve Gmail Taslağı
- 15:30 Tüm Akışı Skill'e Çevirme: /teklif-kutusu
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Desktop | yok | CLI | yok | Claude masaüstü uygulaması; Claude Code sekmesiyle yerel klasörde çalışılıyor. | 2:42 | We need to download the Claude desktop application. |
| Claude Code | yok | CLI | yok | Desktop içindeki sekme; işlemler yerel klasörde yürütülüyor. | 2:42 | we need to click on the "Claude Code" tab at the top. |
| Opus 5 | yok | teknik | yok | Sunucunun içinde çalıştığı ana model; Opus 5 Extra seçiliyor. | 4:44 | select Opus 5.5, and I select extra. Opus 5 will be sufficient |
| Google Workspace CLI | yok | CLI | https://github.com/googleworkspace/cli | gws komut satırı aracı; Drive, Docs, Sheets, Gmail işlemlerini yapar. | 4:36 | npm install -g @googleworkspace/cli komutu ekranda (karede: kanıttan) npm install -g @googleworkspace/cli komutu ekranda |
| npm | yok | CLI | yok | gws'nin global kurulumu için paket yöneticisi. | 4:36 | npm install -g @googleworkspace/cli (karede: kanıttan) npm install -g @googleworkspace/cli |
| Skills CLI | yok | CLI | https://github.com/googleworkspace/cli | npx skills add ile gws skill'leri kuruluyor. | 4:36 | npx skills add .../skills/gws-docs (karede: kanıttan) npx skills add .../skills/gws-docs |
| gws-docs | yok | skill | yok | Docs belge okuma/yazma skill'i. | 4:36 | npx skills add .../gws-docs (karede: kanıttan) npx skills add .../gws-docs |
| gws-drive | yok | skill | yok | Drive dosya yönetimi skill'i. | 4:36 | npx skills add .../gws-drive (karede: kanıttan) npx skills add .../gws-drive |
| gws-gmail | yok | skill | yok | Gmail okuma/yazma/taslak skill'i. | 4:36 | npx skills add .../gws-gmail (karede: kanıttan) npx skills add .../gws-gmail |
| gws-sheets | yok | skill | yok | Sheets okuma/yazma skill'i. | 4:36 | npx skills add .../gws-sheets (karede: kanıttan) npx skills add .../gws-sheets |
| gws-shared | yok | skill | yok | gws ortak skill'i. | 4:36 | npx skills add .../gws-shared (karede: kanıttan) npx skills add .../gws-shared |
| Google Cloud Console | yok | teknik | yok | Proje, API etkinleştirme, OAuth ekranı ve istemci oluşturma. | 5:16 | we need to go to the Google Cloud Console. |
| Gmail API | yok | teknik | yok | Taslak oluşturmak için etkinleştirilen API. | 5:53 | 1st, Google Gmail API. |
| Google Sheets API | yok | teknik | yok | Tablo güncelleme için etkinleştirilen API. | 5:53 | 2nd, Google Sheets API. |
| Google Docs API | yok | teknik | yok | Belge doldurma için etkinleştirilen API. | 5:53 | We need to open the Google Docs API |
| Google Drive API | yok | teknik | yok | Dosya/klasör ve PDF için etkinleştirilen API. | 5:53 | finally the Google Drive API. |
| OAuth | yok | teknik | yok | OAuth onay ekranı ve Desktop App istemcisi (client_secret.json) ile yetkilendirme. | 6:54 | client ID type Desktop App |
| gws auth login | yok | CLI | yok | Google hesabını bağlayan giriş komutu. | 7:36 | gws auth login --services drive,docs,sheets,gmail (karede: kanıttan) gws auth login --services drive,docs,sheets,gmail |
| Google Drive | yok | iş akışı | yok | Şablon, tablo, aylık klasör ve PDF'lerin depolandığı yer. | 0:28 | We are working with Drive here. |
| Google Docs | yok | iş akışı | yok | Teklif şablonu ve doldurulmuş teklif belgeleri. | 0:36 | Teklif Şablonu - Google Docs, {{firma}} yer tutucuları (karede: kanıttan) Teklif Şablonu - Google Docs, {{firma}} yer tutucuları |
| Google Sheets | yok | iş akışı | yok | Firma listesi; durum, link, tarih, pdf sütunları güncelleniyor. | 0:28 | Firma Listesi tablosu, durum Taslak hazır (karede: kanıttan) Firma Listesi tablosu, durum Taslak hazır |
| Gmail | yok | iş akışı | yok | PDF ekli taslak e-posta oluşturuluyor. | 14:17 | Prepare an email to go to the company official. Do not send |
| teklif-kutusu | yok | skill | https://github.com/eyaprak/skills/tree/main/teklif-kutusu | Tüm akışı tek komutla çalıştıran skill. | 15:30 | Create a skill named "Proposal Box." |
| Claude Skills | yok | teknik | yok | Konuşmadan kalıcı skill üretme tekniği. | 15:30 | All the actions we took... will be turned into a skill. |
| Konnektörler | yok | ipucu | yok | Claude connectors yerine gws tercih edilmesinin nedeni anlatılıyor. | 7:56 | we can already connect from the connectors section · kanıt: yok |
| Antigravity | yok | CLI | yok | Yorumda alternatif olarak anılıyor; sahip gws ve skill dosyasının çalıştığını söylüyor. | açıklama | yorumda: o Antigravity'de de çalışıyor |
| Windows CMD | yok | teknik | yok | gws auth login komutunun çalıştırıldığı Windows komut istemi. | 7:56 | I copy this and go to CMD, and paste it into the command prompt · kanıt: yok |
| JavaScript | yok | teknik | yok | Skill içindeki kayit-sec.js ve mail-olustur.js betikleri JavaScript ile yazıldı. | 16:02 | Edited kayit-sec.js, ran a command (karede: Claude çıktısında kayit-sec.js ve mail-olustur.js dosya adları ve JavaScript etiketi görünüyor.) |
| Google Workspace CLI kurulumu | yok | prompt | yok | Bilgisayara Google Workspace komut satırı aracını kur ve hazır hale getir; global kur, sürümü doğrula, yalnızca beş gws skill'ini ekle, hesap bağlamayı adım adım anlat ama girişi kendin yapma. | 4:53 | kaynak: kare |
| Dosyaları Drive'a yükleme ve tabloyu dönüştürme | yok | prompt | yok | Yüklenen dolu teklifi ve Excel tablosunu Drive'da 'Teklif Kutusu' klasörüne yükle, Excel'i Google Sheets'e çevir (Musteriler), orijinal adını değiştir, ayar dosyasında kimlikleri sakla. | 8:51 | kaynak: kare |
| Şablon oluşturma | yok | prompt | yok | Dolu teklifi, müşteri sütunlarına göre yer tutuculu tekrar kullanılabilir şablona çevir; fiyat tablosuna dokunma, ne değiştiğini raporla, geçerlilik tarihini gönderim tarihi +1 ay yap. | 10:20 | kaynak: kare |
| İlk firma için teklif üretimi | yok | prompt | yok | Şablonu kullanarak listedeki ilk 'Bekliyor' firma için teklif hazırla: kopya çıkar, alanları doldur, aylık klasöre taşı, tabloda durumu 'Belge hazır' yap, tarih ve linki yaz; belirsizlikte sor. | 12:15 | kaynak: kare |
| PDF üretimi | yok | prompt | yok | Bu belgenin PDF'ini al, aynı ay klasörüne belgeyle aynı adla koy ve ana listede o firmanın pdf sütununa linki yaz. | 13:24 | kaynak: kare |
| Gmail taslağı | yok | prompt | yok | Firma yetkilisine e-posta hazırla, gönderme, taslak bırak; PDF'i ekle; durumu 'Taslak hazır' yap. | 14:17 | kaynak: altyazı |
| Akışı skill'e çevirme | yok | prompt | yok | Bu sohbetteki işi kalıcı yap: 'teklif-kutusu' adlı skill oluştur; çağrıldığında 'Bekliyor' durumundaki ilk firma için baştan sona tüm adımları yapsın. | 15:34 | kaynak: kare |
## Açıklama bağlantıları
- https://github.com/googleworkspace/cli — Google Workspace CLI deposu · aday: evet (Google Workspace CLI) · Videoda kurulan ve kullanılan gws aracı. · sınıf: diğer
- https://console.cloud.google.com — Google Cloud Console · aday: evet (Google Cloud Console) · Videoda API açma ve OAuth için kullanıldı. · sınıf: diğer
- https://claude.com/download — Claude indirme sayfası · aday: evet (Claude Desktop) · Claude Desktop indiriliyor. · sınıf: diğer
- https://youtu.be/RP7QH24Qqvs — Skills videosu · aday: hayır · Yazarın başka videosu; araç değil, referans. · sınıf: diğer
- https://drive.google.com/drive/folders/101SCBVaRUi-nxjsKA6WDOnb5-wcxVjdB?usp=sharing — Ücretsiz kaynak klasörü (örnek dosyalar) · aday: hayır · Örnek dosya paylaşımı; izleyicinin kullanacağı araç değil. · sınıf: diğer
- https://github.com/eyaprak/skills/tree/main/teklif-kutusu — teklif-kutusu skill deposu · aday: evet (teklif-kutusu) · Videoda üretilen skill'in kendisi. · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| npm install -g @googleworkspace/cli | gws aracını global kurar (karede: Prompt'ta '1. Aracı global olarak kur: npm install -g @googleworkspace/cli') | 4:36 | kare |
| gws --version | Kurulumu doğrular (karede: '2. Kurulumu doğrula: gws --version') | 4:36 | kare |
| npx skills add https://github.com/googleworkspace/cli/tree/main/skills/gws-docs | gws-docs skill'ini ekler (karede: npx skills add gws-docs satırı) | 4:36 | kare |
| npx skills add https://github.com/googleworkspace/cli/tree/main/skills/gws-drive | gws-drive skill'ini ekler (karede: npx skills add gws-drive satırı) | 4:36 | kare |
| npx skills add https://github.com/googleworkspace/cli/tree/main/skills/gws-gmail | gws-gmail skill'ini ekler (karede: npx skills add gws-gmail satırı) | 4:36 | kare |
| npx skills add https://github.com/googleworkspace/cli/tree/main/skills/gws-shared | gws-shared skill'ini ekler (karede: npx skills add gws-shared satırı) | 4:36 | kare |
| npx skills add https://github.com/googleworkspace/cli/tree/main/skills/gws-sheets | gws-sheets skill'ini ekler (karede: npx skills add gws-sheets satırı) | 4:36 | kare |
| gws auth login --services drive,docs,sheets,gmail | Google hesabını OAuth ile bağlar (karede: CMD'de gws auth login --services drive,docs,sheets,gmail) | 7:36 | kare |
| gws auth status | Bağlantı durumunu doğrular (karede: Sohbette 'Doğrulama: gws auth status') | 7:26 | kare |
| /teklif-kutusu | Skill'i çağırıp ilk 'Bekliyor' firmanın teklifini baştan sona işler | 16:30 | altyazı |
| npx skills add https://github.com/googleworkspace/cli/tree/main/skills/gws-docs (ve gws-drive, gws-gmail, gws-shared, gws-sheets için aynı) | Google Docs, Drive, Gmail, Shared ve Sheets gws skill'lerini Claude'a ekler. (karede: Claude yanıtında beş adet npx skills add komutu sırayla yazılı.) | 4:36 | kare |
| gws auth login --readonly --services drive,docs,sheets,gmail | Yalnızca okuma izniyle Google hesabını bağlar; videoda tercih edilmedi. (karede: Claude yanıtında readonly seçeneği önerisi görünüyor.) | 8:02 | kare |
| gws auth login | Tarayıcıda Google hesabı onayını açar ve izinleri kaydeder. | 7:56 | altyazı |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Sistem e-posta göndermiyor, yalnızca taslak hazırlıyor; son kontrol kullanıcıda. | 1:28 | özellik |
| Connectors yerine gws ile Sheets'te satır güncellemek çok daha kolay. | 7:56 | karşılaştırma |
| XLSX'te güncelleme sorunları çıkıyor; Google Sheets'e çevrilmesi gerekiyor. | 9:51 | özellik |
| Çalışması için bir Claude aboneliği yeterli. | 2:29 | öneri |
| Ücretsiz Gmail hesabıyla kurulabilir, ücretli Workspace gerekmez; Cloud'da proje açmak ücretsiz. | açıklama | özellik |
| Tekrarlı işleri skill'e çevirmek açıklamayı tekrarlamayı gereksiz kılıyor. | 18:32 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:28 | Google Drive | Google Drive | We are working with Drive here. |
| konuşma 0:28 | Excel firma listesi | aday değil: başka adayın parçası (Google Sheets) | companies... in this Excel list. |
| kare 0:36 | Google Docs şablonu | Google Docs | Teklif Şablonu - Google Docs |
| kare 0:28 | Gemini düğmesi | aday değil: konu dışı | Ask Gemini ekranda |
| konuşma 2:42 | Claude Desktop | Claude Desktop | download the Claude desktop application |
| konuşma 2:42 | Claude Code sekmesi | Claude Code | click on the Claude Code tab |
| kare 2:34 | Claude indirme sayfası | Claude Desktop | Download Claude / Claude by Anthropic |
| konuşma 4:44 | Opus 5 | Opus 5 | select Opus 5.5... extra |
| kare 4:36 | npm | npm | npm install -g |
| kare 4:36 | Skills CLI | Skills CLI | npx skills add |
| kare 4:36 | gws-docs/drive/gmail/sheets/shared | gws-docs | npx skills add ... skills/gws-docs (diğerleri ayrı satır) |
| konuşma 4:53 | Google Workspace CLI | Google Workspace CLI | install the Google Workspace command-line tool |
| kare 5:10 | gcloud / Google Cloud SDK | aday değil: konu dışı | gcloud'u kur seçeneği önerildi ama kullanılmadı |
| kare 5:16 | Kubernetes Engine, Cloud Storage, BigQuery, VPC menüleri | aday değil: konu dışı | Cloud konsolu ana sayfasında menü |
| kare 5:16 | n8nkursu-v2 projesi | aday değil: konu dışı | Mevcut proje; yenisi oluşturuldu |
| konuşma 5:53 | Google Cloud Console | Google Cloud Console | go to the Google Cloud Console |
| konuşma 5:53 | Gmail API | Gmail API | Google Gmail API |
| konuşma 5:53 | Google Sheets API | Google Sheets API | Google Sheets API |
| konuşma 5:53 | Google Docs API | Google Docs API | Google Docs API |
| konuşma 5:53 | Google Drive API | Google Drive API | Google Drive API |
| kare 5:42 | Sheets MCP API / Google Drive MCP / Gmail MCP API | aday değil: konu dışı | Marketplace arama sonucu, kullanılmadı |
| kare 5:32 | youtube.googleapis.com | aday değil: konu dışı | Enable service ekranı, kullanılmadı |
| konuşma 6:34 | OAuth onay ekranı | OAuth | OAuth consent screen... Desktop App |
| konuşma 7:56 | Claude connectors (Google Calendar, Drive) | Konnektörler | connect from the connectors section |
| kare 8:08 | 21st.dev, Figma, Claude in Chrome, n8n bağlayıcıları | aday değil: konu dışı | Connectors menüsünde listelenmiş, kullanılmadı |
| kare 6:56 | AnyDesk, Codex Görseli, Hermes Agent küçük resmi | aday değil: konu dışı | İndirilenler klasöründeki dosyalar |
| konuşma 14:17 | Gmail | Gmail | our Gmail... drafts |
| konuşma 15:30 | teklif-kutusu skill | teklif-kutusu | turned into a skill |
| konuşma 16:30 | Claude Skills | Claude Skills | learn more about skills |
| konuşma 18:32 | Hermes Agent | aday değil: konu dışı | kanalda başka videolar olarak anıldı |
| kare 16:02 | kayit-sec.js / mail-olustur.js | teklif-kutusu | Skill içinde düzenlenen JS dosyaları |
| yorum | Antigravity | Antigravity | Claude Code yerine antigravity kullanamaz mıyız? |
| açıklama | Örnek dosya klasörü (Drive) | aday değil: konu dışı | Ücretsiz kaynaklar klasörü |
| açıklama | Claude Opus modeli | Opus 5 | Videoda Claude'un Opus 5 modeli kullanıldı |
| linkli sayfa | Chrome Web Store Claude eklentisi, VS Code uzantısı, 21st.dev base-ui/visx | aday değil: konu dışı | Bağlantılı sayfalarda geçiyor, videoda kullanılmadı |
## Kareden okunanlar
- 0:26: Firma Listesi tablosu: firma, yetkili, e-posta, hizmet, tutar, durum, teklif_linki, gonderim_tarihi, pdf sütunları; Mavi Ofis ve Yıldız Reklam 'Taslak hazır'.
- 0:36: Teklif Şablonu belgesi: {{firma}}, {{yetkili}}, {{hizmet}}, {{tutar}}, {{gonderim_tarihi+1ay}} yer tutucuları.
- 4:36: Prompt: npm install -g @googleworkspace/cli, gws --version ve beş npx skills add komutu.
- 7:36: Scope seçimi: Google Drive, Sheets, Gmail, Docs, Cloud Platform (5/5 seçili).
- 7:54: gws auth login çıktısı: Authentication successful, status success, kimlik bilgileri şifreli kaydedildi.
- 14:50: Gmail taslağı: Teklifimiz - Sosyal medya yönetimi (6 ay), ek: Teklif - Yıldız Reklam Ajansı.pdf.
- 6:34: OAuth Audience sayfası: External, Test users bölümü.
## Belirsizlikler
- Model adı konuşmada 'Opus 5.5', ekranda ve açıklamada 'Opus 5 Extra / Opus 5' geçiyor.
- Gmail, Drive, Docs, Sheets ayrı kayıtlar olarak da API adayları; connectors listesinde görünen 21st.dev, Figma, n8n, Claude in Chrome kullanılmadı, aday yapılmadı.
- Kare listesindeki kaynak yolları '[yol]' olarak verildi; kareler sırayla eşleştirildi, bazı zamanlar yaklaşık.
- Bağlantılı sayfalardaki (code.claude.com, 21st.dev, base-ui, visx) içerikler videoda kullanılmadı.
- Sözlük eşleşmeleri (Matter.js, Make, Next.js vb.) ses bulanık eşleşmesi; videoda anlatılmıyor.
- Ekrandaki otomatik OCR metinleri bozuk; yalnızca okunabilen kısımlar kullanıldı.
- 'Teklif Kutusu' (skill adı) altyazıda 'Proposal Box' diye çevrilmiş; ekranda /teklif-kutusu.
## Atlanan segment oranı
0/23 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://github.com/googleworkspace/cli | 4:36 | ekran | evet |
| https://console.cloud.google.com | açıklama | açıklama | evet |
| https://claude.com/download | 2:34 | ekran | evet |
| https://youtu.be/RP7QH24Qqvs | açıklama | açıklama | hayır |
| https://drive.google.com/drive/folders/101SCBVaRUi-nxjsKA6WDOnb5-wcxVjdB?usp=sharing | açıklama | yorum | hayır |
| https://github.com/eyaprak/skills/tree/main/teklif-kutusu | açıklama | yorum | evet |
| https://github.com/googleworkspace/cli/tree/main/skills/gws-docs | 4:36 | ekran | evet |
| https://github.com/googleworkspace/cli/tree/main/skills/gws-drive | 4:36 | ekran | evet |
| https://github.com/googleworkspace/cli/tree/main/skills/gws-gmail | 4:36 | ekran | evet |
| https://github.com/googleworkspace/cli/tree/main/skills/gws-sheets | 4:36 | ekran | evet |
| https://github.com/googleworkspace/cli/tree/main/skills/gws-shared | 4:36 | ekran | evet |
| https://www.googleapis.com/auth/drive | 7:36 | ekran | hayır |
| https://www.googleapis.com/auth/spreadsheets | 7:36 | ekran | hayır |
| https://www.googleapis.com/auth/gmail.modify | 7:36 | ekran | hayır |
| https://www.googleapis.com/auth/documents | 7:36 | ekran | hayır |
| https://www.googleapis.com/auth/cloud-platform | 7:36 | ekran | hayır |
| console.cloud.google.com/auth/clients/create | 6:48 | ekran | evet |
| docs.google.com | 0:26 | ekran | evet |
| drive.google.com | 0:26 | ekran | evet |
| mail.google.com | 1:36 | ekran | evet |
| http://code.claude.com/docs/en/desktop-linux | açıklama | açıklama | hayır |
| https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/overview | açıklama | açıklama | hayır |
| https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code | açıklama | açıklama | hayır |
| https://claude.ai/?redirect=claude.com&via=static_email | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/quickstart#step-1-install-claude-code | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/github-actions | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/changelog | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/setup#system-requirements | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/common-workflows | açıklama | açıklama | hayır |
| https://base-ui.21st.dev | açıklama | açıklama | hayır |
| https://visx.21st.dev | açıklama | açıklama | hayır |
| maviofis.com.tr | 0:26 | ekran | hayır |
| yildizreklam.com | 0:26 | ekran | hayır |
| anadolulojistik.com.tr | 0:26 | ekran | hayır |
| egetekstil.com | 0:26 | ekran | hayır |
| beyazmimarlik.com | 0:26 | ekran | hayır |
| kdgida.com.tr | 0:26 | ekran | hayır |
| novayazilim.com | 0:26 | ekran | hayır |
| marmaramakina.com.tr | 0:26 | ekran | hayır |
| akdenizturizm.com | 0:26 | ekran | hayır |
| simsekenerj.com.tr | 0:26 | ekran | hayır |
| https://code.claude.com/docs/en/desktop-quickstart | 2:34 | ekran | hayır |
| https://console.cloud.google.com/welcome?authuser=3&organizationId=0&project=n8nkursu-v2-494215 | 5:16 | ekran | evet |
| https://console.cloud.google.com/projectcreate | 5:30 | ekran | evet |
| https://console.cloud.google.com/marketplace/product/google/gmail.googleapis.com | 5:54 | ekran | evet |
| https://console.cloud.google.com/marketplace/product/google/sheets.googleapis.com | 5:58 | ekran | evet |
| https://console.cloud.google.com/marketplace/product/google/drive.googleapis.com | 6:00 | ekran | evet |
| https://console.cloud.google.com/apis/api/gmail.googleapis.com/overview | 6:08 | ekran | evet |
| https://console.cloud.google.com/apis/api/sheets.googleapis.com/metrics | 6:10 | ekran | evet |
| https://console.cloud.google.com/apis/api/drive.googleapis.com/metrics | 6:12 | ekran | evet |
| https://console.cloud.google.com/auth/overview | 6:22 | ekran | evet |
| https://console.cloud.google.com/auth/audience | 6:32 | ekran | evet |
| https://console.cloud.google.com/apis/credentials | 6:46 | ekran | evet |
| https://youtube.googleapis.com | 5:32 | ekran | hayır |
| https://accounts.google.com | 7:40 | ekran | hayır |
| https://drive.google.com/drive/u/3/folders/1b-k8-HuHUiUsl7So11bHaorVX1TmN0K | 9:12 | ekran | hayır |
| https://docs.google.com/spreadsheets/d/1hgX8-4lzh5_DcZ8AuriGZbxJKfhZqll0T757FG8QpTM/edit | 9:18 | ekran | evet |
| https://docs.google.com/document/d/1cchbtV-AAwCFWfPofSWB5CP57o7trlJt/edit | 1:14 | ekran | hayır |
| https://mail.google.com/mail/u/3/#drafts | 1:36 | ekran | evet |
| https://www.google.com/search?q=download+claude+desktop | 2:34 | ekran | hayır |
| https://drive.google.com/file/d/1uWmmg9B92Glyg1Y6HJvKNEf4rOgnXX2Y/view | 13:28 | ekran | hayır |
| https://docs.google.com/document/d/17vfGp4ogVOQX0a_CNvie6l-4NNUvimCsGV5jnqqC8/edit | 13:10 | ekran | hayır |
| https://drive.google.com/file/d/14vJ2SKXr8tTkm7GZdlxZDpGiHAg_NRR4/view | 17:08 | ekran | hayır |
| https://21st.dev | 8:08 | ekran | hayır |
## İş akışı
- 1. adım — Claude Desktop indirilip kuruldu, hesapla giriş yapıldı — araçlar: Claude Desktop
- 2. adım — Claude Code sekmesinde yerel 'teklif-kutusu' klasörü seçilip yeni sohbet açıldı — araçlar: Claude Code, Opus 5
- 3. adım — Google Workspace CLI ve beş gws skill'i kurduruldu — araçlar: Google Workspace CLI, npm, Skills CLI
- 4. adım — Cloud Console'da yeni proje açılıp Gmail, Sheets, Docs, Drive API'leri etkinleştirildi — araçlar: Google Cloud Console, Gmail API, Google Sheets API, Google Docs API, Google Drive API
- 5. adım — OAuth onay ekranı ve Desktop App istemcisi oluşturuldu, JSON indirilip .config\gws\client_secret.json olarak kaydedildi — araçlar: Google Cloud Console, OAuth
- 6. adım — CMD'de gws auth login ile hesap bağlandı, bağlantı doğrulandı — araçlar: gws auth login, Google Workspace CLI
- 7. adım — Dolu teklif ve Excel listesi Drive'a yüklendi, liste Google Sheets'e çevrildi, aylık klasör oluşturuldu — araçlar: Claude Code, Google Drive, Google Sheets
- 8. adım — Dolu teklif yer tutuculu şablona çevrildi; geçerlilik tarihi sorusu yanıtlandı — araçlar: Claude Code, Google Docs
- 9. adım — İlk firma için şablon kopyalanıp dolduruldu, tabloda durum ve link güncellendi — araçlar: Claude Code, Google Docs, Google Sheets
- 10. adım — Belge PDF'e çevrilip aylık klasöre kaydedildi, pdf sütununa link yazıldı — araçlar: Claude Code, Google Drive, Google Sheets
- 11. adım — PDF ekli Gmail taslağı hazırlanıp durum 'Taslak hazır' yapıldı, taslak kontrol edildi — araçlar: Claude Code, Gmail
- 12. adım — Konuşma 'teklif-kutusu' skill'ine dönüştürüldü — araçlar: Claude Code, Claude Skills, teklif-kutusu
- 13. adım — Yeni sohbette /teklif-kutusu çalıştırıldı; Yıldız Reklam için belge, PDF, tablo ve taslak doğrulandı — araçlar: teklif-kutusu, Google Docs, Google Sheets, Gmail
## Promptlar
- Google Workspace CLI kurulumu — Bilgisayara Google Workspace komut satırı aracını kur ve hazır hale getir; global kur, sürümü doğrula, yalnızca beş gws skill'ini ekle, hesap bağlamayı adım adım anlat ama girişi kendin yapma.
- Dosyaları Drive'a yükleme ve tabloyu dönüştürme — Yüklenen dolu teklifi ve Excel tablosunu Drive'da 'Teklif Kutusu' klasörüne yükle, Excel'i Google Sheets'e çevir (Musteriler), orijinal adını değiştir, ayar dosyasında kimlikleri sakla.
- Şablon oluşturma — Dolu teklifi, müşteri sütunlarına göre yer tutuculu tekrar kullanılabilir şablona çevir; fiyat tablosuna dokunma, ne değiştiğini raporla, geçerlilik tarihini gönderim tarihi +1 ay yap.
- İlk firma için teklif üretimi — Şablonu kullanarak listedeki ilk 'Bekliyor' firma için teklif hazırla: kopya çıkar, alanları doldur, aylık klasöre taşı, tabloda durumu 'Belge hazır' yap, tarih ve linki yaz; belirsizlikte sor.
- PDF üretimi — Bu belgenin PDF'ini al, aynı ay klasörüne belgeyle aynı adla koy ve ana listede o firmanın pdf sütununa linki yaz.
- Gmail taslağı — Firma yetkilisine e-posta hazırla, gönderme, taslak bırak; PDF'i ekle; durumu 'Taslak hazır' yap.
- Akışı skill'e çevirme — Bu sohbetteki işi kalıcı yap: 'teklif-kutusu' adlı skill oluştur; çağrıldığında 'Bekliyor' durumundaki ilk firma için baştan sona tüm adımları yapsın.
ikinci göz KAPALI: --ikinci-goz yok
