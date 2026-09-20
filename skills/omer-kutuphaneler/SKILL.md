---
name: omer-kutuphaneler
description: "Ömer'in onayladığı frontend kütüphaneleri ve referans projeleri: hangi proje tipinde ne kullanılır, pinli kurulum satırı, lisans ve context7 kimliği. Kütüphane seçerken veya kurarken aç."
---

# Ömer'in kütüphane rafı

Kaynak: KURULUM-6 envanteri (19 Eyl 2026). Sürümler 20 Eyl 2026'daki npm karşılıkları.

**Kural:** bu raftan bir şey kullanılırsa `DESIGN.md` → *Hareket* bölümüne **ad + sürüm + gerekçe** yazılır.
Lisansı olmayanlar yalnız REF'tir: kod kopyalanmaz, fikir/yapı için okunur.

## Kütüphaneler

| kütüphane | ne işe yarar | hangi proje tipinde | pinli kurulum | lisans | context7 |
|---|---|---|---|---|---|
| tempus | requestAnimationFrame döngüsü yöneticisi (öncelik, özel kare hızı) | scroll/animasyon ağırlıklı landing | `npm.cmd i tempus@1.0.0` | MIT | `/darkroomengineering/tempus` |
| lenis | smooth-scroll; WebGL ile senkron | scroll ağırlıklı landing/portfolyo | `npm.cmd i lenis@1.3.26` | MIT | `/darkroomengineering/lenis` |
| swup | çok sayfalı sitede AJAX sayfa geçiş animasyonu | klasik MPA vitrin siteleri | `npm.cmd i swup@4.10.0` | MIT | `/swup/swup` |
| @react-three/a11y | R3F sahnelerine odak/klavye/ekran okuyucu katmanı | erişilebilir Three.js/R3F sahnesi | `npm.cmd i @react-three/a11y@3.0.0` | MIT | `/pmndrs/react-three-a11y` |
| @14islands/r3f-scroll-rig | R3F WebGL'i smooth scroll'a ve DOM öğelerine bağlar | scroll ağırlıklı Three.js landing | `npm.cmd i @14islands/r3f-scroll-rig@8.15.0` | ISC | `/14islands/r3f-scroll-rig` |
| size-limit | JS bundle boyut bütçesi, CI'da aşımda hata | frontend perf bütçesi (Next.js/Vite) | `npm.cmd i -D size-limit@14.0.0` | MIT | context7'de yok |
| @capsizecss/core | font metriğiyle öngörülebilir satır yüksekliği/boşluk | tipografi hassas tasarım sistemleri | `npm.cmd i @capsizecss/core@4.1.3` | MIT | `/seek-oss/capsize` |
| @builder.io/partytown | 3. parti scriptleri web worker'a taşır | analytics/reklam yükü olan perf kritik siteler | `npm.cmd i @builder.io/partytown@0.10.3` | MIT | `/qwikdev/partytown` |
| @number-flow/react | animasyonlu sayı/sayaç bileşeni | istatistik/fiyat sayacı olan arayüzler | `npm.cmd i @number-flow/react@0.6.2` | MIT | `/barvian/number-flow` |

### Paket olarak kurulmayanlar

- **satus** (darkroomengineering) — Next.js 16 + React 19 + Tailwind v4 (+WebGL) başlangıç kiti · *yeni Next.js landing/site*.
  npm'deki `satus` başka bir paket (repo alanı boş) → **pinlenmez**, şablon olarak klonlanır:
  `npx degit darkroomengineering/satus <proje>` · lisans MIT · context7'de yok.
- **utopia-core-scss** (trys) — Utopia akışkan tipografi/spacing SCSS karşılığı · *responsive tipografi ölçeği kuran projeler*.
  Repoda LICENSE dosyası yok (npm metadata ISC diyor) → **kod kopyalanmaz, yalnız REF**:
  https://github.com/trys/utopia-core-scss · context7 `/trys/utopia-core-scss` (okumak serbest).
- **headroom-desktop** (gglucass) — Headroom'un masaüstü tepsi uygulaması · **ücretli abonelik (7 gün deneme), kurulmadı**. Headroom CLI + MCP zaten kurulu, masaüstü katmanı gerekmiyor.

## REF — yalnız okunur, kod kopyalanmaz

claude.ai'de GitHub bağlayıcısıyla açılır; yerelde `.tmp-kurulum6` kopyaları durur.

| REF | ne | yol |
|---|---|---|
| YildizDikme/threejs-fluid-reveal-portfolio | imleçle görsel açan Three.js editoryal portfolyo | `C:/Projeler/.tmp-kurulum6/YildizDikme__threejs-fluid-reveal-portfolio` |
| YildizDikme/3d-camera-landing-page | Next.js + R3F + GSAP 3D kamera landing (README yok) | `C:/Projeler/.tmp-kurulum6/YildizDikme__3d-camera-landing-page` |
| YildizDikme/3D-threejs-spiral-gallery | GLSL + Lenis + GSAP spiral galeri hero'su | `C:/Projeler/.tmp-kurulum6/YildizDikme__3D-threejs-spiral-gallery` |
| gishamer/skill-ui | Agent Skill keşif/kurma/yayınlama masaüstü uygulaması + CLI | lisans yok → REF |
| figma/code-connect | Figma bileşenlerini koda bağlama (MIT) | `C:/Projeler/.tmp-kurulum6/figma__code-connect` |
| gist e20ead11b3df4de46ab32b4a7269abe0 | tek dosyalık örnek (lisans yok) | `C:/Projeler/.tmp-kurulum6/gist__e20ead11b3df4de46ab32b4a7269abe0` |

GitHub adresleri: `https://github.com/<REF adı>` · gist: `https://gist.github.com/e20ead11b3df4de46ab32b4a7269abe0`

## Kullanım sırası

1. İhtiyacı adlandır (scroll, tipografi, perf bütçesi, 3D a11y, sayaç).
2. Tablodan tek kütüphane seç — iki kütüphane aynı işi yapıyorsa projede zaten kurulu olan kazanır.
3. Pinli satırla kur; sürümü `package.json`'da sabit bırak.
4. `DESIGN.md` → Hareket'e ad + sürüm + gerekçe yaz.
5. Ayrıntılı API için context7 kimliğiyle belge çek; kimliği olmayanda repo README'si.
