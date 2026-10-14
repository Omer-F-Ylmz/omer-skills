---
name: departman-frontend
description: "Frontend/UI müdürü: hangi tasarım aracı hangi sırayla. Arayüz, landing, bileşen, CSS/Tailwind/Razor işine başlarken önce oku."
---

# Departman: frontend — iş sırası

Ana hat `frontend-craft`. Çakışmada sıra: frontend-craft > impeccable > ui-ux-pro-max > taste-* > diğerleri; alttakinin kuralı düşer.
Katalog: `docs/departmanlar/frontend.md` · yaşam döngüsü: `docs/departmanlar/organizasyon.md`.
Araç kataloğu: bu klasördeki `katalog.md` (araç · ne zaman · sıradaki adım) — adımdaki araç yoksa ya da emin değilsen Read; oturuma yüklenmez.
Zor iş (≥2 alan, alan dışı ya da aracın adını bilmiyorsan): `<katalog>` eki geldiyse yalnız ondan seç, ek sorgu yok; gelmediyse TEK kez Skill `yetenek-getir` (iş başına ayrı sorgu yok). Rutin tek alanlı işte katalog yok.

## Adımlar
1. **Tasarım kararı** — `DESIGN.md` yoksa önce o: mevcut ürün/site için `create-design-md`, URL'den `design-extractor` · `taste`, görselden `design-dna`. Sonra `frontend-craft` yükle (mod tespiti REF/FREE, yön keşfi → DESIGN.md → DUR). Yön keşfi görsel isterse tuval: `claude-design` · `figma` · `stitch` (DESIGN.md yine önce).
2. **Yığın** — Razor → `dotnet-aspnetcore` + `frontend-craft` · React/Next → `vercel-react-best-practices` + `vercel-composition-patterns` · Astro → `frontend-craft`.
3. **Referans ve bileşen** — `21st-ui` (get_inspiration · get_component · get_theme · search_logo), `ui-ux-pro-max` (palet, font çifti, UX kuralı), kütüphane `omer-kutuphaneler`, Figma varsa `figma`. Yalnız eksik kalan kararı sorar; DESIGN.md'yi ezmez.
4. **Yapım (iki-pass)** — `frontend-craft` Bölüm 8: pass 1 iskelet + token, pass 2 detay. Estetik yön gerekirse `impeccable`, o da yetmezse `taste-skill`; yasak liste frontend-craft'tan. Premium landing/scroll yalnız brief isterse, frontend-craft altında: `web-sahne-desenleri` · `scroll-craft`. Animasyon/efekt (giriş, scroll, sayfa geçişi, parçacık, 3D exploded, intro video) önce `animasyon-atolyesi` tarifi (kopyala-uyarla + olc.py ölçümü), tarif yetmezse GSAP/Theatre.js/Remotion skill'leri.
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

## Yapım promptu şablonu
Site/UI'ı başka bir ajana (ya da alt ajana) yaptırırken prompt bu satırları taşır. Kural kapsamları: omer-kurallar:25 "site/UI yapım promptlarında" (teknoloji + dosya) · omer-kurallar:26 "3D/animasyonlu sahnelerde" (config); küçük işte "en basit çözüm" önde. Videolardan çıkan kalıplar: `docs/departmanlar/frontend-promptlar.md`.
- teknoloji: kütüphane + sürüm (ör. Three.js r160, GSAP 3.12, Lenis 1.1, Vite 5); yalnız omer-kutuphaneler rafından.
- dosya: dosya başına tek sorumluluk (ör. main.js sahne · style.css tipografi · config.js parametreler).
- config: ayarlanabilir sahne parametreleri (görsel sayısı, hız, boşluk) tek CONFIG nesnesi/dosyasında; yalnız 3D/animasyonlu sahnede.
- hareket: animasyon terimleriyle tarif (scroll reveal, stagger, parallax, easing, süre); prefers-reduced-motion karşılığı.
- asset: görsel/video/font listesi, oran ve ton (ör. 12 dikey fotoğraf, koyu arka plan); yoksa üretim yolu. 3D model: ~2 MB tercih (sıkıştırılmış GLB), 6 MB detay yalnız gerekçeyle (24c K7).
- kabul: ölçülebilir kabul (ör. 60 fps, 390/768/1440 taşma yok, axe 0 hata, LCP sayısı).
- dokunulmaz: hazır tasarım promptu mevcut siteye uygulanırken dokunulmaz alanlar adıyla (ör. hero, mevcut animasyonlar); prompttan yalnız ilgili bölüm alınır (K3, 24 Eyl). Elle ayarlanmış 3D pozisyon/kamera/ışık değerleri de dokunulmaz alandır (24c K7).
- bileşen: bütün butonlar tek bileşenden varyantla; hover/focus/active o bileşende (K16, 24 Eyl).
- perspektif: 3D/derinlik sahnesinde kamera açısı, perspektif ve eğim sayıyla yazılır (ör. perspective 1200px, rotateX 12°); yazılmazsa kartlar düz ya da yanlış açıda çıkar.
- klasör: görseller önce `public/` altına konur; promptta klasör adı ve dağıtım kuralı (rastgele/dengeli) verilir, ajan dosyaları kendisi yerleştirir.
- sahne: video üretim promptunda sahne sahne kamera hareketi, ışık ve atmosfer ayrı cümlelerle tarif edilir.

## Kurulu araç notları
- `scroll-craft`: görsel üretimi ücretli kie.ai API'sini çağırır; yalnız Ömer onayı ve çağrı tavanıyla ("en fazla N").
- `design-dna`: "varlığı kaynak URL'den al" adımı referans sitelerde uygulanmaz; referanstan yalnız stil/teknik alınır, görsel/font/3D model/video izinsiz kullanılmaz (lisanslı ya da müşteri varlığı).

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

