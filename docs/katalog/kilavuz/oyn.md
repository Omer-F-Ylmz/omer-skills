# oyn — 16 benzersiz kayıt

**Amaç:** Oyun geliştirme ve mod ajanları: netcode, düşman AI, yol bulma, denge, seviye/oyun tasarımı, envanter, three.js/Unity/Godot betikleri ve 3DMigoto mod onarım/birleştirme/paketleme.

**İç yapı:** Tümü [ajan], ad kalıbı oyn-<iş>; gruplar: oyun sistemi (ag-senkronu, dusman-ai, yol-bulma, oyun-envanter, uyarlanabilir-zorluk), tasarım (oyun-denge, oyun-dokuman, seviye-tasarim, oyun-ses-geri-bildirim), motor (oyun-motoru-script, three-oyun-sahne, lua-betik), mod (mod-onarim, mod-birlestirici, mod-paketleme, mod-guvenlik-kontrol).

## En güçlü parçalar
- `oyn-mod-onarim` — Oyun güncellemesinden sonra bozulan 3DMigoto modlarını ini bölümü, hash ve loglarla teşhis eder.
- `oyn-mod-guvenlik-kontrol` — İndirilen mod dosyalarında şüpheli betik, çalıştırılabilir ve paketli DLL arar.
- `oyn-ag-senkronu` — Otoriter sunucu, tahmin, uzlaştırma ve gecikme telafisiyle çok oyunculu netcode.
- `oyn-oyun-dokuman` — Çekirdek döngü, mekanik ve kapsamla tek sayfalık oyun tasarım dokümanı.
- `oyn-three-oyun-sahne` — Küçük three.js tarayıcı oyunu: girdi, döngü, çarpışma, sahne yapısı.

## Birlikte kullanım
- oyn-mod-guvenlik-kontrol → oyn-mod-onarim / oyn-mod-birlestirici → oyn-mod-paketleme: mod yaşam döngüsü.
- oyn-oyun-dokuman → oyn-seviye-tasarim + oyn-oyun-denge + oyn-uyarlanabilir-zorluk.
- oyn-three-oyun-sahne + build ailesi (build-isometric-arpg, build-threejs-enemy-systems).

## Tuzaklar
- oyn-mod-onarim 3DMigoto'ya özgü (ini, hash); başka mod sistemlerinde doğrudan geçerli değil.
- Örtüşme: oyn-oyun-envanter ile build-game-inventory, oyn-dusman-ai ile build-threejs-enemy-systems; tek biri seçilmeli.

## Üyeler
- ajan (16): oyn-ag-senkronu, oyn-dusman-ai, oyn-lua-betik, oyn-mod-birlestirici, oyn-mod-guvenlik-kontrol, oyn-mod-onarim, oyn-mod-paketleme, oyn-oyun-denge, oyn-oyun-dokuman, oyn-oyun-envanter, oyn-oyun-motoru-script, oyn-oyun-ses-geri-bildirim, oyn-seviye-tasarim, oyn-three-oyun-sahne, oyn-uyarlanabilir-zorluk, oyn-yol-bulma
