# GRAPHIFY-RAM-1 devir (14 Eki, çağrı 30'da durdu)
DESKTOP 21:33 (ULTRA-1 ÖNCE BU): 3.5 GB'lık "budama" update'ini KOŞMA. Onun yerine eski graphify-out'u SILMEDEN taşı (graphify-out.yedek-14eki/) ve .graphifyignore ile TEMİZ yeniden kur (`graphify . --code-only` + `graphify cluster-only . --no-label`, graphify_hafif.py kuralıyla: RAM <%75, tek örnek) — eski 337 MB grafı hiç yüklemez. Sonra iki ardışık update ölç (tepe RSS + süre) + graphify_kapi.py önce/sonra. .graphifyignore + sarmalayıcı + kapı betiklerini HEMEN commit et (diğer ajanların update'i de hafif olsun). 21:19'daki 3.5 GB update'i Desktop durdurdu (düğüm budama yarıda; grafı kullanma, yeniden kur).
Kök neden: graphify-out/graph.json 337 MB (754k düğüm); update bunu iki kez json.load ediyor (watch.py:1030/1037) → ~3.5 GB.
Düğümlerin 641k'sı untracked ölçüm klasörlerinden (.claude/t7f2-birlesik 250k, b2-aile 224k, b2-olcum 168k); docs/video-tarama 54k (izlenen, kaldı).
update'te --code-only yok (yalnız extract'ta); update zaten AST-only. Yol: .graphifyignore (watch.py is_ignored_always her rebuild'de düğüm siler).
Yapılan: .graphifyignore (kök) · .kos/kopru/graphify_hafif.py (RAM<%75 kapısı, tek örnek kilidi, tepe RSS+süre) ·
.kos/kopru/graphify_kapi.py (once alındı: rapor/graphify-ram-1/once, 5 query + 4 oku). Commit YOK.
Önce ölçümü: RAM %77 → koşmadı; önce değeri = Desktop gözlemi 3.2–3.5 GB + graph.json 337 MB.
Sıradaki (RAM <%75 iken, sırayla):
1. `python .kos/kopru/graphify_hafif.py` → ilk koşu eski grafı yükleyip dışlananları siler (ağır, ~3.5 GB). Shrink guard reddederse `... --force`.
2. Aynı komut ikinci kez → kararlı durum tepe RSS/süre (hedef ≤1 GB, ≤60 sn); graph.json boyutu.
3. `python .kos/kopru/graphify_kapi.py sonra` + `... fark` (dışlanan klasör satırları süzülür).
4. rapor/graphify-ram-1.md (≤12 satır) · DEVAM-KURALI 20:58 satırına "sarmalayıcı: .kos/kopru/graphify_hafif.py" ekle ·
   commit main (.graphifyignore + iki betik force-add + rapor; CLAUDE.md/.claude/settings.json'a dokunma) · SIRA "GRAPHIFY-RAM-1 BİTTİ".
BİTTİ (14 Eki, GRAPHIFY-ULTRA-1 d1 içinde) — rapor/graphify-ram-1.md
