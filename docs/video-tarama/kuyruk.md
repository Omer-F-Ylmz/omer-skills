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
| kHtOSJRUkLs | 19.8 | Never run out of tokens (Sharbel) | yapıştırılan talimat/konfigürasyon: tasarruf mekanizması, bizde CLAUDE.md/Headroom/RTK karşılığı | bekliyor |
| 6cEQEba0i2A | 10.7 | Save millions of Claude tokens (Nate Herk) | açıklamada 9 link; her teknik ayrı özellik, tasarruf ayrıştırma | bekliyor |
| g89FJiNAlEs | 15.1 | 4 free repos cut token usage | 4 GitHub repo; her biri araç adayı + mekanizma; Headroom/RTK/context-mode ile çakışma | bekliyor |
| V0XbuApxlhg | 19.0 | Paying Anthropic 20x more (Chase AI) | model/plan/effort seçimi iddiaları → iddia sınama (bizim ölçümlerimiz: effort A/B, Opus/Sonnet) | bekliyor |
| oHKt0FUbR58 | 0.8 | Free repo fixes token limits | repo adı ekranda/açıklamada; araç adayı | işlendi: aaa5dd0 |
| bS6IlkUozAI | 1.7 | Web browsing tokens −90% | tarayıcı/web getirme sıkıştırma aracı; bizde video getir + Headroom karşılaştırması | işlendi: aaa5dd0 |
| NogIRR1B6gY | 0.7 | PDF'ler token tüketmesin | PDF okuma stratejisi; pdf-reading skill ile karşılaştır | işlendi: aaa5dd0 |
| klDiYMzW0o0 | 0.7 | Token harcamanı yarıya indiren 4 araç | 4 araç; kurulu olanlar ZATEN VAR, yeniler DENE | işlendi: aaa5dd0 |
| lipJRiztOgM | 0.7 | 5 skills save 10x sessions | skill adları; kurulu/eşdeğer kontrolü | işlendi: aaa5dd0 |

### Sıra 1 — site yapımı / tasarım / prompt
| id | süre | başlık (kısa) | Desktop notu | durum |
|---|---|---|---|---|
| ptGXxk1-Uj4 | 15.2 | Opus 5.5 ile ödüllü 3D site (Yıldız Dikme) | Site/UI teknikleri + prompt anatomisi zorunlu; web-sahne-desenleri ile karşılaştır (aynı kanal önceki videoları) | bekliyor |
| 86HM0RUWhCk | 27.9 | Beautiful websites with CC (Nate Herk) | uçtan uca iş akışı + prompt anatomisi; açıklama 9 link | bekliyor |
| Ysr7oNDajJI | 12.9 | Claude Design skills for beautiful sites | 7 GitHub repo; her biri araç adayı; frontend departmanı | bekliyor |
| Q9ty3eopOPs | 20.1 | Top 10 frontend design skills/plugins/CLIs | 7 repo; kurulu olanlar (impeccable, frontend-design vb.) ZATEN VAR + yeni kullanım ÖĞREN | bekliyor |
| n5eIrepe-Fg | 10.9 | AI slop olmayan web sitesi (GPT-6 ASTRA) | model bağımsız teknikleri ayır; anti-slop kuralları design-stack ile karşılaştır | bekliyor |
| Pj2FnVE-W3c | 18.3 | Kaliteli site 5 aşama (Esad Kılıç) | aşamalar → frontend-craft akışıyla eşleştir; eksik aşama UYARLA | bekliyor |
| BdLrWHzdYt4 | 14.9 | CC + Nano Banana Pro + Kling ile 3D site | görsel/video üretim hattı; asset bütçesi (GLB/video), ücretli servis tavanı | bekliyor |
| M9qgd_KJkWc | 0.7 | CC killed $10k websites | kanıt iddiası → iddia sınama; teknik varsa Site/UI | bekliyor |
| BK9P0rYIQY8 | 0.8 | AI websites look fake — 3 skills | 3 skill; kurulu kontrolü | bekliyor |
| 0JZtdAtJiyk | 1.0 | Top 3 skills for non-designers | bAhPV1Sl-rg ile aynı başlık; karşılaştır | bekliyor |
| bAhPV1Sl-rg | 0.8 | Top 3 skills for non-designers (Yury AI) | 0JZtdAtJiyk ile aynı konu | bekliyor |
| O1zei0WXHvY | 1.2 | Open-source Claude Design (ücretsiz) | repo adı; claude-design MCP'mizle karşılaştır | bekliyor |
| V-CIbnAAhc4 | 0.6 | CC + Google Stitch entegrasyonu | Stitch MCP kurulu → ZATEN VAR; akış ÖĞREN | bekliyor |
| Vngbdm2IEXM | 1.1 | UI concept: Figma + AE + Blender | tasarım tekniği (Site/UI); 3D + hareket | bekliyor |
| q1QQN08ZK6I | 1.0 | Living hero section (UI × 3D × motion) | hero tekniği; web-sahne-desenleri | bekliyor |
| eKnpRVgqXR8 | 1.1 | UI tutorial Figma + Blender | tasarım tekniği | bekliyor |
| 9opJeH9j9qs | 0.9 | UX/UI concept Figma + AE + Blender | tasarım tekniği | bekliyor |
| -_S3KD0ZIfI | 0.9 | GPT 6 Astra → Blender | 3D varlık üretimi (Blender otomasyonu) | bekliyor |
| AAtagrbBOto | 1.1 | CC motion design studio (Remotion) | Remotion skill; video/hareket | bekliyor |

