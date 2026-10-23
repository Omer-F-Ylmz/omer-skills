## Yapım promptu şablonu
Site/UI'ı başka bir ajana (ya da alt ajana) yaptırırken prompt bu satırları taşır. Kural kapsamları: omer-kurallar:25 "site/UI yapım promptlarında" (teknoloji + dosya) · omer-kurallar:26 "3D/animasyonlu sahnelerde" (config); küçük işte "en basit çözüm" önde. Videolardan çıkan kalıplar: `docs/departmanlar/frontend-promptlar.md`.
- teknoloji: kütüphane + sürüm (ör. Three.js r160, GSAP 3.12, Lenis 1.1, Vite 5); yalnız omer-kutuphaneler rafından.
- dosya: dosya başına tek sorumluluk (ör. main.js sahne · style.css tipografi · config.js parametreler).
- config: ayarlanabilir sahne parametreleri (görsel sayısı, hız, boşluk) tek CONFIG nesnesi/dosyasında; yalnız 3D/animasyonlu sahnede.
- hareket: animasyon terimleriyle tarif (scroll reveal, stagger, parallax, easing, süre); prefers-reduced-motion karşılığı.
- asset: görsel/video/font listesi, oran ve ton (ör. 12 dikey fotoğraf, koyu arka plan); yoksa üretim yolu. 3D model: ~2 MB tercih (sıkıştırılmış GLB), 6 MB detay yalnız gerekçeyle (24c K7).
- kabul: ölçülebilir kabul (ör. 60 fps, 390/768/1440 taşma yok, axe 0 hata, LCP sayısı).
- dokunulmaz: hazır tasarım promptu mevcut siteye uygulanırken dokunulmaz alanlar adıyla (ör. hero, mevcut animasyonlar); prompttan yalnız ilgili bölüm alınır (K3, 24 Eyl). Elle ayarlanmış 3D pozisyon/kamera/ışık değerleri de dokunulmaz alandır (24c K7).
- bileşen: bütün butonlar tek bileşenden varyantla; hover/focus/active o bileşende (K16, 24 Eyl).
- perspektif: 3D/derinlik sahnesinde kamera açısı, perspektif ve eğim sayıyla yazılır (ör. perspective 1200px, rotateX 12°); yazılmazsa kartlar düz ya da yanlış açıda çıkar.
- klasör: görseller önce `public/` altına konur; promptta klasör adı ve dağıtım kuralı (rastgele/dengeli) verilir, ajan dosyaları kendisi yerleştirir.
- sahne: video üretim promptunda sahne sahne kamera hareketi, ışık ve atmosfer ayrı cümlelerle tarif edilir.

## Kurulu araç notları
- Site + 3D işinin adım/araç/kapı sırası: `docs/atlas/site-3d.md` (ATLAS kararları `docs/atlas/kart.jsonl`).
- `scroll-craft`: görsel üretimi ücretli kie.ai API'sini çağırır; yalnız Ömer onayı ve çağrı tavanıyla ("en fazla N").
- `design-dna`: "varlığı kaynak URL'den al" adımı referans sitelerde uygulanmaz; referanstan yalnız stil/teknik alınır, görsel/font/3D model/video izinsiz kullanılmaz (lisanslı ya da müşteri varlığı).
