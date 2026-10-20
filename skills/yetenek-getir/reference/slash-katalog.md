# Slash katalog — iş türü → hangi "/" komutu/skill (SLASH-ÖĞREN d1; kaynak: .kos/ogrenme/slash-envanter.tsv, 2127 kalem)
Erişim (CC, denendi 20 Eki): ana oturum `Skill` aracıyla çağırır; Agent alt ajanı da çağırır (alt ajan tanımında `tools:` varsa `Skill` yazılı olmalı). Slash komutu = .md dosyası → alt ajan Read ile okuyup uygulayabilir. Köprü (ajan_sira) oturumu varsayılan GÖRMEZ (`--disable-slash-commands` + `--tools` listesinde Skill yok); açmak: `python onay/slash_ac.py uygula` (geri: `--geri`).
Kalan ~2100 kalem: `yetenek-getir` ya da `.kos/ogrenme/slash-envanter.tsv` (Grep ad/aciklama). Aynı ad çok pluginde kopya (98 çift ad: claude-api, mcp-builder, frontend-design, docx…) — hangisi çağrılsa aynı gövde.
Ölçülen kazanç sütunu: yalnız ölçülen yazıldı; "denenmedi" = kartta iddia yok.

| iş türü | çağır | ne zaman / argüman | kombo | ölçülen kazanç |
|---|---|---|---|---|
| kod tabanı sorusu, ilişki, mimari | `/graphify` (query/path/explain) | önce sor2/graphify query; grafik yoksa kur | → jev ilgili → Read dar aralık | denenmedi (token-rea ölçümleri ayrı) |
| 2+ alana yayılan / araç belirsiz iş | `plan-kur` | tek çağrı; yetenek-getir içinde | → departman-* müdürü | denenmedi |
| "hangi araç/skill/MCP var?" | `yetenek-getir` | katalog araması (3.3k kalem) | → plan-kur | denenmedi |
| hata, kırık test, beklenmeyen davranış | `superpowers:systematic-debugging` | düzeltmeden ÖNCE; kök neden kanıtı | → TDD (yeniden üretim testi) | denenmedi |
| özellik/bugfix kodu yazmadan önce test | `superpowers:test-driven-development` | kırmızı gör → min kod | ← systematic-debugging | denenmedi |
| "X yapalım" belirsiz istek, tasarım seçimi | `superpowers:brainstorming` | kod/plan öncesi | → writing-plans/plan-kur | denenmedi |
| mevcut kodda yönlendirmeli yeni özellik | `/feature-dev:feature-dev <özellik>` (komut) | keşif→mimari→uygula; büyük özellik | → code-review | denenmedi |
| web arayüzü yapmak/değiştirmek | `frontend-craft:frontend-craft` | UI'ya dokunan HER iş, önce; Bölüm 6 turu şart | → impeccable (denetim/polish) | denenmedi |
| tasarım eleştirisi, polish, redesign | `impeccable:impeccable` | frontend-craft'tan sonra; çakışmada frontend-craft kazanır | ← frontend-craft | denenmedi |
| yeni kod/PR güvenlik incelemesi | `phoenix-security-review:security-reviewer` | web/API/CLI kodu eklenince | → departman-guvenlik | denenmedi |
| PR/diff kod incelemesi | `/code-review:code-review` (komut; gh gerekir) | PR numarası/dalı | ← feature-dev | denenmedi |
| MCP sunucusu yazmak | `mcp-builder` (example-skills:/claude-api: kopyası) | yeni MCP tasarımı | → test-qa | denenmedi |
| Claude API / Agent SDK uygulaması | `claude-api` | anthropic SDK kodu, model/cache | — | denenmedi |
| skill yazmak/iyileştirmek/ölçmek | `skill-creator:skill-creator` | Windows'ta run_eval çalışmaz → tek seferlik claude -p | → zip_denetle | denenmedi |
| video içeriği (ses+görüntü) anlamak | `watch:watch <url> [--engine gemini\|local --whisper groq]` | altyazısız reel/video; gemini = tam izleme (ücretsiz 20 istek/gün), local+groq = kare+ses metni | video-izle'nin altyazı-yok halkası | IG reel, `--engine local --whisper groq`: 10,5 sn · 30 segment (ses okundu; `video izle` 0 segment) · rapor 9,2 KB; gemini 429 (günlük kota) → doğruluk karşılaştırması YAPILAMADI |
