# ENVANTER-DOGRULA-1
- Girdi kurtarma: 279 kayıp değildi, tsv'ye yazılmamıştı. `ogren/yeni1-cikti/env*.tsv` ham çıktısından `yeni1_birlestir.py` mantığıyla (ad,tür) tekilleştirilince 1043 satır geri çıktı; bunların 279'u eski kaba ad-alt-dize eşleşmesiyle "KURULU" idi (tsv'ye yalnız 764 KURULACAK yazılmıştı).
- Tekilleştirme: repo slug (owner/repo) > normalize ad → 1043 satır → **955 tekil**.
- Sonuç (955 tekil): **KURULU-KANIT 174 · KURULACAK 703 · BELİRSİZ 78**
- KURULU-KANIT: 40 repo-URL eşleşmesi (installed_plugins/known_marketplaces/araclar+indirilen git remote/kayit.jsonl KUR), 134 ad eşleşmesi (~/.claude/skills, plugin cache, araclar/, C:\AI\indirilen, _inv_* mcp/npm/pip/uv/winget/plugin/skills, envanter.tsv CC/ikisi/claude.ai, ~/.claude.json mcp adları). Kanıt yolu her satırda `kanit` sütununda.
- BELİRSİZ: yalnız benzer (≥7 harf, ≥%60 örtüşen) ad ya da yalnız katalog (yetenek.tsv) eşleşmesi; aynı araç mı doğrulanmadı. Model/CLI ile `--version` doğrulaması yapılmadı.
- Sınırlar: ad eşleşmesi 134 satırda aynı-araç garantisi vermez (repo URL'si yok); `where`/`--version` ve mcp list canlı sınanmadı; YANLIŞ EŞLEŞME/KISMEN ayrımı yapılmadı (BELİRSİZ'e düştü). Eski 279 kaba "kurulu"nun tekil karşılığı: 955 içinde 174 kanıtlı.
- Çıktı: `rapor/video-yeni-1-kurulacaklar-tekil.tsv` (sınıf sıralı). Betik: tmp/ed1_b.py. Kurulum yapılmadı.

## TUR 2 (29 Eki): BELİRSİZ 78 sıfırlandı

Yöntem: betik eşleme (ogren/ev_tur2.py, ev_tur2b.py: SKILL.md frontmatter, git remote, known_marketplaces.json repo, mcpServers, `where`) + elle karar (ogren/uygula_tur2.py). Model çağrısı yok. Yedek: `.yedek-tur2`. Kurulum yapılmadı.

78 BELİRSİZ dağılımı: KURULU-KANIT 26 · KURULACAK 34 · AYNI-AİLE 17 · BULUNAMADI 1.

Güncel dağılım (955 tekil): KURULU-KANIT 200 · KURULACAK 737 · AYNI-AİLE 17 · BULUNAMADI 1 · BELİRSİZ 0.

Notlar:
- Her satırın `kanit` sütununa `| tur2: <kanıt>` eklendi.
- Repo klonu (C:/AI/indirilen) remote eşleşirse repo/referans türünde KURULU-KANIT; kurulum gerektiren araç/kütüphanede klon tek başına KURULACAK (klon yolu notta).
- Canlı sınanan: skillspector.exe çalışıyor; `where comfyui/whisper` boş; firecrawl CLI npm'de var. Sınanmayan: Python paket sürümleri (Scrapling), OpenMontage/diagram-design kaynak URL eşleşmesi.
- Yalnız-ad eşleşmesiyle KURULU-KANIT: find-skills, i-have-adhd, Scientific Skills (source alanı K-Dense, skill 598B kısa).

## TUR 3: AYNI-AILE 17 kurulumu (29 Eki)

| kalem | kuruldu | kanit | kart |
|---|---|---|---|
| Firecrawl / Firecrawl MCP | npm firecrawl-mcp 3.36.0 (MIT), CLI 1.26.22 | require ok; MCP global eklenmedi; FIRECRAWL_API_KEY yok = hesap-en-sona | yok |
| Remotion | npm remotion 4.0.539 | require ok (araclar/kutuphane-deneme); lisans Remotion License (sirket >3 kisi ucretli) | yok |
| React Three Fiber | @react-three/fiber 9.8.2 + three | require ok | yok |
| Scrapling x2 | pip scrapling 0.5 (BSD-3) | import + css secici ok | yok |
| diagram-design x2 | zaten skills/diagram-design-paket | cathynlaveny/diagram-design 404, kaynak dogrulanamadi | yok |
| OpenMontage x2 | klon araclar/openmontage | AGPL-3.0; gitleaks 23 (test/skill-doc yer tutucu), semgrep 11 dusuk | yok |
| Netlify Drop | site referansi | kurulum yok, netlify MCP kayitli | yok |
| AutoClip | klon araclar/autoclip (zhouxiaoka, MIT) | gitleaks 31 (test/doc yer tutucu), semgrep 0; video kaynagi belirsiz, en yakin aday; calistirilmadi | yok |
| interfaces.dev | site referansi | plugin interfaces kurulu | yok |
| Nano Banana | plugin 0.1.1 + GEMINI_API_KEY var | models.list 6 goruntu modeli, 0 uretim | yok |
| ElevenLabs | pip elevenlabs 2.75.0 | import ok; ELEVENLABS_API_KEY yok = hesap-en-sona | yok |
| Whisper | faster-whisper 1.2.1 + large-v3 | gercek transkript (tiny): "Hello world, this is a whisper test." | yok |
| Blender Lab MCP | blender-mcp.exe (ahujasid, MIT) zaten kurulu | resmi Blender Lab deposu bulunamadi; sinif AYNI-AILE kaldi | yok |

Sapmalar: usta karti araci tools/ altinda yok, kart uretilmedi. Playwright/gitleaks bulgulari yer tutucu, gercek sizinti yok. SkillSpector: kurulan sey skill degil, calistirilmadi.

## TUR 4 (29 Eki, kısmi)

Gruplar (737 KURULACAK, `rapor/tur4-gruplar.tsv`): site 225 · repo 163 · paket 105 · skill 68 · uygulama 48 · yöntem 42 · plugin 32 · model 29 (yerel-medya-1'e bırakıldı) · mcp 19 · hesap 6 (en sona).

Yapılan:
- SİTE 225 → katalog satırı `docs/kaynak-kutuphane/site-katalog-tur4.tsv`, tsv'de KURULU-KANIT (kurulum yok, yalnız katalog).
- Skill 4 → diskte aynı araç doğrulandı: skill-creator, frontend-design, Remotion Skills (remotion-best-practices), Vibesec (vibesec-skill).
- Güncel dağılım: KURULU-KANIT 445 · KURULACAK 508 · AYNI-AİLE 1 · BULUNAMADI 1.

Yapılmayan: skill (64), paket, repo, MCP, plugin kurulumu ve usta kartı (bu tur bütçesi); sonraki tur skill → paket → repo → MCP sırasıyla devam. Çoğu skill satırında ad/URL boş, tek tek aday araştırması gerekiyor.

## TUR 5 (31 Eki, skill, kısmi)
- Lisans kapısı (gh api): MIT/Apache → elayadesign/ai-design-skills, better-icons, stop-slop, emilkowalski/skills, addyosmani/agent-skills, drawio-skill, book-to-skill, mattpocock/skills, offer-master, instagram-agent-skill (klon C:/AI/indirilen/skills-tur5, gitleaks 0). Lisanssız → kurulmadı: vercel-labs/agent-skills, ComposioHQ/awesome-claude-skills. 404: apk-reverse, rossark-motion-skill.
- Kopyalandı (~/.claude/skills, üzerine yazma yok): addyosmani 20 yeni skill, drawio-skill, book-to-skill, better-icons; emilkowalski/stop-slop/landing-page-design zaten vardı.
- tsv: 7 satır KURULU-KANIT (508 → 501 KURULACAK). Yedek `.yedek-tur5`.
- Yapılmadı: offer-master, instagram-agent-skill, mattpocock, gamedev (74), ffmpeg-skill, video-shotcraft (200 MB), day-trader (finans), tsv'ye işlenmedi; ad/URL'si boş ~45 skill satırı; plugin/MCP/paket/repo. SkillSpector/semgrep koşulmadı. Hakem puanı yok.

## TUR 6 (31 Eki, kısmi)
- Skill: instagram-agent-skill (13 ig-*), offer-master-skill (8 offer-*) MIT, gitleaks 0, ~/.claude/skills'e kopyalandı (21 yeni); mattpocock/skills (MIT, gitleaks 0) zaten kuruluydu (31 skill adı mevcut, 0 kopya); Teach skill = mevcut.
- Plugin: 11 satır installed_plugins.json ile kanıtlandı (Adobe, Anthropic skills, knowledge-work-plugins ve 5 alan eklentisi, ECC).
- tsv: 14 satır KURULU-KANIT; 501 → 487 KURULACAK. Kalan plugin satırlarının çoğu ad/URL'siz (Hermes, GSD, BMad, PPT Master vb.): aday araştırması gerekiyor.
- Yapılmadı: MCP/paket/repo, semgrep, hakem puanı, usta kartı. Harcama sınırı nedeniyle durdu.

## TUR 7 (31 Eki, kısmi)
- MCP: `claude mcp list` ile 21st, rea (6.8.0), github, figma bağlı; exa eklenti kurulu (auth Ömer'de) → 5 KURULU-KANIT. blockbench-mcp-plugin GPL-3.0 → RET (şart: kopyaleft). Lisans MIT: Perplexity, ScrapeGraph, PostHog, Glif, davinci-resolve-mcp; kurulmadı (API anahtarı/hesap ya da Resolve uygulaması gerekir) → sabah Ömer listesi.
- Paket: animejs, three, radix-ui, @number-flow/react, lenis (npm) + tree-sitter, dspy (pip) scratch `tmp/paket-tur7`'e kuruldu, import OK → 7 KURULU-KANIT. satori MPL-2.0 → RET (şart: değiştirilen MPL dosyaları açık).
- tsv: 487 → 473 KURULACAK (KURULU-KANIT 478, RET 2). Yedek `.yedek-tur7`. semgrep/hakem/usta kartı yapılmadı; gitleaks bu turda koşulmadı (yalnız resmi paket kayıtları).