<!-- dizin:bas -->
## Dizin
Adımdaki araç işe tam uymuyorsa buradan seç, adla çağır (Skill; `ajan:` = alt ajan, claude.ai'de bu klasördeki `ajanlar/<ad>.md` talimatını kendin uygula). departman-* cevap değil. Adı işini söyleyen skill'ler burada yok: listedeki adla çağır.
### claude.ai + Claude Code
ajan:bl-animasyon-anahtar: an object or camera must move
ajan:bl-dokuya-pisirme: detail must move into textures
ajan:bl-glb-disa-aktar: a model goes to three.js or the web
ajan:bl-gorsel-ani-kontrol
ajan:bl-isik-kurulumu: a scene looks flat or harsh
ajan:bl-malzeme-kurucu: a Blender object needs a realistic material
ajan:bl-mod-modeli-blender
ajan:bl-sahne-temizlik: a scene is messy before export
ajan:bl-urun-turntable
ajan:fe-animasyon-tasarimci
ajan:fe-bilesen-yazar: asked for a button, card, modal or menu
ajan:fe-bos-durum-yazar: screens show blank or raw errors
ajan:fe-css-hata-bulucu
ajan:fe-cursor-efekt
ajan:fe-dashboard-duzeni: designing admin panels or analytics screens
ajan:fe-gorsel-optimize
ajan:fe-ikon-sistemi: icons look mixed or inconsistent
ajan:fe-karanlik-mod: a site needs a dark theme
ajan:fe-meta-seo-duzeltici
ajan:fe-navigasyon-tasarimci
ajan:fe-react-bilesen-inceleme
ajan:fe-responsive-kontrol
ajan:fe-scroll-hikayesi
ajan:fe-slayt-kurucu: asked for web based presentations
ajan:fe-tailwind-duzenleyici
ajan:fe-tasarim-incele
ajan:fe-tasarim-sistemi-kurucu
ajan:fe-tasarim-yonu
ajan:fe-tipografi-uzmani: text looks flat, crowded or inconsistent
ajan:fe-ux-metin-yazar
ajan:fe-webgl-3d-hero
ajan:fe-yazdir-stili: a page must print or export well
ajan:otm-webhook-tasarimci
ajan:oyn-dusman-ai: enemies feel dumb or unfair
ajan:oyn-mod-paketleme: Packages mods with clear folder layout, readme and
ajan:oyn-oyun-dokuman: a game idea needs shape
ajan:oyn-three-oyun-sahne
ajan:vid-hareket-grafigi: graphics must move cleanly
ajan:vid-hyperframes-kompozisyon: a motion piece is authored as web code
ajan:vid-video-performans-web
banana: Generate, edit, compare, and review images with Google
baseline-ui: kaçın: genel UI cilası → frontend-craft
img: Generate, edit, or plan images with OpenAI gpt-image-2
improve-ui: kaçın: genel UI cilası → frontend-craft
mod-atolyesi: 3DMigoto mod atölyesi — Genshin (standalone) · ZZZ/HSR/WuWa
omer-kutuphaneler: ılır, pinli kurulum satırı, lisans ve context7 kimliği
### yalnız Claude Code
accessibility: WCAG 2.2 レベル AA 標準を用いてインクルーシブなデジタルプロダクトを設計・実装・監査します。Web 用のセマンティック ARIA および
adaptive: Instructions to make or update an app's UI
archify: the user asks to visualize system architecture, infrastructure
better-accessibility: Reviews and fixes keyboard and focus behavior, ARIA
break: Renders a component you choose under every scenario
browse: Drive a real browser through Aside: open a
cobejs: adding a lightweight interactive globe with cobe (canvas
competitive-analysis: you need to know what others actually do
cro: wants to optimize, improve, or increase conversions on
dependency-map: Map cross-team dependencies and the critical path for
documentation-lookup: names a framework (e.g
feedback-patterns: the system must acknowledge success or change
frontend-craft: UI jenerik/cilasız, landing iyileştir; UI işinde İLK
gpt-taste: Elite UX/UI & Advanced GSAP Motion Engineer
grill-me: A relentless interview to sharpen a plan or
handoff-protocols: Designing smooth transitions between agents and between AI
heuristic-evaluation: you need findings without recruiting participants
human-in-the-loop: Designing intervention points where humans review, approve, or
impeccable: the user wants to design, redesign, shape, critique
jakobs-law: deciding whether to innovate on a familiar pattern
journey-map: improving an existing experience
loading-states: content takes time to arrive
matterjs: implementing 2D physics interactions with Matter.js, including Engine/World
mcp:infinite-canvas: sonsuz tuval: eskiz, akış şeması, moodboard
mentorship: Mentor designers and emerging leaders
navigation-event: Intercept back gestures and run Predictive Back animations
offers: wants to design, construct, or improve an offer
opportunity-framework: there are more ideas than capacity
pixeljury: Rendered web sayfasi icin gorsel QA - Chromium'da
plugin:webgpu-threejs-tsl: WebGPU three.js TSL shader/node
prioritisation-at-scale: Prioritise design investment across a portfolio of teams
prototype: Build multiple genuinely different versions of a UI
remotion-markup: Content, animation and effects best practices
securing-resources: Secure headcount and budget for the design org
taste-distillation: the user wants to capture the look of
tastemaker: ever the user asks to build, design, style
troubleshooting: Uses Chrome DevTools MCP and documentation to troubleshoot
vantajs: adding animated WebGL background effects with Vanta.js (setup
variant: Builds multiple variants of a component you're working
<!-- dizin:son -->
