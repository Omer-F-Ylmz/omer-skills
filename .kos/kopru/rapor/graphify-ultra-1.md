# GRAPHIFY-ULTRA-1 — ARA (d3, 14 Eki 22:13)
Katalog: kullanılan [graphify query --budget, graphify_hafif/hizli, oku_yonlendir, olcum_sira, arka.py, bekle.py] · atlanan [plan-kur/katalog (rutin tek alan), alt ajan (kural 0)]
| ölçü | önce | sonra |
|---|---|---|
| artımlı update süre / tepe RSS | 48 sn / 829 MB | 3.8 sn / 332 MB (d2) |
| artımlı RAM kapısı | %75 | %85 (tam %75 kalır; graphify_hafif esik, is-akisi L33/L42) |
| query yanıtı (--budget 400, 5 soru) | ~2000 jeton | 14–24 satır, ~200 kelime (G3 ≤40 satır ✓) |
| A/B profil (omer-skills, n=2) girdi medyan A→B | 265k (334k·197k) | 198k (199k·197k) → 0.75× |
| A/B telve (TELVE fincan.js 872 sat., n=2) | 259k (259k·259k) | 226k (258k·194k) → 0.87× |
| A/B kontrol hafif (d2, n=1) | 198k | 334k → yayılım ±%70 |
| tur · süre (medyan) | profil 3·52 sn, telve 4·54 sn | profil 3·45 sn, telve 4·52 sn |
- G5 KAPISI GEÇMEDİ: keşif jetonu 0.75–0.87× (hedef ≤0.5×), maliyet usd A≈B (0.52–0.57). Kanca farkı gürültü bandında (kontrol ±%70) → Desktop kararı (1) gereği global CC kancası için onay --kuru HAZIRLANMADI (kanıt yok).
- Doğruluk: yanıtlar graphify-ultra-ab.tsv'de; K8 kör puan yapılmadı. Kancanın gerçekten tetiklenip tetiklenmediği --no-session-persistence yüzünden transkriptten doğrulanamadı.
- G1 örneklem (5 soru, --budget 400): 3/5 isabet; kaçak: yeni dosya (oku_yonlendir, graf bayat) + .kos/ grafta yok (git-ignore değil, takipli → graphify gizli dizin süzgeci şüphesi, kanıtlanmadı).
- G4: is-akisi "Token araç sırası"na keşif sırası satırı (harita → query/oku → Read aralık). test_is_akisi 1/1.
- claude -p: d3'te 6 (toplam 10/10). graphify update bu oturumda koşmadı.
- Yapılmadı: G1 20 soru, G3 harita (OmniRoute etiket), G6 paket, TELVE .graphifyignore. Devir: devir/graphify-ultra-1-devam.md
