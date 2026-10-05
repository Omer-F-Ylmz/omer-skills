# Video kuyruğu — Desktop ön incelemesi

Ömer'in kuralı (28 Eyl): gönderilen hiçbir video elenmez. Her video en ince ayrıntısına kadar tam hattan geçer; iyi özellikleri mekanizmasıyla alınır (nasıl yapılmış, neden iyi, bizde nasıl daha iyi yapılır), token tasarrufu olanlar kesin denenir, kalite takası tablosu ve tasarruf ayrıştırma geçerli (omer-kurallar 21-24). İyi özellikler ayıklanıp gerektiğinde kendi skill · plugin · MCP · CLI · hook'umuz üretilir; amaç her şeyden kendimize katmak, geliştirmek, mükemmel olmak. Videodaki, açıklamadaki ve bağlantılardaki her repo/araç/site araştırılır (Ömer, 28 Eyl).

Akış: Ömer linki Desktop'a atar → Desktop meta + ön inceleme (neye özellikle bakılacak) → CC kuyruğu partilerle tam hattan geçirir → EN SONDA çift dikiş: video hattı tam istenen hale geldiğinde Ömer'in gönderdiği BÜTÜN videolar (eski 70 + bu kuyruk + sonrakiler) son haliyle yeniden analiz edilir; eksik kalan ya da daha fazla alınabilecek her şey yakalanır (Ömer, 28 Eyl).

Sıra (yalnız işleme sırası, eleme değil): 1 = site yapımı / prompt / token tasarrufu · 2 = araç/skill/plugin/MCP · 3 = genel iş akışı ve diğer.
Meta önbelleği (başlık, kanal, süre, açıklama, açıklama linkleri): C:\Projeler\.video-cache\kuyruk-meta-2026-09-28.json
Parti boyu önerisi: uzun video (≥7 dk) 3/oturum · short (<2 dk) 8/oturum.

## Eklenen: 2026-09-28 (83 tekil video + 6 kaynak)

### Sıra 1 — token tasarrufu
| id | süre | başlık (kısa) | Desktop notu: özellikle bakılacaklar | durum |
|---|---|---|---|---|
| L9c49WVG_ho | 0.6 | Ücretsiz API anahtarı (Esad Kılıç) | ÖMER SORUSU: basit işleri ücretsiz modellere devredip Claude token'ı azaltmak. Aday: tarayıcı alt ajanının çıkarım kısmını OpenRouter ücretsiz/ucuz modele devretmek (Jev altyapısı gibi), Claude yalnız yargıda; takas tablosuyla DENE | işlendi: aaa5dd0 |
| kHtOSJRUkLs | 19.8 | Never run out of tokens (Sharbel) | yapıştırılan talimat/konfigürasyon: tasarruf mekanizması, bizde CLAUDE.md/Headroom/RTK karşılığı | işlendi: b4af98c |
| 6cEQEba0i2A | 10.7 | Save millions of Claude tokens (Nate Herk) | açıklamada 9 link; her teknik ayrı özellik, tasarruf ayrıştırma | işlendi: b4af98c |
| g89FJiNAlEs | 15.1 | 4 free repos cut token usage | 4 GitHub repo; her biri araç adayı + mekanizma; Headroom/RTK/context-mode ile çakışma | işlendi: b4af98c |
| V0XbuApxlhg | 19.0 | Paying Anthropic 20x more (Chase AI) | model/plan/effort seçimi iddiaları → iddia sınama (bizim ölçümlerimiz: effort A/B, Opus/Sonnet) | işlendi: 57a0138 |
| oHKt0FUbR58 | 0.8 | Free repo fixes token limits | repo adı ekranda/açıklamada; araç adayı | işlendi: aaa5dd0 |
| bS6IlkUozAI | 1.7 | Web browsing tokens −90% | tarayıcı/web getirme sıkıştırma aracı; bizde video getir + Headroom karşılaştırması | işlendi: aaa5dd0 |
| NogIRR1B6gY | 0.7 | PDF'ler token tüketmesin | PDF okuma stratejisi; pdf-reading skill ile karşılaştır | işlendi: aaa5dd0 |
| klDiYMzW0o0 | 0.7 | Token harcamanı yarıya indiren 4 araç | 4 araç; kurulu olanlar ZATEN VAR, yeniler DENE | işlendi: aaa5dd0 |
| lipJRiztOgM | 0.7 | 5 skills save 10x sessions | skill adları; kurulu/eşdeğer kontrolü | işlendi: aaa5dd0 |

