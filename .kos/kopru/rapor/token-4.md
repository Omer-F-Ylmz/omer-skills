# TOKEN-4 — araç katmanı

## d1 ara (14 Eki ~21:55) — claude -p 0/6, alt ajan 0
- A0 UYGULANDI: `.claude/token4/a0.py` (10 sn) → docs/kutuphane/olcum/token-4-arac.tsv. Bugün (1 gün, tüm projeler):
  - RTK: tüm zaman 43.4M kurtarıldı (%82.4); 1 günde Bash 2651/10489 rtk'lı; kaçak 1013 komut ≈189k token (ls -la 114, grep -n 123, git add 204, wc -l 37, tail -c 124). rtk grep 8372 komut %25.6, rtk read %19.8 (en düşük oranlı en büyük iki kalem).
  - Headroom: 305.6M kurtarıldı (%31.1, 10216 istek). **Durma 1098/5321 adım (%20.6), önbelleksiz 12.3M token** (görevdeki ~%5 tahmini bugün tutmuyor).
  - claude-mem: 657 enjeksiyon, blok medyan 6.3k kar.
  - Kullanım (çağrı · dönüş kar.): graphify 103 · 132k; ucuz_alt/Gemini 182 · 121k; cc_profil 88; context-mode 59 · 170k; bekle.py 43; cc-kopru oku 2; qmd 1; mem-search 1; headroom retrieve 1; smart-explore 0; headroom-compress 0; strategic-compact 1; Agent Reach 1.
