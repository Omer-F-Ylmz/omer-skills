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

## d1b — K0 (14 Eki ~13:10; yeni claude -p yok)
Betik `.claude/token2/k0_olc.py` (TELVE taban.oturum yeniden kullanıldı; iş adı = istemdeki ilk BÜYÜK-HARF etiketi; ağırlık token_olc: önbelleksiz 1 · okuma 0.1 · yazma 1.25 · çıktı 5). Son 14 gün, 4 proje, 1357 oturum, 850M ağırlıklı (alt ajan dahil). Ayrıntı k0_olc.json.

| proje · iş | oturum | ağırlıklı M | alt ajan % | çıktı % | kaçırma | ilk bağlam k | top kategori |
|---|---|---|---|---|---|---|---|
| omer-skills · etiketsiz (köprü dışı/-p) | 403 | 201.0 | 19 | 15 | 462 | 84 | dosya_okuma, arama_kesif |
| mod · etiketsiz | 23 | 50.5 | 1 | 19 | 104 | 92 | dosya_okuma, headroom_retrieve |
| omer-skills · ENVANTER | 42 | 44.7 | 33 | 12 | 62 | 67 | dosya_okuma, devir |
| omer-skills · KARAR | 10 | 27.0 | 30 | 16 | 51 | 105 | dosya_okuma |
| omer-skills · TOKEN | 36 | 26.3 | 11 | 15 | 57 | 64 | dosya_okuma, devir |
| TELVE · TELVE | 16 | 22.8 | 29 | 19 | 33 | 70 | dosya_okuma, görüntü |
| blender · GLB | 12 | 21.1 | 0 | 25 | 23 | 78 | dosya_okuma, görüntü |
| omer-skills · BLENDER | 17 | 17.8 | 11 | 15 | 30 | 62 | dosya_okuma, ölçüm |
| omer-skills · DEVAM-KURALI / KALİTE / RUFLO / VİDEO | 8–22 | 11–17 | 2–56 | 6–21 | 20–28 | 41–63 | dosya_okuma |

En büyük 5 israf adayı (M ağırlıklı): omer-skills sabit taban (ilk bağlam × adım × 0.1) 164 · omer-skills önbellek kaçırma (>30k yeniden yazım, ilk adım dahil = üst sınır) 149 · omer-skills alt ajan 121 · omer-skills çıktı 99 · mod önbellek kaçırma 28. Araç sonucu kategorileri (dosya_okuma ≤3M) sabit taban/kaçırma/alt ajanın yanında küçük.

Sabit taban bileşenleri (context-profil-tam-75k, /context): Custom agents 29.2k (%47) · Skills 24.3k (nameonly 18.3k) · Messages (SessionStart enjeksiyonları: claude-mem, superpowers, context-mode, ponytail, rtk) 5.5k · System prompt 2.1k · Memory/CLAUDE.md 1.4k · MCP 339k ve sistem araçları 14k ertelenmiş (bağlamda değil). Toplam ≈62k = Veri'deki "62k/adım". K2 için en büyük kalem ajan listesi (~400 ajan açıklaması); ajan oturumunda kapatma adayı.

| aşama | araç (katalog_ara) | nasıl | beklenen tasarruf | kullanılmıyorsa neden |
|---|---|---|---|---|
| araştırma | departman-arastirma-ogrenme, ara-* ajanları, OmniRoute (K8), defuddle | alt adımı Claude dışına / temiz markdown | R0a 6.7M alt ajan → ≤0.5M (hedef) | OmniRoute alt adımı köprüde yok (TOKEN-1 M9) |
| tasarım | design-extractor, design-dna, create-design-md, taste | DESIGN.md tek çağrı | tasarım keşfi okuma turu | ölçülmedi |
| iskelet | K7 site kiti (yok), animasyon-scroll-paket | tek komut kurulum | iskelet 1 adım | kit henüz yok (K7) |
| sahne/shader | animasyon-atolyesi, web-sahne-desenleri §2d, threejs-3d-paket, web-technique-to-skill | hazır tarif | sahne yazımı çıktı jetonu | — |
| varlık/Blender | blender-oturum, blender-uretim, blender_patlat.py, Poly Haven/ambientCG | betik önce, JSON çıktı | görüntü okuma (blender·GLB çıktı %25, görüntü 2. kategori) | — |
| doğrulama | kapi.mjs, chrome-kontrol, departman-test-qa | sayı önce, görüntü eşikte | görüntü_okuma | — |
| devir/bağlam | graphify+oku, headroom, rtk, context-mode, claude-mem, strategic-compact | dar okuma, sıkıştırma | dosya_okuma + sabit taban | mod'da headroom_retrieve 0.44M: sıkışan Read'in geri çağrısı israf |

## d1b — K1b doğal tetik
(arka planda: .kos/kopru/token-2-k1b.log → .claude/token2/k1b.jsonl; sonuç aşağıya)
