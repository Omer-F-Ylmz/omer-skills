# Claude can watch your videos now, not just read about them.
## Künye
Claude can watch your videos now, not just read about them. · claudetipsandtricks · süre: 0:00 · ? · https://www.instagram.com/p/DZqNTY4jE1b/ · platform: instagram · tür: görsel gönderi · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-23 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (7)
altyazı yok: kare-yalnız
claude-sonnet-5-5: claude-sonnet-5-5 · 25017 tk · claude-haiku-5-5: claude-haiku-5-5 · 34039 tk
## Özet
Instagram karusel gönderisi (@claudetipsandtricks): Claude'un artık videoları izleyebildiğini anlatıyor. Claude videodan kareleri görsel olarak çeker, zaman damgalı ses dökümünü okur ve görüneni ile söyleneni birlikte yorumlar. 5 ipucu: nasıl çalışır, video özetleme, ekran kaydı hata ayıklama, ekrandaki metni okuma (--resolution) ve uzun videolarda --start/--end ile aralık seçme. Doğruluk 10 dakikanın altında en iyidir.
## Bölümler
- 0:00 Kapak: Claude videolarınızı izliyor
- 0:00 1. Nasıl çalışır (/watch demo.mov)
- 0:00 2. Video özetleme (/watch youtu.be/abc)
- 0:00 3. Kaydı hata ayıklama (/watch bug-repro.mov)
- 0:00 4. Ekranı okuma (--resolution)
- 0:00 5. Doğru kalma (--start / --end)
- 0:00 Kapanış: Takip çağrısı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude | yok | CLI | yok | Videodan kare çekip zaman damgalı ses dökümünü okuyarak videoyu izleyen yapay zekâ asistanı | 0:00 | Kapakta 'CLAUDE WATCHES your Videos now'; sayfa 2'de kare ve döküm anlatımı (karede: kanıttan) Kapakta 'CLAUDE WATCHES your Videos now'; sayfa 2'de kare ve döküm anlatımı |
| /watch | yok | skill | yok | Video dosyası ya da bağlantısını Claude'a izleten slash komutu; --resolution, --start, --end seçenekleri var | 0:00 | Sayfa 2-6'da '/watch demo.mov', '/watch youtu.be/abc' komut kartları (karede: kanıttan) Sayfa 2-6'da '/watch demo.mov', '/watch youtu.be/abc' komut kartları |
| Claude Code | yok | CLI | yok | Açıklamadaki hashtag'te geçen, /watch komutunun çalıştığı varsayılan ortam | açıklama | Açıklamada #ClaudeCode hashtag'i; gönderide ortam açıkça gösterilmiyor |
| YouTube | yok | ipucu | yok | Özetlenecek video kaynağı olarak youtu.be bağlantısı | 0:00 | Sayfa 3: 'Paste a YouTube link' ve '/watch youtu.be/abc' (karede: kanıttan) Sayfa 3: 'Paste a YouTube link' ve '/watch youtu.be/abc' |
| Instagram | yok | ipucu | yok | Gönderinin yayınlandığı platform | 0:00 | Her kartta 'Instagram claudetipsandtricks' etiketi (karede: kanıttan) Her kartta 'Instagram claudetipsandtricks' etiketi |
| Anthropic | yok | ipucu | yok | Claude'un geliştiricisi, yalnız hashtag'te anılıyor | açıklama | Açıklamada #Anthropic hashtag'i |
| Videonun genel akışını anlatma | yok | prompt | yok | Demo videoyu baştan sona adım adım anlat. | 0:00 | kaynak: kare |
| Video özetleme | yok | prompt | yok | YouTube videosunu özetle. | 0:00 | kaynak: kare |
| Ekran kaydında hata ayıklama | yok | prompt | yok | Kayıtta neyin yanlış gittiğini söyle. | 0:00 | kaynak: kare |
| Ekrandaki metni okuma | yok | prompt | yok | Videoda gösterilen tüm komutları listele. | 0:00 | kaynak: kare |
| Uzun videoda aralık seçerek özet | yok | prompt | yok | Belirtilen zaman aralığını özetle. | 0:00 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| /watch demo.mov | Yerel videoyu Claude'a izletir; ardından 'walk me through this' sorulur (karede: Sayfa 2 komut kartı: /watch demo.mov, walk me through this) | 0:00 | kare |
| /watch youtu.be/abc | YouTube videosunu izletip özetletir (karede: Sayfa 3 komut kartı: /watch youtu.be/abc, summarize this) | 0:00 | kare |
| /watch bug-repro.mov | Hata içeren ekran kaydını inceletir (karede: Sayfa 4 komut kartı: /watch bug-repro.mov) | 0:00 | kare |
| /watch talk.mp4 --resolution | Kare çözünürlüğünü artırarak ekrandaki metni okutur (karede: Sayfa 5 komut kartı: /watch talk.mp4 --resolution) | 0:00 | kare |
| /watch lecture.mp4 --start 12:00 --end 15:00 summarize this | Videonun yalnız 12:00-15:00 aralığını özetletir (karede: Sayfa 6 komut kartı: --start 12:00, --end 15:00, summarize this) | 0:00 | kare |
| /watch lecture.mp4 --start 12:00 --end 15:00 | Videonun 12:00-15:00 aralığını Claude'a verir; "summarize this" ile yalnız o bölümü özetletir. (karede: Kare 6: sohbet kutusunda "/watch lecture.mp4 --start 12:00 --end 15:00 summarize this" yazıyor.) | 0:00 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Claude kareleri görsel olarak çeker ve zaman damgalı dökümü okuyup görüneni ve söyleneni birlikte yorumlar. | 0:00 | özellik |
| Özetleme, videoyu 2x izlemekten daha hızlıdır. | 0:00 | karşılaştırma |
| Doğruluk 10 dakikanın altındaki videolarda en iyidir. | 0:00 | sayısal |
| Uzun videolarda başlangıç ve bitiş zamanı verilmesi önerilir. | 0:00 | öneri |
| Kare çözünürlüğü artırılınca Claude ekrandaki kelimeleri birebir okuyabilir. | 0:00 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| kare 1 · 0:00 | Claude | Claude | CLAUDE WATCHES your Videos now |
| kare 2-6 · 0:00 | /watch komutu | /watch | /watch demo.mov, talk.mp4 --resolution vb. |
| kare 2 · 0:00 | demo.mov örnek dosyası | aday değil: konu dışı | Örnek dosya adı |
| kare 3 · 0:00 | YouTube bağlantısı | YouTube | Paste a YouTube link; youtu.be/abc |
| kare 4 · 0:00 | bug-repro.mov | aday değil: konu dışı | Örnek dosya adı |
| kare 5 · 0:00 | --resolution seçeneği | aday değil: başka adayın parçası (/watch) | /watch talk.mp4 --resolution |
| kare 6 · 0:00 | --start / --end seçenekleri | aday değil: başka adayın parçası (/watch) | --start 12:00 --end 15:00 |
| kare 1-7 · 0:00 | Instagram / @claudetipsandtricks | Instagram | Instagram claudetipsandtricks etiketi |
| açıklama | Claude Code | Claude Code | #ClaudeCode |
| açıklama | Anthropic | Anthropic | #Anthropic |
| açıklama | #Claude #ClaudeAI #AITips hashtag'leri | aday değil: genel kavram | Hashtag listesi |
| açıklama | Gönderi bağlantısı | aday değil: konu dışı | https://www.instagram.com/p/DZqNTY4jE1b/ |
| yorum | Yorumlar | aday değil: konu dışı | Girişsiz alınamıyor |
## Kareden okunanlar
- 1 (0:00): CLAUDE WATCHES your Videos now; @claudetipsandtricks
- 2 (0:00): /watch demo.mov · walk me through this
- 3 (0:00): /watch youtu.be/abc · summarize this
- 4 (0:00): /watch bug-repro.mov · what's going wrong?
- 5 (0:00): /watch talk.mp4 --resolution · list every command shown
- 6 (0:00): /watch lecture.mp4 --start 12:00 --end 15:00 summarize this
- 7 (0:00): One Claude tip, every day. Follow @claudetipsandtricks; save
## Belirsizlikler
- /watch komutunun hangi sürümde, skill ya da yerleşik komut olarak sunulduğu belirtilmiyor; 'skill' türü tahmindir.
- Claude Code yalnız hashtag'te geçiyor; komutun orada çalıştığı gönderide açıkça gösterilmiyor.
- Gönderide gerçek video süresi yok (görsel karusel); zamanlar 0:00 olarak verildi.
- youtu.be/abc örnek yer tutucudur, gerçek bir video değildir.
- Yorumlar girişsiz alınamadı.
## Atlanan segment oranı
0/0 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.instagram.com/p/DZqNTY4jE1b/ | açıklama | açıklama | hayır |
| youtu.be/abc | 0:00 | ekran | hayır |
## İş akışı
- 1. adım — Videoyu (yerel dosya ya da YouTube bağlantısı) /watch ile Claude'a ver — araçlar: /watch, Claude
- 2. adım — Claude kareleri görsel olarak çıkarır ve zaman damgalı ses dökümünü okur — araçlar: Claude
- 3. adım — Videoyu özetletmek için prompt yaz — araçlar: /watch, YouTube
- 4. adım — Ekran kaydındaki hatayı bulmasını iste — araçlar: /watch
- 5. adım — Ekrandaki metin için --resolution ile çözünürlüğü artır — araçlar: /watch
- 6. adım — 10 dakikadan uzun videolarda --start ve --end ile aralık seç — araçlar: /watch
## Promptlar
- Videonun genel akışını anlatma — Demo videoyu baştan sona adım adım anlat.
- Video özetleme — YouTube videosunu özetle.
- Ekran kaydında hata ayıklama — Kayıtta neyin yanlış gittiğini söyle.
- Ekrandaki metni okuma — Videoda gösterilen tüm komutları listele.
- Uzun videoda aralık seçerek özet — Belirtilen zaman aralığını özetle.
