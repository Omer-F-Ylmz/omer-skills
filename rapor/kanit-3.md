# KANIT-3 raporu
- Önce: KURULU-KANITSIZ 1.746 (arac 1.379, yontem 170, varlik 83, kutuphane 59, site 33, prompt 14, ui 8) · CALISIYOR 522
- Sonra: 1.498 CALISIYOR (skill 843, klon 386, plugin 111, cli 86, mcp 56, baglanti 16) · 248 KANITSIZ-<neden> · KURULU-KANITSIZ 0
- Betik: tools/kurulu_kanit4.py (kurulu_kanit2/3 yöntemi genişletildi; kurulum/yan etkili komut yok, güvenlik araçlarında yalnız --version, husky/lefthook yasak)
- Çıktı: tmp/kanit3_sonuc.tsv, docs/video-tarama/kurulu-kanit.tsv (yedek .oncesi-kanit3-1107-2235), ana-liste.tsv (yedek .yedek-kanit3-1107-2235)
- Doğrulama: 40 rastgele KANIT satırı yeniden koşuldu: 40/40 (%100) tekrarlandı
- Kalan KANITSIZ nedenleri: ESLESME-YOK 213 (GUI/Docker gibi PATH dışı, ad eşleşmesi yok, yanlış kayıt) · LINK-ULASILAMADI 26 · KAYNAK-LINK-YOK 7 · BOZUK-KAYIT 2
- Sınır: eşleşme ad normalizasyonuyla; klon kanıtı dizin+git HEAD (çalıştırma değil), mcp kanıtı kayıt+komut çözümü (canlı listeleme değil)
