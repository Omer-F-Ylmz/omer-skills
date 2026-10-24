# REA-AGIR-1 — KISMEN (kök neden kanıtlı, parçalı mod çalışıyor; 4 hedef + kalite kapısı koşulmadı)

## Kök neden (ölçüldü, excalidraw.com)
- Aşama ayrımı: yakalama+kaynak tutma (`inspect_web_page include_script_sources`) 3.6 sn / 384 MB RSS / 6 MB çıktı → sorun YAKALAMA değil ANALİZ. `fetch_source_maps` zaten varsayılan false (webBundleAnalysis.js:7), kaynak haritası suçsuz.
- Betik başına taze süreç (2 GB tavan): 9/10 betik ≤334 MB, ≤1.1 sn (en büyüğü 192 708 düğüm). Tek `assets/index-*.js` (2.2 MB, minify) >2 GB'a çıkıp OOM (exit 134) → patoloji tek betikte, `analyzeScript` içindeki anlamsal evre (webBundleAnalyzerInspection.js:13-37: bağlama/alıcı dizinleme, ambient write, üye mutasyon) boyuta göre süperlineer. Normal modda tüm betikler tek süreçte biriktiği için ~40 MB/sn büyüme + 2 GB'ta tıkanma (önceki tur ölçümü).
- Hangi anlamsal alt evre: kanıtlanmadı. 8 GB/340 sn stderr'siz ölüm: araştırılmadı.
- Seçenek (adım 2): analyze_web_bundle'da betik filtresi/akış yok; `export_web_scripts` capture→diske var (manifest, 10 dosya 2.8 MB) ama analiz aracı canlı sayfa ister → yerel dosyadan analiz için REA'nın `analyzeScript`'i doğrudan çağrılıyor.

## Parçalı mod (commit)
- tools/rea_parcali.py: yakala (rea_mcp_cagri, tavanlı) → betik başına JSON → `rea_parcali_isci.mjs script` (taze node, 2048 MB, RAM ≥%85 bekle, ≥%88 öldür) → tavanı aşan betik wakaru@1.14.0 ile modüllere açılıp modül başına ayrı süreç → `birlestir` (REA'nın buildWebBundleAnalysis'i, accumulator birleştirme) → ozet/olcum/analiz.json diske.
- tools/rea_parcali_isci.mjs, rea_mcp_cagri.py, rea_heap_ornek.cjs.

## excalidraw sonuç (tek koşu, 3 sn'lik yakalama = 10 betik, 2.8 MB)
| | normal | parçalı |
|---|---|---|
| sonuç | OOM (52-129 sn) | tamamlandı, 221 sn (wakaru 33 sn + 155 süreç), sistem RAM tepe %74.2, işçi tepe 2.2 GB (OOM'a giden süreç) |
| kapsama | 0 | 9/10 betik + index-*.js'in 154/155 modülü = 1 modül analiz edilemedi (%99.4 modül; "%100" hedefi TUTMADI) |
Not: yakalama 3 sn; 20 sn'lik canlı yakalama daha çok parça getirir, koşulmadı. Modül dosyalarındaki satır/sütun wakaru çıktısına göre (özgün bundle değil); bulgular üst betik anahtarına yazıldı.

## YAPILMADI (neden: araç çağrı tavanı 45, bütçe)
- Kalite kapısı (HN + orta SPA'da normal↔parçalı ≥%98 örtüşme): koşulmadı. Birleştirme mantığı seen-kümelerini birleştiriyor ama örtüşme ölçülmedi.
- figma / notion / Electron asar hedefleri; tepe-RAM tablosu yalnız excalidraw.
- Kalan 1 modülü bulma/yeniden bölme; heavy-targets.md taslağı ve skill önerisi.

## Devam
1. `python tools/rea_parcali.py <url> <dizin>` HN + orta SPA'da; normal analyze_web_bundle ile edge/library/bundle örtüşmesi. 2. Başarısız modülü wakaru çıktısından bul, `birlestir`e dahil et ya da alt bölme. 3. figma/notion/asar. 4. references/heavy-targets.md (CC + claude.ai).
Maliyet: bu tur ~$0.62 + önceki ~$0.66 = tavan $0.80 aşıldı (ölçüm koşuları, wakaru 155 süreç).
