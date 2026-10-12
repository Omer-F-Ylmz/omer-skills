# Malzeme tarifleri — Blender 5.2.1

Kod: `malzemeler.py` — `kur(ad)` → `MAT-<Ad>`, Principled tabanlı, kendi kodumuz. Tüm sayısal değerler **öneri**; referans görsel/brief gelince değiştir.
Kurmadan önce canlı soket sorgusu (`[i.name for i in node.inputs]`); `isik_kur.soket()` tutmayan adda mevcut adları listeler → hata metniyle `search_api_docs` (#12: "Specular" → "Specular IOR Level"; 5.2'de doku `Fac` → `Factor`).

| tarif | özü | kaynak |
|---|---|---|
| seramik_sirli | açık krem, Roughness 0.25, Coat 1 / Coat Roughness 0.03 (sır), IOR 1.5 | öneri (Q5 küme) |
| seramik_mat | Roughness 0.65, Specular IOR Level 0.35, ince Noise kabartma | öneri (Q5 küme) |
| bakir | cezve; Metallic 1, Roughness 0.28, Voronoi dövme kabartması | öneri (Q5 küme) |
| pirinc | Metallic 1, Roughness 0.32 | öneri (Q5 küme) |
| cam | Transmission Weight 1, Roughness 0, IOR 1.5 | öneri (Q5 küme) |
| ahsap_koyu | Wave (Distortion 6) → ColorRamp iki koyu kahve → Base Color, Roughness 0.45 | öneri (Q5 küme) |
| kahve_sivi | çok koyu, Roughness 0.05, IOR 1.33 | öneri (Q5 küme) |
| kahve_kopuk | karamel, Subsurface 0.3 (ölçek 2 mm), küçük Voronoi kabarcık | öneri (Q5 küme) |
| cekirdek | kavrulmuş; Noise → ColorRamp, Coat 0.3 (yağlı parlama) | öneri |

Gerçekçilik gerekirse Poly Haven CC0 doku → Principled prosedürelden ucuz (#6): `tools/varlik_indir.py`.

## Dış malzeme okuma (NodeToPython)
- Yalnız başkasının kurduğu malzemeyi **okumak** için (#19). Canlı oturumda: `scene.ntp_material_slots` + `bpy.ops.ntp.export()` (SCRIPT → clipboard; headless boş döner).
- Çıktı repo dışına: `C:\AI\blender-tarif\<ad>.py`; başına Blender sürümü yazılır. GPL-3.0 eklenti; üretilen betik repoya girmez, buradaki tarifler kendi kodumuzdur.
- Okunan tarifi boş sahnede `blender_cli` ile koştur, sonra gerekeni kendi tarifine aktar.
