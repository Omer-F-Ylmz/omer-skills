# ciao — mekanizma kartı (SİTE-OKULU-1)
Ham: `.kos/site-okulu/ciao/` (yerel). Gemini gemini-3.5-flash-lite, 4691 jeton; Claude görüntü okumadı.

## Ne görülüyor (Gemini, 'tahmin' doğrulanmadı)
- 00:01 Siyah arka plan üzerinde dikey konumlandırılmış gri tonlarda 'Ciro Energy' logosu ve %0 yükleme sayacı (tahmin)
- 00:09 Yükleme tamamlanıyor, ekranda beliren enerji kutusu modeli ile ana sahne açılıyor
- 00:10 Merkezde 'Double Litchi' yazılı kutu ve kaydırma göstergesi
- 00:11 Kullanıcı kaydırmasıyla yanlardan yeni kutu varyasyonlarının gelmesi (tahmin)
- 00:14 Kutunun yakın plana geçmesi, 'Double Litchi' metni ve açıklaması
- 00:16 Kutunun dönerek arka yüzündeki içerik detaylarını göstermesi
- **Kamera:** Bölüm başına poz mu, sabit mi; kaydırma eksenine duyarlı kontrollü 3B yörünge hareketi
- **Geçiş:** Scroll tabanlı yumuşak interpolasyon (lerp); Kamera rotasyonu ve FOV değişimi
- **Post:** bloom; vinyet; hafif alan derinliği (DoF)
- **Tipografi:** Dev başlık, dikey kayan metinler, harf düzeyinde animasyon, 3B mekan içinde katmanlama
- **Yükleyici:** % sayacı, yaklaşık 9-10 saniye, siyah zemin üzerinde minimal dikey logo ve sayı
- **Ses:** Sol üst köşede görünür ON/OFF ses düğmesi
- **Etkileşim:** imleç takibi; hover; scroll tabanlı 3B nesne kontrolü; sağ tarafta bölüm atlama ikonları
- **Mobil:** Mobil karelerde 3B aktif, dikey tasarıma uyarlanmış sadeleşmiş arayüz ve dokunmatik kaydırma
- **Kod çapraz:** bloom ✓ · DoF/blur ✓ · kromatik ✗ · gren/dither ✓ · maske geçiş ✗ · scroll uniform ✓ · SplitText ✓ · ses kütüphanesi ✗

## Nasıl yapılmış (kod kanıtı)
- İmza: three=161, three-composer, gsap, scrolltrigger, splittext, lenis, ktx2, draco, meshopt, lottie
- Shader: 68 `void main` penceresi; sınıf: dither 19, blur 13, bloom 10, aa 8, golge 8, kirilma 7, instancing 6, parcacik 6
- JS 2439 KB · sayfa docH 12807 · canvas 1440x900 fixed · yük 1829 ms
- Bütçe (perf API, çapraz kökende eksik sayar): 0.35 MB / 73 istek · mobil 0.71 MB · tür KB {'js': 350, 'css': 0, 'avif': 0, 'svg': 0, 'woff2': 0, 'webm': 0, 'mjs': 0, 'hdr': 0}

## Öne çıkan teknikler (Gemini)
- WebGL ile yüksek kaliteli ürün render ve shader kullanımı
- Scroll (kaydırma) pozisyonuna bağlı senkronize kamera ve metin animasyonları
- Dinamik yansımalar ve metalik malzeme shaders
- UI ve 3B dünya koordinatlarının kusursuz eşleşmesi
- Mobil uyumlu duyarlı 3B viewport optimizasyonu

## Hazır karşılığı
- `teknikler.md` maddeleri: 1, 6, 7, 8, 9, 15 (kaynak + lisans orada)

## Zorluk: 5/5 (Gemini) · token: kart başına Claude ~0 (betik üretti)
