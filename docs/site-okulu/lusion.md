# lusion — mekanizma kartı (SİTE-OKULU-1)
Ham: `.kos/site-okulu/lusion/` (yerel). Gemini gemini-3.5-flash-lite, 4807 jeton; Claude görüntü okumadı.

## Ne görülüyor (Gemini, 'tahmin' doğrulanmadı)
- 00:00 Siyah fon üzerinde beyaz % sayacı ile yükleyici ekranı başlangıcı (tahmin)
- 00:05 Yükleyicinin tamamlanması ve ana sayfaya geçiş
- 00:07 LUSION logosu, üst menü ve 3B interaktif mavi-beyaz-siyah nesne sahnesi
- 00:09 Metin içerikleri ve sol tarafta organik mavi dalgalı/boya izi efekti
- 00:11 Kırmızı fonlu 'PLAY REEL' video gösterim alanı ve mobil önizleme kareleri
- 00:13 Projelerin listelendiği 'Featured Work' grid bölümü (Görseller ve etiketler)
- **Kamera:** bölüm başına poz mu, sabit mi; hareket türü: Kaydırma (scroll) ile tetiklenen yumuşak kamera geçişleri ve 3B sahnelerde orbital/serbest rotasyon (tahmin)
- **Geçiş:** kesme; solma; noise-maske; dönüşüm (tahmin)
- **Post:** bloom; DoF; gren; vinyet; kromatik sapma (tahmin)
- **Tipografi:** dev başlık, satır/harf bölme animasyonu, 3B ile katmanlama
- **Yükleyici:** % sayacı, süre, tasarımı: Siyah arka plan, minimalist beyaz tipografi ile sayaç ve ilerleme çubuğu
- **Ses:** görünür ses düğmesi vb.: Arayüzde özel bir ses düğmesi görünmüyor, minimalist üst menü kullanılmış
- **Etkileşim:** imleç takibi; hover; sürükleme; tık kapısı
- **Mobil:** mobil karelerde 3B var mı, sadeleşme nasıl: Mobil karelerde 3B nesneler korunmuş ancak performans için optimize edilmiş dikey yerleşim kullanılmış (tahmin)
- **Kod çapraz:** bloom ✓ · DoF/blur ✓ · kromatik ✓ · gren/dither ✓ · maske geçiş ✓ · scroll uniform ✗ · SplitText ✗ · ses kütüphanesi ✗

## Nasıl yapılmış (kod kanıtı)
- İmza: three=158
- Shader: 156 `void main` penceresi; sınıf: dither 30, blur 30, kirilma 19, matcap 16, bloom 12, parcacik 11, noise 10, aa 8
- JS 1918 KB · sayfa docH 900 · canvas 1440x900 fixed, 45x45 static · yük 2875 ms
- Bütçe (perf API, çapraz kökende eksik sayar): 0.52 MB / 107 istek · mobil 0.6 MB · tür KB {'js': 306, 'woff2': 191, 'css': 14, 'diger': 6, 'svg': 2, 'ico': 1, 'json': 0, 'ogg': 0}

## Öne çıkan teknikler (Gemini)
- WebGL tabanlı gerçek zamanlı 3B nesne etkileşimi
- Özel shader tabanlı boya/dalga Efektleri
- Scroll tabanlı akışkan kamera ve sahne yönetimi
- DOM elementleri ile 3B katman entegrasyonu
- Performans odaklı mobil duyarlı 3B sadeleştirme
- Minimalist ve akışkan tipografi animasyonları

## Hazır karşılığı
- `teknikler.md` maddeleri: 4, 6, 7, 8 (kaynak + lisans orada)

## Zorluk: 5/5 (Gemini) · token: kart başına Claude ~0 (betik üretti)
