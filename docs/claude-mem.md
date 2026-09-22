# claude-mem — iki taraf · KURULUM-11b · 20 Eyl 2026

Sürüm 13.25.2 · sağlayıcı **claude + haiku-4.5** · worker **127.0.0.1:37777**.

## Yazma yolu (K5a — kanıtlı karar)

| Yol | Sonuç | Kanıt |
|---|---|---|
| MCP yazma araçları | **kapalı** | `scripts/mcp-server.cjs`: `yE=["observation_add","observation_record_event","observation_search","observation_context","observation_generation_status","memory_add","memory_search","memory_context"]`, `SE(e,t){return t==="server"?[...e]:…e.filter(r=>!BA.has(r.name))}` — yalnız `runtime==="server"` (cmem.ai Pro; `CLAUDE_MEM_SERVER_{URL,API_KEY,PROJECT_ID}`). Pro kapsam dışı. |
| worker HTTP `POST /api/memory/save` | **çalışıyor** | `{"success":true,"id":359,"message":"Memory saved as observation #359"}` |
| worker HTTP `POST /api/observations` | yok | HTTP 404, `Cannot POST` (uç salt GET) |
| `claude-mem` CLI | PATH'te yok | `command -v claude-mem` boş |

**Desktop kararı — yapısal:** yazma ucu makinede çalışıyor ama Desktop chat'te o ucu
çağıracak araç yok (`mcp-fetch` salt GET). Desktop'ta hook da yok. CC tarafında hook
zaten worker'a yazıyor → **CC yazar, Desktop okur.**

## Korpuslar (K5b)

| ad | filtre | gözlem |
|---|---|---|
| `omer-skills` | project=omer-skills · types=decision,discovery,change,feature | **335** (160.632 token) |
| `divisima` | project=divisima · +bugfix | **0** |
| `corvano` | project=corvano · +bugfix | **0** |

`GET /api/projects` → `{"projects":["omer-skills"]}`. divisima ve corvano claude-mem'de
**hiç kayıtlı değil**; korpuslar kuruldu ama boş, o projelerde CC oturumu açıldıkça dolar.

`rebuild_corpus` **dalga kapanışında** koşar (yeni gözlemler korpusa girsin diye).

`query_corpus` kanıtı: "KURULUM-10a'da pixeljury neden başarısız oldu" sorusu
primed `omer-skills` korpusundan yanıtlandı (session `6a9a7db4`).

## session_start_context (K5f)

`session_start_context(project="omer-skills")` → oturum başı enjeksiyon.
Ölçüm: **50 gözlem · ~21.1k token okundu · 241k iş · %91 tasarruf**.

**Öneri (uygulanmadı):** `CONTEXT_OBSERVATIONS` 50 → **30**; gerekçe: listenin son
üçte biri aynı dalganın adım adım satırları (344-360), özet değeri düşük, oturum başı
sabit maliyeti yüksek. Ayarı Ömer değiştirir.

## Arama yüzeyi (K5d/K5e)

- `search(type="prompts")` / `search(type="sessions")` — kendi geçmiş promptlarını bulmak için.
- `get_tool_uses` — geçmiş oturumdan ham komut/çıktı.
- `smart_*` Desktop'ın **tek** kod keşif yolu (graphify CLI Desktop'ta koşmaz) — çift kopya değil.

## Yetenek tablosu — KURULUM-11m-A-FIX-5 (22 Eyl 2026, ölçülerek)

- **SessionStart enjeksiyonu**: çalışıyor (10 111 kr blok). İşe yaradı: oturum açılışında
  son işler geliyor. Kusur: başlık canlı saat damgası taşıyor (worker-service.cjs:225
  `Eoe()`), gövde uzunluğu her çağrıda değişiyor → `ajan` prompt cache'i kırılıyor
  (14 678 → 9 523 kr, cache okuma %0 → %46). Köprü tarafında susturulamıyor: bağlamı
  worker render ediyor, çocuk sürecin `CLAUDE_MEM_CONTEXT_*` değişkeni etkisiz (ölçüldü).
- **mem-search (`search`)**: çalışıyor. İşe yaradı: #719 "Headroom compression is lossy",
  #923 "Headroom proxy URL still unreachable" bu dalganın teşhisine girdi. Kusur yok.
- **Korpus (`list_corpora`/`query_corpus`)**: çalışıyor ama korpus 20 Eyl'de donmuş
  (335 gözlem, son kayıt 2026-09-20). İşe yaramadı — bu dalganın kayıtları içinde yok.
  Kusur: rebuild gerekiyor; rebuild sağlayıcı çağrısı ürettiği için tarife göre
  yapılmadı (ücretli çağrı tavanı) → Ömer'in kararına bırakıldı.
- **`get_tool_uses`**: çalışıyor (id 2872 ham girdi/çıktısıyla döndü; yeniden koşmaya
  gerek kalmadı). Kusur: köprü gözlemleri `tool_use_id` göndermediği için worker
  `tool_uses` satırı yazmıyordu (`XR`: `if(t.toolUseId)`) → bu dalgada eklendi
  (`kos.mjs gozlemGovde` → `kopru_<uuid>`).
- **`smart_*` (`smart_search`)**: koşuyor ama boş dönüyor — `ciktiHazirla` için
  `tools/cc-kopru` altında 27 dosya tarandı, 0 sembol. Kusur: .mjs export'larını
  bulamıyor; keşifte graphify query kullanılıyor, bu yüzden dalgayı engellemedi.
- **Köprü `kaydet` / `oturum_ozeti`**: `kaydet` gitleaks kapısından geçen metni
  `/api/memory/save` ucuna yazıyor, `oturum_ozeti` `/api/sessions/summarize` +
  `/api/processing-status` okuyor (sunucu.mjs). Kusur: özetleme asenkron ve ajan
  yuvası 2 ile sınırlı; kuyruk doluyken sonuç gecikiyor (CLAUDE-MEM-1 ölçümü).
