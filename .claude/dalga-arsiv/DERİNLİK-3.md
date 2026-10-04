# DERİNLİK-3 PANEL DOĞRULUĞU
KARAR: sıra Y3 → Y1 → Y2 → Y7 → Y5 → Y4 → Y6; sığmayan KALAN'a. Tavan 50 çağrı, 45'te commit+push+DUR. Başlangıç suiti yok (fef94a5 yeşil), tam suit yalnız sonda.
Model 0 · gh istekleri arası ≥2 sn · ~/.claude yalnız okunur · değişiklik yalnız video motoru kodu/testleri/docs · eski test çelişirse DUR, sor.
Y1 Ön-doldurma ≠ Ömer kararı: Ömer hücresine yazılan ön-doldurma durum.json'da ayrıca saklanır. --yeniden'de hücre saklanan ön-doldurmayla aynıysa yeni öneriyle
  yenilenir; farklıysa (Ömer yazmış) korunur. Bu partide Ömer hiç hücre yazmadı; mevcut değerlerin hepsi ön-doldurma sayılır.
  Test: skill-creator eski ön-doldurma "ZATEN VAR", yeni öneri "UYARLA" → hücre yenilenir; elle yazılmış hücre korunur.
Y2 --yeniden eksik kapsamı tamamlar: "onceki"/"tamam" adaylarda model araştırması yok, ama Kapsam'da eksik çağrısız işler koşulur: güvenlik taraması
  (S5 seyrek dahil; ruflo 591 MB → seyrek), lisans API'si, son commit tarihi. Test.
Y3 S7 birleştirmesi --yeniden'de mevcut durum.json'a da uygulanır, gerçek aday adlarıyla (slug'da parantez kaybı dahil). Bu partide ruflo ×3,
  ECC ×2 (everything-claude-code-ecc + everything-claude-code; -gelistirme ayrı kalır), security-guidance ×2 tek satıra. Test gerçek panel adlarıyla.
Y4 Son commit tarihi kurulu olmayan her repo için de alınır (stop-slop, marketingskills, ui-ux-pro-max-skill, vercel-labs/skills, ruvnet/ruflo);
  sürüm numarasıyla kurulu plugin'de tag → commit → tarih (derinlik-3.md S3).
Y5 S8 (derinlik-3.md: aday işlevi kurulu skill/plugin açıklamalarında aranır, ad şart değil; en yakın 3 kurulu karşılık panelde "bizde benzer";
  CSV stil/palet+arama betiği → ui-ux-pro-max; depo geneli güvenlik taraması → security-assessment / Strix / gstack-cso) + kurulu kaynakların
  tamamı: installed_plugins + ~/.claude/skills + plugin skill dizinleri (yalnız OKUNUR). Test: nextlevelbuilder/ui-ux-pro-max-skill → kurulu
  ui-ux-pro-max (ZATEN VAR + güncellik); gstack → garrytan/gstack; paket içi security-review → ECC reposu.
Y6 S9 (derinlik-3.md): Prompt adayında metin neden alınmadı teşhis (altyazı mı, kare mi); düzeltilir; yine alınamazsa sebep Kapsam'da.
Y7 Kurulu fork: kurulu marketplace reposu için gh api repos/<repo>; fork ise source/parent son commit'i. Fork bayrağı yoksa video/karedeki sahip
  kurulu reponun sahibinden farklıysa aynı kontrol. Kapsam: "kaynak farklı: kurulu <repo> (son commit X) ↔ asıl <repo> (son commit Y)",
  öneri "UYARLA / kaynağa geç". Test: worldflowai/everything-claude-code (2026-01-23) ↔ affaan-m/ECC (2026-10-02).
Kanıt: docs/kurulumlar/parti/2026-10-03-short/panel.md + durum.json · derinlik-3.md · known_marketplaces.json 146-151 (ECC → worldflowai).
Kabul: her Y kırmızı-önce ayrı commit · eski test değişmez · tam suit (RAM ≥6 GB, ağır süreç yok) · gitleaks · git add <dosya> (parti/ ve .kos/ hariç)
  · arşiv .claude/dalga-arsiv/DERİNLİK-3.md · push · graphify update .
Ömer komutu sonda: video parti akil 2026-10-03-short --yeniden

## Durum
- Y3+Y1 ✓ (d327343 kırmızı, ortak · b9a845e yeşil) · video 557. Y3: parantez içi ad birebir eşse videolar arası tek aday (ruflo köprüsü);
  eski panel satırı slug'la _cesit(adlar) eşleşirse birleşik satıra iner, Ömer kararı taşınır. Y1: durum.json on_doldurma; kaydı yoksa
  mevcut hücreler ön-doldurma (ponytail notu). Yenilenen hücre yeni ön-doldurma kuralıyla (UYARLA için kural yok → boş, Ömer karar verir).
- tam suit 557·81·314·178·40·22 yeşil (cc-kopru ilk koşuda 178/178 ama çıkış 1: suit.mjs:46 işaretli canlı süreç 2, sonra çıkmış;
  tek başına yeniden koşu çıkış 0, canlı 0 → geçici) · RAM 9,9 GB
KALAN: Y2 → Y7 → Y5 → Y4 → Y6 (DERİNLİK-3 devamı; tanımlar yukarıda). Not: durum.json .kos/2026-10-03-short/ altında.
