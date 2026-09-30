# Three.js Awesome Graphics Agent Skills

- Kaynak: https://github.com/scottstts/Threejs-Awesome-Graphics-Agent-Skills (npm `threejs-awesome-graphics-agent-skills` 0.11.0, d1cb23d).
- Durum: **KURULDU** (2026-10-01, KURULUM-3Db) `npx.cmd threejs-awesome-graphics-agent-skills@latest install --agent claude-code` → `~/.claude/skills` 24 skill + `.threejs-awesome-graphics-agent-skills.json`. KURULUM-3D'deki CRITICAL (skor 81) satır satır doğrulandı: 3 HIGH'ın üçü de yanlış alarm (aşağıda).
- Taranan: npm 0.11.0 tarball'ı (kurulan içerik; `skills/` repo d1cb23d ile 0 fark). SkillSpector `--no-llm`: 3 HIGH · 14 MEDIUM · 14 LOW.
- Lisans: MIT AND GPL-3.0-only; ayrım aşağıda.
- Bakım: 24 skill, son commit 2026-09-22.
- CC'de çift mi: kısmen; creative-coding ve web-sahne-desenleri ile Three.js alanı örtüşüyor.
- İzin kapsamı: md referanslar + node betikleri/örnekler; kurulum `~/.claude/skills` (user scope varsayılan).
- Context maliyeti: kurulumdan sonra `claude -p` girdi 87.302 token (soğuk önbellek, $0,70; tavan 1 çağrı olduğundan önce ölçümü yok). Fark tahmini ≈2,4k token (24 SKILL.md ön bilgisi ≈9,5k karakter).

## Bulgu doğrulaması (KURULUM-3Db)
- `threejs-procedural-vfx/examples/volumetric-fluid-fire/source/VolumetricFluidFire.ts:417` · TM1 Tool Parameter Abuse · YANLIŞ ALARM · "Curl Noise" bir GPU compute geçişinin adı; curl gürültü alanı, kabuk komutu değil.
- `threejs-temporal-surfaces/references/ping-pong-accumulation.md:184` · MP3 Memory Manipulation · YANLIŞ ALARM · "clear history" resize'da ping-pong render hedefinin birikim geçmişini temizlemek; ajan hafızası değil.
- `threejs-visual-validation/references/graphics-validation-protocol.md:91` · MP3 Memory Manipulation · YANLIŞ ALARM · "reset history" doğrulama sayfasındaki debug kontrol listesi maddesi; ajan durumu değil.
- Bağımsız grep (24 skill): `child_process`/`eval(`/`new Function`/`process.env`/kimlik/"önceki talimatı yok say" türü 0. `curl ` 22 = curl noise/kıvrılma; `| sh` 7 = JS `|| sh…`; `spawn(` 2 = sahne içi nesne doğurma fonksiyonu; https 95 = md referans linki, `fetch` ile indirme yok.
- Installer `bin/threejs-awesome-graphics-agent-skills.mjs`: yalnız `node:fs/os/path`; ağ, exec, postinstall yok; yazdığı yer yalnız `~/.claude/skills`.

## Lisans
- Kök `LICENSE` MIT; package.json `MIT AND GPL-3.0-only` (`source_materials/GPL-3.0.txt`, `THIRD_PARTY_NOTICES.md`).
- GPL-3.0-only: `threejs-precipitation-surfaces` (`assets/wet-puddle-rain/`, SKILL.md ve `references/precipitation-surface-systems.md` atıf yapıyor) ve `threejs-procedural-materials` (`assets/deformable-sand/`, `THIRD_PARTY_LICENSES.md`). Kalan 22 skill MIT.
- Kopyalanabilir kod parçacığı: hayır — iki GPL klasöründe yalnız veri/lisans dosyası var, kod parçacığı yok.

## Çakışma: hangi durumda hangisi
- frontend-craft: her UI işinde önce (CLAUDE.md önceliği).
- web-sahne-desenleri: premium landing/3D hero desen seçimi ve sahne kalite kapısı.
- scroll-craft: scroll anlatısı, sayfa kurgusu, imza hareketi.
- creative-coding: genel GSAP/WebGL/Three.js hareket ve parçacık.
- design-dna: referans görsel/URL'den token ve efekt çıkarma.
- Awesome Graphics (kurulursa): render kalitesi tekniği (bloom, SSAO, gölge, su/bulut/atmosfer, renk derecelendirme, görsel doğrulama).
