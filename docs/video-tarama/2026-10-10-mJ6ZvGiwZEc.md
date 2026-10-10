# Claude Motion Explained: Make Videos Inside Claude
## Künye
Claude Motion Explained: Make Videos Inside Claude · Leonardo Grigorio | Build & Ship with AI · süre: 4:27 · en-orig · https://youtu.be/mJ6ZvGiwZEc · şema 2
motor: parti 2026-10-10-short-11 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 88365 tk · claude-haiku-5-5: claude-haiku-5-5 · 90199 tk
## Özet
Video, Anthropic'in 8 Ekim'de Claude Dashboards ile birlikte beta olarak çıkardığı Claude Motion özelliğini anlatıyor. Motion bir video üretim modeli kullanmıyor. Claude metin, grafik, şekil ve görselleri canlandıran kod yazıyor. Özellik yalnızca Team ve Enterprise planlarında var. /motion yazarak ya da Output > Motion ile başlatılıyor. Sohbetle ya da editörle düzenleniyor, MP4 olarak dışa aktarılıyor veya Adobe, Descript, Runway gibi araçlarda açılıyor. Video bunu Claude Code + Remotion, HeyGen HyperFrames ve HTML + FFmpeg skill yöntemleriyle karşılaştırıyor. Bu yöntemlerde her kare zamanın fonksiyonu olarak yazılıyor, başsız tarayıcı kareleri ekran görüntüsü olarak alıyor, FFmpeg de MP4'e birleştiriyor. Motion'da ses, toplu render ve kendi repo yok. Team koltuk başı aylık 20 dolar, en az 2 koltuk, yaklaşık 40 dolar. Remotion 3 kişiye kadar ücretsiz, HyperFrames ücretsiz ve açık kaynak, Claude Code Pro'da aylık 17 dolardan başlıyor.
## Bölümler
- 0:00 Claude Motion nedir
- 0:37 Kimler kullanabilir
- 0:56 Üret, düzenle, dışa aktar
- 1:48 Geliştiriciler bunu daha önce nasıl yapıyordu
- 2:56 Ne kazanılır, ne kaybedilir
- 3:29 Maliyet
- 3:53 Remotion hâlâ gerekli mi
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Motion | yok | iş akışı | yok | Prompttan ya da rapordan kodla animasyonlu video üreten Anthropic beta özelliği | 0:42 | Tabloda Claude Motion (beta) satırı; Team ve Enterprise işaretli (karede: Plan tablosunda 'Claude Motion (beta)' satırı, Free/Pro/Max için çarpı, Team/Enterprise için onay) |
| Claude Code | yok | CLI | yok | Remotion ve HyperFrames ile video kodlatmak için kullanılan kodlama ajanı | 0:14 | Karede 'Claude Code + Remotion' yazıyor (karede: Claude logosu ve 'Claude Code + Remotion' yazısı) |
| Remotion | yok | teknik | https://github.com/remotion-dev/remotion | React tabanlı video çerçevesi; Claude Code için skills yayınladı | 1:58 | Zaman çizelgesinde Jan: Agent Skills ve remotion-dev/skills komutu (karede: Çizelgede Jan işareti, Agent Skills etiketi ve 'npx skills add remotion-dev/skills') |
| HyperFrames | yok | teknik | https://github.com/heygen-com/hyperframes | HeyGen'in açık kaynak HTML'den MP4'e çerçevesi | 2:02 | Apr işaretinde HeyGen HyperFrames, 'HTML -> MP4' (karede: Çizelgede Apr altında 'HeyGen HyperFrames' logosu ve 'HTML -> MP4') |
| FFmpeg | yok | CLI | yok | Ekran görüntülerini MP4'e birleştiren araç | 2:50 | 300 kare ve FFmpeg oku dosyaya iniyor (karede: '300 frames, 10 s at 30fps' ve aşağı oklu 'FFmpeg') |
| Node.js | yok | teknik | yok | Remotion ve HyperFrames için gereken çalışma ortamı | 2:57 | DIY sütununda Node.js kutusu (karede: Setup satırında DIY altında 'Node.js' ve 'coding agent' kutuları) |
| npm | yok | CLI | yok | Kurulum adımı olarak gösterilen paket yöneticisi | 0:14 | Kurulum kutuları arasında 'npm install' (karede: 'render', 'npm install', 'FFmpeg', 'Node.js' kutuları ve 'setup' yazısı) |
| Agent Skills | yok | skill | yok | Remotion'un Claude Code için çıkardığı skill paketi | 1:58 | Jan işaretinde 'Agent Skills' etiketi (karede: Mavi Remotion ikonu üstünde 'Agent Skills') |
| SKILL.md | yok | skill | yok | HTML ve FFmpeg üzerine kurulu talimat dosyası yaklaşımı | 2:24 | Çizelgede SKILL.md dosyası, HTML ve FFmpeg etiketleri · kanıt: kare (karede: 'SKILL.md' belgesi, üstünde 'HTML' ve 'FFmpeg' kutuları) |
| Opus 5.5 | yok | CLI | yok | Eylül'de çıkan ve üç dakikalık kodla yapılmış AI tarihi videosunda anılan model | 2:24 | Sep işaretinde 'Opus 5.5' ve '100% code' (karede: Sep altında 'Opus 5.5' kutusu ve 3:00 süreli video, '100% code') |
| Sonnet 5.5 | yok | CLI | yok | Motion arayüzünde seçili model | 0:17 | Mesaj kutusunun altında 'Sonnet 5.5 Med' (karede: Mesaj kutusu, solda 'Project or folder', sağda 'Sonnet 5.5 Med') |
| Claude Dashboards | yok | iş akışı | yok | Motion ile aynı gün çıkan pano özelliği | 0:19 | Oct 8 etiketinde Bike share panosu görünüyor (karede: Oct 8 etiketi, solda 'System overview' panosu, sağda Motion mesaj kutusu) |
| Headless browser | yok | teknik | yok | Her anı ekran görüntüsüne çeviren pencerisiz tarayıcı | 2:36 | 'headless browser' ve 'no window' etiketi (karede: Kesikli kutuda 'headless browser', altında 'no window') |
| frame = f(t) | yok | teknik | yok | Her karenin zamanın fonksiyonu olduğu render yaklaşımı | 2:31 | Sayfa altında turuncu 'frame = f(t)' ve zaman kaydırıcısı (karede: 'page' kutusu, turuncu 'frame = f(t)' ve t kaydırıcısı) |
| Adobe | yok | iş akışı | yok | MP4'ün açılabildiği dışa aktarma hedefi | 1:27 | MP4'ten Adobe'ye ok (karede: Adobe logosu ve MP4 dosyasından ona giden ok) |
| Descript | yok | iş akışı | yok | MP4'ün açılabildiği dışa aktarma hedefi | 1:29 | Descript logosu ok ucunda (karede: Üstte Descript logosu, yanında Runway ve Adobe) |
| Runway | yok | iş akışı | yok | MP4'ün açılabildiği dışa aktarma hedefi | 1:29 | Runway logosu görünüyor (karede: Sağ üstte Runway logosu) |
| HeyGen | yok | iş akışı | yok | Dışa aktarma hedefi; HyperFrames'in geliştiricisi | 1:30 | HeyGen logosu sol altta (karede: Sol altta HeyGen logosu, çevrede yedi hedef) |
| Higgsfield | yok | iş akışı | yok | MP4'ün açılabildiği dışa aktarma hedefi | 1:30 | Higgsfield logosu (karede: Altta yeşil Higgsfield logosu) |
| invideo | yok | iş akışı | yok | MP4'ün açılabildiği dışa aktarma hedefi | 1:30 | invideo logosu (karede: Altta invideo logosu) |
| Luma AI | yok | iş akışı | yok | MP4'ün açılabildiği dışa aktarma hedefi | 1:30 | Luma AI logosu (karede: Sağ altta Luma AI logosu) |
| Skills CLI | yok | CLI | yok | npx skills add komutuyla skill paketlerini Claude Code'a ekleyen komut satırı aracı. | 1:58 | npx skills add remotion-dev/skills (karede: Zaman çizelgesinde 'Agent Skills' etiketi altında 'npx skills add remotion-dev/skills' yazısı.) |
| Sora | yok | teknik | yok | Video üretim modeli; Motion'ın bunun gibi olmadığı karşıtlık olarak anılıyor. | 0:00 | picture a board slide that moves, not Sora. |
| Üç aylık rapordan Motion videosu üretmek | yok | prompt | yok | Ekli üç aylık raporu, tüm çalışanlar toplantısı için 30 saniyelik animasyonlu bir açıklayıcı videoya çevir. | 1:06 | kaynak: kare |
| Sohbetle animasyonu düzenlemek | yok | prompt | yok | Videodaki Q3 değerini yüzde 18 olarak değiştir; geri kalan aynı kalsın. | 1:18 | kaynak: kare |
| Fiyat karşılaştırma animasyonu örneği (Anthropic'in örneği) | yok | prompt | yok | Satış başlangıç toplantısı için fiyat planlarının nasıl karşılaştırıldığını canlandır. | 1:32 | kaynak: altyazı |
## Açıklama bağlantıları
- https://claude.com/resources/articles/dashboards-and-motion — Anthropic'in Dashboards ve Motion duyuru yazısı · aday: evet (Claude Motion) · Alan adı Claude'u adlandırıyor, sayfa videonun konusu Claude Motion'ı anlatıyor · sınıf: diğer
- https://support.claude.com/en/articles/17454997-get-started-with-claude-motion — Claude Motion başlangıç yardım sayfası · aday: evet (Claude Motion) · İzleyicinin kullanabileceği aracın resmi yardım sayfası · sınıf: diğer
- https://claude.com/pricing — Claude fiyatlandırma sayfası · aday: evet (Claude Motion) · Alan adı Claude servisini adlandırıyor, planlar videoda karşılaştırılıyor · sınıf: diğer
- https://www.remotion.pro/license — Remotion lisans sayfası · aday: evet (Remotion) · Alan adı videoda anlatılan Remotion'u adlandırıyor · sınıf: diğer
- https://github.com/heygen-com/hyperframes — HyperFrames GitHub deposu · aday: evet (HyperFrames) · Videoda anlatılan açık kaynak aracın deposu · sınıf: diğer
- https://www.heygen.com/research/html-to-video — HeyGen HTML'den videoya araştırma yazısı · aday: evet (HeyGen) · Alan adı videoda gösterilen HeyGen'i adlandırıyor, HyperFrames'i anlatıyor · sınıf: diğer
## Site/UI teknikleri
- EKSİK: formda site/UI tekniği yok (kısmi kabul)
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| /motion | Claude mesaj kutusunda Motion animasyon çıktısını başlatır (karede: Mesaj kutusunda '/motion' yazısı ve üstte Motion öğesi) | 1:01 | kare |
| npx skills add remotion-dev/skills | Remotion'un Claude Code için agent skills paketini ekler (karede: Jan işareti altında 'npx skills add remotion-dev/skills' etiketi) | 1:58 | kare |
| npm install | Kurulum adımı örneği olarak gösterilen paket kurulumu (karede: 'npm install' kutusu, 'render', 'FFmpeg', 'Node.js' kutularıyla) | 0:14 | kare |
| /motion Turn this quarterly report into a 30-second explainer for our all-hands. | Ekli raporu 30 saniyelik açıklayıcı animasyona çevirmesini ister. (karede: Mesaj kutusunda 'Q3 report.pdf' eki ve '/motion Turn this quarterly report into a 30-second explainer' yazısı.) | 1:06 | kare |
| render | Remotion ile videoyu işleyip MP4 üretir (ekranda etiket olarak gösteriliyor; tam komut gösterilmiyor). (karede: Kurulum etiketleri listesinde 'render' yazısı.) | 0:14 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Motion video üretim modeli kullanmıyor; metin, grafik, şekil ve görselleri canlandırıyor | 0:19 | özellik |
| Motion beta aşamasında ve yalnızca Team ile Enterprise planlarında; Free, Pro, Max'te yok | 0:42 | özellik |
| Team koltuk başı aylık 20 dolar, yıllık faturalı, en az 2 koltuk; tek kişi yaklaşık 40 dolar öder | 3:39 | sayısal |
| 10 saniyelik klip 30 fps'te 300 ekran görüntüsüdür | 2:53 | sayısal |
| Remotion 3 kişiye kadar ücretsiz, HyperFrames ücretsiz ve açık kaynak | 3:49 | karşılaştırma |
| Motion'da ses ve toplu render dokümanlarda yok; Remotion ve HyperFrames'te var | 3:14 | karşılaştırma |
| Claude Code, Pro planda yıllık faturalı aylık 17 dolardan başlıyor | 3:49 | sayısal |
| Pro veya Max'tekiler Remotion, HyperFrames ya da bir skill kullanmalı | 4:06 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Claude Motion | Claude Motion | Motion bir prompt ya da raporu video yapıyor |
| kare 0:14 | Claude Code + Remotion | Claude Code | Karede Claude Code + Remotion yazıyor |
| kare 0:14 | Remotion | Remotion | Claude Code + Remotion etiketi |
| kare 0:14 | npm install | npm | Kurulum kutuları arasında |
| kare 0:14 | Node.js ve FFmpeg | Node.js | Setup kutuları; FFmpeg ayrıca aday |
| kare 0:17 | Sonnet 5.5 Med | Sonnet 5.5 | Mesaj kutusu model seçici |
| konuşma 0:19 | Claude dashboards | Claude Dashboards | Motion ile aynı gün çıktı |
| konuşma 0:19 | Sora | aday değil: konu dışı | Yalnızca 'Sora değil' karşılaştırması |
| kare 0:19 | video model, footage, people | aday değil: genel kavram | Motion'un yapmadıkları listesi |
| kare 0:42 | Free, Pro, Max, Team, Enterprise planları | aday değil: genel kavram | Plan tablosu |
| kare 1:06 | Q3 report.pdf | aday değil: genel kavram | Örnek ek dosya |
| kare 1:22 | Editör | Claude Motion | 'or: the editor' etiketi |
| kare 1:27 | Adobe | Adobe | Dışa aktarma hedefi |
| kare 1:29 | Descript | Descript | Dışa aktarma hedefi |
| kare 1:29 | Runway | Runway | Dışa aktarma hedefi |
| kare 1:30 | HeyGen | HeyGen | Dışa aktarma hedefi ve HyperFrames sahibi |
| kare 1:30 | Higgsfield | Higgsfield | Dışa aktarma hedefi |
| kare 1:30 | invideo | invideo | Dışa aktarma hedefi |
| kare 1:30 | Luma AI | Luma AI | Dışa aktarma hedefi |
| kare 1:36 | Get set up ve Compare plans örnek animasyonları | aday değil: genel kavram | Anthropic'in örnek çıktıları |
| kare 1:58 | Agent Skills / remotion-dev/skills | Agent Skills | npx skills add komutu |
| kare 2:02 | HyperFrames | HyperFrames | Apr işaretinde HeyGen HyperFrames |
| kare 2:24 | SKILL.md, HTML, FFmpeg | SKILL.md | Çizelgede SKILL.md dosyası |
| kare 2:24 | Opus 5.5 | Opus 5.5 | Sep işaretinde etiket |
| kare 2:31 | frame = f(t) | frame = f(t) | Render yaklaşımı |
| kare 2:36 | headless browser | Headless browser | Etiket ve 'no window' |
| kare 2:53 | FFmpeg | FFmpeg | 300 kareyi MP4'e birleştirir |
| kare 2:57 | coding agent | aday değil: genel kavram | Genel terim, DIY yol gereksinimi |
| konuşma 3:14 | Artifacts sekmesi | aday değil: başka adayın parçası (Claude Motion) | Animasyonlar orada duruyor |
| kare 3:39 | Team fiyatı | aday değil: genel kavram | Plan fiyatı bilgisi |
| açıklama | claude.com makalesi, support.claude.com yardım, claude.com/pricing | Claude Motion | Açıklama bağlantıları |
| açıklama | remotion.pro/license | Remotion | Açıklama bağlantısı |
| açıklama | github.com/heygen-com/hyperframes ve heygen.com araştırma sayfası | HyperFrames | Açıklama bağlantıları |
| açıklama | Apache-2.0 lisansı | aday değil: genel kavram | HyperFrames lisansı |
| linkli sayfa claude.com/pricing | platform.claude.com, docs.claude.com bağlantıları | aday değil: konu dışı | Fiyat sayfasındaki API dokümanları, videoda kullanılmadı |
| linkli sayfa remotion.pro/license | remotion.dev, remotion-dev/remotion LICENSE, docs, license FAQ | Remotion | Remotion lisans sayfasının bağlantıları |
| yorum | Remotion, Hyperframes, voiceover sorusu | Remotion | Yorumcu videoyu nasıl yaptığını soruyor |
| yorum | Claude desktop uygulaması ve terminal sorusu | aday değil: konu dışı | Videoda cevaplanmayan izleyici sorusu |
## Kareden okunanlar
- 0:00: Başlık 'Claude Motion turns reports into videos'; Q3 all-hands explainer, Revenue growth Q1 8%, Q2 6%
- 0:12: 'const q = [9, 12, 14];' kod bloğu, '<Title>Revenue growth</Title>', '<Bars values={q} />'
- 1:01: Mesaj kutusunda '/motion', 'or: Output > Motion', 'Sonnet 5.5 Med'
- 1:22: Diff: '- q3: 14' ve '+ q3: 18'; 'it's code', 'or: the editor'
- 1:36: 'Get set up' 3 adımlı listesi ve 'Compare plans' Starter/Team/Scale
- 1:58: 'npx skills add remotion-dev/skills' komutu, 'Agent Skills', Jan/Apr/Oct 8 çizelgesi
- 2:49: 'engine: not said' etiketi Motion kutusunun altında
- 4:06: 'owner turns it on', 'on by default', 'a chart', 'a walkthrough'
## Belirsizlikler
- Sözlük eşleşmeleri Framer Motion, Emotion, Next.js, Chart.js, Three.js ve benzerleri videoda gösterilmedi; yanlış eşleşme sayıldı.
- Sora yalnızca 'Sora değil' karşılaştırması olarak geçiyor; kullanılmadığı için aday yapılmadı.
- Motion'un arka planda ne çalıştırdığı belli değil; Anthropic söylemiyor ('engine: not said').
- Fiyat planlarını gösteren pricing sayfası claude.com üzerinde; Team/Enterprise planlarının ayrıntısı videoda yalnızca özetlendi.
- Altyazıdaki 'Remotion' ekranda 'Remotion' yerine 'Remotion/Remotion' diye de okunuyor; kare metninde 'Remotion' yazımı kullanıldı.
- Açıklamadaki Nodeless yorum sorusu (Claude Code terminalinde yapılır mı) videoda yanıtlanmadı.
- EKSİK: rapor (bölüm eksik: ## Site/UI teknikleri)
## Atlanan segment oranı
0/8 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://claude.com/resources/articles/dashboards-and-motion | açıklama | açıklama | evet |
| https://support.claude.com/en/articles/17454997-get-started-with-claude-motion | açıklama | açıklama | evet |
| https://claude.com/pricing | açıklama | açıklama | evet |
| https://www.remotion.pro/license | açıklama | açıklama | evet |
| https://github.com/heygen-com/hyperframes | açıklama | açıklama | evet |
| https://www.heygen.com/research/html-to-video | açıklama | açıklama | evet |
## İş akışı
- 1. adım — Claude'da mesaj kutusuna /motion yazılır ya da Output altından Motion seçilir — araçlar: Claude Motion
- 2. adım — Q3 raporu PDF olarak eklenip 30 saniyelik açıklayıcı video istenir — araçlar: Claude Motion, Sonnet 5.5
- 3. adım — Animasyon sohbetin yanında kendi penceresinde açılır ve önizlenir — araçlar: Claude Motion
- 4. adım — Yanlış Q3 değeri sohbetten yüzde 18 olarak düzeltilir — araçlar: Claude Motion
- 5. adım — İstenirse değer editörde kodda elle düzeltilir — araçlar: Claude Motion
- 6. adım — Video MP4 olarak dışa aktarılır, paylaşılır ya da Adobe, Descript, Runway, HeyGen, Higgsfield, invideo, Luma AI'da açılır — araçlar: Claude Motion, Adobe, Descript, Runway, HeyGen, Higgsfield, invideo, Luma AI
- 7. adım — Karşılaştırma için DIY yol: Claude, her karesi zamanın fonksiyonu olan bir sayfa yazar — araçlar: Claude Code, Remotion, HyperFrames
- 8. adım — Başsız tarayıcı her ana gidip ekran görüntüsü alır — araçlar: Headless browser
- 9. adım — FFmpeg kareleri MP4'e birleştirir — araçlar: FFmpeg
## Promptlar
- Üç aylık rapordan Motion videosu üretmek — Ekli üç aylık raporu, tüm çalışanlar toplantısı için 30 saniyelik animasyonlu bir açıklayıcı videoya çevir.
- Sohbetle animasyonu düzenlemek — Videodaki Q3 değerini yüzde 18 olarak değiştir; geri kalan aynı kalsın.
- Fiyat karşılaştırma animasyonu örneği (Anthropic'in örneği) — Satış başlangıç toplantısı için fiyat planlarının nasıl karşılaştırıldığını canlandır.
