# STRIX (27 Eki 2026)

Durum: kurulu, deneme yarım. Docker + sandbox imajı çalıştı, ama ücretsiz Gemini günlük kotası dolduğu için (model başına 20 istek) tarama bitmedi.

Kullanım (CC + ajanlar):
- Docker Desktop açık olmalı: `tools/docker_ac.py`, iş bitince `tools/docker_kapat.py` (RAM için, .wslconfig memory=2GB).
- docker CLI: `C:\Program Files\Docker\Docker\resources\bin\docker.exe` PATH'te olmalı.
- LLM: `STRIX_LLM=gemini/<model>` (anahtar HKCU ortamındaki GEMINI_API_KEY'den okunur, değeri yazılmaz). Gemini kotası doluysa Groq ya da OpenRouter'ın ücretsiz modeli (`STRIX_LLM=openrouter/...`) ile çalıştır, kota yenilenmesini bekleme.
- Yerel hedef: siteyi 0.0.0.0'da sun, hedef `http://host.docker.internal:<port>`.
- Deneme betiği: `tools/strix_deneme.py` (`_strix_baslat.py` ile arka planda), log `.kos/kopru/strix-deneme.log`.

Sıradaki adım: Docker açıkken başka ücretsiz sağlayıcıyla tekrar koşmak.

## F1 koşusu (27 Eki 20:55–21:17, ücretsiz OpenRouter)
- Model: `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free` (önceki iki :free model 404 / "unavailable for free"; `tools/strix_deneme.py <gemini|openrouter|groq>` ile sağlayıcı seçilir).
- Hedef: parfum-desktop statik sitesi (`http://host.docker.internal:4180`), mod `quick`.
- Sonuç: 366 LLM isteği (~26 M girdi jetonu, maliyet 0), koşu 1500 sn zaman aşımına uğradı (`TimeoutExpired`, run.json `running`). Rapor: `strix_runs/host-docker-internal-4180_da1d/findings.sarif` = 1 kapsam kaydı (DOM tabanlı XSS, main.js tam kod incelemesi: sorun yok). Gerçek zafiyet bulgusu yok; tarama tamamlanmadı, "temiz" kanıtı değil.
- Sonraki: süre sınırını (1500 sn) artırıp aynı modelle yeniden koş ya da Gemini kotası yenilenince; RAM kapısı (≤%89) geçerli.
- Kapanış: STRIX sandbox konteyneri (`dazzling_lalande`) `docker rm -f` ile kaldırıldı; Docker açık bırakıldı (clodfarm).