### Sıra 2 — araç / skill / plugin / MCP / resmi kaynak
| id | süre | başlık (kısa) | Desktop notu | durum |
|---|---|---|---|---|
| gv0WHhKelSE | 25.9 | Claude Code best practices (Anthropic) | RESMİ kaynak: her öneri kural adayı → kural çifti; iddialar birincil kaynak | bekliyor |
| Nn0OyCWer1k | 1.9 | "I built Claude Code. Use Subagents." | alt ajan kullanım ipuçları; suite-kosucu/araştırıcı düzenimizle karşılaştır | bekliyor |
| ZAaxx3qyT8g | 7.6 | CC agent dashboard | -INveHwbRz4 ile aynı özellik (agent view); sürüm/özellik | bekliyor |
| -INveHwbRz4 | 0.7 | Introducing agent view (Claude resmi) | resmi özellik duyurusu | bekliyor |
| j7Fyi5gQ85k | 44.5 | Sıfırdan Jev Masterclass (Burhan) | JEV TAM KULLANIM: bizim jev CLI/hook/kalibre ile karşılaştır; bilmediğimiz özellik → ÖĞREN/UYARLA | bekliyor |
| Wz4qYO-91zg | 11.0 | Jev: 75 kat hızlı karar | Jev iddiaları → iddia sınama (13b kalibrasyonumuz) | bekliyor |
| EJyuu6zlQCg | 16.7 | 5 skills I use daily (Matt Pocock) | kaynak mattpocock/skills ile birlikte | bekliyor |
| zKBPwDpBfhs | 27.3 | Master 95% of CC skills (Nate Herk) | skill yazım/kullanım mekanizmaları; writing-skills ile karşılaştır | bekliyor |
| 4XqVR6xI6Kw | 15.2 | One plugin 10x'd CC | 1 repo; araç adayı | bekliyor |
| V2RIVnGCy74 | 17.5 | 17 Claude plugins (Chase AI) | 12 repo — en geniş; kurulu/eşdeğer kontrolü önce | bekliyor |
| OFyECKgWXo8 | 17.8 | 10 CC plugins (Chase AI) | V2RIVnGCy74 ile örtüşme | bekliyor |
| uuUo7gWuH9w | 21.9 | Only CC plugins you need (Tech With Tim) | 3 repo | bekliyor |
| ZSvcxjNZdxk | 19.3 | 100+ skills, best 6 (Tech With Tim) | 4 repo | bekliyor |
| L2JKgj7WzU4 | 21.3 | 6 CC GitHub repos | 6 repo | bekliyor |
| jqoFP9QapXI | 16.2 | 32 tricks (Nate Herk) | her hile ayrı ipucu/kural adayı (T0) | bekliyor |
| cAeQjck1jHs | 16.2 | 9 skills daily (Zinho) | skill adları | bekliyor |
| kMk4pvFJ13s | 17.3 | 5 skills worth $500K | skill adları | bekliyor |
| 3XIGcM7VICc | 20.2 | 6 AI skills (Nate Herk) | GÖRÜLDÜ (eski akış) → yeni hatla yeniden | bekliyor |
| 40KWXNxzgPA | 0.7 | Strix: uygulamana saldır | GÖRÜLDÜ; strix kurulu → ZATEN VAR + yeni kullanım | bekliyor |
| FAN5w6y-rgk | 0.9 | CC'nin en büyük sorununu çözdüm (Ömer Göçmen) | 9 link; çözülen sorun ve mekanizma | bekliyor |
| g3Mh8Hws-jo | 1.8 | Hackathon winner CC setup | rABIViSQmsc ile aynı (everything-claude-code?) | bekliyor |
| rABIViSQmsc | 0.7 | Hackathon winner open-sourced setup | g3Mh8Hws-jo ile aynı konu | bekliyor |
| I0ADpAN2qT0 | 0.5 | Tüm güvenlik açıklarını bulan eklenti | güvenlik departmanı; kurulu (strix/semgrep) eşdeğer kontrolü | bekliyor |
| PWRWO749oro | 2.2 | Top 5 plugins from day one | liste | bekliyor |
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
