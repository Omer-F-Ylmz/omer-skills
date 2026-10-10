# Kütüphane ölçüm planı (KÜTÜPHANE-3a, 10 Eki 2026)

Kural: kalite ve performans düşmez, token tasarrufu artar. Her aday `tools/olcum/kosucu.py` ile A/B (12 görev, `gorevler.json`; profil = `profiller.json`). Bu belge ayar değiştirmez; settings.json değişiklikleri Ömer'de.

## Ölçülen bileşenler (boş klasör, "tamam yaz", `bilesen-2026-10-10.json`)
| Bileşen | Sayı | Jeton payı (tahmin) | Dayanak |
|---|---|---|---|
| Skill listesi | 1871 skill, 2136 slash | ≈ 55k (~%40) | `--disable-slash-commands` maliyeti 1.055→0.637 USD (−%40) |
| MCP araç tanımları | 51 sunucu, 515 araç | ≈ 14k (~%10) | `--strict-mcp-config` 1.055→0.948 USD |
| Ajanlar | 278 | ≈ 6–10k | olcum-3: 87 kullanıcı ajanı ≈ 5.7k; plugin ajanları ek |
| Çekirdek (sistem, yerleşik araçlar, CLAUDE.md, RTK.md) | – | ≈ 55–65k | kalan |
| Hook çıktısı | 97 olay / ~49 KB olay verisi | belirsiz (bağlama yalnız additionalContext girer) | stream-json |
| **Toplam tam profil** | | ≈ 136.6k (olcum-3) | |
| **Runner A1 profili** (hafif.py bayrakları) | araç 0, MCP 0, skill 0, ajan 4 | **6.9k** (cc 3.2k + cr 3.7k) | gerçek çağrı, USD 0.06 |

Not: ilk üç kolda `--max-budget-usd 0.5` ilk turda aşıldı → result olayında usage yok; jeton payları USD oranından türetildi (tahmin). Koşucu düzeltildi (bütçe 3 USD + ilk tur usage yedeği); kesin sayı için sonraki ölçümde yeniden koşulmalı (3 çağrı).

