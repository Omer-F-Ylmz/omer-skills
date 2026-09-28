# Parti D — ilk 15'in 11-13'ü (2026-09-28)

Hat: SERTİFİKA-1 (paket → tarama → toplu → on → araştırıcı → bizde → katman --yeniden → teknik → brief). Karar kaynağı: docs/kurulumlar/kayit.jsonl satır 222-254 (33 satır). Toplu: docs/video-tarama/2026-09-28-toplu-3.md · rapor: docs/kurulumlar/2026-09-28-uygula.md Koşu 7 · brief: docs/kurulumlar/yeniden/parti-d-brief.md. Etiket: `yeniden:parti-d`. 30 aday: 28 aday.md + 2 ayrıştırma.

## fCc97Rv-60w (Fable 5.1 vs Fable 5 · bitmemiş siteyi tek promptla tamamlatma)
- karar dağılımı: ÖĞREN 6 · ZATEN VAR 1 · departman frontend 5 / verimlilik 2
- T0: ipucu 3 · teknik 3 — awwwards-seviyesi ÖĞREN (bilgi/awwwards.md kartına destek) · sektöre-göre-scroll ÖĞREN (tasarım olgusu, kural değil) · kritik-iş-için-pahalı-model ÇİFT (omer-kurallar:15) · Fable 5.1/5 ÖĞREN (model olgusu → bilgi/model-effort-claude-code.md) · mercury ÖĞREN (referans site)
- Site/UI: `video teknik` UYARLA 7 (bekleyen/teknik-*) · ÖĞREN 0
- prompt kalıbı: klasik-prompt-şablonu (anatomi dolu, 4 kalıp: 2 OLASI TEKRAR · 1 UYARLA → bekleyen/prompt-awwwards-seviyesinde-yap-… · kart bilgi/klasik-prompt-şablonu.md)
- ÜRETİLEBİLİR: 0 · ayrıştırma: 1 ("4 ayrı Skill (önceki videodan)" → 39IlNR-P3-Q'nun 4 kurulu iskeleti; ayrı aday yok)
- araştırıcı: yok (prompt adayı; metin `video on --rapor 2026-09-28-fCc97Rv-60w.md` on.md'den, ~563 token)
- güvenlik ön taraması: yok (repo yok)

## v-vRYtvWDYs (Claude Code token/limit ayarları · context-mode)
- karar dağılımı: ÖĞREN 3 · ZATEN VAR 3 · KUR 2 (bekleyen kural, ONAY) · ARACA ÖZEL 1 · DENE 1 · departman verimlilik 5 / surec-ajan-arac 5
- T0: ipucu 5 · iş akışı 2 · teknik 1 — max-thinking-tokens ve compact-clear ONAY kural (bekleyen/kural-*.md) · iş-türüne-göre-model toplu ÇİFT (omer-kurallar:15) · kullanılmayan-MCP toplu ÇİFT · claude-mcp-list ARACA ÖZEL (yerleşik CLI) · autocompact ÖĞREN (kart birleşti) · subagent-model ÇELİŞKİ (CLAUDE:14, alt ajan sonnet) → eklenmedi · context-rot ÖĞREN
- Site/UI: teknik 0/0 (raporda site/UI yok)
- prompt kalıbı: yok
- ÜRETİLEBİLİR: 0 · ayrıştırma: 1 ("plugin marketplace add / install" → context-mode kurulum adımı)
- context-mode: DENE → docs/denemeler/context-mode-sandbox-context-saving.md (koşulmaz; kurulum ONAY; takas tablosu + Headroom/RTK çakışma notu: kısmen aynı çıktılar, sıra RTK → context-mode → Headroom, iki PreToolUse Bash yeniden yazıcısı riski). Geçmiş: önce ELENDİ (RTK çifti) + 24 Eyl K4 DENE; bu koşu da DENE.
- everything-claude-code: kurulu → ZATEN VAR (videoda içerik anlatılmıyor, yeni kullanım yok)
- araştırıcı: context-mode 71k token · 11 çağrı · tam (DEVAM-3) · Elastic-2.0 (MIT/Apache değil; koşullar DENE dosyasında)
- güvenlik ön taraması: `video on --repo mksglu/context-mode` → SkillSpector koşmadı (MCP)

## 39IlNR-P3-Q (Prompt değil skill · 4 skill + Seedance referans videosu ile scroll sitesi)
- karar dağılımı: ÖĞREN 7 · ZATEN VAR 6 · KUR 2 (bekleyen kural, ONAY) · ARACA ÖZEL 1 · departman frontend 10 / surec-ajan-arac 5 / verimlilik 1
- kurulu 4 araç (frontend-design · taste-skill · scroll-craft · design-dna): ZATEN VAR + yeni kullanım ÖĞREN 4 (dörtlü yığın · animasyon düzeyi · referans videodan scroll geçişi · referans video analizi); klon/araştırıcı yok
- T0: ipucu 7 · teknik 1 — skill-hatırlatma ve en-fazla-10-skill ONAY kural · ekran-görüntüsü-fix-this ÇİFT (omer-kurallar:16) · responsive K4 ZATEN VAR (kalıp:27, p 0.82) · seedance ARACA ÖZEL · güçlü-model ÖĞREN (model kartı) · pear.no ÖĞREN (referans site)
- Site/UI: `video teknik` ÖĞREN 4 · UYARLA 2
- prompt kalıbı: scroll-site-promptu (ekrandaki prompt, 8:47; anatomi dolu, 3 kalıp: 1 OLASI TEKRAR) · kart bilgi/scroll-site-promptu.md
- ÜRETİLEBİLİR: 0 · ayrıştırma: 0
- araştırıcı: yok · scroll-site-promptu `arastirma: yarım` (raporda tür=prompt satırı yok → on.md prompt metni boş; alanlar rapor Bölümler 8:47'den)
- güvenlik ön taraması: yok (kurulu araçlar; `video on` ZATEN VAR yolu klonlamaz)

## OLASI TEKRAR (0.4–0.6, Desktop'ta karar)
- 3: klasik-prompt-şablonu ↔ DESIGN.md (frontend-craft:15) p 0.45 · klasik-prompt-şablonu ↔ kalıp:12 p 0.50 · scroll-site-promptu ↔ kalıp:27 p 0.57 → docs/kurulumlar/bekleyen/olasi-*.md. Karara bağlanmadı.

## T0 şüpheli sınıflamalar
- max-thinking-tokens ONAY kural: davranış kuralı değil settings.json env ayarı (olgu/araca özel olmalıydı).
- compact-clear ONAY kural: global CLAUDE.md "/clear dalga başında, /compact içinde" satırıyla kısmen çift; katman çift bulmadı.
- mercury-referans-site ve sektöre-göre-scroll → scroll-reveal kartına birleşti; context-rot → caveman-kural-maliyeti kartına destek (yanlış eşleşme şüphesi).
- claude-mcp-list tarama raporunda CLI; aday.md'de ipucu yazıldı (yerleşik komut, kurulum yok) → ARACA ÖZEL.

## Ölçüm
- araştırıcı: bu dalga 0 (context-mode DEVAM-3'te 71k · 11 çağrı · tam) · yarım 1/3 prompt/kurulu dışı aday (scroll-site-promptu, ana ajan).
- Jev: bizde ≤62 · katman ≤202 (tavan 350; katman sayı basmadı, üst sınır tavanlardan) · claude -p 0 · web 0.
- rapor-denetle: 3 tarama raporu + 8 aday (context-mode · 2 prompt · 5 kurulu) GEÇTİ; 21 T0 girdisi tarama raporu sayılıp 8 yapısal hata veriyor (Parti C T0 dosyası da aynı) → denetim hedefi değil.

## Kalan (Ömer)
- ONAY kural 4: bekleyen/kural-{max-thinking-tokens-ayarı, compact-clear-karar-kuralı, skill-hatırlatmasını-prompt-a-yazma, en-fazla-10-skill}.md → `video kural-onay <slug>`.
- context-mode DENE: kurulum ONAY'ı + deneme koşusu (≤4 koşu).
- OLASI TEKRAR 3: Desktop incelemesi.
