# YARIM-DOGRULA-1 (30 Eki 2026)

Yöntem: her işin son `result` satırı (`arka/<ad>.log`) + git log + dosya/görev denetimi. Özet dökümü: `arka/_yd1_ozet.txt` (betik `arka/_yd1_ozet.py`). Yeni işler `arka/_yd1_isler.py` ile üretildi, `_sira.txt` sonuna eklendi (mevcut sıra bozulmadı). Hiçbir iş koşturulmadı, ücretli çağrı 0.

| iş | gerçek durum | kanıt | yeni iş / soru |
|---|---|---|---|
| yarim-216 | 178/216 BITTI; 38 açık: 6 ENGEL, 16 OMER, 14 ESKI | log result; 7ec2565c, 11e654ce | yarim-216-2 (olum-teshis kök neden, ESKI yeniden sınıf); derin-tamamla ENGEL-30'da yeniden başladı (dfa4803f) |
| hic-122 | 109/123 BITTI, 14 açık (8 ENGEL) | log result, docs/ogren/README.md | hic-122-2 (6 engelsiz iş) |
| karar-14 | KAPANDI (14B) | 09a57c26, 74a14290 | 9 karar sorusu: `arka/karar-14-soru.md` |
| omer-karar-10 | 9/10; zk, claude-mods kurulamadı | rapor/omer-karar-10.md | omer-karar-10-2 |
| acik-31 | 15/23; engellerin büyük kısmı acik-32 ile işlendi | acik-32 result | kalan: ig-giris (Ömer hesabı), mem-fix-2 (kota), yarim-b1-devam-b (ders mekanizması kararı) → soru |
| acik-32 | KAPANDI: A 9/10 kabul tuttu | 01648a4e | yok |
| karar-30 | m2 G5 ölçümü zaman aşımı, sonuç yok | 1af374e6 | karar-30-2 (parçalı ölçüm) |
| envanter-dogrula-1 | 229 kapandı, 508 KURULACAK kaldı | ffc5ebbf, b1304daa | envanter-dogrula-1-2 |
| video-kaynak | 138/140; 2 IG karuseli çerez ister | log result | soru: tarayıcı çerezi onayı |
| video-yeni-1 | tur 1: 417/433 derin; karusel görsel okuma yok | 6b2ebba8 | video-yeni-1-2 |
| kalan-son | token-rea-d20 ölçüldü, kapı geçmedi (plan.md d21); yeniden-gecis RAM engelli | log result | kalan-son-2 (RAM önkoşullu) |
| derin-hiz-2 | Groq 0,913<0,98; toplu koşu yok | log result | derin-hiz-3 zaten kuyrukta; soru: yerel large-v3 ~120 sa mı, kapı %95 mi |
| gpu-sinir-2 | hedef tutmadı (%10 > %2), sayaç yok | c105c779 | gpu-sinir-2-2 |
| kod-modu-her-sey | Bölüm 1 yapılmadı, katman ölçümü var | 6509140e | kod-modu-her-sey-2 |
| ertele-2 | kapı tutmadı, geri alındı (ölçülmüş sonuç) | 8ac53af4 | yok (negatif sonuç kapandı) |
| ertele-3 | kapı tutmadı; n=12 yeniden ölçüm öldü | 011e07ae | ertele-3-2 |
| bosta-arac-1 | kapı %92,5 geçti; commit + 28/36 yeniden puan eksik | log result | bosta-arac-1-2 |
| mem-abone-1 | kapı tutmadı (A %83, B %67), canlı değişmedi | log result | mem-abone-1-2 |
| profil-gorsel-1 | 7 tur, hakem 5-7 (<8), DUR | b38d1c0a | soru: yaklaşım değişsin mi (3 başarısız deneme kuralı) |
| yerel-gorsel-turbo | VRAM düzeldi, RAM tepe %94,9; benchmark/skill yok | log result | yerel-gorsel-turbo-2 (kuyruğun başı yeni işler arasında) |
| yerel-medya-1 | BSOD 0x139 sürücü adı bilinmiyor (dump yönetici ister); video koşmadı | e92d3fbc | soru: dump okuma yetkisi |
| film-repo-8 | 7/8; #6 yok, #5 belirsiz, semgrep yok | 73db3ff0 | film-repo-8-2 |
| arka-fix | env testi var; 2 alt ajan testi koşmadı | ab99d29b | arka-fix-2 |
| zip-yukle-30eki | 0/14 yüklendi; Chrome debug portu yok | log result | soru: Chrome profil/yeniden başlatma onayı |
| link-30eki-26 | 2/3; FreeVideo 23,4 GB >15 GB sınırı | log result | soru: FreeVideo ve büyük modeller onayı |
| yaka-kapanis | 5/6 PASS, ZAP yok | log result (764b057 İLİK deposu) | yaka-kapanis-2 |
| ilik-ucretsiz-3d / ilik-tripo | kredi yok, ZeroGPU kota dolu, site değişmedi | 17e49c4f | ilik-ucretsiz-3d-4; soru: kredi alınsın mı |
| ilik-gece-yayin | görev 30 Eki 00:04 koştu, LastTaskResult 0; yayın etkisi doğrulanmadı | Get-ScheduledTaskInfo | ilik-ucretsiz-3d-4 içinde doğrulama |
| ucretsiz-3d-1 | KAPANDI: hakem sonradan geldi (55,2 / 56,8) | ilik-gece-yayin result | yok |
| skill-mode | KAPANDI: 171 skill açıldı, 125,6k | log result; 384518b9 | yok |
| yaka-d2 | KAPANDI: D2b | log result (c1b279e İLİK deposu) | yok |
| ab-taban | duman testi (haiku), teslimat yok | json görevi | yok |
| ilik-v2 | log yalnız BASLADI; ilik-v4 ile devralındı (76c3aec, Lighthouse 95) | ilik-v4 result | yok |