## Runner çağrı bağlamı
`tools/video/video/hafif.py` A1: `--tools "" --setting-sources "" --strict-mcp-config --safe-mode --disable-slash-commands --no-session-persistence` → 6.9k boş bağlam (tam profilin %5'i). `motor-usage.jsonl` gerçek günlük: 9 Eki 2065 çağrı × ort. 26k bağlam (cc 20k + cr 5.7k) = 136.96 USD; 10 Eki (öğlene kadar) 672 çağrı × 38k = 69.07 USD. Tam profille aynı çağrılar ≈ 2065 × 136k = 281M jeton/gün; mevcut 54M → hafif profil zaten ~%80 tasarruf. Kalan: ortalama 26–38k içinde 6.9k sabit, gerisi paket+kare+çıktı (cc 20–30k = paket içeriği). `tools/video/ab_ucuz.py` ve `kur.py:661` (deneme) hafif bayrak kullanmıyor.

## Hook gürültüsü
`[hook hata: plugin:ecc|… bootstrap …]` kaynağı: ecc `session-start-bootstrap.js` normal bilgi satırlarını (`[SessionStart] Found 66 recent session(s)`, `No CLAUDE_SESSION_ID…`) stderr'e yazar; cc-kopru `tools/cc-kopru/hook.mjs:392` exit 0 olsa da stderr doluysa "hook hata" etiketler. Gerçek hata değil. Maliyet: çağrı başına ~40–80 jeton (3 satır). Susturma: (1) köprüde etiketi yalnız `r.kod !== 0` için bırak (`hook.mjs`, repo içi, düşük risk); (2) ya da ecc session-start hook'unu köprü komutlarında atla. settings.json gerekmez.

## Sıralı öneriler
1. **Skill listesi: name-only + departman yönlendirici** — kazanç ≈ −28k (kurulum-2d tahmini; yukarıdaki ölçüme göre üst sınır ≈ −55k). Kalite koruma: skill gövdesi yerinde, yalnız açıklama gizli; yönlendirici skill departman→skill haritası taşır. A/B ölçütü: G03, G05, G07 araç-isabeti (`arac_isabet`) tam üzerinde düşmez ≥ taban; kalite puanı ≥ taban. Uygulayan: Ömer (`tools/overrides-uygula.ps1`, settings.json).
2. **MCP araç tanımları deferred/ihtiyaçta** — ≈ −14k. 51 sunucudan günlük işte kullanılmayanlar proje düzeyinde kapalı; `/mcp` ile açılır. Kalite koruma: G06 (web) ve G04 kullanılan araçlar açık kalır. Ölçüt: G06 doğru araç + kalite ≥ taban. Uygulayan: Ömer.
3. **Ajan kütüphanesi + /ajan-getir** — ≈ −6–10k (278 ajan; olcum-3: −5.7k yalnız kullanıcı ajanları). Kalite koruma: sık kullanılan 10–15 ajan yüklü kalır. Ölçüt: G01, G09 (code-reviewer/security-auditor tetikleniyor mu). Uygulayan: Ömer (~/.claude/agents taşıma).
4. **Hook gürültüsü (stderr etiketi) susturma** — ≈ −50 jeton/köprü çağrısı (küçük ama bedava); `hook.mjs` düzeltmesi + test. Kalite etkisi yok (gerçek hata exit≠0 ile hâlâ görünür). Uygulayan: Claude (ayrı dalga, test ile).
5. **Runner profil sıkılaştırma** — günlük 2000+ çağrıda sabit 6.9k'nın altına inmek zor; asıl kazanç paket boyutunda (cc 20–30k/çağrı): kare sayısı/paket sıkıştırma. Ek: `ab_ucuz.py` ve `kur.py` deneme çağrılarına A1 bayrakları. Kalite koruma: rapor denetimi (`video rapor-denetle`) geçişi + kalite puanı ≥ taban A/B. Uygulayan: Claude (runner'a şimdi dokunulmadı).

## KÜTÜPHANE-4 bulguları (10 Eki öğleden sonra)
- `/context` (yerel, model çağrısı yok) ile ölçüldü: **Skills 49.3k = `SLASH_COMMAND_TOOL_CHAR_BUDGET` 150000 tavanı**. Tavansız (600000) istek: tam 189.5k · name-only 164.4k → liste bugün tavanda kırpılıyor, skill'lerin çoğu modele hiç görünmüyor.
- Yalnız name-only (1726 skill, departman-* + 42 çekirdek açıklamalı): jeton farkı **0** (tavan sabit), 294 satır kısaldı → aynı bütçeye daha çok ad sığıyor (keşif artışı, maliyet sabit). 12 görev A/B G01–G05: bağlam 136–141k, kalite aynı.
- Bütçe kolu: 75000 → Skills **24.3k** (−25k, /context toplam 91.4k → 67.4k); 40000 → 18.3k. Ajan listesi 29.2k (273 ajan; 186 plugin, 87 kullanıcı) ikinci büyük kalem.
- Koşucu düzeltmeleri: TSV satır satır, `--arka` (profil başına ayrı günlük), `--bekle-pid`, geçici klasör temizlik hatası koşuyu düşürmez (G12 bu yüzden düşmüştü), init ad dökümü `<tarih>-<profil>-init.json`.
- Profil üretimi: `tools/olcum/profil_uret.py` (name-only blok) + `profil_varyant.py` (bütçe env'i). Çıktı json'ları gitignore'da, komutla yeniden üretilir.

## Sonraki adım
Düzeltilmiş koşucu ile `tam` ve `hafif` profil taban ölçümü (12+12 çağrı, ~4 USD/çağrı tavanı konuşulmalı: tam profilde tek "tamam yaz" ≈ 1.05 USD).
