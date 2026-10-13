---
name: ders-bankasi
description: Önceki koşulardan damıtılmış dersleri görev başında getirir, görev sonunda yeni ders kaydeder (ReasoningBank döngüsü). Tekrarlanan bir görev türüne başlarken ya da bir görev başarıyla/başarısızlıkla bitince kullan.
---

# Ders bankası

Döngü: görev başı getir (alaka eşiğini geçen ≤2 ders, ≤120 jeton) → uygula → sonuç → ders kaydet + kullanılan derse geri bildirim.
Claude Code'da bu döngü otomatik de koşar (yalnız yerel): `tools/ogrenme/kanca.py` kancası alt ajan başında dersi ekler, oturum sonunda yargılayıp ≤3 ders damıtır. claude.ai'de kanca yok — adımları elle izle.

Banka konumu `OGRENME_DIZIN` (içinde `dersler.jsonl`):
- Claude Code / Desktop (yerel): ayarlama, varsayılan `C:/Projeler/omer-skills/.kos/ogrenme`.
- claude.ai: banka konuşmalar arası kalıcı değil. Kullanıcı `dersler.jsonl` eklediyse onu bir klasöre koy, `OGRENME_DIZIN` o klasör; sonunda güncellenen `dersler.jsonl`'i kullanıcıya dosya olarak ver. Ek yoksa boş bankayla başla.

Komutlar (bu skill klasöründeki `ders.py`):
1. Başta: `python ders.py getir --ajan <rol> --gorev "<görevin tek satırı>"` → çıkan dersleri uygula; göreve uymuyorsa yok say.
2. Sonda, kullandığın her ders için: `python ders.py geri --id <id> --sonuc basari|basarisizlik`.
3. Görev öğretici olduysa en fazla 3 genellenebilir ders: `python ders.py ekle --ajan <rol> --sonuc basari|basarisizlik --kaynak <görev> --baslik "..." --kosul "ne zaman uygulanır" --icerik "ne yapılmalı"`. Göreve özgü sayı/içerik değil, kural/yöntem yaz. Sır, anahtar, kişisel veri yazma (süzgeç reddeder).
4. Bankayı görmek: `python ders.py liste`.

Ajan dosyalarına kalıcı yuva (yalnız yerel): `python onsoz.py enjekte <ajan.md> [--kuru] [--geri]`.
