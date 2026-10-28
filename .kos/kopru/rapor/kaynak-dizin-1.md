# KAYNAK-DIZIN-1 (28 Eki)
- Dizin: `tools/envanter_tara.py --dizin [--tam]` → .kos/kopru/kaynak-dizin/dizin.tsv, 7058 satır: yontem 6168 · site 330 · varlik 413 · proje 54 · klon 44 · arac 24 · model 10 · baglayici 10 · sablon 5. mtime önbelleği: artımlı 1,0 sn, tam 39 sn. Günlük görev `omer-kaynak-dizin` 03:30 (kullanıcı görevi).
- Sorgu: çıktıya "## kaynaklar" (≤15 satır); `--kaynak "<iş>" [--hepsi]` tam eşleşme kümesini açar. Eski 3 kaynak grubu dizine taşındı, gövde payı küçüldü: 5 işte jeton yeni 1741–2179 ≤ eski 1912–2677 (bayt/3,6 tahmini; tiktoken yok).
- Süre: kaynaklar yalnız 0,17 sn; tam çıktı önbelleksiz ~10 sn (eski graphify/katalog alt süreçleri), önbellekli 0,1 sn.
- Recall (elle altın küme, 30 kaynak/5 iş): `--hepsi` %97 (29/30; kaçan: site-bg işinde scrolltide.co); top-15 %80 (24/30) → hedef %96 TUTMADI (top-15 için). Borsa botu için dizinde yalnız 3 ilgili kaynak var (içerik boşluğu).
- Sapmalar: özetler ücretsiz havuzla DEĞİL kural tabanlı (ilk **Ne:**/başlık satırı); A/B (özet vs tam bağlam plan) YAPILMADI; sistem kaynakları: yalnız ollama, global npm, Chrome yer imi (uygulama/font/pip/eklenti yok); video-derin 2070 JSON satırı yontem'i şişiriyor; docs/kutuphane/olcum çıktıları dizinden hariç.
- Ölçüm betiği: .kos/kopru/kaynak-dizin/olc.py (eski sürüm karşılaştırması için git HEAD kopyası gerekir).
