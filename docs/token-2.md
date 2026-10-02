# TOKEN-2 — claude-mem observer önbelleği (L3) · 2 Eki 2026 · DURUM: kapandı (TOKEN-2c) — yama AL

## 1. Teşhis
- Observer'ın 14 gündeki 46.2M ağırlıklı tokenının tamamı 678 tek atımlık compress isteğinden geliyor (`runStandaloneObserverPrompt`, `maxTurns:1`).
- Her yük benzersiz ve sistem istemi boş, bu yüzden önbellek okuması olamaz. Yazılan önbellek bir daha okunmuyor.
- 1h TTL, CLI'nin abonelik varsayılanından geliyor. `settingSources:[]` olduğu için settings.json:680 yüklenmiyor.
- Ana observer oturumu `--no-session-persistence` ile koşuyor. Transcript'i olmadığı için ölçülemedi (Ek3).

## 2. Yama (claude-mem 13.25.2)
- `tools/cmem_yama.py`: worker-service.cjs'te yalnız compress çağrısına `DISABLE_PROMPT_CACHING:"1"` ekler. Yedek alır, idempotenttir ve en yeni sürümü bulur. `node --check` kırık çıkarsa geri alır. `--kontrol` ve `--geri` seçenekleri var. Çapa sayısı 0 ya da >1 olursa DUR.
- Elenen yollar: (a) claude-mem ayarlarında TTL ya da önbellek anahtarı yok. (b) Worker env'i kalıcı değil ve ana observer oturumunu da etkiler.
- `token_olc`: son compress isteğinde 1h yazma görülürse UYARI verir. claude-mem güncellenince yama düşer; `python tools/cmem_yama.py` yeniden koşulur.
- Kanıt: 32eef5e (kırmızı) → 07dda53 (yeşil, 28/28).

## 3. Karar — AL (Ömer)
- Önbellek modelin çıktısını değiştirmez, bu yüzden işlevsel kanıt yeterli sayıldı: worker sağlıklı · yamadan sonra gözlem 4744/4745 · compress 1h yazma 0.
- Kör puan ve sayı eşleştirmesi bu karar için yapılmadı. Düşüş gürültü payının içinde kalsa bile kural 21 gereği karar AL.

## 4. Önce/sonra maliyet (compress, haiku-4-5, message.id tekil)
- Önce tabanı: `kapi-once` penceresinde (t0–t2) compress isteği 0 çıktı. Kayıtlar dosya mtime'ına göre değil, kendi timestamp'lerine göre tarandı; sonuç değişmedi. Bu yüzden taban olarak yama öncesi 14 gün kullanıldı (18 Eyl–2 Eki 16:34Z, n=518; 158 sıfır-token `<synthetic>` kayıt hariç). Sonra: `kapi-sonra` penceresi, n=4.
- Ağırlıklar (token_olc): girdi 1 · okuma 0.1 · 5m 1.25 · 1h 2 · çıktı 5.

| | n | 1h yazma | okuma | çağrı başı ağırlıklı | çağrı başı $ | ×48/gün $ |
|---|---|---|---|---|---|---|
| önce (14 gün) | 518 | 20.3M | 2.70M | 89.5k | 0.0895 | 4.30 |
| sonra | 4 | 0 | 54.6k | 16.6k | 0.0166 | 0.80 |

- Ham düşüş −%81, ama yükler eşit boyda değil: çağrı başı prompt önce 44.4k, sonra 13.6k token. Token başına normalize edilince ($/1k prompt 0.00202 → 0.00122) düşüş −%39.5.
- Yalnız girdi tarafına bakınca çıktı hariç ağırlıklı/prompt token 1.78'den 0.10'a iniyor. Önbellek yazma payı tamamen kalktı. Sonra tarafında kalan maliyetin çoğu çıktıdan geliyor.
- n=4 küçük bir örnek. Sayılar bağımsız bir yeniden sayımla doğrulandı (kapi_analiz.py kullanılmadı, ham jsonl'dan sayıldı); sapma yok.

## 5. Açık notlar
- (a) Önbellek kapalıyken compress istekleri yine 54.6k okuma gösterdi; kaynağı açıklanmadı → TOKEN-6.
- (b) Eşleştirme sorgusu (observations ⋈ sdk_sessions, content_session_id) 0 buldu; sebebi açıklanmadı. `kapi-once` koşusunun kendi penceresinde neden compress tetiklenmediği de açıklanmadı.
- (c) `discovery_tokens` (≈45.1M/12 gün) observer maliyeti sayılmamalı. Bu doğrulanmadı.

## 6. Sıradaki
- L3b adayı: ana observer oturumunu ölçülebilir yapmak, gerekirse Headroom'dan geçirerek. Kalite kapısı gerekir.
- Kör puan için ileride sonnet'e sabitlenmiş bir ajan tanımı gerekiyor. Agent aracında model parametresi yok.
- `.claude/token2/` (kapi · kapi_analiz · kor_cift · mühür betikleri) arşiv olarak commit'lendi.
