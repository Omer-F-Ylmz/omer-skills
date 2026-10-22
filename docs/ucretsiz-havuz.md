# Ücretsiz havuz — hangi iş, hangi çağrı

Kaynak: `tools/ucretsiz_havuz.py` (halkalar, kota, soğuma). Canlı durum: `.kos/kopru/havuz-envanter.tsv` (`python -I tools/havuz_envanter.py` ile yenile).
Anahtar değerleri hiçbir yere yazılmaz; yalnız varlık kontrolü yapılır.

## Roller (envanter sütunu `roller`)
- `M` metin · `TR` Türkçe doğru · `K` kod · `G` görsel (renk testi geçti) · `E` gömme

## Hangi iş → hangi çağrı
| İş | Çağrı | Not |
|---|---|---|
| Özet, log süzme | `cagir("ozet", istem, max_tokens=...)` | Z rolü; halka sırası kota/yük ile seçilir |
| Hakem (görsel) | `python .kos/kopru/gorsel_hakem.py <png...>` | 5 aile (gemini, nvidia, qwen, minimax, ministral); en az 3 aile uyarsa karar; önbellek `.kos/kopru/ucretsiz/hakem-onbellek.json` |
| Kod taslağı | `cagir(..., aile=)` ile K rolü modeli | Doğrulanmış K modeli için envanter `roller` sütununa bak; yoksa Claude'a düşer |
| İki bağımsız görüş | `iki_aile("ozet", istem)` | İki farklı aile, biri düşerse sıradaki |
| Çeviri/yazım | `cagir("yazim", istem)` | Türkçe doğru halkalar (TR) öncelikli |

## Halka durumu (20 Eki 2026 probu)
- G (görsel) doğrulandı — `python tools/gorsel_dogrula.py` (renk · OCR · sahne, 3/3 geçen G'de kalır; sonuç `.kos/kopru/ucretsiz/gorsel-dogrula.json`): gemini 3.1-flash-lite · gemini 3.5-flash-lite · groq qwen3.8-27b · openrouter minimax-m3.1-flash:free · omniroute cc-ucuz-free · mistral ministral-8b · nvidia llama-3.2-11b-vision-instruct · nvidia ising-calibration-1.5-31b
- G kapalı: gemini 3.6-flash · nvidia step-5-preview — 3 testte da erişilemedi (429/503/boş); yanlış yanıt değil, yeniden denenmeli
- Eski not: llama-3.2-11b-vision bir probda `Beyaz` demişti; bu turda üç testte de doğru (`Mavi.`, `HAVUZ 42.`) — tek probun sonucu kesin kapatma sayılmaz; hakemde ADAY değil, değişmedi
- Ölçüm: ilk turda 120 jeton düşünme metnini keserdi ve düşünme metni cevap sayılabiliyordu; son tur 1500 jeton + renk/OCR için yalnız son satır kuralıyla ölçüldü (sonuçlar bu tur)
- Kapalı/zaman aşımı (40 sn): nvidia deepseek-v4.1-flash, gemma-4-31b-it, glm-5.3(-flash), llama-guard-4, llama-3.2-90b-vision; gemini 3.8-flash
- Metin yok (400/404): nvidia nemotron-3-ultra, nemotron-3.5-lightning (görsel), riva-translate, safety-guard; openrouter nemotron-3-ultra:free (görsel yok)
- Hız sınırı başlıkları groq/mistral döner; diğerleri 429 gövdesiyle bildirir

## Kurallar
- 429/5xx/zaman aşımı → beklemeden sıradaki halka; düşen halka soğuma sonra tek deneme.
- Claude (Haiku) son çare; yalnız çağıranın `haiku_tavan` değeri kadar.
- Tek aile ile karar verilmez (hakem en az 3 aile ister; altı → TEK-AİLE veya Haiku tek oy).
