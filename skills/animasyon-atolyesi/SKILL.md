---
name: animasyon-atolyesi
description: Hazır, ölçülmüş animasyon tarifleri — web giriş/scroll, sayfa geçişi, Three.js parçacık, Blender patlatılmış görünüm + GLB, ffmpeg intro videosu; sıfırdan yazmak yerine kopyala-uyarla, headless ölç.
---

# Animasyon atölyesi

Animasyon/efekt işinde önce buradaki tarifi kopyala, yalnız AYAR bloğunu/argümanları değiştir, sonra `olc.py` ile ölç. Sıfırdan yazmak hem daha çok jeton hem daha çok hata demek; tarifler 60 fps, `prefers-reduced-motion` ve pencere açmama kurallarını zaten taşır.

## Tarif seçimi

| İstek | Tarif | Bağımlılık |
|---|---|---|
| Hero kademeli giriş, scroll'la belirme, ilerleme çubuğu | `tarifler/giris-scroll.html` | yok |
| Liste ↔ detay, paylaşılan öğe morfu, sayfa geçişi | `tarifler/sayfa-gecisi.html` (View Transitions) | yok |
| WebGL hero arka planı, parçacık/buhar/toz, fare etkileşimi | `tarifler/parcacik-three.html` | three (CDN importmap) |
| 3D patlatılmış görünüm (exploded view), kamera yörüngesi, animasyonlu GLB | `tarifler/blender_patlat.py` | Blender (`-b`) |
| Başlıklı kısa intro/outro videosu (mp4) | `tarifler/video_intro.py` | ffmpeg |

Her tarifin başında "Nasıl uyarlanır" notu var — önce onu oku (yalnız baş yorum, ~15 satır), gövdeyi okumana gerek yok.

## Akış

1. Tarifi hedefe kopyala (`cp tarifler/<tarif> <hedef>`), dosya adını görev neyse ona çevir.
2. Yalnız AYAR bloğunu (html) ya da CLI argümanlarını (py) değiştir: metin, renk, süre, eğri, sayı. Gövdeye dokunma; gerekmedikçe yeniden yazma.
3. Üret: Blender `"<blender.exe>" -b --factory-startup --python blender_patlat.py -- --cikti <klasör> [--blend <dosya>] [--render 4]` · video `python video_intro.py --baslik ... --alt ... --cikti x.mp4 [--sure 4 --en 1280 --boy 720 --fps 30]`.
4. Ölç: `python olc.py <dosya> --kare <klasör>` → tek satır JSON. Kabul: html fps ≥55 (WebGL ≥30), `konsol_hata` 0, `reduced_motion` true, `duzen_animasyonu` false, `hareket` > 0 · mp4 en/boy/fps/süre istenenle aynı, `dolu` true · glb `animasyon` ≥1, `mesh` beklenen sayıda.
5. Kareye bak (`--kare` klasöründeki PNG); sorun yoksa bitti. Ölçüm geçmezse yalnız ilgili AYAR değerini düzelt, yeniden ölç.

## Kurallar

- Yalnız `transform` ve `opacity` animasyonu; width/height/top/left/margin animasyonu yok (`duzen_animasyonu` yakalar).
- Her harekete `prefers-reduced-motion` karşılığı: hareket kapanır, içerik görünür kalır.
- LCP öğesi (hero başlığı) opacity 0'dan geç başlamaz; giriş ≤600 ms, kademe ≤80 ms.
- Pencere/tarayıcı açma (`start`, `os.startfile`, `webbrowser` yok); Blender yalnız `-b`, ölçüm headless.
- Tarif yetmiyorsa: çok sahneli/veriye bağlı video → Remotion/hyperframes; karmaşık zaman çizelgesi → GSAP (ScrollTrigger/SplitText); 3D sahne kurgusu → Theatre.js. Bunlar ayrı skill'lerde; bu atölye en ucuz yoldur.
