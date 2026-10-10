# Repo desenleri (REPO-ÖĞREN-1, 10 Eki 2026)

Kaynak: yalnız yerel dosyalar. Sayılar `.claude/repo_env*.py` envanterinden (407 satır: `plugins/cache`, `marketplaces`, `skills`, `.kos/kurulum-tarama/klon`; ~380'i skill/ajan/hook içerir). Not: cache'te aynı repo birkaç adla görünür (`example-skills`=`claude-api`=`discernment-nudge`, `hyperframes`=`core-skills`, `superpowers`=`skills`) — sayılar tekilleştirilmedi. Derin okunanlar: ecc, octo, gstack, superpowers, mattpocock, context-mode, impeccable, frontend-design, ui-ux-pro-max, hyperframes, marketingskills, claude-mem. Doğrulanamayan: rtk, headroom (yalnız hook), baoyu (cache'te ayrı satır çıkmadı) — yorum yok.

Ölçüler hakkında: "açıklama" = SKILL.md frontmatter `description` karakteri; ">400L" = 400 satırı aşan SKILL.md sayısı; satır sayıları medyan.

## (a) Repo başına özet

**ecc** (1027 skill, 307 ajan, 448 komut; ort. açıklama 192 kr; 259 skill >400 satır; yalnız 16'sında references/)
- İyi: GateGuard "gerçek kanıt iste" fikri (önce önemli bilgiyi topla, sonra düzenle); 7 Stop + 9 PreToolUse hook ile otomatik kalite kapısı; dile özgü reviewer/build-resolver ajan ayrımı.
- Kötü: katalog devasa (aynı işi yapan çok reviewer), her oturumda ~38 hook kaydı, uzun SKILL.md'ler (259 tanesi >400 satır), lazy-load yok → bağlam şişmesi.
- Bizde: GateGuard'ı olduğu gibi değil, "düzenlemeden önce 3 gerçek" kuralı olarak departman-* skill'lerine yaz; ecc'den ajan kopyalama.

**octo** (120 skill, 69 ajan, 109 komut; 46 skill >400 satır; 18 hook olay türü, ~38 kayıt; SessionStart'ta 9 hook)
- İyi: persona/droid ayrımı, "yalnız kullanıcı Octopus başlatırsa" yetki cümlesi (ajan açıklamasında).
- Kötü: en çok hook yükü; `hooks/telemetry-webhook.sh` curl ile dışarı POST eder — ama yalnız `OCTOPUS_WEBHOOK_URL` tanımlıysa (tanımsızsa sessiz çıkar); yani risk "env set edilirse" ile sınırlı. Her olayda hook çalıştırma gecikmesi.
- Bizde: hook sayısı bütçesi koy (aşağıda #2); env değişkenini asla tanımlama (zaten tanımsız, kontrol et).

**gstack** (54 iç içe skill; kök SKILL.md 232 satır "router"; ~70 bin/ betiği)
- İyi: tek yönlendirici kök skill + alt skill'ler (ad-yalnız yükleme mantığı); `bin/` altında deterministik betikler (karar günlüğü, diff-scope, context-bill → ölçüm).
- Kötü: `gstack-telemetry-sync` yerel olayları Supabase'e yollar (onay işaretine bağlı, "egress receipt" ile fail-closed — iyi tasarlanmış ama yine de dışa veri); çok sayıda profil/brain-sync betiği = bakım yükü.
- Bizde: router + `bin/` desenini al; telemetry bileşenini asla çalıştırma.

**superpowers** (15 skill, ort. açıklama 153 kr; yalnız 1 hook: SessionStart)
- İyi: açıklama "Use when …" ile yalnız TETİKLEME koşulu; süreç skill'leri (brainstorming, systematic-debugging, TDD) sert kapı koyar; hook yükü minimum.
- Kötü: TDD skill'i 330 satır (referansa bölünmemiş); `using-superpowers` her oturum enjekte edilir ve "%1 ihtimal bile varsa çağır" zorlaması gereksiz skill çağrısı → jeton.
- Bizde: "Use when" açıklama kalıbı + sert doğrulama kapıları al; zorunlu-çağrı cümlesini alma.

**mattpocock** (38 skill, medyan 75 satır, ort. açıklama 142 kr, tdd 38 satır)
- İyi: en yalın yazım: kısa SKILL.md, tek amaç, kısa açıklama. Token/kalite oranı bu setin en iyisi.
- Kötü: references/ yok; derin konular için kaynak ayrımı eksik (zaten kısa olduğu için sorun değil).
- Bizde: skill boyut hedefi için ölçüt: medyan ≤80 satır (aşağıda #1).

**context-mode** (11 skill, 9 PreToolUse hook, `ctx_*` sandbox araçları)
- İyi: büyük çıktıyı sandbox'ta işleyip yalnız özeti bağlama koymak = en güçlü jeton azaltıcı; indeksle + FTS5 ara.
- Kötü: her araç çağrısında hook çalışır (9 PreToolUse); bazı oturumlarda "[hook hata]" gürültüsü; talimat bloğu her oturum başında büyük (bu oturumda da görüldü).
- Bizde: "ham çıktı bağlama girmez" ilkesini departman-* skill'lerine yaz (tek komut = özet).

**impeccable** (SKILL.md 86 satır; reference/ + scripts/ + 4 ajan; hooks.json var)
- İyi: kısa SKILL.md + `reference/` + betikler + ayrı ajanlar (asset-producer, finish-reviewer): doğrulama ayrı ajanda.
- Kötü: açıklama 895 karakter — tüm komut adlarını sayıyor (bağlama her zaman girer).
- Bizde: finish-reviewer desenini (tasarım sözleşmesine karşı bitiş incelemesi) frontend-craft'a al; açıklamayı bu kadar uzatma.

**frontend-design / ui-ux-pro-max / taste-skill** (Anthropic frontend-design 71 satır; ui-ux-pro-max SKILL.md 739 satır; taste-skill en uzunu 1465 satır, 5 skill >400)
- İyi: frontend-design kısa ve estetik yön sorusu soruyor; ui-ux-pro-max veri tabanı tabanlı (BM25) öneri.
- Kötü: ui-ux-pro-max ve taste-skill çok uzun, birbirleriyle ve impeccable ile çakışıyor (tipografi/renk kuralları dörde bölünmüş).
- Bizde: CLAUDE.md'deki öncelik zinciri (frontend-craft > impeccable > ui-ux-pro-max > taste) doğru; uzun olanları lazy-load yap (aşağıda #4).

**hyperframes** (40 skill, 22'sinde references/, medyan 154, en uzun 1204 satır; "Mandatory entry point" kök skill)
- İyi: kök giriş skill'i + alt skill'ler + references/; tek tetikleyici.
- Kötü: açıklama ort. 510 kr; en uzun 3 skill >400 satır; cache'te iki adla yinelenir.
- Bizde: kök-giriş + alt-skill yapısını video-tarama/video-uygula için kullan (zaten benzer).

**marketingskills** (50 skill, 46'sında references/, ort. açıklama 765 kr, 13 skill >400 satır)
- İyi: references/ kullanımı en yüksek (46/50); skill içinde ürün bağlamı dosyası önce okutuluyor.
- Kötü: açıklamalar çok uzun (765 kr × 50 = ~9.6k token sadece listede).
- Bizde: referans ayırma oranını al; açıklamayı 200 kr'ın altında tut.

**claude-mem** (42 skill; 8 olay türünde hook; yerel DB)
- İyi: gözlem özeti + `get_observations` ile kademeli ayrıntı (3 katmanlı açılım); hooks yalnız yerel.
- Kötü: her oturumda büyük bağlam enjeksiyonu (bu oturumda ~1.5k token "recent context"); SessionStart ×2; park/kuyruk karmaşası (hafızada kayıtlı).
- Bizde: "önce indeks (ID+başlık), sonra tek tek getir" deseni (aşağıda #3).

**agent-skills (addy)** (25 skill, 4 ajan, 9 komut; medyan 311 satır; 1'inde references/)
- İyi: yaşam döngüsü komutları (spec→plan→build→test→review→ship) net; ajanlar (code-reviewer, security-auditor, test-engineer, web-performance-auditor) tek boyutlu.
- Kötü: skill'ler uzun ve references/ yok; superpowers ile "plan/review/debug" kümesinde çakışır.
- Bizde: 5 boyutlu inceleme listesini (doğruluk/okunabilirlik/mimari/güvenlik/performans) departman-surec-inceleme'ye al.

**expo** (24 skill, 15'inde references/, medyan 176) — iyi: alan bilgisi references/'ta, SKILL.md kısa yönlendirme. Kötü: yalnız Expo işine yarar. Bizde: ek bir şey yok, desen kataloğunda.

**anthropics/claude-code + plugins-official + skill-creator** (skill-creator 485 satır ×19, her biri references/ ile; 57 ajan; `example-skills` 100 skill, 15 >400 satır)
- İyi: skill-creator'ın "betik + eval + ajan" döngüsü; resmi plugin'lerde `hooks.json` güvenlik/değişim denetimi.
- Kötü: `claude-api` 100 skill kataloğu açıklama yükü; cache kopyaları yinelenir.
- Bizde: skill-creator'ın tetik-testi fikrini al (run_eval Windows'ta bozuk — tek seferlik `claude -p` betiği).

**Global ~/.claude/skills** (405 doğrudan SKILL.md; yalnız açıklamalar toplam ≈126k kr ≈ 31.5k token; 664 skill >400 satır; 263'ünde references/)
- İyi: references/'lı skill sayısı yüksek.
- Kötü: tam yükleme olursa listenin tek başına ~31k token tutması; çoğu oturumda kullanılmaz.
- Bizde: gerçek maliyet `claude -p /context` ile ölçülmeli (CC listeyi kısaltıyor olabilir — varsayım, doğrulanmadı).

## (b) En iyi desenler kataloğu

| Desen | Repo | Neden iyi | Bizim skill'lere uygulanışı |
|---|---|---|---|
| 1. "Use when …" yalnız tetik koşulu açıklaması | superpowers, mattpocock | Açıklama kısa (142–153 kr), yanlış tetik azalır | departman-* ve video-* açıklamaları 125–217 kr (zaten iyi); "Kullan:" kalıbına çevir, iş özetini gövdeye taşı |
| 2. İlerlemeli açılım (kısa SKILL + references/) | marketingskills, expo, hyperframes | 46/50, 15/24, 22/40 oranında references/; gövde bağlama girmez | departman-frontend (59L), video-uygula (105L), web-sahne-desenleri (127L) için 60 satırı aşan bölümleri references/'a taşı |
| 3. Üç katmanlı geri getirme (indeks → özet → tam) | claude-mem, headroom | İlk katman birkaç token | video-tarama kayıt.jsonl okumasında: önce `jev` indeksi, sonra tek rapor |
| 4. Çıktıyı sandbox'ta özetle | context-mode | En büyük jeton tasarrufu | Tüm "rapor/log" adımlarını `jev log|triage` ile; skill'e "ham çıktı yazdırma" cümlesi |
| 5. Kök yönlendirici + alt skill | gstack, hyperframes | Tek girişle tembel yükleme | departman-* zaten 15 küçük skill; ek kök yönlendirici `omer-kutuphaneler` (66L) olarak kalsın, açıklaması liste olmasın |
| 6. Kanıt-zorlayıcı kapı | ecc GateGuard | "Emin misin?" yerine somut gerçek ister | Düzenleme öncesi: etkilenen çağıranlar + test + şema listesi (departman-test-qa) |
| 7. Bitiş incelemesi ayrı ajanda | impeccable finish-reviewer, addy code-reviewer | Yazanın dışında bir göz | frontend-craft Bölüm 6: ayrı `okuyucu` alt ajan, sözleşme + ekran görüntüsü karşılaştırması |
| 8. Sert süreç kapıları (brainstorm→plan→TDD→doğrula) | superpowers | Kalite sapması azalır | CLAUDE.md zaten var; kapıya "kırmızı görüldü" kanıt satırı ekle |
| 9. Betikle deterministik adım | gstack bin/, skill-creator | Model yerine betik = ucuz ve tekrarlanabilir | video-tarama `rapor-denetle` gibi; yeni: skill-boyut ve açıklama-uzunluk lint betiği |
| 10. Tek amaçlı kısa skill | mattpocock tdd (38L) | Token/kalite oranı en iyi | 100 satırı aşan her skill için "bölünebilir mi?" kontrolü |

## (c) Düzeltilecek kötü yanlar

| Sorun | Etki | Önerilen düzeltme | Ölçüm yolu | Kim |
|---|---|---|---|---|
| 1. ~/.claude/skills'te 405 skill, açıklamalar ≈31k token | Jeton (her oturum olası) | Kullanılmayan skill'leri plugin kapsamına al / name-only moda geçir (silme yok, devre dışı) | `claude -p /context` önce/sonra | Ömer ayarı |
| 2. octo (~38 hook kaydı, 9 SessionStart) ve ecc (~24 kayıt) birlikte açık | Sürtünme + gecikme + "hook hata" gürültüsü | Aynı anda yalnız birini açık tut; SessionStart hook sayısı ≤3 hedefi | Oturum başlangıç süresi + hata satırı sayısı | Ömer ayarı |
| 3. Büyük açıklamalar (impeccable 895, marketing 765, logo-design 1016) | Jeton | Açıklamayı ≤250 kr kısalt (kopya kuralı: sahip değiliz → yerel sarmalayıcıda yaz) | avgDesc betik çıktısı | CC kodu (yerel sarmalayıcı) |
| 4. ui-ux-pro-max (739L), taste (1465L), hyperframes (1204L) tam yüklenir | Jeton + kural çakışması | Öncelik zincirinde alttakini yükleme; yalnız gerektiğinde oku | Skill çağrı sayacı (`cagri-sayac-*.txt`) | CC kodu |
| 5. Gate sert redleri (ecc GateGuard, superpowers "%1 kuralı") | Sürtünme | Reddi bilgi isteğine çevir (kanıt satırı iste, engelleme yapma) | Ret sayısı / oturum | Ömer ayarı |
| 6. Dışarı veri yolu: gstack telemetry-sync (Supabase), octo webhook (opt-in) | Güvenlik | Env tanımlı olmadığını boolean doğrula; gstack telemetri kapalı kalsın | `Test-Path env` boolean (değer yazdırma yok) | Ömer ayarı |

## (d) Çakışan skill kümeleri (silme yok, yalnız yönlendirme)

1. **Tasarım/frontend**: frontend-craft (en iyi: zincirin başı) · impeccable · ui-ux-pro-max · taste-* · frontend-design · designer-toolkit/ui-design/design-systems setleri. Hepsi frontend-craft altında "öncelik zinciri" ile yönlenir; alt sıradaki kural çakışmada düşer.
2. **TDD/test**: superpowers TDD · mattpocock tdd (en kısa/en iyi) · ecc tdd-guide · octo tdd-orchestrator · departman-test-qa. Yönlendirici: departman-test-qa → mattpocock tdd gövdesi.
3. **Kod inceleme**: ecc ×~15 reviewer · octo code-reviewer · addy code-reviewer · feature-dev · pr-review-toolkit · plugin-dev. Yönlendirici: departman-surec-inceleme; dile özgü olanlar yalnız ilgili dosya türünde.
4. **Plan/brainstorm/debug**: superpowers (brainstorming, writing-plans, systematic-debugging) · octo · ecc planner · agent-skills. Yönlendirici: departman-surec-plan.
5. **Güvenlik**: ecc security-reviewer · vibesec · never-get-hacked · cloudflare security-audit · phoenix-security · octo security-auditor. Yönlendirici: departman-guvenlik (semgrep/gitleaks önce).
6. **Hafıza/bağlam**: claude-mem · context-mode · agent-memory · graphify · headroom. Rol ayrımı: headroom=sıkıştırma, context-mode=sandbox, claude-mem=oturum hafızası, graphify=kod grafiği; çakışan kısım "özet enjekte etme" (tek kaynak seç).
7. **Skill yazımı**: skill-creator · superpowers writing-skills · plugin-dev skill-reviewer. Yönlendirici: skill-creator (tetik testi) + bizim lint betiği.
8. **Belge (pdf/docx/pptx)**: Anthropic document skills · adobe-* · daymade-docs. Yönlendirici: departman-belge.
9. **Pazarlama/SEO**: marketingskills · claude-ads (34 skill, 25 ajan) · ai-seo/seo-audit/seo-expert. Yönlendirici: yalnız iş çıkınca yükle.

(9 küme)

## (e) omer-skills'e ilk 10 iyileştirme

1. Skill boyut + açıklama lint betiği (`jev` altı): medyan ≤80 satır, açıklama ≤200 kr, hedef aşıldığında uyarı. Ölçü: mattpocock medyanı 75L.
2. departman-frontend (59L), video-uygula (105L), web-sahne-desenleri (127L): >60 satır bölümü `references/` altına taşı (şu an yalnız 3 skill references/ kullanıyor).
3. Üç katman: video-tarama okuma sırası "indeks → özet → tam rapor" olarak SKILL.md'ye yaz (tek adım yetmezse üst katmana çık).
4. Açıklamaları "Kullan: …" kalıbına çevir (departman-* zaten 125–167 kr; iş özeti gövdeye).
5. frontend-craft Bölüm 6'ya bağımsız bitiş-inceleme ajanı (okuyucu) + sözleşme karşılaştırması ekle (impeccable finish-reviewer deseni).
6. Her departman-* skill'ine tek satır "ham çıktı yazdırma, `jev log|triage` ile özetle" kuralı.
7. Kanıt kapısı: kod değişikliği skill'lerine "etkilenen çağıranlar + test + şema" 3 satırı (GateGuard'ın yumuşatılmış hali, ret yerine bilgi isteği).
8. Çakışma yönlendirmesi: omer-kutuphaneler skill'ine yukarıdaki 9 kümeyi tek tablo olarak ekle (ad → hangi skill). Silme yok.
9. Skill çağrı sayacından (`cagri-sayac-*.txt`) 30 gün kullanılmayan skill listesi üret; ilk aday listesi Ömer'e (kapatma önerisi, kendi başına kapatma yok).
10. Oturum başı yük bütçesi: `claude -p /context` ölçümü (CC) ve hedef: ilk bağlam ≤N token; octo+ecc eşzamanlı hook sayısı ≤ hedef (Ömer ayarı).
