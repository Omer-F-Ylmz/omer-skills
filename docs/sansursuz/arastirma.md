---
type: research
status: draft
tags: [sansursuz, abliteration, heretic, refusal]
relatedTo: [arastirma-a, arastirma-b, tersine, karar-agaci]
---
# SANSURSUZ-3 araştırma özeti (3 Kas 2026)

Kapsam: açık ağırlıklı LLM'lerde "ret" davranışını kaldırma yöntemleri; yalnız yerel/kendi kullanım. Ayrıntı ve kaynakça linkleri:
- **arastirma-a.md**, Arditi 2024, FailSpy, Sumandora, mlabonne, grimjim, Heretic (kaynak/mekanizma, sayılar, lisans).
- **arastirma-b.md**, Arditi sonrası makaleler (çok yönlü ret, MoE, reasoning, savunmalar) + alternatif yollar.
- **tersine.md**, gerçek heretic ağırlıklarının tensör tensör ölçümü (bu PC'de ölçüldü).
- **karar-agaci.md**, model-bağımsız tarif ve donanım tablosu.

## Ana bulgular
1. Ret büyük ölçüde **residual akışta tek bir yön**: `r = ort(kötü istem) − ort(iyi istem)` (son istem tokeni, orta-geç katman). Yönü çıkarıp yazan matrislerden (`o_proj`, `down_proj`) `W' = W − w·r rᵀW` ile silmek reddi düşürür (Arditi 2406.11717). Ölçümümüz (tersine.md): Heretic çıktısı da tam bu biçimde, fark matrisi rank-1.
2. Yöntemler arası fark ret % değil **KL (sağlam kalan kapasite)**: Gemma-3-12B'de ret 97→3/100 hepsinde; KL mlabonne 1.04, huihui-ai 0.45, Heretic 0.16 (Heretic README v1.0.1). Heretic farkı: Optuna TPE ile (ret, KL) birlikte arama + katman-ağırlık çekirdeği + LoRA rank-1 uygulama.
3. Tek yön yetmeyebilir: çok yönlü ret konileri (2502.17420), "tek yön + stil" ayrımı (2602.02132), düşünme izinde ret (2510.06036). Heretic v2 "ARA" (rank ≤50) bu yüzden eklenmiş (makalesi yok).
4. Savunmalardan ağırlık ortogonalleştirmeye karşı sonuç bildirenler: Extended Refusal (2505.19056), AMRA (2608.18093); TAR/circuit breakers/ReFAT/gpt-oss için ortogonalleştirmeye karşı kanıt bulunamadı ("bildirilmemiş").
5. MoE: Heretic her uzmanın down-proj'unu tek tek düzenliyor, router'a dokunmuyor; makalelerde MoE'ye doğrudan sınama yok (çıkarım), tersine.md'de 35B-A3B üzerinde ölçüldü.
6. Alternatifler (ağırlık dışı): kontrol vektörü, prefill, şablon, DPO/ORPO/LoRA, birleştirme, tablo arastirma-b.md Bölüm 2; hepsi ya kalite/donanım bedeli ya da zayıf kanıt.

## Lisans
Heretic AGPL-3.0, grimjim GPL-3.0, FailSpy MIT, Sumandora Apache-2.0. Kendi yerel kullanım serbest; kod kopyalayıp dağıtırsak koşullar döner. Bu çalışmada kod kopyalanmadı, yalnız fikir/ölçüm.

## Okunamayanlar
Arditi ekinin sonu, FailSpy/Sumandora kod dosyaları, Heretic PR #211 ve v2 ARA tablosu, Fool's Gold (2608.17202), arastirma-a/b "açık noktalar".

## SANSURSUZ-2 için öneriler (birleşik)
Tam listeler: arastirma-a.md ve arastirma-b.md sonu. Öncelik sırası:
1. Hazır heretic varsa onu kullan (HF'de çoğu model için var); yoksa Heretic'i yerelde çalıştır (dağıtım yok → AGPL yükü yok).
2. Aday arama: 100–200 deneme (30–60 rastgele), hedef ret ≤%1–3, KL ≤0,01–0,2 (model boyutuna göre), yetenek kaybı ≤1 puan.
3. Tersine bulgusu: katman 0–3 dokunulmaz, ablasyon gücü ≈0,5–0,8 düz kernel, tek global yön (cos 0,99) → arama uzayı küçük tutulabilir.
4. Ölçümde ≥2 yargıç + elle örnekleme; düşünen modellerde düşünme izi ve son cevap ayrı sayılır.
5. Yedekler: çalışma anı kontrol vektörü → prefill → kısa DPO/ORPO.
