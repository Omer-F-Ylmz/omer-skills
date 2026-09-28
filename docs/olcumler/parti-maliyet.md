# Parti maliyeti — ana ajan / alt ajan (MOTOR-M1 K1, 29 Eyl 2026)

Kaynak: `~/.claude/projects/C--Projeler-omer-skills/<oturum>.jsonl` + `<oturum>/subagents/*.jsonl` (gerçek `message.usage`). CC her içerik bloğunu ayrı satıra yazdığı için istekler `message.id` ile tekilleştirildi. Alt ajan = `subagents/` dosyaları + ana dosyadaki `isSidechain` satırları. Video = video-tarayici prompt'larındaki `video-cache/<id>` + `video paket|tara|kare|… <id>` komutları. Jev/OR = `mcp__jev__*` + `jev`/`openrouter` geçen Bash komutları; $ tutarı transcript'te yok → **$ veri yok** (sütundaki $0.000 ölçülemedi demektir). Hücre biçimi: istek · girdi · önbellek okuma · önbellek yazma · çıktı (k = bin jeton).

| Dalga | oturum | ana model | ana: istek · girdi · önb.okuma · önb.yazma · çıktı | alt: istek · girdi · önb.okuma · önb.yazma · çıktı | alt model | alt ajan türleri | Jev/OR çağrı · $ | video | ana/video (tüm jeton) |
|---|---|---|---|---|---|---|---|---|---|
| Parti C | 1/1 | claude-opus-5-5 | 81 · 0.2k · 14,432.1k · 1,031.5k · 146.7k | 69 · 120.7k · 1,688.0k · 268.6k · 52.2k | claude-sonnet-5 | video-tarayici×3, aday-arastirici×3, suite-kosucu×1 | 6 · $0.000 | 3 | 5,203.5k |
| Parti D + devam 1-4 | 5/5 | claude-opus-5-5 | 266 · 0.5k · 35,579.1k · 1,170.6k · 201.3k | 62 · 77.3k · 1,332.2k · 276.9k · 30.2k | claude-sonnet-5,claude-sonnet-5-5 | suite-kosucu×3, video-tarayici×3, aday-arastirici×1 | 21 · $0.000 | 3 | 12,317.2k |
| 24e-1 (+devam, kapanış) | 3/3 | claude-opus-5-5 | 85 · 105.0k · 10,444.6k · 750.1k · 139.4k | 8 · 0.0k · 101.3k · 16.1k · 0.9k | claude-sonnet-5-5 | suite-kosucu×1 | 9 · $0.000 | 0 | video yok |
| 24e-2 | 1/1 | claude-opus-5-5 | 25 · 0.1k · 4,128.1k · 220.3k · 91.6k | 26 · 0.1k · 1,728.4k · 211.7k · 15.3k | claude-sonnet-5-5 | Explore×1, suite-kosucu×1 | 4 · $0.000 | 0 | video yok |
| TOKEN-DENEME-2a | 1/1 | claude-opus-5-5 | 44 · 0.1k · 6,232.9k · 342.5k · 78.3k | 48 · 0.1k · 1,983.4k · 239.4k · 23.7k | claude-sonnet-5-5 | video-tarayici×4, Explore×1, suite-kosucu×1 | 12 · $0.000 | 4 | 1,663.5k |
| TOPLAM | | | 501 · 105.9k · 70,816.9k · 3,515.1k · 657.3k | 213 · 198.2k · 6,833.3k · 1,012.5k · 122.2k | | | | 10 | 7,509.5k |

ana/alt oranı (tüm jeton): 9.2 · (önbellek okuma hariç): 3.2 · çıktı: 5.4

## Video başına (video işlenen parti dalgaları: Parti C + Parti D, 6 video)

- Ana (claude-opus-5-5): 52.562k jeton (önbellek okuma dahil) → **8.760k/video**; önbellek okuma hariç 2.551k → 425k/video; çıktı 348k → 58k/video.
- Alt (Sonnet): 3.846k → 641k/video; önbellek okuma hariç 826k → 138k/video; çıktı 82k → 14k/video.
- Parti C 5.204k/video, Parti D (4 devam oturumu) 12.317k/video: devam oturumu sayısı ana payı ikiye katlıyor.
- 2a (4 video, yalnız tarama denemesi) ana 1.664k/video.

**Sonuç: parti dalgalarında ana/alt = 13,7× (tüm jeton) · 3,1× (önbellek okuma hariç) · 4,2× (çıktı); video başına maliyetin büyüğü ana Opus oturumunun her istekte yeniden okunan bağlamı.**

Notlar: alt ajan modeli Parti C'de claude-sonnet-5, Parti D sırasında claude-sonnet-5-5'e geçti (sebep ölçülmedi); 24e-1'den beri hepsi claude-sonnet-5-5. Beş dalga genelindeki oran tablonun altındaki satırda.
