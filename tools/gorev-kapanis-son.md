DEVAM-4 / SON (KAPANIS-GECE-0811), yeni hafif oturum. Once tools\gorev-kapanis-gece-0811.md (kurallar) ve rapor\gece-0811-ilerleme.md'nin son 12 satirini oku. Durma kurali: cagri sayaci durma sebebi degil; yalniz ctx 150k'yi gecince devir notu yaz ve dur.

DURUM (08:25, Desktop olctu): sira3 BITTI (tmp\bulunan-0811.tsv 1063 satir). sira9b (2497/3746), sira9a (193/490), sira8 (260/632) ~08:00'de DURDU: ucretsiz saglayicilarin hepsi hata verdi (tmp\sira8_0811.arka.log): OmniRoute ucretsiz-ozet2 HTTP 502, mistral-small-latest 429, Groq llama-3.3-70b-versatile 404, NVIDIA meta/llama-3.3-70b-instruct 410, gemini-2.0-flash 404 — model adlari eskimis + OmniRoute sunucusu ayakta degil.

0. ONCE SAGLAYICI ONARIMI: (a) OmniRoute'u ayaga kaldir (tmp\omni_baslat.py / omni-serve.log; sagligi bir istekle dogrula). (b) Groq, NVIDIA, Gemini, Mistral, Cloudflare, OpenRouter(:free), SambaNova icin GUNCEL model listesini her saglayicinin /models ucundan cek, calisan ucretsiz modelleri sec, sira8/9a/9b betiklerindeki model listesini guncelle (kod degisikligi kucuk, yedekli). 429'da geri cekilme (backoff) ekle. Her saglayiciyi tek istekle dogrula. (c) Uc betigi kaldigi yerden yeniden baslat (arka planda, python -I -S tmp\<ad>.py; ciktisini tmp\<ad>.arka.log'a). Bitene kadar Monitor ile izle (en fazla 90 dk); yine durursa nedenini yaz ve elde olanla devam et.

ISLER:
1. Sayilari dosyadan say: sira9b, sira9a, sira8, bulunan-0811 (durum dagilimlari).
2. sira8 'hayir' satirlarini (ucuz model != mevcut kategori) Sonnet ile hakemle; 9b'den 200 satirlik orneklemi Sonnet hakemlesin (dogru/yanlis orani); bulunan-0811'deki 'bulanik' eslesmeleri Sonnet hakemlesin. Sonuclar tmp\*-hakem-0811.tsv.
3. 9a'nin UYGULAMA?/BUYUK/KAYNAK-YOK satirlarini rapor\omer-sorulacak.tsv'ye ekle.
4. Ana-liste birlestirme: once tmp\ana-liste.yedek-0811-<saat>.tsv; bulunan-0811'deki dogrulanmis (tam-ad + hakemden gecen bulanik) eslesmeleri BULUNDU-ADAY'a, kaynagiyla; satir sayisi ayni kalmali.
5. 9b sonuclarini slash-ne-zaman dosyasina hizali birlestir (yedekle).
6. Git: gitleaks bulgusu 8681 kontrol edildi — bir Bash komut ozeti, anahtar YOK (Desktop dogruladi). 16 bulgunun hepsi sahte/ornek. Yeni isleri hook'larla commit et (git status'ta gercek degisiklikler; .gitignore'daki gecicileri ekleme) ve `git push`. Push hata verirse (boyut, hook) nedenini rapora yaz, gecmisi yeniden yazma. Commit mesaji sonu:
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CMeX3RcQcWu9uTiaj9pwjy
7. rapor\gece-0811-rapor.md'yi son haline getir: Yapilanlar (tum SIRA'lar sayilarla), Kalanlar, Omer'e sorulacaklar (omer-sorulacak.tsv ozet sayilari: uygulama / buyuk / guvenlik / toplu-kurulum-onayi / yukle / lisans), ana-liste son durum dagilimi, kullanilan araclar. Sayilar dosyadan.
