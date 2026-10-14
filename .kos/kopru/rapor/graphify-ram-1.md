# GRAPHIFY-RAM-1 — BİTTİ (14 Eki, GRAPHIFY-ULTRA-1 d1 içinde kapatıldı)
| | önce | sonra |
|---|---|---|
| graph.json | 337 MB, 372k düğüm | 28–37 MB, 48k düğüm |
| `update` tepe RSS / süre | ~3.5 GB (Desktop gözlemi) | tam 1552 MB / 74 sn · artımlı 829–975 MB / 48–63 sn |
| manifest | 22 679 dosya | 5 992 |
- Kök: .graphifyignore + .gitignore dışı untracked ölçüm klasörleri (.claude/b2-*, t7f2…) grafın %87'si.
- İlk ağır geçiş (eski grafı 2× json.load, ~3.5 GB) atlandı: `graphify_buda.py <kök>` grafı öğe öğe budadı (tepe 730 MB, 31 sn), graphify'ın kendi `_load_graphifyignore/_is_ignored` kuralıyla.
- `graphify_hafif.py [kök] [--tam]`: varsayılan artımlı (built_at_commit'ten git diff + çalışma ağacı → `_rebuild_code(changed_paths)`), RAM <%75 kapısı, kilit.
- Kapı (`graphify_kapi.py fark`): oku 4/4 AYNI; 5 query başlangıç düğümleri aynı, fark yalnız başlık sayısı/sıra.
- Hedef ≤1 GB: artımlıda TUTTU, tamda 1.55 GB. ≤60 sn: artımlı 48 sn sınırda (süre detect taraması + yükleme; ULTRA G2'de).
- is-akisi SKILL.md L1 satırına sarmalayıcı eklendi (DEVAM-KURALI artık oraya yönlendiriyor).
