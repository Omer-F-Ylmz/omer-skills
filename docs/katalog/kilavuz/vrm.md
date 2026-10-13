# vrm — 14 benzersiz kayıt

**Amaç:** Verimlilik ajanları: bağlam bütçesi ve sıkıştırma, ham çıktıyı bağlam dışında tutma, log özetleme, headroom geri çağırma, oturum devri, plan limit izleme, maliyet denetimi, paralel worktree.

**İç yapı:** Tümü [ajan], vrm-<konu>; bağlam (butce, kum-havuzu, cikti-sikistirma, log-ozetleyici, headroom), hafıza (oturum-kaydi, hafiza-arama, bilgi-tabani), paralellik (alt-ajan, worktree), maliyet/limit.

## En güçlü parçalar
- `vrm-baglam-butcesi` — Dosya, araç, istemin bağlam maliyetini tahmin edip kırpma önerir.
- `vrm-log-ozetleyici` — Büyük logu hata satırları, sayılar ve ilk başarısız nedene indirir.
- `vrm-oturum-kaydi` — Bitirmeden/compact'tan önce durum, karar, sonraki adımla devir kaydı.
- `vrm-headroom-geri-cagirma` — Headroom sıkıştırmasında hash ile orijinali getirir, okumayı daraltır.
- `vrm-plan-limit-izleme` — Claude plan oturum/haftalık limitlerini, yanma hızını, sıfırlama zamanını izler.
- `vrm-alt-ajan-dagitim` — Bağımsız işi sözleşmeli paralel alt görevlere bölüp yalnız özet döndürür.
- `vrm-baglam-kum-havuzu` — Sandbox analiz ve arama indeksiyle ham çıktıyı bağlam dışında tutar.
- `vrm-worktree-paralel` — Görev başına dal, port/env çakışması ve temizlikle paralel worktree.

## Birlikte kullanım
- vrm-baglam-butcesi + vrm-cikti-sikistirma + vrm-log-ozetleyici.
- vrm-oturum-kaydi → vrm-hafiza-arama: devir ve sonraki oturumda geri bulma.
- cli ailesindeki rtk, headroom, jev araçlarıyla.

## Tuzaklar
- vrm-hafiza-arama ile claude-mem:mem-search, vrm-oturum-kaydi ile claude-mem:handoff çakışır.
- vrm-headroom-geri-cagirma headroom vekilinin kurulu olmasını gerektirir.
- vrm-maliyet-denetci ile ecc:cost-tracking örtüşür.

## Üyeler
- ajan (14): vrm-alt-ajan-dagitim, vrm-baglam-butcesi, vrm-baglam-kum-havuzu, vrm-bilgi-tabani-hazirla, vrm-cikti-sikistirma, vrm-dx-surtunme, vrm-hafiza-arama, vrm-headroom-geri-cagirma, vrm-log-ozetleyici, vrm-maliyet-denetci, vrm-ortam-yoneticisi, vrm-oturum-kaydi, vrm-plan-limit-izleme, vrm-worktree-paralel
