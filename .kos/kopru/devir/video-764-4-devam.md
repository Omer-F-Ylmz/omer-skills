# VIDEO-764-4 d1 devir
- Altın set 40 + held-out 30: ogren/video-764-altin.json (tohum 764). Sonnet altın kararlar: ogren/video-764-4-tahmin.json["sonnet/altin"] (ÖĞREN 21 · UYARLA 12 · ELE 7; AL 0 → AL sınıfı örneği yok).
- Tutarlılık: tanım ilk denemede 8/10 (fark ELE↔ÖĞREN: model haberi/içeriksiz) → "AI-ajan alanındaysa ELE değil ÖĞREN" netleştirildi, altın yeniden verildi → 9/10 (kalan fark UYARLA↔ELE, ig-Dej2yO_M87p).
- Haiku vs altın: 35/40 = %87.5 (<%95). Cloudflare: günlük ücretsiz kota doldu (429); Groq gpt-oss-120b: dakika TPM 429 (3 deneme düştü). Karar verici SEÇİLMEDİ.
- Sayaç: claude 24/120 · havuz 19/200. Betik: .kos/kopru/video764_karar2.py (altin|ver|tutar|olc <cf|groq|haiku> <altin|heldout>); eksik: yeniden komutu, aday listesi.
- Sıradaki (d2): cf/groq kota açılınca olc ölçümü (groq için n=3 + 20 sn ara) → en ucuz ≥%95; yoksa ucuz + sınır vakasında Sonnet; held-out 30 kapısı; yeniden karar [karar-v2]; aday tsv/Obsidian/ogren.md; SkillSpector --no-llm planı.
