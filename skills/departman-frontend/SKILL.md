---
name: departman-frontend
description: "Frontend/UI müdürü: hangi tasarım aracı hangi sırayla. Arayüz, landing, bileşen, CSS/Tailwind/Razor işine başlarken önce oku."
---

# Departman: frontend — iş sırası

Ana hat `frontend-craft`. Çakışmada sıra: frontend-craft > impeccable > ui-ux-pro-max > taste-* > diğerleri; alttakinin kuralı düşer.
Katalog: `docs/departmanlar/frontend.md` · yaşam döngüsü: `docs/departmanlar/organizasyon.md`.
Ölçülü karar ağacı + kombin zincirleri (kayıtlı tur sayıları, denenmeyenler): bu klasördeki `ogren.md` — Read; oturuma yüklenmez.
Araç kataloğu: bu klasördeki `katalog.md` (araç · ne zaman · sıradaki adım) — adımdaki araç yoksa ya da emin değilsen Read; oturuma yüklenmez.
Zor iş (≥2 alan, alan dışı ya da aracın adını bilmiyorsan): `<katalog>` eki geldiyse yalnız ondan seç, ek sorgu yok; gelmediyse TEK kez Skill `yetenek-getir` (iş başına ayrı sorgu yok). Rutin tek alanlı işte katalog yok.

