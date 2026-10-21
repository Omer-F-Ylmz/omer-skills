# Kombo kataloğu — ÖĞREN 2. tur d1 (hepsi `aday`; ölçüm d2'de)
Kural: tek başına en iyi araçla A/B; kalite · token · süre · kullanışlılık dördünde de üstün değilse `gecersiz`. Makine okunur: `docs/atlas/kombo.jsonl`.
Aday sayısı: 32 · kategori içi: 27 · kategoriler arası: 5 · ★ = öncelikli (önceki ÖĞREN-2'de DENENMEDİ dalı).

## frontend-tasarim (5)
- **fe-referans-diff** — iş: referans siteden yeni sayfa tasarımı → kod
  - sıra: `playwright ref.mjs (headless ölçüm)` → `yon.mjs (3 yön PNG)` → `DESIGN.md (token+yerleşim)` → `hero.html` → `node diff.mjs hero.html <tur> (pixelmatch)`
  - rakip: /frontend-craft tek başına (referanssız doğrudan sayfa yazımı) · ölçüm: held-out: betikle seçilen, linear.app dışı bir referansın hero'su; kalite=diffPct, token=toplam, süre, kullanış=tur sayısı · not: kombin-1; pixeljury yargı adımı DENENMEDİ
- **fe-a11y-perf-kapisi** — iş: bitmiş sayfayı erişilebilirlik+hareket performansı kapısından geçirme
  - sıra: `playwright + @axe-core/playwright (wcag2a/aa)` → `CDP Performance.getMetrics 3 sn` → `lh.mjs Lighthouse` → `fixing-motion-performance`
  - rakip: Lighthouse tek başına · ölçüm: held-out: TELVE'den bir sayfa (kombin-3 yalnız küçük lab sayfasında denendi); kalite=ihlal+LayoutCount, token, süre, kullanış · not: kombin-3
- **fe-sahne-animasyon** ★ — iş: three.js sahnesi + scroll/giriş animasyonu
  - sıra: `esbuild build.mjs (three npm)` → `playwright run.mjs (WebGL renk örnekleme)` → `prefers-reduced-motion ölçümü` → `Lenis/Motion ya da R3F + motion/react`
  - rakip: gsap-frameworks skill tek başına · ölçüm: held-out: React'li ve React'siz iki mini sahne; kalite=reduced-motion davranışı doğru+ERR 0, token, süre, kullanış · not: kombin-2; React'li dal ve GSAP dalı DENENMEDİ
- **fe-desktop-referans-devri** ★ — iş: Desktop'un referansa bakıp CC'ye devri
  - sıra: `Desktop: Claude in Chrome / claude-design / Figma bakışı` → `bulguyu 10-15 satır metne indir` → `cc-kopru ajan/komut` → `CC: fe-referans-diff zinciri`
  - rakip: CC tek başına (yalnız ref.mjs ölçümü, görsel bakış yok) · ölçüm: held-out: aynı referans, iki kol; kalite=diffPct + estetik kör yargı, token (görüntü tokenı dahil), süre, kullanış · not: kombin-4 Desktop DENENMEDİ — Desktop araçları CC'den çağrılamaz
- **fe-pixeljury-yargi** ★ — iş: piksel diff'in ölçemediği tasarım kalitesi yargısı
  - sıra: `fe-referans-diff çıktısı (hero.html tur PNG)` → `pixeljury (claude-code + ollama qwen3.5:4b)` → `kendi bakış` → `düzelt→yeniden diff`
  - rakip: yalnız pixelmatch diffPct · ölçüm: held-out: 3 yön PNG'sinden betikle seçilmiş 2 çift; kalite=yargının kör hakemle uyumu, token, süre, kullanış · not: kombin-1 görsel yargı adımı DENENMEDİ

## ajan-orkestrasyon (4)
- **ao-kademe-yonlendirme** — iş: alt işi en ucuz yeterli modele atama
  - sıra: `python tools/ordu.py sinif "<iş>"` → `python tools/yonlendir.py sec <tür>` → `Agent (model alanı açık)` → `mekanik denetim` → `yonlendir.kaydet`
  - rakip: her alt işi Sonnet'e vermek · ölçüm: held-out: betikle üretilmiş 10 alt iş (sınıflama·özet·kod·test); kalite=kabul testi geçme, token/USD, süre, kullanış=yükseltme sayısı · not: ROUTER-1 başarı 12/12, USD −%30,4 (yonlendir.md) — taze ölçüm gerekir
- **ao-ucretsiz-havuz-hakem** — iş: toplu sınıflama/özet taslağı
  - sıra: `python tools/ucretsiz_havuz.py` → `mekanik denetim (birebir alıntı/şema)` → `Haiku (yalnız denetim düşerse)` → `Sonnet hakem`
  - rakip: Haiku tek başına · ölçüm: held-out: 40 kalemlik betikle seçilmiş özet işi; kalite=denetimden geçen oran, token(ücretli), süre, kullanış · not: yeni sağlayıcı aileleri kartı delta'da
- **ao-uzun-dalga** — iş: çok oturumlu iş
  - sıra: `plan-kur (tek katalog çağrısı)` → `.claude/dalga.md (KARAR·kabul·durum ≤30 satır)` → `devir/<görev>-devam.md ara kayıt` → `/clear + yeniden başlangıç`
  - rakip: plan-kur tek başına (dalga.md/devir olmadan) · ölçüm: held-out: aynı 3 oturumluk betik iş; kalite=kabul kriteri karşılanma, token(oturum başı yükleme), süre, kullanış · not: K4 (ajan-orkestrasyon kombin-d2)
- **ao-kopru-yonetimi** — iş: Desktop'tan köprü oturumlarını yönetme
  - sıra: `kontrol.py` → `ram_ust.py` → `sira_durum.py` → `sonuc_oz.py` → `devir/*.md`
  - rakip: kuyruk/log dosyalarını elle okuma · ölçüm: held-out: 3 köprü oturumu durum sorusu; kalite=doğru durum, token, süre, kullanış · not: K1

## video-medya (3)
- **vm-video-izle** — iş: video içeriğinden rapor
  - sıra: `yt-dlp <url>` → `ffmpeg kare çıkarma` → `/watch <url>` → `video rapor-denetle`
  - rakip: /watch tek başına · ölçüm: held-out: betikle seçilmiş 3 kısa video; kalite=rapor denetim geçme+olgu doğruluğu, token, süre, kullanış · not: mini koşu bu oturumda: ffmpeg 9.0.1, yt-dlp 2026.08.19 hazır
- **vm-blender-dekupaj** — iş: 3B model → web katmanı
  - sıra: `blender -b (Cycles 64x64 PNG + glb)` → `PIL LANCZOS 4x` → `rembg` → `katman.html` → `playwright headless` → `three GLTFLoader.parse`
  - rakip: Blender render tek başına · ölçüm: held-out: 2 betikli sahne; kalite=glb geçerli+dekupaj kenar hatası, token, süre, kullanış · not: kombin-5
- **vm-tam-sayfa-yakalama** — iş: uzun sayfanın tek görüntüsü + görsel QA
  - sıra: `playwright` → `stitched-full-page-capture` → `frontend-visual-qa`
  - rakip: playwright full_page=True · ölçüm: held-out: 3 uzun sayfa (lazy-load'lu); kalite=kayıp/çift bölge sayısı, token, süre, kullanış · not: stitched-full-page-capture ve frontend-visual-qa delta kartı

## test-qa (3)
- **tq-kirmizi-once** — iş: .NET'te kırmızı-önce test + kapsam
  - sıra: `writing-mstest-tests` → `run-tests (kırmızı→yeşil)` → `run-tests --collect` → `coverage-analysis`
  - rakip: dotnet test tek başına · ölçüm: held-out: betikle üretilmiş 3 küçük C# sınıfı + mutasyon (tutar > 50 → >=); kalite=mutasyonu yakalama, token, süre, kullanış · not: kombin-d1 (1)
- **tq-e2e-gorsel-regresyon** — iş: uçtan uca davranış + görsel regresyon
  - sıra: `playwright (python, headless) assert` → `ref.png` → `degisti.png` → `PIL ImageChops farkı`
  - rakip: playwright assert tek başına · ölçüm: held-out: 3 sayfada betikli CSS değişikliği; kalite=yakalanan değişiklik/yanlış alarm, token, süre, kullanış · not: kombin-d1 (2)
- **tq-desktop-kombin** ★ — iş: Desktop'tan test koşturup kapı kararı
  - sıra: `Desktop: sonuç okuma/karar` → `cc-kopru komut/ajan` → `CC: suite-kosucu ya da dotnet test` → `özet sayı`
  - rakip: CC'den doğrudan koşu · ölçüm: held-out: 7 suite koşusu, Desktop ve CC kolu; kalite=doğru kapı kararı, token, süre, kullanış · not: kombin-d1 (5) Desktop DENENMEDİ (yalnız varlık)

## guvenlik (1)
- **gv-sizinti-sast** — iş: değişiklik öncesi sır+kod güvenliği taraması
  - sıra: `gitleaks detect --no-git -s <yol> --redact --no-banner -f json -r <dosya>` → `semgrep scan --config auto <yol>` → `security-guidance` → `düzelt→yeniden tara`
  - rakip: semgrep tek başına · ölçüm: held-out: betikle tohumlanmış 6 zafiyet (3 sır, 3 kod) içeren repo kopyası; kalite=yakalama/yanlış alarm, token, süre, kullanış · not: mini koşu bu oturumda: gitleaks tools/ → 19 bulgu, 2,9 sn; çoğu test fixture

## veri-backend (4)
- **vb-ef-sorgu-optimizasyon** — iş: yavaş EF Core sorgusu
  - sıra: `dotnet-data:optimizing-ef-core-queries` → `dotnet test <csproj>` → `dotnet-aspnetcore:dotnet-webapi`
  - rakip: optimizing-ef-core-queries tek başına · ölçüm: held-out: betikle üretilmiş N+1'li küçük proje; kalite=sorgu sayısı düşüşü+test yeşil, token, süre, kullanış
- **vb-build-teshis** — iş: açıklaması belirsiz derleme hatası
  - sıra: `dotnet build /bl:{}` → `dotnet-msbuild:binlog-generation` → `dotnet-msbuild:binlog-failure-analysis`
  - rakip: konsol çıktısını okuma · ölçüm: held-out: betikle bozulmuş 3 csproj (zincirleme hata); kalite=kök neden bulma, token, süre, kullanış
- **vb-api-gozlemlenebilirlik** — iş: yeni uç nokta + izleme
  - sıra: `dotnet-aspnetcore:dotnet-webapi` → `agent-skills:observability-and-instrumentation` → `dotnet-aspnetcore:configuring-opentelemetry-dotnet`
  - rakip: dotnet-webapi tek başına · ölçüm: held-out: 2 uç nokta ekleme görevi; kalite=OTLP çıktısında iz/ölçüm var + test yeşil, token, süre, kullanış
- **vb-supabase-sorgu** — iş: Postgres şema/sorgu iyileştirme
  - sıra: `supabase:supabase` → `supabase:supabase-postgres-best-practices` → `EXPLAIN sonucu`
  - rakip: supabase:supabase tek başına · ölçüm: held-out: betikle üretilmiş yavaş sorgu seti (yerel Postgres); kalite=plan maliyeti düşüşü, token, süre, kullanış · not: yerel Postgres gerekir; yoksa ölçüm düşer

## arastirma (4)
- **ar-olgu-dogrulama** — iş: güncel olgu doğrulama
  - sıra: `WebSearch (allowed_domains)` → `WebFetch birincil kaynak` → `atıf`
  - rakip: WebSearch tek başına · ölçüm: held-out: 10 sürüme bağlı olgu sorusu; kalite=doğru+atıflı oran, token, süre, kullanış · not: R1
- **ar-kutuphane-dokuman** — iş: kütüphane API'si öğrenme
  - sıra: `context7 CLI (resolve → query-docs)` → `WebFetch yedek`
  - rakip: WebFetch tek başına · ölçüm: held-out: 10 güncel API sorusu; kalite=doğru kod, token, süre, kullanış · not: R2
- **ar-arac-degerlendirme** — iş: yeni araç/repo alıp almama kararı
  - sıra: `dört ölçüt (bakım·çift·izin·context)` → `SkillSpector --no-llm` → `lisans kontrolü` → `kurulum kapanışı`
  - rakip: README'yi elle okuma · ölçüm: held-out: 6 aday repo (2 zararlı tohumlu, 2 lisanssız); kalite=doğru karar, token, süre, kullanış · not: R3
- **ar-desktop-web-kopru** — iş: web + yerel kod birleşik araştırma
  - sıra: `Desktop WebSearch/WebFetch (yerleşik)` → `cc-kopru oku/katalog/ajan` → `CC dosya/sembol okuma`
  - rakip: yalnız Desktop web araması · ölçüm: held-out: 5 web+kod karışık soru; kalite=doğru, token, süre, kullanış · not: R4 — Desktop tarafı denenmedi

## token (3)
- **tk-kod-sorusu** — iş: kod tabanı sorusu
  - sıra: `python -I -S .kos/kopru/token-rea/sor2.py "<soru>"` → `graphify query "<soru>"` → `rg -n <desen>` → `Read dar satır aralığı`
  - rakip: rg/grep tek başına · ölçüm: held-out: betikle seçilmiş 15 kod sorusu (cevap dosyası bilinen); kalite=doğru dosya/sembol, token, süre, kullanış · not: mini koşu bu oturumda: sor2 1.111 B/1,96 sn · graphify 6.690 B/3,96 sn · rg 1.186 B/0,21 sn (aynı soru)
- **tk-log-okuma** — iş: büyük log/tarama çıktısı
  - sıra: `jev log|triage <dosya>` → `rtk (sıkıştırılmış komut çıktısı)` → `headroom_retrieve <hash>` → `Read dar aralık`
  - rakip: ham çıktıyı bağlama basmak · ölçüm: held-out: 3 gerçek CI/test logu; kalite=kök neden satırını bulma, token, süre, kullanış
- **tk-model-merdiveni** — iş: tekrarlı toplu iş maliyeti
  - sıra: `python tools/yonlendir.py sec <tür>` → `tools/ucretsiz_havuz.py` → `FORCE_PROMPT_CACHING_5M=1 claude -p` → `python tools/ccusage_kiyas.py`
  - rakip: her işte Sonnet medium · ölçüm: held-out: 20 işlik betik seti; kalite=kabul geçme, token/USD, süre, kullanış · not: ccusage kartı kaynak_yetersiz olabilir (PATH'te yok)

## kategoriler-arasi (5)
- **x-kod-guvenlik-test** — iş: değişiklik: bul → güvenlik incele → kırmızı test → düzelt
  - sıra: `graphify query "<soru>"` → `semgrep scan --config auto <yol>` → `security-reviewer` → `writing-mstest-tests` → `run-tests`
  - rakip: security-reviewer tek başına · ölçüm: held-out: tohumlu zafiyetli küçük API; kalite=zafiyet kapatma+regresyon testi, token, süre, kullanış
- **x-tasarim-erisilebilirlik-sizinti** — iş: site yayın öncesi tam kapı
  - sıra: `fe-referans-diff` → `fe-a11y-perf-kapisi` → `gitleaks detect --no-git -s <yol>`
  - rakip: yalnız Lighthouse · ölçüm: held-out: TELVE sayfası + tohumlu sır; kalite=yakalanan sorun, token, süre, kullanış
- **x-video-site** — iş: videodaki arayüzden sayfa
  - sıra: `/watch <url>` → `DESIGN.md taslağı` → `fe-referans-diff` → `frontend-visual-qa`
  - rakip: yalnız /watch + doğrudan kodlama · ölçüm: held-out: 2 kısa ürün videosu; kalite=diffPct vs. video karesi, token, süre, kullanış
- **x-arastirma-ajan** — iş: doküman araştırması → özet → karar
  - sıra: `context7 CLI` → `python tools/ordu.py sinif "<iş>"` → `okuyucu alt ajan (salt-okuma)` → `derleme (ana oturum)`
  - rakip: ana oturumda doğrudan okuma · ölçüm: held-out: 4 doküman araştırma görevi; kalite=doğru özet, ana bağlam tokenı, süre, kullanış
- **x-token-ajan-log** — iş: büyük CI/test logu → kök neden
  - sıra: `jev log|triage <dosya>` → `okuyucu alt ajan` → `headroom_retrieve <hash>` → `özet satırı ana bağlama`
  - rakip: ana oturumda log okuma · ölçüm: held-out: 3 gerçek log; kalite=kök neden, ana bağlam tokenı, süre, kullanış

## d1 düzenek mini koşuları (en ucuz 3 aday)
- tk-kod-sorusu: aynı soru ("ucretsiz havuz saglayici dagitimi nasil calisir") → sor2 1.111 B / 1,96 sn; graphify query 6.690 B / 3,96 sn; rg 1.186 B / 0,21 sn. Düzenek çalışıyor; kalite (doğru dosya) d2'de.
- gv-sizinti-sast: gitleaks (WinGet) `tools/` taraması 2,6 sn, 19 bulgu (çoğu test fixture: omniroute.test.mjs, .pytest_cache); semgrep kurulu, `--version` 5 sn. Düzenek çalışıyor; yakalama oranı d2'de tohumlu repoyla.
- vm-video-izle: ffmpeg 9.0.1 ve yt-dlp 2026.08.19 PATH'te; video indirilmedi (ağ/süre), zincir komutları var.

## d2 A/B ölçümü (betikli, model yok; `.kos/kopru/ogren/tur2_d2_olc.py`, ham: `.claude/ogren-tur2-d2/olc.json`)
Kural: dört eksende (kalite · token · süre · kullanış) tek başına en iyi araçtan üstün değilse `gecersiz`. Ölçülen 3 aday HEPSİ `gecersiz`.
- **tk-kod-sorusu → gecersiz**: 10 held-out soru (tools/*.py docstring ilk cümlesi, cevap=dosya). Kombo (sor2 → graphify) 8/10 · 8.804 tok · 30,7 sn · 14 adım; `git grep` 9/10 · 6.417 tok · 1,0 sn · 10 adım.
- **gv-sizinti-sast → gecersiz**: tohumlu 6 zafiyet. gitleaks+semgrep 4/6 · 912 tok · 16,2 sn · 2 komut; semgrep tek başına 3/6 · 581 tok · 15,2 sn · 1 komut. Kalite üstün, diğer üçü geride. Yanlış alarm 0/0. gitleaks AKIA…EXAMPLE'ı allowlist'ler; `yaml.load`'ı semgrep auto da kaçırdı.
- **tq-e2e-gorsel-regresyon → gecersiz**: 3 sayfada betikli CSS değişikliği. assert+ImageChops 3/3 · 0,38 sn · 3 adım; assert 1/3 · 0,19 sn · 1 adım. Token ölçülmedi (model yok) → üstünlük kanıtlanamadı.
- Ölçülemeyen ★ adaylar `aday` kalır (uydurma ölçüm yok): fe-desktop-referans-devri · tq-desktop-kombin (Desktop araçları CC'den çağrılamaz), fe-pixeljury-yargi · fe-sahne-animasyon (model üretimi + görüntü yargısı gerekir; bütçe dışı).
- Güvenlik kategorisine 2 aday eklendi (3'e tamamlandı): gv-skill-tedarik-zinciri · gv-diff-onkapisi (`aday`).
