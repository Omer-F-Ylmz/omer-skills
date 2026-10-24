# REA-AGIR-1 — KISMEN (kök neden kısmen kanıtlı; parçalı mod YAZILMADI)

Durum: 4 hedef tablosu, kalite kapısı, heavy-targets.md yapılmadı (neden aşağıda). Tavan $0.80'e 45 çağrı sınırıyla yaklaşıldı (~$0.66).

## Kök neden (ölçüldü, excalidraw.com, REA 1 süreç, Chrome headless CDP 9333)
- Yığın CANLI veri olarak doğrusal büyüyor, çöp değil: 5.9 sn 261 MB → 10.6 sn 415 MB → 16.3 sn 741 MB → 24.7 sn 1012 MB (~40 MB/sn); 2 GB tavanda Mark-Compact 2038→2031 MB etkisiz → "Ineffective mark-compacts" (exc-snap.json.gc.txt, 357 GC satırı).
- Ana iş parçacığı OOM'a dek ~100+ sn inspector isteğine yanıt vermiyor (işçi parçacığından HeapProfiler.getSamplingProfile 700 MB RSS eşiğinde istendi, yanıt hiç gelmedi, ragir/exc-heap.json.log "esik" var "cevap" yok) → tek uzun eşzamanlı/yerel aşama. Fatal-error raporunda JS yığını yok ("No stack").
- Boru hattı (dosya:satır): CdpBrowserProvider.js:87-99 analyzeBundle → #capture; CdpPageCaptureScripts.js:15,50 tüm script kaynakları `Debugger.getScriptSource` ile `drafts` dizisinde bellekte tutuluyor → WebSourceMapFetcher.js (çıktı tavanı 64 MiB, kaynak haritaları) → domain/webBundleAnalyzer.js analyzeCapturedWebBundle → webBundleAnalyzerInspection.js:14 her script için `parseJavaScriptSource` (@babel/types AST) + semantik gezinti (satır 4-7).
- KANITLANMADI: büyümenin hangi aşamada olduğu (kaynak tutma / source map / Babel AST). Heap snapshot 1 GB ve 450 MB tavanda RSS 4.2/1.8 GB'a çıkıp RAM bekçisini (%88) tetikledi, dosya boş kaldı. Sonraki adım: snapshot'ı 250 MB tavanda al ya da aşamaları `fetch_source_maps:false` / `include_script_sources` ile tek tek aç-kapa ölç.
- Seçenekler (adım 2): analyze_web_bundle girdisi yalnız include_* bayrakları, allowed_origins, observation_ms, fetch_source_maps; script sayısı/boyut filtresi, akış kipi YOK. `fetch_source_maps:false` excalidraw'da denenmedi.
- 8 GB / 340 sn stderr'siz ölüm: ARAŞTIRILMADI.

## Ortam kısıtı (bulgu)
- Bu makinede taban RAM %75-82 (diğer claude.exe oturumları ~4 GB + python 2 GB); %85 tavanı REA+Chrome için ~1-2 GB pay bırakıyor. Parçalı mod tasarımı alt süreç başına ≤~800 MB hedeflemeli.
- Excalidraw koşuları: tepe REA RSS 1.3-2.3 GB, sistem tepe %85.9-88.1; iki koşu kendi %88 bekçimce durduruldu.

## Hedef tablosu
| hedef | normal mod | parçalı mod |
|---|---|---|
| news.ycombinator.com | 1.0 sn, 391 MB, 10 KB çıktı (taban, ragir/hn-normal.cevap.json) | yapılmadı |
| excalidraw.com | OOM (2048: 52 sn/2.27 GB; 1200: 129 sn/exit 134) | yapılmadı |
| figma / notion / Electron asar | koşulmadı | yapılmadı |
Kalite kapısı (%98 örtüşme): ÇALIŞTIRILMADI.

## Üretilenler (commit)
- tools/rea_mcp_cagri.py — REA MCP'yi ayrı node'da (bellek bayraklı) koşar, headless Chrome CDP açar, tepe RSS/süre ölçer, %88'de öldürür.
- tools/rea_heap_ornek.cjs — işçi parçacıklı örnekleme yığın profili (ana iş parçacığı kilitliyken çalışmadı; bilinen sınır).

## Devam: sıra
1. `fetch_source_maps:false` + excalidraw (aşama ayrımı), 2. 250 MB tavanda snapshot, 3. tools/rea_parcali.py: export_web_scripts girdisi (include_script_sources) → bundle başına taze süreç `analyze_javascript_application`, wakaru@1.14.0 unpack.
Ders: Heredoc ters eğik çizgiyi yutar (.cjs bozuldu) → Write ile yaz; AST/kaynak tutan REA'da JS yığını OOM raporunda yok, aşamaları bayrakla ayır.
