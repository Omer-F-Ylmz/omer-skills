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

## d2 (ara kayıt, 14 Eki 13:45) — K2 + K5 + K8 tasarımı; K1b ve K8 kör karşılaştırma devirde
K2: 14 günlük 3841 transkriptte 851 Agent çağrısı, 16 farklı ajan; ~/.claude/agents'taki 580 kullanıcı ajanından yalnız 2'si kullanıldı (ajn-ajan-tanimi-yazar 21, dok-rapor-uretici 2). `tools/cc_profil.py` yeni `ajanTut` anahtarı: dışındaki kullanıcı ajanları oturuma özel `permissions.deny Agent(ad)` (--settings dosyası; global ayar yok). Profil `ajan` (profiller/cc-arka.json). Yerleşik, proje ve plugin ajanları etkilenmez.
| kol (ajan_sira bayrakları, haiku, 1 adım boş görev) | ilk istek girdisi |
|---|---|
| önce (TTL 5m) | 64 999 |
| sonra (`ajan` profili) | 28 735 (−%56; hedef ≤30k ✓) |
Köprüye bağlama AÇIK KARAR (devir): katalog ajanları gizlenir; plan-kur önerirse CC_PROFIL_ZORLA=tam.
K5: DEVAM-KURALI'na tek satır (ölçüm yöntemi).
K8: `tools/ucuz_alt.py`: istem + bağlam dosyaları → OmniRoute cc-yedek-dis (Claude-dışı), yanıt dosyaya, stdout'a yalnız yol/model/jeton; düşünme kapalı, UA başlığı, kesik yanıt → çıkış 2. Kör karşılaştırma koşulmadı (oturum çağrı tavanı 40/45) → devir 2. adım.
Not: mod'daki headroom_retrieve 0.44M israfı (sıkışan Read'in geri çağrısı) K2/K4'te ele alınacak.
claude -p: 2/2 (k2_olc.py). Test: test_cc_profil + test_token1 21 ✓, test_ucuz_alt 3 ✓.

## d3 ara (14 Eki ~14:45) — K9 · K1b farkı · K8
- K9 düşünme: CC 2.1.295 kodu Opus 4.7+/5.5'e her zaman `thinking:{type:"adaptive"}` yollar; MAX_THINKING_TOKENS>0 yalnız eski modellerde budget_tokens olur → köprü işçilerinde ETKİSİZ (k7b-think10k "≈taban" sonucunun nedeni). Ölçüm: MAX_THINKING_TOKENS=2000 ile tek istekte çıktı 5112 (görünür ~200) → tavan yok sayıldı; cevap doğru. Kaldıraç effort: aynı görev --effort medium çıktı 4314 (−%16), cevap doğru (n=1).
- Tavanın keseceği pay (k9_dusunme.py, dökümler; düşünme ≈ çıktı − görünür/4):

| proje | istek | düşünme/çıktı | 10k üstü istek | 10k kesimi (çıktı) | 4k kesimi |
|---|---|---|---|---|---|
| TELVE | 1383 | %82 | %2.2 | %11.5 | %24.2 |
| Blender | 928 | %82 | %2.5 | %7.4 | %22.1 |
| omer-skills | 30992 | %75 | %0.4 | %2.0 | %8.3 |

- Öneri: ajan profiline MAX_THINKING_TOKENS EKLENMEZ; mekanik adımlara --effort medium, gerçek işte kalite kapılı A/B sonrası (Desktop kararı).
- K1b farkı: 6769 test vekili ve 6768 aynı headroom 0.39.0 çalışma zamanı; fark 6768'de headroom-desktop'un verdiği ~40 HEADROOM_* değişkeni (MODE, SAVINGS_PROFILE, COLD_RECOMPACT, READ_MATURATION, COMPRESS_USER_MESSAGES, BACKGROUND_COMPRESSION…) + --log-messages; k1_dogrula bunları geçirmiyor → 6769 neredeyse sıkıştırmasız (%1.5) koştu, durma 0 bu yüzden karşılaştırılamaz. Sonraki: 6768 ortamının kopyasıyla A kolu, durursa bayrakları ikiye bölerek ara (≤2 claude -p, izinle).
- K8: ucuz_alt.py combo'da 400 veriyordu (3 model de düşünmeyi zorunlu tutuyor, reasoning_effort "none" reddediliyor) → "low" + max_tokens 8000, test 3/3. Lisans görevi iki kolda koştu: OmniRoute gpt-6.1-sol 34.7k girdi/656 çıktı/15 sn (Claude 0) ↔ okuyucu sonnet 20.8k. Kör puan d4'te.
- claude -p: 2/2 kullanıldı. Kalan: K8 puan · K3/K7 · rapor sonu.

