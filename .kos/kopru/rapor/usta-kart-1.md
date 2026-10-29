# USTA-KART-1 tur5 (29 Eki)
- Karar: üretim Haiku'ya taşındı (alt ajan yolu; claude -p 399 sn soğuk başlatma atlandı). Aynı 32 kalem (40 değil: usta.jsonl'de 32 kart var).
- Haiku medium: hakem (bağımsız Haiku alt ajan) 29/32 = %91 < %92 → merdiven: Haiku high.
- Haiku high: 31/32 = %97 ≥ %92 KAPI GEÇTİ (tek ret: örnek codex exec, kullanım örneği değil).
- Maliyet: ölçülemedi ($ alınmadı); alt ajan jetonu: medium ~4×32k + hakem 58k; high ~4×43k + hakem 57k (toplam ≈ 0,45M Haiku jeton).
- Kod: usta_kart.py hazirla/isle komutları; çıktı .kos/kopru/usta-haiku/haiku.jsonl (medium sonuçları _medium/). usta.jsonl'e henüz birleştirilmedi; ikinci göz (ücretsiz doğrulama) Haiku hattında yok.
- Sıradaki: kalan kalemleri aynı hatla ölçekle (hazirla --g 8 genelleme gerekir: şu an yalnız mevcut kartlı kalemleri alır).

# TUR 8 (29 Eki)
- 100 yeni kart (13 Haiku high alt ajanı, 8'lik grup), usta.jsonl 200 kart. Boş ornek 48, boş kombin 47 (kaynakta yok → uydurma yok).
- Hakem (bağımsız Haiku alt ajan, 20 rastgele kart): 20/20 = %100 ≥ %92. Sınır: 5 kartta Read kaynağı kesti, o kısımlar doğrulanamadı; 15 kart tam doğrulandı.
- Maliyet: $ ölçülemedi; alt ajan jetonu 13 üretici ≈ 590k + hakem; kart başı ≈ 6k Haiku jetonu. Haiku medium ön denemesi yapılmadı (kısa kaynak ayrımı eklenmedi).
- Yedek: usta-haiku/_arsiv/tur7, usta.jsonl.bak. Push yok.
