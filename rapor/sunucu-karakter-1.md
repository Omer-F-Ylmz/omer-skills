# SUNUCU-KARAKTER-1 tur 2 — TUR BITTI (hakem kapısı geçilmedi)

Çıktı: `Desktop\Claude ile yapılanlar\sosyal-oto\sunucu\{free-ai-drop,curiosity-well}\` + `etiket-plani.md`. Kod: `tools/sunucu_rig.py`, `sunucu_uret.py`, `sunucu_video.py`. Yayın/yükleme yok.

## Görsel yol (ücretli yok)
- Gemini görsel: 429 kota dolu (diğer model adları 404). Pollinations: çalışıyor ama filigranlı, düşük kalite, seed tutarlılığı zayıf → kullanılmadı. Higgsfield/Cloudflare denenmedi (CF kotası 03:00 TR sonrası; giriş yok).
- Seçilen yol: kodla çizilmiş stilize karakter (Dropi robot, Wick baykuş). Aynı donanım + parametreli poz/ifade = tutarlılık kod garantili, seed gerekmez.

## Üretilenler (her marka)
- yon-alternatifleri.png (3 yön, 1 seçili), karakter-karti.png (ön/3-4/yan, 6 ifade, palet, kıyafet), tutarlilik-10-poz.png + tutarlilik/poz-01..10.png (reçete: aynı rig, yaw/ifade/kol/eğim parametreleri `POSES`).
- ses/: 2 edge-tts adayı + yerel SAPI Zira (~15 sn, İngilizce). edge-tts resmî olmayan uç → ticari yayın öncesi lisans notu etiket-plani.md'de.
- ornek-klip-*.mp4: 1080x1920, 13,1 sn (A) / 14,9 sn (B), ses zarfından dudak senkronu, AI rozeti her karede.

## Hakem (okuyucu, bağımsız, Ömer ölçeği)
- Tur 1: tutarlılık A 9/10, B 9/10 (≥8 geçti); yön 6, kart 7, klip 6-7, özgünlük 6, profesyonellik 5-6.
- Tur 2 (yön + hareket sonrası): tutarlılık 9/9; kart 7/7; yön 5/6; klip 5/5; özgünlük 5/5; profesyonellik 5/5.
- Kapı "her parça ≥8" GEÇİLMEDİ: yalnız tutarlılık geçti. Hakem puanları tur arası tutarsız (klip 6-7 → 5); örnekleme 0,5 sn aralıklı kare.

## Açık kalanlar (sonraki tur)
1. Klip: ağız 3-4 şekle bölünsün, gövde nefes/sallanma, her 0,25 sn ağız değişimi; Well son cümlelerde poz değişimi.
2. Yön alternatifleri farklı çizim dilinde (gölgeli/dokulu) yeniden; kartta yan görünüş kafa kayması + ifade etiketi/palet başlığı sıkışıklığı.
3. Özgünlük/derinlik: gölge, doku, ışık; vektör "stok maskot" izlenimi. Ücretsiz bulut görsel kotası dönünce (Cloudflare 03:00 TR) kılavuz referans olarak denenebilir.
4. Ses kalitesi insan kulağıyla ölçülmedi (hakem sesi dinleyemez); Ömer dinlemeli.
