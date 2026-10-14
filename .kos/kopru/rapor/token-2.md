# TOKEN-2 rapor

## d1 — K1 önbellek durması kök nedeni (14 Eki ~12:50)
Durma = cache_write 0 VE önbelleksiz girdi ≥3k (token_olc --durma tanımı). Kaynak: ~/.headroom/h2a_kayit.jsonl (3887 istek, 3–5 Eki; her istekte mesaj karması ÖNCE/SONRA + cw/cr/un) ve savings_events.jsonl v2 (66k istek, 2–14 Eki). Betik/çıktı: docs/kutuphane/olcum/token-2/.
| Headroom son mesajı (CC'nin cache_control koyduğu yer) | Opus 5.5 durma | Sonnet 5.5 |
|---|---|---|
| yeniden yazdı (sıkıştırma) | 320/705 (%45.4) | 8/38 |
| aynı bıraktı | 11/1537 (%0.7) | 3/212 |
| yalnız ara mesaj değişti (tüm modeller) | 9/1537 (%0.6) | |
- Durmaların 252/320'sinde okuma bir önceki istekle birebir aynı → işaret zaten önbellekli noktada kalıyor, kuyruk yazılmıyor (R0f imzası: okuma 115.9k sabit, cw=0, önbelleksiz kuyruk büyür).
- Kod: headroom 0.39.0 (Desktop runtime, 6767/6768 vekilleri) `cache/prefix_tracker.py` normalize_message_cache_control → _breakpoint_index: "yeniden yazılmış kuyruk" (block_rewrite_tail, ≥20 blok) görünce en yeni işareti son bloğa değil "kararlı koşu" sonuna taşır; kendi docstring'i: "a marker anchored short of the final block leaves the tail billing as fully uncached input". Kapatma bayrağı: HEADROOM_STABLE_BOUNDARY_BREAKPOINT=0 (yama gerekmez, Headroom kalır).
- Önceki elenenler (TELVE-TOKEN-1): TTL değil, görüntü değil, ölçüm artefaktı değil, CC sürümü kanıtsız. opus-4-7 satırları (%95–100) önbelleksiz model, karşılaştırma dışı.
- Doğrulama (≤2 claude -p): test vekili 6769 (k1_vekil.py, her _breakpoint_index kararını izler) · A varsayılan / B bayrak=0 · opus high MCP'siz, 24 dosya sıralı Read. Günlük .kos/kopru/token-2-k1.log.
- SONUÇ: DOĞRULANAMADI. A 24 istek · B 25 istek; ikisinde de durma 0 · _breakpoint_index yer değiştirme 0/24 ve 0/25 · önbelleksiz 48/50 · sonuç 214 (ikisi doğru). Kısa sıralı Read görevi ≥20 bloklu yeniden yazılmış kuyruk üretmedi → mekanizma tetiklenmedi; aday kök neden ne doğrulandı ne çürüdü. claude -p hakkı (2/2) bitti. Sonraki adım ek claude -p istemez: canlı vekillerin önündeki izleyiciyle (k1_vekil.py kancası) doğal uzun oturumlarda durma × yer değiştirme toplanır.

## d1 — K0
Yapılmadı (oturum çağrı tavanı 40/45, M5 bölünmesi) → devir/token-2-devam.md.
