# frontend — öğrenilenler (ÖĞREN-2 G1: frontend-tasarım + 3d/görsel + oyun-mod)
Kartlar: `docs/atlas/kart.jsonl` (katman A 146 = tam kart, B 585 = betik kartı); kaynak özetleri `.kos/kopru/ogren/ozet-g1.jsonl`. Aşağıda yalnız ölçülmüş kısım.

## Hangi durumda hangi araç
- Referans siteden yön: playwright headless ölçüm (renk/boyut/tipografi) → `create-design-md` / `design-extractor` ile DESIGN.md → kod. Ağır görsel bakış gerekirse Desktop (Chrome/Figma/claude-design), sonucu metne indir.
- Kod turu: `frontend-craft` iki-pass; tur başına yalnız piksel-diff JSON'u (pixelmatch + h1/p/cta ölçüsü) oku, PNG'yi açma.
- Estetik çakışma: frontend-craft > impeccable > ui-ux-pro-max > taste-* (taste-skill kolleksiyonunun çağrısı `npx skills add …taste-skill`, tek skill adı `design-taste-frontend`).
- Animasyon: React'siz → Lenis + GSAP ya da Motion/CSS; React'li → `motion/react` (motion-foundations → motion-advanced; advanced önce foundations ister), GSAP React'te `gsap-react` + `gsap.context` + `ctx.revert()`, plugin uygulama düzeyinde bir kez kayıt.
- Sahne: three.js (npm + esbuild paketleme, CDN yok); `prefers-reduced-motion` altında Lenis başlatma. Blender -b → glb/PNG; ComfyUI RAM kuralı yüzünden denenmedi.
- Kapı: axe → Lighthouse → `fixing-motion-performance`; width/height animasyonu yerine `transform`.
- MCP: `21st` (bileşen/ilham, API anahtarı gerekir), `godot` (@coding-solo/godot-mcp, yerel node), `blender` (blender-mcp, Blender eklentisi açık), `claude-design` (köprü araçları tools/cc-kopru/tasarim.mjs).

## Kombin kartları (lab/frontend/kombin/, d3'te yeniden koşuldu)
| kart | zincir | ölçüm |
|---|---|---|
| kombin-1 | ref ölçüm → 3 yön → DESIGN.md → iki-pass → diff | diff %7,51 → %0 (2 tur) |
| kombin-2 | esbuild + three r186 + Lenis + giriş animasyonu | WebGL2, 4 renk, reduced-motion'da animasyon/Lenis yok |
| kombin-3 | axe + CDP metrik + Lighthouse + motion-perf | LayoutCount 180 → 0, TBT 20 → 0 ms, axe 0/0, LH 1/1 |
| kombin-4 | Desktop referans incelemesi → metin → CC | DENENMEDİ (Desktop bağlayıcıları CC'den çağrılamaz) |
| kombin-5 | Blender -b → PNG/glb → rembg → katman | Laplace 1265/329/9,3; rembg 106 sn |
| kombin-6 | oyun modu .ini kopyası + canvas | 14/14, 32 kare assert |

## Denenmedi / sınır
- pixeljury + ollama qwen görsel yargı adımı; kombin-2'de GSAP ScrollTrigger ve R3F dalı; ComfyUI/rojo; gerçek proje (TELVE) sayfasında kapı.
- Kartlarda kalan "belirsiz": komut 1 (figma__code-connect), sınırlar 4 (kaynakta uyarı satırı yok).
