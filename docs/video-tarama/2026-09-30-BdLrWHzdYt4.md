# Claude Code + Nano Banana Pro + Kling AI Kullanarak 3D Websiteleri Oluştur.
## Künye
Claude Code + Nano Banana Pro + Kling AI Kullanarak 3D Websiteleri Oluştur. · AI Temple · süre: 14:57 · tr-orig · https://youtu.be/BdLrWHzdYt4
motor: parti 2026-09-30-uzun-3 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (6)
## Özet
AI Temple, Claude Code ile scroll animasyonlu 3D/premium web siteleri yapmayı anlatıyor. Akış: VS Code ve Claude Code eklentisi kurulur, iki skill dosyası (frontend-design, video-to-website) .claude/skills altına konur. Nano Banana ile ilk ve son kare görseli üretilir, Kling 3.0 ile (Kie API veya OpenArt üzerinden) videoya çevrilir. Video kareye bölünür ve scroll ile senkronlanır. Gemini'ye video analizi yaptırılıp Claude için prompt yazdırılır, Claude plan modunda plan çıkarır, onaylanınca siteyi kurar. Geri bildirim ve ekran görüntüleriyle site düzeltilir, sonra Netlify'a sürükle-bırak ile yayınlanır. Yerel ve web dünyası farkı da açıklanır.
## Bölümler
- 0:00 Giriş ve VS Code + Claude Code kurulumu
- 1:02 Klasör yapısı ve skill dosyaları
- 2:03 Çalışma mantığı: video kareleri ve scroll senkronu
- 3:04 Kie ve OpenArt platformları
- 5:06 Kling 3.0 playground ayarları
- 6:08 Gemini ile prompt yazdırma ve Claude'da plan modu
- 8:09 Site sonucu ve geri bildirim
- 11:12 Netlify ile yayınlama
- 13:13 Yerel ve web dünyası mantığı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| video-to-website skill | yok | skill | yok | Videoyu karelere bölüp scroll ile senkronlayan siteyi Claude Code'a kurduran markdown skill dosyası. | 1:02 | Video iki skill dosyasının gerekli olduğunu söylüyor. (karede: Explorer'da skills altında frontend-design/SKILL.md ve video-to-website/SKILL.md klasörleri görünüyor.) |
| frontend-design skill (özelleştirilmiş) | yok | skill | yok | Orijinalinden yazarın değiştirdiği frontend tasarım skill'i; ücretsiz toplulukta paylaşılıyor. | 1:02 | Orijinal dosyayı alıp kendim için biraz değiştirdiğim frontend design skilli. |
| Kling 3.0 (Kie API) | yok | teknik | yok | İlk/son kareden video üreten model; Kie playground'unda prompt, süre ve mod ayarlanır. | 5:06 | Kie'de Kling 3.0 ile ilk kare, son kare, süre ayarı kullanılıyor. (karede: KIE API Playground: Start Frame ve End Frame'de saat görselleri, multi_shots ve sound anahtarları, prompt, duration ve std/pro/4K modları.) |
| OpenArt | yok | teknik | yok | Birçok video, görüntü ve ses modeline tek abonelikle erişim sağlayan platform. | 4:05 | Tek bir Open Art aboneliği yapıyorsun. (karede: OpenArt Frame to Video ekranı; Kling 3.0 seçili, model listesinde Seedance 2.0, Kling 3.0 Omni, Veo 3.1 vb.) |
| Gemini ile prompt üretimi | yok | iş akışı | yok | Üretilen videoyu Gemini'ye verip Claude ajanı için site prompt'u yazdırma. | 6:08 | Bunu Cemina'ya gönderiyorum. Biliyorsun Ceminay'ın video analiz yetenekleri var. |
| Claude Code plan modu + dosya etiketleme | yok | ipucu | yok | Önce plan çıkarttırıp onaylama, ardından bypass permissions ile inşa; videoyu @ ile etiketleme. | 7:08 | Plan modunu açmam gerekiyor. Çünkü öncelikle bir plan yapalım. |
| Netlify sürükle-bırak yayın | yok | iş akışı | yok | Proje klasörünü Netlify'a sürükleyip siteyi herkese açık yayınlama. | 11:12 | Klasörü Netlify'a sürükleyip bırakacağım ve sistem çok basit yayına girmiş olacak. |
| Claude'a ilk siteyi düzelttirmek (ekran görüntüleriyle birlikte, sesli anlatımdan özetlenmiştir). | yok | prompt | yok | Siteyi inceledim. Hero'daki 001 hero yazısını kaldır, tazeliğin gücü yazısını küçült, özellikler daha erken çıksın, video tam ekran olsun, vinyet ekle, sayacı sadeleştir, CTA metnini karta sığdır ve fontu değiştir. | 9:10 | kaynak: altyazı |
| Kling için Kie playground'undaki örnek video prompt'u (kısmen görünüyor, 738 karakter). | yok | prompt | yok | Outdoor terrace of a European villa, by a dining table ... the camera zooms in, the woman swirls the juice in a glass ... | 3:35 | kaynak: kare |
## Açıklama bağlantıları
- https://n8n.partnerlinks.io/afrwto8ks57s — n8n ortaklık (affiliate) bağlantısı · aday: hayır · Videoda n8n geçmiyor; sponsor/affiliate link.
- https://openart.ai/home?utm_source=tolt&utm_medium=affiliate&utm_campaign=affiliate-tolt--acq-web&via=ahmetdemirci — OpenArt affiliate bağlantısı · aday: evet (OpenArt) · Videoda OpenArt platformu tanıtılıyor (4:05); bağlantı bu platformun affiliate linki.
- https://repocloud.io/?ref=r6dwor1 — RepoCloud ortaklık bağlantısı · aday: hayır · Videoda RepoCloud anlatılmıyor; affiliate link.
- https://www.instagram.com/ahmetdemirciai/ — Yazarın Instagram hesabı · aday: hayır · Sosyal medya profili, araç değil.
- https://www.skool.com/ai-tapinak-plus-6938 — Skool topluluğu (plus) · aday: hayır · Topluluk sayfası; skill dosyaları burada ama içerik erişilemez. · erişilemez: Skool topluluğu, giriş/üyelik gerekli
- https://www.skool.com/ai-tapnak-5680 — Ücretsiz Skool topluluğu · aday: hayır · Skill dosyalarının alındığı topluluk; içerik üyelik olmadan görülemez. · erişilemez: Skool topluluğu, giriş/üyelik gerekli
- https://x.com/ahmetdemirciai — Yazarın X hesabı · aday: hayır · Sosyal medya profili, araç değil.
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Scroll ile senkronize kare animasyonu (video kareleri) | Video karelere bölünür; kaydırdıkça kareler değişir, ürün parçalanma animasyonu akar. | 2:03 | altyazı |
| Frame klasörü (webp kareler) | Örnek projede saat videosundan çıkarılmış frame_0001.webp... dosyaları var. (karede: Explorer'da projeler/saat/frames altında frame_0001.webp ... frame_0027.webp; sağda saat.mp4 önizlemesi.) | 2:34 | kare |
| Özellik kartları, koyu kart çerçeve, sayaç animasyonu, hero ve CTA | Kartlar animasyonlu gelir, koyu kart arka plandan ayrışır, sayılar artar; hero metni ve CTA taşması sonradan düzeltilir, vinyet eklenir, video tam ekran yapılır. | 9:10 | altyazı |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Claude Code kullanmak için ücretli plan gerekir; ücretsiz planda erişim yok. | 0:31 | özellik |
| Sitedeki interaktif animasyonlar aslında videodur; kareye bölünüp scroll ile senkronlanır. | 2:03 | özellik |
| Kie kredi mantığıyla çalışır; abonelikten ucuz olabilir, 5-10 dolarlık paketler var. | 3:04 | karşılaştırma |
| İdeal video süresi 5-7 saniye; uzun olursa çok kaydırma gerekir. | 5:06 | öneri |
| Ses ve multishot kapatılabilir, çünkü site için gerekli değil. | 5:06 | öneri |
| Kie ekranında 10 sn, ses açık ve std modda 200 kredi Run düğmesi görünüyor. | 5:37 | sayısal |
| Doğrudan video verip site istemek de çalışır ama kalite için Gemini ile prompt yazdırmak öneriliyor. | 6:08 | öneri |
| Netlify'da güncellemeleri tekrar yüklemezsen kullanıcılar eski sürümü görür. | 12:12 | özellik |
## Kareden okunanlar
- 0:31: VS Code sitesi: 'The open source AI code editor', Download for Windows düğmesi.
- 1:32: skills/frontend-design/SKILL.md ve video-to-website/SKILL.md; settings.local.json, nike-volcano, tazeligin-gucu, blender.mp4, CLAUDE.md.
- 2:34: Claude Code paneli 'TODO: Everything. Let's start.'; projeler/saat/frames altında webp kareler; saat.mp4 0:05.
- 3:35: KIE API Playground: Start/End Frame, multi_shots ve sound kapalı, prompt 738/2500, Run 90.
- 4:36: OpenArt Frame to Video: Kling 3.0 seçili; model listesinde Seedance 2.0, Kling 3.0 Omni, Wan 2.7, Veo 3.1, Grok Imagine; Generate 600.
- 5:37: Kie: sound açık, duration 10, mode std/pro/4K, Run 200.
## Belirsizlikler
- Skill klasörünün adı altyazıda 'NCloud' geçiyor; karede skills yolu görünüyor, büyük olasılıkla .claude ama tam yol okunmuyor.
- Nano Banana ile görsel üretimi gösterilmiyor, yalnızca anlatılıyor.
- Gemini'ye verilen prompt metni ve Claude'a yapıştırılan prompt gösterilmiyor.
- Hiçbir terminal komutu söylenmedi veya gösterilmedi; kurulum_komutlar boş.
- Kie'de 5:06 sonrası 'Kıi/Kia' yazımı ASR hatası; kastedilen Kie API.
- Reçete'deki geri bildirim prompt'u sesli söylenenin özetidir, birebir metin değildir.
- Kare zamanları (0:31 vb.) videonun o anıyla eşleşiyor; kare 3:35 ve 5:37'deki kredi rakamları farklı ayarlardan geliyor.
## Atlanan segment oranı
0/15 (paket tam okuma, motor)
ikinci göz KAPALI: --ikinci-goz yok
