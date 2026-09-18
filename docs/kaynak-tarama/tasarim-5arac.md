# Tasarım kaynakları taraması, 18 Eyl — 3 kaynak · kurulum yok · SkillSpector v2.11.2 --no-llm

## 1 senlindesign/taste-skill — ELE
- bakım: 344★, archived=false, son push 2026-07-07 · lisans YOK (license=null)
- çift: amaç frontend-craft REF moduyla ve daha önce ELE edilen design-dna ile aynı (siteden token çıkarma)
- farklı olan tek şey: canlı siteyi Playwright MCP ile açıp DOM'dan `getComputedStyle` ile ölçüyor; REF ise statik PNG'yi k-means ile ölçüyor. Doğrulanmadı.
- izin: `@playwright/mcp@latest` sürümü sabitlenmemiş, Chromium indiriyor; CLAUDE.md/.cursor/GEMINI.md dosyalarına yazıyor · context: SKILL ~5.4k token, tam akış ~15.8k
- SkillSpector: 90/100 CRITICAL "DO NOT INSTALL"; 5 HIGH (AS1 agent-config dizinine erişim, SKILL.md:19), 9 MEDIUM

## 2 billhector/design-skills — ELE
- bakım: archived=true, son push 2026-04-10, 4★ · lisans MIT
- içerik: 2 skill. design-extractor (Firecrawl ile site tarayıp Tailwind v4 @theme üretir) ve design-auditor (token tablosu, WCAG kontrast, renk körlüğü raporu)
- çift: ~%50 (ikisi de impeccable extract/audit ve frontend-craft REF/audit.mjs ile kısmi örtüşüyor). Örtüşmeyen kısımlar: @theme çıktısı ve renk körlüğü simülasyonu.
- izin: extractor Firecrawl ister (ağ, büyük olasılıkla ücretli API anahtarı); auditor yalnız dosya okur · context: iki SKILL.md toplam ~11.7k token (yalnız açıklamalar ~170)
- SkillSpector: 65/100 HIGH "DO NOT INSTALL"; 2 HIGH (P2 gizli talimat, şablon yorumu olabilir), 11 MEDIUM (sürümü sabitlenmemiş `npx firecrawl`)

## 3 vercel.com/design/guidelines + vercel-labs/agent-skills web-design-guidelines — A-B (kuralları al, skill'i kurma)
- kurallar: 129 kural, 8 bölüm. Interactions 28 · Content 24 · Forms 19 · Performance 16 · Copywriting 14 · Design 11 · Animations 10 · Layout 7. A11y ayrı bölüm değil, bölümlere dağılmış (~17-35 madde).
- skill: agent-skills 31k★, son push 2026-08-28, lisans YOK. SKILL ~318 token; kuralları çalışırken WebFetch ile raw.githubusercontent'ten çekiyor (ağ bağımlı). SkillSpector: LOW, 0 güvenlik bulgusu.
- kural kaynağı web-interface-guidelines MIT lisanslı → kurallar uyarlanabilir
- impeccable farkı: audit.md ve harden.md a11y/perf konusunu kavramsal olarak kapsıyor. ~70-80/129 madde karşılıksız: URL-as-state, yapıştırma engelleme, autocomplete, kaydedilmemiş değişiklik uyarısı, optik hizalama, Copywriting bölümünün tamamı.
- frontend-craft Bölüm 4 kabul kriterine aday 5 kural (hepsi makineyle kontrol edilebilir):
  1. mobilde `<input>` font-size ≥16px (iOS otomatik zoom yapmasın)
  2. `<meta viewport>` içinde `maximum-scale=1` / `user-scalable=no` yok
  3. form alanlarında uygun `autocomplete` değeri var (email/name/tel…)
  4. dokunma hedefi ≥24px, mobilde ≥44px (bbox ölçümü)
  5. submit düğmesi istek sürerken disabled (çift gönderim yok, puppeteer tıklama testi)
