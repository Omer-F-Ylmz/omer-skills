# Yöntem

Ret residual akışta tek yönle aracılanır (Arditi 2024, 2406.11717): `r = ort(kötü) − ort(iyi)`, son token, orta-geç katman; `W' = W − w·r rᵀW`. Ölçülen heretic çıktısı tam bu: rank-1, tek global yön, kısmi güç.

Fark ret değil **KL**: Gemma-3-12B'de ret 97→3/100 hepsinde, KL mlabonne 1,04 · huihui 0,45 · Heretic 0,16.

Yetmezse: çok yönlü koniler (2502.17420), stil ayrımı (2602.02132), reasoning ret cliff (2510.06036), MoE uzman dağınımı (2606.04160). Savunmalı modeller (2505.19056, 2608.18093) tek yönü zayıflatır.

Yedek merdiven: rank-3 → ARA LoRA → kısa DPO/ORPO → çalışma anı → model değiştir.

Lisans: Heretic AGPL-3.0, grimjim GPL-3.0, FailSpy MIT. Yerel kullanım serbest; buradaki betikler kendi yazımımız.
