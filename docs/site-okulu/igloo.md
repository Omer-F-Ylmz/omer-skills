# igloo — mekanizma kartı (SİTE-OKULU-1)
Ham: `.kos/site-okulu/igloo/` (yerel). Gemini gemini-3.5-flash-lite, 4708 jeton; Claude görüntü okumadı.

## Ne görülüyor (Gemini, 'tahmin' doğrulanmadı)
- 00:00 Minimalist yükleme ekranı, gri arka plan üzerinde ortalanmış yükleme animasyonu.
- 00:06 Wireframe (tel kafes) şeklinde igloo ve zemin yapısının belirme aşaması.
- 00:09 İgloo modelinin kaplanması, karlı zemin ve atmosferik sis efektinin eklenmesi.
- 00:11 Ana sayfa görünümü, igloo blokları üzerinde numaralandırma ve sol/sağ köşelerde kurumsal metinler.
- 00:14 Kameranın yukarı doğru kayarak bulutlar ve sis arasından geçişi.
- 00:15 Havada asılı duran kırık buz/taş portfolyo objesi ve detay metinleri.
- **Kamera:** sürekli yol mu, bölüm başına poz mu, sabit mi; hareket türü: Bölüm başına poz geçişleri ve kaydırma (scroll) ile tetiklenen akışkan 3B kamera hareketleri, Z ekseninde derinlik geçişleri.
- **Geçiş:** kesme; solma; z ekseninde uçuş/kameranın bulutların içinden geçmesi; noise-maske; dönüşüm
- **Post:** bloom; DoF (Derinlik Algısı); film greni; kromatik sapma (chromatic aberration); vinyet; atmosferik sis
- **Tipografi:** Modern sans-serif, başlıklar üst köşelerde konumlanmış, tahmin: satır ve harf bölme animasyonları, 3B objelerle derinlikli katmanlama.
- **Yükleyici:** Gri tonlarında minimalist çizgi/karakter tabanlı yükleme animasyonu, tahmin: %0-%100 sayacı barındırıyor, süre yaklaşık 6 saniye.
- **Ses:** Sol alt köşede 'Sound: Off' / ses düğmesi göstergesi mevcut.
- **Etkileşim:** imleç takibi; hover ile blok numaralandırmaları; scroll tabanlı 3B sahne ilerlemesi; tık kapısı (click to explore)
- **Mobil:** Mobil karelerde tam 3B sahne korunmuş, tahmin: shader optimizasyonları ve düşük poligonlu modellerle performans için sadeleşmeye gidilmiş, arayüz dikey ekrana uyarlanmış.
- **Kod çapraz:** bloom ✓ · DoF/blur ✓ · kromatik ✓ · gren/dither ✓ · maske geçiş ✓ · scroll uniform ✓ · SplitText ✗ · ses kütüphanesi ✗

## Nasıl yapılmış (kod kanıtı)
- İmza: pmndrs-post, three-composer, gsap, scrolltrigger, ktx2, draco, meshopt, webgpu, svelte, splat
- Shader: 236 `void main` penceresi; sınıf: gecis/maske 44, kaydirma-uniform 34, dither 31, parcacik 27, akiskan 25, blur 22, noise 22, kirilma 14
- JS 1835 KB · sayfa docH 900 · canvas yok/iframe · yük 593 ms
- Bütçe (perf API, çapraz kökende eksik sayar): 15.4 MB / 95 istek · mobil 15.4 MB · tür KB {'ktx2': 11011, 'ogg': 2945, 'js': 571, 'drc': 556, 'wasm': 315, 'json': 2, 'png': 2}

## Öne çıkan teknikler (Gemini)
- Wireframe'den 3B dokulu modele geçiş animasyonu
- Scroll pozisyonuna bağlı Z ekseni kamera uçuşu
- Kromatik sapma ve film greni ile sinematik post-processing
- İgloo blokları üzerinde interaktif UI numaralandırma katmanı
- Havadaki kırık buz objelerinde ray-marching veya yüksek detaylı normal map kullanımı
- Minimalist ve akışkan yükleme ekranı geçişi

## Hazır karşılığı
- `teknikler.md` maddeleri: 1, 4, 5, 6, 7, 8, 15, 18, 21 (kaynak + lisans orada)

## Zorluk: 5/5 (Gemini) · token: kart başına Claude ~0 (betik üretti)
