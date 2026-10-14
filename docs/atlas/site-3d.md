# Oyun kitabı — site + 3D + Blender (ATLAS-1 d1)

Karar kaynağı: `docs/atlas/kart.jsonl` (`karar` · `kosul` · `asama` · `nasil`); aynı karar `docs/katalog/yetenek.jsonl` satırında. VARSAYILAN = her uygun işte; GEREKİNCE = koşulu kartta; KULLANMA = kurulu kalır, seçilmez.

## 0. Her işte ilk adım (KATALOG-ÖNCE)
1. Eşleşen departman-* dizini (site → `departman-frontend`, 3D varlık → `blender-uretim`) + bu kitap.
2. Eksik kalan için `python tools/katalog_ara.py "<sorgu>"` (≤3 sorgu, ≤40 satır); 2+ alan ise `plan-kur`.
3. Hazırı al (skill tarifi, hazır bileşen, hazır varlık) → üzerine premium değişiklik. Yalnız ilgili SKILL.md bölümü açılır.

## A. TELVE benzeri site (scroll anlatı + 3D nesne + ses)
| Adım | Araç (VARSAYILAN) | Komut / kaynak | Kapı |
|---|---|---|---|
| A1 Referans-önce | `playwright` MCP (headless) | 2–3 referans: ekran görüntüsü 390/768/1440 + `browser_evaluate` ile `tools/site-inceleme/olc.js` (kütüphane, font, renk, ızgara, geçiş) | Önce `docs/site-inceleme/` (50 inceleme) içinde var mı bak; sayılar önce |
| A2 Çıkarım | `design-extractor` (URL → sayılar) · `design-dna` (ekran görüntüsünden kimlik) | Mekanizma tablosu `tools/site-inceleme/SABLON.md` biçimi: ne görünüyor → nasıl yapılmış → bizde nasıl | Kaynak kod/varlık kopyası yok |
| A3 Birleştir | `frontend-craft` (REF modu) | 2–3 referansın iyi yanı + özgün fikir → `DESIGN.md` | DESIGN.md olmadan kod yok |
| A4 Yapım | `frontend-craft` iki-pass · `web-sahne-desenleri` · `animasyon-atolyesi` | Hareket: `gsap-skills:gsap-core` + `gsap-skills:gsap-scrolltrigger` (+ Lenis) | Kütüphane önce `omer-kutuphaneler` |
| A5 3D sahne | `threejs-skill-router` | Uzman `threejs-*` / `3d-*` skill'ini router seçer; model → B | GLB ~2 MB (6 MB yalnız gerekçeyle) |
| A6 Doğrulama | `playwright-cli` · `@playwright/cli` · `threejs-visual-validation` · `fixing-motion-performance` · `inclusive-interaction:motion-sensitivity` | Screenshot → sapma tablosu → düzelt; ölçü betiği (TELVE: `r2b` kapısı, p95 kare süresi, ilk JS gz, konsol hata 0) | En fazla 4 tur; `prefers-reduced-motion` karşılığı zorunlu |
| A7 Ses / medya | — | CC0 kaynak (sayfasından lisans teyidi), kolofona atıf, ilk istek 0 (kullanıcı eylemiyle iner) | Lisans satırı raporda |

GEREKİNCE (koşul):
- `impeccable` — frontend-craft turundan sonra denetim/cila; çakışmada frontend-craft kazanır.
- `ui-ux-pro-max` — palet/font/stil verisi; çakışmada frontend-craft ve impeccable kazanır.
- `taste-skill:*`, `tastemaker` — stil yönü seçimi; aynı sıralamayla düşer.
- `21st:21st-ui` — hazır bileşen (katalog-önce).
- `taste-skill:image-to-code` — referans ekran görüntüsünden bölüm iskeleti; sonra özgünleştir.
- `ecc:taste` — design-dna yetmezse (aynı iş).
- `threejs` — temel sahne/GLTF; `webgpu-threejs-tsl` — yalnız WebGPU/TSL hedefi.
- `gsap-skills:gsap-timeline|plugins|react|performance|utils|frameworks` — o konu gerekince.
- `universal-modder:fal-assets`, `scroll-craft` (kie.ai) — ücretli API; tarifte sayısal tavan + Ömer onayı.
- `remotion-*`, `hyperframes:*`, `motion-os`, `motion-studio`, `ecc:taste-*` — video/hareketli grafik işi (site değil).
- Oyun skill'leri (`build-*game*`, `*-vfx`, `optimize-threejs-games`) — oyun/efekt işi.

KULLANMA (neden):
- `gsap` (tek skill) — gsap-skills resmi seti kapsıyor.
- `taste-skill:design-taste-frontend-v1` — eski sürüm.
- `landing-report`, `gstack-landing-report` — gstack sürüm kuyruğu, site işi değil.
- `build-vesperfall-review-assets` — Vesperfall projesine özgü.
- `*-paket`, `ig41-ucuncu-taraf` — CC'de üye skill doğrudan seçilir; paket yalnız claude.ai'de (kartta GEREKİNCE: "yalnız claude.ai").

