# Blender 3D varlık — birleşim tarifi
Ne zaman: Blender'da ürün modeli, malzeme, render ya da web için GLB üretimi.

## Fazlar
1. Oturum: `blender:blender-oturum` — Blender oturumunu (aç, MCP sunucusu, kaydet, kapat) CC yönetir; yalnız Claude Code'da · birlikte: `blender` (MCP) çalışan Blender'ı uzaktan yönetir.
2. Brief ve plan: `blender:blender-uretim` — brief, ölçüler, kod olarak sahne, render kontrolleri hattı.
3. Modelleme: `bl-python-betik` — headless bpy ile toplu içe aktarma, değiştirme, render, dışa aktarma · birlikte: `blender` (MCP) sahneyi canlı düzenler.
4. Render: `bl-render-ayari` — Cycles/Eevee, örnek sayısı, gürültü azaltma · birlikte: ürün dönüşü için `bl-urun-turntable`; hareket için `bl-animasyon-anahtar`.
5. Dışa aktarma: `bl-glb-disa-aktar` — three.js ve web için küçük GLB hazırlar.
6. Doğrulama: katalogda kurulu özel doğrulama kapısı yok — genel: `blender:blender-uretim` render kontrolleri; `blender` (MCP) doğrulama kapısı değildir.
7. Kapanış: `superpowers:verification-before-completion`.

## İnceleme ajanları
- `bl-render-ayari`: gürültülü ya da yavaş render teşhisi.
- `ecc:blender-motion-state-inspection`: rig, poz, yer teması; ekran görüntüsünün yetmediği durumlar.

## Güvenlik ve kalite kapıları
- Render kontrolü kanıtlı (görüntü dosyası), "oldu" sözü yetmez.
- GLB boyutu web için küçük; three.js'de açılıyor.
- Oyun formatına taşımada ölçek ve kemik: `bl-mod-modeli-blender`.

## Tartışma konseyi
- Karar: prosedürel model mi içe aktarılan mesh mi, poligon bütçesi.
- `ecc:council` — varsayılan Claude personaları: 3D sanatçı, web performans, ürün sahibi.

## Jeton bütçesi
- Oturum: küçük (~3k, tahmini). Plan: küçük (~6k). Modelleme: büyük (~40k). Render: orta (~10k). Dışa aktarma: küçük (~5k). Doğrulama: orta (~10k). Hepsi tahmini.
- Uzun bpy log okuması `okuyucu` alt ajanına.

## Kaçınılacaklar
- `blender-uretim` ile `blender:blender-uretim` kopyasını birlikte yüklemek; birini seç.
- `blender` (MCP) çıktısını doğrulama kanıtı saymak.
- Oturumu açık bırakmak; kapat adımını atlamak.

## Aday (kurulu değil)
- `blender_cli`: headless Blender betik sözleşmesi.
- `blender_oturum`: aç/kapat/durum aracı.
- `blender_bekci`: Blender kod bekçisi PreToolUse hook'u.
- `bpy_kontrol`: var olmayan bpy özniteliği/operatörünü listeler.
- `blender_dogrula`: sayısal kapı.
- `blender_gorunum`: 4 Workbench + 1 Eevee görünüm kanıtı.
- `blender_pisir`: headless ışık/AO pişirme.
- `blender-dogrulama`: sayısal kapı, görünüm+IoU ve GLB hattı doğrulaması.
