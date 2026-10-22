# egitim-1 (22 Eki 2026) - ucretsiz/yerel modelleri Opus/Fable seviyesine yaklastirma

## Hermes Agent (NousResearch/hermes-agent)
- Lisans MIT (gh api), 256k yildiz, son push 22 Eki. Python agent calisma zamani; herhangi bir OpenAI-uyumlu uc ile calisir (`hermes model`), skills + gateway (Telegram vb.) + trajectory compression (tool-calling model egitimi icin).
- Tarama (izole dizin C:/Temp/hermes-denetim, kaynak dizinine calistirma yok): gitleaks 933 bulgu - 881 generic-api-key, hepsi optional-skills(622)/tests(248)/sabit adlari; gercek sir kaniti yok (Bulgu ornekleri auth_constants.py = sabit adi). semgrep p/security-audit (agent, gateway, tools, hermes_cli): 63 bulgu / 80 kural, hepsi 'blocking' etiketli genel kural eslesmesi; elle triyaj yapilmadi.
- Karar: KURULMADI (DENE degil, IZLE). Gerekce: tam bir ikinci ajan calisma zamani; bizim arac kapimiz (tools/ogret/arac_kapi.py) ayni isi salt-okunur ve 100 satirda yapiyor. Alinacak fikir: trajectory compression -> damitma verisi. Kurulursa: izole venv, anahtarlar env'de, gateway kapali.
- "Hermes model ailesi" (Nous agirliklari) ayri: lisans model basina; LoRA tabani olarak Qwen/Gemma 7-8B ile birlikte adim 4'te olculur (YAPILMADI, asagiya bak).

## Damitma (tools/ogret/damit.py -> .kos/kopru/ogret/damit.json)
160 Opus oturumu (medyan 44 arac cagrisi): %91 dogrulama komutu kosar, %72 kapanistan onceki son 5 adimda; en sik bigram YY (kos-kos), OO, YO; gorunen metinde alternatif/gerekce yalniz %6 (dusunme bloklari dokumde bos, Fable dokumu yok) -> dusunme kalibi Fable skill'inden (fable-dusunme) alindi, is-yapma kalibi istatistikten.
Sablonlar: tools/ogret/sablonlar/{dusunme-kalibi,is-yapma-kalibi,ornek-kod,ornek-cikarim,ornek-mantik,ornek-genel}.md (toplam 294 sozcuk). Sarmalayici: tools/ogret/sarmal.py; ucretsiz_havuz.cagir(..., sablon="kod|cikarim|mantik", zor=...).

## Kapi (tools/ogret/kapi.py; kod/cikarim/mantik x 20 gorev, betikle dogrulama)
Dogru/20: kod duz 20 · sablon 19 · Haiku 20 | cikarim 20 · 20 · 20 | mantik 16 · 20 · 20. Sablonlu ucretsiz toplam 59/60 = %98,3 (kapi %92 gecti). Dis cagri: ucretsiz 120 + Haiku 60 = 180 (tavan 200+60).
DURUST SINIR: gorevler kolay (tavan etkisi); sablon farki yalniz mantik'ta gorundu (16->20, n=20, kollar arasi model karisimi farkli = gurultu olabilir). Sonnet kolu KOSULMADI (plan limiti; Haiku referans). Gercek is turleri (site-3d/guvenlik/belge) icin 20'ser gorev YAZILMADI - kapi yalniz kod/cikarim/mantik icin gecti.
Yonlendirme: kod/cikarim/mantik ROUTER-1 turu degil; 'ucretsiz once' girisi Desktop onayinda (yonlendir-kurallar.json tur listesine eslestirme).

## Arac kapisi (tools/ogret/arac_kapi.py)
Ucretsiz modelin OpenAI-uyumlu tool calling ile kombin_sec/katalog_ara/dosya_oku/ara (salt okunur, kok-ici yol, gizli ad reddi). Canli: minimax-m3.1-flash:free kombin_sec + katalog_ara cagirdi.

## Havuz (adim 6)
sarmal.kaydet: kapi.py'de dogrulanmis sablon kolu basarisi .kos/kopru/ogret/havuz.jsonl'e girer, onek() son 2 ornegi ekler. Gercek is sonu kancasi (zorunlu-arac-3) baglanmadi - Desktop karari.

## Acik / Desktop'a
- 2b(b) Fable ile 10 zor gorevde dogrulatma + A/B: Desktop'ta Fable 5.1 gerekir, yapilmadi. 2b(a) skill/zip/havuz sarmalayicisi fable-kur-1 ile hazirdi (skills/fable-dusunme, dist/fable-dusunme.zip, ZOR_SABLON).
- Adim 4 LoRA (RTX 4070 Ti): yapilmadi; once 20 gorev kapisi gercek turlerde zorlastirilmali (tavan etkisi), sonra damitma verisi buyutulmeli.
- Alt ajan tanim dosyalarina sablon eklenmedi (.claude/agents mid-session yuklenmez).