### Sıra 1 — site yapımı / tasarım / prompt
| id | süre | başlık (kısa) | Desktop notu | durum |
|---|---|---|---|---|
| ptGXxk1-Uj4 | 15.2 | Opus 5.5 ile ödüllü 3D site (Yıldız Dikme) | Site/UI teknikleri + prompt anatomisi zorunlu; web-sahne-desenleri ile karşılaştır (aynı kanal önceki videoları) | işlendi: 57a0138 |
| 86HM0RUWhCk | 27.9 | Beautiful websites with CC (Nate Herk) | uçtan uca iş akışı + prompt anatomisi; açıklama 9 link | işlendi: 3e42f9f |
| Ysr7oNDajJI | 12.9 | Claude Design skills for beautiful sites | 7 GitHub repo; her biri araç adayı; frontend departmanı | işlendi: 57a0138 |
| Q9ty3eopOPs | 20.1 | Top 10 frontend design skills/plugins/CLIs | 7 repo; kurulu olanlar (impeccable, frontend-design vb.) ZATEN VAR + yeni kullanım ÖĞREN | işlendi: e71132a |
| n5eIrepe-Fg | 10.9 | AI slop olmayan web sitesi (GPT-6 ASTRA) | model bağımsız teknikleri ayır; anti-slop kuralları design-stack ile karşılaştır | işlendi: e71132a |
| Pj2FnVE-W3c | 18.3 | Kaliteli site 5 aşama (Esad Kılıç) | aşamalar → frontend-craft akışıyla eşleştir; eksik aşama UYARLA | işlendi: e71132a |
| BdLrWHzdYt4 | 14.9 | CC + Nano Banana Pro + Kling ile 3D site | görsel/video üretim hattı; asset bütçesi (GLB/video), ücretli servis tavanı | işlendi: 83e8d83 |
| M9qgd_KJkWc | 0.7 | CC killed $10k websites | kanıt iddiası → iddia sınama; teknik varsa Site/UI | işlendi: 7bc7142 |
| BK9P0rYIQY8 | 0.8 | AI websites look fake — 3 skills | 3 skill; kurulu kontrolü | işlendi: 7bc7142 |
| 0JZtdAtJiyk | 1.0 | Top 3 skills for non-designers | bAhPV1Sl-rg ile aynı başlık; karşılaştır | işlendi: 7bc7142 |
| bAhPV1Sl-rg | 0.8 | Top 3 skills for non-designers (Yury AI) | 0JZtdAtJiyk ile aynı konu | işlendi: 7bc7142 |
| O1zei0WXHvY | 1.2 | Open-source Claude Design (ücretsiz) | repo adı; claude-design MCP'mizle karşılaştır | işlendi: 7bc7142 |
| V-CIbnAAhc4 | 0.6 | CC + Google Stitch entegrasyonu | Stitch MCP kurulu → ZATEN VAR; akış ÖĞREN | işlendi: 7bc7142 |
| Vngbdm2IEXM | 1.1 | UI concept: Figma + AE + Blender | tasarım tekniği (Site/UI); 3D + hareket | işlendi: 7bc7142 |
| q1QQN08ZK6I | 1.0 | Living hero section (UI × 3D × motion) | hero tekniği; web-sahne-desenleri | işlendi: 7bc7142 |
| eKnpRVgqXR8 | 1.1 | UI tutorial Figma + Blender | tasarım tekniği | işlendi: 4d1c6d8 |
| 9opJeH9j9qs | 0.9 | UX/UI concept Figma + AE + Blender | tasarım tekniği | işlendi: 4d1c6d8 |
| -_S3KD0ZIfI | 0.9 | GPT 6 Astra → Blender | 3D varlık üretimi (Blender otomasyonu) | işlendi: 4d1c6d8 |
| AAtagrbBOto | 1.1 | CC motion design studio (Remotion) | Remotion skill; video/hareket | işlendi: 4d1c6d8 |

