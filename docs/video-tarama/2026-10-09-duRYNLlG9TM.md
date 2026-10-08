# 600+ Dilde Sesini Klonla: OmniVoice
## Künye
600+ Dilde Sesini Klonla: OmniVoice · İsa Nurdoğdu · süre: 0:47 · tr-orig · https://youtu.be/duRYNLlG9TM · şema 2
motor: parti 2026-10-09-short-2 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (8)
claude-sonnet-5-5: claude-sonnet-5-5 · 16810 tk · claude-haiku-5-5: claude-haiku-5-5 · 31139 tk
## Özet
İsa Nurdoğdu, ElevenLabs'e ücretsiz ve açık kaynaklı alternatif olarak OmniVoice'u tanıtıyor. Araç birkaç saniyelik kayıttan 600'den fazla dilde ses klonluyor, yaş, cinsiyet, aksan, perde ve duygu kontrolleri sunuyor, metne kahkaha/iç çekme eklenebiliyor. Yerleşik MCP ile Claude Code'a bağlanıp prompttan ses üretebiliyor ve yerelde çalışıyor.
## Bölümler
- 0:00 OmniVoice'un tanıtımı: ElevenLabs alternatifi
- 0:06 Referans kayıttan ses klonlama ve diller
- 0:10 OmniVoice TTS Generator arayüzü ve ses seçimi
- 0:22 Ses tasarımı: yaş, cinsiyet, aksan, perde
- 0:33 MCP ile Claude Code entegrasyonu
- 0:40 Yerelde çalıştırma ve yorum/DM çağrısı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| OmniVoice | yok | CLI | https://github.com/k2-fsa/OmniVoice | Açık kaynaklı, yerelde çalışan, 600+ dilde ses klonlayan ve ses tasarlayan metinden sese aracı. | 0:00 | Adı Omnivice; açık kaynak olarak kendi bilgisayarında çalıştırabiliyorsun. |
| ElevenLabs | yok | CLI | yok | OmniVoice'un alternatifi olduğu ücretli ses üretim servisi; karşılaştırma için anıldı. | 0:00 | Ekran metni: ElevenLabs'e ücretsiz; konuşmada Eleven Laps. (karede: kanıttan) Ekran metni: ElevenLabs'e ücretsiz; konuşmada Eleven Laps. |
| Claude Code | yok | CLI | yok | OmniVoice MCP'sine bağlanıp prompttan ses üreten kodlama aracı. | 0:33 | Karede Claude Code simgesi OmniVoice simgesine bağlı; altyazıda cloud kod. (karede: kanıttan) Karede Claude Code simgesi OmniVoice simgesine bağlı; altyazıda cloud kod. |
| MCP | yok | MCP | yok | OmniVoice'un yerleşik MCP desteği, araçların ses üretmesini sağlıyor. | 0:30 | Yerleşik MCP sayesinde aracı cloud kod gibi araçlara bağlayabiliyorsun. |
| Claude | yok | CLI | yok | Promptu alıp sesi doğrudan üreten yapay zekâ asistanı. | 0:37 | Ekran metni: ve Claude senin; altyazıda cloud senin yerine ses üretebiliyor. (karede: kanıttan) Ekran metni: ve Claude senin; altyazıda cloud senin yerine ses üretebiliyor. |
| Whisper ASR | yok | teknik | yok | Referans kaydın otomatik yazıya dökülmesi için kullanılan konuşma tanıma. | 0:06 | Karede Automatic transcription with Whisper ASR maddesi görünüyor. (karede: kanıttan) Karede Automatic transcription with Whisper ASR maddesi görünüyor. |
| OmniVoice TTS Generator | yok | iş akışı | yok | Metin girip ses seçerek konuşma üreten web arayüzü. | 0:10 | Karede OmniVoice TTS Generator başlığı, metin alanı ve ses listesi. (karede: kanıttan) Karede OmniVoice TTS Generator başlığı, metin alanı ve ses listesi. |
| Voice design | yok | teknik | yok | Yaş, cinsiyet, aksan ve perde etiketleriyle ses tasarlama modu. | 0:22 | Karede Voice design paneli, etiket seçenekleri görünüyor. (karede: kanıttan) Karede Voice design paneli, etiket seçenekleri görünüyor. |
| Voice Cloning | yok | teknik | yok | 3 saniyelik referanstan 646 dilde çapraz dilli ses klonlama. | 0:07 | Karede Cross-lingual Voice Cloning in 646 languages yazıyor. (karede: kanıttan) Karede Cross-lingual Voice Cloning in 646 languages yazıyor. |
## Açıklama bağlantıları
- https://www.isanurdogdu.com/kaynaklar/omnivoice — Yazarın OmniVoice kaynak sayfası · aday: evet (OmniVoice) · OmniVoice bağlantısını veren kaynak sayfası; yola OmniVoice adı geçiyor ve araç anlatılıyor. · sınıf: diğer
- https://github.com/k2-fsa/OmniVoice — OmniVoice'un GitHub deposu. · aday: evet (OmniVoice) · Videonun anlattığı OmniVoice aracının resmi kaynak kodu ve kurulum deposu. · sınıf: diğer
- https://www.isanurdogdu.com — Yaratıcının ana web sitesi. · aday: hayır · Yaratıcının kişisel sitesi; araç ya da servis değil. · sınıf: diğer
- https://www.isanurdogdu.com/#kur — Yaratıcı sitesinde kurulum bölümüne işaret eden bağlantı. · aday: hayır · Yaratıcı sitesinin iç bağlantısı; bağımsız bir araç değil. · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Koyu temalı iki sütunlu üretici arayüzü | Metin giriş alanı solda, ses seçimi sağda (two-column layout, dark UI) (karede: OmniVoice TTS Generator başlığı, solda Enter your text alanı, sağda Select a voice listesi.) | 0:10 | kare |
| Etiketli ses kartları listesi | Etiket çipli, oynat düğmeli seçilebilir ses kartları (tag chips, voice cards) (karede: Elon Musk, SpongeBob SquarePants, Donald J. Trump kartları; Male, Deep gibi etiketler, oynat simgesi.) | 0:15 | kare |
| Etiket seçimli ses tasarım paneli | Cinsiyet, yaş, perde, aksan seçimi için çip düğmeleri (toggle chips) (karede: Voice design başlığı altında gruplanmış etiket düğmeleri ve turuncu Generate düğmesi.) | 0:22 | kare |
| Onay işaretli kontrol listesi animasyonu | Özellik maddeleri sırayla tik alıyor (staggered checklist animation) (karede: Üç maddelik Reference in, voice out listesi, yeşil tik işaretleri.) | 0:07 | kare |
| Bağlantı çizgili uygulama simgeleri diyagramı | Claude Code simgesi OmniVoice simgesine çizgiyle bağlı (connector diagram) (karede: Beyaz zeminde Claude Code ve OmniVoice simgeleri arasında ince bağlantı çizgisi.) | 0:33 | kare |
| Altyazı kutusu | Beyaz yuvarlatılmış kutuda alt altyazı (caption overlay) (karede: Altta beyaz kutuda kaydı verdiğinde yazısı.) | 0:06 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| OmniVoice birkaç saniyelik kayıttan konuşmanın tonunu, ritmini ve duygusunu taklit ediyor. | 0:00 | özellik |
| 600'den fazla dili destekliyor (arayüzde 646 dil). | 0:07 | sayısal |
| Referans klipler en az 3 saniye olabilir. | 0:06 | sayısal |
| Yaş, cinsiyet, aksan, perde ve duygu ayarlanabiliyor; metne kahkaha ve iç çekme eklenebiliyor. | 0:22 | özellik |
| ElevenLabs'e ücretsiz ve açık kaynaklı alternatif. | 0:00 | karşılaştırma |
| Yerleşik MCP ile Claude Code'a bağlanıp prompttan ses üretebiliyor. | 0:33 | özellik |
| Üretim başına 4000 karakter sınırı var. | 0:22 | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | OmniVoice | OmniVoice | Adı Omnivice; ücretsiz açık kaynaklı alternatif. |
| kare 0:00 | ElevenLabs | ElevenLabs | Ekran metni ElevenLabs'e ücretsiz. |
| kare 0:06 | Whisper ASR | Whisper ASR | Automatic transcription with Whisper ASR. |
| kare 0:07 | Cross-lingual Voice Cloning | Voice Cloning | 646 dilde klonlama maddesi. |
| kare 0:10 | OmniVoice TTS Generator | OmniVoice TTS Generator | Arayüz başlığı görünüyor. |
| kare 0:15 | Elon Musk, SpongeBob, Donald J. Trump ses kartları | aday değil: başka adayın parçası (OmniVoice TTS Generator) | Ses listesindeki hazır kartlar. |
| kare 0:22 | Voice design paneli | Voice design | Aksan, perde, yaş etiketleri. |
| konuşma 0:30 | MCP | MCP | Yerleşik MCP sayesinde bağlanıyor. |
| kare 0:33 | Claude Code | Claude Code | Claude Code simgesi OmniVoice'a bağlı. |
| kare 0:37 | Claude | Claude | Ve Claude senin yerine ses üretiyor. |
| açıklama | yorum ve DM ile bağlantı gönderme | aday değil: konu dışı | Yoruma ses yaz, DM'den göndereyim. |
| açıklama | https://www.isanurdogdu.com/kaynaklar/omnivoice | OmniVoice | Açıklamadaki OmniVoice kaynak sayfası. |
| linkli sayfa | https://github.com/k2-fsa/OmniVoice | OmniVoice | Kaynak sayfasından bağlanan GitHub deposu. |
| linkli sayfa | https://www.isanurdogdu.com | aday değil: konu dışı | Yazarın ana sayfası. |
| linkli sayfa | https://www.isanurdogdu.com/#kur | aday değil: konu dışı | Yazarın ana sayfasındaki bölüm bağlantısı. |
## Kareden okunanlar
- 0:06: Reference clips as short as 3 seconds; Automatic transcription with Whisper ASR
- 0:07: Cross-lingual Voice Cloning in 646 languages
- 0:10: OmniVoice TTS Generator; Free, 646 Languages, Voice Cloning, Voice Design, No Account
- 0:15: Elon Musk, SpongeBob SquarePants, Donald J. Trump kartları ve etiketleri
- 0:22: Voice design: aksan, perde, yaş etiketleri
- 0:33: Claude Code ile OmniVoice simgeleri bağlı
## Belirsizlikler
- Altyazıda Omnivice ve Eleven Laps yazıyor; ekran metnine göre OmniVoice ve ElevenLabs alındı.
- Kare 0:07'deki 646 dil sayısı altyazıdaki 600+ ile uyumlu, ancak OCR bulanık.
- Ünlü sesli hazır kartlar (Elon Musk, Trump, SpongeBob) listede görünüyor, videoda kullanılmadı.
- Kurulum komutu gösterilmedi veya söylenmedi.
- Açıklamadaki bağlantının sponsor/affiliate işareti yok.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.isanurdogdu.com/kaynaklar/omnivoice | açıklama | açıklama | evet |
| https://www.isanurdogdu.com/kaynaklar/omnivoice | açıklama | yorum | evet |
| https://github.com/k2-fsa/OmniVoice | açıklama | açıklama | evet |
| https://www.isanurdogdu.com | açıklama | açıklama | hayır |
| https://www.isanurdogdu.com/#kur | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — OmniVoice'un ElevenLabs alternatifi olarak tanıtılması — araçlar: OmniVoice, ElevenLabs
- 2. adım — Birkaç saniyelik referans kayıttan ses klonlama özelliğinin gösterilmesi — araçlar: OmniVoice, Voice Cloning, Whisper ASR
- 3. adım — TTS Generator arayüzünde metin girişi ve hazır ses seçimi — araçlar: OmniVoice TTS Generator
- 4. adım — Ses tasarımı panelinde yaş, cinsiyet, aksan ve perde ayarı — araçlar: Voice design
- 5. adım — OmniVoice'un MCP ile Claude Code'a bağlanması — araçlar: MCP, Claude Code, Claude
- 6. adım — Yerel çalıştırma bilgisi ve yorum yoluyla bağlantı paylaşımı çağrısı — araçlar: OmniVoice
## Promptlar
- yok
