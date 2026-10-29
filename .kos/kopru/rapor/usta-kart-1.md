# USTA-KART-1 tur5 (29 Eki)
- Karar: üretim Haiku'ya taşındı (alt ajan yolu; claude -p 399 sn soğuk başlatma atlandı). Aynı 32 kalem (40 değil: usta.jsonl'de 32 kart var).
- Haiku medium: hakem (bağımsız Haiku alt ajan) 29/32 = %91 < %92 → merdiven: Haiku high.
- Haiku high: 31/32 = %97 ≥ %92 KAPI GEÇTİ (tek ret: örnek codex exec, kullanım örneği değil).
- Maliyet: ölçülemedi ($ alınmadı); alt ajan jetonu: medium ~4×32k + hakem 58k; high ~4×43k + hakem 57k (toplam ≈ 0,45M Haiku jeton).
- Kod: usta_kart.py hazirla/isle komutları; çıktı .kos/kopru/usta-haiku/haiku.jsonl (medium sonuçları _medium/). usta.jsonl'e henüz birleştirilmedi; ikinci göz (ücretsiz doğrulama) Haiku hattında yok.
- Sıradaki: kalan kalemleri aynı hatla ölçekle (hazirla --g 8 genelleme gerekir: şu an yalnız mevcut kartlı kalemleri alır).
