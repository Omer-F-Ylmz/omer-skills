# ÖĞREN-1 — Token araçları ustalık + kombin kartları (d3, 15 Eki)

Kaynak: `.kos/kopru/ogren/ozet-token-v2.jsonl` (32 kalem, v2 şema, Claude jetonu 0; v1: ozet-token.jsonl) + gerçek mini koşular `.claude/ogren1/mini/` (d1 + `d2.tsv`).
Özet doğruluğu (5 kalem: rtk · headroom · qmd · jev · mem-search, 4 alan = 20 alan): model hatası 3/20 = %15, üçü de `mekanizma` alanında (headroom/qmd/jev "önbellek" denmiş; gerçekte sıkıştırma · dizin · delegasyon). Ayrıca mem-search kaynak eşlemesi yanlış (claude-mem-cowork bulut sürümü; kurulu olan yerel claude-mem 13.31) → özet sadık ama yanlış belgeye (d3'te yollar.tsv düzeltildi).

**Özet hattı v2 (d3; tüm ÖĞREN kategorilerinin ortak hattı)** — `python -X utf8 .claude/ogren1/ozet.py` → `.kos/kopru/ogren/ozet-token-v2.jsonl` (kaynak listesi `.claude/ogren1/yollar.tsv`: ad · tür · yol; çıktı varsa kalem atlanır → kaldığı yerden sürer). Kollar: OmniRoute `openrouter/nvidia/nemotron-3-super-120b-a12b:free` → ollama `gpt-oss:20b-cloud` → `qwen3.5:4b`; tavan 90 çağrı (32 kalem = 40 çağrı).
Şema: `{ad, ne_yapar, mekanizma: [1-2 değer], mekanizma_gerekce, kanit, ne_zaman, komut, girdi_cikti, sinirlar, cakistigi_arac}`; `mekanizma` kapalı liste: sıkıştırma · önbellek · bağlam dışı depolama · delegasyon · özetleme · tur azaltma · yönlendirme · ölçüm (istemde tek cümlelik tanımlarıyla). `kanit` = belgeden birebir alıntı; `gecerli()` liste dışı değeri ve belgede bulunmayan alıntıyı (boşluk/tırnak/markdown normalize) reddeder → sonraki kol. Başka kategori için: `yollar.tsv` + `CIKTI` adı değişir, şema aynı kalır.

## Ustalık kartları (ölçülmüş)

**headroom (proxy + MCP retrieve)** — sıkıştırma + araç şeması erteleme (istek anında).
- Ne zaman: hep açık (ANTHROPIC_BASE_URL). Sıkışık çıktıda `headroom_retrieve(hash)`.
- Ölçüm: opus isteklerinde `saved_tool_schema` ≈21.2k/istek; sonnet alt ajanda 0. Bugün %26.9.
- Tuzak: Read/Bash çıktısı ~200 kelimeyi aşınca sıkışır → dar Read; yoksa her okuma +1 retrieve turu.

**A6 `--tools` (cc_profil "araclar", KALIR — Desktop 01:14)** — araç tanımı hiç serileşmez.
- Kapı: kalite aynı (24 passed · tsv 83, araç hatası yok). count_token 53.6k→33.5k.
- Çakışma: headroom `saved_tool_schema` ile ikisi üst üste kazanç vermez (gerçek API iki kol 22 319 ↔ 22 319); A6 yedek katman — vekil düşerse/doğrudan çağrıda ~20k/tur korur.
- Not: köprü oturumları `--strict-mcp-config` boş → claude-mem / context-mode MCP yok (tasarım gereği, A6 değil). Yerine HTTP: aşağıdaki claude-mem kartı.

**rtk (Bash önişleme, hook)** — komut çıktısı süzme.
- Ölçüm: toplam 43.7M token %82.1. `git log -30` −%55 · `pytest -q` −%82 · `rtk pytest -v` 2388→18 B.
- `rtk read` varsayılan 0 kazanç (2730→2729 B); `rtk read -l aggressive` 2730→386 B (−%86, yalnız imzalar) — düzenleme için değil, yapı görmek için.
- Tuzak: `git log --stat`, büyük untracked `git status` 0 kazanç; çıktı bozuk/boşsa `rtk proxy <cmd>` (bu oturumda 1 kez gerekti).
- Çakışma: rtk çıktısı headroom'da ikinci kez sıkışır (`rtk recall` + `hash=` aynı sonuçta) — zararsız; işlenecek çıktı dosyaya.

**graphify_sor.py** (`.kos/kopru/graphify_sor.py "<sembol>"`) — birebir etiket araması.
- Ölçüm: "env_oku" 260 B / 0.3 s ↔ `graphify query` aynı soru 25 552 B / 2.5 s (−%99).
- Ne zaman: sembol/dosya adı biliniyorsa İLK. Adı yoksa git grep, o da yoksa query --budget 400'e düşer.

**graphify query/explain/path** — bağlam dışı graf + bütçeli BFS. 3.0 s, 16–25 KB.
- Tuzak: graf 48.9k düğüm, video/haber düğümleriyle kirli → genel Türkçe soruda alakasız başlangıç. Temizlik ayrı iş.

**harita** (`.kos/kopru/harita/*.md`) — elle damıtılmış proje haritası, 4.8 KB toplam. İlk yön bulma; graf yerine.

**qmd** — yerel BM25 (+vektör `qmd embed` sonrası). `qmd search "zip_denetle" -n 3` <1 s, isabetli.
- Tuzak: embed yok (RAM %71.6 ≥ %70 eşiği, bu oturumda da yapılmadı) → `qmd query` henüz anlamsal değil.

**claude-mem** (yerel worker 127.0.0.1:37777, 13.31) — bağlam dışı oturum hafızası.
- Köprüde MCP yok → `curl -s "127.0.0.1:37777/api/search?query=<q>&limit=5"` 1.4 KB / 0.1 s (indeks tablosu) → `get_observations` ile yalnız seçilen id.
- Tuzak: `/api/timeline` depth parametrelerini yok sayıyor → 37.8 KB (152 kayıt); köprüde timeline yerine search. Vektör arama kapalı (chroma: uvx worker PATH'te yok, `degraded`) → yalnız FTS.

**jev ilgili / log / triage** — delegasyon (ucuz model dosya/satır seçer). Yeşil log `jev log` 74 B, 0 model çağrısı.
- Tuzak: `yollar` dizin değil dosya ister (dizinde PermissionError).

**ucuz_alt.py** (`tools/ucuz_alt.py istem.md cikti.md [bağlam…]`) — Claude-dışı combo `cc-yedek-dis`; stdout'a yalnız yol+jeton (126 B). Mini: 1400 girdi → 74 çıktı, 3 s.
- Tuzak: combo :free değil, kredi yiyebilir (bugün `gpt-6.1-sol`). Combo DEĞİŞMEZ (OmniRoute ayarı Ömer'in; limit yedeği). ÖĞREN-* ve :free kurallı işte ucuz_alt KULLANILMAZ → yalnız `ozet.py` / açık `:free` model adı (Desktop 15 Eki 01:27).

**OmniRoute ücretsiz kolları** — `ucretsiz-groq` (gpt-oss-120b) · `openrouter/...:free` · ollama yerel.
- Groq kök neden (d2, kanıt `mini/groq-kok.txt`): KIRIK DEĞİL. Python-urllib UA → Cloudflare 1010 → 403 (combo'da 502). `user-agent: curl/8.4` ile `ucretsiz-groq` ve `groq/openai/gpt-oss-120b` 200. Llama 3.3/4-scout 400 = OmniRoute `/v1/models` statik katalog eski (Groq canlı katalogda yok).
- Görsel yargı: `nemotron-3-nano-omni-30b-a3b-reasoning:free` 49.7 KB PNG → 289 girdi jetonu, 27 s (`gorsel_mini.py`). Tuzak: düşünme jetonu `max_tokens`'u yer → ≥3000 ver.

**headroom-compress** (zip skill, `scripts/compress.py dosya --oran 0.3`) — yapı koruyan yerel sıkıştırma. ozet-token.jsonl 35 747→16 441 B (−%54), 0.2 s, model yok. Ne zaman: Desktop'a büyük JSON/kod yapıştırmadan önce.

**omni-cache / omni-compression / omni-context-rtk** (OmniRoute yönetim API) — yanıt önbelleği · istem sıkıştırma · RTK filtresi.
- Tuzak: `OMNIROUTE_KEY` yönetim API'sinde `AUTH_001 Invalid management token` → yönetim jetonu ayrı; CLI kullan.
**cli-compression / cli-cost-usage / cli-contexts** — `omniroute compression|usage analytics|context-eng show`; CLI ~/.omniroute/.env'i kendisi yükler, 0.7–6.5 s.

**Ölçüm araçları** — `rtk gain` (rtk kazancı) · `headroom` savings_events.jsonl · `claude-usage` · `tools/token_olc.py olc --gun N` (ağırlıklı: girdi×1, cache okuma×0.1) · `cagri_sayac` hook ("çağrı N/45 · alt M" her Bash sonrası) · ctx-stats (yalnız etkileşimli CC, MCP).
- Tuzak: `claude-usage today` `scan` sonrası da "No usage recorded today" (tarih/dizin uyumsuzluğu) → güncel ölçüm için token_olc. `token_olc`/`model_sec` alt komut ister; `model_sec --help` KeyError ile düşer.

**İstem skill'leri (koşu yok, davranış kuralı)** — strategic-compact (mantıksal sınırda /compact) · context-engineering · token-budget-advisor (derinlik seçimi, ±%15) · full-output-enforcement (yer tutucu yasak) · content-hash-cache-pattern (SHA-256 anahtarlı dosya önbelleği deseni) · cost-tracking · vrm-headroom-geri-cagirma · vrm-maliyet-denetci. Köprüde slash komut kapalı (`--disable-slash-commands`); etkileşimli CC'de geçerli.

**context-mode** (ctx_batch_execute / ctx_execute_file) — sandbox'ta işle, yalnız türetilen sonuç bağlama. Köprüde YOK (strict MCP); etkileşimli CC'de ham Bash yerine. Eşdeğeri köprüde: çıktıyı dosyaya yaz → Grep -n / python özet.

## Kombin kartları (iş türü → zincir · ölçülmüş)
1. **Uzun köprü oturumu**: A6 + headroom (sabit bağlam) → `cagri_sayac` 45'te devir dosyası → geçmiş için claude-mem HTTP search (MCP değil) → toplu metin `ozet.py`/ucuz_alt. Bu oturumda doğrulandı: hook sayacı, sıkışma işaretleri, MCP yokluğu.
2. **Büyük repo keşfi**: `harita` (4.8 KB) → `graphify_sor` sembol (260 B) → dar Read (~20 satır). Genel soru: `qmd search` (belge) / graphify explain. Kazanç: query'ye göre −%99.
3. **Test/log ağır iş**: `rtk pytest` (2388→18 B) → kırmızıysa log dosyaya → `jev log|triage` (yeşil 74 B, 0 model) → kanıt satırı Read.
4. **Video/medya, toplu metin**: kaynak metin hiç Claude'a girmez → `ozet.py` sabit şema (:free, kalem ~15 s) → Claude yalnız özet; `mekanizma` alanını ölçümle düzelt; 5 kalemde özgün kontrol.
5. **Görsel yargı**: PNG → nemotron-nano-omni :free (289 jeton, 27 s, curl UA) → Claude yalnız hüküm satırı; şüpheli karede Read ile görüntü.
6. **Desktop köprü kontrol döngüsü**: `durum_ozet.py <görev>` (3.9 KB) → devir dosyası dar Read → claude-mem search → Desktop'ın kendi araçları (cc-kopru oku iskelet/sembol/aralık · headroom_retrieve · rtk-desktop `rtk read -l aggressive` · graphify-desktop graphify_sor). Büyük yapıştırma öncesi headroom-compress.
Çakışma matrisi: rtk↔headroom çift sıkıştırma (zararsız) · A6↔headroom şema (yedek katman) · graphify query↔graphify_sor (sembolde sor) · qmd↔graphify (belge↔kod) · ucuz_alt↔ozet.py (:free kural varsa ozet.py) · claude-mem MCP↔HTTP (köprüde HTTP).

## Karar ağacı
1. Kod/sembol → `harita` → `graphify_sor` → (yoksa) `graphify explain|path` → dar Read.
2. Belge/skill/rapor metni → `qmd search` (BM25) → dar Read.
3. Büyük komut çıktısı → rtk otomatik; işlenecekse dosyaya + Grep -n; bozuksa `rtk proxy`.
4. Dosya yapısı (düzenleme değil) → `rtk read -l aggressive`.
5. Geçmiş karar/oturum → claude-mem (CC: mem-search MCP · köprü: HTTP `/api/search`) → `get_observations([id])`.
6. Çok dosyalı keşif, test/log → alt ajan (okuyucu); köprüde alt ajan yoksa jev log|triage.
7. Toplu metin özeti → `ozet.py` (:free → ollama); ucuz_alt yalnız ücret kuralı OLMAYAN işte (ÖĞREN-* değil).
8. Görsel → nemotron-nano-omni :free, curl UA, max_tokens ≥3000.
9. Ölçüm → rtk gain · headroom savings · token_olc (claude-usage değil).
