# Three.js Awesome Graphics Agent Skills

- Kaynak: https://github.com/scottstts/Threejs-Awesome-Graphics-Agent-Skills (npm `threejs-awesome-graphics-agent-skills` 0.11.0, d1cb23d).
- Durum: **KURULMADI** (2026-10-01, KURULUM-3D). SkillSpector `--no-llm`: CRITICAL / DO_NOT_INSTALL, hem repo (skor 87) hem yalnız `skills/` (skor 81); hat kuralı yalnız LOW'da kurar.
- `skills/` HIGH bulguları: `threejs-temporal-surfaces/references/ping-pong-accumulation.md` ve `threejs-visual-validation/references/graphics-validation-protocol.md` (ajan hafızası/durumu), `threejs-procedural-vfx/.../VolumetricFluidFire.ts` (parametre kötüye kullanımı). Grafik bağlamında yanlış pozitif olabilir; LLM'li tarama ya da elle inceleme Ömer kararı.
- Lisans: package.json `MIT AND GPL-3.0-only` (LICENSE dosyası MIT); GPL'li kısım belirlenmeden kurulmaz.
- Bakım: 24 skill, son commit 2026-09-22.
- CC'de çift mi: kısmen; creative-coding ve web-sahne-desenleri ile Three.js alanı örtüşüyor.
- İzin kapsamı: md referanslar + node betikleri/örnekler; kurulum `~/.claude/skills` (user scope varsayılan).
- Context maliyeti: 24 SKILL.md ön bilgisi ≈9,5k karakter ≈2,4k token (tahmin; claude -p ölçümü kurulmadığı için yapılmadı).

## Çakışma: hangi durumda hangisi
- frontend-craft: her UI işinde önce (CLAUDE.md önceliği).
- web-sahne-desenleri: premium landing/3D hero desen seçimi ve sahne kalite kapısı.
- scroll-craft: scroll anlatısı, sayfa kurgusu, imza hareketi.
- creative-coding: genel GSAP/WebGL/Three.js hareket ve parçacık.
- design-dna: referans görsel/URL'den token ve efekt çıkarma.
- Awesome Graphics (kurulursa): render kalitesi tekniği (bloom, SSAO, gölge, su/bulut/atmosfer, renk derecelendirme, görsel doğrulama).
