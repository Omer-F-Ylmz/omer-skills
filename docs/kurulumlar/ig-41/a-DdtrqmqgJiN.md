# DdtrqmqgJiN · charliehills · görsel gönderi (karusel) · https://www.instagram.com/p/DdtrqmqgJiN/

## Özet
TypeSafe AI'nin karar modeli Jev üzerine kurulmuş 20 topluluk projesi: ajanlar, bağlam/hafıza araçları, geliştirici akışı, skill'ler ve eğlence demoları. Hepsi TYPESAFE_API_KEY ister; bizde jev MCP + typesafe plugin + jev CLI kurulu.

## Kalemler
| ad | tür | link | karar | ölçütler (bakım · çift · izin · context) | gerekçe |
|---|---|---|---|---|---|
| jev-ultrafast | tarayıcı ajanı | https://github.com/browser-use/jev-ultrafast | UYARLA | ★22757 push:2026-09-30 arşiv:h · önceki-karar:karar.tsv:REF · tarayıcı (oturumlu Chrome), ağ, hesap · - | alınacak: numaralı eleman tablosu + tek kararda işlem/hedef + tazelik/örtüşme denetimi → otm-tarayici-otomasyon |
| agent-desktop | masaüstü otomasyon CLI | https://github.com/lahfir/agent-desktop | UYARLA | ★1788 push:2026-10-06 arşiv:h · yok · shell, erişilebilirlik izni · - | yalnız macOS; alınacak: yerel pencere = erişilebilirlik yolu, web = CDP ayrımı → Windows UIA notu |
| jev-drone | demo | https://github.com/RomanSlack/jev-drone | ÖĞREN | ★270 push:2026-09-24 arşiv:h · yok · shell, hesap · - | küçük karar modeli kontrol döngüsünde ucuz politika olabilir |
| Blink | kod arama | https://github.com/ellipsis-dev/blink | RED | ★100 push:2026-09-16 arşiv:h · kısmen:graphify, jev ilgili · shell, hesap · - | lisans yok; bizde graphify + jev ilgili aynı işi görüyor |
| fast-jev-compaction | CC plugin | https://github.com/tamaratran/fast-jev-compaction | KUR | ★7605 push:2026-09-18 arşiv:h · kısmen:headroom, context-mode · ağ, hesap · kanca, bağlam yükü düşük | özet yerine bayat araç sonucunu silme bizde yok; Jev anahtarı var; 32k istek sınırı → parçalı |
| Winnow | CC bağlam süzgeci | https://github.com/GhalebDweikat/winnow | UYARLA | ★109 push:2026-10-06 arşiv:h · kısmen:headroom, context-mode · ağ, hesap · kanca (her araç sonucu) | alınacak: blok başına alaka kararı + geri çağrılabilir stub → headroom/jev log; slayttaki winnow-rs yanlış repo |
| neo4jev | demo | https://github.com/jexp/neo4jev | ÖĞREN | ★173 push:2026-09-18 arşiv:h · kısmen:graphify · ağ, hesap · - | graf gezinmede komşu seçimini ucuz sınıflandırıcıya bırak |
| SemDecide | CLI | https://github.com/sharziki/semdecide | UYARLA | ★77 push:2026-09-16 arşiv:h · kısmen:jev CLI · shell, ağ, hesap · - | alınacak: karar sonucunu çıkış koduna bağlayıp CI adımını geçir/durdur → jev CLI |
| typesafe-mcp | MCP | https://github.com/itsmostafa/system-one-connector | RED | ★350 push:2026-10-09 arşiv:h · kurulu:jev mcp, typesafe plugin · ağ, hesap · her oturum | bizde aynısı kurulu |
| Composio Jev toolkit | barındırılan MCP | https://composio.dev/toolkits/jev | RED | site canlı · kurulu:jev mcp · ağ, hesap · her oturum (2 araç) | doğrudan MCP varken üçüncü taraf aracının artısı yok |
| jev-codex-router | model yönlendirici | https://github.com/0xNatoshi/jev-codex-router | RED | ★273 push:2026-09-22 arşiv:e · yok · shell, hesap · - | arşivlenmiş |
| jev-review | kod inceleme | https://github.com/devagrawal09/jev-review | UYARLA | ★683 push:2026-09-17 arşiv:h · kısmen:code-review, inc-diff-risk-puani · shell, ağ, hesap · - | alınacak: önce dosya başına ucuz risk skoru, derin inceleme yalnız yüksek skora → inc-diff-risk-puani |
| json-render | üretken UI kütüphanesi | https://github.com/vercel-labs/json-render | ÖĞREN | ★18629 push:2026-10-12 arşiv:h · yok · - · - | model serbest kod değil katalog bileşenlerini seçen JSON üretsin |
| Canny | kanca seti | https://github.com/qkal/Canny | UYARLA | ★122 push:2026-09-22 arşiv:h · kısmen:inc-dogrulama-oncesi-bitis, hookify · shell (node 22) · Stop kancası | alınacak: bitiş iddiasında kanıt arayan Stop kancası → hookify kuralı |
| jev-curate | veri eleme CLI | bulunamadı | RED | repo 404 (PyPI 0.2.0 deneysel) · yok · ağ, hesap · - | repo kaldırılmış; eğitim verisi işi yok |
| killmyidea | demo | https://github.com/monteduro/killmyidea | ÖĞREN | ★262 push:2026-09-24 arşiv:h · yok · ağ, hesap · - | sabit seçenekli tipli karar ucuz ve tekrarlanabilir |
| jev-trader | ticaret ajanı | https://github.com/jarrodwatts/jev-trader | ÖĞREN | ★2965 push:2026-10-12 arşiv:h · yok · cüzdan anahtarı, hesap · - | blok başına tek karar deseni; gerçek para riski, kurulmaz |
| Prism liquidity agent | ticaret ajanı | https://github.com/irfndi/prism-liquidity-agent | ÖĞREN | ★125 push:2026-09-28 arşiv:h · yok · cüzdan anahtarı, hesap · - | geriye dönük testli strateji + ucuz karar modeli; kurulmaz |
| typesafe-mario | demo | https://github.com/fhshaik/typesafe-mario | ÖĞREN | ★449 push:2026-09-16 arşiv:h · yok · shell, hesap · - | pikselden değil yapısal durumdan karar hızlı ve ucuz |
| OneVOneJev | demo (Three.js oyun) | https://github.com/emrickgarrett/OneVOneJev | ÖĞREN | ★42 push:2026-09-18 arşiv:h · yok · ağ, hesap · - | oyun rakibi kararlarını ucuz tipli modele vermek |
