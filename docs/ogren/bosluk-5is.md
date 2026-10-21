# ARAÇ-DENETİM-1 · boşluk taraması (5 iş)

Kaynak: `python tools/katalog_ara.py "<tarif>" --aday 8`, 5 sorgu. Katalog çıktısı kurulu durumunu satır bazında vermiyor (yalnız grup başına "kurulu değil" sayısı); "durum" sütunu Skill/Agent listesinde doğrulanabilenleri gösterir, gerisi "belirsiz". Kurulu olmayanlar yalnız önerildi, kurulmadı.

## 1 · TELVE — ultra-gerçekçi Blender render
| araç | neden | hangi adım | birebir komut | durum |
|---|---|---|---|---|
| blender:blender-uretim | bpy ile obje/ışık/kamera kurulumu | sahne kurma | `Skill: blender:blender-uretim` | belirsiz |
| bl-isik-kurulumu | üç nokta / stüdyo ışığı | ışıklandırma | `Agent bl-isik-kurulumu` | bu oturumda Agent listesinde yok |
| bl-render-ayari | Cycles örnekleme + denoise | render ayarı | `Agent bl-render-ayari` | bu oturumda Agent listesinde yok |

Not: Blender headless (`blender -b`), pencere açılmaz (ekran kuralı).

## 2 · NEFFEX — scroll-3D site
| araç | neden | hangi adım | birebir komut | durum |
|---|---|---|---|---|
| build-threejs-scroll-worlds | scroll'a bağlı WebGL dünyası | 3D sahne | `Skill: build-threejs-scroll-worlds` | belirsiz |
| web-sahne-desenleri | scroll'a bağlı 3D hero/ürün pozu | sahne deseni | `Skill: web-sahne-desenleri` | belirsiz |
| site_kit | Astro + GSAP/Lenis şablonu (repo içi) | iskelet | `python tools/site-kit/...` (yol doğrulanmadı) | repo içi, belirsiz |

## 3 · Logo tasarımı
| araç | neden | hangi adım | birebir komut | durum |
|---|---|---|---|---|
| logo-design:logo-design | brief → SVG → üretim dosyaları | logo üretimi | `Skill: logo-design:logo-design` | belirsiz |
| brand-systems | logo + renk + marka sistemi | marka kimliği | `Skill: brand-systems` | belirsiz |
| logo-design (plugin) | geometrik SVG, optik düzeltme | SVG çizim | plugin; aynı aile, ikinci kaynak | belirsiz |

## 4 · OKTAN — Vercel + güvenlik kapanışı
| araç | neden | hangi adım | birebir komut | durum |
|---|---|---|---|---|
| deploy-to-vercel | Vercel dağıtımı | yayın | `Skill: deploy-to-vercel` | belirsiz |
| slash-dar:security-reviewer | yayın öncesi güvenlik incelemesi | kapanış güvenlik | `Skill: slash-dar:security-reviewer` | kurulu (Skill listesinde) |
| sec-cikis-oncesi-guvenlik | sır, auth, bağımlılık, başlık kontrolü | yayın öncesi liste | `Agent sec-cikis-oncesi-guvenlik` | bu oturumda Agent listesinde yok |

## 5 · Sosyal video
| araç | neden | hangi adım | birebir komut | durum |
|---|---|---|---|---|
| reel-plan | kısa dikey video hook'u + tutma denetimi | senaryo | `Skill: reel-plan` | belirsiz |
| moneyprinter-paket | konudan otomatik kısa video | üretim | `Skill: moneyprinter-paket` | belirsiz |
| vid-sosyal-video-bicim | dikey/kare/geniş uyarlama, güvenli alan | format | `Agent vid-sosyal-video-bicim` | bu oturumda Agent listesinde yok |
