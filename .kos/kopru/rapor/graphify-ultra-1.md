# GRAPHIFY-ULTRA-1 — ARA (d4, 14 Eki 23:45)
Katalog: kullanılan [graphify query --budget, graphify_hafif/hizli, graphify_sor (yeni), graphify_harita (yeni), graphify_ultra_g1 (yeni)] · atlanan [plan-kur/katalog (rutin tek alan), alt ajan (kural 0), claude -p (izin 10/10 bitti), OmniRoute etiket (dizin etiketi yetti)]
| ölçü | önce | sonra |
|---|---|---|
| artımlı update süre / tepe RSS | 48 sn / 829 MB | 3.8 sn / 332 MB (omer-skills, d2) · 3.1 sn / 74 MB (TELVE, d4) |
| G1 isabet (20 soru, grep alt doğruluk) | 15/20 (query --budget 400) | 18/20 (graphify_sor) |
| G1 yanıt boyu (ortalama) | 19.6 satır / 188 kelime | 2.6 satır / 16 kelime (≤40 satır ✓) |
| .kos/kopru betikleri grafta | yok (.gitignore /.kos/) | 52 betik, +884 düğüm |
| proje haritası | yok | omer-skills ~568 · TELVE ~596 jeton (≤800 ✓) |
| A/B keşif jetonu (d3, n=2) | 1× | 0.75× / 0.87× — G5 kapısı GEÇMEDİ |
- G1 kök neden: graphify .gitignore'u uyguluyor; `/.kos/` köprü kodunu da gizliyordu (takipli dosyalar dahil). `.graphifyignore` negation zinciri yalnız `.kos/kopru{,/onay,/video}/*.py`'yi geri alır (günlük/devir dışarıda, _is_ignored ile 10 yol doğrulandı).
- G1 kaçak sınıfı 'siralama' (4/5): Türkçe soru kelimeleri query'yi dağıtıyordu → `graphify_sor.py`: tanımlayıcıyı etikette birebir arar (sembol · dosya:satır · docstring özeti + çağıran/içerik), yoksa git grep tanımı, yoksa query. Kalan 2 kaçak: md başlık sorusu (tanımlayıcısız), TELVE'de 10+ kopya dosyada aynı ad.
- G3 harita `.kos/kopru/harita/<proje>.md` (graphify-out/ Read izninde kapalı). Küme etiketi = kümenin en sık dizini (shortcut; ücretsiz model etiketi gerekmedi).
- Tablo, G1: docs/kutuphane/olcum/graphify-ultra-g1{,-sor}.tsv. Desktop 23:00 kararı: oku_yonlendir köprü profilinde kalır, global kanca önerisi yok.
- Yapılmadı: is-akisi keşif satırını graphify_sor + harita'ya çevirmek, G6 paket (graphify skill 0.9.57→0.9.88, zip_denetle, atlas kartı), G0 izleme koşusu (yarın aynı saat), BİTTİ. Devir: devir/graphify-ultra-1-devam.md
