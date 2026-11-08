# TANE-PREMIUM-VARLIK raporu (30 Eki)

Kaynak: yerel ComfyUI Z-Image (`tools/gorsel_uret.py --is foto`), TRELLIS.2 (C:\AI\ComfyUI-T2, port 8190), `tools/glb_hat.py --doku 1024`. Para harcanmadı. Puanlar sert, İLİK ölçeğiyle.

## Görseller (img/, 1600x1000 jpg q82, hepsi ≤350 KB; Read ile bakıldı)
| dosya | KB | tohum | puan | not |
|---|---|---|---|---|
| koken.jpg | 223 | 11 | 70 | sisli teras, iyi; hafif düz renk |
| kiraz.jpg | 140 | 11 | 78 | çiy damlalı kiraz, temiz |
| kavrum.jpg | 199 | 11 | 72 | duman/fıçı iyi; arka plan krem, "karanlık atölye" değil |
| ogutum.jpg | 184 | 22 | 70 | ilk tohum (11) pirinç kapta yazı benzeri kabartma vardı → mat çelik kase + tohum 22 |
| v60.jpg | 110 | 11 | 62 | su spirali yok, sahne sönük |
| moka.jpg | 95 | 22 | 72 | tohum 11 moka değil ibrikti → istem sertleştirildi, tohum 22 |
| cezve.jpg | 210 | 11 | 76 | kumda cezve + kor, en güçlü |
| press.jpg | 140 | 11 | 70 | temiz |
| fincan.jpg | 141 | 11 | 66 | pencere kenarı hafif patlak, kaplama güzel |

## 3D referans (ref/, 1024x1024 png, beyaz zemin): cekirdek, degirmen, fincan, paket (tohum 11)
Bakıldı: çekirdek 80, değirmen 80, fincan 75, paket 70 (kalay bağı yok). TRELLIS girdisi RGBA olmalı (RGB `IndexError` verdi); `gorsel_uret.py arkaplan` (rembg) ile arka plan kaldırıldı.

## 3D (models/, meshopt + webp, glb_hat doğrulaması hata 0 / uyarı 0)
| dosya | MB | üçgen | süre / VRAM tepe | durum |
|---|---|---|---|---|
| cekirdek.glb | 2,4 | ~324k | 811 sn / 11295 MiB | üretildi |
| degirmen.glb | 1,8 | — | 684 sn / 8708 MiB | üretildi |
| fincan.glb | 1,4 | — | 783 sn / 8502 MiB | üretildi |
| paket.glb | — | — | — | YOK: doku aşamasında sunucu iki kez çöktü (2. deneme RAM %91'de). Yalnız dokusuz `C:\AI\ComfyUI-T2\output\t2_tane_paket_WhiteMesh_00001_.glb` (8,6 MB) var, kullanıma uygun değil |

## Açık noktalar (dürüst)
- GLB'lere görsel bakılmadı: RAM %91 olduğu için (kural ≥%89 yeni süreç yok) Blender render koşulmadı. Kalite puanı verilemedi; üçgen/doku/boyut ölçüldü, görünüm ölçülmedi. Render betiği: `C:\AI\_t2\render_glb.py` (Blender 5.2 `-b`).
- cekirdek koşusunun VRAM tepesi 11295 MiB, tavan 9826 MiB'ı aştı (diğer ikisi altında). Aşım nedeni ölçülmedi.
- GLB'ler `EXT_meshopt_compression`, `EXT_texture_webp`, `KHR_mesh_quantization` kullanıyor; three.js r128 GLTFLoader bunları çözmez (MeshoptDecoder + webp desteği gerekir). Siteyi kuran taraf r128 ile açacaksa sıkıştırmasız/PNG sürüm gerekir (üretilmedi).
- Ham dokulu GLB'ler (19–24 MB) C:\AI\ComfyUI-T2\output\ ve Desktop\tane-uretim\glb\*_raw.glb içinde.
- 2. beyne (Obsidian) özet yazılmadı (tur bütçesi bitti).
