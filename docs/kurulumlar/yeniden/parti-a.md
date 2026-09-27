# Parti A — ilk 15'in 1-4'ü (2026-09-28)

Hat: SERTİFİKA-1 (tarama → katman → araştırıcı → katman). Karar kaynağı: docs/kurulumlar/kayit.jsonl (ad başına son satır, tarih 2026-09-28; K0 kural kararları hariç). Rapor: docs/kurulumlar/2026-09-28-uygula.md · brief: docs/kurulumlar/yeniden/parti-a-brief.md.

## NyNScAc2u_o (Yıldız Dikme · 3D ring galeri)
- karar dağılımı: KUR 3 (bekleyen kural, ONAY) · UYARLA 1 · ZATEN VAR 1 · departman frontend
- Site/UI: UYARLA 1 özellik (scroll-mouse-parallax-rotasyon) + teknik UYARLA 7 (bekleyen/teknik-*) · ÖĞREN 0
- prompt kalıbı: 7 (ZATEN VAR 7 · UYARLA 0) → docs/departmanlar/frontend-promptlar.md
- ÜRETİLEBİLİR: 1 — nyns-3d-galeri-promptu-scroll-mouse-parallax-rotasyon → departman-frontend şablonu · `ÜRET` (koşulmadı)
- ayrıştırma: 0 (token özelliği yok)
- araştırıcı: 67.9k token · **araştırma yarım: tur tavanı** (12 tur, rapor dönmedi; aday.md'de `arastirma:` işareti, DENE verilmedi)

## Gg35_iQWx7g (Burhan KOCABIYIK · skills CLI)
- karar dağılımı: KUR 4 (skills-cli 2 özellik ONAY + 2 bekleyen kural) · ÖĞREN 1 · departman surec-ajan-arac / surec-git-yayin
- Site/UI: yok
- prompt kalıbı: 0
- ÜRETİLEBİLİR: 0
- ayrıştırma: 0
- araştırıcı: skills-cli 35.3k token (MIT, T2)

## JNM_rxqtlvY (İsa Nurdoğdu · claude-usage)
- karar dağılımı: KUR 4 (terminal-ozet ONAY + 3 bekleyen kural) · DENE 1 (web-dashboard) · ZATEN VAR 1 · departman verimlilik
- Site/UI: yok
- prompt kalıbı: 0
- ÜRETİLEBİLİR: 0
- ayrıştırma: 0 (token aracı, ama hiçbir özellik kalite/takas nedeniyle RED/SOR almadı; takas tablosu deneme sonucu ister, claude -p 0 → yok)
- araştırıcı: claude-usage 71.0k token (>40k)

## jGJ09wdTGDI (Yıldız Dikme · Claude Design e-ticaret)
- karar dağılımı: KUR 1 (bekleyen kural) · ÖĞREN 2 (design-system düzeltmesi dahil) · UYARLA 1 · ZATEN VAR 1 · DENE 1 · departman frontend / test-qa
- Site/UI: UYARLA 1 özellik (tek-prompt-e-ticaret-sitesi) + teknik UYARLA 8 · ÖĞREN 2 (design-system-ui-kit-paneli, prompt-u-i-ngilizce-yazma)
- prompt kalıbı: 5 (ZATEN VAR 5 · UYARLA 0)
- ÜRETİLEBİLİR: 1 — jgj0-claude-design-promptu-tek-prompt-e-ticaret-sitesi → frontend-craft Bölüm 4 · `ÜRET` (koşulmadı)
- ayrıştırma: 0
- araştırıcı: 81.9k token (12 tur tavanında raporsuz; aday.md sonradan yazıldı, rapor-denetle GEÇTİ)

## Düzeltme
- design-system-ui-kit-paneli: RED (lisans yok) → ÖĞREN (frontend); kayit.jsonl'e düzeltme satırı eklendi (satır 75 değişmedi).

## YÜKLENECEK ZIP
dist/yukle-parti-a/replace/: frontend-craft.zip · departman-frontend.zip (claude.ai'ye elle yüklenir; skill_denetim 0 hata).
