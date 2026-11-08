DEVAM-3 (KAPANIS-GECE-0811 / E bolumu), yeni hafif oturum. Once tools\gorev-kapanis-gece-0811.md (kurallar/sinirlar) ve rapor\gece-0811-rapor.md'yi oku. Baska bir CC oturumu SIRA 3'u (tmp\sira3_0811.py, tmp\bulunan-0811.tsv) yurutuyor: o dosyalara ve docs\video-tarama\ana-liste.tsv'ye YAZMA (ana-liste'ye islenecekleri tmp\e-ana-liste-yama-0811.tsv'ye yaz; birlestirmeyi SIRA 3 bitince Desktop yapacak).

Durma kurali: "cagri N/45" sayaci/devir onerisi durma sebebi DEGIL; yalniz ctx 150k'yi gecince devir notu yaz ve dur. Toplu LLM isleri ucretsiz API'lerle (OmniRoute/Groq/Gemini/Mistral/Cloudflare/NVIDIA; anahtarlar kullanici ortaminda), Sonnet yalniz orneklem hakemi. Uzun isleri arka planda kos, ilerlemeyi dosyadan oku. RAM %90 ustundeyse 5 dk bekle.

SIRA:
1. SIRA 8 kategori hakemligi: 285 farkli cikan + 150 denetlenmemis satir (kaynak: kategori denetimi ciktilari; bulamazsan rg ile "kategori" / "kat_kos" / "kd_" dosyalarindan bul). Ucuz model ilk karar, Sonnet yalniz celiskililer. Sonuc tmp\sira8-hakem-0811.tsv.
2. SIRA 9a: 260 "ise yarar" varlik (varlik siniflandirma ciktisi) - boyut yokla; <2GB ve uygulama olmayanlari C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\varlik\ altina indir; >=2GB/uygulama -> rapor\omer-sorulacak.tsv. Sonuc tmp\sira9a-0811.tsv.
3. SIRA 9b: 22.946 slash satirina "ne zaman kullanilir" (tek cumle, Turkce) - ucretsiz API'lerle 100'luk partiler, kaldigi yerden devam edebilir betik; 200 orneklemi Sonnet hakemlesin. Sonuc tmp\sira9b-0811.tsv (+ ilerleme sayaci).
4. SIRA 10: bu gece ve dun kurulan yeni skill'leri claude.ai icin paketle (docs\claude-ai-yukleme.md, 1000 kayit siniri / aile paketi), zip'ler dist\'e; listesi rapor\omer-sorulacak.tsv'ye "yukle" notuyla.
5. Git: .kos\kopru\beyin-olay.jsonl:8681 satirina bak (gitleaks bulgusu). Gercek anahtar DEGILSE ve diger 15 bulgu rapordaki gibi sahte/ornekse: yeni isleri commit et (hook'larla) ve `git push` yap. Gercekse push YAPMA, rapora yaz. Commit mesaji sonu:
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CMeX3RcQcWu9uTiaj9pwjy
6. Her adim sonunda rapor\gece-0811-ilerleme.md'ye satir; bitince rapor\gece-0811-rapor.md'nin "Kalanlar"/"Yapilanlar" bolumlerini guncelle (sayilar dosyadan).
