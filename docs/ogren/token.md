# ÖĞREN-1 — Token araçları ustalık + kombin kartları (d1 taslak, 15 Eki)

Kaynak: `.kos/kopru/ogren/ozet-token.jsonl` (ücretsiz model özeti, nemotron-3-super :free) + bu oturumdaki gerçek mini koşular (`.claude/ogren1/mini/`).
Özet hattı: 32 kalem, 32 çağrı (tavan 90), 0 hata, kalem başına ~15 s, Claude jetonu 0. Doğruluk (mekanik, 5 kalem: rtk · headroom-compress · mem-search · strategic-compact · ucuz_alt): `komut` alanındaki tanımlayıcıların hepsi özgün metinde var, uydurma komut 0/5 (mem-search alanına düzyazı karışmış). Anlamsal karşılaştırma d2'de.
Kombin mini koşu (test/log ağır iş): `rtk pytest -v` 2388→18 B · yeşil log'da `jev log` 74 B, 0 model çağrısı (yerel süzgeç önce) → zincir: rtk pytest → kırmızıysa log dosyaya → `jev log|triage` → yalnız kanıt satırı Read.
d1 durumu: ölçülen kartlar aşağıda; özet doğruluk kontrolü (5 kalem), kalan kartlar, kombin mini koşuları ve skill/zip güncellemesi d2'de.

## Ustalık kartları (ölçülmüş)

**headroom (proxy + MCP retrieve)** — mekanizma: sıkıştırma + araç şeması erteleme (proxy, istek anında).
- Ne zaman: her zaman açık (ANTHROPIC_BASE_URL). Elle iş yok; sıkışık çıktıda `headroom_retrieve(hash)`.
- Ölçüm: opus isteklerinde `saved_tool_schema` ≈21.2k/istek (savings_events.jsonl); sonnet alt ajan isteklerinde 0. Bugün %26.9.
- Tuzak: Read/Bash çıktısı ~200 kelimeyi aşınca sıkışır → dar Read aralığı, yoksa her okuma +1 retrieve turu.
- Birleşim: A6 `--tools` ile ÇAKIŞIR — kullanılmayan şemaları zaten ertelediği için `--tools` gerçek API'de +0 (kapı: iki kol 22 319 ↔ 22 319).

**rtk (Bash önişleme)** — mekanizma: komut çıktısı sıkıştırma (hook ile otomatik `rtk <cmd>`).
- Ölçüm: toplam 43.7M token, %82.1 (`rtk gain`). `git log -30` 8383→3766 B (−%55); `pytest -q` 101→18 B (−%82).
- Tuzak: `git log --stat` 0 kazanç (geçiş); `git status` büyük untracked listede 19.3k→19.3k (0). Bu durumlarda çıktıyı dosyaya yaz + Grep.
- Birleşim: rtk çıktısı headroom'da İKİNCİ kez sıkışır (aynı Bash sonucunda `rtk recall` + `words compressed … hash` birlikte görüldü) — token için zararsız, ama işlenecek çıktı dosyaya.

**A6 `--tools` (cc_profil "araclar")** — mekanizma: araç tanımı hiç serileşmez.
- Kapı (15 Eki): kalite aynı (24 passed · tsv 83, araç hatası yok). Gerçek API kazancı headroom açıkken 0; headroom kapalıyken sigorta (count_tokens 53.6k→33.5k).

**graphify query** — mekanizma: bağlam dışı depolama (graf) + bütçeli BFS.
- Ölçüm: 3.0 s, 16.6 KB; varsayılan ~2000 token bütçede 81 düğümden 38'i.
- Tuzak: graf 48 921 düğüm ve video/haber düğümleriyle kirli → genel sorguda başlangıç düğümleri alakasız ("Slack helps Box…"). Sembol adıyla `graphify explain`/`path` ya da `context_filter` kullan.

**qmd (yerel belge arama)** — mekanizma: bağlam dışı dizin (BM25; vektör için `qmd embed`).
- Durum: 0 dosyaydı → bu oturumda `omer-skills` (skills/**/*.md) + `omer-docs` (docs/**/*.md) koleksiyonları eklendi. `qmd search "zip_denetle" -n 3` <1 s, isabetli (kurulum-6c-denetim.md %92).
- Tuzak: `qmd embed` yapılmadı (3974 hash vektörsüz) → `qmd query`/vsearch henüz anlamsal değil; RAM'e bakarak d2.

**jev ilgili** — mekanizma: delegasyon (ucuz model dosya seçer).
- Tuzak: `yollar` dosya ister, dizin verince `PermissionError` (rc 1). Önce Glob/Grep ile dosya listesi, sonra jev.

## Karar ağacı (taslak)
1. Kod/sembol sorusu → `graphify explain|path` (genel `query` değil) → dar Read.
2. Belge/skill/rapor metni arama → `qmd search` (BM25) → dar Read.
3. Büyük komut çıktısı → rtk otomatik; işlenecekse dosyaya yaz + Grep -n / ctx_execute_file.
4. Geçmiş karar/oturum → claude-mem `mem-search` / `get_observations([id])`.
5. Çok dosyalı keşif, test/log → alt ajan (okuyucu); yalnız özet döner.
6. Toplu metin özeti → OmniRoute :free / ollama (Claude dışı) → Claude yalnız özeti okur.
