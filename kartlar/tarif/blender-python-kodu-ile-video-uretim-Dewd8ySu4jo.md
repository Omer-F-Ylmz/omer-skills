# blender-python-kodu-ile-video-uretim (Dewd8ySu4jo)

**Amaç:** AI video modelleri yerine kod tabanlı frame-by-frame kontrol ile video üretimi.
**Araçlar:** Claude Code (AI), Blender (3D Rendering), Python (Scripting), Node (Arayüz), ffmpeg (Video Dönüşümü)

**Adımlar**
1. [0:07-0:10] Claude tarafından her frame için 'ekran neye benzemeli?' sorusuna yanıt veren Python scripti oluşturulur.
2. [0:10-0:15] Script, Blender'a her frame için nesne konumları, ışık ve kamera ayarlarını gönderir.
3. [0:15-0:20] Blender render işlemini gerçekleştirir ve frame'ları oluşturur.
4. [0:20-0:25] Boş/bozuk frame'lar tespit edilir ve sadece o frame'lar yeniden render edilir.
5. [0:25-0:30] Python ile müzik ve ses efektleri sentezlenir.
6. [0:30-0:32] ffmpeg kullanılarak render edilmiş frame'lar video dosyasına dönüştürülür.

**Prompt/kod/ayar:** Claude Code: 'What should the screen look like at this exact moment?'
**Sonuç:** 12 saniye, 1080p, 30 fps video (sesli)
**Bizde (öneri, modelden):** kurulu araçlarla nasıl: Blender + Python scriptleri ile her frame için kod tabanlı kontrol sağlanabilir, ancak AI destekli prompt optimizasyonu için Claude Code gibi araçlar kullanılabilir.
**Daha iyi (öneri):** AI modelleri yerine kod tabanlı kontrol ile daha düşük maliyetli ve daha kontrol edilebilir video üretimi sağlanabilir.
