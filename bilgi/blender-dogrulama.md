# Blender doğrulama katmanı (BLENDER-ARAC-1 · 1 Eki 2026)

Kaynak: docs/kaynak-tarama/7-blender.md Q1 + Faz 1 madde 3·4·6. Mekanizma alındı, kod kopyalanmadı.

## Sıra
Sayısal kapı → biçim (Workbench) → görünüş (Eevee). Görüntü ölçeği, pivotu ve topolojiyi kanıtlamaz (#8: 0.01 ölçek, 14 non-manifold kenar görüntüde görünmez).
Tüm araçlar `tools/blender_cli.py` sözleşmesi üstünde: `-b [blend] --python <betik> -- <json>`, tek satır `SONUC:` JSON, zaman aşımı 300 sn (PID ağacı kapatılır), exit 0 geçti · 1 kapı kaldı · 2 kullanım/yol · 3 çöktü/SONUC yok.

## Kapı listesi (`tools/blender_dogrula.py`)
bbox · non_manifold (+kapalı) · olcek_dondurme · havada · pivot · basibos_empty · malzeme (her yüz) · uv (dokulu malzeme) · eksik_doku · mutlak_yol · ucgen_butce · glb (geri okuma: mesh > 0, malzeme sayısı, bbox) + gltf-transform validate. `aykiri` (ekranda küçük, üçgeni yüksek) rapor alanıdır, kapı değil.
Havada muafiyeti: nesne özelliği `dogrula_serbest = True` ya da `--serbest a,b` (exploded view); muaflar raporda `serbest` listesinde.

## Eşikler
- Kaynaklı: bbox ±0.001 m (#8) · non-manifold 0 + kapalı (#8, #11) · glTF geri okumada mesh > 0 (#8) · 4 görünüm + 1 Eevee, kamera uzaklığı bbox'tan (#11, #12).
- Öneri (kaynakta yok; rapora `esik_kaynak: oneri`): silüet IoU ≥ 0.90 · bbox oranı ±%3 · GLB bbox ±%1 · üçgen bütçesi 500 000 · aykırı = ekran alanı < %1 ∧ > 10 000 üçgen · havada toleransı 0.001 m.

## Q1 geçiş koşulu
Kapı tam PASS ∧ IoU eşiği ∧ açık madde 0. Workbench FLAT + SINGLE, X-ray kapalı; saydam/yansıtıcı nesneler de opak silüet (gizlenmez — cam gizlenirse silüet eksik kalır).

## Dört ölçüt (araç değerlendirme)
- Bakım: stdlib + Blender'ın kendi bmesh/numpy'si; dış bağımlılık sabit sürümlü: @gltf-transform/cli 4.5.1 (npm -g, MIT) · fake-bpy-module-5.2==20260730 + pyright==1.1.414 (uv önbellekli ayrı ortam, MIT).
- CC'de çift mi: Lab MCP `get_blendfile_summary_missing_files` / `path_info` eksik doku ve mutlak yolu canlı oturumda listeler; kapı bunları exit kodlu tek JSON'da headless verir (çift değil, kapı rolü). Bekçinin karşılığı yok. pyright-lsp eklentisi kurulmadı (bpy_kontrol ile çift olurdu).
- İzin kapsamı: .blend yalnız Desktop\<Proje>\blender\; kanıt ve GLB çıktısı yalnız Desktop\<Proje>\; global PreToolUse hook yalnız `mcp__blender__execute_blender_code[_for_cli]`; npm -g tek paket.
- Context maliyeti: her araç tek satır JSON; görünüm tek `sayfa.png` (tek Read); bekçi reddi tek satır; SKILL.md +5 satır.

## Kod bekçisi — koruma, sınır değil
`tools/blender_bekci.py` (AST, <100 ms, ağ yok) reddeder: os.remove/unlink/rmdir · shutil.rmtree/move · subprocess/os.system/os.popen/ctypes · socket/urllib/requests/http · exec/eval/compile/__import__/getattr gizleme · Desktop\<Proje>\ dışına open() yazma, save/export filepath, `.filepath` ataması, filepath atanmadan `write_still`. Red mesajı tek satır: `sebep → düzeltme`. Statik taramayı kararlı biri aşabilir; amaç kazayı ve dikkatsizliği durdurmak, yetki sınırı değil.

## bpy statik kontrol sınırı
`tools/bpy_kontrol.py` modül düzeyi adları yakalar (`bpy.ops.mesh.primitive_cube_addd`, `bpy.types.Objekt`); bpy_struct örnek öznitelikleri (`bpy.context.scene.frame_strat`) fake-bpy'de dinamik olduğundan yakalanmaz.

## Kural 29 karşılaştırması (Lab MCP, ZATEN VAR)
Lab MCP'nin üstün yanı canlı sahnede bağlı kütüphane özeti ve kullanım tahmini; bizde bağlı kütüphane yalnız mutlak yol için denetlenir. Alınan: resmi sunucunun "ekranda küçük, üçgeni yüksek" örneği `aykiri` rapor alanı olarak.
