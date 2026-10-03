# KANAL-2a — etiket + otomatik takip + envanter (3 Eki)
KARAR: tavan 35 araç (30'da commit+push, DUR). Model 0. Ölçüm günü: yalnız video motoru kodu/testleri, docs/, .kos/.
Ömer kuralı: gönderilen her yeni videonun kanalı otomatik takip (38 kanal kanallar.json'da onaylı).

## Kabul
- A1 tarihsiz (eski hat) + kararsız → "etiketsiz (eski hat)"; özet değerli·değersiz·etiketsiz; liste işlenen "n (eski k)" (k>0 ise; eski test değişmez).
- A2 B2 kayıt sayımı: degerli(kok, sayac) karar kaydı başına sınıf sayar (liste tekil ad kalır); kalan fark = aynı adın tekrar kayıtları.
- A3 takip_ekle(kok, vids, ctx, kuyruk): meta → .kos/kanal/video-kanal.json → yoksa uyarı (ağ yok); varsa değişmez; kuyruk notunda `kaynak: kanal:<id>` → ekleme yok. Bağlantı: akil.kapat (git status öncesi) + cli.toplu (parti dışı).
- A4 envanter: shorts sekmesi yok → 0 short, yarım değil. Canlı: envanter (arka plan, ≥60 sn yoklama) → etiket → liste.
- kırmızı-önce ayrı commit · mutasyon (varsa değişmez kaldır → kırmızı) · tam suit · gitleaks · arşiv · push · graphify update.

## Durum
- B2 teşhis: 32 bağsız kayıt / 27 tekil ad (jcode×3 · webcmd×3 · markitdown-microsoft×2).
