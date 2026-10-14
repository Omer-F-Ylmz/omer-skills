# abeto — mekanizma kartı (SİTE-OKULU-1)
Ham: `.kos/site-okulu/abeto/` (yerel). Gemini gemini-3.5-flash-lite, 4443 jeton; Claude görüntü okumadı.

## Ne görülüyor (Gemini, 'tahmin' doğrulanmadı)
- 00:01 Beyaz arkaplanda zarf ikonu ve 'loading' yazısı içeren minimalist yükleme ekranı.
- 00:03 Turkuaz renkli dalgalı bir dalga ile yükleme ekranının yukarı kayarak açılması.
- 00:04 Turkuaz deniz ortasında küçük dairesel bir 3B ada modelinin belirerek ortaya çıkması.
- 00:05 Adanın detaylarının yüklenmesi, üzerindeki binalar ve yeşilliklerin görünür hale gelmesi.
- 00:06 Adanın üzerinde büyük, kalın 3B harflerle 'MESSENGER' başlığı ve altında sarı 'BEGIN' butonu beliriyor.
- 00:07 Sahne sabit kalırken dairesel adanın yavaşça kendi ekseni etrafında dönmeye başlaması.
- **Kamera:** sabit, adanın kendi ekseni etrafında dairesel dönüş hareketi
- **Geçiş:** solma; maske tabanlı açılış
- **Post:** toon shading; kenar çizgisi (outline)
- **Tipografi:** dev 3B blok harfler, kalın ve gölgeli tipografi
- **Yükleyici:** zarf ikonu ve 'loading' metni, tahmini % sayacı içermeyen sanat yönetimi odaklı yükleyici
- **Ses:** görünür ses düğmesi yok
- **Etkileşim:** hover; tık edilebilir 'BEGIN' butonu
- **Mobil:** mobil karelerde 3B ada modeli korunmuş, dikey düzene uyarlanmış

## Nasıl yapılmış (kod kanıtı)
- İmza: three=180, pmndrs-post, three-composer, ktx2, draco, meshopt, webgpu, svelte
- Shader: 221 `void main` penceresi; sınıf: dither 28, noise 22, instancing 19, golge 18, blur 14, parcacik 12, kirilma 9, matcap 6
- JS 2253 KB · sayfa docH 900 · canvas yok/iframe · yük 1000 ms
- Bütçe (perf API, çapraz kökende eksik sayar): 5.87 MB / 111 istek · mobil 5.87 MB · tür KB {'ogg': 3685, 'js': 577, 'ktx2': 573, 'drc': 504, 'font': 261, 'wasm': 232, 'icon': 35, 'png': 2}

## Öne çıkan teknikler (Gemini)
- Toon shading / Cel-shading 3B ada modeli
- Dairesel dönen dünya efekti
- 3B dev tipografi entegrasyonu
- Özel çizim tarzı arayüz elemanları
- Dinamik yükleme animasyonu

## Hazır karşılığı
- `teknikler.md` maddeleri: 4, 6, 7, 8, 15, 21 (kaynak + lisans orada)

## Zorluk: 4/5 (Gemini) · token: kart başına Claude ~0 (betik üretti)
