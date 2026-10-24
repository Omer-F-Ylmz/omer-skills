# KAYNAK-KUTUPHANE-1, PARÇA 1 raporu (24 Eki 2026)
**Sonuç:** 678 tekil host listelendi (228 kartlı); PARÇA 1'de 49 site tarandı → 17 AL, 7 AL-ŞARTLI, 25 ATLANDI. 14 repo klonlandı (~1,1 GB, kütüphane klasörü repo dışı). Kalan 4 parça kuyrukta.

## Sayılar
- Girdi: `docs/kaynak-kutuphane/url-listesi.tsv` (kart 228 + derin json 1916 dosyadan; instagram/youtube/localhost gürültüsü süzüldü; OCR bozuk hostlar, `github.con`, `ollaya.dev`, listede duruyor, p5'te elenecek).
- Tarama: HTTP + robots.txt + sitemap (≥1 sn aralık, giriş yok), HTML + ilk 6 JS paketinden kütüphane tespiti, GitHub bağlantıları → `gh repo view` ile lisans/yıldız/son push (59 repo). 1 site zaman aşımı (originkit.dev).
- Türe göre (karar): UI bileşen 7 AL / 3 şartlı / 5 atlandı · animasyon kütüphanesi 4 / 2 / 2 · 3D 1 / 0 / 5 · font 2 / 0 / 1 · ikon 1 / 1 / 0 · şablon 0 / 0 / 5 · diğer (WebGL, scroll vb.) 2 / 1 / 7.
- Kütüphane haritası: 18 kütüphane (`kutuphane-haritasi.tsv`); en yaygın: tailwind, shadcn, next.js, lucide, gsap, lenis.
- Klonlanan 14: react-bits, fancy, kokonutui, cult-ui, componentry, canvas-ui, arc-library, vengenceui, vanta, lenis, lucide, game-icons, fontjoy, zoetrope. Her birinde `KAYNAK.md` (url, lisans, atıf, tarih).
- Çalışan deneme (adım 4): vanta+lenis+gsap ScrollTrigger+lucide SVG, headless; kanıt `kart-deneme-animasyon.md` (scrub x 74,7→288, hata 0).

## Lisans notları (K2i / okuma kuralı)
- react-bits, canvas-ui: **MIT + Commons Clause** (satış/yeniden dağıtım yasak; ürün/sitede kullanım serbest) → AL-ŞARTLI, klonlandı, bileşenleri ürün olarak dağıtma.
- remotion: özel lisans (≤3 kişilik şirket/bireysel ücretsiz) · gsap: GSAP Standard (ücretsiz) · game-icons: CC BY 3.0 atıf zorunlu · lucide: ISC.
- skecher-ui: GitHub'da lisans dosyası yok → ATLANDI. 21st.dev platformu MIT ama bileşen lisansı yazara bağlı.
- Giriş/ödeme duvarlı (sketchfab, spline, textures, lordicon ücretli kısmı) ALINMADI; CAPTCHA/giriş aşılmadı.

## Yapılmadı + neden (sessiz kapsam kırpma yok)
- Kapsam 50 siteden 49 (1 erişilemedi). Site başı 300 sayfa tarama **yapılmadı**: yalnız sitemap URL sayısı + ilk 8 örnek (`site/<host>-icerik.tsv`); öğe-düzeyi (her bileşen/ikon) envanter p2+ işi. Gerekçe: bütçe + 45 tur.
- REA `analyze_web_bundle`/design-extractor/design-dna ve Playwright ekran görüntüsü site başına **koşulmadı**; 0b yığın tespiti HTML+JS regex ile (anma sayısı; sürüm yok). Sebep: 49 site için ağır, parça 2+'a bırakıldı.
- Her varlık için ayrı deneme yapılmadı: 1 birleşik deneme (animasyon/scroll/ikon). Model/doku/font için deneme yok (3D varlıkların çoğu giriş duvarlı).
- Obsidian 30-kaynaklar özeti yazılmadı (vault yolu repoda bulunamadı); 3dicons/fontshare/googlefonts lisans sayfaları okunmadan "ATLANDI/AL" kararı verildi (envanterde işaretli).
- Zorunlu araç listesi: agent-reach, design-extractor, design-dna, image-to-code, threejs-3d-paket, gsap-skills, web-sahne-desenleri, frontend-craft, departman-frontend, impeccable, pixeljury, playwright-cli, seo-audit, accessibility-audit **çağrılmadı**, iş UI üretimi değil veri toplama/lisans envanteri; HTTP+gh+playwright(py) yeterliydi. playwright headless kullanıldı.

## Kalan parçalar (`.kos/kopru/gorev-kaynak-kutuphane-1-p<N>.md`)
p2 UI bileşen/animasyon kalan (49) · p3 ikon/3D/şablon kalan (19) · p4 ilham galerisi + eğitim (111) · p5 kartsız, ≥2 video anması (57).

## Araç·model·$ (K5)
Araçlar: python urllib/gh/git/playwright-py, ruflo pattern-search. Model: sonnet-5-5. Maliyet ≈ $1,5 (hedef $0,50 aşıldı: 50 sitelik tarama + 14 klon + ek-ayıklama turları).
Dosyalar: `tools/kk1_urller.py`, `kk1_tara.py`, `kk1_yaz.py`; `docs/kaynak-kutuphane/{envanter,kutuphane-haritasi,url-listesi}.tsv`, `site/*.md|tsv`.
