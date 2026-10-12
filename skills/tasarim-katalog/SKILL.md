---
name: tasarim-katalog
description: Use when picking a visual direction, reference site, UI library, font or design prompt source for a web page and you want proven, non-generic (non AI-slop) options with numbers instead of browsing the web. Turkish triggers include "referans site öner", "hangi kütüphane/font", "AI gibi görünmesin", "ödüllü site gibi", "tasarım yönü seç", "slop olmasın", /tasarim-katalog KONU. Returns at most 5 rows from two local catalogs (17 measured award-level sites with stack/type/colour numbers; 257 sites, libraries, fonts and prompts mined from our video reports). Do NOT use for building the page itself (frontend-craft), for installing libraries (omer-kutuphaneler) or for outside tools not about design (awesome-rehber).
---

# tasarim-katalog

Token disiplini: katalog sorgula > web'de dolaş. Dosyaların tamamını okuma; Grep ile satır çek.

## Kataloglar
- `references/siteler.tsv` — 17 ölçülmüş site (TASARIM-1, headless): ad · url · kat (webgl/editoryal/saas/portfolyo) · yığın · fontlar · h1_govde · vurgu (ton kümesi) · renk (benzersiz) · slop_imza · mb · lisans · neden.
- `references/kaynak.tsv` — video raporlarından 257 kaynak: ad · video (kaç videoda geçti) · sinif (skill/prompt, hareket/3b, font, css/cati, uretici, galeri, bilesen) · tur · link · ne · ornek_video.

## Akış
1. İhtiyacı adlandır: kategori (ör. editoryal portfolyo) ya da sınıf (ör. hareket/3b).
2. Grep: `siteler.tsv` içinde `kat`, `kaynak.tsv` içinde `sinif`/`ne`; video sayısı yüksek olan önce.
3. En çok 5 satır döndür: ad · link · neden (≤15 kelime) · ölçü (h1_govde, vurgu, mb ya da video sayısı).
4. Yön keşfinde (frontend-craft Bölüm 11) her yön bir `siteler.tsv` satırına bağlanır; künyeye ölçü yazılır.

## Sınırlar
- Siteler yalnız referanstır: kod, metin, görsel, font dosyası alınmaz; mekanizma (ölçek oranı, renk sayısı, hareket dili) alınır.
- Prompt kaynaklarında lisans/izin `link` sayfasından doğrulanmadan metin kullanılmaz; alıntı ≤15 kelime.
- Ölçülebilir slop denetimi frontend-craft `scripts/slop.mjs`; ilkeler omer-skills `docs/tasarim/ilkeler.md`.
