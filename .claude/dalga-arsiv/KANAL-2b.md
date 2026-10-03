# KANAL-2b — kuyruk + istisna + kanal ekleme
KARAR: Ömer onayı 3 Eki. ≤35 araç çağrısı (30'da commit+push+DUR). Model çağrısı 0. İndirme yok; metadata istekleri ≥2 sn.
Ek karar: ESKİ HAT 8 id "işlenmiş" atlamasından muaf; atlama yalnız kuyrukta bekleyen ya da tarihli (yeni hat) raporu olan id'ye.

Kabul:
- C1 "takip: hayır" notlu satırın kanalı otomatik takibe girmez; listedeyse değer değişmez. Test + mutasyon.
- C2 `video kanal ekle <url>` → channel_id, kanallar.json takip (kaynak "Ömer · kanal linki"), varsa korunur, sonra envanter. Test (sahte yt-dlp).
- C3 InsiderForce · Nick Automates · Andrii Bachinskyi: teşhis + kök neden + test, yeniden envanter; olmazsa sebebiyle "yarım".
- C4 kuyruğa ekleme (kaynak: Ömer); tekilleştirme; çift dikiş → docs/video-tarama/cift-dikis.md.
- C5 canlı: C2 MeticsMedia · C3 · C4 · kanal liste; parti önerisi (koşulmaz).
- Kırmızı-önce ayrı commit (C1·C2·C3) · eski test değişmez · tam suit · gitleaks · arşiv · push · graphify update.

Durum:
- Kırmızı-önce: fc867a2 (C1) · 44dec07 (C2) · fcca141 (C3). C1 mutasyon kırmızı görüldü, geri alındı.
- C1/C2/C3 kodu yeşil (kanal testleri 10/10). C3 kök neden: yalnız-short kanalda videos sekmesi yok → envanter yalnız shorts için "sekme yok" tanıyordu → yarım + döngü kırılıyordu. Düzeltme: `rf"does not have a {sekme} tab"`.
- 30 çağrı sınırında DUR (commit+push yapıldı).
- KALAN: C3 canlı yeniden envanter (3 kanal: `video kanal envanter --kanal <cid>`) · C4 kuyruk ekleme (biçim `| id | süre | başlık | not | bekliyor |`; süre/başlık .kos/kanal ya da yt-dlp -J ≥2 sn; ESKİ HAT muaf) · cift-dikis.md · C2 canlı MeticsMedia · kanal liste · parti önerisi · tam suit · gitleaks · arşiv · graphify update.
