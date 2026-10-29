---
type: rapor
status: tamam
tags: [gitleaks, guvenlik, video-izle-kur-1]
relatedTo: [video-izle-kur-1, guvenlik-4]
---
# gitleaks-20 — 20 aracın 1084 bulgusu tek tek (TUR 7, 29 Eki)
Sonuç: gerçek sızıntı 0 · emin olunamayan 0 → 20 aracın 20'si KURULABİLİR. Sınıf: örnek/yer tutucu 609, test verisi 444, yanlış alarm 31.
Yöntem: `ogren/video-izle-kur-1/gitleaks20.py` — yol/değer kalıbıyla otomatik sınıf, kalan 60 satır maskeli bağlamla elle okundu (ELLE listesi, gerekçeli); yer tutucu sayılan 9 test/doc dışı satır da elle doğrulandı (hepsi #[test] içinde ya da istem metni örneği). Değer sütunu: ilk 4 karakter + uzunluk.
Magpie `internal/provider/google.go:76,85` clientSecret: Gemini CLI ve Antigravity'nin kurulu-uygulama (installed app) Google OAuth istemcisi; kodda yorum 'secret is no secret: it ships in CLI'. Google bu tür istemci sırrını gizli saymaz → yanlış alarm, Magpie'nin kendi sırrı değil.
Dikkat (risk değil, tercih): iFix AI, Magpie, ReelMimic, Cloudroom PostHog telemetrisi gömülü → kurulumda telemetri kapatılmalı.

## Araç başı özet
| araç | örnek/yer tutucu | test | yanlış alarm | gerçek | karar |
|---|---|---|---|---|---|
| AirLLM | 0 | 1 | 0 | 0 | KUR |
| Cloudroom | 0 | 0 | 2 | 0 | KUR |
| Diffusion_Studio_Editor | 1 | 0 | 0 | 0 | KUR |
| Fallow | 5 | 184 | 2 | 0 | KUR |
| Free_Claude_Code | 0 | 3 | 0 | 0 | KUR |
| Hindsight | 33 | 10 | 1 | 0 | KUR |
| Hypit | 0 | 0 | 1 | 0 | KUR |
| Jcode | 6 | 5 | 2 | 0 | KUR |
| Magpie | 55 | 78 | 8 | 0 | KUR |
| Munder_Difflin | 426 | 10 | 0 | 0 | KUR |
| OpenQodex | 0 | 56 | 0 | 0 | KUR |
| Orca | 56 | 95 | 12 | 0 | KUR |
| PhotoCraft | 1 | 0 | 0 | 0 | KUR |
| Prime_Agent | 1 | 1 | 0 | 0 | KUR |
| ReelMimic | 0 | 0 | 1 | 0 | KUR |
| Reicon | 0 | 0 | 1 | 0 | KUR |
| TradingAgents | 2 | 0 | 0 | 0 | KUR |
| iFix_AI | 0 | 0 | 1 | 0 | KUR |
| prompts.chat | 17 | 0 | 0 | 0 | KUR |
| tcl-lsp | 6 | 1 | 0 | 0 | KUR |

## Bulguların tamamı
| araç | dosya:satır | kural | değer | sınıf | gerekçe |
|---|---|---|---|---|---|
| AirLLM | `air_llm/tests/test_notebooks/test_sealllm.ipynb:3246` | huggingface-access-token | `hf_a…/37` | test-verisi | test/fixture dizini |
| Cloudroom | `gui/apps/server/src/services/cloudroom/github-login.ts:11` | generic-api-key | `Ov23…/20` | yanlis-alarm | GitHub OAuth client ID (Ov23..) herkese acik tanimlayici, sir degil |
| Cloudroom | `gui/packages/config/src/env-vars.ts:360` | generic-api-key | `phc_…/48` | yanlis-alarm | PostHog phc_ proje anahtari: istemci tarafi icin herkese acik tasarim |
| Diffusion_Studio_Editor | `apps/web/.env.example:2` | generic-api-key | `sb_p…/46` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Fallow | `.github/workflows/fuzz-smoke.yml:63` | generic-api-key | `fuzz…/47` | yanlis-alarm | actions/cache 'key:' onbellek anahtari dizgesi |
| Fallow | `benchmarks/type-aware-semantic-capabilities.json:69` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-semantic-capabilities.json:911` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:399` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:418` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:437` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:456` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:494` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:513` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:551` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:570` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:589` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:608` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:646` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:665` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:684` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:703` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:722` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:741` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:760` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:779` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:798` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:817` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:836` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:855` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:893` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:912` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:931` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:950` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:969` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:988` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1045` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1064` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1083` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1140` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1159` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1178` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1197` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1216` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1235` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1254` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1273` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1292` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1349` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1368` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1406` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1425` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1444` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1463` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1482` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1501` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1520` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1539` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1558` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1577` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1596` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1615` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1634` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1653` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1672` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1691` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1710` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1767` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1805` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1824` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1862` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1900` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1938` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1957` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1976` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:1995` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2014` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2033` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2071` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2090` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2109` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2128` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2185` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2204` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2223` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2242` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2261` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2299` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2318` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2337` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2356` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2375` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2394` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2432` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2470` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2489` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2508` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2527` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2546` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2565` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2584` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2622` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2641` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2660` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2679` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2698` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2755` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2774` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2812` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2831` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2850` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2888` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2926` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2945` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2964` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:2983` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3002` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3021` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3040` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3059` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3078` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3097` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3116` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3135` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3154` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3173` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3192` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3211` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3230` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3249` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3306` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3325` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3344` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3363` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3382` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3401` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3420` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3439` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3458` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3477` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3496` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3515` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3534` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3572` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3591` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3629` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3667` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3688` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3707` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3726` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3745` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3764` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3783` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3802` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3821` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3840` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3878` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3897` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3916` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3935` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3954` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3973` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:3992` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:4011` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:4030` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:4049` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:4068` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:4106` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:4125` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:4144` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:4182` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:4201` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:4239` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:4258` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:4296` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:4334` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:4353` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `benchmarks/type-aware-corpus-evidence.json:4402` | generic-api-key | `tac_…/24` | test-verisi | test/fixture dizini |
| Fallow | `crates/core/src/analyze/security/hardcoded_secret.rs:852` | private-key | `----…/318` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Fallow | `crates/core/src/analyze/security/hardcoded_secret.rs:502` | generic-api-key | `mF9a…/20` | test-verisi | Fallow'un sir-tespit kuralinin test ornekleri |
| Fallow | `crates/core/src/analyze/security/hardcoded_secret.rs:506` | generic-api-key | `mF9a…/20` | test-verisi | Fallow'un sir-tespit kuralinin test ornekleri |
| Fallow | `crates/core/src/analyze/security/hardcoded_secret.rs:944` | jwt | `eyJh…/61` | test-verisi | Fallow'un sir-tespit kuralinin test ornekleri |
| Fallow | `crates/core/src/analyze/security/hardcoded_secret.rs:1017` | jwt | `eyJh…/61` | test-verisi | Fallow'un sir-tespit kuralinin test ornekleri |
| Fallow | `crates/extract/src/visitor/tests.rs:2212` | generic-api-key | `mF9a…/20` | test-verisi | ayristirici testindeki uydurma degerler |
| Fallow | `crates/extract/src/visitor/tests.rs:2232` | generic-api-key | `R8vK…/20` | test-verisi | ayristirici testindeki uydurma degerler |
| Fallow | `crates/extract/src/visitor/tests.rs:2248` | generic-api-key | `n7Pq…/20` | test-verisi | ayristirici testindeki uydurma degerler |
| Fallow | `crates/extract/src/visitor/tests.rs:2276` | generic-api-key | `mF9a…/20` | test-verisi | ayristirici testindeki uydurma degerler |
| Fallow | `scripts/signing-migration.json:5` | generic-api-key | `v+9n…/44` | yanlis-alarm | GitHub ortam PUBLIC key'i (key_id+key, sealed-box acik anahtar); workflow 'unchanged public key' diyor |
| Fallow | `tests/fixtures/security-hardcoded-secret-892/src/entropy.ts:1` | generic-api-key | `mF9a…/20` | test-verisi | test/fixture dizini |
| Fallow | `tests/fixtures/security-hardcoded-secret-892/src/object.ts:2` | generic-api-key | `n7Pq…/20` | test-verisi | test/fixture dizini |
| Fallow | `tests/fixtures/security-hardcoded-secret-892/src/assignment.ts:2` | generic-api-key | `Qz7L…/20` | test-verisi | test/fixture dizini |
| Fallow | `tests/fixtures/security-hardcoded-secret-892/src/template.ts:1` | generic-api-key | `R8vK…/20` | test-verisi | test/fixture dizini |
| Fallow | `tests/fixtures/security-hardcoded-secret-892/tests/provider.test.ts:1` | generic-api-key | `AKIA…/20` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Fallow | `tests/fixtures/security-hardcoded-secret-892/src/safe.ts:4` | generic-api-key | `0123…/40` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Fallow | `tools/mutation-runner/test/protocol.test.mjs:188` | generic-api-key | `0123…/22` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Fallow | `tools/mutation-runner/test/protocol.test.mjs:200` | generic-api-key | `0123…/16` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Free_Claude_Code | `tests/cli/test_hermes_config.py:53` | generic-api-key | `FCC_…/17` | test-verisi | test/fixture dizini |
| Free_Claude_Code | `tests/cli/test_hermes_config.py:61` | generic-api-key | `FCC_…/17` | test-verisi | test/fixture dizini |
| Free_Claude_Code | `tests/cli/test_hermes_config.py:154` | generic-api-key | `FCC_…/17` | test-verisi | test/fixture dizini |
| Hindsight | `.env.example:169` | generic-api-key | `qwen…/20` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Hindsight | `hindsight-api-slim/tests/test_recall_boost.py:344` | generic-api-key | `stag…/26` | test-verisi | test/fixture dizini |
| Hindsight | `hindsight-api-slim/tests/test_recall_boost.py:377` | generic-api-key | `stag…/26` | test-verisi | test/fixture dizini |
| Hindsight | `hindsight-api-slim/tests/test_recall_boost.py:432` | generic-api-key | `stag…/26` | test-verisi | test/fixture dizini |
| Hindsight | `hindsight-api-slim/tests/test_recall_boost.py:442` | generic-api-key | `stag…/26` | test-verisi | test/fixture dizini |
| Hindsight | `hindsight-api-slim/hindsight_api/config.py:1695` | generic-api-key | `b1a0…/36` | yanlis-alarm | xAI OAuth client ID: herkese acik tanimlayici |
| Hindsight | `hindsight-api-slim/tests/test_memory_defense.py:60` | generic-api-key | `pypi…/20` | test-verisi | test/fixture dizini |
| Hindsight | `hindsight-cli/src/config.rs:607` | generic-api-key | `dCcx…/44` | test-verisi | #[test] fn icinde ayristirma testi degeri |
| Hindsight | `hindsight-dev/upgrade_tests/conftest.py:104` | generic-api-key | `llam…/23` | test-verisi | test/fixture dizini |
| Hindsight | `hindsight-dev/upgrade_tests/version_runner.py:64` | generic-api-key | `llam…/23` | test-verisi | test/fixture dizini |
| Hindsight | `hindsight-docs/docs/developer/development.md:54` | generic-api-key | `llam…/23` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Hindsight | `hindsight-docs/docs/sdks/embed.md:142` | generic-api-key | `llam…/23` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Hindsight | `hindsight-docs/docs/developer/mcp-server.md:70` | curl-auth-header | `your…/15` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Hindsight | `hindsight-docs/docs/developer/configuration.mdx:835` | generic-api-key | `llam…/23` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Hindsight | `hindsight-docs/versioned_docs/version-0.10/developer/development.md:54` | generic-api-key | `llam…/23` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Hindsight | `hindsight-docs/versioned_docs/version-0.10/sdks/embed.md:142` | generic-api-key | `llam…/23` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Hindsight | `hindsight-docs/versioned_docs/version-0.9/developer/development.md:54` | generic-api-key | `llam…/23` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Hindsight | `hindsight-docs/versioned_docs/version-0.9/sdks/embed.md:143` | generic-api-key | `llam…/23` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Hindsight | `hindsight-docs/versioned_docs/version-1.0/developer/development.md:54` | generic-api-key | `llam…/23` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Hindsight | `hindsight-docs/versioned_docs/version-0.9/developer/mcp-server.md:70` | curl-auth-header | `your…/15` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Hindsight | `hindsight-docs/versioned_docs/version-0.10/developer/mcp-server.md:70` | curl-auth-header | `your…/15` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Hindsight | `hindsight-docs/versioned_docs/version-1.0/sdks/embed.md:142` | generic-api-key | `llam…/23` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Hindsight | `hindsight-docs/versioned_docs/version-1.1/developer/development.md:54` | generic-api-key | `llam…/23` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Hindsight | `hindsight-docs/docs/developer/configuration.mdx:1682` | curl-auth-header | `your…/19` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Hindsight | `hindsight-docs/versioned_docs/version-0.10/developer/configuration.mdx:807` | generic-api-key | `llam…/23` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Hindsight | `hindsight-docs/versioned_docs/version-1.1/sdks/embed.md:142` | generic-api-key | `llam…/23` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Hindsight | `hindsight-docs/versioned_docs/version-1.0/developer/mcp-server.md:70` | curl-auth-header | `your…/15` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Hindsight | `hindsight-docs/versioned_docs/version-1.1/developer/mcp-server.md:70` | curl-auth-header | `your…/15` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Hindsight | `hindsight-docs/versioned_docs/version-0.10/developer/configuration.mdx:1500` | curl-auth-header | `your…/19` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Hindsight | `hindsight-docs/versioned_docs/version-1.0/developer/configuration.mdx:807` | generic-api-key | `llam…/23` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Hindsight | `hindsight-embed/tests/test_control_center.py:397` | generic-api-key | `sk-x…/14` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Hindsight | `hindsight-docs/versioned_docs/version-1.1/developer/configuration.mdx:833` | generic-api-key | `llam…/23` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Hindsight | `hindsight-embed/hindsight_embed/env.example:169` | generic-api-key | `qwen…/20` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Hindsight | `hindsight-docs/versioned_docs/version-0.9/developer/configuration.md:623` | generic-api-key | `llam…/23` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Hindsight | `hindsight-docs/versioned_docs/version-0.9/developer/configuration.md:1221` | curl-auth-header | `your…/19` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Hindsight | `hindsight-docs/versioned_docs/version-1.0/developer/configuration.mdx:1500` | curl-auth-header | `your…/19` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Hindsight | `hindsight-docs/versioned_docs/version-1.1/developer/configuration.mdx:1650` | curl-auth-header | `your…/19` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Hindsight | `hindsight-integrations/openclaw/tests/hooks.integration.test.ts:789` | generic-api-key | `sess…/17` | test-verisi | test/fixture dizini |
| Hindsight | `hindsight-integrations/openclaw/tests/hooks.integration.test.ts:806` | generic-api-key | `sess…/17` | test-verisi | test/fixture dizini |
| Hindsight | `skills/hindsight-docs/references/developer/development.md:54` | generic-api-key | `llam…/23` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Hindsight | `skills/hindsight-docs/references/sdks/embed.md:142` | generic-api-key | `llam…/23` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Hindsight | `skills/hindsight-docs/references/developer/mcp-server.md:70` | curl-auth-header | `your…/15` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Hindsight | `skills/hindsight-docs/references/developer/configuration.md:828` | generic-api-key | `llam…/23` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Hindsight | `skills/hindsight-docs/references/developer/configuration.md:1662` | curl-auth-header | `your…/19` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Hypit | `packages/provider-hypihub/src/oauth.ts:9` | generic-api-key | `hyc_…/28` | yanlis-alarm | OAuth client ID (hyc_): herkese acik tanimlayici |
| iFix_AI | `ifixai/telemetry.py:38` | generic-api-key | `phc_…/48` | yanlis-alarm | PostHog phc_ proje anahtari: herkese acik (telemetri; kurulumda kapatilabilir) |
| Jcode | `crates/jcode-app-core/src/tool/browser_fast_tests.rs:1061` | generic-api-key | `sk-t…/24` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Jcode | `crates/jcode-base/src/auth/cursor_tests.rs:298` | generic-api-key | `tok_…/13` | test-verisi | *_tests.rs test degeri |
| Jcode | `crates/jcode-base/src/auth/copilot_auth_tests.rs:641` | generic-api-key | `Iv1.…/20` | test-verisi | *_tests.rs test degeri |
| Jcode | `crates/jcode-base/src/gateway_tests.rs:90` | generic-api-key | `0123…/64` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Jcode | `crates/jcode-base/src/gateway_tests.rs:91` | generic-api-key | `fedc…/64` | test-verisi | *_tests.rs test degeri |
| Jcode | `crates/jcode-base/src/gateway_tests.rs:113` | generic-api-key | `0123…/64` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Jcode | `crates/jcode-base/src/gateway_tests.rs:114` | generic-api-key | `fedc…/64` | test-verisi | *_tests.rs test degeri |
| Jcode | `crates/jcode-base/src/auth/tests.rs:748` | jwt | `eyJh…/47` | test-verisi | test modulu JWT ornegi |
| Jcode | `crates/jcode-fuzzy/src/lib.rs:758` | generic-api-key | `clau…/15` | yanlis-alarm | bulanik arama test dizgesi ('claude...' model adi) |
| Jcode | `crates/jcode-fuzzy/src/lib.rs:761` | generic-api-key | `clau…/20` | yanlis-alarm | bulanik arama test dizgesi ('claude...' model adi) |
| Jcode | `crates/jcode-terminal-prompt/src/secret_pty_tests.rs:119` | generic-api-key | `AIza…/15` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Jcode | `scripts/repro/tls-bad-record-mac/src/main.rs:191` | generic-api-key | `sk-t…/18` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Jcode | `tests/e2e/test_support/mod.rs:681` | generic-api-key | `0123…/64` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/access/access_test.go:329` | generic-api-key | `sk-m…/23` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/cli/daemon_cli_test.go:143` | generic-api-key | `0123…/32` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/cli/gateway_keys_cli_test.go:75` | generic-api-key | `cpa-…/19` | test-verisi | test/fixture dizini |
| Magpie | `internal/cli/gateway_keys_cli_test.go:99` | generic-api-key | `cpa-…/19` | test-verisi | test/fixture dizini |
| Magpie | `internal/cli/gateway_keys_cli_test.go:99` | generic-api-key | `cpa-…/18` | test-verisi | test/fixture dizini |
| Magpie | `internal/daemon/daemon_test.go:438` | generic-api-key | `0123…/32` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gateway/copilot_refused_test.go:28` | generic-api-key | `gho_…/14` | test-verisi | test/fixture dizini |
| Magpie | `internal/gateway/groupfast_test.go:337` | generic-api-key | `clau…/24` | test-verisi | test/fixture dizini |
| Magpie | `internal/gateway/masked_sent_test.go:21` | generic-api-key | `sk-p…/36` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gateway/masked_sent_test.go:67` | generic-api-key | `sk-p…/36` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gateway/mask_actions_test.go:20` | generic-api-key | `sk-p…/36` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gateway/lite_lift_test.go:111` | generic-api-key | `sk-p…/36` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gateway/middleware_off_test.go:79` | generic-api-key | `sk-p…/36` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gateway/middleware_off_test.go:141` | generic-api-key | `sk-p…/36` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gateway/middleware_test.go:27` | generic-api-key | `sk-p…/36` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gateway/media_redact_test.go:21` | generic-api-key | `sk-p…/36` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gateway/overflow_stream_test.go:21` | generic-api-key | `ffbe…/36` | test-verisi | test/fixture dizini |
| Magpie | `internal/gateway/overflow_stream_test.go:22` | generic-api-key | `ffbe…/36` | test-verisi | test/fixture dizini |
| Magpie | `internal/gateway/overflow_stream_test.go:24` | generic-api-key | `ffbe…/36` | test-verisi | test/fixture dizini |
| Magpie | `internal/gateway/prev_response_test.go:225` | generic-api-key | `sk-p…/36` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gateway/lan_test.go:359` | generic-api-key | `dGhl…/24` | test-verisi | test/fixture dizini |
| Magpie | `internal/gateway/prompt_text_test.go:20` | generic-api-key | `sk-p…/36` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gateway/redact_test.go:55` | generic-api-key | `sk-p…/36` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gateway/redact_test.go:126` | generic-api-key | `sk-p…/36` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gateway/redact_test.go:175` | generic-api-key | `sk-p…/36` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gateway/remote_magpie_masked_test.go:21` | generic-api-key | `sk-p…/36` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gateway/responses_socket_test.go:23` | generic-api-key | `dGhl…/24` | test-verisi | test/fixture dizini |
| Magpie | `internal/gateway/testdata/upstream_bodies/anthropic-to-responses.json:1` | generic-api-key | `c036…/36` | test-verisi | test/fixture dizini |
| Magpie | `internal/gateway/testdata/upstream_bodies/responses-to-chat.json:1` | generic-api-key | `792f…/36` | test-verisi | test/fixture dizini |
| Magpie | `internal/gateway/testdata/upstream_bodies/anthropic-to-chat.json:1` | generic-api-key | `2062…/36` | test-verisi | test/fixture dizini |
| Magpie | `internal/gateway/testdata/opencode2_responses_tools.json:1` | generic-api-key | `ses_…/30` | test-verisi | test/fixture dizini |
| Magpie | `internal/gateway/unmasked_route_test.go:44` | generic-api-key | `sk-p…/36` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gateway/user_betas_test.go:158` | generic-api-key | `inte…/31` | test-verisi | test/fixture dizini |
| Magpie | `internal/gateway/unredacted_test.go:25` | generic-api-key | `sk-p…/36` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gateway/unredacted_test.go:164` | generic-api-key | `sk-p…/36` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gateway/unredacted_test.go:242` | generic-api-key | `sk-p…/36` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gateway/unredacted_test.go:295` | generic-api-key | `sk-p…/36` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gateway/testdata/workdir/codex-0.162.1-tool-search.json:1` | generic-api-key | `01a1…/36` | test-verisi | test/fixture dizini |
| Magpie | `internal/gateway/testdata/workdir/codex-0.162.0.json:1` | generic-api-key | `01a1…/36` | test-verisi | test/fixture dizini |
| Magpie | `internal/gui/apppage_test.go:231` | generic-api-key | `0123…/20` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gui/github_token_test.go:51` | generic-api-key | `gho_…/24` | test-verisi | test/fixture dizini |
| Magpie | `internal/gui/laststate_test.go:31` | generic-api-key | `ghp_…/14` | test-verisi | test/fixture dizini |
| Magpie | `internal/gui/masking_test.go:24` | generic-api-key | `sk-p…/36` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gui/masking_test.go:156` | generic-api-key | `sk_w…/35` | test-verisi | test/fixture dizini |
| Magpie | `internal/gui/mask_alert_test.go:139` | aws-access-token | `AKIA…/20` | test-verisi | test/fixture dizini |
| Magpie | `internal/gui/tests/browser-access.test.cjs:20` | generic-api-key | `0123…/32` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gui/tests/balance-fix.test.cjs:291` | generic-api-key | `eyJh…/41` | test-verisi | test/fixture dizini |
| Magpie | `internal/gui/tests/context-map-live.test.cjs:35` | generic-api-key | `01a1…/28` | test-verisi | test/fixture dizini |
| Magpie | `internal/gui/tests/context-window.test.cjs:45` | generic-api-key | `01a1…/28` | test-verisi | test/fixture dizini |
| Magpie | `internal/gui/tests/context-scroll-end.test.cjs:44` | generic-api-key | `01a1…/28` | test-verisi | test/fixture dizini |
| Magpie | `internal/gui/tests/context-text.test.cjs:45` | generic-api-key | `01a1…/28` | test-verisi | test/fixture dizini |
| Magpie | `internal/gui/tests/factory-key.test.cjs:14` | generic-api-key | `fk-a…/17` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gui/tests/context-map.test.cjs:47` | generic-api-key | `01a1…/28` | test-verisi | test/fixture dizini |
| Magpie | `internal/gui/tests/gateway-own-key.test.cjs:47` | generic-api-key | `cpa-…/19` | test-verisi | test/fixture dizini |
| Magpie | `internal/gui/tests/fixtures/curl/unsloth-studio.ps1:1` | curl-auth-header | `sk-u…/19` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gui/tests/fixtures/curl/zhipu.sh:1` | curl-auth-header | `YOUR…/12` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gui/tests/import-link-gemini.test.cjs:67` | generic-api-key | `sk-f…/15` | test-verisi | test/fixture dizini |
| Magpie | `internal/gui/tests/lan-docker.test.cjs:29` | generic-api-key | `sk-m…/26` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gui/tests/lan-public.test.cjs:28` | generic-api-key | `sk-m…/26` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gui/tests/mask-actions.test.cjs:18` | generic-api-key | `sk-p…/28` | test-verisi | test/fixture dizini |
| Magpie | `internal/gui/tests/mcp-oauth-app.test.cjs:23` | generic-api-key | `0123…/40` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gui/tests/masking-records.test.cjs:24` | generic-api-key | `sk-p…/24` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gui/web_app_test.go:29` | generic-api-key | `0123…/20` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gui/web_test.go:58` | generic-api-key | `0123…/16` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gui/web_test.go:62` | generic-api-key | `0123…/21` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gui/web_test.go:82` | generic-api-key | `0123…/21` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/gui/web_oneport_test.go:179` | generic-api-key | `0123…/32` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/mcpauth/github_app_test.go:194` | generic-api-key | `Ov23…/20` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/mcpauth/github_app_test.go:234` | generic-api-key | `Ov23…/20` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/mcpauth/github_app_test.go:263` | generic-api-key | `Ov23…/20` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/mcpauth/github_app_test.go:284` | generic-api-key | `Iv23…/20` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/pii/guard/testdata/tokens.json:20` | curl-auth-header | `eyJh…/117` | test-verisi | test/fixture dizini |
| Magpie | `internal/pii/guard/testdata/tokens.json:29` | generic-api-key | `sk-p…/48` | test-verisi | test/fixture dizini |
| Magpie | `internal/pii/guard/testdata/tokens.json:20` | jwt | `eyJh…/117` | test-verisi | test/fixture dizini |
| Magpie | `internal/provider/balance_test.go:374` | generic-api-key | `eyJh…/40` | test-verisi | test/fixture dizini |
| Magpie | `internal/provider/balance_test.go:491` | generic-api-key | `sk-s…/16` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/provider/migrate_movers_test.go:155` | generic-api-key | `fk-k…/23` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/provider/plugin_free_price_test.go:41` | generic-api-key | `devi…/14` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/provider/plugin_moved_test.go:72` | generic-api-key | `cog_…/16` | test-verisi | test/fixture dizini |
| Magpie | `internal/provider/google.go:76` | generic-api-key | `GOCS…/35` | yanlis-alarm | Gemini CLI / Antigravity'nin kurulu-uygulama OAuth istemcisi; kodda yorum: 'secret is no secret: it ships in CLI' — Google installed-app akisi, sir sayilmaz, Magpie'nin kendi sirri degil |
| Magpie | `internal/provider/google.go:85` | generic-api-key | `GOCS…/35` | yanlis-alarm | Gemini CLI / Antigravity'nin kurulu-uygulama OAuth istemcisi; kodda yorum: 'secret is no secret: it ships in CLI' — Google installed-app akisi, sir sayilmaz, Magpie'nin kendi sirri degil |
| Magpie | `internal/redact/decimal_test.go:106` | generic-api-key | `4417…/15` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/actions_test.go:45` | generic-api-key | `sk-p…/28` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/hits_test.go:52` | generic-api-key | `sk-p…/28` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/hits_test.go:68` | generic-api-key | `sk-p…/28` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/escape_test.go:127` | npm-access-token | `npm_…/40` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/redact/modelfits_test.go:22` | generic-api-key | `llam…/15` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/modelfits_test.go:24` | generic-api-key | `mixt…/18` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/modelfits_test.go:93` | generic-api-key | `9f2c…/32` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/code_test.go:30` | generic-api-key | `abc1…/12` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/code_test.go:34` | generic-api-key | `abcd…/12` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/redact/modelids_test.go:18` | generic-api-key | `019a…/36` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/modelids_test.go:19` | generic-api-key | `019a…/36` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/modelids_test.go:21` | generic-api-key | `4f2a…/36` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/modelids_test.go:25` | generic-api-key | `9f8e…/32` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/testdata/codex-0.162.1-request.json:1` | generic-api-key | `01a1…/36` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/eval_cases_test.go:22` | generic-api-key | `wJal…/22` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/eval_cases_test.go:301` | generic-api-key | `llam…/15` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/package_known_test.go:89` | generic-api-key | `Zq8v…/12` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/package_known_test.go:98` | generic-api-key | `Zq8h…/15` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/scrub_test.go:14` | jwt | `eyJh…/73` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/digest_test.go:20` | generic-api-key | `1a2b…/20` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/digest_test.go:21` | generic-api-key | `0123…/20` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/redact/digest_test.go:22` | generic-api-key | `0123…/24` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/redact/digest_test.go:23` | generic-api-key | `a1b2…/20` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/digest_test.go:24` | generic-api-key | `a1b2…/20` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/digest_test.go:25` | generic-api-key | `A1B2…/20` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/digest_test.go:37` | generic-api-key | `9f2c…/20` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/digest_test.go:38` | generic-api-key | `0123…/20` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/redact/digest_test.go:39` | generic-api-key | `0123…/18` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/redact/digest_test.go:43` | generic-api-key | `AbC1…/21` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/fieldvalue.go:25` | generic-api-key | `env.…/13` | yanlis-alarm | redakte kurali deseni (env.X degisken adi) |
| Magpie | `internal/redact/fieldvalue.go:188` | generic-api-key | `env.…/13` | yanlis-alarm | redakte kurali deseni (env.X degisken adi) |
| Magpie | `internal/redact/redact_test.go:14` | generic-api-key | `sk-p…/36` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/redact/redact_test.go:15` | generic-api-key | `ghp_…/38` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/redact/rules_test.go:9` | generic-api-key | `oc_s…/38` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Magpie | `internal/redact/rules_test.go:25` | generic-api-key | `Zq81…/20` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/rules_test.go:27` | generic-api-key | `Zq81…/20` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/rules_test.go:28` | generic-api-key | `Zq81…/20` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/rules_test.go:29` | generic-api-key | `Zq81…/20` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/shape_test.go:62` | github-pat | `ghp_…/40` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/shape_test.go:11` | generic-api-key | `sk_w…/35` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/shape_test.go:198` | generic-api-key | `sk_p…/26` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/shape_test.go:221` | generic-api-key | `sk_n…/24` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/model.go:174` | generic-api-key | `llam…/15` | yanlis-alarm | model adi dizgesi (llama...) |
| Magpie | `internal/redact/package_names_test.go:93` | generic-api-key | `AbC1…/18` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/package_names_test.go:94` | generic-api-key | `Zq8v…/12` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/fieldvalue_test.go:45` | generic-api-key | `env.…/13` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/fieldvalue_test.go:85` | generic-api-key | `AbC1…/18` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/fieldvalue_test.go:90` | generic-api-key | `Lk8x…/12` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/fieldvalue_test.go:92` | generic-api-key | `k9x2…/16` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/fieldvalue_test.go:93` | generic-api-key | `ab12…/12` | test-verisi | test/fixture dizini |
| Magpie | `internal/redact/fieldvalue_test.go:95` | generic-api-key | `tok-…/16` | test-verisi | test/fixture dizini |
| Magpie | `internal/stats/stats.go:32` | generic-api-key | `phc_…/48` | yanlis-alarm | PostHog phc_ proje anahtari: herkese acik |
| Magpie | `internal/provider/vertex_test.go:401` | generic-api-key | `AQ.A…/15` | test-verisi | test/fixture dizini |
| Magpie | `internal/provider/vertex_test.go:403` | generic-api-key | `AQ.A…/15` | test-verisi | test/fixture dizini |
| Magpie | `internal/provider/vertex_test.go:404` | generic-api-key | `AQ.A…/15` | test-verisi | test/fixture dizini |
| Magpie | `site/public/docs/zh/integrate.html:100` | curl-auth-header | `magp…/11` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Magpie | `site/public/docs/integrate.html:100` | curl-auth-header | `magp…/11` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Magpie | `site/worker.js:185` | generic-api-key | `phc_…/48` | yanlis-alarm | PostHog phc_ proje anahtari: herkese acik |
| Magpie | `site/worker.js:315` | generic-api-key | `c09e…/32` | yanlis-alarm | Cloudflare Web Analytics beacon token: HTML'e gomulu herkese acik |
| Munder_Difflin | `blog/src/_includes/base.njk:70` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/404.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/about/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/agent-tools-today-2026-10-08/index.html:102` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/agent-tools-today-2026-10-03/index.html:102` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/agent-tools-today-2026-10-18/index.html:101` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/agent-tools-today-2026-10-07/index.html:102` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/agent-tools-today-2026-10-09/index.html:102` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/agent-tools-today-2026-10-04/index.html:102` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/agent-security-and-sandboxing/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/agent-tools-today-2026-10-22/index.html:101` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/ai-agent-glossary/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/agent-tools-today-2026-10-11/index.html:102` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/agent-tools-today-2026-10-19/index.html:101` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/agent-tools-today-2026-10-26/index.html:101` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/agent-tools-today-2026-10-17/index.html:101` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/agent-tools-today-2026-10-13/index.html:102` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/agent-tools-today-2026-10-23/index.html:101` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/agent-tools-today-2026-10-12/index.html:102` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/agent-tools-today-2026-10-21/index.html:101` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/agent-tools-today-2026-10-06/index.html:102` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/agents-ran-our-launch-week-analytics/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/agent-tools-today-2026-10-05/index.html:102` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/append-only-event-log-agents/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/agent-tools-today-2026-10-15/index.html:102` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/an-agent-redesigned-this-blog/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/aider-vs-claude-code/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/agent-tools-today-2026-10-16/index.html:102` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/agent-tools-today-2026-10-10/index.html:102` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/architecture-two-planes-one-renderer/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/agents-rule-of-two/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/ai-agent-office-github/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/ai-agent-use-cases-our-office/index.html:116` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/asd-ste100-prompting/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/best-ai-coding-agents/index.html:116` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/atomic-file-mailboxes-for-agents/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-code-skills/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-code-best-practices/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-code-max-plan-tips/index.html:116` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/best-claude-code-multi-agent-tools/index.html:116` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/build-your-personal-agi-on-your-computer/index.html:118` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-code-alternatives/index.html:113` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/black-october-php2shell/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-api-version-2026-10-21/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-duet-waitlist/index.html:113` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-duet-app/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-code-vs-antigravity/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-code-orchestration-guide/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/chatgpt-dots-alternatives/index.html:112` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/building-a-terminal-ui-xterm-node-pty/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-code-router/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/building-reliable-ai-agents/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/building-an-ai-office-floor/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-code-agent-teams/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-code-git-worktrees-vs-hive/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-code-subagents-vs-multi-agent-harness/index.html:116` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/command-center-guide/index.html:118` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-code-orchestration-tools-compared/index.html:101` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-code-multi-agent-setup-tutorial/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-code-routines/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/build-your-own-claude-duet/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-cowork-vs-claude-code/index.html:116` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-haiku-5-5/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-duet-alternatives/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-duet-for-developers/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-managed-agents-dynamic-workflows/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-code-projects/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-squad-alternative/index.html:101` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-code-vs-cursor/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/codex-alternatives/index.html:116` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-duet-vs-munder-difflin/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/can-claude-code-agents-talk-to-each-other/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-squad-vs-munder-difflin/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-code-automation-while-you-sleep/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/cline-alternatives/index.html:111` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/codex-cli-vs-claude-code/index.html:118` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-md-best-practices/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/codex-max-plan-tips/index.html:116` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/codex-vs-claude-code-usage-limits/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/compressing-agent-memory/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/codex-vs-cursor/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/cline-vs-munder-difflin/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/connect-slack-to-munder-difflin/index.html:116` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/claude-code-hooks-explained/index.html:116` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/crystal-claude-code-alternative/index.html:101` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/codex-computer-use/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/conductor-claude-code-alternative/index.html:101` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/context-engineering-for-ai-agents/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/codex-pricing/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/codex-vs-gemini-cli/index.html:111` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/crewai-autogen-vs-a-local-agent-harness/index.html:118` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/coordinating-ai-coding-agents/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/deploy-automated-pr-reviewer-agent/index.html:116` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/deepseek-v4-1-flash-1017/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/cursor-vs-cline/index.html:111` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/cursor-alternatives/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/debugging-multi-agent-systems/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/from-one-terminal-to-a-team/index.html:101` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/gemini-4-argon-pricing/index.html:116` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/cursor-pricing/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/do-more-with-less-model-routing/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/deploy-a-blog-writer-agent/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/gemini-4-argon-inside-google/index.html:113` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/generative-engine-optimization-techniques/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/gemini-4-argon/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/gpt-6-intelligent-ui/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/evaluating-ai-agent-reliability/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/how-much-does-claude-code-cost/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/gemini-cli-vs-claude-code/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/gemini-4-argon-vs-claude-opus-5-5/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/how-to-choose-a-multi-agent-tool/index.html:101` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/how-ai-answer-engines-choose-sources/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/herdr-alternatives/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/gpt-6-1-terra/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/file-based-coordination-vs-message-queues/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/grok-bot-pricing/index.html:112` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/does-the-june-2026-agent-sdk-change-affect-munder-difflin/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/how-to-add-a-github-copilot-cli-agent/index.html:118` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/how-agents-remember-semantic-memory/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/give-claude-code-long-term-memory/index.html:100` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/how-to-talk-to-your-orchestrator/index.html:118` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/how-to-run-multiple-claude-code-agents/index.html:101` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/hermes-agent-alternatives/index.html:112` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/how-to-connect-ollama-to-claude-code/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/how-to-hire-from-the-agent-gallery/index.html:118` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/how-ai-agents-verify-their-own-work/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/hire-manifest-untrusted-input/index.html:118` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/grok-bot-alternatives/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/how-to-use-the-built-in-monaco-ide/index.html:118` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/hermes-agent-vs-openclaw/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/how-the-god-orchestrator-works/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/github-copilot-cli-vs-claude-code-for-hive-work/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/how-to-install-codex-cli/index.html:116` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/how-to-use-gemini-4-argon/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/human-in-the-loop-approving-ai-agents/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/how-to-use-claude-code/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/how-to-use-claude-code-plan-mode/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/how-to-install-gemini-cli/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/is-claude-code-open-source/index.html:116` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/how-to-add-an-mcp-server-to-claude-code/index.html:116` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/keep-agent-semantic-memory-clean/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/human-in-the-loop-ai-agents/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/how-to-install-and-use-munder-difflin/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/launching-munder-difflin-v0-2-4/index.html:119` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/kilo-code-vs-cline/index.html:111` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/launching-munder-difflin-v0-2-0/index.html:116` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/is-claude-code-max-worth-it/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/is-ollama-good-for-coding/index.html:116` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/launching-munder-difflin-v0-2-8/index.html:119` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/launching-munder-difflin-v0-3-3/index.html:119` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/launching-munder-difflin-v0-3-5/index.html:119` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/launching-munder-difflin-v0-4-4/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/launching-munder-difflin-v0-3-2/index.html:119` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/launching-munder-difflin-v0-3-0/index.html:119` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/long-running-agents-the-2026-shift/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/litellm-1-107-0-compromise/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/loop-engineering-for-ai-agents/index.html:118` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/mcp-security-tool-poisoning/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/mistral-large-4/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/launching-munder-difflin-v0-4-6/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/markdown-first-agent-memory/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/multi-agent-orchestration-patterns/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/local-first-ai-agent-orchestration/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/local-first-vs-cloud-agent-sdks/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/launching-munder-difflin-v0-5-2/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/meta-muse-vs-grok-bot/index.html:111` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/munder-difflin-faq/index.html:125` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/mcp-and-skills-in-a-hive/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/manage-multiple-claude-code-sessions/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/orca-vs-munder-difflin/index.html:118` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/meta-muse-grok-bot-privacy/index.html:112` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/munder-difflin-v0-2-4-feature-walkthrough/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/omniagent-alternatives/index.html:116` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/munder-difflin-0-5-3/index.html:116` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/meta-muse-alternatives/index.html:111` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/observability-for-agent-fleets/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/muse-wonder/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/open-source-ai-agents/index.html:116` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/muse-code-vs-claude-code/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/one-prompt-automated-pr-review/index.html:101` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/number-five-on-product-hunt/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/opencode-vs-claude-code/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/opencode-alternatives/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/reflection-beam/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/munder-difflin-vs-chatgpt-dots/index.html:113` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/openclaw-alternatives/index.html:112` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/open-source-ai-tools-on-purpose/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/ade/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/prompt-caching-for-ai-agents/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/agent-design/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/indian-open-source-ai-projects-vs-big-tech/index.html:111` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/openai-text-watermarking/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/openai-decisions-api/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/rendering-many-live-terminals-performance/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/run-an-office-of-ai-agents/index.html:101` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/recovering-from-agent-failures/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/aeo/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/agentic-ai/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/opencode-2-0/index.html:116` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/review-agent-work-where-it-happens/index.html:118` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/pi-agent-alternatives/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/run-a-release-train-with-agents/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/overnight-ai-coding-realistic-expectations/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/qm-vs-munder-difflin/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/autogen/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/shareable-agent-roles/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/node-pty-electron-real-terminals/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/ai-search/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/run-ai-agent-hive-from-slack-setup/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/run-a-mixed-engine-office/index.html:118` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/ai-coding-agents/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/seven-releases-in-eight-days/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/run-munder-difflin-on-a-mac-mini/index.html:118` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/architecture/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/security-for-ai-coding-agents/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/autonomous/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/autonomy/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/cline/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/scheduling-autonomous-agent-missions/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/byok/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/brand/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/changelog/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/single-committer-git-pattern/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/cloud-agents/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/small-team-ai-agents-playbook/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/claude-api/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/coding-agents/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/semantic-memory-for-ai-agents/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/run-munder-difflin-on-open-models/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/community/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/code-review/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/command-center/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/command-injection/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/concurrency/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/computer-use/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/context/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/coordination/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/context-engineering/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/copilot/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/content/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/automation/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/devrel/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/discord/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/crewai/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/cursor/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/design/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/copilot-cli/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/ai-agents/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/desktop-apps/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/eleventy/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/geo/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/cli-agents/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/evaluation/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/error-handling/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/feedback/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/gemini-cli/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/debugging/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/electron/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/editors/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/git-worktrees/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/codex/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/game-dev/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/i18n/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/hitl/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/faq/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/event-log/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/git/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/github/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/hooks/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/glossary/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/ide-agents/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/industry/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/india/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/daily-brief/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/guardrails/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/github-copilot/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/harness-engineering/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/god/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/cost/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/ide/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/integrations/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/kanban/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/lm-studio/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/hive/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/getting-started/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/interoperability/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/human-in-the-loop/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/langgraph/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/mac-mini/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/markdown/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/launch/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/engines/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/long-running-agents/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/mistral/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/messaging/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/monaco-ide/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/munder-difflin/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/models/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/meta/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/node-pty/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/model-routing/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/openai/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/non-technical/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/opencode/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/comparisons/index.html:56` | generic-api-key | `phc_…/48` | test-verisi | test/fixture dizini |
| Munder_Difflin | `docs/blog/tags/ollama/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/observability/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/mempalace/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/mcp/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/memory/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/concepts/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/internals/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/pi/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/onboarding/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/orca/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/privacy/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/performance/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/postmortem/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/pixijs/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/prompt-caching/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/realtime/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/product/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/research/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/product-hunt/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/pro/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/protocols/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/python/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/orchestration/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/local-first/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/reddit/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/seo/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/setup/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/prompt-injection/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/ssrf/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/pricing/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/reliability/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/slack/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/talk-mode/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/subagents/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/telemetry/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/terminals/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/the-office/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/tmux/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/tooling-landscape/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/trust/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/windows/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/transcription/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/trends/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/guides/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/tools/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/security/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/tutorial/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/release/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/skills/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/usage-limits/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/webhooks/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/visualization/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/voice/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/xtermjs/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/use-cases/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/workflow/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/story/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/claude-code/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/topics/memory/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/the-newline-that-silenced-windows-agents/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/the-multi-agent-cost-playbook/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/the-lethal-trifecta-for-coding-agents/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tmux-and-scripts-vs-an-agent-harness/index.html:118` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/the-office-parody-behind-munder-difflin/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/vibe-kanban-alternative/index.html:101` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/the-hook-shim-pattern/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/visualizing-ai-agents-pixijs/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/the-clone-army-trap-mixed-swarm-vs-identical-agents/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/topics/story/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/trigger-ai-agents-from-slack/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/topics/use-cases/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/we-opened-a-discord/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/turn-feedback-into-a-backlog-with-agents/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/topics/news/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/what-are-claude-code-agents/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/open-source/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/topics/orchestration/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/the-spend-counter-that-went-back-to-zero/index.html:116` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/voice-as-a-control-plane-for-agent-fleets/index.html:118` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/what-is-a-multi-agent-harness/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/topics/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/what-is-claude-agent-sdk/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/what-is-claude-cowork/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/tags/multi-agent/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/what-is-codex/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/what-is-claude-duet/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/topics/internals/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/what-is-harness-engineering/index.html:118` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/what-is-aeo-for-dev-tools/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/trigger-ai-agents-from-github-webhook/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/what-is-an-agent-development-environment/index.html:118` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/what-is-an-mcp-server/index.html:116` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/what-reddit-told-us-about-munder-difflin/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/what-is-vibe-coding/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/what-is-roo-code/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/what-is-nanoclaw/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/what-is-chatgpt-dots/index.html:112` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/what-is-hermes-agent/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/what-is-pi-agent/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/what-is-opencode/index.html:116` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/whats-up-with-munder-difflin/index.html:118` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/why-we-built-munder-difflin/index.html:101` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/whats-new-in-agentic-ai-june-2026/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/what-is-zcode/index.html:116` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/why-cli-agents-are-powerful/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/why-does-claude-code-keep-asking-for-permission/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/what-is-gemini-spark/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/what-is-zeroclaw/index.html:115` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/why-local-first-matters-for-ai-agents/index.html:113` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/your-first-hour-with-munder-difflin/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/why-our-auto-update-never-ran/index.html:117` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/when-do-agents-need-an-agent-protocol/index.html:114` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/topics/concepts/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/blog/topics/comparisons/index.html:56` | generic-api-key | `phc_…/48` | test-verisi | test/fixture dizini |
| Munder_Difflin | `docs/blog/topics/guides/index.html:56` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/wall.html:466` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/pro/index.html:1005` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `docs/index.html:1717` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Munder_Difflin | `test/slack-timeout.test.cjs:52` | private-key | `----…/1865` | test-verisi | test/fixture dizini |
| Munder_Difflin | `test/repro/bug-17.repro.cjs:92` | generic-api-key | `gsk_…/23` | test-verisi | test/fixture dizini |
| Munder_Difflin | `test/repro/bug-12.repro.cjs:420` | generic-api-key | `whse…/26` | test-verisi | test/fixture dizini |
| Munder_Difflin | `test/repro/bug-12.repro.cjs:98` | private-key | `----…/1865` | test-verisi | test/fixture dizini |
| Munder_Difflin | `test/voice-messages.test.cjs:185` | slack-app-token | `xapp…/36` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Munder_Difflin | `test/voice-messages.test.cjs:185` | slack-app-token | `xapp…/36` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Munder_Difflin | `test/voice-messages.test.cjs:189` | generic-api-key | `AIza…/38` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Munder_Difflin | `test/voice-messages.test.cjs:193` | generic-api-key | `8f9a…/20` | test-verisi | test/fixture dizini |
| Munder_Difflin | `test/voice-messages.test.cjs:199` | generic-api-key | `abc1…/27` | test-verisi | test/fixture dizini |
| Munder_Difflin | `test/voice-messages.test.cjs:191` | stripe-access-token | `sk_l…/29` | test-verisi | test/fixture dizini |
| Munder_Difflin | `test/voice-messages.test.cjs:191` | stripe-access-token | `sk_l…/29` | test-verisi | test/fixture dizini |
| Munder_Difflin | `tools/landing-halloween/base.html:1471` | generic-api-key | `phc_…/48` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:279` | sentry-access-token | `8d3c…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:280` | sentry-access-token | `f321…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:281` | sentry-access-token | `e43c…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:282` | sentry-access-token | `081f…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:293` | sentry-access-token | `9c13…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:294` | sentry-access-token | `dfb6…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:295` | sentry-access-token | `4df4…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:296` | sentry-access-token | `c1d4…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:297` | sentry-access-token | `2b81…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:298` | sentry-access-token | `603b…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:369` | sentry-access-token | `ec55…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:370` | sentry-access-token | `cfbb…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:371` | sentry-access-token | `26f5…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:372` | sentry-access-token | `82aa…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:373` | sentry-access-token | `b56e…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:374` | sentry-access-token | `89b5…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:375` | sentry-access-token | `a9bd…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:376` | sentry-access-token | `a9b4…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:377` | sentry-access-token | `95dd…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:378` | sentry-access-token | `acbc…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:49` | generic-api-key | `6411…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:180` | generic-api-key | `ae71…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:181` | generic-api-key | `4917…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:182` | generic-api-key | `4027…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:183` | generic-api-key | `470e…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:184` | generic-api-key | `7f8c…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:185` | generic-api-key | `0bdf…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:186` | generic-api-key | `f269…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:249` | generic-api-key | `4d41…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:250` | generic-api-key | `a99c…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:251` | generic-api-key | `0af1…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:252` | generic-api-key | `7262…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:253` | generic-api-key | `9d7f…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:278` | generic-api-key | `593b…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:309` | generic-api-key | `d9ee…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:310` | generic-api-key | `63a9…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:311` | generic-api-key | `2987…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:312` | generic-api-key | `ba90…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:313` | generic-api-key | `f2d9…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:314` | generic-api-key | `7089…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:315` | generic-api-key | `01df…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:316` | generic-api-key | `a4a3…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:317` | generic-api-key | `25ed…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:359` | generic-api-key | `5754…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:360` | generic-api-key | `9b20…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:361` | generic-api-key | `e356…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:362` | generic-api-key | `53f7…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:363` | generic-api-key | `7738…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:364` | generic-api-key | `b9e8…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:365` | generic-api-key | `8cac…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:366` | generic-api-key | `64b6…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:367` | generic-api-key | `bdb6…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `benchmark/index/comparisons/compare-2026-10.json:368` | generic-api-key | `ab97…/64` | test-verisi | test/fixture dizini |
| OpenQodex | `packages/core/src/redact.test.ts:32` | private-key | `----…/199` | test-verisi | test/fixture dizini |
| OpenQodex | `packages/cli/test/review-report.test.ts:471` | private-key | `----…/199` | test-verisi | test/fixture dizini |
| OpenQodex | `packages/core/src/render/html.test.ts:54` | private-key | `----…/280` | test-verisi | test/fixture dizini |
| Orca | `.github/actions/cloud-sql-rollout-lease/storage-lease.test.mjs:129` | generic-api-key | `stab…/18` | test-verisi | test/fixture dizini |
| Orca | `.github/actions/cloud-sql-rollout-lease/storage-lease.test.mjs:174` | generic-api-key | `stab…/18` | test-verisi | test/fixture dizini |
| Orca | `.github/actions/cloud-sql-rollout-lease/storage-lease.test.mjs:213` | generic-api-key | `stab…/18` | test-verisi | test/fixture dizini |
| Orca | `.github/actions/cloud-sql-rollout-lease/storage-lease.test.mjs:251` | generic-api-key | `stab…/18` | test-verisi | test/fixture dizini |
| Orca | `.github/actions/cloud-sql-rollout-lease/storage-lease.test.mjs:293` | generic-api-key | `stab…/18` | test-verisi | test/fixture dizini |
| Orca | `cloud/apps/relay/src/relay-upgrade-malformed-uri.blackbox.test.ts:25` | generic-api-key | `dGhl…/24` | test-verisi | test/fixture dizini |
| Orca | `cloud/apps/relay/src/relay-first-frame-close.blackbox.test.ts:79` | generic-api-key | `dGhl…/24` | test-verisi | test/fixture dizini |
| Orca | `cloud/apps/relay/src/relay.blackbox.test.ts:25` | generic-api-key | `test…/42` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Orca | `config/patches/@xterm__addon-webgl@0.20.0-beta.300.patch:6` | generic-api-key | `e.Tw…/16` | yanlis-alarm | xterm kucultulmus kodu yamasi (degisken atamasi) |
| Orca | `config/scripts/raw-markdown-comment-scan-benchmark.mjs:36` | generic-api-key | `0123…/32` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Orca | `config/patches/@xterm__addon-webgl@0.20.0-beta.300.patch:7` | generic-api-key | `e.Tw…/16` | yanlis-alarm | xterm kucultulmus kodu yamasi (degisken atamasi) |
| Orca | `config/scripts/pty-transcript-secret-scan.test.mjs:25` | generic-api-key | `AIza…/38` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Orca | `config/scripts/pty-transcript-secret-scan.test.mjs:24` | jwt | `eyJh…/61` | test-verisi | test/fixture dizini |
| Orca | `config/patches/@xterm__xterm@6.1.0-beta.304.patch:6` | generic-api-key | `t.Tw…/16` | yanlis-alarm | xterm kucultulmus kodu yamasi (degisken atamasi) |
| Orca | `config/patches/@xterm__xterm@6.1.0-beta.304.patch:7` | generic-api-key | `t.Tw…/16` | yanlis-alarm | xterm kucultulmus kodu yamasi (degisken atamasi) |
| Orca | `config/scripts/windows-pty-table-stress-observer.test.mjs:176` | generic-api-key | `2345…/21` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Orca | `docs/bug-reproductions/usage-scan-append/validation.json:17` | generic-api-key | `e96c…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/native-chat-tool-pairing/rendered-validation.json:20` | generic-api-key | `87c7…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/native-chat-tool-pairing/rendered-validation.json:29` | generic-api-key | `6e3e…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-resource-evidence-receipt.json:3` | sourcegraph-access-token | `bcfb…/40` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-resource-evidence-receipt.json:69` | sourcegraph-access-token | `51e7…/40` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-resource-evidence-receipt.json:70` | sourcegraph-access-token | `8467…/40` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-resource-evidence-receipt.json:71` | sourcegraph-access-token | `b44a…/40` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-resource-evidence-receipt.json:145` | sourcegraph-access-token | `8467…/40` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-resource-evidence-receipt.json:152` | sourcegraph-access-token | `8467…/40` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-resource-evidence-receipt.json:159` | sourcegraph-access-token | `b44a…/40` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-resource-evidence-receipt.json:166` | sourcegraph-access-token | `b44a…/40` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-resource-evidence-receipt.json:187` | sourcegraph-access-token | `51e7…/40` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-resource-evidence-receipt.json:20` | generic-api-key | `f138…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-resource-evidence-receipt.json:21` | generic-api-key | `87c7…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-resource-evidence-receipt.json:44` | generic-api-key | `6e3e…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/codex-parser-memory.json:43` | generic-api-key | `fb3e…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/codex-parser-memory.json:65` | generic-api-key | `fb3e…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/codex-parser-memory-final.json:43` | generic-api-key | `fb3e…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/codex-parser-memory-final.json:65` | generic-api-key | `fb3e…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/native-chat-tool-pairing/mobile-rendered-validation.json:114` | generic-api-key | `549c…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/native-chat-tool-pairing/mobile-rendered-validation.json:137` | generic-api-key | `0675…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/native-chat-tool-pairing/mobile-rendered-validation.json:148` | generic-api-key | `09eb…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/native-chat-tool-pairing/mobile-rendered-validation.json:186` | generic-api-key | `ef55…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-source-compression-100k.json:181` | generic-api-key | `7a66…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-source-compression-100k.json:261` | generic-api-key | `7a66…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-source-compression-100k.json:427` | generic-api-key | `7a66…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-persistence-cost-final-16k.json:141` | generic-api-key | `7a66…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-persistence-cost-final-16k.json:220` | generic-api-key | `7a66…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-persistence-cost-final-16k.json:383` | generic-api-key | `7a66…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-readiness-cost-final.json:155` | generic-api-key | `7a66…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-readiness-cost-final.json:235` | generic-api-key | `7a66…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-readiness-cost-final.json:401` | generic-api-key | `7a66…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-source-compression-varied-100k.json:181` | generic-api-key | `7a66…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-source-compression-varied-100k.json:262` | generic-api-key | `7a66…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-source-compression-varied-100k.json:427` | generic-api-key | `7a66…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-source-compression-16k.json:181` | generic-api-key | `7a66…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-source-compression-16k.json:260` | generic-api-key | `7a66…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-source-compression-16k.json:429` | generic-api-key | `7a66…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-persistence-cost-final-100k.json:142` | generic-api-key | `7a66…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-persistence-cost-final-100k.json:220` | generic-api-key | `7a66…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/usage-scan-append/claude-persistence-cost-final-100k.json:384` | generic-api-key | `7a66…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `mobile/google-services.json:23` | gcp-api-key | `AIza…/39` | yanlis-alarm | Firebase mobil API anahtari (AIza): uygulamaya gomulu herkese acik tasarim |
| Orca | `docs/bug-reproductions/native-chat-tool-pairing/full-fold-benchmark.json:24` | generic-api-key | `09eb…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/native-chat-tool-pairing/full-fold-benchmark.json:81` | generic-api-key | `09eb…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `docs/bug-reproductions/native-chat-tool-pairing/full-fold-benchmark.json:141` | generic-api-key | `09eb…/64` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| Orca | `mobile/rpc-foundation/goldens/matrix-pairing.pre-profile-relay-status.json:68` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.credential-rotation-pairing.getendpoints-2.json:541` | generic-api-key | `PF6B…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.credential-rotation-pairing.getendpoints-2.json:628` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-pairing.pre-profile-pairing.provisionrelay-1.json:28` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-pairing.pre-profile-pairing.provisionrelay-1.json:69` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-pairing.pre-profile-pairing.provisionrelay-1.json:120` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-pairing.pre-profile-pairing.provisionrelay-1.json:168` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-pairing.pre-profile-pairing.provisionrelay-1.json:201` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-pairing.pre-profile-pairing.provisionrelay-1.json:269` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-pairing.pre-profile-pairing.provisionrelay-1.json:340` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-pairing.pre-profile-pairing.provisionrelay-1.json:381` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-pairing.pre-profile-pairing.provisionrelay-1.json:414` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-pairing.pre-profile-pairing.provisionrelay-1.json:484` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-pairing.pre-profile-pairing.provisionrelay-1.json:680` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.direct-upgrade-pairing.getendpoints-1.json:216` | generic-api-key | `7ehR…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.direct-upgrade-pairing.getendpoints-2.json:151` | generic-api-key | `7ehR…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-pairing.pre-profile-pairing.getendpoints-1.json:137` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.credential-rotation-pairing.getendpoints-1.json:575` | generic-api-key | `PF6B…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.credential-rotation-pairing.getendpoints-1.json:628` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.direct-upgrade-pairing.provisionrelay-1.json:18` | generic-api-key | `7ehR…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.direct-upgrade-pairing.provisionrelay-1.json:68` | generic-api-key | `7ehR…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.direct-upgrade-pairing.provisionrelay-1.json:186` | generic-api-key | `7ehR…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.direct-upgrade-pairing.provisionrelay-1.json:239` | generic-api-key | `7ehR…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.direct-upgrade-pairing.provisionrelay-1.json:334` | generic-api-key | `7ehR…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.direct-upgrade-pairing.provisionrelay-1.json:367` | generic-api-key | `7ehR…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.direct-upgrade-pairing.provisionrelay-1.json:413` | generic-api-key | `7ehR…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.direct-upgrade-pairing.provisionrelay-1.json:474` | generic-api-key | `7ehR…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.direct-upgrade-pairing.provisionrelay-1.json:524` | generic-api-key | `7ehR…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.direct-upgrade-pairing.provisionrelay-1.json:559` | generic-api-key | `7ehR…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.direct-upgrade-pairing.provisionrelay-1.json:624` | generic-api-key | `7ehR…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-pairing.pre-profile-direct-status.json:33` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.credential-rotation-pairing.provisionrelay-1.json:34` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.credential-rotation-pairing.provisionrelay-1.json:71` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.credential-rotation-pairing.provisionrelay-1.json:105` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.credential-rotation-pairing.provisionrelay-1.json:148` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.credential-rotation-pairing.provisionrelay-1.json:185` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.credential-rotation-pairing.provisionrelay-1.json:229` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.credential-rotation-pairing.provisionrelay-1.json:270` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.credential-rotation-pairing.provisionrelay-1.json:306` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.credential-rotation-pairing.provisionrelay-1.json:374` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.credential-rotation-pairing.provisionrelay-1.json:436` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.credential-rotation-pairing.provisionrelay-1.json:595` | generic-api-key | `PF6B…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/matrix-relay.credential-rotation-pairing.provisionrelay-1.json:648` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/patches/@xterm__addon-webgl@0.20.0-beta.300.patch:6` | generic-api-key | `e.Tw…/16` | yanlis-alarm | xterm kucultulmus kodu yamasi (degisken atamasi) |
| Orca | `mobile/patches/@xterm__addon-webgl@0.20.0-beta.300.patch:7` | generic-api-key | `e.Tw…/16` | yanlis-alarm | xterm kucultulmus kodu yamasi (degisken atamasi) |
| Orca | `mobile/rpc-foundation/goldens/relay-direct-upgrade-commits.json:108` | generic-api-key | `7ehR…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/relay-pairing-recovery-invite-authorizes.json:75` | generic-api-key | `7ehR…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/relay-rotation-installs-and-commits.json:154` | generic-api-key | `PF6B…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/relay-rotation-installs-and-commits.json:197` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/pairing-pre-profile-direct-wins-and-provisions.json:33` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/goldens/pairing-pre-profile-provision-unsupported-saves-direct-host.json:28` | generic-api-key | `yrnY…/43` | test-verisi | test/fixture dizini |
| Orca | `mobile/rpc-foundation/pilot-scenarios.json:10961` | generic-api-key | `yrnY…/43` | test-verisi | RPC senaryo fixture'i (token hash) |
| Orca | `mobile/rpc-foundation/pilot-scenarios.json:11107` | generic-api-key | `7ehR…/43` | test-verisi | RPC senaryo fixture'i (token hash) |
| Orca | `mobile/rpc-foundation/pilot-scenarios.json:11304` | generic-api-key | `7ehR…/43` | test-verisi | RPC senaryo fixture'i (token hash) |
| Orca | `mobile/rpc-foundation/pilot-scenarios.json:11410` | generic-api-key | `yrnY…/43` | test-verisi | RPC senaryo fixture'i (token hash) |
| Orca | `mobile/rpc-foundation/pilot-scenarios.json:11516` | generic-api-key | `yrnY…/43` | test-verisi | RPC senaryo fixture'i (token hash) |
| Orca | `mobile/src/transport/mobile-paired-e2ee-primitives.ts:36` | generic-api-key | `deri…/29` | yanlis-alarm | fonksiyon adi eslesmesi (deriveV2KeySchedule) |
| Orca | `src/main/browser/browser-local-https-test-certificate.ts:2` | private-key | `----…/1703` | test-verisi | yerel HTTPS test sertifikasi anahtari (dosya adi test) |
| Orca | `src/main/browser/extensions/browser-extension-crx.ts:12` | generic-api-key | `61f7…/64` | yanlis-alarm | Chrome Web Store yayinci anahtar OZETI (hash), sir degil |
| Orca | `src/main/claude-usage/store.test.ts:294` | generic-api-key | `clau…/24` | test-verisi | test/fixture dizini |
| Orca | `src/main/claude-usage/store.test.ts:324` | generic-api-key | `clau…/24` | test-verisi | test/fixture dizini |
| Orca | `src/main/claude-usage/store.test.ts:372` | generic-api-key | `clau…/24` | test-verisi | test/fixture dizini |
| Orca | `src/main/claude-usage/store.test.ts:499` | generic-api-key | `clau…/24` | test-verisi | test/fixture dizini |
| Orca | `src/main/codex-accounts/managed-codex-auth-readiness.test.ts:14` | generic-api-key | `e30.…/46` | test-verisi | test/fixture dizini |
| Orca | `src/main/ipc/pty/pty-ipc-test-constants.ts:43` | generic-api-key | `e30.…/46` | test-verisi | test sabiti (e30. = '{}' bos JWT basligi) |
| Orca | `src/main/observability/redactor.test.ts:16` | jwt | `eyJh…/127` | test-verisi | test/fixture dizini |
| Orca | `src/main/observability/redactor.test.ts:18` | private-key | `----…/106` | test-verisi | test/fixture dizini |
| Orca | `src/main/persistence/loading-store/profile-state-direct-flush.test.ts:78` | generic-api-key | `158a…/36` | test-verisi | test/fixture dizini |
| Orca | `src/main/plugins/catalog/plugin-update-approval.test.ts:48` | generic-api-key | `CmdO…/17` | test-verisi | test/fixture dizini |
| Orca | `src/main/plugins/catalog/plugin-update-approval.test.ts:159` | generic-api-key | `CmdO…/17` | test-verisi | test/fixture dizini |
| Orca | `src/main/rate-limits/minimax/minimax-request-context.test.ts:473` | generic-api-key | `sk-t…/18` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Orca | `src/main/rate-limits/minimax/minimax-fetcher.test.ts:507` | generic-api-key | `sk-t…/18` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Orca | `src/main/runtime/orchestration/orchestration-legacy-storage-db.test.ts:708` | generic-api-key | `ask_…/15` | test-verisi | test/fixture dizini |
| Orca | `src/main/runtime/orchestration/orchestration-legacy-storage-db.test.ts:717` | generic-api-key | `ask_…/15` | test-verisi | test/fixture dizini |
| Orca | `src/main/runtime/orchestration/orchestration-legacy-storage-db.test.ts:725` | generic-api-key | `repl…/18` | test-verisi | test/fixture dizini |
| Orca | `src/main/runtime/orchestration/orchestration-legacy-storage-db.test.ts:755` | generic-api-key | `repl…/18` | test-verisi | test/fixture dizini |
| Orca | `src/main/runtime/orchestration-message-delivery-identity.test.ts:30` | generic-api-key | `sta-…/15` | test-verisi | test/fixture dizini |
| Orca | `src/main/runtime/rpc/methods/agent-launch-session-reservation.test.ts:143` | generic-api-key | `clau…/43` | test-verisi | test/fixture dizini |
| Orca | `src/main/runtime/rpc/methods/computer.test.ts:206` | generic-api-key | `CmdO…/15` | test-verisi | test/fixture dizini |
| Orca | `src/main/ssh/config/ssh-known-hosts.test.ts:369` | generic-api-key | `AAAA…/68` | test-verisi | test/fixture dizini |
| Orca | `src/main/ssh/config/ssh-known-hosts.test.ts:370` | generic-api-key | `AAAA…/68` | test-verisi | test/fixture dizini |
| Orca | `src/main/ssh/orcad-windows-stdio-bridge-test-cell.ts:43` | generic-api-key | `dGhl…/24` | yanlis-alarm | RFC 6455 ornek Sec-WebSocket-Key (dGhl.. 'the sample nonce') |
| Orca | `src/main/ssh/ssh-remote-windows-command-line-limit.test.ts:26` | generic-api-key | `123e…/36` | test-verisi | test/fixture dizini |
| Orca | `src/main/ssh/ssh-remote-windows-command-line-limit.test.ts:29` | generic-api-key | `123e…/36` | test-verisi | test/fixture dizini |
| Orca | `src/renderer/src/components/editor/raw-markdown-comment-scan.test.ts:5` | generic-api-key | `0123…/32` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Orca | `src/renderer/src/components/editor/raw-markdown-html.details-fences.test.ts:8` | generic-api-key | `0123…/32` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Orca | `src/renderer/src/components/editor/rich-markdown-link-shortcut.test.ts:11` | generic-api-key | `0123…/32` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Orca | `src/renderer/src/components/editor/rich-markdown-html-superscript-link.test.ts:38` | generic-api-key | `0123…/32` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Orca | `src/renderer/src/components/native-chat/use-native-chat-toggle-shortcut.keybindings.test.ts:129` | generic-api-key | `Doub…/13` | test-verisi | test/fixture dizini |
| Orca | `src/renderer/src/web/web-paired-e2ee-primitives.ts:28` | generic-api-key | `deri…/29` | yanlis-alarm | fonksiyon adi eslesmesi (deriveV2KeySchedule) |
| Orca | `src/shared/appimage-cache-identity.ts:10` | generic-api-key | `gene…/19` | yanlis-alarm | surum dizgesi (NAMESPACE_KEY_VERSION) |
| Orca | `src/shared/crash-reporting.test.ts:414` | private-key | `----…/140` | test-verisi | test/fixture dizini |
| Orca | `src/shared/mobile-e2ee-legacy-fixtures.ts:6` | generic-api-key | `18a9…/64` | test-verisi | E2EE test vektoru fixture'i |
| Orca | `src/shared/mobile-e2ee-v2-fixtures.ts:44` | generic-api-key | `df17…/64` | test-verisi | E2EE test vektoru fixture'i |
| Orca | `src/shared/mobile-e2ee-v2-fixtures.ts:45` | generic-api-key | `7136…/64` | test-verisi | E2EE test vektoru fixture'i |
| Orca | `src/shared/pairing.test.ts:14` | generic-api-key | `abcd…/48` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Orca | `src/shared/plugins/approval/plugin-update-access-growth.test.ts:37` | generic-api-key | `CmdO…/17` | test-verisi | test/fixture dizini |
| Orca | `src/shared/plugins/approval/plugin-update-access-growth.test.ts:40` | generic-api-key | `CmdO…/17` | test-verisi | test/fixture dizini |
| Orca | `src/shared/plugins/approval/plugin-update-access-growth.test.ts:41` | generic-api-key | `CmdO…/17` | test-verisi | test/fixture dizini |
| Orca | `src/shared/secret-at-rest-protection.test.ts:6` | generic-api-key | `sk-a…/19` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Orca | `tests/e2e/terminal-long-table-fixtures.ts:230` | generic-api-key | `z6Mk…/114` | test-verisi | test/fixture dizini |
| Orca | `tests/e2e/terminal-long-table-scroll-restore.spec.ts:475` | generic-api-key | `z6Mk…/42` | test-verisi | test/fixture dizini |
| PhotoCraft | `crates/automation/src/security.rs:506` | generic-api-key | `0123…/16` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| Prime_Agent | `crates/pa-tui/tests/golden/preview.json:50` | curl-auth-header | `abc1…/12` | test-verisi | test/fixture dizini |
| Prime_Agent | `prime-agent-runtime/test/test_bash.py:711` | generic-api-key | `0123…/16` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| prompts.chat | `src/app/api/cron/reset-credits/route.ts:13` | curl-auth-header | `YOUR…/16` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| prompts.chat | `src/app/docs/api/page.tsx:866` | curl-auth-header | `pcha…/23` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| prompts.chat | `PROMPTS.md:55260` | linkedin-client-id | `Reco…/14` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| prompts.chat | `PROMPTS.md:55262` | linkedin-client-id | `Reco…/14` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| prompts.chat | `prompts.csv:42430` | linkedin-client-id | `Reco…/14` | ornek-yer-tutucu | istem metnindeki ornek ('demo secret dev-secret' JWT / 'LinkedIn: Recommendation' basligi) |
| prompts.chat | `prompts.csv:147733` | stripe-access-token | `sk_l…/18` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| prompts.chat | `PROMPTS.md:178267` | stripe-access-token | `sk_l…/18` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| prompts.chat | `PROMPTS.md:182929` | jwt | `eyJh…/347` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| prompts.chat | `PROMPTS.md:182935` | jwt | `eyJh…/152` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| prompts.chat | `PROMPTS.md:182941` | jwt | `eyJh…/303` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| prompts.chat | `prompts.csv:151674` | jwt | `eyJh…/347` | ornek-yer-tutucu | istem metnindeki ornek ('demo secret dev-secret' JWT / 'LinkedIn: Recommendation' basligi) |
| prompts.chat | `prompts.csv:151680` | jwt | `eyJh…/152` | ornek-yer-tutucu | istem metnindeki ornek ('demo secret dev-secret' JWT / 'LinkedIn: Recommendation' basligi) |
| prompts.chat | `prompts.csv:151686` | jwt | `eyJh…/303` | ornek-yer-tutucu | istem metnindeki ornek ('demo secret dev-secret' JWT / 'LinkedIn: Recommendation' basligi) |
| prompts.chat | `PROMPTS.md:206582` | stripe-access-token | `sk_l…/20` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| prompts.chat | `PROMPTS.md:206606` | stripe-access-token | `sk_l…/20` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| prompts.chat | `prompts.csv:173119` | stripe-access-token | `sk_l…/20` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| prompts.chat | `prompts.csv:173143` | stripe-access-token | `sk_l…/20` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| ReelMimic | `.claude/skills/media-use/scripts/lib/telemetry.mjs:10` | generic-api-key | `phc_…/47` | yanlis-alarm | PostHog phc_ proje anahtari: herkese acik |
| Reicon | `scripts/seo/ping.mjs:13` | generic-api-key | `e44e…/32` | yanlis-alarm | IndexNow anahtari: tasarim geregi sitede /<key>.txt olarak yayimlanir |
| tcl-lsp | `docs/kcs/codes/kcs-diagnostic-t103-taint-regexp-pattern.md:93` | generic-api-key | `tclL…/23` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| tcl-lsp | `docs/kcs/codes/kcs-diagnostic-t106-taint-double-encoding.md:89` | generic-api-key | `tclL…/23` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| tcl-lsp | `rust/bigip-report-gen/python/tests/test_certs.py:97` | generic-api-key | `BHDL…/24` | test-verisi | test/fixture dizini |
| tcl-lsp | `rust/tcl-bigip/src/redact.rs:1886` | private-key | `----…/452` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| tcl-lsp | `rust/tcl-f5mku/README.md:15` | generic-api-key | `BHDL…/24` | ornek-yer-tutucu | dokuman/ornek dosyasi |
| tcl-lsp | `rust/tcl-f5mku/src/lib.rs:40` | generic-api-key | `BHDL…/24` | ornek-yer-tutucu | doc-test ornegi (//! satiri, sonucu 'KEY45678') |
| tcl-lsp | `rust/tcl-sslictcl/src/key.rs:150` | private-key | `----…/1059` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| TradingAgents | `tests/test_alpha_vantage_hardening.py:165` | generic-api-key | `AVKE…/18` | ornek-yer-tutucu | deger yer tutucu kalibinda |
| TradingAgents | `tests/test_fred.py:261` | generic-api-key | `abcd…/32` | ornek-yer-tutucu | deger yer tutucu kalibinda |
