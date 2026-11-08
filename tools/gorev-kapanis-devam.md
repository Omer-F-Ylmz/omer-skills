DEVAM-2 (KAPANIS-GECE-0811), yeni hafif oturum. Once tools\gorev-kapanis-gece-0811.md (kurallar/sinirlar) ve rapor\gece-0811-ilerleme.md'nin son 15 satirini oku. Bitti: SIRA 2,5,6,7; SIRA 1 kismi; SIRA 11 kismi.

Durma kurali: "cagri N/45" sayaci ve "devir onerisi" notlari durma sebebi DEGIL. Yalniz son kullanim ctx 150k token'i gecince devir notu yazip dur. Alt ajanlari kullan ama her birinin ciktisini dosyaya yazdir, sonucu kisa oku. RAM %90 ustundeyse ajan acmadan 5 dk bekle (en fazla 3 kez), sonra tek ajanla devam et.

SIRA (bu oturum):
A. Plugin kaydi onarimi (07:10 UYARI): installed_plugins.json'da olup yeni known_marketplaces.json'da olmayan 33 marketplace'i, installed_plugins.json'daki kaynak bilgisinden (repo/url) yeniden kaydet. Once ~\.claude\plugins\ altini yedekle (tmp\plugins-yedek-0811\). Sonra `claude plugin marketplace list` ile 149'un hepsi gorunuyor mu dogrula. Yapilamayanlari ilerlemeye yaz.
B. SIRA 1 kalan: 15 bozuk adli kalem -> adini videodaki yazima gore duzelt, Haiku aciklamasini yaz; Sonnet %5 orneklem (en az 50) kontrolu.
C. SIRA 4: 292 adayin SALT-OKUR dogrulamasi (repo var mi, son commit, lisans, boyut, uygulama mi) -> tmp\sira4-dogrula-0811.tsv. Toplu kurulum YAPMA (izin denetimi reddetti); kurulabilir olanlarin listesi Omer'e sorulacaga "toplu-kurulum-onayi" notuyla tek satir ozet.
D. SIRA 3: 880 bulunamayan kalemin kaynagi — ana-liste'de BULUNAMADI-* ve kurulum-d2 sonuc dosyalarinda BULUNAMADI-2 durumlu kalemlerden derle (dosya yoksa kendin uret: tmp\sira3-girdi-0811.tsv), sonra winget/VS Code/Blender/npm/PyPI/GitHub aramasi; ucretsiz modelle eslestirme, Sonnet yalniz suphelileri. Sonuc tmp\bulunan-0811.tsv.
E. SIRA 8 kategori hakemligi, SIRA 9a varlik (boyut yokla, <2GB indir), SIRA 9b slash "ne zaman kullanilir" (ucretsiz API'ler), SIRA 10 claude.ai paketleme.
F. SIRA 11: gitleaks 16 bulgu (tmp\gitleaks-0811.log) - PUSH YAPMA, gecmisi YENIDEN YAZMA. Her bulgu icin: dosya, commit, tur (redakte), gercek mi/sahte mi tahmini -> rapor\gitleaks-0811-ozet.tsv. Gercek gorunen anahtarlar icin "anahtari iptal et + gecmis temizligi" kararini sorulacaga yaz.
G. Kapanis: ana-liste durum dagilimini yeniden olc, rapor\gece-0811-rapor.md'yi yaz (dunku bicim: yapilanlar sayilarla, kalanlar, Omer'e sorulacaklar ozeti, kullanilan araclar).
