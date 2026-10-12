# Işık profilleri (Blender 5.2.1)

Kod: `isik_kur.py` — `kur(profil, boyut_m, merkez, etiket=None, hdri=None)` üç noktayı + profil eklerini kurar.
`kaynak`: #no = docs/kaynak-tarama/7-blender.md · video id = docs/video-tarama/2026-10-01-toplu.md · öneri = kaynaksız varsayılan.

## Profiller (anahtar:dolgu:kenar güç oranı)

| profil | oran | sıcaklık | HDRI dolgu | ek | kaynak |
|---|---|---|---|---|---|
| urun | 5:1:1.5 | 5000K | 0.3 | — | #1 |
| cam | 3:1:1.2 | — | 0.3 | gradyan düzlem | #1 (oran) · Q2, ZYk3OOf-gBk (gradyan) |
| ahsap | 4:1:1.5 | 3000K | 0.3 | — | #1 |
| kumas | 3:1:0.5 | — | 0.3 | — | #1 |
| metal | 5:1:1.5 | 5000K | 0.1 | iki uzun şerit | öneri (oran, 0.1) · ZYk3OOf-gBk (uzun alan, az HDRI) |
| seramik_sirli | 5:1:1.5 | 5000K | 0.3 | iki dikey şerit softbox | öneri (Q2: kaynakta yok) |
| seramik_mat | 5:1:1 | 5000K | 0.3 | — | öneri (Q2: kaynakta yok) |

## Yerleşim

| değer | kural | kaynak |
|---|---|---|
| uzaklık | max(boyut × 1.5, 1 m) | #1 |
| profil belirsiz | 3 nokta + HDRI dolgu 0.3 | #1 |
| anahtar | kamera ekseninden 40°, 30° yukarı; geniş yumuşak area | öneri (EK zayıf: 30-45°) |
| güç | 1 m'de anahtar 300 W, uzaklığın karesiyle; `ANAHTAR_W` kalibrasyon düğmesi | öneri (video ~3000 W daha büyük sahne: wySOWP-MevI) |
| alan ışığı boyu | max(boyut × 2, 0.3 m), ürüne yakın | wySOWP-MevI · 4Uy2SzB-Kuk |
| world | yeni WLD-Dolgu; mevcut world ezilmez | Q2 (#6) |
| HDRI | Poly Haven stüdyo 1k-2k, `varlik_indir.py`; yalnız yansıma için | #6 |

## Malzemeye göre

| malzeme | kural | kaynak |
|---|---|---|
| metal / cam | önce neyin yansıdığını kur: kameraya görünmez geniş softbox/gradyan düzlem; kenar ışığı yansımayı şekillendirir; test mat gri + krom küre | Q2 |
| metal | uzun alan ışıkları, HDRI az | ZYk3OOf-gBk |
| sırlı seramik | ürün profili + iki dikey şerit softbox (uzun vurgu çizgisi) | öneri |
| mat seramik / plastik | ürün profili, kenar 1 | öneri |

## Video teknikleri (yalnız UYGULA, tekrarlar birleşik)

| teknik | isik_kur | video |
|---|---|---|
| Üç nokta aydınlatma | `kur()` | ZYk3OOf-gBk · 4Uy2SzB-Kuk |
| Görünmez dolgu düzlemi (Visibility > Camera kapalı) | `gorunmez_dolgu()` | ZYk3OOf-gBk |
| Işıksız duvarla sekme dolgusu; duvar tonunu kısma | `sekme_duvari(ton=)` | wySOWP-MevI · 4Uy2SzB-Kuk |
| Light Linking ile zemini ışıktan ayırma | `zemini_ayir(isik, zemin)` | ZYk3OOf-gBk |
| Kıvrımlı beyaz zemin / backdrop; büyük + küçük ışık | `kivrimli_zemin()` + `kur()` | ZYk3OOf-gBk · wySOWP-MevI |
| Gradyan dokulu alan ışığı (cam/metal) | `gradyan_duzlem()` | ZYk3OOf-gBk · 4Uy2SzB-Kuk |
| Gobo; renkli gobo | `gobo(doku=, renk=)` | ZYk3OOf-gBk · wySOWP-MevI |
| Teaser: yalnız arka ışıklar | `teaser()` | ZYk3OOf-gBk |
| Bevel shader + modifier | `bevel(o, mat=)` | ZYk3OOf-gBk |
| Alan derinliği | `dof(kamera, hedef)` | 4Uy2SzB-Kuk |
| Ölçülü compositing: Lens Distortion + vinyet + sensör gürültüsü | `compositing()` | wySOWP-MevI |
| Cycles + OptiX denoise (yoksa OIDN) | `cycles_denoise()` | 4Uy2SzB-Kuk |
| Anahtarı etikete hedefleme | `kur(etiket=)` | wySOWP-MevI |
| Işık exposure ile ince ayar | elle: `Light.exposure` | wySOWP-MevI |
| Sun ışığıyla sert gölge, açıyla yumuşatma | elle: SUN + `angle` | ZYk3OOf-gBk |
| Spot + düzlemle arka plan gradyanı | elle | 4Uy2SzB-Kuk |

Girmeyen: BEKLE adaylar (120 mm odak · world 0 ile arka ışıktan başlama · rendered view kontrolü · saf siyah world) ve ışık dışı UYGULA'lar (3D imleç pivot · Patreon sahnesi · ChatGPT ile ışık).

## 5.2 notları (canlı sorgu 2026-10-01)
- Doku düğümü çıkışı ve ColorRamp girişi `Factor` (eski `Fac`); Mix (ShaderNodeMix) compositor'da da kullanılır, `A`/`B`/`Result`.
- Compositing `scene.compositing_node_group` + `NodeGroupOutput`; EllipseMask/Blur `Size` soket.
- Işık: `use_temperature` + `temperature`; nesne `visible_camera`; light linking `obj.light_linking.receiver_collection`.
