# LISTE-GUNCEL-2 raporu (7 Kas)
Yedek: docs/video-tarama/ana-liste.tsv.yedek-guncel2-2129. Üretici: tools/liste_durum_guncel.py (liste_birlestir.py eski, yeniden koşturulsa BULUNAMADI-KESIN/BULUNDU-ADAY/KANIT katmanlarını silerdi; bu yüzden mevcut dosya üstüne kanıtlı katman eklendi). 23650 kalem sabit.
## Önce → sonra (kurulu = KURULDU*/ZATEN/CALISIYOR/KURULU-KANITSIZ; kurulmadı = SIRADA/KESIN/ADAY/ARANIYOR)
tür: kurulu / kurulmadı
- arac 1329/7400 → 2592/6137 · kutuphane 108/14 → 104/18 · yontem 218/0 → 210/8 · varlik 106/29 → 101/34 · prompt 20/0 → 18/2 · site-ucretsiz 24/0 → 21/3 · site-ilham 12/0 → 12/0 · ui-kutuphane 10/0 → 10/0
- durum toplamı: kurulu 1827 → 3068 · KURULMADI-SIRADA 7303 → 6089 · BULUNDU-ADAY 31 → 7 · BULUNAMADI-KESIN 103 → 100 · CALISIYOR 90 → 522 · KURULDU 0 → 417 · ZATEN 0 → 248 · KURULDU-SARMALAYICI/KAYNAK/KUTUPHANE/DOGRULANMADI 0 → 95/24/4/12 · KURULU-KANITSIZ 1737 → 1746 · KAYITLI 14380 (değişmedi)
- tmp/kalan_say.py sınıf × (kurulmamış) önce → sonra: SINIFSIZ 2014→2017 · REPO-LINKLI 1166→1043 · HIZMET 1017→1009 · UYGULAMA 559→549 · GENEL 444→440 · SKILL 455→427 · BELIRSIZ 294→293 · CLI 233→184 · MODEL 231→211 · PAKET 30→25 (BUGUN-KURULDU 4 kaldı, ana-listeye işlenmemiş = sonuç dosyasında kurulu, 'kalem' adı eşleşmedi)
## Eklenen kaynaklar (satır sayısı)
kurulum-d2-sonuc 1095 · kurulum-omer 718 · omer2 885 · gurultu 12 · guvenlik 8 · ek-1107 0 · duzelt-1107 0 (KURULDU*/ZATEN) · ~/.claude/skills 10528 klasör · agents 8 · npm -g 160 · uv tool 66 · pip --user 118 · araclar klonları 1110 · kurulu-kanit*.tsv KANIT (766+75+71) → KURULU-KANITSIZ'ı CALISIYOR'a yükseltti (432).
## Kök neden bulguları (ilk doğrulama 38/50 = %76)
1. Eski üretici docs/envanter/envanter.tsv'deki arastirilan (611) ve nerede=yok (633) kayıtlarını 'kurulu' saymıştı → sıkı kurulu endeksiyle 59 kalem KURULMADI-SIRADA'ya döndü.
2. 'tfjs-models' gibi owner__repo klon dizinleri ve github.com/.../tree/... bağlantı kuyruğu eşleşmiyordu → düzeltildi (+237 kalem).
3. Sürüm/'AI ' öneki/'Cloud' soneki (Claude Code v2.0.76, AI Video Toolkit, OpenHands Cloud) → varyant anahtarı (+65 kalem).
## Doğrulama (rastgele 25 kuruldu + 25 kurulmadı; kanıt: rapor/liste-guncel-2-dogrulama-seed12.txt, -seed21.txt)
- düzeltme sonrası iki taze örnek: otomatik uyuşma 47/50 ve 49/50 (%96); 4 uyuşmazlığın 4'ü doğrulayıcı sınırı, kanıt elle bulundu (klon spec-kit, skill security-audit, mattpocock-* skill'leri, npm lighthouse) → elle 100/100.
- Elle kontrolle kurulu çıkanlar: beads → npm bd, ecc-universal → ecc bin, pdf/Banana Skill/Sales/Hex/ctx-stats/Segment Analysis → envanter CC/claude.ai kaydı + canlı skill listesi.
- Sınır: kurulmadı tarafında 'yok' kanıtı yalnız taranan kaynaklara göre (masaüstü uygulamaları/Program Files taranmadı).
Araçlar: python/csv betikleri, npm/uv/pip CLI. jev/graphify/REA kullanılmadı: iş deterministik dosya eşleştirmesi, yargı/görsel yok. /simplify atlandı: tek kullanımlık veri-yenileme betiği.
