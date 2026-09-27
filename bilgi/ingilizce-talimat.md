---
iddia: İngilizce talimat/prompt Türkçeden daha az token tutar; "İngilizce prompt daha iyi sonuç verir" kalite iddiası bizde ölçülmedi.
kaynak: İNGİLİZCE-AB ölçümü — docs/token-notlari-eylul.md "Bölüm 2 (KURULUM-3)" (commit f347f3d, 17 Eyl); İngilizce geçiş commit 043a465
guven: orta
dogrulama: kısmen doğru
tarih: 2026-09-28
bayatlama: 2026-12-27
etiketler: verimlilik, frontend
---
# İngilizce talimat (İNGİLİZCE-AB)
- iddia: Türkçe yerine İngilizce yazılan talimat daha ucuz; videolarda ayrıca "İngilizce prompt daha iyi sonuç verir" deniyor (jGJ09wdTGDI 1:39).
- ölçüm: iki yarı, 2× `claude -p "/context"` — TR 648+651−5 = 1,294 token · EN 487+496−5 = 978 token → −%24.4.
- sonuç: token kazancı ölçüldü (−%24.4, %25 eşiğinin hemen altında; aynı MCP araçları 2. koşuda ~%5 yüksek sayıldı → sınırda). Global CLAUDE.md 17 Eyl'de İngilizceye geçti (043a465). Çıktı kalitesi farkı ölçülmedi.
- güven: orta — token tarafı tek ölçüm ve gürültü payı eşiğe yakın; kalite tarafı doğrulanamadı.
- ilgili kart: prompt-u-i-ngilizce-yazma (video iddiası), prompt-turkce-cevirt.
