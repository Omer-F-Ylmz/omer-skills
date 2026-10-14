# vid — 18 benzersiz kayıt

**Amaç:** Video üretim ajanları: brief/senaryo, kurgu ritmi, hareket grafiği, ses düzeyi, renk uzayı, sosyal format uyarlama, ffmpeg/yt-dlp işlemleri, Remotion/HyperFrames ile kodla video.

**İç yapı:** Tümü [ajan], vid-<konu>; ön üretim (brief, senaryo, reel-kanca), kurgu/post (gecis, ses, renk, hareket), araç (ffmpeg, ytdlp, kare), kodla video (remotion, hyperframes).

## En güçlü parçalar
- `vid-ffmpeg-donusturucu` — Dönüştürme, kırpma, sıkıştırma ve kare çıkarma ffmpeg komutları.
- `vid-ytdlp-indirme` — yt-dlp ile format seçimi ve hız limitiyle video, ses, altyazı indirme.
- `vid-renk-uzayi` — Soluk/düz/aşırı doygun dışa aktarım, renk aralığı ve HDR→SDR uyumsuzluğu.
- `vid-kisa-klip-secici` — Transkript/altyazıda kısa klip için doruk anlarını bulur.
- `vid-reel-kanca-merdiveni` — Dikey Reels/Shorts/TikTok için hook, tutma merdiveni, haftalık plan.
- `vid-ses-duzeni` — Ses, müzik, efekt seviyeleri, ducking ve loudness hedefleri.
- `vid-video-ozetle` — Altyazıdan zaman damgalı ana noktalar.
- `vid-remotion-kurucu` — Remotion kompozisyon, sequence, interpolation ile kodla video.

## Birlikte kullanım
- vid-video-brief → vid-video-senaryo → vid-gecis-ve-ritim.
- vid-ytdlp-indirme → vid-video-ozetle → vid-kisa-klip-secici → vid-sosyal-video-bicim.
- vid-hyperframes-kompozisyon hyperframes ailesiyle, vid-remotion-kurucu remotion ailesiyle.

## Tuzaklar
- cli ailesindeki ffmpeg/yt-dlp araçlarının kurulu olması gerekir; ajanlar komut kurar.
- vid-hyperframes-kompozisyon hyperframes skill'leriyle, vid-remotion-kurucu remotion ailesiyle örtüşür.
- vid-premiere-akis Premiere Pro lisansı gerektirir; katalog metninde ayrıca belirtilmemiş.

## Üyeler
- ajan (18): vid-ffmpeg-donusturucu, vid-gecis-ve-ritim, vid-hareket-grafigi, vid-hyperframes-kompozisyon, vid-kare-cikarici, vid-kisa-klip-secici, vid-podcast, vid-premiere-akis, vid-reel-kanca-merdiveni, vid-remotion-kurucu, vid-renk-uzayi, vid-ses-duzeni, vid-sosyal-video-bicim, vid-video-brief, vid-video-ozetle, vid-video-performans-web, vid-video-senaryo, vid-ytdlp-indirme
