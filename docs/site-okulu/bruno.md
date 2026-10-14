# bruno — mekanizma kartı (SİTE-OKULU-1)
Ham: `.kos/site-okulu/bruno/` (yerel). Gemini gemini-3.5-flash-lite, 4438 jeton; Claude görüntü okumadı.

## Ne görülüyor (Gemini, 'tahmin' doğrulanmadı)
- 00:00 tahmin: Boş beyaz yükleme ekranı
- 00:01 Koyu mor zemin üzerinde grid çizgileri beliriyor
- 00:02 Ortada parlayan neon çember beliriyor
- 00:07 Çember içinden parçacık efektiyle 3B sahne yükseliyor
- 00:08 Ağaç, sokak lambası, çit ve kırmızı arazi aracından oluşan diorama tamamlanıyor; 'Click to start' yazısı ve ses ikonu beliriyor
- **Kamera:** sabit mi; izometrik/ortografik açı, hafif yukarıdan bakan sabit 3B kamera görünümü
- **Geçiş:** kesme; parçacık tabanlı belirme efekti
- **Post:** bloom; parçacık/nokta matris greni
- **Tipografi:** el yazısı stilinde 'Click to start' yönlendirmesi
- **Yükleyici:** % sayacı görünmüyor, tahmini 1-2 saniyelik siyah/beyaz başlangıç ekranı
- **Ses:** görünür ses açma/kapama ikonu sağ tarafta yer alıyor
- **Etkileşim:** tık kapısı (Click to start); tahmin: imleç ile etkileşimli 3B diorama kontrolü
- **Mobil:** mobil karelerde 3B model aynen korunuyor, dikey orana uyarlanmış grid yapısı kullanılıyor

## Nasıl yapılmış (kod kanıtı)
- İmza: three=183, three-composer, gsap, scrolltrigger, howler, ktx2, draco, meshopt, webgpu, tsl, rapier
- Shader: 5 `void main` penceresi; sınıf: parcacik 2
- JS 5676 KB · sayfa docH 900 · canvas 1440x900 static · yük 1406 ms
- Bütçe (perf API, çapraz kökende eksik sayar): 7.51 MB / 115 istek · mobil 7.51 MB · tür KB {'wasm': 2512, 'mp3': 1975, 'js': 1093, 'glb': 1004, 'ktx': 878, 'woff2': 23, 'ico': 15, 'css': 7}

## Öne çıkan teknikler (Gemini)
- Grid tabanlı perspektif zemin
- Parçacık efektiyle nesne türetme (spawn)
- Neon çember ışıklandırması ve bloom
- İzometrik low-poly diorama tasarımı
- Etkileşimli başlangıç kapısı (Click to start)

## Hazır karşılığı
- `teknikler.md` maddeleri: 1, 6, 7, 12, 15, 20, 21 (kaynak + lisans orada)

## Zorluk: 4/5 (Gemini) · token: kart başına Claude ~0 (betik üretti)
