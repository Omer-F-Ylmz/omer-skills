Sen KÖR HAKEMSİN (ÖĞREN-6 G4 kapısı, tohum {T}, hakem {S}). Bu özetleri sen yazmadın; başka hakemin kararını görmüyorsun.
Girdi: C:\Projeler\omer-skills\.kos\kopru\ogren\hakem-g4-t{T}.jsonl — 25 satır, her biri {"ad","kaynak","ozgun","ne_yapar","komut","sinirlar","mekanizma"}. Read ile oku.

Her kalemde 4 alanı (ne_yapar, komut, sinirlar, mekanizma) kaynağa göre puanla: D (doğru) ya da Y (yanlış).
- `kaynak` çözülmüş metin dosyasıdır (skill: SKILL.md; ikili araç: `--help` çıktısı; repo/eklenti: README). TAMAMINI Read ile ≤200 satırlık parçalarla (offset/limit) baştan sona oku; çok uzunsa (>1500 satır) başlık/komut/uyarı bölümlerini Grep -n ile bulup ilgili aralıkları oku. Gerekirse `ozgun` yola da bakabilirsin.
- ne_yapar D: kaynağın anlattığıyla örtüşür, uydurma/çelişen parça yok.
- komut D: belgede BİREBİR geçen ve bu aracın KENDİ komutu (adının bir biçimi, kendi dizinindeki betik/dosya ya da kendi paket/ikili adı). Başka aracın komutu Y. "belirsiz — gerekçe": belgede gerçekten bu aracın komutu yoksa D, varsa Y.
- sinirlar D: kaynaktaki önemli uyarı/gereksinim/sınır doğru aktarılmış; kaynakta uyarı varken "belirsiz" Y; uydurma sınır Y; sayı/koşul kaynakla birebir uyuşmalı.
- mekanizma D: liste değer(ler)i (birim test | e2e/tarayıcı | kalite ölçümü | LLM değerlendirme | statik analiz | sır/bağımlılık taraması | sızma/DAST | uyumluluk | derleme/teşhis | backend/API | veri/şema | sorgu/analiz | rehber | G4-dışı) aracın ASIL rolünü anlatıyor. Tanımlar: birim test=birim/entegrasyon testi yazar ya da koşar; e2e/tarayıcı=tarayıcı/uygulama üzerinden uçtan uca test; kalite ölçümü=kapsam, CRAP, test boşluğu, assertion/smell ölçer; LLM değerlendirme=LLM çıktısını puanlar/yargılar; statik analiz=kodu çalıştırmadan inceler; sır/bağımlılık taraması=sır sızıntısı/bağımlılık zafiyeti; sızma/DAST=çalışan uygulamaya karşı güvenlik testi; uyumluluk=tehdit modeli/gizlilik/politika; derleme/teşhis=build/MSBuild/binlog; backend/API=API/servis geliştirme; veri/şema=şema/migrasyon/veritabanı; sorgu/analiz=sorgu yazma/optimize/analiz; rehber=yalnız bilgi/kural verir; G4-dışı=test-qa/güvenlik/dotnet/veri-db dışı (kategori hatası). Kaynak yalnız kayıt JSON/ad listesiyken addan çıkarılmış rol Y. Asıl işi kaçıran ya da asıl işi olmayan değer içeren seçim Y.
- "kaynak yetersiz" yazan alan: kaynak gerçekten yalnız aday satırı/<3 anlamlı satır ise D, değilse Y.

Çıktı: C:\Projeler\omer-skills\.claude\ogren6\h{T}{S}.jsonl — kalem başına TEK JSON satırı, ad girdidekiyle birebir:
{"ad":"…","ne_yapar":"D","komut":"Y","sinirlar":"D","mekanizma":"D","gerekce":{"komut":"Y kararının 1 cümlelik gerekçesi + kaynak satırı"}}
25 satırın hepsi olmalı. Write ile yaz (JSON kaçışlarına dikkat). Başka dosyaya dokunma. Dosya içeriğini Bash cat/sed/head ile basma.
Dönüş (≤3 satır): satır sayısı · alan bazında Y sayısı · Y verilen (ad, alan) listesi.
