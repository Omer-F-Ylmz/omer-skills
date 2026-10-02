# TOKEN-3a — skill listesi: tetik ölçümü + profil tasarımı · 2 Eki 2026 · AYAR DEĞİŞİKLİĞİ YOK

Uygulama TOKEN-3b'de. Bu dalgada yalnız ölçüm, araç (`tools/tetik_olc.py`), tetik seti (`olcum/tetik-seti.json`) ve tasarım var.

## 1. K1 — TOKEN-1 Blender dersi (yeni koşu yok; iki transcript, okuyucu ajanı/sonnet)

Kaynak: `Desktop\blender-kum\olcum\B-fincan-rehber{,-T1}\kosu-d1.jsonl`, `puan.json`, `kor.py:12`.

- **En olası sebep:** profil koşusu skill'in referans rehberlerini okumadı. Gövde system prompt'taydı ama `Skill` aracı ve skill listesi yoktu; tam koşuyu `references/` dosyalarına götüren adım kayboldu. Işık bu yüzden rehber yerine varsayılan HDRI ile kuruldu.
- Kanıt:
  - tam `:25-26` Skill `blender-oturum` + `blender-uretim`; profil init `:9` → 60 araç, `Skill` yok, 0 skill / 0 slash.
  - tam `:42-46` Read `olculer.md · donel-model.md · web-aktarim.md · malzemeler.md · isik-profilleri.md`, `:70-71` `isik_kur.py · malzemeler.py`.
  - profil `:14` `references/` yalnız `ls`; okunan tek referans `isik_kur.py` (`:41`); `isik-profilleri.md`, `malzemeler.md`, `donel-model.md` hiç okunmadı.
  - tam `:349` iki dikey AREA şerit (`LGT-SeritSol/Sag ±70°`, "seramik_sirli: iki dikey şerit"), `exposure 0.0`, kulp `KULP_ACI=-45` ("kulp sağda, kameraya dönük").
  - profil `:331` `isik_kur.kur("seramik_sirli", hdri=HDRI)`, `exposure -1.5`, kulp açısı yok.
  - kör puan (bicim/malzeme/ışık/kompozisyon/teknik/uygunluk): tam 4/4/4/4/4/3, profil 3/3/**2**/3/3/2 → fark en çok **ışık** (−2); not "Aşırı parlak … kulp neredeyse kayıp, fon açık gri değil".
- Tur: tam 201 asistan mesajı / 112 tool_use (Edit 23, Read 20, blender kodu 25); profil 107 / 54 (Edit 2, Read 9, blender kodu 13). Profil modelleme+malzeme+ışığı tek betikte yaptı, düzeltme turu yok.
- Elenen: Blender MCP eksikliği (iki koşuda aynı 26 `mcp__blender__*` aracı). Kısmi: tur azlığı. Dışlanamayan: model rastlantısı (n=1).
- Ders: profil skill **gövdesini** enjekte etse de skill'in **referans katmanına yönlendirmeyi** taşımalı. Kapalı aileye erişim yolu yalnız "gövde system prompt'ta" olamaz; SKILL.md + references Read edilebilir kalmalı.

## 2. K2 — yerleşik mekanizma (CC 2.1.287; okuyucu ajanı, resmi doküman + `claude --help`)

