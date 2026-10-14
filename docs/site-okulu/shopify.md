# shopify — mekanizma kartı (SİTE-OKULU-1)
Ham: `.kos/site-okulu/shopify/` (yerel). Gemini gemini-3.5-flash-lite, 4437 jeton; Claude görüntü okumadı.

## Ne görülüyor (Gemini, 'tahmin' doğrulanmadı)
- 00:00 Boş gri yükleme ekranı tahmini
- 00:02 İlk 3B raflar ve kapakların yüklenmesi
- 00:03 İkinci rafın ve alt zaman çizelgesinin belirginleşmesi
- 00:04 Zaman çizelgesinde yıl ve konu etiketlerinin yerleşmesi
- 00:23 Mobil görünümde 3B dikey katmanlı kart yığını
- **Kamera:** bölüm başına poz mu, sabit mi; hafif açısal perspektif geçişleri
- **Geçiş:** kesme; solma; dönüşüm tahmini
- **Post:** gölge; vinyet tahmini
- **Tipografi:** dev başlık, satır/harf bölme animasyonu tahmini
- **Yükleyici:** % sayacı görünmüyor, gri ekran fonu ile hızlı geçiş tahmini
- **Ses:** görünür ses düğmesi mevcut (mobil karelerde)
- **Etkileşim:** imleç takibi; hover; sürükleme tahmini
- **Mobil:** mobil karelerde 3B var, yatay raflar yerine dikey üst üste binen kart yığını olarak sadeleşmiş
- **Kod çapraz:** bloom ✗ · DoF/blur ✓ · kromatik ✓ · gren/dither ✓ · maske geçiş ✓ · scroll uniform ✗ · SplitText ✗ · ses kütüphanesi ✗

## Nasıl yapılmış (kod kanıtı)
- İmza: r3f, lenis, barba, ktx2, draco, meshopt, react, splat
- Shader: 71 `void main` penceresi; sınıf: dither 20, kirilma 9, fresnel 9, golge 8, instancing 6, matcap 6, parcacik 6, tonemap 4
- JS 4224 KB · sayfa docH 900 · canvas 1440x900 static · yük 3578 ms
- Bütçe (perf API, çapraz kökende eksik sayar): 2.62 MB / 72 istek · mobil 1.97 MB · tür KB {'webp': 873, 'mp4': 833, 'js': 695, 'diger': 135, 'glb': 51, 'png': 26, 'css': 10, 'gif': 0}

## Öne çıkan teknikler (Gemini)
- 3B raf ve kitap/dergi kapağı modeli
- Zaman çizelgesi senkronizasyonu
- Duyarlı 3B görünüm uyarlaması (mobil için yığın)
- WebGL tabanlı doku kaplama
- Gerçekçi gölgelendirme

## Hazır karşılığı
- `teknikler.md` maddeleri: 6, 7, 8, 13, 15, 18 (kaynak + lisans orada)

## Zorluk: 4/5 (Gemini) · token: kart başına Claude ~0 (betik üretti)
