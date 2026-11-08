---
name: scroll-cinematic
description: "Tek istemden sinematik '3D scroll' sitesi (Apple/Awwwards tarzı): hero görseli + kısa klip(ler) → ~90-180 numaralı kare → canvas görüntü-dizisi scrub + Lenis yumuşak kaydırma + bölüm reveal. Ürün, portfolyo, ajans, restoran, emlak, kişisel marka. Ücretsiz yerel hat: Z-Image görsel, Wan 2.2 TI2V 5B klip, ffmpeg kare. Tetik: 3D scroll, scroll animasyonu, sinematik hero, fly-through, turntable, scroll sitesi. Kaynak zubair-trabzada/scroll-cinematic-claude (lisanssız, iç kullanım) uyarlaması."
---

# scroll-cinematic (SCROLL-CINEMATIC-KUR, 30 Eki 2026)

"3D scroll" Three.js değildir: kısa bir klip numaralı JPG'lere bölünür, hepsi önyüklenir, `<canvas>`'a çizilen kare scroll ilerlemesiyle seçilir. Lenis + scroll'a bağlı yazı = premium 3D hissi. Yığın: düz HTML + CSS + JS + Lenis, derleme yok.

## Hat (orijinaldeki ücretli Higgsfield yerine ücretsiz yerel)
| Adım | Orijinal | Burada |
|---|---|---|
| Hero görsel | Higgsfield nano_banana_pro | `python scripts/yerel_hat.py gorsel --prompt "..." --cikti hero.png` (Z-Image, 1344x768) |
| Klip | Higgsfield seedance 6 sn 1080p | `python scripts/yerel_hat.py klip --gorsel hero.png --hareket "..." --cikti spin.mp4` (Wan 2.2 TI2V 5B, 1024x576, 49 kare ≈3 sn) |
| Kare | extract+compress .sh | `python scripts/yerel_hat.py kare --video spin.mp4 --cikti frames/spin` (ffmpeg, 1600px, q3) |

`gorsel`/`klip` omer-skills deposunu (`OMER_SKILLS` env, varsayılan `C:/Projeler/omer-skills`), ComfyUI'yi ve boş RAM ≥13 GB'ı ister; ComfyUI'yi kendi açıp kapatır. `kare` yalnız ffmpeg ister. claude.ai tarafında yerel hat yoktur: klibi kullanıcı verir ya da `ucretsiz-web-ai` skill'i (Wan i2v) üretir; `kare` + şablonlar aynen çalışır.

## Akış
1. **Brief**: site türü, hero öznesi, palet, marka adı, 2 hareket (ürün → 360° + reveal; portfolyo → soyut morf + parallax; restoran → tabak orbit + buhar; emlak → fly-through + detay). Emin değilsen: 1 orbit/fly-through + 1 reveal.
2. **Görsel** (`gorsel`): öznesi net, güçlü ışık, bilinçli arka plan, "ultra sharp, photorealistic, editorial". UI işiyse `frontend-craft` önce yüklenir.
3. **Klip** (`klip`): hareket kalıpları — turntable "smooth seamless full 360-degree rotation, stays centered"; fly-through "slow continuous forward camera flight, smooth dolly, deep parallax"; reveal "elements burst outward and float in slow motion"; soyut "slow-morphing liquid-metal form drifting". Sert kesim yok (geri scrub'da çirkin). Klip başına ~10 dk; art arda koş, paralel değil.
4. **Kare** (`kare`): çıktı kare sayısı kaynak fps ile sınırlıdır (Wan 3 sn ≈ 49-90 kare); `frameCount` betiğin yazdığı sayı. Klip uzunluğunu `--uzunluk` ile artır (Wan 2.2 5B ≤ ~121 kare).
5. **Site**: `templates/index.html, styles.css, scroll-cinematic.js` kopyala; `SCRUB_SECTIONS` girişleri: `{ section:"#hero", frameCount:N, bg:"#0a0a12", framePath:(i)=>`frames/spin/frame_${String(i).padStart(4,"0")}.jpg` }`. Marka metni + palet (CSS değişkenleri), bölümler, CTA yaz. Renk varyantı: `ffmpeg -i base.png -vf "hue=h=120:s=1.15" v.png`.
6. **Sun ve doğrula**: `python -m http.server <port>` (Windows'ta .command yok); sayfa + bir kare 200 dönsün; playwright headless ile scroll edip canvas piksel örneklemesi (başsız ekran görüntüsü sticky-canvas'ı boş gösterebilir). Pencere/varsayılan tarayıcı açma.

## Motor kuralları (şablonda hazır)
Tüm kareleri önyükle, kare 0'ı hemen çiz, yalnız indeks değişince yeniden çiz. Sticky sahne: dış bölüm `height: 420–600vh`, iç `position:sticky; top:0; height:100vh`; ilerleme `clamp(-rect.top/(rect.height-innerH),0,1)`. Cover-fit + HiDPI (dpr ≤2), Lenis rAF döngüsünden sür. Eksik elemanlı bölümler atlanır.

## Sınırlar (ücretsiz hat)
Wan 5B: 1024x576, ~3 sn klip, el/yüz/metin kararsız; Higgsfield 6 sn 1080p kadar akıcı değil (kare az → scrub daha adımlı; kısa bölüm yüksekliği ve kenar yumuşatma ile telafi). VRAM <3 GB boş bekler; RAM <13 GB boşsa klip koşmaz. Çok kare = yavaş yükleme: 1600px/q3 ve ≤~180 kare.

Lisans: kaynak repoda LICENSE yok → yalnız iç kullanım; yeniden dağıtma.
