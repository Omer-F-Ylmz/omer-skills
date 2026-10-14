# oryzo — mekanizma kartı (SİTE-OKULU-1)
Ham: `.kos/site-okulu/oryzo/` (yerel). Gemini gemini-3.5-flash-lite, 6204 jeton; Claude görüntü okumadı.

## Ne görülüyor (Gemini, 'tahmin' doğrulanmadı)
- 00:00 Beyaz ekran ve yükleme başlangıcı
- 00:02 Yeşil arayüz üzerinde odaklanma halkası ve yükleme grafiği
- 00:05 Ana sayfa açılışı, mantar bardak altlığı görseli ve Oryzo başlığı
- 00:09 El tutuşunda 3B mantar bardak altlığı görünümü
- 00:14 Giyilebilir ürün konsepti ve ceket üzerinde altlık
- 00:20 Dergi kapağı entegrasyonu ve tasarım detayları
- **Kamera:** sürekli yol mu, bölüm başına poz mu, sabit mi; hareket türü: tahmin: Kaydırma tabanlı sürekli kamera yolu (scrolling camera path) ve sahne değişimlerinde yumuşak poz geçişleri
- **Geçiş:** tahmin: Yumuşak kesmeler; tahmin: Kaydırma tabanlı parallax geçişleri; tahmin: Noise maske ve RT kompozit
- **Post:** bloom; DoF; gren; vinyet
- **Tipografi:** Dev başlıklar, satır/harf bölme animasyonları, 3B nesnelerle katmanlanmış tipografi
- **Yükleyici:** % sayacı ve dairesel çizgesel tasarım (00:02 - 00:04 arası)
- **Ses:** tahmin: Görünür özel bir ses düğmesi bulunmuyor, arayüzde sesli geri bildirimler yer alıyor
- **Etkileşim:** imleç takibi; hover; sürükleme; tık kapısı
- **Mobil:** mobil karelerde 3B var mı, sadeleşme nasıl: tahmin: 3B modeller korunmuş, dikey düzene uygun olarak arayüz elemanları ve metin blokları sadeleştirilmiş, tek sütunlu yapıya geçilmiş

## Nasıl yapılmış (kod kanıtı)
- İmza: three=178, gsap, splittext, rive, splat · gsap 3.47.0
- Shader: 117 `void main` penceresi; sınıf: blur 48, dither 12, bloom 11, vinyet 9, aa 9, dof 8, gecis/maske 6, gpgpu 5
- JS 3132 KB · sayfa docH 56691 · canvas 1440x900 fixed, 571x734 absolute · yük 3437 ms
- Bütçe (perf API, çapraz kökende eksik sayar): 21.87 MB / 148 istek · mobil 20.85 MB · tür KB {'webp': 6633, 'mp4': 6451, 'buf': 3629, 'sog': 3580, 'avif': 539, 'png': 521, 'js': 306, 'woff2': 126}

## Öne çıkan teknikler (Gemini)
- Gerçekçi mantar doku shader'ları ve fizik tabanlı malzeme (PBR) işleme
- Kaydırma ile senkronize çalışan 3B kamera yolu ve model animasyonları
- Termal kamera ve teknik çizim katman efektleri
- HTML/WebGL katman bileşimi ile derinlik hissi
- Duyarlı mobil adaptasyon ve dokunmatik etkileşim optimizasyonu
- Gelişmiş post-processing (DoF ve bloom kombinasyonu)

## Hazır karşılığı
- `teknikler.md` maddeleri: 4, 6, 7, 8, 9, 18, 22 (kaynak + lisans orada)

## Zorluk: 5/5 (Gemini) · token: kart başına Claude ~0 (betik üretti)