## Ara rapor d4 (14 Eki ~16:10)
Katalog: kullanılan [blender-uretim, animasyon-atolyesi, mevcut k1_dogrula/ab_r0e, ucuz_alt] · atlanan [katalog_ara (rutin, araç adları biliniyor), frontend-craft (plugin-only, d5)]
- VEKİL KAZASI kök nedeni: önceki d4 HEADROOM_CC_SWITCH_* (RECONCILE, PROXY_URL, CAPTURE_PATH, PIN_UPSTREAM) kopyaladı → 6769 uzlaştırıcıyı kendi koşup ~/.claude/settings.json'u kendine çevirdi. k1c.py artık CC_SWITCH_* hariç tutar + settings.json/cc-switch-upstream.json bayt koruması (değişirse geri yazar; bu koşuda değişmedi). vekil_dene: 6767/6768/doğrudan 401.
- K1b env-klon (38 HEADROOM_* ad, değer yazdırılmadı): 12 istek, durma 0, yer değişimi 0, ağırlıklı girdi 207.6k, 1.19 USD, 202 sn → 6768 ayarları durmayı üretmiyor; bölme gerekmedi. Ayar değişikliği önerisi yok.
- K9b effort medium gerçek mekanik adım (pytest 2 dosya + varlik_getir ara): cevap doğru (passed=6 sonuc=3), 3 tur, çıktı 485 (düşünme 26), 44 sn. d3 aynı-görev A/B −%16 ile birlikte → mekanik adımlarda medium AL (DEVAM-KURALI K9).
- K8 kör (X=claude sonnet alt ajan 20.8k Claude jetonu, Y=gpt-6.1-sol OmniRoute 0 Claude jetonu): ikisi 3/3 doğru karar, uydurma 0; X ELv2 alt-lisans yasağını atladı, Y Apache marka istisnasında daha kesin → Y ≥ X. Lisans taraması ucuz_alt'a gider.
- K3: skills/blender-uretim/varlik_getir.py (+ duzenle_b.py) API yol kaçışı koruması, tests/test_varlik_getir.py 3/3; canlı ara 3 kaynakta sonuç döndü. blender-uretim + animasyon-atolyesi SKILL.md güncellendi.
- claude -p: 2/2. Kalan: devir/token-2-devam.md (K7 site kiti, frontend-craft/web-sahne-desenleri, plugin kopyası + dist zip).

## d5 — K1c gerçek iş yükü (14 Eki ~16:45)
Katalog: kullanılan [k1_dogrula.kol (+effort parametresi), k1c klon env + global ayar koruması, durma_detay, bekle/arka] · atlanan [katalog_ara (rutin, araçlar biliniyor)]
- A (6768 klonu, .claude/token2/k1d.py, geçici klasör, 11 × 24–33 KB md + 1 PNG, opus low, 13 istek): durma 0/13 (%0), cw her adım ~10k ilerledi, yer değişimi 0, ağırlıklı 346.3k (g 26 · cw 166.8k · cr 1.32M · ç 1.0k), Headroom 13/13 istek sıkıştırdı, 188k/1.95M jeton (%9.6) çıkardı; 117 sn, 1.62 USD.
- Kök (headroom/cache/prefix_tracker.py:678-708 `_breakpoint_index`): kırılma noktası yalnız (a) mesaj ≥20 içerik bloğu VE (b) aynı sıradaki mesaj önceki istekte vardı ve kuyruğu yeniden yazıldıysa (RELATION_BLOCK_REWRITE_TAIL) geriye sabitlenir. Normal ekleme akışında son mesajın sırası önceki istek uzunluğuna eşit → her zaman `newest`. Yani iş yükü büyüklüğü durmayı tetiklemez; A/B ekleme akışında yapı gereği aynıdır. "Büyüt, tek tekrar" bu yüzden koşulmadı (claude -p 1/2).
- TELVE 4ed59962 adım 28 tam yeniden yazımı (cr 86k→6.6k, cw 93.7k): adım 27'den 8 sn sonra → TTL değil; önek ~6.6k'da değişmiş (Headroom/istemci geçmiş yeniden yazımı). Durma bölgesi 14–27'de adım arası 7–47 sn.
- TELVE'de kuyruk yeniden yazımını ne ürettiği (eşzamanlı oturumların izleyici anahtarı paylaşması mı, Headroom geçmiş sıkıştırması mı) bu oturumda kanıtlanamadı; üretim günlüğü debug düzeyinde değil ("anchored" 0 satır).
- KARAR: UYGULAMA — koşul (A durma ≥%30) sağlanmadı. Not: TELVE türü durmada B açıkça daha ucuz (kuyruk 1×/adım yerine 1.25× bir kez + 0.1×), B'nin en kötü durumu yeniden yazılan kuyrukta +%25 cw; ama tetikleyici yeniden üretilmeden ayar değişmez. Sonraki adım (Desktop kararı): 6767'de prefix_tracker debug günlüğü ya da k1_vekil izi ile gerçek bir Desktop oturumunda "anchored" olayını yakalamak.
- d4 kalanı: web-sahne-desenleri §4 tablosuna varlik_getir satırı (yalnız bu hunk commit'te; TELVE-R0d 2d bölümüne dokunulmadı). frontend-craft plugin-only (skills/ altında yok) → satır eklenemedi. Not: tools/varlik_indir.py (eski, Poly Haven/ambientCG CC0) skills/blender-uretim/varlik_getir.py ile örtüşüyor; eski silinmedi.
- Kapanış: 6769 kapalı (yalnız TIME_WAIT), vekil_dene 6767/6768/doğrudan 401; settings.json/cc-switch-upstream.json bayt koruması geri yazma gerektirmedi.
