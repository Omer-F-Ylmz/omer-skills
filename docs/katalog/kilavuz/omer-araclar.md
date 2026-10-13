# omer-araclar — 47 benzersiz kayıt

**Amaç:** Ömer'in repo içi Python araçları: Blender headless hattı ve doğrulama kapıları, token/önbellek ölçümü ve yamaları, skill/ajan kataloğu ve kalite denetimi, claude.ai zip paketleme.

**İç yapı:** Tümü [arac]; açıklama önekleri dalga kodunu verir: BLENDER-ARAC-*, TOKEN-*, KALİTE-*, ENVANTER-*, KURULUM/YUKLE-*, İKİ TARAF (claude.ai paketleri).

## En güçlü parçalar
- `katalog_ara` — Yetenek kataloğunda iş tarifiyle en iyi 8 aracı tek satır sonuçla bulur.
- `blender_dogrula` — Sayısal kapı; görüntüden önce koşulur, ölçek/pivot/topolojiyi görüntü kanıtlamaz.
- `blender_gorunum` — 4 Workbench + 1 Eevee görünüm ve dogrula.json ile görünüm kanıtı.
- `glb_hat` — meshopt + webp optimize → validate → inspect, önce/sonra KB.
- `bpy_kontrol` — Var olmayan bpy özniteliği/operatörünü statik olarak listeler.
- `skill_filo_denetim` — Bütün skill filosunun API'siz salt-okur statik denetimi.
- `token_olc` — Oturum jsonl'lerinden ağırlıklı token ölçümü.
- `model_sec` — claude -p adımı için kural tabanlı yönlendirme; model düşürülmez.
- `gpu_kilit` — GPU kullanan iki işin aynı anda koşmasını engeller.
- `varlik_indir` — Poly Haven ve ambientCG'den CC0 HDRI/doku/model indirir.

## Birlikte kullanım
- blender_cli → bpy_kontrol → blender_dogrula → blender_gorunum → glb_hat.
- katalog_yenile → katalog_ara: kataloğu yenileyip iş tarifiyle aramak.
- skill_filo_denetim → skill_iyilestir → kalite3_zip: denetim, iyileştirme, paketleme.
- blender_pisir + gpu_kilit: GPU'lu pişirmede çakışmayı önlemek.

## Tuzaklar
- aciklama_yaz, tetik_olc abonelikle claude -p çağırır; çağrı sayısı sınırlanmalı.
- headroom_yama ve cmem_yama belirli sürümlere (Headroom 0.39.0) bağlı yamalar.
- yukle8/yukle10/yukle12b farklı dalgaların paketleyicileri; yanlış sürümü seçmek kolay.
- Bazı açıklamalar iç bağlam ister (gstack_browse, h2_sinif); tek başına anlaşılmıyor.

## Üyeler
- arac (47): aciklama_yaz, ajan_getir_zip, ajan_katalog, ajan_uret, awesome_katalog, awesome_rehber_zip, blender_bekci, blender_cli, blender_dogrula, blender_gorunum, blender_oturum, blender_pisir, bpy_kontrol, cagri_sayac, cc_profil, cmem_yama, departman_katalog, duman_claudeai, fable_ajan_hook, glb_hat, godmode_onsoz, gorsel_uret, gpu_kilit, gstack_ai, gstack_browse, h2_sinif, h2a_kayit, headroom_yama, kalite3_hiz, kalite3_zip, katalog_ara, katalog_yenile, kontur_profil, model_olc, model_sec, node_yolu_uyari, profil, rtk_onisle, skill_denetim, skill_filo_denetim …
