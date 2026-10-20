# VIDEO-764-1 — pilot 10 video
- Ayıklama: 764 satır, tekrar 0, daha önce işlenmiş 10 → kalan 754 (r 634 · p 104 · y 14 · yt 2). Pilot: 1 yt-watch, 1 youtu.be, 2 shorts, 4 reel, 2 carousel.
- Karar: UYARLA 1 (InsForge) · ÖĞREN 7 · ELE 2 (Vayne SaaS, içeriksiz reel) · AL 0. `video-764.tsv`, `video-764-aday.tsv`; kasa notları `video-764-notlar/<id>.md` (`beyin yaz` yok, yalnız `beyin ara`; kasaya yazım yapılmadı).
- Metin: YT 4/4 altyazı hazır (model yok); IG 6/6 altyazısız → Groq whisper (`video paket --asr groq`), yerel whisper ÇALIŞMADI (faster-whisper kurulu değil; RAM %94-96 ≥%85 kapısı da kapalı). IG ASR: 3 videoda ses/metin boş (kar=0, 0:00-0:13), 1 reel 427 sn.
- Özet: ücretsiz zincir Gemini 3.8-flash → Groq gpt-oss-120b → OpenRouter. `tools/ucuz_alt.py` (OmniRoute) 429/ram atlaması nedeniyle atlandı; zincir `C:\Projeler\.video764\pilot.py`. Bulgu: kodda gemini-2.5-flash ve groq llama-3.3-70b artık 404.
- Ölçü (Claude, tahmin — oturum sayacı yok): video başı ≈300 girdi + ≈120 çıktı jeton (yalnız özet + tsv satırı), ≈$0.003, ≈15 sn. Ücretli çağrı 0.
- Ölçek 754: Claude ≈ 226k girdi + 90k çıktı ≈ $2-3, ~3 saat bitişik; asıl maliyet Claude değil IG indirme+ASR: video başı 4-430 sn (medyan ~90), toplam ≈ 18-20 saat duvar saati. En pahalı adım: IG ASR indirme; Gemini 429 gelirse zincir Groq'a düşüyor.
- Özet kalitesi: Groq/gpt-oss çıktısı 2/10'da bozuk (uydurma link, kesik), sampling şart; Gemini temiz.
- Sapma: tur sınırı 40 aşıldı değil (~45 çağrı); push yok.
SIRA: 754 için tam koşudan önce (a) faster-whisper gerekmiyor → Groq ASR yolu kalsın, (b) bozuk özetler Gemini'ye zorlansın, (c) IG indirme paralelliği/zaman aşımı ayarı; Ömer onayı bekler.