- Skill listesi için MCP tool search benzeri erteleme **yok** (skills sayfası: "listing always contains every skill name… drops some descriptions"). Tool search yalnız MCP için (`ENABLE_TOOL_SEARCH`, varsayılan açık; özel `ANTHROPIC_BASE_URL` varken varsayılan kapalı — env-vars).
- `skillOverrides` (ayar): `on` ad+açıklama · `name-only` yalnız ad, model çağırabilir · `user-invocable-only` modelden gizli, `/ad` çalışır · `off` tamamen gizli. **Plugin skill'leri etkilenmez** → plugin ailesi `enabledPlugins` ile.
- `SLASH_COMMAND_TOOL_CHAR_BUDGET` eski ad; yenisi `skillListingBudgetFraction` (bağlamın %1'i, yedek 8 000 kr). Dolunca ad kalır, **en az çağrılan** skill'lerin açıklaması düşer; giriş başı açıklama+when_to_use 1 536 kr'de kesilir; uyarı yalnız `--debug`.
- Frontmatter: `disable-model-invocation: true` açıklamayı listeden çıkarır (yalnız `/ad`); `user-invocable: false` yalnız menüden gizler; `paths` glob ile koşullu yükleme (liste etkisi kanıtsız).
- `--disable-slash-commands` Skill aracını da kaldırır — K1 kanıtı: T1 init `:9` 60 araç, `Skill` yok.
- **Karar:** profil yerleşik iki ayar üstüne kurulur: plugin aileleri proje `.claude/settings.json` → `enabledPlugins: {"<plugin>@<market>": false}` (TOKEN-1'de `--settings` ile 51→47 plugin düştü); plugin olmayan aileler (gstack, threejs, önsiz) → `skillOverrides: "name-only"`. `--disable-slash-commands` ve gövde enjeksiyonu kullanılmaz (K1).
- 3b'de deneyle doğrulanacak (kanıtsız): `skillOverrides`/`enabledPlugins` proje dosyasından okunuyor mu · kapalı plugin'in SKILL.md'si diskte Read edilebiliyor mu · `name-only` skill Skill ile çağrılabiliyor mu.

## 3. K4 — taban tetik (tam liste, gerçek ortam)

- Koşu: 30 istem · `claude -p` stream-json · `--max-turns 2` · `--permission-mode plan` · istemin kendi cwd'si · sırayla, boş RAM ≥4 GB. Headroom açık (`ANTHROPIC_BASE_URL` yerinde); init'te `Skill` aracı 30/30 koşuda var (pilot bl1: 413 araç · 393 skill · 490 komut · 51 plugin) → **30/30 gerçek ortam**; BASE_URL'siz teşhis koşusu gerekmedi.
- **recall 0.769** (20/26 pozitif istem kabul kümesinden ≥1 skill tetikledi) · **precision 0.926** (tetiklenen 27 skill'in 25'i kabulde) · negatif temiz 4/4.
- İlk ctx ort. 101.0k tok · toplam $30.58 (istem başı $1.02) · bitiş: error_max_turns 26, success 4 · tetik yolu: Skill aracı 25, SKILL.md Read 2.
- Tür başı (isabet · istem: tetiklenen):
  - blender 3/3 · bl1: blender-oturum, blender-uretim; bl2: blender-oturum, blender-uretim; bl3: blender-oturum, blender-uretim
  - mod 2/2 · md1: mod-atolyesi; md2: mod-atolyesi
  - video 2/2 · vd1: video-tarama; vd2: video-uygula
  - frontend 2/3 · fe1: frontend-craft; fe2: —; fe3: frontend-craft
  - dotnet-api 1/2 · dn1: —; dn2: surec
  - veri-db 2/2 · db1: optimizing-ef-core-queries; db2: departman-veri-db
  - test 0/2 · ts1: —; ts2: —
  - guvenlik-kvkk 2/2 · gv1: use-case-triage; gv2: sdp, surec
  - deploy 2/2 · dp1: deploy-to-vercel; dp2: departman-surec-git-yayin
  - belge 1/2 · bg1: departman-belge, make-pdf; bg2: —
  - arastirma 1/2 · ar1: departman-arastirma-ogrenme; ar2: —
  - skill-plugin 2/2 · sk1: departman-guvenlik, departman-surec-ajan-arac, jev; sk2: update-config
  - negatif temiz 4/4 · ng1: —; ng2: —; ng3: —; ng4: —
- Yanlış skill dökümü (kabul kümesi dışı tetik): departman-guvenlik×1, jev×1. Not: süreç skill'leri (brainstorming vb.) kabulde değilse yanlış sayıldı; 3b'de aynı set ve aynı kural kullanılır.
- Eksik (kabulden hiçbiri tetiklenmedi): fe2 (birincil beklenen frontend-craft), dn1 (birincil beklenen dotnet-webapi), ts1 (birincil beklenen code-testing-agent), ts2 (birincil beklenen test-driven-development), bg2 (birincil beklenen departman-belge), ar2 (birincil beklenen departman-arastirma-ogrenme)
- **L15 aday listesi** (açıklama netleştirme; içerik silinmez): code-testing-agent, departman-arastirma-ogrenme, departman-belge, departman-guvenlik, dotnet-webapi, frontend-craft, jev, test-driven-development

## 4. Profil tasarımı (TOKEN-3b'de uygulanır)

Liste: 140 263 kr ≈ 46.2k tok; 393 skill · 490 komut · 51 plugin (init). Aile payı (kr): anthropic-skills 17.5k · dotnet-test 13.0k · dotnet-msbuild 12.9k · agent-skills 10.7k · phoenix-prd 10.4k · threejs 9.2k · önsiz 8.0k · claude-mem 6.0k · taste-skill 4.9k · gstack 4.6k · phoenix-security 4.5k · example-skills 3.8k · plugin-dev 3.3k · superpowers 2.9k · ponytail 2.7k · diğer phoenix 6.1k.

- **Her profilde açık:** anthropic-skills (12 departman router'ı + kendi skill'ler), superpowers, ponytail, frontend-craft, skill-creator, hookify, commit-commands, küçükler (<500 kr). **Her profilde kapalı:** phoenix-* (7 plugin, %17.4; 14 günde 0 çağrı) — erişim departman-guvenlik/plan router'ından.
- **Proje türü → ek açık aileler:**
  - `skill-arac` (omer-skills; Blender işi de burada): plugin-dev, example-skills, claude-api, claude-mem, agent-skills, everything-claude-code, typesafe · name-only: gstack, threejs → **≈21.2k** (−%54).
  - `web` (TELVE, Corvano, Garajim, zombi-survival): taste-skill, threejs, gstack, design, design-mastery, impeccable, nateherk-design, 21st, nano-banana-2, frontend-design, supabase, agent-skills, example-skills → **≈25.2k** (−%45).
  - `dotnet` (Divisima, EgeYapiPanel): dotnet-test/msbuild/aspnetcore/data/nuget, agent-skills, supabase, everything-claude-code · name-only: gstack → **≈26.4k** (−%43).
  - `mod-blender` (Kendi oyun modlarim, blender-kum): yalnız her-zaman-açık küme · name-only: threejs → **≈11.9k** (−%74).
- **Kapalı aileye erişim:** departman router'ı. Bugün 12 router'ın hiçbiri SKILL.md yolu içermiyor (`grep -c SKILL.md` = 0 ×12). Router'a eklenecek bölüm: "Profil dışı üyeler" — ad → `~/.claude/plugins/cache/<market>/<plugin>/*/skills/<ad>/SKILL.md` (sürüm klasörü değiştiği için glob) + talimat "listede yoksa Glob ile bul, SKILL.md'yi ve gerekirse `references/`'ı Read et". Eşleme: frontend → taste/threejs/design/impeccable/21st; backend-dotnet → dotnet-*; veri-db → dotnet-data, supabase; test-qa → dotnet-test, agent-skills:test; guvenlik → phoenix-security-review, phoenix-sast-rules, phoenix-cti-search; surec-plan → phoenix-prd-pipeline, phoenix-readiness-reviews; belge → phoenix-docs-research, example-skills; surec-ajan-arac → plugin-dev, example-skills:mcp-builder, claude-api.
- Profil seçimi: proje `.claude/settings.json` (proje başına bir kez; kurulum kalır). Profil şablonları `profiller/` altında JSON; 3b'de `tools/cc_profil.py` ile yazılır/geri alınır.
- Beklenen tur başı taban: 89k medyan (TOKEN-0) → profil başına −20k ile −34k.

## 5. TOKEN-3b kapısı

- Tetik: aynı 30 istem, aynı `tools/tetik_olc.py`, gerçek ortam; profilli recall ve precision **tabanın altına düşmez**, negatif temiz ≥ taban; kaçan istemler tek tek raporlanır.
- Görev başarısı (Opus 5.5 ile yeni taban, tam vs profil): rtk-ab kod görevi + bir Blender işi (B-fincan-rehber). Blender'da kör puan okuyucu ajanıyla; ölçüt başına fark ve **referans Read sayısı** raporlanır (K1 dersi). Tur ve ağırlıklı token birlikte raporlanır.
- Ön koşul: §2'deki üç deney yeşil.
