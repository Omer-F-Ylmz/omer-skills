# dok — 24 benzersiz kayıt

**Amaç:** Teknik ve iş dokümanı yazan/dönüştüren ajan kadrosu: ADR, API dokümanı, changelog, runbook, rapor, sözleşme incelemesi, docx/pdf/pptx/xlsx üretimi, çeviri.

**İç yapı:** Tümü [ajan], ad kalıbı dok-<iş>; gruplar: mühendislik dokümanı (adr-yazar, api-dokumani, runbook, degisiklik-gunlugu, dokuman-sapmasi), dosya üretimi (docx, pdf, pptx, xlsx, markitdown), metin düzenleme (icerik-editoru, ste100-sade, cevirmen-teknik), iş metni (teklif, toplanti-notu, destek-yaniti, sozlesme-madde).

## En güçlü parçalar
- `dok-dokuman-sapmasi` — Doküman örneklerini, imzaları, CLI bayraklarını ve config anahtarlarını güncel koda karşı denetler.
- `dok-markitdown-donusum` — PDF, DOCX, PPTX, XLSX'i LLM'e verilecek temiz Markdown'a çevirir.
- `dok-adr-yazar` — Teknik seçim için bağlam, seçenekler ve sonuçlarla mimari karar kaydı yazar.
- `dok-runbook` — Nöbetçi için tetik, teşhis adımı, komut ve rollback içeren operasyon runbook'u.
- `dok-rapor-ozetleyici` — Uzun belgeyi ana noktalar, kararlar ve açık sorularla tek sayfaya indirir.
- `dok-cevirmen-teknik` — Türkçe-İngilizce teknik çeviride tutarlı terim kullanır.

## Birlikte kullanım
- dok-markitdown-donusum → dok-rapor-ozetleyici: belgeyi Markdown'a çevir, sonra özetle.
- dok-rapor-uretici + dok-tablo-duzenle + dok-docx-uretici / dok-pdf-uretici: biçimli rapor çıktısı.
- dok-api-dokumani + dok-dokuman-sapmasi: yazılan API dokümanının kodla uyumunu sürdür.

## Tuzaklar
- dok-kullanim-kosullari hukuk incelemesine gidecek taslak üretir, dok-sozlesme-madde yalnız riskleri işaretler; hukuki onay yerine geçmez.
- Örtüşen roller: dok-rapor-uretici ile dok-rapor-ozetleyici, dok-sorun-giderme-rehberi ile dok-runbook; görev tanımına göre seçilmeli.

## Üyeler
- ajan (24): dok-adr-yazar, dok-api-dokumani, dok-blog-yazisi, dok-cevirmen-teknik, dok-degisiklik-gunlugu, dok-destek-yaniti, dok-docx-uretici, dok-dokuman-sapmasi, dok-hata-mesaji, dok-icerik-editoru, dok-kullanim-kosullari, dok-markitdown-donusum, dok-pdf-uretici, dok-pptx-sunum, dok-rapor-ozetleyici, dok-rapor-uretici, dok-runbook, dok-sorun-giderme-rehberi, dok-sozlesme-madde, dok-ste100-sade, dok-tablo-duzenle, dok-teknik-teklif, dok-toplanti-notu, dok-xlsx-tablo
