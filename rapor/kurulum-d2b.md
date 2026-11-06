# KURULUM-D2B — TUR 1 (adım 1 tamam, adım 2-5 sürüyor)

Adım 1 LİSTE-1105: kapalı.
- Girdi: 325 Instagram kodu (linkler-1104/1105-*/acil/eksik); ana-liste.tsv'de 208 eksikti (ham/<kod> hazır).
- 174 kod için ham/ (info.json + aciklama.txt + transkript.txt) -> docs/video-tarama/derin-3/*.json; 34'ünün derin json'u vardı.
- liste_cikar llm (ücretsiz havuz, hata 0): 208/208 işlendi -> llm-d2b.jsonl; liste_birlestir -> ana-liste.tsv 17107 -> 17372 satır (+265 satır; yeni kalemler 139 videodan 416 satır).
- Kalan 69 kod: 35 LLM kalem çıkarmadı (içerik yok), 34 yalnız marka/genel ad (Claude, ChatGPT, YouTube) — mevcut filtre. Gerekçeli liste: docs/video-tarama/ana-liste-icerik-yok-d2b.tsv. Kapı: 208/208 ya kalemli ya gerekçeli.
- Rastgele 30 kalem kaynakla kontrol: 30/30 geçti (okuyucu ajanı; alt dize eşleşmesi, kısa adlarda iyimser olabilir) >= %98.
- Yeni satırlar durum: KURULMADI-SIRADA 141, KAYITSIZ 106, KURULU-KANITSIZ 105, KAYITLI 54, CALISIYOR 10. Tür: arac 240, varlik 56, yontem 48, kutuphane 32, site 26, ui-kutuphane 12.
- liste_bizde koştu (bizde_nerede yenilendi). Yedek: ana-liste.tsv.yedek-d2b, ana-liste-ozellik.tsv.yedek-d2b.
- Araç düzeltmeleri: liste_cikar dosyalar() derin-3 ekledi; liste_birlestir llm-d2b.jsonl okur + csv.field_size_limit (dizin.tsv 131072 sınırını aşmıştı).

Yapılmadı (neden): ana-liste-ozellik/yapilis md'leri yeni kalemler için üretilmedi (liste_ozellik video>=3 eşiği; yeni kalemler 1-2 video). 
Adım 2-5: kurulum-d2-sonuc.tsv durumları değişmedi (BULUNAMADI-2 956, KAPI-GECTI 442, HATA 437, YANLIS 291, YOLU-YOK 92...). ~2300 kalemin kaynak çözme + semgrep/gitleaks + kurulum turu bu turda başlamadı (tur bütçesi; toplu üçüncü taraf kurulum parti parti, tools/kurulum_coz.py ile sürecek).
Ömer'e: yok henüz. claude.ai zip listesi: bu turda yeni zip yok.
Kategori başına araç: bu tur yalnız veri-db/arastirma (liste_cikar/ücretsiz havuz, okuyucu ajanı, derin-3 ham okuma).
