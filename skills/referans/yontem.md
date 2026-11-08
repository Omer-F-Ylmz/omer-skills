# Yöntem (mekanizma, lisans, yedekler)

Ret, residual akışta büyük ölçüde tek yön ile aracılanır (Arditi vd. 2024, arXiv 2406.11717): `r = ort(kötü) − ort(iyi)`, son istem tokeni, orta-geç katman; yönü yazıcı matrislerden `W' = W − w·r rᵀW` ile silmek reddi düşürür. Ölçtüğümüz gerçek heretic çıktısı tam bu biçimde: rank-1, tek global yön, kısmi güç.

Yöntemler arası fark ret yüzdesi değil **KL** (kalan kapasite). Gemma-3-12B'de ret 97→3/100 hepsinde; KL: mlabonne 1,04 · huihui-ai 0,45 · Heretic 0,16. Heretic farkı: (ret, KL) çok amaçlı arama + katman-ağırlık çekirdeği + LoRA rank-1.

Tek yön yetmediğinde: çok yönlü ret konileri (2502.17420), "tek yön + stil" ayrımı (2602.02132), reasoning'de ret cliff (2510.06036), MoE'de uzman dağınımı (2606.04160). Savunmalı modeller (Extended Refusal 2505.19056, AMRA 2608.18093) tek yönü zayıflatır → alt uzay + geniş istem seti + yedek DPO.

## Yedek merdiven (sırayla, her biri ölçülür)
1. rank-3 alt uzay, geniş katman aralığı, yüksek güç
2. ARA benzeri rank ≤50 LoRA (L-BFGS, koruma + itme kaybı)
3. Kısa DPO/ORPO: `unalignment/toxic-dpo-v0.2`, `mlabonne/harmful_behaviors`; QLoRA r=64, 1 epoch, 24 GB'da 7–14B, 48 GB'da 32B
4. Çalışma anı: kontrol vektörü + prefill + sistem istemi
5. Model değiştir (aynı boyutta daha az savunmalı taban)

## Lisans
Heretic AGPL-3.0, grimjim GPL-3.0, FailSpy MIT, Sumandora Apache-2.0. Yerel kullanım serbest; buradaki betikler kopya değil, kendi yazımımız. Aracı çalıştırmak lisans yükü doğurmaz, kodu gömüp dağıtmak doğurur.

## Açık kalanlar
Arditi ekinin sonu, FailSpy/Sumandora kod dosyaları, Heretic PR #211 ve v2 ARA tablosu, Fool's Gold (2608.17202) okunmadı. Qwen3/R1 topluluk sonuçları ve 35B router ölçümü eksik.
