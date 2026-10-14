# lando — mekanizma kartı (SİTE-OKULU-1)
Ham: `.kos/site-okulu/lando/` (yerel). Gemini gemini-3.5-flash-lite, 4791 jeton; Claude görüntü okumadı.

## Ne görülüyor (Gemini, 'tahmin' doğrulanmadı)
- 00:00 Neon sarı arka plan üzerinde yükleme ekranı ve 'LOAD 00/100' ibaresi
- 00:03 Hero bölümü: Yüzün üzerine katmanlanmış şeffaf kask vizörü ve 3B/2B arayüz öğeleri
- 00:07 Metin ve hikaye anlatımı bölümü, büyük tipografi blokları ve koyu arka plan
- 00:09 Asimetrik fotoğraf galerisi ve medya ızgarası, topoğrafik çizgi arka plan
- 00:15 'Helmets Hall of Fame' bölümü, özel kask tasarımlarının sergilendiği grid yapısı
- 00:19 Partners & Campaigns bölümü, marka logoları ve ortaklık kaydırma alanı
- **Kamera:** bölüm başına poz, dikey kaydırma eksenli yumuşak interpolasyon
- **Geçiş:** kesme; solma; dönüşüm; scroll-tabanlı parallax kaydırma
- **Post:** gren; vinyet; hafif kromatik sapma
- **Tipografi:** dev başlık, satır ve harf bölme animasyonu, 3B derinlik katmanlaması
- **Yükleyici:** % sayacı (0-100), tahmini 3-4 saniye, minimalist tipografik tasarım
- **Ses:** görünür ses düğmesi veya ses durumu tespiti yok (tahmin: arayüz ses efektleri mevcut olabilir)
- **Etkileşim:** imleç takibi; hover efektleri; yatay/dikey sürükleme; tık kapısı
- **Mobil:** mobil karelerde 3B vizör efekti korunmuş, karmaşık grid yapılar dikey akış için sadeleştirilmiş

## Nasıl yapılmış (kod kanıtı)
- İmza: three-composer, gsap, scrolltrigger, splittext, lenis, ktx2, draco, meshopt, webgpu, rive · gsap 3.13.0
- Shader: 88 `void main` penceresi; sınıf: dither 21, matcap 16, gecis/maske 16, noise 9, instancing 8, bloom 8, kirilma 7, kaydirma-uniform 7
- JS 2023 KB · sayfa docH 13577 · canvas 60x60 static, 36x36 static · yük 781 ms
- Bütçe (perf API, çapraz kökende eksik sayar): 0.23 MB / 123 istek · mobil 0.23 MB · tür KB {'diger': 227, 'css': 0, 'woff2': 0, 'svg': 0, 'js': 0, 'webp': 0, 'wasm': 0, 'png': 0}

## Öne çıkan teknikler (Gemini)
- şeffaf kask vizörünün yüz üzerine 3B katmanlanması
- topoğrafik çizgi desenli SVG/WebGL arka plan
- asimetrik fotoğraf ve medya yerleşimi
- scroll tetiklemeli tipografi animasyonları
- kesintisiz marka ortakları kaydırma bandı
- interaktif kask sergileme galerisi

## Hazır karşılığı
- `teknikler.md` maddeleri: 1, 4, 7, 8, 9, 15, 21, 22 (kaynak + lisans orada)

## Zorluk: 5/5 (Gemini) · token: kart başına Claude ~0 (betik üretti)
