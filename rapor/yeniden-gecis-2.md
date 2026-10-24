# YENIDEN-GECIS-2
- Ölçüm (5 video, tools/yg2_olcum.py): 2 işçi 292/saat RAM%83 GPU%34 · 4 işçi 482/saat RAM%78 GPU%41 · 6 işçi 343/saat RAM%84 GPU%37. Hiçbiri %85'i geçmedi.
- Seçilen: 4 işçi (6 işçi %85 altında ama daha yavaş ve sınıra yakın; sapma gerekçesi bu).
- Liste: 2040 url (reel+post+shorts + telefon/omer notları − ig-silinen) → .kos/kopru/yeniden-gecis-2-liste.txt; çıktı docs/video-tarama/derin-2/ (biten kod atlanır → kaldığı yerden sürer).
- İlk 5 dk: 46 video (post ağırlıklı, ~550/saat); reel ağırlıklı kısımda düşebilir. Tahmini bitiş: 4–6 saat.
- Arka plan: yönetici sahipli arka-istek, pid 57564 (toplu_gozetmen 3 yeniden deneme). Günlük .kos/kopru/yeniden-gecis-2-tara.log (arka: ...-arka.log). Yeniden başlat: arka-istek/yeniden-gecis-2.json'dan "pid" silinirse yönetici sürdürür.
- Adım 3–4 (tarama bitince): modlar.tsv ve yeniden-gecis-1-yeni.tsv betik yolu bu repoda bulunamadı/doğrulanmadı → ayrı iş; çalıştırılmadı. Girdi: docs/video-tarama/derin-2/*.json.
