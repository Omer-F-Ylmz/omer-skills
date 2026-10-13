# ajn — 17 benzersiz kayıt

**Amaç:** Claude Code ajan altyapısı ajanları: alt ajan/hook/slash komut/plugin/MCP yazımı, ajan orkestrasyonu ve belleği, istem denetimi, skill tetik testi, model göçü, Codex/Gemini köprüsü.

**İç yapı:** Tümü [ajan], ajn-<konu>; yazıcılar (ajan-tanimi, hook, slash-komut, plugin-iskelet, mcp-sunucu), denetçiler (prompt, mcp-kurulum, skill-test, arena), tasarım (orkestrasyon, bellek).

## En güçlü parçalar
- `ajn-skill-test` — Skill'in tetiklenip işe yarayıp yaramadığını eşli koşu ve rubrikle ölçer.
- `ajn-mcp-kurulum-denetci` — MCP/plugin yapılandırmasını etkinleştirmeden önce fazla izin ve sır sızıntısına karşı inceler.
- `ajn-hook-yazar` — Güvenli çıkış kodlarıyla doğrulama/otomasyon hook'u.
- `ajn-ajan-tanimi-yazar` — Dar araç, ucuz model ve kısa istemli alt ajan tanımı.
- `ajn-prompt-denetci` — Belirsizlik, eksik çıktı formatı, örnek ve enjeksiyon riski için istem denetimi.
- `ajn-ajan-arena` — İki ajan/istemin rubrik ve önyargı kontrollü kör eşli karşılaştırması.
- `ajn-ogrenilen-ders` — Biten işten yeniden kullanılır ders çıkarıp kurala çevirir.
- `ajn-basliksiz-isci-havuzu` — Sandbox seviyeli, zaman aşımlı paralel headless ajan CLI işçileri.

## Birlikte kullanım
- ajn-ajan-tanimi-yazar → ajn-skill-test → ajn-ajan-arena.
- ajn-mcp-sunucu-yazar → ajn-mcp-kurulum-denetci.
- ajn-plugin-iskelet + ajn-hook-yazar + ajn-slash-komut-yazar.

## Tuzaklar
- claude-plugins-official plugin-dev:* ve anthropic-agent-skills mcp-builder ile çakışır.
- ajn-basliksiz-isci-havuzu paralel ajan çağrısı yapar; zaman aşımı/sayı sınırı şart.
- ajn-migrasyon-model eval karşılaştırması ister; model çağrısı maliyetli.

## Üyeler
- ajan (17): ajn-ajan-arena, ajn-ajan-bellek-tasarimi, ajn-ajan-orkestrasyon, ajn-ajan-tanimi-yazar, ajn-basliksiz-isci-havuzu, ajn-cc-otomasyon-oneri, ajn-claude-api-gelistirici, ajn-codex-claude-koprusu, ajn-hook-yazar, ajn-mcp-kurulum-denetci, ajn-mcp-sunucu-yazar, ajn-migrasyon-model, ajn-ogrenilen-ders, ajn-plugin-iskelet, ajn-prompt-denetci, ajn-skill-test, ajn-slash-komut-yazar
