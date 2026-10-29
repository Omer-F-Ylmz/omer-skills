# KAYNAK-DIZIN-1 (28 Eki)
- Dizin: `tools/envanter_tara.py --dizin [--tam]` → .kos/kopru/kaynak-dizin/dizin.tsv, 7058 satır: yontem 6168 · site 330 · varlik 413 · proje 54 · klon 44 · arac 24 · model 10 · baglayici 10 · sablon 5. mtime önbelleği: artımlı 1,0 sn, tam 39 sn. Günlük görev `omer-kaynak-dizin` 03:30 (kullanıcı görevi).
- Sorgu: çıktıya "## kaynaklar" (≤15 satır); `--kaynak "<iş>" [--hepsi]` tam eşleşme kümesini açar. Eski 3 kaynak grubu dizine taşındı, gövde payı küçüldü: 5 işte jeton yeni 1741–2179 ≤ eski 1912–2677 (bayt/3,6 tahmini; tiktoken yok).
- Süre: kaynaklar yalnız 0,17 sn; tam çıktı önbelleksiz ~10 sn (eski graphify/katalog alt süreçleri), önbellekli 0,1 sn.
- Recall (elle altın küme, 30 kaynak/5 iş): `--hepsi` %97 (29/30; kaçan: site-bg işinde scrolltide.co); top-15 %80 (24/30) → hedef %96 TUTMADI (top-15 için). Borsa botu için dizinde yalnız 3 ilgili kaynak var (içerik boşluğu).
- Sapmalar: özetler ücretsiz havuzla DEĞİL kural tabanlı (ilk **Ne:**/başlık satırı); A/B (özet vs tam bağlam plan) YAPILMADI; sistem kaynakları: yalnız ollama, global npm, Chrome yer imi (uygulama/font/pip/eklenti yok); video-derin 2070 JSON satırı yontem'i şişiriyor; docs/kutuphane/olcum çıktıları dizinden hariç.
- Ölçüm betiği: .kos/kopru/kaynak-dizin/olc.py (eski sürüm karşılaştırması için git HEAD kopyası gerekir).

## TUR 2 (28 Eki)
- Recall (30 kaynak/5 iş, elle altın küme): top-15 %87 (26/30) · özet+kuyruk (top-15 + sonraki 70 kaynağın adı, tür başına satır, "+N daha: --hepsi [--tur]") %100 · --hepsi %100. Kayıpsız: görünmeyen kalem `--kaynak "<iş>" --hepsi` ile açılır.
- `--brief` modu (graphify atlanır, tür başı 3 kalem, aile yok): 5 işte 1893–2484 jeton (tiktoken cl100k; tam çıktı 2245–3264; eski 2079–2691). 1.000 şartı kalktı, 1.500–2.500 bandında. arka_ajan.girdi() brief'i otomatik ekler (hata → boş).
- Süre: önbellekli 0,1 sn; alt süreç çıktıları 6 saat önbellekli + katalog/graphify paralel. Önbelleksiz yeni iş 7–9 sn → ≤5 sn HEDEFİ TUTMADI (katalog_ara ONNX gömme yüklemesi 4–7 sn).
- YAPILMADI: A/B (brief vs tam bağlam plan, bağımsız hakem); MCP/claude.ai bağlayıcı/artifact listelerinin dizine alınması, Notion/Slack başlık çekimi, gece görevine kor_nokta/her_sey_tara/mcp_adlar ekleme (tur bütçesi bitti).
- Ölçüm: .kos/kopru/kaynak-dizin/olc.py (tiktoken kurulu).

## TUR 3 (29 Eki)
- Dizine eklendi (tarama_satirlari, 7907 → 7692 satır tekil): uygulama 129, mcp 231 (kullanıcı+proje+plugin adları), baglayici 117 (CC-MARKET + notion/slack/linear/atlassian "bağlı değil" notu, giriş denenmedi), eklenti 24, model 49 (ollama+HF+ComfyUI), arac 94, varlik 423 (steam/epic dahil). Gizli girdiler (ANAHTAR-ADLARI, VERI, Divisima-gizli, htpasswd) kodda anahtar listesinde yok; dizinde eşleşme 0. Artımlı 0,76 sn.
- Gece görevi omer-kaynak-dizin: pythonw ile her_sey_tara + kor_nokta çalıştırıp `--dizin` koşar (pencere yok). mcp_adlar.py dizin sırasında çağrılır.
- A/B (brief vs tam çıktıyla plan, iki sıra, hakem ücretsiz havuz farklı modeller): borsa botu brief 2/2; İLİK 3D 1/2 (sıra yanlılığı, berabere). Brief tam plandan kötü değil; örnek 2 iş, tek hakem ailesi garanti değil.
- Kalan: Notion/Slack/Linear başlık çekimi bağlı olmadığından yapılamadı; önbelleksiz ≤5 sn tutmadı (ONNX yüklemesi); özetler hâlâ kural tabanlı. Ölçüm: .kos/kopru/kaynak-dizin/ab.py.
