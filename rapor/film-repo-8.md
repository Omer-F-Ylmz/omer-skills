# FILM-REPO-8 (30 Eki) — TUR BITTI (7/8 kesin, #6 belirsiz)
Rate: gh search 30/dk; çok kelime 0 döner → stars+created filtresi çalıştı. Klonlar raf/ (gitignore), gitleaks 0 bulgu (14 repo), semgrep koşulmadı.
| # | repo | ★ | lisans | son commit |
1 lemomo-ai/lemo-opuscar (66 stil) · 9.46k · MIT · 10-29
2 Vincentwei1021/mg-styles-15 · 2.6k · MIT · 10-05
3 JohnHeibel/ClaudeAnimationBase (31 duygu, Clawd) · 2.3k · MIT · 09-24
4 mexicat/pdoom-video (kod-render MV; JohnHeibel/PDoomVideo lisanssız, klonlanmadı) · 3.6k · MIT · 10-05
5 EGSECDA/vocaloid-style-mv-pipeline (lyric MV) + makevoid/motion-graphics-music-video-skill (çizgi karakterli MV, Fal/ücretli kollar) — #5 eşleşmesi tahmin değil aday: kesin değil
6 BELİRSİZ: "18 prompt/54 örnek/~$2" hiçbir README'de bulunamadı. Klonlu adaylar: latent-spaces/brag (19.5k★ MIT), Leonxlnx/cinetic (922★ MIT), huashu-motion (1.9k★), motion-video-kit (1.2k★, 28 lansman filmi)
7 athemeroy/awesome-claude-5-5-videos (424 gönderi doğrulandı) · 835★ · CC-BY-4.0 · 10-11
8 yihui-dev/awesome-opus5-5-videos (703 prompt doğrulandı) · 12.6k★ · MIT · 10-13
Ek: opusvideo/awesome-claude-video, zhuyansen/awesome-claude-video-skills (180 repo listesi) klonlu.
## Kurulum
CC ~/.claude/skills: cinetic, huashu-motion, lemo-opuscar, motion-graphics-music-video, business-motion-film, vocaloid-style-mv (brag zaten vardı). vocaloid description tek satıra çevrildi (zip_denetle `>-` yanlış pozitifi).
claude.ai: dist/film8-<skill>.zip ×6, hepsi zip_denetle TEMİZ (≤146 dosya). Yüklenmedi (Ömer elle). lemo-opuscar zip'i 2 dosya: 66 stil verisi repoda (raf), claude.ai'de stil listesi yok → ayrı iş.
## Sapmalar
areas 1000 sınırı için aile paketi yapılmadı (6 ayrı zip). mg-styles-15 1.1 GB. İkinci beyin kaydı yapılmadı. #5/#6 kesinleşmedi; sebintel post başlığı/yorumlarından doğrulanmalı.
Kalıplar: tools/film-kaliplari.md
## Kalan işler (31 Eki)
(a) #6 hâlâ BULUNAMADI: gh search repos/code 5 sorgu (18 prompt/54 örnek varyantları) 0 ilgili sonuç; 14 klonda rg 0 eşleşme (en yakın: huashu-motion "54 prompt-gallery filmi" + 142 film — "18 prompt" yok). sebintel post yorumları erişilemedi (IG girişi gerekir) → sabah Ömer listesi.
(b) #5 kararı: ikisi farklı iş. vocaloid-style-mv-pipeline (234★ MIT): ücretsiz, Canvas2D+Playwright+ffmpeg, söz/lyric MV, API yok. motion-graphics-music-video-skill (191★ MIT): Fal AI ~$30 + ~3M token, görsel/karakter üretimi, 7 örnek. İlk gönderi metni elde yok → "lyric MV" ise vocaloid, "karakterli/ücretli" ise motion-graphics; ikisi de kurulu, karar gerekmedi.
(c) 6 kurulu skill: gitleaks 0 sızıntı (6/6); semgrep p/security-audit 5 bulgu: cinetic kit.py SHA1 ×2 (WARNING, kriptografik değil varsayımı kodda doğrulanmadı), vocaloid fetch_fonts.py urllib ×2 (WARNING), render_final.mjs child_process ×1 (ERROR; yerel ffmpeg çağrısı, okunmadı). Diğer 4 skill temiz. Çıktı tmp/film8-semgrep.json. Lisans: MIT. Test/CI yok (skill dosyaları).
