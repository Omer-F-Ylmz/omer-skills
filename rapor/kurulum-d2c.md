# KURULUM-D2C - TUR 2 BITTI (A,B,C,D,F tamam; E kismen)
Tekil kalem sayilari (1341 hedef: BULUNAMADI-2 956 + YANLIS 291 + YOLU-YOK 92 + HATA 2).
Onceki (coz-2): DOGRULANDI 335 (SKILL 126/CLI 136/MODEL 56/PAKET 17), ADAY 189, YOK 817.
Sonraki (docs/video-tarama/kurulum-coz-4.tsv): DOGRULANDI 389 (SKILL 201/CLI 165/PAKET 23), MODEL-BEKLE 72, YOK 880, ADAY 0.
A) ADAY 189 -> 107 DOGRULANDI + 82 YOK (4 Sonnet ajani, README/gh repo view; gh search yok).
B) YOK yeniden arama: gh-kotali 188 tek tek gh search (3 sn arayla, kota hic <3 olmadi) -> 7 DOGRULANDI; kalan 193 (PyPI/npm/HF/ana-liste) -> 12 DOGRULANDI. Toplam YOK->DOGRULANDI 19.
   Zayiflik: winget/VS Code/Blender aramasi kalem kalem yapilmadi (v1-v4 ajanlari yalniz kismen: v2 LoopTools=blender, localwhisper=pip). 39+ YOK satiri eski belirsiz-ad gerekcesini tasiyor.
   Lisans: LISANS-YOK/other/GPL satirlari gerekcede isaretli (ornek: twozero, context-inspector, margin-analyzer, auto-dream, LoopTools GPL); Omer karari gerekir. offensive-sqli (saldirgan skill) kurulmadan once Omer onayi.
C) MODEL: DOGRULANDI 56 + yeni = 72 kalem MODEL-BEKLE (silme yok, sonuc sutunu degisti; eski dosyalar duruyor). 56 kalemin 31'i olculdu: ~6000 GB (GLM 5.1/5.0 1404, GLM-5.3 704...); boyut yol sutununda.
D) Kanit (tools/kurulu_kanit.py, 8 sn/kalem, .ilerleme, parti): 802 tekil kurulu -> KANIT 695 (SKILL 465, CLI 133, PAKET 82, MODEL 15), KANITSIZ 107 (PAKET 56, CLI 43, SKILL 5, MODEL 3) -> docs/video-tarama/kurulu-kanit.tsv (neden ayrinti sutununda).
E) Kategori: 802 kalemin 802'si kategori.tsv'de (eksik yok). Bagimsiz 2. model+hakem (tools/kurulu_kategori_denetim.py): UYUM 517, FARK 285; 651 satir gercekten denetlendi, 150 satir ucretsiz havuz yanit vermedigi icin denetimsiz. kategori.tsv DEGISMEDI (FARK listesi kurulu-kategori.tsv'de, uygulama Omer/hakem karari). Ana FARK ornekleri: ajan-arac->diger-genel, 3d-blender->frontend-ui/ajan-arac.
   envanter_tara / katalog_yenile calistirildi; ajan_katalog calistirildi (cikti son satirlar).
F) Kapi testi: `--sadece-kapi --n 5` coz-4 ile 11 sn (onceki koşu 1 dk 53 sn, --n 3); 4 dk sinirinin altinda. Sorun yalniz paralel agir kosuydu (neden cikti olcumle dogrulanmadi).
Omer'in TEK komutu (kurulum): python tools/kurulum_d2.py --faz kur --coz docs/video-tarama/kurulum-coz-4.tsv
Kapi, izin denetimi nedeniyle kurulumu ben baslatmadim. Kurulum DENEME degil: yalniz kapi calisti.
Kullanilan: Agent(sonnet) x9 (4 ADAY, 1 gh search, 4 YOK), gh/npm/pip/curl, kurulu_kanit, kategori_denetim (ucretsiz havuz + hakem), envanter_tara, katalog_yenile, ajan_katalog, yeni: coz3_birlestir.py, kurulu_kategori_denetim.py. Commit yok.
Kalan: 150 denetimsiz kategori satiri (havuz kotasi dolunca tools/kurulu_kategori_denetim.py'yi yeniden calistir, biten atlanir); 107 KANITSIZ kalemin nedeni listede.
