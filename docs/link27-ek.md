# LINK-27 EK — gözden geçirmede atlandığı görülenler (27 Eki 19:30)
Kurallar link27-kalan-kurulum.md ile aynı. Her madde [x] + log + .kos/kopru/son-durum.md'ye 1 satır.

- [x] F1 (koşuldu, zaman aşımı, bulgu yok; docs/kurulumlar/strix.md) STRIX: Docker açıkken ücretsiz modelle (Groq/OpenRouter :free) yeniden koş (docs/kurulumlar/strix.md); bitince Docker kapanmasın (clodfarm), yalnız STRIX konteyneri kapanır
- [x] F2 (docs/ram-kurali.md; ajan_sira'da esik()/tavan()/ram_bekle zaten var, kod değişmedi) RAM önerileri (devir notu): ajan_sira boş RAM'e göre ajan sayısı; Docker/Ollama/STRIX iş bitince kapat kuralı → .kos/kopru/ajan_sira.py + docs/ram-kurali.md
- [ ] F3 BEKLİYOR (docs/headroom-f3.md): Headroom: MCP "havuz 404" (~/.local/bin/headroom sürümü ≠ desktop 0.39.0) → MCP kopyasını 0.39.0'a yükselt; proxy 1.5 GB RAM → ayar/önbellek ile düşür (Headroom KALDIRILMAZ/durdurulmaz), önce/sonra ölç
- [x] F4 (npm ci + build geçti, preview HTTP 200) 3d-model-anything (wesbos): klonlu → npm ci + build + preview smoke
- [x] F5 (dashersw/liquid-glass-js, şablona eklendi, build geçti) paket kimliği belirsiz (npm liquid-glass-js 0.1.0 eamonliu mu, dashersw mu?) Liquid Glass.js: araclar\sablon-3d-site'ye ekle, build geçsin
- [x] F6 (GERÇEK ÇAĞRI YAPILDI: görsel→GLB; docs/kurulumlar/hunyuan3d.md: HF Space yolu bulundu, gerçek çağrı+Blender bağı yapılmadı) Hunyuan3D (Tencent, ücretsiz metin/görsel→3D): yerel ya da ücretsiz API yolu bul, Blender ajan hattına bağla (blender-uretim); büyük model indirmesi öncesi boyut + C ≥80 GB
- [x] F7 (varlik_temizle.py + SKILL; çalıştırıldı) Metinden 3D oyun varlığı (Blender+Python, Deg4e9QjnaY) → blender-uretim'e "metin→varlık" akışı (UYARLA)
- [~] F8 (plan docs/link27-uyarla.md, uygulanmadı) Programatik reels skill (kinetik altyazı + ses, De6cx6MRxbZ) → OpenMontage/Remotion ile reel otomasyon skill'i (UYARLA)
- [x] F9 (tools/oturum_mesaj.py + kural; Hermes bağlanmadı) CC Mods (oturumlar arası mesaj, dashboard, basit işi Haiku'ya): oturumlar arası mesajı Hermes'e, Haiku yönlendirmesini ajan_sira'ya bağla (UYARLA)
- [x] F10 (departman-diger'e 5 rol satırı; videonun 27 rol listesi yok, ölçülmedi) 27 ajanlı şirket (Gbrain+Hermes): departman-* yapımızla karşılaştır, eksik rolleri ekle (UYARLA)
- [x] F11 (docs/borsa-botu/link27.md) Borsa-botu: self-improve trading bot mimarisi + Claude+TradingView+Fintables BIST terminali → areas borsa-botu planına docs/borsa-botu/link27.md (UYARLA, kod yok)
- Not: Bytez (Ömer hesap açarsa), kitap gibi site (SONRA), Meshy/Tripo + coucou + 4070 Ti (Ömer çıkardı)
- [ ] F12 HF_TOKEN eklendi (Ömer 20:31, kullanıcı ortamı): yeni süreçte görünür olduğunu doğrula (değer yazma), tools/ucretsiz_havuz.py'de HF Inference model satırını aç (ücretsiz bir sohbet modeli), 1 test çağrısı; Hunyuan3D (F6) indirmesinde de bu token kullanılır
- [ ] F12 BEKLİYOR: HF_TOKEN var, router.huggingface.co 402 (kredi yok); ücretsiz havuza HF satırı eklenmedi