- A2 kök (`.claude/token4/durma.py`): durmanın 5.6M'i (%46) **claude-mem gözlemcisi** — 407 tek adımlık haiku oturumu, 407/407 cw=0 cr=0 (medyan 14.6k, p90 22.7k, en çok 67.6k). Kalan 6.6M ana opus oturumları (omer-skills 329/2081, TELVE 195/1404, alt ajan 61/361): desen cr sabit, cw=0, kuyruk 6–8k önbelleksiz, 406 durma bir durmanın ardından.
  - Mekanizma (kaynak okundu, ölçülmedi): headroom/cache/prefix_tracker.py `HEADROOM_STABLE_BOUNDARY_BREAKPOINT` (varsayılan AÇIK) — ≥20 bloklu mesajda kuyruk yeniden yazılınca kesme noktası kararlı önek sonuna taşınıyor → yazım yok, kuyruk her adım tam fiyat.
  - Kapı gerekli: ayrı portta ikinci vekil (env =0, yalnız çocuğun --settings'inde; global ayar/ANTHROPIC_BASE_URL değişmez) ile ≤2 claude -p A/B. Kuyruk her adım gerçekten değişiyorsa =0 daha pahalı olur (1.25 yazım boşa).
- A3: damga `new Date()` (context-generator.cjs Ye()), ayar/ortam değişkeni yok. TOKEN-3'te gösterildi: msg1 istemden sonra geliyor, farklı istemli oturumlarda paylaşılmıyor; aynı istemli ölçüm koşuları zaten CLAUDE_MEM_INTERNAL=1 kullanıyor → damgayı sabitlemenin kazancı ≈0. Gözlemci girdi tavanı (OBSERVER_MAX_CONVERSATION_CHARS 400k) düşürülürse: 30k token tavanı −%3, 20k −%8 → küçük. Gözlemcide asıl kaldıraç önbellek ya da sağlayıcı (CLAUDE_MEM_PROVIDER=gemini: 6.2M token/gün Anthropic'ten çıkar; gözlem kalitesi ölçülmedi) → yalnız öneri.
- A1/A6 UYGULANDI: is-akisi §3 "Token araç sırası" 3 ölçümlü satır (konum → graphify/Grep; rtk'sız kalıplar; ev/AppData/`..` ls YASAK: komut başı 28–114 sn, girdi 0.9–2.8M) + aynı yasak DEVAM-KURALI.md 1. satırda. pytest test_is_akisi 1/1.
- Yapılmadı: A4, A5, kapı (4 temsilî iş), claude.ai zip, onay betiği (kapısı geçen öneri yok). Önce/sonra tablosu: yalnız "önce" var.

## d2 ara (14 Eki ~23:15) — claude -p 3/6, alt ajan 0
- A2 kapı (hr_ab.py, vekiller artık TEK TEK + RAM <%75 bekçisi): A (BREAKPOINT=0) n=2 ağırlıklı 81.1k / 68.2k, B (varsayılan) n=1 81.9k; **iki kolda durma 0** — 4 adımlık görev ≥20 bloklu mesaj üretmiyor, mekanizma tetiklenmedi → karar YOK, ayar değişmedi. 3. koşu RAM %75'te bekçiyle durdu. vekil_dene 401 ✓.
- A3 (mem_kiyas.py): d1 koşusu 20/20 boş (OmniRoute dva/gemini 500, yargıç oc/nemotron 403). Düzeltme: Gemini claude-mem'in kendi yolu (doğrudan API, gemini-flash-latest), yargıç cc-yedek-dis. Gemini API **429** (bugünkü kota dolu; video Gemini-önce hattıyla aynı anahtar) → CLAUDE_MEM_PROVIDER=gemini REDDEDİLDİ (kota çakışması gözlemci kaybı demek), kalite kıyası yapılamadı.
- A1: `rtk rewrite` ls -la / grep -n / git add / wc -l / cd&& zincirlerini doğru çeviriyor; cc_profil kancaları koruyor → kaçakların kaynağı kanca dışı (bulunamadı). `git ls-files | wc -l`, `python -c` desteksiz.
- Yapılmadı: A4, A5, kapı (4 iş), zip, onay betiği (kapısı geçen öneri yok), önce/sonra tablosu.

## d3 ara (14 Eki ~23:55) — claude -p 3/6, alt ajan 0
- A3 MODELSİZ YOL YOK (kanıtlı): "gözlemci" oturumları (`~/.claude/projects/C--Users-pc--claude-mem-observer-sessions`, sdk-ts haiku) claude-mem'in alan yoğunlaştırıcısı — >16k kar. her araç alanı için tek seferlik "Condense the tool payload" çağrısı (Oo=16e3 sabit). Son 200 oturum: 184 tek adım, ilk mesaj medyan 29.6k kar., oturumlar arası ortak önek medyan 510 kar. (~130 token < haiku 4096 asgari) → önbellek yazımı geri okunmaz, cw=0 doğru. Tek ayar CLAUDE_MEM_OBSERVER_CONTEXT_WINDOW eşiği yalnız DÜŞÜRÜR (min(16000, pencere×0.4)) → daha çok çağrı. Groq kolu denenmedi (d4; kör yargıçlı).
- A1 KÖK: rtk discover kaçakları transkript tabanlı, kanca yeniden yazımı transkripte düşmez → 1013 kaçağın çoğu yanlış pozitif (14 Eki rtk 4764 koşu, transkriptte önekli 2651). Bugünkü %42.1 düşüşün kökü (history.db): `git show <ref>:<yol>` 85 komut 1.58M → 1.58M (passthrough, telve-r1 1.44M) + `git status --short` 358 komut ort. 780 token passthrough. UYGULANDI: is-akisi §3 L44 (yasak + yol), arsiv.md satır 44; test_is_akisi 1/1.
- Yapılmadı: A2 (koşul: ≤1 claude -p, RAM <%75), A4, A5, 4 iş kapısı, zip, onay --kuru.

## d4 ara (15 Eki ~00:25) — claude -p 6/6 (bütçe doldu), alt ajan 0
- A6 sabit bağlam (`.claude/token4/a6.py`: kayıt vekili, count_tokens kalem farkı; başlık diske yazılmaz) → token-4-a6.tsv: ajan profili tur başı **53 618 token**; araç tanımları 36.5k (%68: Workflow 8.1k, PowerShell 3.7k, DesignSync 3.3k, Monitor 2.9k), claude-mem bağlamı 4.8k, MEMORY.md 1.9k, sistem istemi 1.9k, context-mode 1.8k, global CLAUDE.md 1.4k, superpowers 1.3k, harita 1.2k, ponytail 0.9k.
- Kısma kanıtı: 13 araç 7 günde 2803 oturumda 11'i 0 kez, Workflow 4, ListAgents 1. permissions.deny tanımı DÜŞÜRMÜYOR (53 615, -deny.tsv); `--tools` izin listesi düşürüyor: **33 478 (−%37.6)** (-tools.tsv).
- UYGULANDI (etkisiz, onaya bağlı): cc_profil `araclar` → `--tools` (test 20/20); onay/token_4_uygula.py --kuru "eklenecek" (test 1/1). Kalite kapısı (köprü işi ±) claude -p bütçesi bittiği için koşulmadı.
