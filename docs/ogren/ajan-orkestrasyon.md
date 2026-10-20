# ÖĞREN-3 (G2) — ajan-orkestrasyon + araştırma + bilim/diğer: karar ağacı, kart dizini, kombin

Kaynak: `docs/atlas/kart.jsonl` (A 149 kart, B 3369 betik kartı) · kanıt/kopya: `.kos/kopru/ogren/ozet-ajan-o3.jsonl`, `lab/ajan-orkestrasyon/kombin-d2.md`, `lab/arastirma/kombin-d2.md`.

## Karar ağacı (hangi durumda hangi araç)
1. Zor/çok alanlı iş, araç adı belirsiz → `plan-kur` (içinde `yetenek-getir`, TEK çağrı). Rutin tek alan: katalog çağrısı yok.
2. Plan/spec/görev listesi → planlama: `brainstorming` → `plan-kur` / `pln-prd-yazar` / `pln-mimari-plan`; kapsam kırpma `pln-kapsam-kesici`; sorgulama `interview-me`, `office-hours`.
3. Çok adımlı uygulama → orkestrasyon: `subagent-driven-development` (görev başına taze alt ajan, implementer'lar PARALEL DEĞİL) ya da `superpowers`/`is-akisi`; uçtan uca ürün akışı `gstack`/`feature-dev`.
4. Bağımsız ≥3 iş, ortak durum yok → `dispatching-parallel-agents` (tek yanıtta çoklu Agent); sınır RAM (`ajan-sira.tavan`=3, ESIK %82), skill'den değil.
5. Hangi ajan/model/skill → yönlendirme: `departman-*` müdürleri, `ajan-getir`/`ajan_katalog`, `model-sec`, `OmniRoute` (:free yol; Claude aboneliği OmniRoute'tan GEÇMEZ, ANTHROPIC_BASE_URL = headroom vekili 6767).
6. Denetim → inceleme: `verification-loop`, `plan-ceo-review`, `code-reviewer`, `pr-review-toolkit`, `departman-surec-inceleme`; kör denetçi her zaman ayrı alt ajan.
7. Kanca/koruma → `hook-development`, `hookify-rules`. Ajan tanımı → `agent-development`, `ajn-ajan-tanimi-yazar` (dar araç + ucuz model + kısa istem).
8. Bellek/devir → `ajn-ogrenilen-ders`, claude-mem, `devir/<görev>-devam.md`. İzleme → `olcum`, `model_olc`, `butce`.
9. Araştırma → WebSearch+WebFetch (alt ajanda MCP YOK); belge `context7` (mcporter, `MSYS_NO_PATHCONV=1`); makale `arxiv`; güvenlik taraması `skillspector scan --no-llm`.
10. Model merdiveni: betik/ücretsiz → Haiku → Sonnet (kart yazımı, hakem) → Opus (yalnız ayrışma son kararı).

## Standart: ajan topluluğu şablonu (3 bakış + kör denetçi)
1. Aynı soru tek cümle + ≤120 kelime yanıt istemi her bakışa.
2. Bakışlar: Claude + 2 FARKLI aileden :free (OmniRoute); aynı aileden iki model sayılmaz.
3. Eleştiri turu: diğer yanıtlar (≤900 kr) + "≤100 kelimede eleştir, son öneri".
4. 429/404/403 → model değiştirme yok, "sonuçsuz" yaz, bekleyip tek yeniden deneme (:free havuzu paylaşılınca 429 zincirlenir; aileleri aralıklı çağır).
5. Uzlaşma = oy sayımı; uyuşmazlık gerekçesiyle Claude kararlaştırır.
6. Kör denetçi/hakem: kartı yazmamış AYRI alt ajan (Agent aracı); tohum başı 2 hakem, ayrışan Y'yi kaynağa bakıp Claude karara bağlar. Mekanik doğrulanabilir alanda tek hakem yeter, öznelde 2.
7. Agent çağrısı sınıflandırıcıca reddedilirse istemi değiştirmeden bir kez yeniden dene; ikinci ret → sırala ya da oturum kendisi yapar.
8. Silme yasak; çağrı tavanı sayılır ve rapora yazılır (:free ücretli 0).

## Kombin kartları (gerçek mini koşu: lab/ajan-orkestrasyon/kombin-d2.md)
- K1 Desktop köprü yönetimi — ÇALIŞTI/KISMİ: `kontrol.py` → `ram_ust.py` → `sira_durum.py` → `sonuc_oz.py` → devir/*.md (toplam ~4.5 sn, ~2.5 KB). RAM 3 kez ölçülüyor (kontrol+sira_durum biri yeter). Desktop'ta: tek çağrı, MCP `durum`/`komut`. `ajan_sira.py` ARGV'yi import anında kurar (satır 19, cc_profil.kur("ajan")) → profil değişikliği runner YENİDEN BAŞLAYINCA etkin (Desktop yapar); salt-okuma kipi yok, kuyruk `ajan-sira.tsv/log/tavan`dan okunur. cc-kopru araçları (sunucu.mjs): komut · ajan · oturum · kaydet · katalog · oku · durum · oturum_ozeti.
- K2 Ajan topluluğu standardı — KISMİ: Claude + gemma + laguna bakışları geldi, nemotron 404, 3 eleştiri 429; uzlaşma "öznel 2, mekanik 1 hakem". Şablon yukarıda.
- K3 Ücretsiz alt adım — KISMİ: yoklama 4 :free modelden 1 canlı (laguna-s-2.1, 5 sn; gemma 429, inkling 403, nemotron 404/429); özet alt adımı kota yüzünden koşmadı (denenmedi). OmniRoute yolu Bearer ile doğrulandı. CC'de betik (ham yanıt bağlama girmez).
- K4 Uzun dalga — ÇALIŞTI (biçim): plan-kur/is-akisi → `.claude/dalga.md` (KARAR·kabul·durum ≤30 satır, kapanışta silinir) → ARA kayıt `devir/*-devam.md` (dalga durumundan KOPYA) → yeni oturum önce devir+dalga okur. Canlı devam denenmedi.
- K5 Paralel dağıtım — KISMİ: dispatching (paralel serbest) ↔ SDD (implementer paralel yasak) ayrımı = bağımsız üretim vs ortak depoya yazan implementer. Skill'de auto-mode ret kuralı YOK (boşluk).
- R1 web araştırma (ÇALIŞTI: WebSearch+WebFetch) · R2 context7 (KISMİ: resolve OK, query-docs `MSYS_NO_PATHCONV=1`) · R3 kaynak güvenilirliği/skillspector (KISMİ: ölçütler awesome-rehber:27, video-uygula:16-17; scan 0 bulgu 23.9 sn) · R4 Desktop yolu (denenmedi).
- Bilim/diğer kombinleri: ayrı mini koşu YAPILMADI (denenmedi; kartlar `ecc-ml-bilim-saglik-paket`, `davila7-/kdense-scientific-paket-*`, `arxiv`).

## Tuzaklar
- Kaynağı yalnız kayıt JSON/katalog satırı olan kalemde mekanizma adından tahmin edilmez → `kaynak yetersiz`. Komut alanı: skill/ajan `name:` satırı · MCP `command`/`url` · CLI usage satırı (betik `.claude/ogren3/komut.py`); kaynakta yoksa "belirsiz" (ajan_katalog, skill-ui, yukle12b).
- Zip kopyaları (departman-arastirma-ogrenme ×7) tek kanonik kart; sürüm farkı için `lab`/katalog hash'ine bak.
