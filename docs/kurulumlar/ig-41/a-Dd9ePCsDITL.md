# Dd9ePCsDITL · arham.animations · görsel gönderi (6 slayt) · https://www.instagram.com/p/Dd9ePCsDITL/

## Özet
Modelleme, UV, doku, Geometry Nodes, harita, kamera ve iş akışı alanlarında 12 ücretsiz Blender eklentisinin listesi. Hepsi GPL olduğundan KUR verilmedi; işe yarayan mekanizmalar bl-uv-acma ve varlik-hatti'na yönlendirildi.
Açıklamadaki "Destruction, fracture & rigid-body" satırına slaytlarda bir eklenti adı karşılık gelmiyor (açıklama kesik).

## Kalemler
| ad | tür | link | karar | ölçütler (bakım · çift · izin · context) | gerekçe |
|---|---|---|---|---|---|
| Hardflow | Blender eklentisi | https://extensions.blender.org/add-ons/hardflow/ | ÖĞREN | site canlı · yok · dosya yazma · - | GUI'ye dayalı hard-surface boolean aracı; headless hatta bpy boolean yeterli. Ders: çizerek kesme (draw-to-cut) iş akışı |
| LoopTools | Blender eklentisi | https://extensions.blender.org/add-ons/looptools/ | ÖĞREN | site canlı · yok · dosya yazma · - | GPL. Ders: loop düzleştirme, daire ve köprü işlemleri bpy.ops.mesh.looptools_* ile betikten çağrılabiliyor |
| F2 | Blender eklentisi | https://extensions.blender.org/add-ons/f2/ | ÖĞREN | site canlı · yok · dosya yazma · - | Elle yüz oluşturmayı hızlandırıyor; etkileşimli modelleme alışkanlığı, ajan hattına katkısı yok |
| UniV | Blender eklentisi | https://github.com/Oxicid/UniV | UYARLA | ★172 push:2026-10-07 arşiv:h · kısmen:bl-uv-acma · dosya yazma · - | GPL olduğundan kod alınmaz. alınacak: ada hizalama, istifleme ve texel işlemleri → bl-uv-acma |
| UVO | Blender eklentisi | bulunamadı | RED | - · kısmen:bl-uv-acma · - · - | Extensions sayfası 404, GitHub'da da yok. Örtüşen UV kontrolünü Blender'ın yerleşik UV > Select > Overlap işlevi de yapıyor |
| Texel Density Checker | Blender eklentisi | https://github.com/mrven/Blender-Texel-Density-Checker | UYARLA | ★463 push:2026-07-06 arşiv:h · kısmen:bl-uv-acma · dosya yazma · - | GPL. alınacak: texel yoğunluğunu ölçme, eşitleme ve seçme hesabı → bl-uv-acma + varlik-hatti |
| Molecular Nodes | Blender eklentisi | https://github.com/BradyAJohnston/MolecularNodes | ÖĞREN | ★1382 push:2026-10-12 arşiv:h · yok · dosya yazma, ağ · - | Bilimsel görselleştirme, konumuz dışı. Ders: dış veriyi Geometry Nodes'a aktarma deseni |
| Attribute Baker | Blender eklentisi | https://extensions.blender.org/add-ons/attribute-baker/ | UYARLA | site canlı · yok · dosya yazma · - | GPL. alınacak: GN attribute → doku bake adımı → varlik-hatti (GLB dışa aktarımında GN verisi kaybolmasın) |
| BlenderGIS | Blender eklentisi | https://github.com/domlysz/BlenderGIS | ÖĞREN | ★9469 push:2025-12-20 arşiv:h · yok · ağ, dosya yazma · - | Ders: gerçek dünya arazisi DEM ve uydu görüntüsüyle içe aktarılıp üstüne bina oluşturulabiliyor |
| Camera Shakify | Blender eklentisi | https://github.com/EatTheFuture/camera_shakify | ÖĞREN | ★1273 push:2026-02-07 arşiv:h · yok · dosya yazma · - | Slaytta "Camera Shaky" yazıyor (ad tahmini), lisans NOASSERTION. Ders: kamera sarsıntısı genlik ve frekanslı bir gürültü katmanı; F-curve noise ile kurulabilir |
| Paper Color Manager | Blender eklentisi | bulunamadı | RED | - · yok · - · - | Extensions sayfası 404, GitHub aramasında da yok |
| Quick Favorites | teknik | - | ÖĞREN | - · yok · - · - | Blender'ın yerleşik Q menüsü. Ders: sık kullanılan araçları favorilere eklemek; headless hatta etkisi yok |
