---
name: animasyon-atolyesi
description: Hazır, ölçülmüş animasyon tarifleri — web giriş/scroll, sayfa geçişi, Three.js parçacık, Blender patlatılmış görünüm + GLB, ffmpeg intro videosu; sıfırdan yazmak yerine kopyala-uyarla, headless ölç.
---

# Animasyon atölyesi

Animasyon/efekt işinde buradaki tarifi TEK KOMUTLA üret + ölç. Her ek tur tüm bağlamı yeniden okur; tarifi açıp okuma, Write/Edit ile elle uyarlama, kareye bakma turları sıfırdan yazmaktan pahalıya gelir. Tarifler 60 fps, `prefers-reduced-motion` ve pencere açmama kurallarını zaten taşır.

## Tarif seçimi

| İstek | Tarif | Bağımlılık |
|---|---|---|
| Hero kademeli giriş, scroll'la belirme, ilerleme çubuğu | `tarifler/giris-scroll.html` | yok |
| Liste ↔ detay, paylaşılan öğe morfu, sayfa geçişi | `tarifler/sayfa-gecisi.html` (View Transitions) | yok |
| WebGL hero arka planı, parçacık/buhar/toz, fare etkileşimi | `tarifler/parcacik-three.html` | three (CDN importmap) |
| 3D patlatılmış görünüm (exploded view), kamera yörüngesi, animasyonlu GLB | `tarifler/blender_patlat.py` | Blender (`-b`) |
| Başlıklı kısa intro/outro videosu (mp4) | `tarifler/video_intro.py` | ffmpeg |

Tarif dosyalarını okuma; ayarlar aşağıda. `<S>` = bu skill'in klasörü.

## Akış (tek Bash çağrısı)

- **html:** `python <S>/uyarla.py <tarif.html> <hedef.html> '<ayar json>'` → kopyalar, AYAR'la derin birleştirir (sözlük birleşir, liste yerine geçer), `<title>` = metin.baslik, ölçer, tek satır JSON basar. Yalnız değişen anahtarları ver.
  - giris-scroll: `renk{zemin,murekkep,soluk,yuzey,vurgu}` · `sure` (900ms) · `gecikme` (120ms) · `egri` · `metin{baslik,alt,cta,bolumler:[{baslik,metin}]}` (bölüm sayısı = dizi uzunluğu; ilerleme çubuğu hazır).
  - sayfa-gecisi: `renk{…aynı}` · `sure` · `gecikme` · `egri` · `metin{baslik,alt,geri}` · `kartlar:[{ad,ozet,renk:[a,b],metin}]`.
  - parcacik-three: `sayi` (20000) · `renkA` · `renkB` · `arka` · `hiz` · `cekim` · `boyut` · `metin{baslik,alt,cta}`.
- **Blender:** `"<blender.exe>" -b --factory-startup --python <S>/tarifler/blender_patlat.py -- --cikti <klasör> [--blend <dosya>] [--kare 72 --bosluk 0.06 --fps 24 --render 4 --cozunurluk 384] && python <S>/olc.py <klasör>/telve_anim.glb` (kareler `kare_NNNN.png`)
- **video:** `python <S>/tarifler/video_intro.py --baslik … --alt … --cikti x.mp4 [--sure 4 --en 1280 --boy 720 --fps 30 --renk1 --renk2 --vurgu] && python <S>/olc.py x.mp4`

Kabul (JSON'dan oku): html fps ≥55 (WebGL ≥30), `konsol_hata` 0, `reduced_motion` true, `duzen_animasyonu` false, `hareket` > 0 · mp4 en/boy/fps/süre istenenle aynı, `dolu` true · glb `animasyon` ≥1, `mesh` beklenen sayıda. Geçtiyse BİTTİ — kareye bakma, dosyayı yeniden okuma. Geçmezse yalnız ilgili ayarı değiştirip aynı komutu yeniden koş; ancak o zaman `<hedef>-kare/` PNG'sine bak.

## Kurallar

- Yalnız `transform` ve `opacity` animasyonu; width/height/top/left/margin animasyonu yok (`duzen_animasyonu` yakalar).
- Her harekete `prefers-reduced-motion` karşılığı: hareket kapanır, içerik görünür kalır.
- LCP öğesi (hero başlığı) opacity 0'dan geç başlamaz; giriş ≤600 ms, kademe ≤80 ms.
- Pencere/tarayıcı açma (`start`, `os.startfile`, `webbrowser` yok); Blender yalnız `-b`, ölçüm headless.
- Tarif yetmiyorsa: çok sahneli/veriye bağlı video → Remotion/hyperframes; karmaşık zaman çizelgesi → GSAP (ScrollTrigger/SplitText); 3D sahne kurgusu → Theatre.js. Bunlar ayrı skill'lerde; bu atölye en ucuz yoldur.