### Sıra 2 — araç / skill / plugin / MCP / resmi kaynak
| id | süre | başlık (kısa) | Desktop notu | durum |
|---|---|---|---|---|
| gv0WHhKelSE | 25.9 | Claude Code best practices (Anthropic) | RESMİ kaynak: her öneri kural adayı → kural çifti; iddialar birincil kaynak | işlendi: 83e8d83 |
| Nn0OyCWer1k | 1.9 | "I built Claude Code. Use Subagents." | alt ajan kullanım ipuçları; suite-kosucu/araştırıcı düzenimizle karşılaştır | işlendi: 4d1c6d8 |
| ZAaxx3qyT8g | 7.6 | CC agent dashboard | -INveHwbRz4 ile aynı özellik (agent view); sürüm/özellik | işlendi: 83e8d83 |
| -INveHwbRz4 | 0.7 | Introducing agent view (Claude resmi) | resmi özellik duyurusu | işlendi: 4d1c6d8 |
| j7Fyi5gQ85k | 44.5 | Sıfırdan Jev Masterclass (Burhan) | JEV TAM KULLANIM: bizim jev CLI/hook/kalibre ile karşılaştır; bilmediğimiz özellik → ÖĞREN/UYARLA | işlendi: 090d56a |
| Wz4qYO-91zg | 11.0 | Jev: 75 kat hızlı karar | Jev iddiaları → iddia sınama (13b kalibrasyonumuz) | işlendi: 090d56a |
| EJyuu6zlQCg | 16.7 | 5 skills I use daily (Matt Pocock) | kaynak mattpocock/skills ile birlikte | işlendi: 090d56a |
| zKBPwDpBfhs | 27.3 | Master 95% of CC skills (Nate Herk) | skill yazım/kullanım mekanizmaları; writing-skills ile karşılaştır | işlendi: 82f64da |
| 4XqVR6xI6Kw | 15.2 | One plugin 10x'd CC | 1 repo; araç adayı | işlendi: 82f64da |
| V2RIVnGCy74 | 17.5 | 17 Claude plugins (Chase AI) | 12 repo — en geniş; kurulu/eşdeğer kontrolü önce | işlendi: 82f64da |
| OFyECKgWXo8 | 17.8 | 10 CC plugins (Chase AI) | V2RIVnGCy74 ile örtüşme | işlendi: 1e2fb05 |
| uuUo7gWuH9w | 21.9 | Only CC plugins you need (Tech With Tim) | 3 repo | işlendi: 1e2fb05 |
| ZSvcxjNZdxk | 19.3 | 100+ skills, best 6 (Tech With Tim) | 4 repo | işlendi: 1e2fb05 |
| L2JKgj7WzU4 | 21.3 | 6 CC GitHub repos | 6 repo | işlendi: 77c718f |
| jqoFP9QapXI | 16.2 | 32 tricks (Nate Herk) | her hile ayrı ipucu/kural adayı (T0) | işlendi: 77c718f |
| cAeQjck1jHs | 16.2 | 9 skills daily (Zinho) | skill adları | işlendi: 77c718f |
| kMk4pvFJ13s | 17.3 | 5 skills worth $500K | skill adları | işlendi: f9416d2 |
| 3XIGcM7VICc | 20.2 | 6 AI skills (Nate Herk) | GÖRÜLDÜ (eski akış) → yeni hatla yeniden | işlendi: f9416d2 |
| 40KWXNxzgPA | 0.7 | Strix: uygulamana saldır | GÖRÜLDÜ; strix kurulu → ZATEN VAR + yeni kullanım | işlendi: 4d1c6d8 |
| FAN5w6y-rgk | 0.9 | CC'nin en büyük sorununu çözdüm (Ömer Göçmen) | 9 link; çözülen sorun ve mekanizma | işlendi: 4d1c6d8 |
| g3Mh8Hws-jo | 1.8 | Hackathon winner CC setup | rABIViSQmsc ile aynı (everything-claude-code?) | bekliyor |
| rABIViSQmsc | 0.7 | Hackathon winner open-sourced setup | g3Mh8Hws-jo ile aynı konu | bekliyor |
| I0ADpAN2qT0 | 0.5 | Tüm güvenlik açıklarını bulan eklenti | güvenlik departmanı; kurulu (strix/semgrep) eşdeğer kontrolü | bekliyor |
| PWRWO749oro | 2.2 | Top 5 plugins from day one | liste | işlendi: f9416d2 |
| BiEvvC_66AQ | 0.6 | Top 5 CC skills | liste | bekliyor |
| vfLtsYbtJf0 | 1.3 | Skill that installs skills | skill-ui-cli eşdeğeri | bekliyor |
| DuDrHzaBQ3k | 0.9 | 60 AI agents inside CC | -qosBoq8V6A ile aynı konu | bekliyor |
| -qosBoq8V6A | 0.7 | Claude'da 60 ajanı aynı anda | DuDrHzaBQ3k; RAM kuralımızla çakışma notu | bekliyor |
| k0gwr-vC2Z4 | 0.8 | 6 plugins nobody uses | liste | bekliyor |
| enFgYQvI1dM | 1.3 | Most powerful free coding agent | ücretsiz ajan → L9c49WVG_ho ile birlikte değerlendir | işlendi: aaa5dd0 |
| AWBsGEuVhuE | 0.8 | 4 CC GitHub repos | 4 repo | bekliyor |
| pR2nuRcLqbI | 0.9 | CC into a dev team in 5 min | 2K1Ps-l4yxk ile aynı konu | bekliyor |
| 2K1Ps-l4yxk | 0.9 | CC'yi yazılım ekibi gibi çalıştır | pR2nuRcLqbI | bekliyor |
| jaAI2evZF44 | 1.8 | Live premium data access | MCP/veri kaynağı | bekliyor |
| DB7DFLa40N4 | 0.7 | Ücretsiz veri çeken 3 eklenti | MCP adayları | bekliyor |
| ZeLSu-ZpeAI | 0.6 | CC çalışırken para kazandıran eklenti | iddia sınama | bekliyor |
| yiO_eMIsSZQ | 0.7 | Olmazsa olmaz 3 MCP | kurulu MCP eşdeğer kontrolü | bekliyor |
| aX7QAfld7hs | 1.3 | 5 MCP servers | kurulu MCP eşdeğer kontrolü | bekliyor |
| UI-FviGoSuY | 0.7 | 181 yetenek tek pakette | paket içeriği; departman envanteriyle karşılaştır | bekliyor |
| N3zTn2Q1spI | 0.8 | 35 prompt hatasını engelle | kural/prompt adayları (T0) | bekliyor |
| geuBwE3l0HM | 1.1 | 5 free GitHub repos | repo adları | bekliyor |
| 4qIZmI_1Zgs | 1.5 | 1000 free APIs for CC | kaynak listesi | bekliyor |
| DQtj7GJE8-I | 1.4 | Full app with AI, no code | iş akışı | bekliyor |

