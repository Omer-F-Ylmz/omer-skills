# scroll-animasyon (DdyqkyqvuUM)

**Amaç:** Scroll hareketiyle birlikte dönen/oluşan ürün animasyonu oluşturma.
**Araçlar:** Google Flow (AI tabanlı resim oluşturma ve animasyon), EasyGIF (video frame dizisine dönüştürme), AI Coding Tool (scroll ile oynayan görüntü dizisi oluşturma)

**Adımlar**
1. [] Başlangıç ve bitiş görüntülerini prompt ile Google Flow'da oluşturun. Örnek: 'Ürünün tamamen monteli halini merkeze oturtan yüksek kaliteli stüdyo fotoğrafı'.
2. [] Flow'da oluşturulan iki resimi video'ya dönüştürün ve aradaki animasyonu oluşturun. 'Pick frames to video' seçeneğini kullanın.
3. [] EasyGIF'e video'yu yükleyin, 'Video to Image Sequence' seçeneğini kullanın ve 30fps ayarlayarak frame'ları zip olarak indirin.
4. [] İndirilen frame'ları içeren klasörü AI kodlama aracına atın ve 'scroll-linked image sequence' komutunu kullanarak canvas'ta animasyonu oluşturun.

**Prompt/kod/ayar:** Google Flow: 'Başlangıç/bitiş görüntüleri için prompt' + 'Ürün animasyonu için detaylı açıklama' (ör: 'Ürünün montaj süreci, 3D perspektifli, yüksek çözünürlük').
EasyGIF: 'Video to Image Sequence' + '30fps' + 'Download as ZIP'.
AI Coding Tool: 'Scroll-linked image sequence' + 'Canvas'ta oynatma'.
**Sonuç:** Scroll animasyonu ile birlikte dönen/oluşan ürün görüntüsü.
**Bizde (öneri, modelden):** Kurulu araçlarla nasıl yapılır?
1. **MidJourney/Stable Diffusion** ile başlangıç/bitiş görüntülerini oluşturun.
2. **Pillow/FFmpeg** ile frame'ları video'ya dönüştürün.
3. **OpenCV** veya **FFmpeg** ile video'yu 30fps frame dizisine ayırın.
4. **Three.js** veya **GSAP** ile scroll animasyonunu canvas'ta oluşturun.
**Daha iyi (öneri):** Frame'ları daha yüksek çözünürlükte (1080p+) oluşturmak ve AI aracında scroll hızını ayarlamak için 'scroll-triggered speed' özelliğini eklemek.
