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
