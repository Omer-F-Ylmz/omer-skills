# DEVİR — 27 Eki 2026 14:45 (Desktop → yeni sohbet)

Kurallar: NİHAİ 31/32/32f · Headroom asla kaldırılmaz · silme yok · anahtar/şifre değeri yazılmaz · RAM bekçisi %95 · C ≥80 GB · SONRA kümesine dokunma · read_media_file KULLANMA (görsel: device_stage_files + PIL küçült + Read) · Türkçe, kısa.

## LINK-27 (78 link)
- 76/78 izlendi (Gemini, 0 Claude). İndirilemeyen: De1u9y2D6Ix, qs-DetJr2nQ. Kararlar: docs/video-tarama/link-27eki-sonuc.md
- 24 repo klonlandı: Desktop\Claude ile yapılanlar\araclar\link27\ · ön özet .kos/kopru/video/link27/kur-ozet.md
- gitleaks bulguları (8 repo) hepsi test/doküman örnek anahtarı → kurulabilir (tools/link27_gitleaks_ozet.py)
- KURULDU: agency-agents 283 ajan → ~/.claude/agents-katalog (ajan-getir katalogu 1150) · rederive CC plugin · ScrapeGraph kendi .venv'i · agent-floor derlendi + 10/10 test, `npm i -g .` sonucu .kos/kopru/video/link27-kurulum2.log'da kontrol edilecek
- SIRADA: google/skills (marketplace ekle, işe yarayan plugin'ler), deer-flow, thinkrail, hibi, OpenMontage, deepseek-harness; site kütüphaneleri (kokonutui, shadergradient, liquid-logo, anime.js, 3d-model-anything) kaynak listesine; bulunamayanlar (trim-l, mcptoon, Harness2, Roast Room, Hermes Meshy) yeniden aranacak; archify (çok büyük) ayrı; coucou yalnız Mac → RAPOR; Desktop (claude.ai zip) + ajan çekirdeği tarafı; Obsidian 2. beyne öğrenilenler; 2 eksik link yeniden.

## clodfarm (Ömer istedi, az RAM)
- docker-compose.override.yml: mem_limit 1600m, restart no, MAX_WORKERS 2, haftalık %80 / 5 saat %85.
- .wslconfig: memory=2GB, processors=4, autoMemoryReclaim=dropcache, sparseVhd=true.
- tools/clodfarm_ac.py (arka planda koşuyor, log .kos/kopru/clodfarm.log → BITIS + docker stats) · tools/clodfarm_kapat.py
- 14:55 kontrol: clodfarm AÇIK, boşta 94 MB / 1.56 GB tavan. agent-floor global kuruldu (`agent-floor --help` çalışıyor).
- Ömer yapacak: konteynerde Claude girişi + arayüz şifresi `docker logs clodfarm` (Claude okumaz).
- Sonra: diğer işlerde RAM önerileri (ajan_sira boş RAM'e göre ajan sayısı; Docker/Ollama/STRIX iş bitince kapat).

## Parfüm yarışı — BİTTİ
- parfum-yaris/KIYAS.md: ajan $2.85 (Sonnet high, ~1M token tahmini) vs Desktop ~212k token → Desktop daha az token, görsel olarak da daha iyi.

## STRIX
- Gemini ücretsiz kotası doldu, Docker kapalıydı. docs/kurulumlar/strix.md. Docker açıkken Groq/OpenRouter ücretsiz modelle yeniden koş.

## 4070 Ti unlock — ÖMER BEKLETTİ ("daha hızlı yolu çıkarsa yazarım")
- Kart PNY 4070 Ti (10de:2782, sub 196E), MSI PRO B760M-P, i7-14700K (iGPU UHD 770), Secure Boot açık, ESP 100MB.
- Windows portu (gpu-unlock-ada/windows/ad104-msi) MSI kart + Z490'a kilitli; uyarlama = salt-okur probe → profil. Linux yolu Ömer reddetti. Hiçbir şey kurulmadı. Kural: vBIOS/sürücü yaması yok; Secure Boot/BitLocker/boot ayarı Claude yapmaz.

## Kuyruk
- Ajan kuyruğu çalışıyor (_tur.py). 3 saatte bir en kısa rapor.
