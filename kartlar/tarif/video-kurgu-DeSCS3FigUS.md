# video-kurgu (DeSCS3FigUS)

**Amaç:** Video kurgusu için otomatik kesim, altyazı ekleme ve format dönüşümü yapmak.
**Araçlar:** ffmpeg, Whisper, Remotion, HyperFrames

**Adımlar**
1. [] Kesim listesi oluşturulur. Konuşma ve sessizlik bölümleri tespit edilir.
2. [] Kesim noktaları kontrol edilir ve görüntü akışı incelenir.
3. [] Kesimler ffmpeg kullanılarak birleştirilir ve render edilir.
4. [] Ses seviyesi dengelenir ve sessizlik tespiti yapılır.
5. [] Türkçe altyazı eklenir.
6. [] Video 9:16 Reels formatına kırpılır.

**Prompt/kod/ayar:** ffmpeg-igirdi.mp4-afsilencedetect=noise=-30dB:d=0.5-fnull
**Sonuç:** Kesilmiş, altyazılı ve format dönüştürülmüş video.
**Bizde (öneri, modelden):** Kurulu araçlarla nasıl yapılır: ffmpeg ve Whisper kullanarak otomatik olarak kesim listesi oluşturulur, altyazı eklenir ve video formatı dönüştürülür.
**Daha iyi (öneri):** Animasyon ve kodlama için Remotion ve HyperFrames gibi araçlar kullanarak daha karmaşık işlemler yapmak.
