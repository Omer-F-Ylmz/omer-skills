# SKILL-MODE-1 — Code Mode mantığı skill/plugin'lere (Desktop yürütür, Ömer 24 Eki 01:40)

Nihai kurallar: hiçbir skill kaybolmaz/silinmez/budanmaz · kalite düşmez, %98–100 kapısı · token en az · öğrenme 0 token (ücretsiz modeller) · her adım 2. beyne · Desktop + CC + claude.ai birlikte.

## Faz 0 — taban ölçüm (BİTTİ 01:45, skill_mode_olc.py → envanter.tsv)
- 7944 SKILL.md (açık 7871), 417 kök; aynı ad tekrarı 2375 (paket içi kopyalar)
- tam ad+açıklama listesi ~575k token (sığması imkânsız) · yalnız ad listesi ~41k token
- gövde medyan 6.2k kar, p90 19k, max 292k; >20k: 709, >8k: 3225
- betikli 960 · references'lı 2878 · ≥3 kod bloğu olup betiksiz 2843
- Mevcut altyapı (sıfırdan başlanmaz): tools/katalog_ara.py (BM25), zorunlu_arac.py ön uçuş, departman-* yönlendirici, context-profil-* ölçümleri, kullanim-defteri.json

## Faz 1 — KAPANDI 24 Eki (SKILL-MODE-2) — her-sey-ara (arama aracı; Ömer 24 Eki: yalnız skill değil HER ŞEY)
- katalog_ara üstüne TEK DİZİN: 7944 skill (paket içi dahil) + plugin + MCP (araç adlarıyla) + CLI + ajan + repo + kütüphane (omer-kutuphaneler) + site/referans adresleri (site-liste.md, kaynak-tam.tsv, tum-linkler.tsv) + indirilen araçlar + MASAÜSTÜ UYGULAMALARI (Ömer SS 24 Eki 02:01: Aurora, Laragon, Radmin VPN, Obsidian, Headroom, BrowserOS, ComfyUI Desktop, PromptHub, OpenPencil, OpenFic, NoteGen, Cascadeur, AutoClip Desktop, Skill UI, LDPlayer 9 + LDMultiPlayer, DBX, Alpemix, Roblox Studio, Blender 5.2, Telegram, XXMI/WWMI/SRMI/ZZMI, TLauncher; masaüstü klasörleri BlenderOl-*, araclar, REA-Code, kids-shorts, dans, bekci-kanit) + claude.ai bağlayıcıları + ücretsiz model API'leri + hook/komut/stil + venv/npm paketleri + varlık/şablonlar; kanonik ad + kopyaları eşle (silme yok). Faz 0 sayımı bu türler için de alınır
- (Nihai 32f, 24 Eki) Sorgu → TAM İLGİLİ KÜME (sınırsız; 3 bin ilgiliyse 3 bin) + çok yönlüler (REA, replika, SS→kod) her zaman. Kopyalar kanonik tekile indirgenir (silinmez). Modele ad dökümü değil, iş adımına göre gruplanmış KULLANIM PLANI gider (adım → skill'ler → betik/gövde ne zaman açılır); BM25 + ücretsiz embedding (bulut ücretsiz; Ollama son çare)
- Erişim: cc-kopru MCP aracı + Code Mode zinciri + CC skill'i + claude.ai skill'i
- TETİK SETİ: her kanonik skill için 3 sorgu (ücretsiz modelle üretilir), %20 ayrılmış test; kapı: ilgili kümenin TAMAMINI bulma (recall) ≥ %98 + çok yönlüler %100 + plan token'ı ölçülür (en düşük)

### Faz 1 durum (24 Eki 10:35)
- Katalog 4580 → 8277 kayıt (yetenek-tam.jsonl); tetik 200 skill × 3 sorgu (100 yeni eklenen)
- recall-taban (katalog_ara BM25): tam katalog @5 %67.5 · @20 %76 · @40 %80.2 → hedef %98'in çok altında
- her_sey_ara.py: önbellekli ters dizin BM25 (katalog_ara skoru aynı, sorgu başına tam tarama yok) + çok dilli yoğun vektör (fastembed paraphrase-multilingual-MiniLM-L12-v2) + RRF k=60; @80 de ölçülür (gerçek aday listesi 80 + tür tabanı)
- Code Mode eşlemesi: M1 tembel şema = yalnız ad·tür·kısa iş döner, gövde istenince · M2 ara sonuç sandbox'ta = arama/sıralama betikte, modele yalnız liste · M3 sözcük skoru = BM25 · M4 arayüz imzası = `cagri` alanı · M5 kısa istem = gruplu kullanım planı
- 11:20 ölçüm (olc_cevir.py, %80 ayar / %20 ayrılmış test, skill bazında): karma @80 ayar %93.8 test %95.0 · karma+en (sorgu ücretsiz modelle EN yeniden yazım + anahtar sözcük, 4 liste RRF) @80 ayar %97.5 test %95.0 · @120 %97.7/%95.8. Çeviri kapsamı 492/600 (eksikler tamamlanıyor). mpnet/e5-large deneyi RAM %89 yüzünden durduruldu; RAM düşünce yalnız mpnet.
- 14:40 KAPANDI (SKILL-MODE-2): karma+en+soz3 @80 ayar %99.4 / ayrılmış test %100 (@20 %96.7/%99.2). Kazanç sırası: çeviri hizası onarımı (105/600 kaymıştı, cevir_duzelt.py) → ad×2/etiket/açıklama sözcük kolu (etiket.json 7002 kayıt, etiket_uret.py) → karma+en. Bağlama: gorev-skill-mode-3.md
- Sonraki: kaçan analizi (kacan_analiz.py) → eş anlam/tetik zenginleştirme → yeniden ölçüm; %98 kapısı geçmeden katalog_ara değiştirilmez
- 25 Eki (SKILL-MODE-3) BAĞLANDI: katalog_ara.karma_aday (CLI aday yolu) + zorunlu_arac.araclar BM25 dolgusu karma_ara.ara'yı kullanır (EN çeviri önbellekli+kosinüs kapılı, havuz kapalı → çevirisiz karma, dizin yok → BM25). Dizin canlı katalogla eşitlendi (esitle.py: tam 8280→8524, vek/bm25), etiket 7002→7588. olc3 @80 ayar %99.4 / test %100. katalog_kanca (her istemde aday) BM25'te bırakıldı (fastembed yükü).
