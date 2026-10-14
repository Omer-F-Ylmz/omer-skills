# taste-skill — 14 benzersiz kayıt

**Amaç:** Şablon görünmeyen ön yüz tasarım zevki skill'leri: brütalist, minimalist, üst düzey görsel, GSAP hareketli sayfa, görselden koda, redesign, Stitch DESIGN.md ve marka/görsel üretim yönü.

**İç yapı:** taste-skill [plugin] + taste-skill:<stil> skill'leri; gruplar: stil (industrial-brutalist-ui, minimalist-ui, high-end-visual-design, gpt-taste), akış (design-taste-frontend, redesign-existing-projects, image-to-code, stitch-design-taste), görsel üretim (brandkit, imagegen-frontend-web, imagegen-frontend-mobile), yardımcı (full-output-enforcement).

## En güçlü parçalar
- `taste-skill:design-taste-frontend` — Brief'ten tasarım yönü çıkarıp şablon görünmeyen landing/portföy ön yüzü kurar.
- `taste-skill:redesign-existing-projects` — Var olan siteyi denetler, jenerik AI izlerini ayıklar, işlevi bozmadan yükseltir.
- `taste-skill:image-to-code` — Önce tasarım görseli üretip inceler, siteyi ona birebir kodlar.
- `taste-skill:high-end-visual-design` — Ajans kalitesi font, boşluk, gölge, kart ve animasyon kuralları.
- `taste-skill:stitch-design-taste` — Google Stitch için kurallı DESIGN.md (tipografi, renk, hareket) üretir.

## Birlikte kullanım
- taste-skill:imagegen-frontend-web → taste-skill:image-to-code: görsel referanstan koda.
- taste-skill:gpt-taste + gsap-skills: GSAP hareketli editoryal landing.
- taste-skill:full-output-enforcement uzun kod çıktısında diğer taste skill'lerine eşlik eder.

## Tuzaklar
- taste-skill:design-taste-frontend-v1 yalnız geriye uyum içindir; yeni işte kullanılmamalı.
- Stil skill'leri farklı estetikler sunar (brütalist katı ızgara, minimalist gradyansız, gpt-taste animasyonlu); bir projede tek stil seçilmeli.

## Üyeler
- plugin (1): taste-skill
- skill (13): taste-skill:brandkit, taste-skill:design-taste-frontend, taste-skill:design-taste-frontend-v1, taste-skill:full-output-enforcement, taste-skill:gpt-taste, taste-skill:high-end-visual-design, taste-skill:image-to-code, taste-skill:imagegen-frontend-mobile, taste-skill:imagegen-frontend-web, taste-skill:industrial-brutalist-ui, taste-skill:minimalist-ui, taste-skill:redesign-existing-projects, taste-skill:stitch-design-taste
