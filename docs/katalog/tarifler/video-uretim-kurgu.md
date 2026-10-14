# Video üretim ve kurgu — birleşim tarifi
Ne zaman: Ham çekimden kurgu, kısa klip, altyazı ya da kodla üretilen video.

## Fazlar
1. Kaynak: `watch` — videodan altyazı ya da whisper transkripti ve kareler çıkarır · birlikte: `vid-ytdlp-indirme` yt-dlp ile format seçerek indirir.
2. Senaryo ve seçim: `vid-kisa-klip-secici` — transkriptte zirve anları bulur · birlikte: dikey kısa video için `reel-plan` hook ve izleyici tutma merdiveni.
3. Kurgu: `ecc:video-editing` — çekim kesme ve video içeriği · birlikte: `ffmpeg` keser, birleştirir, kodlar; komutu `vid-ffmpeg-donusturucu` kurar.
4. Kodla video: `hyperframes:hyperframes` — HTML ile video için zorunlu giriş noktası · birlikte: React tercih edilirse `remotion-best-practices` yönlendirir. Projede birini seç.
5. Altyazı ve erişilebilirlik: `accessible-content:multimedia-accessibility` — altyazı, transkript, sesli betimleme.
6. Render ve teslim: `remotion-render` ya da HyperFrames render · birlikte: `superpowers:verification-before-completion` çıktıyı izleyip kanıtlar.

## İnceleme ajanları
- `vid-hareket-grafigi`: zamanlama, easing, alt yazı tipografisi.
- `okuyucu`: transkript karşılaştırma (sonnet, salt okuma).

## Güvenlik ve kalite kapıları
- Altyazı ve transkript var: `accessible-content:multimedia-accessibility`.
- Son dosya oynatılıp kare kontrolü yapıldı.
- İndirilen içeriğin kullanım hakkı kontrol edildi.

## Tartışma konseyi
- Karar: hangi anlar kalır, kurgu ritmi.
- `ecc:council` — varsayılan Claude personaları: yönetmen, editör, hedef izleyici.

## Jeton bütçesi
- Kaynak: orta (~15k, tahmini); uzun transkript `okuyucu` alt ajanına.
- Seçim: orta (~10k). Kurgu: orta (~15k). Kodla video: büyük (~40k). Altyazı: küçük (~5k). Teslim: küçük (~3k). Hepsi tahmini.

## Kaçınılacaklar
- HyperFrames ile Remotion'ı aynı projede karıştırmak.
- `watch` ile YouTube indirmeyi claude.ai sandbox'ında denemek; çalışmaz.
- Kodlamayı her denemede yeniden yapmak; önce düşük kaliteli önizleme.

## Aday (kurulu değil)
yok
