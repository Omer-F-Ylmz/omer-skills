---
name: animasyon-atolyesi
description: Hazır, ölçülmüş animasyon tarifleri — web giriş/scroll, sayfa geçişi, Three.js parçacık, Blender patlatılmış görünüm + GLB, ffmpeg intro videosu, hazır aday ↔ bizimki yan yana çekim+ölçü; sıfırdan yazmak yerine kopyala-uyarla, headless ölç.
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
| Hazır aday (kod/varlık/HDR) bizimkiyle yan yana çek + ölç → AL/UYARLA kararı | `tarifler/yan_yana.mjs` | playwright-core, sharp, Chrome |

Tarif dosyalarını okuma; ayarlar aşağıda. `<S>` = bu skill'in klasörü.

## Akış (tek Bash çağrısı)

- **html:** `python <S>/uyarla.py <tarif.html> <hedef.html> '<ayar json>'` → kopyalar, AYAR'la derin birleştirir (sözlük birleşir, liste yerine geçer), `<title>` = metin.baslik, ölçer, tek satır JSON basar. Yalnız değişen anahtarları ver.
  - giris-scroll: `renk{zemin,murekkep,soluk,yuzey,vurgu}` · `sure` (900ms) · `gecikme` (120ms) · `egri` · `metin{baslik,alt,cta,bolumler:[{baslik,metin}]}` (bölüm sayısı = dizi uzunluğu; ilerleme çubuğu hazır).
  - sayfa-gecisi: `renk{…aynı}` · `sure` · `gecikme` · `egri` · `metin{baslik,alt,geri}` · `kartlar:[{ad,ozet,renk:[a,b],metin}]`.
  - parcacik-three: `sayi` (20000) · `renkA` · `renkB` · `arka` · `hiz` · `cekim` · `boyut` · `metin{baslik,alt,cta}`.
- **Blender:** `"<blender.exe>" -b --factory-startup --python <S>/tarifler/blender_patlat.py -- --cikti <klasör> [--blend <dosya>] [--kare 72 --bosluk 0.06 --fps 24 --render 4 --cozunurluk 384] && python <S>/olc.py <klasör>/telve_anim.glb` (kareler `kare_NNNN.png`)
- **video:** `python <S>/tarifler/video_intro.py --baslik … --alt … --cikti x.mp4 [--sure 4 --en 1280 --boy 720 --fps 30 --renk1 --renk2 --vurgu] && python <S>/olc.py x.mp4`

Kabul (JSON'dan oku): html fps ≥55 (WebGL ≥30), `konsol_hata` 0, `reduced_motion` true, `duzen_animasyonu` false, `hareket` > 0 · mp4 en/boy/fps/süre istenenle aynı, `dolu` true · glb `animasyon` ≥1, `mesh` beklenen sayıda. Geçtiyse BİTTİ — kareye bakma, dosyayı yeniden okuma. Geçmezse yalnız ilgili ayarı değiştirip aynı komutu yeniden koş; ancak o zaman `<hedef>-kare/` PNG'sine bak.

## Hazır-önce yan yana deneme (TELVE-HAZIR-1)

Mekanizma: hazır adayı (MIT/CC0 kod ya da varlık) bizimkiyle aynı kamera/ışıkta iki sayfaya koy, tek komutla aynı karede çek + ölç; karar kareden ve sayıdan çıkar, tahminden değil.
- Komut: önce `cp <S>/tarifler/yan_yana.mjs <k>/` — `<k>` = `node_modules/playwright-core`'u gören klasör ya da altı (ESM bağımlılığı betiğin klasöründen çözer, cwd'den değil; TELVE'de `docs/r1/_ham/`), sonra `MSYS_NO_PATHCONV=1 node <k>/yan_yana.mjs <ad> <bizim-yol> <hazir-yol> [kare] [cikti] [kok]` (yerel sunucu 8765 açık; proje kökünde playwright-core + sharp). Git Bash'te `MSYS_NO_PATHCONV=1` yoksa `/docs/...` Windows yoluna çevrilir, sayfa 404 verir.
- Sözleşme: iki sayfa da `window.__hazir = true` ya da `window.__T = {hazir, adim(dt,n), olc(ms)}` verir; yoksa 30 sn zaman aşımı. Sahne kurulumunu (kamera, ışık, fon, HDR) bizim sayfadan TEK ortak modüle kopyala, yalnız denenen parça değişsin — yoksa fark ışıktan gelir.
- Okuma: p95 kare süresi ekran tazelemesinde doyar (240 Hz → 4.2–4.3 ms); ikisi de doymuşsa performans farkı yok sayılır, `?q=` düşük ayarla ayrıca ölç. Artık artışı ayrıntı da olabilir gürültü de → kareye bir kez bak.
- İndirilen kod `<proje>/.../indirilen/<ad>/` (commit dışı) klasörüne; çalıştırmadan önce `grep -nE "fetch|XMLHttpRequest|eval\(|new Function|http|localStorage|ga\("`. Hazır betiği DEĞİŞTİRME; ayrı klasik betikle taslak (`ga`, `dat` → kendini döndüren Proxy, eksik DOM düğümü) + ayar ver: üst düzey `let`/`function` başka klasik betikten görünür.
- Tuzak (ölçüldü): ham WebGL demolarında `render()` GL_BLEND'i açık bırakır → dışarıdan yapılan sıfırlama blit'i etkisiz kalır; önce `gl.disable(gl.BLEND)`. Açılışta rastgele splat/parçacık basan demoları ilk rAF'ta temizle (betik içi ilk `update()` eşzamanlıdır).
- Lisans kapısı denemeden önce: MIT/Apache/BSD/ISC/Zlib/CC0 → al; README'de MIT ama LICENSE yok → dosyaya MIT notu + yazar; CC-BY → atıf listesi; NC/lisanssız/Shadertoy → yalnız mekanizma, kod yok.
- Karar sözlüğü: AL (olduğu gibi) · UYARLA (hareket/çekirdek hazırdan, görünüm bizden) · MEKANİZMA (fikir, kod yok) · ATLA. Bir adayda en fazla 3 ayar turu; üçüncüde de kötüyse MEKANİZMA yaz, ayar kovalama.

## Kurallar

- Yalnız `transform` ve `opacity` animasyonu; width/height/top/left/margin animasyonu yok (`duzen_animasyonu` yakalar).
- Her harekete `prefers-reduced-motion` karşılığı: hareket kapanır, içerik görünür kalır.
- LCP öğesi (hero başlığı) opacity 0'dan geç başlamaz; giriş ≤600 ms, kademe ≤80 ms.
- Pencere/tarayıcı açma (`start`, `os.startfile`, `webbrowser` yok); Blender yalnız `-b`, ölçüm headless.
- Tarif yetmiyorsa: çok sahneli/veriye bağlı video → Remotion/hyperframes; karmaşık zaman çizelgesi → GSAP (ScrollTrigger/SplitText); 3D sahne kurgusu → Theatre.js. Bunlar ayrı skill'lerde; bu atölye en ucuz yoldur.
