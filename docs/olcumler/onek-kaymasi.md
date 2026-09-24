# Önek kayması (21a K1)

## Ölçüm
- Son 3 gün, 233 oturumun ilk isteği (transcript usage): cache_creation medyan 76.192, ortalama 49.818; cache_read medyan 7.426. Read kümeleri: 0 (87 oturum, önbellek soğuk/başka proje), ~17k (44), ~7k (27), ~29k (16).
- Kontrollü deneme (2 × `claude -p "ok de"`, sonnet, aynı dizin, art arda, toplam $0.62): ikisinde de **cache_read = 17.565**, cache_creation 76.167 / 77.444. Saniyeler arayla aynı istem bile 17.565. token'dan sonrasını paylaşamıyor.
- headroom perf: 233/4115 istekte write > 2×read; "First 5 avg read=20.7k write=30.9k".

## Ayrışma noktası
> 21b: bu hipotez istek gövdesiyle çürütüldü; sistem metni iki oturumda bayt bayt aynı. Güncel teşhis aşağıda "21b" bölümünde.

17.565. token: araç bloğunun sonu / sistem metninin başı. Aynı dizin ve aynı istemle bile kayma olduğuna göre sebep oturuma özel bir alan. Sistem metnindeki Environment bölümü oturum kimliği taşıyan scratchpad yolunu içeriyor (`...\Temp\claude\<proje>\<oturum-id>\scratchpad`). Bu yüzden sistem kırılım noktası her oturumda ıskalanıyor ve önbellek araç kırılım noktasına düşüyor. Tarih, gitStatus, claude-mem bağlamı ve CLAUDE.md mesajlarda (system-reminder) yer alıyor; bunlar yalnız mesaj önbelleğini etkiliyor.
Güven: ayrışma konumu yüksek (iki bağımsız ölçümde bayt bayt aynı sayı). Sebep orta: istek gövdesi karşılaştırılmadı, çünkü Headroom `--log-messages` açık değil ve 8787'yi caveman tutuyor (bkz. bekleyen/caveman-otobaslat.md).

## Oturum başına yeniden yazılan token
~76k (claude -p ve etkileşimli oturum medyanı aynı). Bunun ~17.5k'sı paylaşılıyor, geri kalan ~58.6k'nın sistem metni kısmı gereksiz yere yeniden yazılıyor.

## Sabitleme önerisi
1. Sebebi kesinleştir: iki oturumun istek gövdesini `headroom capture` ile yakala ve sistem bloklarını diff'le (docs/kurulumlar/bekleyen/onek-sabitle.md, KOŞULMAZ).
2. Scratchpad yolu doğrulanırsa CC tarafında oturumdan bağımsız bir yol ya da kapatma ayarı aranır; ayar yoksa CC'ye hata/istek bildirilir. Repo içinde yapılacak bir değişiklik yok.

## 21b teşhis (istek gövdesi)
Yöntem: 8791'de stdlib kaydedici (scratchpad, repo dışı); `tools` içeren `/v1/messages` gövdesini diske yazıp 400 döndü, upstream'e gitmedi ($0). 2 × `claude -p "ok de"` sonnet, yönlendirme `--settings '{"env":{"ANTHROPIC_BASE_URL":…}}'`. Headroom ikinci örneği kullanılmadı: `--log-messages` yalnız `messages`'ı kaydediyor, `system`/`tools`'u değil (headroom/proxy/handlers/anthropic.py:3477).

İstek düzeni (önek sırası): tools (15, 56.471 kar) → system[0..2] (27.610 kar, kırılım system[2]'de) → messages[0] user (CLAUDE.md, gitStatus, tarih; 10.991 kar, kırılım yok) → messages[1] (tek blok, 195.994 kar, kırılım sonunda).
- tools + system iki oturumda **bayt bayt aynı** = 84.081 kar = paylaşılan 17.565 token. Scratchpad yolu sistem metninde değil; hipotez çürüdü.
- İlk fark: messages[1], ofset 20.594 (~29k token). Parça: ertelenmiş MCP araç listesi + "hâlâ bağlanıyor" sunucu listesi. 2. oturumda mcp-git, mcp-time, mcp-sequential-thinking ilk istekte henüz bağlı değildi (stdio başlatma yarışı). Bu 3 sunucunun satırları atılınca kalan fark yalnız bekleyen sunucu listesi.
- Aynı blokta ofset 8.764'te claude-mem bağlamı dakika damgası ve son gözlemlerle geliyor; messages[0]'da gitStatus var. İkisi de oturumdan oturuma değişiyor, yani yarış olmasa da bu blok neredeyse her yeni oturumda yeniden yazılıyor.

Sonuç: 17.565, önbelleğin ulaşabildiği son kırılım (system sonu). Ondan sonraki ~58.6k token (messages[0] + messages[1]) tek parça halinde yeniden yazılıyor.

messages[1] bileşimi (≈3,53 kar/token): skill listesi ~36.5k (393 skill) · ajan tipleri ~8.3k · ertelenmiş araç listesi ~3.8k · MCP talimatları ~2.7k · hook (ponytail+superpowers) ~2.5k · claude-mem ~1.7k; messages[0] ~3.1k. Skill listesinde en büyükler: anthropic-skills ~4.7k, dotnet-test ~3.7k, dotnet-msbuild ~3.6k, agent-skills ~3.0k, phoenix-prd-pipeline ~2.9k, claude-mem ~1.7k, taste-skill ~1.4k, phoenix-security-review ~1.3k, example-skills ~1.1k.

## 21b çözüm araştırması (CC dokümanı)
- MCP'nin tamamının bağlanmasını bekleten ayar yok. `MCP_TIMEOUT` yalnız sunucu başına başlatma zaman aşımı. code.claude.com/docs/en/mcp.md
- gitStatus'u kapatan ayar yok. `includeGitInstructions` yalnız commit/PR talimatlarını kaldırıyor. settings-reference.md
- SessionStart `additionalContext` için önbellek yerleşimi belgelenmemiş.
- Doküman, araç arama açıkken MCP bağlanmasının öneki bozmadığını söylüyor (prompt-caching.md). Ölçüm bunun tersini gösteriyor: bekleyen/bağlı sunucu listesi kırılımlı blokta.
- Sabitleme mümkün değil: gitStatus ve claude-mem damgası kontrolümüz dışında ya da her oturumda değişiyor. **Kontrolümüzdeki kaldıraç bloğun boyu:** her yeni oturumda yeniden yazılan metni küçültmek.

## Öneri ve beklenen kazanç
Bu repoda kullanılmayan eklentiler proje düzeyinde kapatılır (dotnet-test, dotnet-msbuild, phoenix-prd-pipeline, phoenix-security-review, taste-skill, example-skills). Beklenen: skill listesinden ~13.9k, ajan tiplerinden ek birkaç k → oturum başına ~15k token daha az yeniden yazım. 78 oturum/gün × 15k ≈ **~1.2M token/gün** önbellek yazımı. Uygulama ve doğrulama: docs/kurulumlar/bekleyen/onek-sabitle.md (KOŞULMAZ, Ömer karar verir).
