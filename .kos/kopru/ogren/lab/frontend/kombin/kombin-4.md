# kombin-4 — Desktop kombin: referans inceleme (ÖĞREN-2 d3, G1)
- İş türü: Desktop Claude'un bir referans siteyi/tasarımı inceleyip CC'ye devretmesi. Araçlar (`ogren/desktop-araclar.md`): Claude in Chrome · yerleşik tarayıcı · claude-design (köprü MCP) · Figma / Stitch / 21st bağlayıcıları · cc-kopru.
- Zincir: (1) Desktop: Chrome/Figma/claude-design ile referansa bak (görsel bakış Desktop'un güçlü işi) → (2) Desktop: bulguyu 10–15 satır metne indir (renk, tipografi, yerleşim, ritim; varlık kopyalama yok) → (3) cc-kopru `ajan`/`komut` ile CC'ye ver → (4) CC: kombin-1 zinciri (ref.mjs ölçümü → DESIGN.md → kod → diff).
- Devir noktası: Desktop çıktısı tek metin (DESIGN.md taslağı), ekran görüntüsü CC'ye taşınmaz; CC kendi ref.mjs ölçümüyle sayıyı doğrular.
- Kimde: bakış/estetik yargısı Desktop (görüntü tokenı pahalı ama tek seferlik); ölçüm, kod, diff döngüsü CC (sayı çıktısı ucuz).
- KOŞU: DENENMEDİ (d3). Neden: Desktop araçları (Chrome/Figma/claude-design bağlayıcıları) CC oturumundan çağrılamaz; CC tarafı (adım 4) kombin-1'de doğrulandı (diff 7,51 % → 0 %). claude-design MCP kartı yerel köprü kaynağından (tools/cc-kopru/tasarim.mjs) yazıldı, uzak servis çağrılmadı.
- Tuzak: Desktop'ta ekran görüntüsü tekrar tekrar bakmak token yer; bakışı bir kez yapıp metne indirmek kuralı. Pencere kuralı: CC tarafı yalnız headless; varsayılan tarayıcı (Opera) açılmaz.
