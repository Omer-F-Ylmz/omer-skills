# apple — mekanizma kartı (SİTE-OKULU-1)
Ham: `.kos/site-okulu/apple/` (yerel). Gemini gemini-3.5-flash-lite, 5245 jeton; Claude görüntü okumadı.

## Ne görülüyor (Gemini, 'tahmin' doğrulanmadı)
- 00:01 AirPods Pro 3 tanıtım başlığı ve 3B ürün görseli ile açılış.
- 00:04 Tahmin: Aktif gürültü engelleme özelliğini vurgulayan video/dansçı arka plan geçişi.
- 00:07 Ürün detayları ve siluet formunda AirPods gösterimi.
- 00:11 Tahmin: Kulaklık içi bileşenlerin ve akustik mimarinin 3B şeffaf kesit gösterimi.
- 00:14 Fitness ve kalp atış hızı sensörü odaklı özellik sunumu.
- 00:18 İşitme sağlığı ve pil ömrü özellikleri için kart tabanlı slider alanı.
- **Kamera:** Bölüm başına poz geçişleri ve scroll-driven (kaydırma tabanlı) yumuşak 3B model rotasyonları.
- **Geçiş:** kesme; solma; tahmin: kaydırma tabanlı (scroll-linked) WebGL shader geçişleri ve maskeleme
- **Post:** tahmin: hafif bloom; tahmin: alan derinliği (DoF); tahmin: kromatik sapma
- **Tipografi:** Dev başlıklar, sans-serif Apple San Francisco tipografi ailesi, satır/karakter bazlı kaydırma animasyonları, 3B katmanlama.
- **Yükleyici:** Görünür yüzde sayacı yok; tahmin: standart Apple tarzı hafif loader veya progressive asset streaming.
- **Ses:** Sağ üst köşede video/animasyon oynatımını durdurup/başlatan oynat/durdur (pause/play) kontrol düğmesi.
- **Etkileşim:** imleç takibi; hover; yatay/dikey sürükleme (slider); tık kapısı
- **Mobil:** Mobil karelerde 3B modeller korunuyor; alt alta dikey akışa uygun sadeleşmiş kart yapıları ve dokunmatik optimizasyonlar kullanılıyor.

## Nasıl yapılmış (kod kanıtı)
- İmza: —
- Shader: 0 `void main` penceresi; sınıf: —
- JS 3311 KB · sayfa docH 29233 · canvas yok/iframe · yük 1688 ms
- Bütçe (perf API, çapraz kökende eksik sayar): 22.67 MB / 153 istek · mobil 11.75 MB · tür KB {'mp4': 7896, 'png': 5675, 'webm': 4262, 'jpg': 2744, 'js': 992, 'woff2': 854, 'css': 150, 'diger': 95}

## Öne çıkan teknikler (Gemini)
- Scroll pozisyonuna senkronize edilmiş 3B ürün parçalarına ayrılma (exploded view) animasyonu
- Video siluetleri ile 3B arkaplan efektlerinin GPU tabanlı kompozisyonu
- Akıcı kart tabanlı slider ve etkileşimli özellik karşılaştırma modülleri
- Yüksek performanslı WebGL model yükleme ve optimizasyonu
- Duyarlı tipografi ve maskelenmiş geçiş efektleri
- Kullanıcı kontrolü için video/animasyon durdurma entegrasyonu

## Hazır karşılığı
- `teknikler.md` maddeleri: — (kaynak + lisans orada)

## Zorluk: 5/5 (Gemini) · token: kart başına Claude ~0 (betik üretti)