### Sıra 3 — genel iş akışı ve diğer alanlar
| id | süre | başlık (kısa) | Desktop notu | durum |
|---|---|---|---|---|
| CzGKgU26dP8 | 0.8 | Video kurgusunu otomatikleştirdim (Burhan) | zm6qZXGbFvU ile aynı başlık; kaynak calesthio/OpenMontage ile birlikte | bekliyor |
| zm6qZXGbFvU | 0.8 | Video kurgusunu otomatikleştirdim (Burhan) | CzGKgU26dP8 | bekliyor |
| duRYNLlG9TM | 0.8 | OmniVoice: 600+ dilde ses klonlama | araç; lisans/güvenlik | bekliyor |
| EL9iPRnoWl4 | 0.6 | 270 AI uzmanıyla ajans | ajan paketi | bekliyor |
| sUN3y3CRylc | 0.8 | Google'dan 15 ücretsiz AI aracı | liste | bekliyor |
| 5KX8wIu7g_A | 1.6 | AI agents on your team | platform | bekliyor |
| I7B7-R-4s9c | 1.7 | 5 Claude features run your business | özellikler | bekliyor |
| JhM-rGP5Kx0 | 1.4 | Social media team with 0 employees | 3 link; iş akışı | bekliyor |
| DSTOK9Ui2rw | 1.6 | 4 skills for resume | job-search ile ilgili; skill adayları | bekliyor |
| JLxM8NjvuEw | 0.7 | Claude room redesign | görsel üretim kullanımı | bekliyor |

### Kaynaklar (video değil; `video on --repo` + araştırıcı)
| kaynak | ilgili video | Desktop notu | durum |
|---|---|---|---|
| github.com/mattpocock/skills | EJyuu6zlQCg | skill'ler tek tek; writing-skills/superpowers ile çift kontrolü | bekliyor |
| github.com/gsd-build/get-shit-done | — | iş akışı/ajan sistemi; surec departmanı | bekliyor |
| github.com/mksglu/context-mode | Parti D (v-vRYtvWDYs) | Parti D'de araştırıldı (T2, Elastic-2.0); tekrar araştırma YOK, karar Parti D katmanında | bekliyor |
| github.com/worldflowai/everything-claude-code | g3Mh8Hws-jo, rABIViSQmsc | kurulu olabilir (everything-claude-code envanterde) → ZATEN VAR + bizde olmayan bileşenler | bekliyor |
| github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-code-setup | — | RESMİ plugin; kurulum ve öneri mekanizması | bekliyor |
| github.com/calesthio/OpenMontage | CzGKgU26dP8, zm6qZXGbFvU | video kurgu otomasyonu; lisans + güvenlik ön taraması | bekliyor |

## Eklenen: 2026-10-03 (kaynak: Ömer · KANAL-2b C4)