## Ömer'e tek satır sorular
1. yarim-216: dns-sonrasi-1, kurulum-video-1d, ustalik-1-p2, video-kisa-token-1 (canlı kurulum/npm/ComfyUI) onay?
2. derin-hiz: yerel large-v3 ~120 sa mı, kapı %95'e inecek mi?
3. FreeVideo (23,4 GB) + LongCat/MiniMax/LTX büyük modeller 15 GB sınırı dışında kurulsun mu?
4. BSOD dump okumak için yönetici yetkisi verilsin mi?
5. IG karusel çerezi ve zip-yukle için Chrome oturumu kullanılsın mı?
6. profil-gorsel-1: 7 turda hakem <8; yaklaşım değişsin mi (hazır şablon)?
7. Tripo/3D AI Studio kredisi alınsın mı (şu an 0 harcama)?
8. acik-31 kalanı: yarim-b1-devam-b ders mekanizması kararı; ig-giris-1-a2 hesap.

## Sapmalar
`ilik` ve `yaka` commit'leri İLİK site deposunda, omer-skills'te doğrulanamadı (log'a dayanır). `envanter` KURULACAK sayısı (508) log'dan, tsv'den yeniden sayılmadı.

## ARKA-FIX tavan A/B (30 Eki)
- Neden `claude -p` "yanıt vermiyor": varsayılan yapılandırmada açılış >270 sn (3369 skill dir komutu + 2676 eklenti skill'i, SessionStart kancaları 34 sn+). Plan limiti/ağ/kilit değil. `--strict-mcp-config --disable-slash-commands --settings <tüm enabledPlugins=false>` ile haiku 75 sn'de yanıt verdi.
- A (CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=20000): arka alt ajan başlatıldı, süreç 33 sn'de çıktı (PENDING).
- B (=150000): aynı görev, süreç 222 sn'de çıktı (tavan+açılış; alt ajan bekletildi).
- Sınır: alt ajanın `sleep 45` önplanda engellendi, ZETA_DONE hiç gelmedi; tavanın "sonucu teslim ettirdiği" kanıtlanmadı, yalnız bekleme süresini belirlediği (33 sn vs 222 sn) ölçüldü.
