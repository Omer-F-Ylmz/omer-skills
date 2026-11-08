# KAPANIS-GECE-0811 raporu (DEVAM-2 dahil)

## Yapilanlar (sayili)
- SIRA 2: 173 kalem -> KURULDU 25, KURULU-ZATEN 25, KURULU 4, MCP 1, REPO-VAR-SKILL-DEGIL 25, COZUMSUZ 83, SORULACAK-UYGULAMA 6, ARSIV-ADAY 2, ATLANDI-GUVENLIK 1 (tmp\sira2-sonuc-0811.tsv).
- SIRA 5: 26 kalem -> KURULDU 13, ZATEN 8, SORULACAK 4, COZUMSUZ 1 (rapor\tur2-yeniden-0811.tsv).
- SIRA 6: 21 sistem araci yoklandi, 20 CALISIYOR, PostgreSQL yok.
- SIRA 7: 274 kanitsiz kalem -> 189 CALISIYOR, 56 ENGEL, 2 CALISMIYOR, 27 bulanik.
- A plugin kaydi: known_marketplaces.json 154 kayit; installed_plugins'taki 149 marketplace'in 149'u mevcut, `claude plugin marketplace list` 157 giris, eksik 0 (tmp\mkt-list-0811.txt). Onarim gerekmedi; yedek tmp\plugins-yedek-0811\.
- B SIRA 1: 15 bozuk adli kalemden 2 duzeltildi (/rewind, /usage; video kHtOSJRUkLs). 13'u COZUMSUZ: kirpik OCR/ASR parcasi, kaynak json'da parca yok. Not: duzeltilen 2 satir ayni adli mevcut `arac` satirlariyla cakisir (tur farkli: yontem). Haiku aciklama ve Sonnet %5 orneklem yapilmadi.
- C SIRA 4: "292" yerine coz3-cikti'da DOGRULANDI 126 kalem. 104 gh repo yoklandi (var/son commit/lisans/boyut/arsiv), 22 gh-disi (npm 7, pip 6, hf 7, blender 1, winget 1) yoklanmadi. 125 kurulabilir, 1 uygulama?, >2GB 0, arsivlenmis 0, lisans "yok" 16. Kurulum YOK. -> tmp\sira4-dogrula-0811.tsv.
- D SIRA 3: girdi 1062 kalem (d2 BULUNAMADI-2 + ana-liste BULUNAMADI-*; "880" degil) -> tmp\sira3-girdi-0811.tsv. Arama (PyPI/npm/GitHub tam-ad + bulanik>=50 yildiz) -> tmp\bulunan-0811.tsv; arka planda surerken bu rapor yazildi, satir sayisini dosyadan say. winget/VS Code/Blender aramasi ve LLM eslestirme/Sonnet hakem yapilmadi (tam-ad kurali).
- F SIRA 11: gitleaks 16 bulgu siniflandi -> rapor\gitleaks-0811-ozet.tsv. Hepsi sahte/ornek gorunur: slack-bot-token tur2_d2_olc.py:53 sahte fikstür "xoxb-123456…", linkedin-client-id 10 bulgu prompts.chat ornek metni + gitleaks raporunun kopyalari, generic-api-key 5'i dusuk entropi/ucuncu taraf metin. Push YAPILMADI, gecmis YENIDEN YAZILMADI.
- G ana-liste durum (23650 satir): KAYITLI 14380, KURULMADI-SIRADA 6064, CALISIYOR 2223, KURULDU 418, ZATEN 246, BULUNAMADI-KESIN 100, KURULDU-SARMALAYICI 95, KANITSIZ-ESLESME-YOK 53, KURULDU-KAYNAK 24, KURULDU-DOGRULANMADI 11, KANITSIZ-LINK-ULASILAMADI 10, KURULU-KANITSIZ 6, BULUNAMADI-ARANIYOR 6, BULUNDU-ADAY 5, KURULDU-KUTUPHANE 4, KANITSIZ-KAYNAK-LINK-YOK 3, KANITSIZ-BOZUK-KAYIT 2. (Basa gore: CALISIYOR 2020->2223, KANITSIZ-ESLESME-YOK 213->53.)

## Kalanlar (yapilmadi)
- E: SIRA 8 kategori hakemligi, 9a varlik boyut yoklama/indirme, 9b slash "ne zaman" (22.946 satir), SIRA 10 claude.ai paketleme. Toplu LLM isleri; girdi dosyalari bu oturumda yeniden kurulmadi.
- SIRA 3 LLM/Sonnet hakem adimi, 22 gh-disi aday yoklamasi, 13 kirpik adli kalem.
- Git: commit ef0f39f yerel, push yok.

## Omer'e sorulacaklar
- toplu-kurulum-onayi: tmp\sira4-dogrula-0811.tsv'deki 125 kurulabilir aday (<2GB, uygulama degil) toplu kurulsun mu? (16'sinda lisans yok -> lisans kapisi: kurulmaz.)
- gitleaks: gercek anahtar kaniti yok; "anahtari iptal + gecmis temizligi" gerekmiyor. Yalniz .kos\kopru\beyin-olay.jsonl:8681 elle bakilsin. Push icin onay?
- SIRA 2'den 7, SIRA 5'ten 4 sorulacak (uygulama/guvenlik) kalem: omer-sorulacak.tsv.
- ldid AGPL-3.0 kuruldu (MIT/Apache degil): kalsin mi?

## Kullanilan araclar
gh api/search, claude plugin marketplace list, gitleaks ciktisi + git show, python betikleri (tmp\sira3_0811.py, sira4_0811.py, gl_ozet_0811.py), PyPI/npm kayit API, Monitor. Kullanilmayan: alt ajan (is kucuk/dosya yazar), LLM hakem (yukaridaki nedenle).
