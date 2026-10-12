# Neden AI-slop değil — 17 sitenin ölçümünden ilkeler (TASARIM-1, 12 Eki 2026)

Kaynak: `docs/tasarim/olcum/*.json` (`tools/tasarim/olc.mjs`, headless, 1440 masaüstü + iPhone 13). Siteler: webgl (activetheory, lusion, igloo, resn, immersive-g) · editoryal (locomotive, 14islands, darkroom, basement, obys, cuberto) · saas (linear, stripe) · portfolyo (rauno, emilkowal, paco, brittanychiang). Zaman aşımı: bruno-simon, vercel, raycast. Kod/varlık alınmadı, yalnız sayılar.

1. **Az renk, tek vurgu.** Görünür benzersiz renk medyanı 3; vurgu ton kümesi ≤2 olan 16/17. Slop: her bölüme ayrı vurgu.
2. **Gradyan metin yok.** 0/17. Mor→mavi gradyan 1/17 (stripe; kendi imzası, taklidi slop).
3. **Cam kart yok.** backdrop-blur kart 1/17 (stripe); blur yalnız sabit menüde (linear, paco).
4. **Yazı ailesi kimliktir.** 14/17 özel/lisanslı aile (aeonik, söhne, suisse, nb architekt…); yalnız Inter/sistem fontu 1/17.
5. **Ölçek cesur ya da bilinçli düz.** h1/gövde medyanı 2.7, sayfadaki en büyük yazı/gövde 3.4–51×; portfolyolar bilinçli düz (1.0). Slop: 2–3× orta ölçek + ortalı hero + eş 3'lü kart (0/17 bu üçlüde).
6. **Ortalı hero tek başına sorun değil** (6/17); sorun onu şablon kart satırı ve zayıf ölçekle birleştirmek.
7. **Hareket az ama her yerde tepkili.** transition taşıyan eleman medyanı ~97; prefers-reduced-motion 10/17 (a11y açığı: webgl stüdyolarının çoğu yok — biz zorunlu tutarız).
8. **Gövde küçük ve sıkı olabilir** (11–20 px, medyan 15–16); okunurluk kontrastla sağlanır (medyan kontrast 11:1).

Denetim: `plugins/frontend-craft/skills/frontend-craft/scripts/slop.mjs` bu ilkelerin ölçülebilir kısmını (8 bayrak) sayar; ≥2 bayrak = SLOP.
