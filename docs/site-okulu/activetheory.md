# activetheory — mekanizma kartı (SİTE-OKULU-1)
Ham: `.kos/site-okulu/activetheory/` (yerel). Gemini gemini-3.5-flash-lite, 4531 jeton; Claude görüntü okumadı.

## Ne görülüyor (Gemini, 'tahmin' doğrulanmadı)
- 00:01 Siyah fon üzerinde dairesel yükleme sayacı ve desen
- 00:06 Yükleme tamamlanıyor, 3B dairesel logo ve parçacık efekti ortaya çıkıyor
- 00:11 'CREATIVE DIGITAL EXPERIENCES' metni ve 3B halka/logo objesi
- 00:13 Projelerin listelendiği 3B kaydırılabilir kart sistemi ve arka planda organik dokular
- **Kamera:** sürekli yol mu, bölüm başına poz mu, sabit mi; hareket türü: Bölüm başına yumuşak geçişli poz/kaydırma tabanlı 3B kamera hareketi (tahmin)
- **Geçiş:** kesme; solma; RT kompozit; parçacık/noise tabanlı geçiş (tahmin)
- **Post:** bloom; DoF; gren; kromatik; vinyet
- **Tipografi:** dev başlık, satır/harf bölme animasyonu, 3B ile katmanlama
- **Yükleyici:** % sayacı, süre, tasarımı: Dairesel döküm/halka şeklinde, merkezde yüzde sayacı, kabaca 5-6 saniye süren 3B yükleme animasyonu
- **Ses:** Görünür ses düğmesi videoda yer almıyor (tahmin: arka plan sesleri web sitesinde mevcut olabilir)
- **Etkileşim:** imleç takibi; hover; sürükleme; tık kapısı
- **Mobil:** mobil karelerde 3B var mı, sadeleşme nasıl: Mobil ekranlarda aynı 3B cam/metalik halka objesi korunuyor, dikey düzene uyarlanmış sadeleşmiş arayüz ve dokunmatik kaydırma
- **Kod çapraz:** bloom ✓ · DoF/blur ✓ · kromatik ✗ · gren/dither ✗ · maske geçiş ✓ · scroll uniform ✓ · SplitText ✗ · ses kütüphanesi ✗

## Nasıl yapılmış (kod kanıtı)
- İmza: three-composer, theatre, ktx2, draco, splat
- Shader: 228 `void main` penceresi; sınıf: noise 100, kaydirma-uniform 80, matcap 54, fresnel 45, blur 44, gecis/maske 35, parcacik 28, bloom 21
- JS 2864 KB · sayfa docH 900 · canvas 2160x1350 static · yük 1031 ms
- Bütçe (perf API, çapraz kökende eksik sayar): 0.77 MB / 41 istek · mobil 0.77 MB · tür KB {'js': 410, 'wasm': 254, 'vs': 40, 'woff2': 39, 'json': 25, 'png': 2, 'mp4': 1, 'diger': 0}

## Öne çıkan teknikler (Gemini)
- WebGL tabanlı gerçekçi cam ve metalik shader materyalleri
- Parçacık sistemleri ve organik arka plan dokuları
- 3B kart döngüsü (carousel) kaydırma mekanizması
- Derin alan efekti (Depth of Field) ve post-processing entegrasyonu
- Tipografi ile 3B objelerin katmanlı derinlik uyumu
- Akıcı yükleme ekranı ve sahne geçiş senkronizasyonu

## Hazır karşılığı
- `teknikler.md` maddeleri: 1, 4, 6, 7, 15, 18 (kaynak + lisans orada)

## Zorluk: 5/5 (Gemini) · token: kart başına Claude ~0 (betik üretti)