## B. Blender varlık (hazır varlık merdiveni)
| Adım | Araç (VARSAYILAN) | Komut | Kapı |
|---|---|---|---|
| B0 Oturum | `blender:blender-uretim` · `blender:blender-oturum` · `blender` MCP | `python tools/blender_oturum.py ac\|durum\|kapat`; GPU işi öncesi `python tools/gpu_kilit.py al <is> --pid N` | Yalnız CC; GUI yok, `-b` |
| B1 Merdiven | `varlik_getir` · `varlik_indir` | (1) yerel (2) Objaverse: `python skills/blender-uretim/varlik_getir.py ara "<sorgu>"` → `indir objaverse <uid> <dizin>` (3) Poly Haven/ambientCG: `python tools/varlik_indir.py ara polyhaven hdri\|doku\|model` (4) Sketchfab API yalnız Ömer'in token'ı ortamdaysa (5) görüntü→3D HF Spaces (kalite kapısı) (6) en son sade bpy | `atif.json` lisans + yazar; CC-BY → kolofon |
| B2 Küçük düzenleme | `blender_cli` · `bpy_kontrol` · `blender_bekci` (hook) | `python tools/bpy_kontrol.py <betik.py>` → `python tools/blender_cli.py <betik.py> [@spec.json] --blend <x.blend>` | Olmayan bpy özniteliği 0 |
| B3 Malzeme / ışık | GEREKİNCE: `bl-malzeme-kurucu`, `bl-isik-kurulumu`, `bl-uv-acma`, `bl-dokuya-pisirme` | Pişirme: `python tools/blender_pisir.py <x.blend> --mod isik\|ao --boyut 1024` | Doku: ambientCG/Poly Haven CC0 |
| B4 Doğrulama | `blender_dogrula` · `blender_gorunum` · `bl-gorsel-ani-kontrol` | `python tools/blender_dogrula.py <x.blend> --beklenen "ad=GxDxY" --butce-ucgen N` → `python tools/blender_gorunum.py <x.blend> --referans on.png` | Sayısal kapı önce, görünüm sonra (4 Workbench + 1 Eevee) |
| B5 Teslim | `bl-glb-disa-aktar` · `glb_hat` · `@gltf-transform/cli` | `python tools/glb_hat.py <gir.glb> --doku 2048` (meshopt + webp → validate → inspect) | validate 0 hata; önce/sonra KB raporda |

Örnek: TELVE-R2d cezve — Objaverse uid 3b5bb5d4 (CC BY 4.0) → 3 parça birleşti, decimate → 2496 üçgen, ambientCG Metal057A → `glb_hat` 4567 → 56.9 KB, validate 0 hata.

## Yasaklar
- Sıfırdan modelleme (merdiven 6. basamaktan önce).
- Referans sitenin birebir klonu, görsel/font/3D/video varlığının izinsiz kullanımı.
- Varsayılan tarayıcıyı açmak (`start <url>`, `webbrowser.open`); yalnız Playwright headless ya da Chrome.
- Blender GUI; yalnız `-b`.
- Tavansız ücretli API çağrısı.
- 4 screenshot turunu aşmak; DESIGN.md olmadan kod.

## Token notu
Kartların 191/207'sinde token etkisi "bilinmiyor" (kaynak metin söylemiyor). Bu kitabın etkisi TELVE-R2e'de ölçülür: keşif turu (katalog/SKILL.md açma) ve toplam ağırlıklı token, R2d ile karşılaştırılır.

## C. K7 kiti eksik modülleri (SİTE-OKULU-1 kurulum tarifi; TELVE'ye uygulama R3b)
Kit: `python tools/site_kit.py <ad>` → `tools/site-kit/sablon`. Eksik modüller (öncelik `docs/site-okulu/eksikler.md`):
- `npm i postprocessing@^6 detect-gpu@^5` · `npm i -D @gltf-transform/cli` · GSAP SplitText zaten gsap 3.15 paketinde (`gsap/SplitText`).
- package.json betiği: `"varlik:optimize": "gltf-transform optimize public/ham.glb public/sahne.glb --texture-compress ktx2 --compress meshopt"`.
- İskelet dosyalar `src/sahne/`: `post.ts` (EffectComposer+EffectPass) · `kamera-yolu.ts` (CatmullRomCurve3 + ST scrub) · `metin.ts` (SplitText) · `dongu.ts` (IntersectionObserver → setAnimationLoop) · `yukleyici.ts` (LoadingManager.onProgress) · `gecis.ts` (2 RT + mask) · `kademe.ts` (detect-gpu → DPR/post).
- Lisans: postprocessing Zlib, detect-gpu MIT, gltf-transform MIT, KTX-Software Apache-2.0, GSAP Standard License.
