# Slash katalog — iş türü → hangi "/" komutu/skill (SLASH-ÖĞREN d1; kaynak: .kos/ogrenme/slash-envanter.tsv, 2127 kalem)
Erişim (CC, denendi 20 Eki): ana oturum `Skill` aracıyla çağırır; Agent alt ajanı da çağırır (alt ajan tanımında `tools:` varsa `Skill` yazılı olmalı). Slash komutu = .md dosyası → alt ajan Read ile okuyup uygulayabilir. Köprü (ajan_sira) oturumu varsayılan GÖRMEZ (`--disable-slash-commands` + `--tools` listesinde Skill yok); açmak: `python onay/slash_ac.py uygula` (geri: `--geri`).
Kalan ~2100 kalem: `yetenek-getir` ya da `.kos/ogrenme/slash-envanter.tsv` (Grep ad/aciklama). Aynı ad çok pluginde kopya (98 çift ad: claude-api, mcp-builder, frontend-design, docx…) — hangisi çağrılsa aynı gövde.
Ölçülen kazanç sütunu: yalnız ölçülen yazıldı; "denenmedi" = kartta iddia yok.

| iş türü | çağır | ne zaman / argüman | kombo | ölçülen kazanç |
|---|---|---|---|---|
| kod tabanı sorusu, ilişki, mimari | `/graphify` (query/path/explain) | önce sor2/graphify query; grafik yoksa kur | → jev ilgili → Read dar aralık | `graphify query` "Groq whisper nerede": ~1,7k tok · 2,8 sn · 16 groq isabeti; GRAPH_REPORT.md tümü ~250k tok (bayt/4) |
| 2+ alana yayılan / araç belirsiz iş | `plan-kur` | tek çağrı; yetenek-getir içinde | → departman-* müdürü | `plan_kur.py` (reel izle + KVKK web): ~1,5k tok · 0,3 sn tek çağrı; kapılar (KVKK/video) çıktıda 32 isabet |
| "hangi araç/skill/MCP var?" | `yetenek-getir` | katalog araması (3.3k kalem) | → plan-kur | `katalog_ara.py` "altyazısız IG reel sesiyle izle": ~1,7k tok · 0,2 sn; ilk 10 skill'de video-izle #1, watch #7; yetenek.tsv tümü ~192k tok (bayt/4) |
| hata, kırık test, beklenmeyen davranış | `superpowers:systematic-debugging` | düzeltmeden ÖNCE; kök neden kanıtı | → TDD (yeniden üretim testi) | denenmedi |
| özellik/bugfix kodu yazmadan önce test | `superpowers:test-driven-development` | kırmızı gör → min kod | ← systematic-debugging | ÖLÇÜLDÜ (slash_kart.py, n=1): skilli kol kırmızı testi kaynak düzeltmesinden ÖNCE gördü (adım 5<6) · 9 tur · $0,91; skillsiz kol 4 tur · $0,43 · kırmızı test YOK (Edit→python -c) → TDD disiplini ~2x maliyet, kırmızı kanıt yalnız skill ile |
| "X yapalım" belirsiz istek, tasarım seçimi | `superpowers:brainstorming` | kod/plan öncesi | → writing-plans/plan-kur | denenmedi |
| mevcut kodda yönlendirmeli yeni özellik | `/feature-dev:feature-dev <özellik>` (komut) | keşif→mimari→uygula; büyük özellik | → code-review | denenmedi |
| web arayüzü yapmak/değiştirmek | `frontend-craft:frontend-craft` | UI'ya dokunan HER iş, önce; Bölüm 6 turu şart | → impeccable (denetim/polish) | denenmedi |
| tasarım eleştirisi, polish, redesign | `impeccable:impeccable` | frontend-craft'tan sonra; çakışmada frontend-craft kazanır | ← frontend-craft | denenmedi |
| yeni kod/PR güvenlik incelemesi | `phoenix-security-review:security-reviewer` | web/API/CLI kodu eklenince | → departman-guvenlik | denenmedi |
| PR/diff kod incelemesi | `/code-review:code-review` (komut; gh gerekir) | PR numarası/dalı | ← feature-dev | denenmedi |
| MCP sunucusu yazmak | `mcp-builder` (example-skills:/claude-api: kopyası) | yeni MCP tasarımı | → test-qa | denenmedi |
| Claude API / Agent SDK uygulaması | `claude-api` | anthropic SDK kodu, model/cache | — | denenmedi |
| skill yazmak/iyileştirmek/ölçmek | `skill-creator:skill-creator` | Windows'ta run_eval çalışmaz → tek seferlik claude -p | → zip_denetle | denenmedi |
| video içeriği (ses+görüntü) anlamak | `watch:watch <url> [--engine gemini\|local --whisper groq]` | altyazısız reel/video; gemini = tam izleme (ücretsiz 20 istek/gün), local+groq = kare+ses metni | video-izle'nin altyazı-yok halkası | IG reel, `--engine local --whisper groq`: 10,5 sn · 30 segment (ses okundu; `video izle` 0 segment) · rapor 9,2 KB; gemini 429 (günlük kota) → doğruluk karşılaştırması YAPILAMADI. video-izle halkası (d5): `video paket ig-DelsVQJR6ZE --asr groq` önbelleksiz 25,6 sn toplam (asr 5,7 sn), 9 satır Türkçe konuşma, paket ~2,6k tok metin + 3 kare ~1,3k tok, Groq isteği tek (ücretsiz) |