## Adımlar
1. **Tasarım kararı** — `DESIGN.md` yoksa önce o: mevcut ürün/site için `create-design-md`, URL'den `design-extractor` · `taste`, görselden `design-dna`. Sonra `frontend-craft` yükle (mod tespiti REF/FREE, yön keşfi → DESIGN.md → DUR). Yön keşfi görsel isterse tuval: `claude-design` · `figma` · `stitch` (DESIGN.md yine önce).
2. **Yığın** — Razor → `dotnet-aspnetcore` + `frontend-craft` · React/Next → `vercel-react-best-practices` + `vercel-composition-patterns` · Astro → `frontend-craft`.
3. **Referans ve bileşen** — `21st-ui` (get_inspiration · get_component · get_theme · search_logo), `ui-ux-pro-max` (palet, font çifti, UX kuralı), kütüphane `omer-kutuphaneler`, Figma varsa `figma`. Yalnız eksik kalan kararı sorar; DESIGN.md'yi ezmez.
4. **Yapım (iki-pass)** — `frontend-craft` Bölüm 8: pass 1 iskelet + token, pass 2 detay. Estetik yön gerekirse `impeccable`, o da yetmezse `taste-skill`; yasak liste frontend-craft'tan. Premium landing/scroll yalnız brief isterse, frontend-craft altında: `web-sahne-desenleri` · `scroll-craft`. Animasyon/efekt (giriş, scroll'la belirme, sayfa geçişi, parçacık, 3D exploded, intro video) önce `animasyon-atolyesi` tarifi (kopyala-uyarla + olc.py ölçümü), tarif yetmezse GSAP/Theatre.js/Remotion skill'leri; kaydırmaya bağlı (scroll-driven: scrub/pin) hareket doğrudan `gsap-scrolltrigger` (atölyede tarifi yok).
5. **Screenshot döngüsü** — `frontend-craft` screenshot.mjs 390/768/1440; tur = screenshot → sapma tablosu → düzelt. Min 2, **en fazla 4 tur**; 4. turda sapma sürüyorsa DUR raporu.
6. **Erişilebilirlik (axe)** — frontend-craft audit.mjs; bulgu varsa `fixing-accessibility`, teslim öncesi `accessibility-review` (yalnız Desktop/claude.ai; CC'de kapalı). Kontrast, klavye, odak, alt metin 0 hata.
7. **Performans** — `fixing-motion-performance` · `performance-optimization`; React'te `vercel-react-best-practices`. Kapı: Web Vitals/Lighthouse sayısı raporda.
8. **Görsel QA** — `pixeljury` (görsel regresyon), akış/etkileşim `playwright-cli`; tarayıcıda deneme ve e2e → `departman-test-qa`.
9. **Güvenlik** — form, auth, dış istek, CSP/header varsa → `departman-guvenlik` (frontend adımı).
10. **Kapanış** — `design-critique` (yalnız Desktop/claude.ai; CC'de kapalı), tur raporu (frontend-craft ÇEKİRDEK formatı), omer-kurallar:15 altı madde (fonksiyon · güvenlik · bağımlılık · ZAP · KVKK · SEO/A11y; SEO için `fixing-metadata`).

## Kapılar
- DESIGN.md olmadan kod yok (REF modunda referans kazanır).
- Screenshot turu sayıyla raporlanır; 4 turu aşmak yasak.
- a11y 0 hata ve performans sayısı olmadan görsel QA'ya geçilmez; görsel QA geçmeden kapanış yok.
- Kütüphane yalnız omer-kutuphaneler rafından, gerekçesiz eklenmez; TS projesinde lint: oxlint + dmmulroy/anti-slop kural seti (MIT), proje devDependency'si, sürüm sabit; global kurulmaz (IG-18 DdrNeEUN63i).

## Yapım promptu şablonu ve kurulu araç notları
Site/UI'ı başka ajana yaptırırken ve scroll-craft/design-dna/atlas notları için `references/yapim-promptu-ve-notlar.md` dosyasını oku.

## Çakışma
- İki skill aynı kararı veriyorsa üstteki kazanır (sıra yukarıda); DESIGN.md her skill'den önce gelir.
- Referans skill'leri (21st, ui-ux-pro-max, design-dna, taste) öneri verir; kararı frontend-craft adımı yazar.
- Aynı işi yapan ikinci aracı yükleme: bu listede adı geçmeyen tasarım skill'i ancak katalogdaki "ne zaman" eşleşirse.
Videodan gelen teknikler: docs/departmanlar/frontend.md `## Teknikler` (`video teknik`); öneriler bekleyen/teknik-*.md, onaysız eklenmez.

<!-- profil-disi:bas -->
## Profil dışı üyeler (yalnız CC)
Proje profili bu üyeleri listeden çıkarır. Skill aracıyla çağrılamıyorsa `<ad>` yerine üye adını koyup SKILL.md'yi Read ile aç; references dosyalarını SKILL.md'nin klasörüne göre, görev gerektirdiğinde oku. claude.ai/Desktop'ta bu Windows yolları geçersiz; bölümü yok say.
- design-mastery (4): brand-systems, design-masters, design-movements, design-principles · `C:/Users/pc/.claude/plugins/cache/design-mastery/design-mastery/1.0.0/skills/<ad>/SKILL.md`
- taste-skill (13): brandkit, brutalist-skill, gpt-tasteskill, image-to-code-skill, imagegen-frontend-mobile, imagegen-frontend-web, minimalist-skill, output-skill, redesign-skill, soft-skill, stitch-skill, taste-skill, taste-skill-v1 · `C:/Users/pc/.claude/plugins/cache/taste-skill/taste-skill/1.0.0/skills/<ad>/SKILL.md`
- ui-ux-pro-max (1): ui-ux-pro-max · `C:/Users/pc/.claude/skills/<ad>/SKILL.md`
<!-- profil-disi:son -->


Slash katalog (iş türü → /komut·skill): `yetenek-getir/reference/slash-katalog.md` — Read; oturuma yüklenmez.

Kombo adayları (A/B ölçümü geçmedi; önerme, yalnız ipucu): fe-referans-diff, fe-a11y-perf-kapisi, fe-sahne-animasyon, fe-desktop-referans-devri, fe-pixeljury-yargi.

Ders kitabı (web okulu, alıntı denetimli): `docs/okul/web-s1.md` (temel) · `docs/okul/web-s2.md` (animasyon/scroll) · taslak: `docs/okul/web-taslak.md`, Read; oturuma yüklenmez.

<!-- dizin:bas -->
## Dizin: adımdaki araç işe uymuyorsa `references/dizin.md` dosyasını oku, listeden adla çağır.
<!-- dizin:son -->
Yeni aileler (SKILL-YUKLE-1, 35): `references/yukle-1-aileler.md` — Read.
