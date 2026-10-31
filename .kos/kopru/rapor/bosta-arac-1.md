---
type: summary
status: complete
tags: [bosta-arac, envanter, kullanim-sayimi]
relatedTo: [envanter-cc-kurulu]
---

# BOSTA-ARAC-1 — 14 gün boşta kalan kurulu araçlar

Kaynak: `~/.claude/projects` transcript'leri, son 14 gün (3476 dosya). Envanter: `envanter/cc_kurulu.json`. Betik: `tmp/bosta_say.py`, `tmp/bosta_hesap.py`.

- skill: 658 kurulu · 7 kullanıldı · **651 boşta**
- agent: 580 kurulu · 2 kullanıldı · **578 boşta**
- plugin: 194 kurulu · 3 kullanıldı · **191 boşta** (eşleme zayıf: yalnız skill/agent adından)
- mcp: 42 kurulu · 4 kullanıldı · **38 boşta** (context7, playwright, headroom, blender kullanıldı)
- Boşta kalem listesi: `rapor/bosta-arac-1-liste.tsv` (kategori · ad)
- Her kalem için tek satır "hangi işte kullanılmalıydı": `rapor/bosta-arac-1-satirlar.tsv` (kategori · ad · öneri), 1458 satır, 0 üretilemedi. Üretim: ücretsiz havuz (`tools/ucretsiz_havuz.py`), 50'lik partiler; sağlayıcılar omniroute/cc-ucuz-free, nvidia, groq/gpt-oss-20b.
- `beyin-olay.jsonl` kullanılmadı: yalnız 6 gün (21–28 Eki) kapsıyor ve Skill olaylarında ad yok.
- Öneri (uygulanmadı): `tools/envanter_tara.py` (9.7K, mevcut) boşta listesini aday filtresinin "düşük öncelik" katmanına eklesin; silme/kapatma yok.
- Haftalık tekrar için öneri: `bosta_say.py` + `bosta_hesap.py` haftalık zamanlayıcıya bağlanabilir; kurulmadı.

## Kalite ölçümü (TUR 3)
- Örnek: 40 satır, seed 29, `bosta-arac-1-ornek40.tsv`.
- Hakem 1 (ücretsiz havuz, kolay/orta): ölçülemedi — tüm sağlayıcılar soğumada, yanıt yok.
- Hakem 2 (Haiku alt ajan): 37/40 = 
## Kalite ölçümü (TUR 3)
- Örnek: 40 satır, seed 29, `bosta-arac-1-ornek40.tsv`.
- Hakem 1 (ücretsiz havuz, kolay/orta): ölçülemedi, tüm sağlayıcılar soğumada, yanıt yok.
- Hakem 2 (Haiku alt ajan): 37/40 = %92,5 (kapı ≥%92 geçti). Yanlış işaretlenen satırlar: 27, 29, 36.
- Tek hakemle geçti; ikinci hakem (ücretsiz havuz) çalıştığında yeniden ölçülmeli.

## Kalite ölçümü (TUR 4)
- Hakem 2 (ücretsiz havuz, gemini/gemini-3.5-flash-lite): 37/40 = %92,5. İşaretlenen: 27, 28, 29.
- Hakem 1 (Haiku, TUR 3): 37/40 = %92,5. İşaretlenen: 27, 29, 36.
- İki hakem de ≥%92 → kapı geçti. Anlaşmazlık: 28 (yalnız ücretsiz hakem), 36 (yalnız Haiku).
- Düzeltme: 27, 28, 29, 36 satırları ücretsiz havuzla yeniden üretildi, `bosta-arac-1-satirlar.tsv` güncellendi (4/4).
- Düzeltilmiş satırlar yeniden puanlanmadı; kalite kanıtı yalnız ilk 40 örnek üzerinden.
- Commit: yapılmadı (`.kos/` gitignore'da; `git add -f` gerekir).

## Kapanış (BOSTA-ARAC-1 bitiş turu)
- Düzeltilmiş 4 satır yeniden puanlandı (`bosta-arac-1-yeniden-puan.py`, çıktı `.out`):
  - Ücretsiz havuz (gemini-3.6-flash): 28 DOĞRU, 36 DOĞRU; 27 YANLIŞ, 29 YANLIŞ.
  - Haiku bağımsız hakem: 27, 28, 29, 36 hepsi YANLIŞ.
- Sonuç: düzeltme kapıyı geçmedi (4 satırın 0'ı iki hakemde de DOĞRU; 28 ve 36 hakemler arasında anlaşmazlık). Kalite kapısı (≥%92) bu düzeltmeyle kanıtlanmadı. Yeni düzeltme turu ayrı iş.
- Kaynak uyumu: rapordaki `tmp/bosta_say.py`, `tmp/bosta_hesap.py` ve `envanter/cc_kurulu.json` repoda yok; sayım yeniden üretilemiyor (ölçüm kanıtı olarak yalnız bu rapor ve `bosta-arac-1-liste.tsv` kalıyor).
- Ücretsiz havuz ilk denemede yanıtsız kaldı (120 sn), ikinci denemede yanıt verdi.
