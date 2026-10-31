# tailwind

- tür: kutuphane · durum: KAYITLI · videolar: DZ2wiBNF6DU,DaIHoDKE9cT,DatZTo9ybM4,Db4xrgaxvjU,DbevmteOKw9,DcJT3UGNcLl,Dd3wMMsnz2P,Dd7MVRTtYvF,Dd9L7YVgpKs,DdIELTZD2Uw,DdO6-1QkjR-,DdRnP0TTEJM,DdjVME_lbWd,DdmTyGbpo6Z,DdrySmWKwSY,Ddsm5_8gAx6,De11l1Nuxn-,De6mQq5GZWP,DeDLmLpIJLj,DeK6kAomai9,DeMsuI4E3gJ,DeOrk1klA5_,DeU_e5LjQpS,DeV0EnpAJCs,DehO64bvSkV,DehQ41UoYHy,Deju1RFgN1E,Deo5cEelaoZ,DeoXiU1StWq,DeplxLEAvqA,Desw89eoG5a,Devud85nA97,Dew0M4YAhtG,Dewl
- bizde: kaynak-dizin/dizin.tsv; site:.kos\kopru\kaynak-dizin\dizin.tsv; kaynak-kutuphane/envanter:docs/kaynak-kutuphane/kutuphane-haritasi.tsv

## Özellikler
- Figma/Stitch tasarımını MCP ile içe aktarma ve denetleme
- Tailwind token sistemi: tokens.ts + tailwind.config ile paylaşılan tasarım değerleri
- Paylaşılan bileşenler: FadingVideo, AnimatedSection, WordReveal
- Animasyon düzeltmeleri: blur-slide, word reveal, counters, kart/buton hover, reduced motion
- OpenPencil: doğal dille arayüz tarifi, Git dostu JSON tasarım dosyaları, MCP ile herhangi bir ajan erişimi, React + Tailwind veya HTML+CSS'e kod export, CLI; glassmorphism/brutalist gibi stiller CSS değişkenlerine dönüştürülüyor

## Videoda yapılış
Stitch tasarımı MCP ile içe aktarılıp denetleniyor. Option B: 'Build token system (tokens.ts + tailwind.config)'. Ardından paylaşılan bileşenler kuruluyor, 8 bölüm + hero yapılıyor, animasyon düzeltmeleri uygulanıyor, responsive geçiş (375/768/1280) ve erişilebilirlik geçişi yapılıyor, dev sunucu port 3000'de başlatılıyor. OpenPencil'de arayüz doğal dille tarif edilip JSON olarak üretilip React/Tailwind'e export ediliyor.

## Bizdeki karşılık ve fark
BIZDE: kaynak-dizin/dizin.tsv; site: .kos\kopru\kaynak-dizin\dizin.tsv; kaynak-kutuphane/envanter: docs/kaynak-kutuphane/kutuphane-haritasi.tsv. Durum KAYITLI. Fark: videoda Stitch MCP ve tailwind.config token dosyası kullanılıyor; bizde bu akışın kanıtı alıntıda yok.

## Al
Tokenları tek kaynakta (tokens.ts + tailwind.config) tutmak; 375/768/1280 responsive kontrolünü ve reduced motion desteğini iş akışına sabitlemek.

## At
Stitch akışı MCP bağımlılığı istiyor. OpenPencil alıntıda aynı adlı başka bir projeyle karıştırılabileceği belirtiliyor. nocodealex alıntısı kullanılabilir içerik vermiyor. Alıntılar bozuk ve parçalı.
