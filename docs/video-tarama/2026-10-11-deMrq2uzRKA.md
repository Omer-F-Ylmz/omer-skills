# Michael Truell: How Cursor Builds at the Speed of AI
## Künye
Michael Truell: How Cursor Builds at the Speed of AI · a16z · süre: 27:39 · en-orig · https://youtu.be/deMrq2uzRKA · şema 2
motor: parti 2026-10-11-short-4 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 58367 tk · claude-haiku-5-5: claude-haiku-5-5 · 71090 tk
## Özet
a16z Runtime sahnesinde Martin Casado, Cursor kurucu ortağı ve CEO'su Michael Truell ile konuşuyor. Truell, şirketin 3B/CAD (mekanik mühendislik) yan girişimiyle başlangıcını, VS Code'a odaklanıp düzenleyiciyi kendilerinin sahiplenme kararını ve haftalar içinde çıkan ilk sürümü anlatıyor. Ölçekleme sorunlarını (Kubernetes, veritabanı, API sağlayıcı kapasitesi, token satıcıları), çoklu bulut düzenini, çoklu ürün stratejisini (Bugbot, CLI), iki günlük iş denemesine dayalı işe alımı, satın almaları (Supermaven) ve 'yazılım kendini mi yok ediyor' sorusunu ele alıyor. Teknik bir uygulama gösterimi ya da kurulum komutu yok; röportaj formatı.
## Bölümler
- 0:00 Cursor for X çerçevesi
- 3:17 Kör adam ve fil sorunu
- 3:54 Keşke stajyer olsaydık
- 4:15 Odak ve bilim kurgu
- 6:00 Modelleme işinden kalan travma, pratiklik
- 7:00 Aylık yatırımcı güncellemesi taahhüt aracı
- 7:18 İki haftada günlük kullanılan IDE
- 8:48 Komut satırı Vim kullanan Luddite'lerdik
- 9:44 Pencereye iPad: Cursor çöktü
- 11:58 Dört yirmili yaşta genç, çift haneli API geliri
- 12:44 Ölçekte çıkarım kapasitesi bulmak
- 18:16 200+ kişide iki günlük iş denemesi
- 20:39 Gelen müşteri adayları, kotanız var
- 22:11 Hayır dedikten sonra dünyanın öbür ucuna uçmak
- 24:46 Ouroboros sorusu
- 25:26 Otomasyondan çok uzağız
- 26:04 iPod anından iPhone anlarına
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Cursor | yok | teknik | yok | Röportajın konusu olan yapay zekâ destekli kod düzenleyici ve şirket | 0:00 | Please join us in welcoming to stage Michael Troll, co-founder and CEO of Cursor |
| GitHub Copilot | yok | teknik | yok | Kurucuları şirket kurmaya iten ilk faydalı yapay zekâ ürünü, pazardaki rakip | 1:45 | trying GitHub Copilot, the incumbent in our space |
| VS Code | yok | teknik | yok | Cursor'ın üzerine fork edildiği düzenleyici; erken odak noktası | 5:00 | You chose VS Code |
| Vim | yok | CLI | yok | Kurucuların Copilot öncesi kullandığı komut satırı düzenleyici | 9:20 | we were all like using command line Vim |
| IntelliJ | yok | teknik | yok | Rakiplerin entegre olmaya çalıştığı IDE; Cursor bunu yapmamayı seçti | 8:18 | they would like integrate with IntelliJ or whatever it was |
| Kubernetes | yok | teknik | yok | Çok büyük bir küme olarak işletilen ölçekleme altyapısı | 11:58 | we were running a very large Kubernetes cluster |
| CoreDNS | yok | teknik | yok | Kubernetes tarafında çöken ve sorun yaratan DNS bileşeni | 14:46 | there was a whole Kubernetes side of things, like CoreDNS going down |
| AWS | yok | teknik | yok | Web için kullanılan bulut sağlayıcılardan biri; RDS ve Limitless sorunları | 14:20 | we're on AWS, GCP, and Azure for sell for web stuff |
| GCP | yok | teknik | yok | Çoklu bulut düzeninde kullanılan sağlayıcı | 14:20 | we're on AWS, GCP, and Azure |
| Azure | yok | teknik | yok | Çoklu bulut düzeninde kullanılan sağlayıcı | 14:20 | we're on AWS, GCP, and Azure |
| Databricks | yok | teknik | yok | Kullanılan veri platformu sağlayıcılarından biri | 14:15 | We have Databricks, Snowflake |
| Snowflake | yok | teknik | yok | Kullanılan veri platformu sağlayıcılarından biri | 14:15 | We have Databricks, Snowflake |
| PlanetScale | yok | teknik | yok | Veritabanı ölçekleme sorununu çözen yönetilen veritabanı servisi | 15:10 | we went from limitless to PlanetScale |
| AWS RDS | yok | teknik | yok | İlk aşamada ölçeklenen yönetilen veritabanı örneği | 14:55 | usually you should just scale the RDS instance · kanıt: yok |
| Aurora Limitless | yok | teknik | yok | AWS'in shard etmeye gerek bırakmadığını iddia eden ama işe yaramayan servisi (adı 'limitless' olarak geçiyor) | 15:10 | we went from limitless to PlanetScale · kanıt: yok |
| Claude Sonnet | yok | teknik | yok | Birden çok sağlayıcıdan toplanan API tokenlarının modeli | 13:10 | hunting out all the Sonnet tokens that exist in the world |
| Token resellers | yok | teknik | yok | Aynı modelin tokenlarını farklı sağlayıcı ve satıcılardan toplama yöntemi | 12:44 | there are token resellers that exist out there |
| Bugbot | yok | teknik | yok | Cursor'ın kod inceleme/ekip iş birliği tarafındaki ek ürünü | 15:48 | You did Bugbot, you did CLI |
| Cursor CLI | yok | CLI | yok | Cursor'ın çoklu ürün stratejisindeki komut satırı ürünü | 15:48 | You did Bugbot, you did CLI · kanıt: yok |
| Supermaven | yok | teknik | yok | Cursor'ın ilk gerçek satın alması; otomatik tamamlama modeli ekibi | 24:13 | The first real M&A we did was, Supermaven |
| Tabnine | yok | teknik | yok | Supermaven kurucusunun daha önce geliştirdiği otomatik tamamlama aracı | 24:20 | It was started by the person who had built Copilot... which was Tabnine |
| İki günlük iş denemesi | yok | iş akışı | yok | Adayın ofiste iki gün gerçek proje üzerinde çalıştığı işe alım süreci | 18:16 | everyone who gets hired on the eng team and the design team spends two days in office · kanıt: yok |
## Açıklama bağlantıları
- https://x.com/mntruell — Michael Truell'in X profili · aday: hayır · Kişi profili; izleyicinin kullanacağı bir araç değil, videoda kullanılmıyor. · sınıf: diğer
- https://x.com/a16z — a16z'nin X hesabı · aday: hayır · Kurum sosyal medya hesabı; araç değil. · sınıf: diğer
- https://www.linkedin.com/company/a16z — a16z LinkedIn şirket sayfası · aday: hayır · Kurum sayfası; videoda kullanılan araç değil. · sınıf: diğer
- https://open.spotify.com/show/5bC65RDvs3oxnLyqqvkUYX — a16z podcast'inin Spotify sayfası · aday: hayır · Podcast dinleme sayfası; Spotify videoda kullanılmıyor veya anlatılmıyor. · sınıf: diğer
- https://podcasts.apple.com/us/podcast/a16z-podcast/id842818711 — a16z podcast'inin Apple Podcasts sayfası · aday: hayır · Podcast dinleme sayfası; Apple Podcasts videoda kullanılmıyor veya anlatılmıyor. · sınıf: diğer
- https://x.com/eriktorenberg — Erik Torenberg'in X profili · aday: hayır · Kişi profili; araç değil, videoda geçmiyor. · sınıf: diğer
## İddialar
| iddia | zaman | tür |
|---|---|---|
| İlk IDE, karar verildikten birkaç hafta içinde kuruculara günlük kullanımda hizmet etti; toplamda birkaç ayda ilk beta yayımlandı. | 7:18 | sayısal |
| Cursor başlangıçta VS Code'u fork etmedi, IDE'yi sıfırdan yazdı. | 7:18 | özellik |
| Cursor'ın API payı, sağlayıcıların API gelirinin çok yüksek bir çift haneli yüzdesini oluşturuyor. | 12:44 | sayısal |
| Çok büyük bir Kubernetes kümesi yalnızca beş kişilik ekiple yönetildi. | 11:58 | sayısal |
| AWS'in shard gerektirmediğini söyleyen servisi işe yaramadı; PlanetScale'e geçildi. | 15:10 | karşılaştırma |
| Aynı model tokenları birden çok sağlayıcıdan ve satıcıdan alınıp dağıtılması stratejik olarak faydalı. | 12:44 | öneri |
| Cursor artık kendi modellerini eğitiyor ve çıkarımın bir kısmını kendisi yapıyor. | 12:44 | özellik |
| Mühendis ve tasarımcı adayları iki gün ofiste çalışıyor; 4-6 öğün birlikte yeniyor; şirket 200 kişiyi aşmasına rağmen sürdürülüyor. | 19:17 | sayısal |
| İlk satış elemanlarına gerçek gelen müşteri adayları ve kota verildi. | 20:39 | özellik |
| CAD fikri üzerinde yaklaşık 6-7 ay çalışıldı ve bu kötü bir kurucu-pazar uyumuydu. | 4:15 | sayısal |
| Supermaven, beş kişilik bir ekipti ve ilk gerçek satın alma oldu. | 24:13 | sayısal |
| Yazılım geliştirmenin otomasyonundan hâlâ çok uzağız; 'uzun ve dağınık bir ara dönem' var. | 26:04 | karşılaştırma |
| Çoklu ürün şirketi olmak gerekecek, ancak tek üründen çok ürüne geçmek satışa-pazara çıkışta zor. | 15:48 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Cursor | Cursor | Konuşmacı tanıtımında Cursor kurucusu olarak anılıyor |
| kare 0:30 | Michael Truell altyazı bandı | Cursor | Cofounder & CEO, Cursor yazısı |
| kare 0:24 | RUNTIME etkinliği, Sarah Wang, Jennifer Li | aday değil: konu dışı | Etkinlik sunucuları ve etkinlik logosu |
| kare 0:32 | Martin Casado altyazı bandı | aday değil: konu dışı | General Partner, a16z |
| kare 0:20 | The a16z Podcast logosu | aday değil: sponsor/reklam | Kanal marka girişi |
| konuşma 1:02 | 3D şirketi anekdotu | aday değil: konu dışı | Cursor'ın eskiden 3B şirketi olduğu ifadesi |
| konuşma 1:45 | GitHub Copilot | GitHub Copilot | The incumbent in our space |
| konuşma 1:50 | GitHub | aday değil: başka adayın parçası (GitHub Copilot) | Copilot ürününün sahibi şirket adı |
| konuşma 2:03 | Ölçekleme yasaları (scaling laws) | aday değil: genel kavram | Şirket kurma motivasyonu olarak anlatılıyor |
| konuşma 2:03 | Cursor for X çerçevesi | aday değil: genel kavram | Dikey bilgi işi için şirket modeli |
| konuşma 3:54 | CAD systems | aday değil: genel kavram | Bırakılan mekanik mühendislik fikri |
| konuşma 3:17 | Microsoft | aday değil: konu dışı | Rakip olarak anılıyor |
| konuşma 5:00 | VS Code | VS Code | You chose VS Code |
| konuşma 7:18 | Aylık yatırımcı güncellemesi | aday değil: genel kavram | Taahhüt aracı olarak anılıyor |
| konuşma 8:18 | IntelliJ | IntelliJ | Rakiplerin entegre olduğu IDE |
| konuşma 8:18 | C library | aday değil: konu dışı | Rakiplerin genişleme örneği olarak geçiyor |
| konuşma 9:20 | Vim | Vim | command line Vim |
| konuşma 9:44 | iPad 'Cursor's down' | aday değil: konu dışı | Kesinti anekdotu |
| konuşma 11:30 | Mini Dropboxes dosya senkron sistemi | aday değil: başka adayın parçası (Cursor) | Cursor içindeki dosya senkron ve arama motoru |
| konuşma 11:58 | Kubernetes | Kubernetes | very large Kubernetes cluster |
| konuşma 12:44 | Token resellers | Token resellers | Token satıcıları anlatılıyor |
| konuşma 13:10 | Sonnet tokens | Claude Sonnet | hunting out all the Sonnet tokens |
| konuşma 14:15 | Databricks | Databricks | We have Databricks, Snowflake |
| konuşma 14:15 | Snowflake | Snowflake | We have Databricks, Snowflake |
| konuşma 14:20 | AWS | AWS | we're on AWS, GCP, and Azure |
| konuşma 14:20 | GCP | GCP | we're on AWS, GCP, and Azure |
| konuşma 14:20 | Azure | Azure | we're on AWS, GCP, and Azure |
| konuşma 14:30 | PlanetScale | PlanetScale | we use PlanetScale for databases |
| konuşma 14:46 | CoreDNS | CoreDNS | CoreDNS going down |
| konuşma 14:55 | RDS | AWS RDS | scale the RDS instance |
| konuşma 15:10 | Limitless | Aurora Limitless | we went from limitless to PlanetScale |
| konuşma 15:15 | Sam (PlanetScale) | aday değil: konu dışı | Seyirciden teşekkür edilen kişi |
| konuşma 15:48 | Bugbot | Bugbot | You did Bugbot, you did CLI |
| konuşma 15:48 | CLI | Cursor CLI | You did Bugbot, you did CLI |
| konuşma 16:49 | PLG büyüme mühendisliği | aday değil: genel kavram | Çapraz satış yaklaşımı olarak anılıyor |
| konuşma 18:16 | İki günlük iş denemesi | İki günlük iş denemesi | two days in office |
| konuşma 18:46 | LeetCode tarzı mülakat | aday değil: genel kavram | Alternatif olarak anılan klasik mülakat |
| konuşma 22:11 | Satın alma (M&A) | aday değil: genel kavram | Startupların startup alması tartışması |
| konuşma 24:13 | Supermaven | Supermaven | first real M&A we did was, Supermaven |
| konuşma 24:20 | Tabnine | Tabnine | which was Tabnine |
| konuşma 24:20 | OpenAI | aday değil: konu dışı | Supermaven kurucusunun eski işyeri |
| konuşma 24:20 | Thinking Machines | aday değil: konu dışı | Kurucunun çalıştığı kişi/ekip olarak anılıyor |
| konuşma 25:26 | Ouroboros sorusu | aday değil: genel kavram | Yazılımı yok eden ürünün yazılımla yazılması |
| konuşma 26:04 | iPod/iPhone benzetmesi | aday değil: genel kavram | Pazar evrimi benzetmesi |
| kare 27:14 | a16z yasal uyarı metni | aday değil: sponsor/reklam | Disclosure ekranı |
| kare 27:24 | Subscribe! düğmesi | aday değil: sponsor/reklam | Kanal abone çağrısı |
| açıklama | https://x.com/mntruell | aday değil: konu dışı | Kişi profili bağlantısı |
| açıklama | https://x.com/a16z | aday değil: konu dışı | Kurum hesabı bağlantısı |
| açıklama | https://www.linkedin.com/company/a16z | aday değil: konu dışı | Kurum sayfası bağlantısı |
| açıklama | Spotify podcast sayfası | aday değil: konu dışı | Podcast dinleme bağlantısı |
| açıklama | Apple Podcasts sayfası | aday değil: konu dışı | Podcast dinleme bağlantısı |
| açıklama | https://x.com/eriktorenberg | aday değil: konu dışı | Kişi profili bağlantısı |
| linkli sayfa | a16z.simplecast.com ve adviserinfo.sec.gov | aday değil: konu dışı | Bağlantılı sayfalarda geçen yayın/yasal uyarı alanları |
| yorum | Claude Code, Codex, Opencode | aday değil: konu dışı | Yalnızca yorumda rakip olarak anılıyor |
| yorum | Windsurf | aday değil: konu dışı | Yalnızca yorumda anılıyor |
| yorum | Lovable, Replit | aday değil: konu dışı | Yalnızca yorumda anılıyor |
| yorum | OpenAI, Anthropic | aday değil: konu dışı | Yalnızca yorumda anılıyor |
| yorum | https://www.youtube.com/watch?v=2x-aQy730Ew | aday değil: konu dışı | Yorumda paylaşılan YouTube bağlantısı |
| yorum | build a better mousetrap deyişi | aday değil: genel kavram | Yorumda ve konuşmada deyim olarak geçiyor |
## Kareden okunanlar
- 0:10: Sahnede iki koltukta Michael Truell ve Martin Casado; arka planda 'PRESENTED BY A16Z' yazısının alt kısmı kesik görünüyor.
- 0:20: Turuncu zeminde 'The a16z Podcast' logosu.
- 0:24: 'RUNTIME</> PRESENTED BY A16Z' ekranı; sahnede iki sunucu, kısmen 'rah Wang' ve 'nnifer Li' ile a16z yazıları.
- 0:30: 'Michael Truell, Cofounder & CEO, Cursor' altyazı bandı.
- 0:32: 'Martin Casado, General Partner, a16' ikinci altyazı bandı.
- 1:24: Truell ve Casado oturuyor; Truell'in alt bandında 'Michael Truell, Cofounder & CEO, Cursor'.
- 1:28: İki konuşmacının alt bandı: Michael Truell ve Martin Casado, General Partner, a16z.
- 27:14: a16z yasal uyarı metni; a16z.com/investments/ ve a16z.com/disclosures bağlantıları görünüyor.
- 27:24: Turuncu zeminde 'Subscribe!' düğmesi ve The a16z Podcast logosu.
## Belirsizlikler
- Sözlük eşleşmelerindeki Three.js, React, Vue, Next.js, Stitch, Descript, Hermes Agent, taste-skill, design-dna, Skills CLI, Meshy vb. videoda geçmiyor; bulanık eşleşme olarak değerlendirilmedi.
- Yorumlarda geçen Claude Code, Codex, Opencode, Windsurf, Lovable, Replit, OpenAI, Anthropic videoda anlatılmıyor; aday yapılmadı.
- 'limitless' ifadesinin AWS Aurora Limitless Database olduğu tahmindir; altyazıda tam adı geçmiyor.
- GitHub Copilot, VS Code ve diğer adayların altyazı zamanları segment sınırlarından yaklaşık hesaplandı (±30 sn).
- Kareler yalnızca sahne ve başlık görüntüleri içeriyor; ekranda araç, kod veya arayüz gösterimi yok.
- Videoda kurulum komutu, prompt veya site/arayüz kurulumu yok; ilgili alanlar boş.
## Atlanan segment oranı
0/35 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://x.com/mntruell | açıklama | açıklama | hayır |
| https://x.com/a16z | açıklama | açıklama | hayır |
| https://www.linkedin.com/company/a16z | açıklama | açıklama | hayır |
| https://open.spotify.com/show/5bC65RDvs3oxnLyqqvkUYX | açıklama | açıklama | hayır |
| https://podcasts.apple.com/us/podcast/a16z-podcast/id842818711 | açıklama | açıklama | hayır |
| https://x.com/eriktorenberg | açıklama | açıklama | hayır |
| https://a16z.com/disclosures | 27:14 | ekran | hayır |
| https://a16z.com/investments/ | 27:14 | ekran | hayır |
| https://www.youtube.com/watch?v=2x-aQy730Ew | açıklama | yorum | hayır |
| https://open.spotify.com | açıklama | açıklama | hayır |
| https://a16z.simplecast.com | açıklama | açıklama | hayır |
| http://www.adviserinfo.sec.gov | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — Mekanik mühendislik (CAD) için model ve CAD aracı fikriyle başlama, 6-7 ay sonra bırakma — araçlar: CAD systems
- 2. adım — Programlamaya dönüp çok hızlı pratik bir ürün çıkarmaya karar verme — araçlar: Cursor
- 3. adım — Birkaç haftada sıfırdan yazılan IDE'yi kendi günlük işlerinde kullanma — araçlar: Cursor
- 4. adım — Düzenleyiciyi sahiplenme kararı; eklenti yerine VS Code tabanlı düzenleyici — araçlar: VS Code, Vim
- 5. adım — İlk betayı birkaç ayda yayımlama ve ilgi toplama — araçlar: Cursor
- 6. adım — Kubernetes kümesi ve dosya senkron/arama altyapısıyla trafik büyümesini karşılama — araçlar: Kubernetes, CoreDNS
- 7. adım — Veritabanı ölçekleme: RDS'den AWS'in shard'sız servisine, sonra PlanetScale'e geçiş — araçlar: AWS RDS, Aurora Limitless, PlanetScale
- 8. adım — API sağlayıcı kapasitesini çoklu sağlayıcı ve token satıcılarıyla genişletme — araçlar: Claude Sonnet, Token resellers
- 9. adım — Çoklu bulut ve veri platformlarıyla altyapıyı çeşitlendirme — araçlar: AWS, GCP, Azure, Databricks, Snowflake
- 10. adım — Kendi modellerini eğitme ve çıkarımın bir kısmını içeride yapma — araçlar: Cursor
- 11. adım — Çoklu ürün genişlemesi: kod inceleme ve komut satırı ürünleri — araçlar: Bugbot, Cursor CLI
- 12. adım — Ekibi iki günlük ofis iş denemesi ve ortak öğünlerle işe alma — araçlar: İki günlük iş denemesi
- 13. adım — Yetenek için satın alma: Supermaven ekibini yakın takiple katma — araçlar: Supermaven, Tabnine
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
