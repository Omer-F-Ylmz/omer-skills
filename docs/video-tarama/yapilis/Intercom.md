# Intercom

- tür: arac · durum: KURULU-KANITSIZ · videolar: DYexqiLgnIb,DbsSDgAm5JX,DbukLdmuB2x,De4rkL4MSDz,DeHUaCoPFTV,De_0D2tEa9y,De_iYRotE4D,DedbF9YDjmR,DeekQtwk30w,DeexITYieW2,DemfLd2I9EV,DeqGkciIB21,Der3v24JiU9,Detx5PHtW_R,DezCrecDDSm,DfFWZz-gOjz
- bizde: docs/envanter/envanter.tsv; plugin intercom@knowledge-work-plugins:docs\katalog\yetenek.tsv; intercom@knowledge-work-plugins:docs\katalog\yetenek.tsv

## Özellikler
- Stripe, PostHog, Intercom ve Canny verilerini Claude'a tek seferde verme
- Müşteri segmentasyonu: son 30 gündeki müşterileri Power Users / At-Risk / Churned olarak ayırma
- Her segment için ortak davranış, en riskli 10 müşteri ve bu hafta yapılacak 3 kurtarma adımı
- Çıktı: JSON + tek sayfa Markdown rapor
- Codebase audit: PII işleme, güvenlik açıkları ve performans darboğazlarını P0-P3 önceliğiyle listeleme
- Beş prompt sistemi: müşteri segmentasyonu, codebase audit, feature prioritization, pricing & paywall, haftalık üretim

## Videoda yapılış
Veriler (Stripe, PostHog, Intercom, Canny) Claude'a verilir; hazır prompt şöyle: 'Stripe, PostHog ve Intercom verilerimi al. Son 30 gündeki müşterileri Power Users / At-Risk / Churned olarak segment et. Her segment için ortak davranış çıkar, en riskli 10 müşteriyi ve bu hafta yapılacak 3 kurtarma adımını ver. Bana JSON + tek sayfa Markdown rapor ver.' Codebase audit promptu tüm repoyu tarar ve bulguları P0-P3 olarak sıralar.

## Bizdeki karşılık ve fark
BIZDE kayıtları: docs/envanter/envanter.tsv; plugin intercom@knowledge-work-plugins için docs\katalog\yetenek.tsv (iki kayıt). Satır içerikleri bu oturumda okunmadı; karşılaştırma yapılmadı.

## Al
Birden çok veri kaynağını tek prompta verip segment ve kurtarma listesi çıkarma; prompt şablonları

## At
Videoda bu sistemin sınırları, veri gizliliği veya maliyeti anlatılmadı; bilgi yok. Gelir rakamları videoda bir kullanıcının beyanı, doğrulanmadı.
