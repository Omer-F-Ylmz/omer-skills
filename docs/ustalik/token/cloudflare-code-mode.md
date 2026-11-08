# Cloudflare Code Mode MCP — ustalık kartı
Kaynak: IG De40732E27J (Nishant Gupta) · repo cloudflare/mcp · uç https://mcp.cloudflare.com/mcp (OAuth)
Kurulum durumu (5 Kas, doğrulandı): Desktop → "Cloudflare Code Mode" bağlayıcısı, whoami = omery3899@gmail.com · CC → ~/.claude.json `cloudflare-api` (http, aynı uç) · ajanlar CC oturumu üzerinden aynı sunucuyu görür.

Ne işe yarar: Cloudflare'in 2.500+ API ucunu tek MCP'de verir; araçları tek tek bağlama yüklemek yerine (≈1.17M token) model `search` ile gereken ucu bulur, küçük bir JS programı yazar, `execute` ile sandbox'ta çalıştırır, yalnız sonucu alır (≈1.1k token).
En iyi 3 kullanım:
1. Site yayını: Workers/Pages deploy, DNS kaydı, R2'ye varlık yükleme.
2. Güvenlik: Zero Trust, WAF kuralları, TLS ayarı (kapanış listesi madde 2–4).
3. Ücretsiz AI: Workers AI uçları (ucretsiz_havuz'da `cloudflare` halkası).
Akış: `docs` → `search` → `execute`. Önce whoami; hesap kimliği `CLOUDFLARE_ACCOUNT_ID` ortamda.
Tuzaklar: silme işlemleri geri alınamaz → Ömer'e sorulur; büyük liste çıktısını kodda filtrele.
Ders (token): "Code Mode" deseni = araç kataloğunu bağlama dökme, ara+kodla çağır. Bizdeki karşılığı arac-ara/ertele_katalog kapısı (NİHAİ 44) ve code-mode skill/MCP.
