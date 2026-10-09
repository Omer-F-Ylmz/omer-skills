# Karar paneli — 2026-10-03-short

Ömer sütununa AL / RED / ERTELE ya da karar (DENE · ÖĞREN · UYARLA · ZATEN VAR) yaz; boş satır dokunulmaz → `video panel uygula <bu dosya>`.

karar bekleyen 7 · ön-doldurulan 0 (ön-doldurma yalnız öneri; Ömer değiştirebilir)

| aday | tür | video | lisans | güvenlik | önerilen | gerekçe | Ömer |
|---|---|---|---|---|---|---|---|
| everything-claude-code-ecc | plugin | 2 | — | koşmadı: kurulu | ZATEN VAR | eşdeğer: everything-claude-code p 0.9 | ZATEN VAR |
| guvenlik-denetleyicisi-security-guidance | plugin | 1 | bilinmiyor | koşmadı: SkillSpector raporu yok | UYARLA | güncelle: fark: kurulu bf7d404 ↔ upstream bf4a74d · son commit 2026-05-26 | ZATEN VAR |
| skill-creator | skill | 1 | bilinmiyor | koşmadı: kurulu | UYARLA | güncelle: fark: kurulu d182ca4 ↔ upstream 2a40fd2 · son commit 2026-04-23 · alt tür çakışması (kurulu > ürün) | ZATEN VAR |
| stop-slop | skill | 1 | MIT | SkillSpector --no-llm HIGH/CRITICAL 0 | SOR | eksik: son_commit | |
| pazarlama-skill-paketi-30-skill | skill | 1 | MIT | koşmadı: SkillSpector raporu yok | SOR | ürün: kurulum gereği · bizde karşılığı · eksik: bizde_karsilik | |
| tasarim-skill-i-design-overhaul | skill | 1 | MIT (doğrulanmadı: LICENSE dosyası var, içeriği okunamadı; MIT olduğu hatırlanan bilgi) | koşmadı: SkillSpector raporu yok | SOR | eksik: son_commit | |
| superpowers | skill | 2 | MIT | koşmadı: kurulu | UYARLA | güncelle: fark: kurulu 5bf4e78 ↔ upstream 8ca22db · son commit 2026-09-25 | ZATEN VAR |
| install-skills | skill | 1 | bilinmiyor | koşmadı: repo yok | SOR | eksik: lisans, son_commit | |
| skills-cli-npx-skills | CLI | 1 | MIT | SkillSpector --no-llm HIGH/CRITICAL 20 | SOR | eksik: son_commit | |
| claude-icinde-mevcut-goreve-uygun-skill- | prompt | 1 | — | koşmadı: servis | ÖĞREN | prompt: kurulabilir araç değil | ÖĞREN |
| ruflo-videoda-rufflow | plugin | 1 | MIT | atlandı (repo 591 MB) | SOR | eksik: son_commit | |
| rooflow-karede-ruflo | iş akışı | 1 | — | koşmadı: repo yok | T0 | kural önerisi (omer-kurallar) | ÖĞREN |
| frontend-design | plugin | 1 | — | koşmadı: kurulu | UYARLA | güncelle: fark: kurulu d182ca4 ↔ upstream 44490cc · son commit 2026-09-01 | ZATEN VAR |
| code-review | plugin | 1 | bilinmiyor | koşmadı | UYARLA | güncelle: fark: kurulu bf7d404 ↔ upstream db8834b · son commit 2026-03-12 | ZATEN VAR |
| security-review | plugin | 1 | — | koşmadı: kurulu | ZATEN VAR | kurulu: everything-claude-code:security-review | ZATEN VAR |
| claude-mem | plugin | 1 | Apache-2.0 | koşmadı: kurulu | UYARLA | güncelle: fark: kurulu adce0fd ↔ upstream 94cb08b · yeni: skills/agent-cost-report, skills/handoff · son commit 2026-10-03 | ZATEN VAR |
| stack-garry-tan | plugin | 1 | — | koşmadı: kurulu | ZATEN VAR | kurulu: gstack · eşdeğer p 0.3 · araştırılmadı (kurulu) | ZATEN VAR |
| security-review-gelistirme | plugin | 1 | — | — | ÖĞREN | Yayın öncesi depo geneli tarama ve bulgu raporu adımını not al. Mevcut security-guidance ile bu adımın kapsanıp kapsanmadığını dene. (kanıt: k0gwr-vC2Z4 0:28: kare 'Completed', '1 minute ago · 4 findings'. Bizdeki kayıt yalnız kontrol listesi skill'i.) | |
| surekli-ogrenme-sistemi-ecc-icinde | teknik | 1 | — | koşmadı: servis | ÖĞREN | teknik: kurulabilir araç değil | ÖĞREN |
| everything-claude-code | plugin | 1 | — | koşmadı: kurulu | ZATEN VAR | kurulu: everything-claude-code | ZATEN VAR |
| security-guidance | plugin | 1 | — | koşmadı: kurulu | ZATEN VAR | kurulu: security-guidance · alt tür çakışması (kurulu > ürün) | ZATEN VAR |
| claude-dan-goreve-uygun-skill-i-bulup-on | prompt | 1 | — | koşmadı: servis | ÖĞREN | prompt: kurulabilir araç değil | ÖĞREN |
| ruflo | iş akışı | 2 | MIT | koşmadı | T0 | kural önerisi (omer-kurallar) | ÖĞREN |

## Ön-doldurulan
- yok
## form_red
- yok
## Eksik alanlar
- yok
## Belirsiz birleşmeler (ad benzer, repo farklı)
- yok
## ÜRETİLEBİLİR / yapım tarifleri
- guvenlik-denetleyicisi-security-guidance: hedef_tur: hook tarif: PreToolUse hook (matcher: Edit/Write/MultiEdit) yaz. Betik stdin'den tool_input JSON'unu okur (file_path, content/new_string). Kendi kural listeni (eval, exec/os.system, innerHTML, dangerouslySetInnerHTML, pickle.loads, SQL string birleştirme, workflow'da ${{ github.event.* }} enjeksiyonu, sabit sır kalıpları) regex ile eşle. Eşleşirse mesajı stderr'e yazıp exit 2 ile çık; oturum ve dosya+kural anahtarlı küçük bir durum dosyasıyla aynı uyarıyı tekrarlama. Plugin olarak .claude-plugin/plugin.json + hooks/hooks.json ile paketle. Kaynak kodu kopyalama; lisansı belirsiz, kendi kurallarını yaz.
- skill-creator: hedef_tur: skill tarif: Ayrı bir araç gerekmez, ama istersek küçük bir skill yazabiliriz. Skill, ajana OpenAPI/MCP kaynağını okutup `SKILL.md`, ince bir `scripts/` sarmalayıcısı ve `references/` içinde spec kopyası olan bir klasör üretmesini söyler. Sarmalayıcıya list/search/help alt komutları ekleriz. Gotchas bölümünü güncelleme kuralını da skill metnine yazarız. Hazır araç yerine kendi sürümümüzü yapmak, `npx -y` ile uzak paket çalıştırma riskini ortadan kaldırır. Resmi Anthropic skill-creator ile karşılaştırmak da yararlı olur.
- stop-slop: hedef_tur: skill tarif: Türkçe uyarlama: SKILL.md + references/(kaliplar-tr.md, yapilar-tr.md, ornekler-tr.md). Türkçe yapay zeka kalıplarını derle ('Sonuç olarak', 'günümüzde', 'bir yolculuğa çıkalım', 'sadece X değil, aynı zamanda Y', gereksiz edilgenlik, 'önemle belirtmek gerekir'). Aynı 5 boyutlu puanlama ve 35/50 eşiğiyle yeniden yazma döngüsü ekle; em dash/Wh- gibi İngilizce'ye özgü kuralları çıkar. Orijinal MIT lisansına atıf yap.
- pazarlama-skill-paketi-30-skill: hedef_tur: skill tarif: Zaten skill olarak var, doğrudan kurulabilir. Kendi sürümümüz için: (1) MIT lisansı gereği fork et ve ihtiyaç duyulan 8-10 skill'i seç (seo-audit, ai-seo, cro, copywriting, emails, ads, analytics, product-marketing); (2) açıklamaları Türkçe tetikleyicilerle genişlet; (3) Türkiye pazarına özel örnekler ekle; (4) product-marketing bağlam belgesini proje başına tek dosya olarak tut; (5) kullanılmayanları çıkararak bağlam maliyetini düşür.
- tasarim-skill-i-design-overhaul: hedef_tur: skill tarif: Kendi tasarım skill'imizi yazın. (1) skills/tasarim/ altında SKILL.md oluşturun. (2) CSV'lerle ürün türü→stil/palet/yazı tipi/anti-desen eşleştirme tablosu ekleyin. (3) Anahtar kelime aramalı küçük bir Python betiği ekleyin. (4) Teslim öncesi kontrol listesi ekleyin: emoji yerine SVG ikon, kontrast, cursor-pointer, duyarlılık. Veriyi sıfırdan, bizim projelerimize uyarlayın. Yukarıdaki repo yalnızca fikir kaynağı olsun, lisansı doğrulanmadan veri kopyalanmasın.
- superpowers: hedef_tur: skill tarif: Doğrudan kurmak yeterli. Kendi sürümümüz gerekirse, MIT lisansı izin verdiği için lisans notunu koruyup şu dört skill'i uyarlayabiliriz: brainstorming (spec çıkarma), writing-plans, test-driven-development ve verification-before-completion. Bunları omer-skills altına SKILL.md olarak koyar, tetikleme açıklamalarını Türkçe yazarız. Oturum başı zorlama gerekirse küçük bir SessionStart hook'u ekleriz. Subagent akışını isteğe bağlı bırakırız, çünkü token maliyeti yüksektir.
- install-skills: hedef_tur: skill tarif: Kendi 'skill-bul-kur' skill'imiz yazılabilir: (1) kullanıcıdan amaç al; (2) bilinen skill indekslerinde (GitHub repoları, `npx skills` ekosistemi, yerel omer-skills) anahtar kelimeyle ara; (3) adayları SKILL.md açıklamalarıyla listele; (4) kullanıcı onayından sonra, kurulumdan önce içeriği güvenlik taramasından (SkillSpector benzeri) geçirip ~/.claude/skills ve ~/.agents/skills altına kopyala. Orijinal kod incelenmeden birebir eşdeğerlik iddia edilemez.
- ruflo-videoda-rufflow: hedef_tur: hook tarif: Tamamını kopyalamak yerine iki parça yapılabilir. (1) UserPromptSubmit hook'u: istemi sınıflandırıp (basit / orta / karmaşık) uygun alt ajanı ya da modeli öneren bir yönlendirici. (2) Basit bir SQLite/JSON hafıza skill'i: tamamlanan görevlerin özetini ve etiketlerini yazar, yeni oturumda SessionStart hook'u ile ilgili kayıtları bağlama ekler. Swarm koordinasyonu için Claude Code'un yerel alt ajan (Task) özelliği yeterli olabilir. Ruflo'nun swarm, federasyon ve vektör hafızası kapsamının tamamı karşılanmaz.
- code-review: hedef_tur: skill tarif: Kendi `code-review` skill'imizi ya da slash komutumuzu yazabiliriz; yalnızca fikri ve yapıyı alırız, metni kopyalamayız (lisans özel). Tarif: (1) SKILL.md ön kontrol adımı olarak `gh pr view` ile PR durumunu (kapalı, taslak, daha önce yorumlanmış) denetler. (2) Değişen dosyaların yolundaki CLAUDE.md dosyalarını toplar. (3) Paralel alt ajanlar başlatır: CLAUDE.md uyumu ve diff içi hata/güvenlik. İstersek git blame/geçmiş ajanını da ekleriz, çünkü videonun anlattığı da buydu. (4) Her bulgu için ayrı doğrulayıcı alt ajan çalışır, doğrulanamayanlar elenir. (5) Çıktı varsayılan olarak terminale yazılır, `--comment` ile `gh pr comment` kullanılır. (6) 'Pre-existing, linter, üslup' yanlış-pozitif listesini istemin içine koyarız. `allowed-tools` içinde yalnızca gerekli `gh` komutlarına izin veririz.
- claude-mem: hedef_tur: hook tarif: Hafif bir sürüm yapılabilir. (1) PostToolUse ve Stop hook'ları araç olaylarını yerel bir SQLite (FTS5) dosyasına yazar. (2) SessionEnd hook'u oturum özetini claude -p veya küçük bir modelle çıkarıp kısa gözlemler olarak kaydeder. (3) SessionStart hook'u projeye ait son N gözlemi kompakt indeks halinde additionalContext olarak enjekte eder. (4) İsteğe bağlı küçük bir MCP veya skill, indeksten ID ile ayrıntı çekmeyi (3 katmanlı arama) sağlar. Vektör arama ve sürekli çalışan worker olmadan başlanabilir. Sırları süzmek için kayıt öncesi maskeleme eklenmeli.
## Kural önerileri (T0)
- rooflow-karede-ruflo: Claude'u paralel çalışan, hafıza paylaşan ve maliyet yönlendirmeli çok ajanlı ekibe çeviren açık kaynak iş akışı.
## OLASI EŞDEĞER (Jev p 0.5–0.75)
- yok
## OLASI TEKRAR
- yok
## Araştırılmadı
- everything-claude-code-ecc: kapsam eksik (README, lisans, commit, güvenlik)
- guvenlik-denetleyicisi-security-guidance: kapsam eksik (lisans, güvenlik)
- skill-creator: kapsam eksik (lisans, commit, güvenlik)
- stop-slop: kapsam eksik (commit)
- pazarlama-skill-paketi-30-skill: kapsam eksik (commit, güvenlik)
- tasarim-skill-i-design-overhaul: kapsam eksik (commit, güvenlik)
- superpowers: kapsam eksik (commit, güvenlik)
- install-skills: kapsam eksik (repo, README, lisans, commit, güvenlik)
- skills-cli-npx-skills: kapsam eksik (commit)
- claude-icinde-mevcut-goreve-uygun-skill-: kapsam eksik (prompt metni)
- ruflo-videoda-rufflow: kapsam eksik (commit, güvenlik)
- frontend-design: kapsam eksik (lisans, commit, güvenlik)
- code-review: kapsam eksik (lisans, güvenlik)
- security-review: kapsam eksik (repo, README, lisans, commit, güvenlik)
- claude-mem: kapsam eksik (güvenlik)
- stack-garry-tan: kapsam eksik (repo, README, lisans, commit, güvenlik)
## Repo araması
- stop-slop: bulundu: hardikpandya/stop-slop
- pazarlama-skill-paketi-30-skill: arandı, bulunamadı (Pazarlama skill paketi; Pazarlama skill paketi claude; Pazarlama skill paketi Tek kurulumda 30'dan)
- tasarim-skill-i-design-overhaul: arandı, bulunamadı (Tasarım skill'i; Tasarım skill'i claude; Tasarım skill'i 60'tan fazla stille)
- install-skills: arandı, bulunamadı (install skills; install skills claude; install skills Diğer skill'lerde arama)
- skills-cli-npx-skills: arandı, bulunamadı (Skills CLI; Skills CLI claude; Skills CLI Açık ajan skill)
## Kapsam
repo · README · lisans · commit · güvenlik · prompt metni · güncellik · yorum (✓ yapıldı; değilse sebep)
- everything-claude-code-ecc · repo ✓ worldflowai/everything-claude-code · README araştırılmadı (kurulu) · lisans araştırılmadı (kurulu) · commit araştırılmadı (kurulu) · güvenlik koşmadı: kurulu · prompt metni — · güncellik güncel (432485b) · son commit 2026-01-23 · yorum ✓
- guvenlik-denetleyicisi-security-guidance · repo ✓ anthropics/claude-code · README ✓ · lisans bilinmiyor · commit ✓ 2026-05-26 · güvenlik koşmadı: SkillSpector raporu yok · prompt metni — · güncellik fark: kurulu bf7d404 ↔ upstream bf4a74d · son commit 2026-05-26 · yorum ✓
- skill-creator · repo ✓ anthropics/claude-plugins-official · README ✓ · lisans bilinmiyor · commit bilinmiyor · güvenlik koşmadı: kurulu · prompt metni — · güncellik fark: kurulu d182ca4 ↔ upstream 2a40fd2 · son commit 2026-04-23 · yorum ✓
- stop-slop · repo ✓ hardikpandya/stop-slop · README ✓ · lisans ✓ · commit bilinmiyor · güvenlik ✓ · prompt metni — · güncellik — (kurulu değil) · yorum ✓
- pazarlama-skill-paketi-30-skill · repo ✓ coreyhaines31/marketingskills · README ✓ · lisans ✓ · commit bilinmiyor · güvenlik koşmadı: SkillSpector raporu yok · prompt metni — · güncellik — (kurulu değil) · yorum ✓
- tasarim-skill-i-design-overhaul · repo ✓ nextlevelbuilder/ui-ux-pro-max-skill · README ✓ · lisans ✓ · commit bilinmiyor · güvenlik koşmadı: SkillSpector raporu yok · prompt metni — · güncellik — (kurulu değil) · yorum ✓
- superpowers · repo ✓ obra/superpowers · README ✓ · lisans ✓ · commit bilinmiyor · güvenlik koşmadı: kurulu · prompt metni — · güncellik fark: kurulu 5bf4e78 ↔ upstream 8ca22db · son commit 2026-09-25 · yorum ✓
- install-skills · repo arandı, bulunamadı (install skills; install skills claude; install skills Diğer skill'lerde arama) · README repo yok · lisans bilinmiyor · commit bilinmiyor · güvenlik koşmadı: repo yok · prompt metni — · güncellik — (kurulu değil) · yorum ✓
- skills-cli-npx-skills · repo ✓ vercel-labs/skills · README ✓ · lisans ✓ · commit bilinmiyor · güvenlik ✓ · prompt metni — · güncellik — (kurulu değil) · yorum ✓
- claude-icinde-mevcut-goreve-uygun-skill- · repo — (tür prompt) · README — (tür prompt) · lisans — (tür prompt) · commit — (tür prompt) · güvenlik — (tür prompt) · prompt metni alınmadı · güncellik — (kurulu değil) · yorum ✓
- ruflo-videoda-rufflow · repo ✓ ruvnet/ruflo · README ✓ · lisans ✓ · commit bilinmiyor · güvenlik atlandı (repo 591 MB) · prompt metni — · güncellik — (kurulu değil) · yorum ✓
- rooflow-karede-ruflo · repo — (tür iş akışı) · README — (tür iş akışı) · lisans — (tür iş akışı) · commit — (tür iş akışı) · güvenlik — (tür iş akışı) · prompt metni — · güncellik — (kurulu değil) · yorum ✓
- frontend-design · repo ✓ anthropics/claude-plugins-official · README ✓ · lisans bilinmiyor · commit bilinmiyor · güvenlik koşmadı: kurulu · prompt metni — · güncellik fark: kurulu d182ca4 ↔ upstream 44490cc · son commit 2026-09-01 · yorum ✓
- code-review · repo ✓ anthropics/claude-code · README ✓ · lisans bilinmiyor · commit ✓ 2026-03-12 · güvenlik koşmadı · prompt metni — · güncellik fark: kurulu bf7d404 ↔ upstream db8834b · son commit 2026-03-12 · yorum ✓
- security-review · repo repo yok · README araştırılmadı (kurulu) · lisans araştırılmadı (kurulu) · commit araştırılmadı (kurulu) · güvenlik koşmadı: kurulu · prompt metni — · güncellik güncellik bakılamadı (repo bilinmiyor) · yorum ✓
- claude-mem · repo ✓ thedotmack/claude-mem · README ✓ · lisans ✓ · commit ✓ bilinmiyor (README sürüm rozeti 13.29.0) · güvenlik koşmadı: kurulu · prompt metni — · güncellik fark: kurulu adce0fd ↔ upstream 94cb08b · yeni: skills/agent-cost-report, skills/handoff · son commit 2026-10-03 · yorum ✓
- stack-garry-tan · repo repo yok · README araştırılmadı (kurulu) · lisans araştırılmadı (kurulu) · commit araştırılmadı (kurulu) · güvenlik koşmadı: kurulu · prompt metni — · güncellik güncellik bakılamadı (repo bilinmiyor) · yorum ✓
## Site/UI teknikleri
- Jenerik AI görünümünden kaçınan production-grade frontend üretimi (Frontend Design plugin) · k0gwr-vC2Z4 · 0:15 (kare) → docs/departmanlar/frontend.md
- Tanıtım videosu animasyonları: noktalı ızgara arka plan, neon yeşil çerçeve, serif tipografi · k0gwr-vC2Z4 · 0:47 (kare) → docs/departmanlar/frontend.md
## Anatomi bekliyor
- yok
## Geliştirme önerileri
- everything-claude-code-ecc · video: Ajan, skill, komut, hook ve MCP yapılandırmalarını tek plugin olarak kurma; rABIViSQmsc 0:00'da 181 skill, 47 alt ajan, 79 komut sayısı veriliyor. · bizde: everything-claude-code plugin olarak kurulu (agents, skills, hooks, commands, rules). Kurulu sürümdeki sayılar bilinmiyor. · fark: Videodaki sayılar bizdeki kurulu sürümle karşılaştırılamıyor. Bizdeki sürüm eski ya da yeni olabilir, bilinmiyor. · yok: ⚠ S10 ihlali (kapatma/kaldırma önerilmez; TOKEN-3 profilleri) · Kurulu sürümün skill/ajan/komut sayısını videodaki rakamlarla karşılaştır. Sürüm geride ise güncelle. Kaldırma ya da kapatma yapma; yükleme TOKEN-3 profilleriyle yönetilir. · kanıt: rABIViSQmsc 0:00: 181 skill, 47 alt ajan, 79 komut. Bizdeki kayıtta sayı yok, somut fark çıkarılamıyor.
- guvenlik-denetleyicisi-security-guidance · video: I0ADpAN2qT0 0:04: Claude'un yazdığı kodu aynı oturumda tarayıp açıkları bulan eklenti (README: 'security-guidance'). · bizde: security-guidance kurulu: düzenlemede desen uyarısı, Stop'ta LLM diff incelemesi, agentic commit reviewer. · fark: Videodaki işlev bizdeki eklentiyle aynı. Bizde olmayan bir yan yok. · yok: Değişiklik gerekmiyor. · kanıt: 
- skill-creator · video: BiEvvC_66AQ 0:06: Anthropic'in skill-creator'ı ile kendi skill'lerini oluşturma ve düzenleme. · bizde: skill-creator kurulu: skill oluşturma, iyileştirme, eval ve performans ölçümü. · fark: Bizdeki kapsam videodakinden geniş (eval ve benchmark dahil). Daha iyi bir yan yok. · yok: Değişiklik gerekmiyor. · kanıt: 
- superpowers · video: BiEvvC_66AQ 0:30 ve k0gwr-vC2Z4 0:09: strateji-yapı-geliştirme çerçevesi; koda atlamadan önce plan ve test zorlar. · bizde: superpowers kurulu: TDD, hata ayıklama, işbirliği kalıpları. · fark: Videoda bizdekinden farklı bir kullanım gösterilmiyor. Plan ve test önceliği zaten kurulu çekirdek skill'lerin işi. · yok: Değişiklik gerekmiyor. · kanıt: 
- frontend-design · video: k0gwr-vC2Z4 0:15: jenerik yapay zeka estetiğinden kaçınan, üretim kalitesinde arayüz üretimi. · bizde: frontend-design plugin kurulu. Ayrıca 39IlNR-P3-Q kaynaklı, doğrulanmamış (orta güven) bir 'dörtlü skill yığını' notu var. · fark: Videoda bizde olmayan bir yan görünmüyor. Dörtlü yığın iddiası doğrulanmadığı için dayanak sayılmadı. · yok: Değişiklik gerekmiyor. · kanıt: 
- code-review · video: k0gwr-vC2Z4 0:22: beş ajan paralel olarak hataları, kuralları ve git geçmişini inceler. · bizde: code-review plugin kurulu: PR için birden çok özel ajan ve güvene dayalı puanlama. Ayrıca bir code-review MCP kaydı var. · fark: Çok ajanlı inceleme zaten bizde var. Videoda eksik bir yan görünmüyor. · yok: Değişiklik gerekmiyor. · kanıt: 
- security-review · video: k0gwr-vC2Z4 0:28: yayın öncesi kod tabanını tarar; acme-corp/hookrelay için 'Completed', '4 findings' sonucu gösteriliyor. · bizde: everything-claude-code:security-review skill'i var. Kimlik doğrulama, kullanıcı girdisi ve gizli bilgi işlerinde kullanılan kontrol listesi niteliğinde. security-guidance ise yalnız Claude'un düzenlemelerini ve commit'leri inceliyor. · fark: Videoda bulgu sayılı, tamamlanmış bir tam depo taraması gösteriliyor. Bizdeki skill kontrol listesi veriyor; depo genelinde tarama yapıp bulgu raporu üretmiyor. Videodaki aracın ne olduğu bilinmiyor. · ÖĞREN: Yayın öncesi depo geneli tarama ve bulgu raporu adımını not al. Mevcut security-guidance ile bu adımın kapsanıp kapsanmadığını dene. · kanıt: k0gwr-vC2Z4 0:28: kare 'Completed', '1 minute ago · 4 findings'. Bizdeki kayıt yalnız kontrol listesi skill'i.
- claude-mem · video: k0gwr-vC2Z4 0:35: oturumlar arası hafıza; projeyi her seferinde yeniden anlatma ihtiyacını ortadan kaldırır. · bizde: claude-mem kurulu: bağlam oturumlar arası saklanıyor. · fark: Aynı işlev. Videoda ek bir yapılandırma ya da kullanım gösterilmiyor. · yok: Değişiklik gerekmiyor. · kanıt: 
- stack-garry-tan · video: k0gwr-vC2Z4 0:41: Garry Tan'in 23 skill'lik plugin'i; CEO, mühendislik müdürü ve QA rolleri birlikte çalışır. · bizde: gstack skill'i kurulu, tanımı 'gstack skill suite için yönlendirici'. Alt skill sayısı ve rol kapsamı kayıttan bilinmiyor. · fark: Bizdeki rol skill'lerinin 23 sayısı ve CEO/EM/QA rolleriyle örtüşüp örtüşmediği doğrulanamıyor. Somut fark kanıtlanamıyor. · yok: gstack paketindeki skill sayısını ve rollerini say, videodakiyle karşılaştır. Eksik varsa güncelle. · kanıt: 
## Defter
30 çağrı · $2.2405 · 656336 jeton