| id | süre | başlık (kısa) | not | durum |
|---|---|---|---|---|
| jDtLcMOLjIQ | 1.0 | 8 Claude Skills that actually matter | kaynak: Ömer | bekliyor |
| VRtD88WgaBk | 2.5 | Top 10 NEW Github Repos Every Claude User Must Try | kaynak: Ömer | bekliyor |
| b2QkhmQ0sT0 | 20.5 | How I Review AI Code - (Meta Senior Staff Engineer) | kaynak: Ömer | bekliyor |
| VRqW0d8-dIU | 1.6 | Someone just gave Claude Code permanent memory and It's Free | kaynak: Ömer | bekliyor |
| OLsE1GReCBs | 0.8 | Use these 4 AI Plugins to stop your AI from creating generic | kaynak: Ömer | bekliyor |
| bVXiNb9RyyI | 1.8 | How an Anthropic designer uses Claude Slides | kaynak: Ömer | bekliyor |
| yZdxHcgCsmI | 0.6 | Open Montage is a Free Agentic Video Production Agent for cr | kaynak: Ömer | bekliyor |
| fZIBK_4fKq8 | 0.5 | Use Claude Code for free with unlimited usage using Omnirout | kaynak: Ömer | bekliyor |
| RshyfhbaNHA | 0.4 | I Built a $10,000 3D Website with FREE AI Tools in 5 Minutes | kaynak: Ömer | bekliyor |
| eWdvFbDxkJE | 1.2 | Top 5 Claude Code Plugins (2026) | kaynak: Ömer | bekliyor |
| zaBDyEfhrnk | 0.4 | Turn ideas into fully animated 3D sites in seconds #webdesig | kaynak: Ömer | bekliyor |
| 9hetShMMp2s | 11.3 | Claude Code Mods Are Game Changers. Set Up These 5 NOW. | kaynak: Ömer | bekliyor |
| Rn4nmFRPe0s | 9.2 | Claude Mods Is The Biggest Claude Code Upgrade Since Skills | kaynak: Ömer | bekliyor |
| VVDV2m78qa4 | 0.7 | An AI model 100 times faster and cheaper than Claude: JEV | kaynak: Ömer | bekliyor |
| d_UE-wHLoZY | 0.8 | My New UI design Tutorial: Figma → AI → Blender | kaynak: Ömer | bekliyor |
| UcWTeZepXJc | 0.5 | This AI Builds 3D Websites From One Prompt | kaynak: Ömer | bekliyor |
| Ig3k61xIEvc | 10.2 | NEW Claude Code Mod Update! | kaynak: Ömer | bekliyor |
| EIoPt1ry6ng | 113.2 | Claude Code'u nasıl kullanıyorum? Sıfırdan AI destekli uygul | kaynak: Ömer | bekliyor |
| rMw6YJz0Ows | 0.6 | Google just dropped over 100 AI skills that make your Claude | kaynak: Ömer | bekliyor |
| 08lDzkR6UrA | 0.3 | You don't need a subscription to use the top AI video models | kaynak: Ömer | bekliyor |
| 7eVylM1pTrA | 0.7 | 3 Free AI PLugins to Turn Claude Code Into an SEO Expert | kaynak: Ömer | bekliyor |
| gKRrT6biuag | 32.8 | Claude Sonnet 5.5 vs Opus 5.5: Aynı PRD ile 3D Oyun Yaptırdı | kaynak: Ömer | bekliyor |
| XjCOxsRU3N8 | 0.4 | Anthropic Releases 13 Free Certificate Courses for Claude an | kaynak: Ömer | bekliyor |
| NOnIrDx2b_4 | 0.8 | Top 4 Claude Code Plugins to use while Vibe Coding | kaynak: Ömer | bekliyor |
| cCfOfjRaEGc | 0.3 | free-claude-code: Run Claude Code Without Paying Anthropic | kaynak: Ömer | bekliyor |
| FIiV06klo4E | 9.6 | 0928 opus55 final2 | kaynak: Ömer | bekliyor |
| BJhyAatSo1A | 1.4 | This New Skill Let You Vibe Code Apple Level Websites | kaynak: Ömer | bekliyor |
| jH1IjqI3Pi4 | 20.0 | THE FEATURE THAT BOOSTS PRODUCTIVITY / CLAUDE MODS | kaynak: Ömer | bekliyor |
| 6ZSfOO-ZvOs | 1.1 | DeepSeek's New AI Coding Tool is a Game Changer! What is Dee | kaynak: Ömer | bekliyor |
| x3SZvxoOmi0 | 21.7 | How to Create UI Designs for After Effects (Viral Apple Styl | kaynak: Ömer | bekliyor |
| 9C4TRbucmhQ | 15.7 | This 1 Claude Skill fully replaces your Higgsfield Subscript | kaynak: Ömer | bekliyor |
| QIevCKcRbUs | 1.1 | Run Claude Code FREE W/ Unlimited Usage | kaynak: Ömer | bekliyor |
| 1YAss6m8QDo | 0.6 | Mimic tool converts apps into Python code for easy access | kaynak: Ömer | bekliyor |
| Uc18mso08Ro | 1.0 | I Accidentally Turned Claude Into a Hacker... | kaynak: Ömer | bekliyor |
| OXBdKEpHEOI | 8.8 | Claude Opus 5.5 + Fable 5.1 for FREE? (It Actually Works!) | kaynak: Ömer | bekliyor |
| w3Lb7N3MxIg | 11.2 | How to use Claude Code For Free in 2026 | kaynak: Ömer | bekliyor |
| cf6zi39Aaq0 | 8.1 | Yapay Zeka Uygulamalarında Pazar Henüz Boş | kaynak: Ömer | bekliyor |
| 185XGEMefgc | 12.4 | MCP vs API: Why traditional APIs are failing AI agents | kaynak: Ömer | bekliyor |
| _5S2LyYQ_Ys | 20.0 | CLAUDE BUNU DA YAPTI (Bu Kadar İyi Olmamalıydı..) | kaynak: Ömer | bekliyor |
| Zs3faMCDYNs | 14.9 | Turn Claude Code Into Your AI Operating System (4 Layers) | kaynak: Ömer | bekliyor |
| z8UPAVTh2aE | 8.2 | How To Make Your GitHub Stand Out (Gets You Hired!) | kaynak: Ömer | bekliyor |
| 83YfBtINu74 | 0.5 | Get Paid While Claude Code Thinks: Introducing Kickbacks.ai! | kaynak: Ömer | bekliyor |
| BwSMNbleLAE | 0.6 | How To Build Fully Interactive 3D Websites using Claude Code | kaynak: Ömer | bekliyor |
| doR2RhsneRA | 20.6 | This Is What $2,175 of Opus 5.5 Tokens Can Do... | kaynak: Ömer | bekliyor |
| t7uIIuYX2lw | 1.3 | Graph Engineering Nedir? | kaynak: Ömer | bekliyor |
| AlqUtIHHuvI | 24.8 | 7 Free GitHub Repos That Make Claude So Good It Feels Illega | kaynak: Ömer | bekliyor |
| 747ZnEtsRbg | 20.3 | How to Make Insane Motion Graphics With Opus 5.5 | kaynak: Ömer | bekliyor |
| rgSR8ggOwV4 | 1.9 | This Claude MCP Tool Replaces Your Entire Marketing Stack in | kaynak: Ömer | bekliyor |
| C1yAkQ9Y2BI | 8.9 | Claude Code ile Tasarım Harikası Web Siteleri Yap! (Artık Ço | kaynak: Ömer | bekliyor |
| ew2ev-VsknQ | 15.6 | I Solved Claude Code's Biggest Problem: It Doesn't Forget An | kaynak: Ömer | bekliyor |
| 0i65C2vzjpw | 8.8 | How to Get Claude Opus 5 & Kimi K3 for FREE (No Credit Card) | kaynak: Ömer | bekliyor |
| 1M-z8O29ML8 | 18.7 | You're Using Jev + Claude Wrong | kaynak: Ömer | bekliyor |
| GPpYwjMoLio | 10.3 | I Built $10000 Website With Free Al Tools In 10 Minutes / Fr | kaynak: Ömer | bekliyor |
| 6CaQ9ZFuuKI | 21.1 | Claude Code: The Complete AI-Native SDLC Guide | kaynak: Ömer | bekliyor |
| aZe5ZTYcF1M | 9.9 | Sonnet 5.5 Better? I Built an Award-Winning 3D Website with  | kaynak: Ömer | bekliyor |
| 3AzJh3YXfh8 | 0.8 | Cut Claude Code’s Output in Half | kaynak: Ömer | bekliyor |
| iD_L-NacyB0 | 0.6 | 5 Claude Plugins That Make AI Websites Look Premium | kaynak: Ömer | bekliyor |
| 9ywqgu3R_mw | 1.7 | This $40M Startup Was Replaced After Just 3 Days! | kaynak: Ömer | bekliyor |
| y6Jo7lq3i8s | 0.7 | How to Run Claude Code Completely Free forever (2026) | kaynak: Ömer | bekliyor |
| ccBDUlcLx9I | 4.8 | Opus 5.5 Neden Favorim Oldu? | kaynak: Ömer | bekliyor |
| w86c1q59QKU | 2.0 | This Open Source Tool Removes AI's Safety Filters | kaynak: Ömer | bekliyor |
| RYSSqlhuOkU | 0.2 | Build crazy 3D website with Claude | kaynak: Ömer | bekliyor |
| JjrbjHcS2PM | 0.5 | Claude Opus 5.5 Is Taking Over YouTube... | kaynak: Ömer | bekliyor |
| IimeDwWBtWE | 0.7 | The Official Package That Gives Claude 11 New Professions | kaynak: Ömer | bekliyor |
| SwXcetzsSeI | 1.8 | Claude, Gemini, ChatGPT, and Grok Combined Into One Tool - C | kaynak: Ömer | bekliyor |
| _SVU3oC4JX8 | 13.5 | 25 Tricks to Level Up Claude Design in 13 Mins | kaynak: Ömer | bekliyor |
| QrCqBSBHCIo | 0.7 | OmniRoute: The Only AI Endpoint You Need in 2026 | kaynak: Ömer | bekliyor |
| ZKOwrG8lnmE | 1.1 | Claude’a Ödüllü Site Yaptırdım | kaynak: Ömer | bekliyor |
| 0CtisONmL4E | 1.6 | You're Paying 20x More For Your Claude Tokens Than You Need | kaynak: Ömer | bekliyor |
| X0BKFLeoepQ | 0.8 | Analyze Content by Having Claude Watch Dozens of Videos | kaynak: Ömer | bekliyor |
| YrOczcifYbQ | 0.5 | How to Make Animated YouTube Videos with Claude Code | kaynak: Ömer | bekliyor |
| e3vex7__Pqc | 3.0 | 9 Hottest GitHub Repos For Claude Code (Oct. 2026) | kaynak: Ömer | bekliyor |
| ofqHdK9_Tmg | 0.6 | CLI Anything lets you connect Claude Code to any App you use | kaynak: Ömer | bekliyor |
| o0VU6aQg7IM | 0.4 | Stop Paying for AI APIs! Get Free Access to 100,000+ Models  | kaynak: Ömer | bekliyor |
| tTe7GOJuc0E | 2.6 | Claude Code just got a massive update #claude #tech | kaynak: Ömer | bekliyor |
| EOdXR6lU5ZA | 22.3 | This NEW Jev + Claude OS Just Changed Every AI Workflow | kaynak: Ömer | bekliyor |
| eJnk0dTaDPA | 1.9 | 5 Plugins to Make Claude Code Autonomous | kaynak: Ömer | bekliyor |
| 6mG6tS6WG00 | 18.8 | How To Use Claude Code Sub-Agents Better Than 99% of People | kaynak: Ömer | bekliyor |
| z1CcbB4Yj3U | 13.3 | Claude Design ile Web Sitemi Yaptım, Yayınladım (Tek Satır K | kaynak: Ömer | bekliyor |
| rqb994ZQ1fA | 0.8 | AI Just Replaced Expensive Website Agencies (6-Step Workflow | kaynak: Ömer | bekliyor |
| koLhN1PpZYU | 0.5 | Claude AI X Shopify for custom theme sections | kaynak: Ömer | bekliyor |
| IlGilsEsLqo | 10.2 | Claude Code ile Ücretsiz Profesyonel Video Oluştur | kaynak: Ömer | bekliyor |
| 0f4TJMg7jLA | 15.9 | Why Is This New AI So Different? / JEA | kaynak: Ömer | bekliyor |
| iTIfy4Kmeo0 | 8.6 | AWWWARDS-LEVEL CINEMATIC WEBSITE WITH GPT-6 ASTRA | kaynak: Ömer | bekliyor |
| uu-qQVfncko | 17.2 | Claude Limitlerine artık asla takılma | kaynak: Ömer | bekliyor |
| Xu2SIKz8B58 | 186.4 | CLAUDE CODE FULL KURS 3+ SAAT: Kur ve Sat (2026) | kaynak: Ömer | bekliyor |
| uWMt6KppPrM | 42.1 | Tüm Oyun Yapımı Araçları Bir Platformda - Vibe Code'lu Asset | kaynak: Ömer · takip: hayır | bekliyor |
| rcrUN04qQmc | 13.2 | AN AI THAT MAKES MONEY? And It's FREE! / MoneyPrinter | kaynak: Ömer | bekliyor |
| YDAK1lvVXho | 15.3 | I Built an Award-Worthy Website with GPT Astra! Better Than  | kaynak: Ömer | bekliyor |
| EsW_sKnkI2g | 11.8 | ChatGPT Astra 6 + Fable 5.1’e Blender Kullandırdım — Sonuca  | kaynak: Ömer | bekliyor |
| -CS8r-P3NBI | 19.9 | DeepSeek Harness: Qwen 3.8 + Ollama - Ücretsiz Claude Code | kaynak: Ömer · takip: hayır | bekliyor |
| PUtaB4uYvvA | 13.8 | How I Use GPT Astra: Create Your Own Skill | kaynak: Ömer | bekliyor |
| m-f56P_L660 | 15.3 | Claude Fable 5 Built a $10K Website in Minutes | kaynak: Ömer | bekliyor |
| tUq5cfOtfR8 | 23.6 | I Built a One-Person Design Team with Claude Design | kaynak: Ömer | bekliyor |
| 3fdb_giOrLo | 16.3 | 9 Free AI Agent Skills You NEED to Install Now | kaynak: Ömer | bekliyor |
| PJ4JAim5-jQ | 10.2 | WEB DESIGN IS HISTORY! (Claude Code + Stitch) | kaynak: Ömer | bekliyor |
| 6_rCyryA6hg | 9.9 | Claude Code Can Now Automate Your Videos (Remotion + Opus 5. | kaynak: Ömer | bekliyor |
| ljJuOxTsrtY | 17.2 | Design with Claude Code: A Crash Course | kaynak: Ömer | bekliyor |
| _gZx1IxrOrk | 5.1 | Websites Can’t Have Aura? Watch This | kaynak: Ömer | bekliyor |
| bxSr8QAQt7c | 21.9 | How To Use Claude Code In Visual Studio Code - Step by Step | kaynak: Ömer | bekliyor |
| 79hKdSVr5oE | 16.7 | USE CLAUDE COWORK FOR FREE / CLAUDE DESKTOP FREE ACCESS TRIC | kaynak: Ömer | bekliyor |
| uaVYHiF8f7k | 15.8 | Turn Claude Into a Video Editing GENIUS (in 3 simple steps) | kaynak: Ömer | bekliyor |
| QUI6Ug4cHnE | 16.7 | I Built The Ultimate Claude Website Design Skill (steal this | kaynak: Ömer | bekliyor |
| SjboYsIV67A | 0.6 | Supabase Nedir? Backend Yazmadan Proje Geliştir! #backend #c | kaynak: Ömer | bekliyor |
| e7TY56-yIvM | 12.8 | Everything You Know About Skills IS OUTDATED | kaynak: Ömer | bekliyor |
| misjUj4Q_ho | 23.0 | Building a Real App with Claude Code (Start to Finish) | kaynak: Ömer | bekliyor |
| vsGwx28z4jk | 7.0 | Anthropic Just Revealed 12 New Rules for Prompting Opus 5.5 | kaynak: Ömer | bekliyor |
| 5eBlDBD0nho | 34.9 | AI agenti od nuly: Tohle potřebujete vědět | kaynak: Ömer | bekliyor |
| qLfSDQ5NGh0 | 12.8 | He Finally 10x Claude Code With This Method | kaynak: Ömer | bekliyor |
| n1je-98lvsQ | 16.0 | Claude Managed Agents is AMAZING. Here's How to Build Any Ag | kaynak: Ömer | bekliyor |
| bhaEhOPDkXU | 17.7 | Build $30,000 Websites Using Claude Opus 5 (Higgsfield) | kaynak: Ömer | bekliyor |
| h2MjhbwVKLk | 15.4 | Build a $10K Website With GPT Astra (No Code, Full Tutorial) | kaynak: Ömer | bekliyor |
| AWzzmrCPe-A | 27.2 | Top 10 Repos explained: Archify, Omarchi, OpenMAIC, and more | kaynak: Ömer | bekliyor |
| 9afZFAUuQnc | 14.2 | Claude Opus 5.5 Is Actually INSANE for Web Design | kaynak: Ömer | bekliyor |
| eIB1pFMlpbQ | 23.9 | OpenAI Yapay Zeka Ajanları Huggingface'i Nasıl Hackledi? Adı | kaynak: Ömer | bekliyor |
| DTCyvo6cC54 | 31.0 | Every Level of a Claude Second Brain Explained | kaynak: Ömer | bekliyor |
| Zu-hJAHKJug | 13.2 | Opus 5.5 Made Claude Code Unstoppable / 7 Levels in 13 Minut | kaynak: Ömer | bekliyor |
| Da7ZuhyWACg | 9.0 | Claude Opus 5.5 Might Be The Best!!! (3D, Web Design, Animat | kaynak: Ömer | bekliyor |
| 9_SZFIW7tus | 24.7 | 5 GitHub Repos: Kill AI Slop, Go Viral, Make Money | kaynak: Ömer | bekliyor |
| 6U3k4H346Es | 20.4 | GPT-6 Astra Built a $10K Website in Minutes | kaynak: Ömer | bekliyor |
| FaChtkkG9X4 | 9.2 | New Claude Opus 5.5 ! End of Figma Web Design? | kaynak: Ömer | bekliyor |
| wVVt2eOb0L8 | 22.8 | Así Edito todos mis Vídeos con Claude Opus 5.5 en minutos y  | kaynak: Ömer | bekliyor |
| xno-O4vAx7Q | 18.4 | I Had Claude Opus 5.5 Build a Mobile App, Website and Motion | kaynak: Ömer | bekliyor |
| HRe7LxuyHy4 | 15.3 | Stop Wasting AI Credits! Higgsfield Blender Plugin Workflow  | kaynak: Ömer | bekliyor |
| L-BLg_qDrx0 | 23.8 | How to Make a 3D Scroll Animation Website in Minutes (AI + N | kaynak: Ömer | bekliyor |
| -QFHIoCo-Ko | 96.5 | Full Walkthrough: Workflow for AI Coding — Matt Pocock | kaynak: Ömer | bekliyor |
| Ua0APTMVcb8 | 12.7 | Insane GitHub Repos That 10x Your Codex And Claude Code Setu | kaynak: Ömer | bekliyor |
| OIAWkkSO4WY | 11.8 | Claude Opus 5.5 Is INSANE at Motion Graphics | kaynak: Ömer | bekliyor |
| ryX4RSMJf9Q | 21.9 | Claude ile Sıfırdan Oyun Yapıyorum (kod yok) / Bölüm 2: İlk  | kaynak: Ömer | bekliyor |
| p9pPveeSOCQ | 10.9 | The Secret to Building Premium Websites with Claude / Claude | kaynak: Ömer · yeniden: eski hat | bekliyor |
| hAYPvExWmCw | 51.6 | Hafızayı Sıfırdan Anlattım - Claude Code, Obsidian, Notebook | kaynak: Ömer · yeniden: eski hat | bekliyor |
| 818VZH9hi9A | 26.6 | Kendi "Vibe Coding" Sistemimi Kurdum (Adım Adım Rehber) | kaynak: Ömer · yeniden: eski hat | bekliyor |
| oPIhoyYzDFE | 24.8 | Yapay Zekayla Kod Yazdık, Peki Güvenli Mi? | kaynak: Ömer · yeniden: eski hat | bekliyor |
| HOHPUFauSWY | 10.8 | Claude Code'da Loop ile Kendini Test Eden Otomasyon Kurmak | kaynak: Ömer · yeniden: eski hat | bekliyor |
| oGI1YmC2L00 | 21.7 | Claude Code Skills Guide: Build Your Own AI Capabilities fro | kaynak: Ömer · yeniden: eski hat | bekliyor |
| 2WIUAp4Z8EA | 9.5 | Claude Is Lying: Test Your App With This Agent | kaynak: Ömer · yeniden: eski hat | bekliyor |
| QGyKyFcqyDE | 20.9 | Prompts Aren’t Enough! The Secret to Getting Better Results  | kaynak: Ömer · yeniden: eski hat | bekliyor |

## Bağlantılı videolar

| id | süre | başlık (kısa) | not | durum |
|---|---|---|---|---|
| nQFtsehu7h0 | 32.9 | Complete Beginner's Guide to OpenAI’s Co | bağlantılı video (b2QkhmQ0sT0) | bekliyor |
| mZzhfPle9QU | 46.2 | How I use Claude Code (Meta L7 Senior St | bağlantılı video (b2QkhmQ0sT0) | bekliyor |
