---
name: blender-oturum
description: "Blender, 3D model/varlık/sahne işinde önce yükle: Blender oturumunu (aç · MCP sunucusu · kaydet · kapat) CC yönetir; tools/blender_oturum.py ac/kapat/durum. Yalnız Claude Code'da."
---

# blender-oturum — Blender oturumunu CC yönetir

Araç: `python C:\Projeler\omer-skills\tools\blender_oturum.py <komut>` (her proje klasöründen mutlak yolla).

## Akış (her Blender işinde, sıra değişmez)
1. `ac C:\Users\pc\Desktop\<Proje>\blender\<ad>.blend` — var olan dosya. Yeni dosya: `ac <yol> --yeni` (dosya varsa reddeder, boş sahneyle oluşturur).
2. İş: blender MCP araçları (önce `get_objects_summary` ile sahneyi incele; varsayma).
3. Kaydet: MCP ile `bpy.ops.wm.save_mainfile()` → `bpy.data.is_dirty == False` doğrula. Kirliyse bir kez daha kaydet; ikinci denemede de kirliyse quit GÖNDERME, DUR ve Ömer'e bildir.
4. Kapat isteği (MCP, çağrı dönsün diye gecikmeli):
   `bpy.app.timers.register(lambda: bpy.ops.wm.quit_blender(), first_interval=1)`
5. `kapat` — ≤15 sn içinde port kapalı + PID yok doğrular.

İş yarıda kalsa ya da hata olsa da 3 → 4 → 5 çalıştırılır; sunucu açık bırakılmaz.

## Kurallar
- Blender'ı aynı anda tek oturum sürer; `ac` 9876 doluysa reddeder, başka oturumun Blender'ına dokunma.
- .blend yalnız `<Masaüstü>\<Proje>\blender\` altında (büyük/küçük harf duyarsız).
- Sunucu yalnız 127.0.0.1:9876; eklenti tercihi (Host/Port) ve Auto Start (kapalı) DEĞİŞTİRİLMEZ.
- Süreç yalnız durum dosyasındaki PID ile kapatılır; ad ile öldürme (taskkill /IM, Stop-Process -Name) yasak.
- Kaydetmeden kapatma yok: `kapat` zorla kapatmadan önce dosyanın oturumda kaydedildiğini (mtime) denetler.
- `durum`: port · PID · dosya · süre.

## Çıkış kodları
| kod | anlam |
|---|---|
| 0 | açıldı / kapandı / zaten kapalı / zorla kapatıldı (çıktı yazar) |
| 1 | 30 sn'de 127.0.0.1:9876 yok, 127 dışı dinleme, açılış betiği hatası ya da kaydedilmemiş dosyada zorla kapatma reddi; süreç PID ile kapatıldı |
| 2 | kural ihlali: yol sınırı dışı · --yeni'siz olmayan dosya · --yeni ile var olan dosya · port dolu · Host/Port tercihi 127.0.0.1:9876 değil; hiçbir şey başlatılmadı/açık kalmadı |

1 ya da 2'de işe devam etme; çıktıyı Ömer'e aktar.
