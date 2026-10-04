# TOKEN-6e — Enjeksiyon daraltma

**Karar: hiçbir ayar uygulanmaz.** Ponytail kapatma kaliteyi düşürmüyor ama tasarrufu %4.8, takas eşiği %25 → RED(token). security-guidance RED, superpowers/ECC dokunulmaz, claude-mem TOKEN-6e-2 adayı, kendi dosyalarımız ayrı aday.

## Envanter (her oturum SessionStart, aksi yazılmadıkça)
Ölçülen = gerçek ilk istek context farkı (boş görev K2 n=1, `olcum/token-6e-k2.json`; ponytail ayrıca K3 n=3). Tahmin = hook çıktısı karakter × 0.162 tok/kr (4 kol en küçük kareler) ya da dosya bayt/3.5.

| kaynak | ölçülen Δ | tahmin | kaldıraç |
|---|---|---|---|
| claude-mem | −3.1k (K2; kendi çıktısı koşular arası 21.2k↔32.0k kr, ±1.7k gürültü) | 3.4–5.2k | `~/.claude-mem/settings.json` (global dosya); oturum başına yok (aşağıda) |
| ponytail | −1.7k rtk · −1.8k orta (K3 ilk ctx, 3/3 tutarlı); K2 −0.07k gürültüde | ~1.8k | env `PONYTAIL_DEFAULT_MODE=off` (config.js:3-10, activate.js:28-35) |
| superpowers | +0.3k (gürültü) | ~1.2k | yok |
| security-guidance | +2.5k (gürültü; cmem çıktısı o kolda 32k kr) | ~0.1k (2×284 kr) | env `SECURITY_GUIDANCE_DISABLE` (hook.py:40-41, 164-171) |
| ECC | — | ~0 (6a +17 tok) | bağlam basmıyor |
| hookify · headroom · guard · UserPromptSubmit | — | ≤571 kr / ≤40 kr | — |
| jev-skill | — | koşullu | — |
| global CLAUDE.md · MEMORY.md · proje CLAUDE.md · RTK.md | — | 0.9k · 0.7k · 0.34k · 0.13k (bayt/3.5) | kendi dosyamız → ayrı aday |

## A/B: taban ↔ ponytail-off (`olcum/token-6e-k3.json`, kör puan `olcum/token-6e-kor.json`)
Düzenek 6d: rtk-ab kısa (base d0af0b5) + kur.py orta (base 33b2bd5), iç içe n=3, opus, kol = `claude -p --settings` env `PONYTAIL_DEFAULT_MODE=off`. Kör puan: okuyucu (sonnet), 12 diff A–F adlı, 0–3 × doğruluk · eksiksizlik · kalite; eşleme puanlamadan sonra açıldı.

| görev | başarı T · pt | kör /9 T · pt | $ | ağırlıklı | çıktı | araç T → pt | ilk ctx |
|---|---|---|---|---|---|---|---|
| rtk kısa | 3/3 · 3/3 | 9.00 · 8.67 | −%7.7 | −%7.4 | +%9.1 | 14.0 → 13.0 (−%7.1) | −1.7k |
| orta | 3/3 · 3/3 | 8.33 · 9.00 | −%1.1 | −%0.4 | +%14.1 | 8.7 → 9.7 (+%11.5) | −1.8k |
| toplam | 6/6 · 6/6 | 8.67 · 8.83 | −%4.8 | −%4.4 | — | 22.7 → 22.7 (±0) | — |

Alt ajan her koşuda 0. Taban kendi oynama aralığı: rtk $ 0.92–1.10 · araç 13–16; orta $ 0.74–0.79 · araç 7–10 (ort 8.7, üst uç +%15.4); kör puan aynı kolda 8–9.

## Keşif kapısı
Genel: araç çağrısı ±%0, alt ajan 0 → 0. Görev başına: rtk −%7.1; orta +%11.5 — tabanın kendi aralığı 7–10 (ortalamanın +%15.4'üne kadar), pt ortalaması 9.7 bu aralıkta → **gürültü içinde, kapı geçer**.

## Kararlar
- **ponytail: RED(token).** kur.py:348 `takas(s, d)` (omer-kurallar 21 takas tablosu): düşüş d = 0 (kör puan 8.67 → 8.83, başarı 6/6 → 6/6), tasarruf s = %4.8 sıcak $ < %25 eşik → "düşüş 0, eşik aşılmadı". Uygulanacak satır yok; ponytail varsayılan `full` kalır.
- **security-guidance: RED.** Enjeksiyon ~0.1k (gürültünün altında), güvenlik aracı.
- **superpowers · ECC: dokunulmaz.** Kendi kaldıraçları yok (ECC bağlam basmıyor).
- **claude-mem → TOKEN-6e-2 adayı (SOR).** Oturum başına env/CLI ile geçersiz kılma yok:
  - Öncelik `context-generator.cjs` `applyEnvOverrides`: `process.env[n]!==void 0&&(r[n]=process.env[n])` → process.env > settings.json > DEFAULTS (`CLAUDE_MEM_CONTEXT_OBSERVATIONS:"50"`).
  - Ama okuyan uzun ömürlü WORKER süreci; SessionStart hook yalnız `GET /api/context/inject?projects=..&colors=true` atar (`worker-service.cjs` handleContextInject: yalnız projects · colors · full · platformSource, sayı parametresi yok). `claude --settings` env'i hook alt sürecine geçer, worker'a geçmez (worker'ı o oturum ilk başlatırsa miras alır — koddan çıkarım, denenmedi).
  - Tek kaldıraç global `~/.claude-mem/settings.json` → 6e-2'de Ömer onayıyla A/B.
- **Kendi dosyalarımız → ayrı aday.** Toplam tahmin ~2.1k; metin kısaltma A/B'ye girmedi.

## Uygulanacak satırlar
Yok. (ponytail RED, security-guidance RED, claude-mem 6e-2'ye.) Global ayar değişmedi.
