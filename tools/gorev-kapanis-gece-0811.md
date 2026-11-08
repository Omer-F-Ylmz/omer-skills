KAPANIS-GECE-0811 — video kurulum isinin kalanlarini bitir. Omer bilgisayardan uzakta; geri alinabilir her adimi kendin yap, durma, soru sorma. Nihai kurallar (C:\Projeler\omer-kurallar.md) gecerli: once oku, her adimda uy.

BASLARKEN: rapor\gece-0811-ilerleme.md'deki devir notunu oku, oradan surdur. Bu oturum hafif modda (skill listesi/MCP kapali, hook'lar ve CLAUDE.md acik) - baglam tasarrufu icin; skill gerekirse dosyasini dogrudan oku. 60 sn'den uzun surebilecek her betigi arka planda kos (run_in_background), ciktiyi dosyadan oku. Ciktilari kisa tut (head/tail/wc), buyuk dosyayi asla tum okuma.

ILERLEME DOSYASI: rapor\gece-0811-ilerleme.md — her alt is bitince 1-3 satir ekle (saat, is, sayi, kanit dosyasi). En gec 2 dk'da bir Obsidian'a (2. beyin) kisa not. Context sisiyorsa ilerleme dosyasina devir notu yaz ve dur; Desktop seni --resume ile surdurecek.

KESIN SINIRLAR
- Calisan isler: gece_kuyruk.py (kur_tur2 ikinci kosu, ardindan coz6) arka planda suruyor. Bunlara DOKUNMA; docs\video-tarama\kurulum-d2*.tsv, rapor\kur-tur2-*.tsv, docs\video-tarama\kurulum-coz-6.tsv dosyalarina YAZMA. Kuyrugu yeniden baslatma.
- YENI KURAL (Omer 8 Kas 04:40): boyutu >=2 GB olan her sey (indirme, klon, model, paket, varlik) ve masaustu UYGULAMALARI (winget/installer/exe/msi ile kurulan programlar) KURULMAZ/INDIRILMEZ. Bunlari rapor\omer-sorulacak.tsv'ye yaz: kalem, tur(uygulama|buyuk|diger), tahmini_boyut, kaynak, neden. Boyut bilinmiyorsa once salt-okur yokla (GitHub API size, HF dosya listesi, HEAD); yoklanamazsa sorulacaga yaz.
- Guvenlik/sizma araci kategorisindeki kalemleri (GUVENLIK-RED vb.) bu dalgada ATLA; sorulacak listesine "guvenlik-ayri-dalga" notuyla yaz.
- Modeller kurulmaz (eski karar). Silme yok: gereksiz bulunan her sey sadece listelenir.
- docs\video-tarama\ana-liste.tsv: yazmadan once tmp\ana-liste.yedek-0811-<saat>.tsv yedegi al; satir sayisi ayni kalmali; degisen satirlara kanit yaz.
- RAM: islem baslatmadan once RAM %85 ustundeyse agir isi (toplu LLM, klon) 5 dk ertele.

SIRA (hizli kazancli once):
1. Haiku aciklama turu (liste-eksik): bitti mi kontrol et (tmp\le_haiku8.log, tmp\le_say.py). Bitmediyse kalanini ucuz modelle bitir. Sonra Sonnet orneklem kontrolu (%5, en az 50 kalem) + kalem adlarini videodaki yazima gore duzelt (tmp\ad_duzelt / ad_hizala akisi).
2. tmp\kurulum_ayir.tsv (173 kalem): 29 toplu skill deposu -> skill klasorlerini kur (boyut sinirina uy); 20 Windows surumu dogrulanamayan -> yokla, uygulama degilse ve kurulabiliyorsa kur; 38 silinmis depo -> fork/arsiv/ayna ara, bulunani kaydet; 86 yolu olmayan -> gerekcesiyle COZUMSUZ olarak kesinlestir.
3. Bulunamayan 880 kalem: winget search, VS Code marketplace, Blender extensions, npm, PyPI, GitHub'da kalem kalem ara (ucretsiz/yerel modelle eslestir, Sonnet yalniz suphelileri hakemler). Sonuc tmp\bulunan-0811.tsv; uygulama ise sorulacaga.
4. kurulum-coz-3'teki 292 aday: kaynaklari dogrula (repo var mi, son commit, lisans, boyut). Dogrulanan + uygulama olmayan + <2GB olanlari kur.
5. TUR2 ilk kosu hatalari (rapor\kur-tur2-sonuc.tsv): 17 PLUGIN + 9 APT hatasinin kok nedenini cikar (WSL o sirada kapaliydi, simdi acik). PLUGIN'leri `claude plugin` ile yeniden dene, APT'leri WSL'de yeniden dene (guvenlik kalemleri haric). Sonuclari rapor\tur2-yeniden-0811.tsv'ye yaz. D2 hatalarina dokunma.
6. 21 atlanan sistem araci (Python, Node, Go, PHP, PostgreSQL, VCRedist, CUDA vb.): kurulu mu tek tek yokla (where / --version). Kurulu olanlari ana listede CALISIYOR'a kanitla isle; kurulu olmayanlar sorulacaga (uygulama).
7. Kanitsiz kurulu kalemler (ana listede KANITSIZ-*, KURULU-KANITSIZ, KURULDU-DOGRULANMADI; ~285): her birini calistir (--help/--version/skill yuklenir mi) ya da engelini yaz.
8. Kategori hakemligi: 285 farkli cikan + 150 denetlenmemis satir — ucuz modelle ilk karar, Sonnet sadece celiskilileri.
9. Hic baslanmayan: (a) 260 ise yarar varlik — boyut yokla, <2GB olanlari araclar klasorune indir, buyukleri sorulacaga; (b) 22.946 slash satirina "ne zaman kullanilir" — ucretsiz API'lerle toplu (OmniRoute/Groq/Gemini/Mistral/Cloudflare), 200'luk orneklemi Sonnet hakemlesin.
10. Yeni kurulan skill'leri claude.ai icin paketle (docs\claude-ai-yukleme.md, 1000 kayit siniri / aile paketi duzeni), zip'ler dist\'e. Yukleme Omer'de; listesini sorulacaga "yukle" notuyla yaz.
11. Git: commit'ler hook'larla atilsin; commit'lenmemis ~30.058 dosyayi sinifla (gecici/cikti/gercek), gecicileri .gitignore'a ekle — silme yok. Push oncesi gonderilmemis commit araligina gitleaks tara; temizse push et, bulgu varsa push etme ve rapora yaz. Commit mesaji sonu:
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CMeX3RcQcWu9uTiaj9pwjy

DOGRULAMA: her alt isin sonunda sayilari dosyadan yeniden say (tahmin yok). Kapanista ana liste durum dagilimini yeniden olc.

KAPANIS: rapor\gece-0811-rapor.md — dunku rapor bicimiyle (yapilanlar sayilarla; kalanlar; Omer'e sorulacaklar ozeti; kullanilan araclar). Kisa, sayili, tahminsiz.
