# Ajan / skill / plugin geliştirme — birleşim tarifi
Ne zaman: Yeni skill, alt ajan, hook, MCP sunucusu ya da plugin yazmak veya iyileştirmek.

## Fazlar
1. Keşif: `departman-surec-ajan-arac` — skill, plugin, hook, MCP ve Claude API geliştirme sırası · birlikte: `ecc:skill-scout` var olan skill'i bulur ya da çatallar.
2. Eval önce: `ecc:eval-harness` — kodlamadan önce yetenek ve regresyon eval'i, pass@k · birlikte: `promptfoo-evaluation` Promptfoo yapılandırması.
3. Yazım: skill için `skill-creator:skill-creator` (oluştur, eval koş, benchmark); alt ajan için `ajn-ajan-tanimi-yazar` (dar araç, ucuz model, kısa prompt); hook için `plugin-dev:hook-development`.
4. MCP: `mcp-server-dev:build-mcp-server` — MCP sunucusu tasarımı ve dağıtım modeli · birlikte: `ecc:mcp-server-patterns` araç, kaynak, Zod doğrulama, taşıma seçimi.
5. Paketleme: `plugin-dev:plugin-structure` — plugin.json ve bileşen düzeni · birlikte: `plugin-dev-plugin-validator` yapıyı doğrular.
6. Güvenlik ve test: `skill-scanner` — skill'de enjeksiyon ve güvenlik taraması · birlikte: `ecc:security-scan` .claude dizinini, hook'ları ve ajan tanımlarını denetler; MCP elle sınama `@modelcontextprotocol/inspector`.
7. Kapanış: `superpowers:verification-before-completion`.

## İnceleme ajanları
- `ecc:agent-architecture-audit`: ajan hatalı davranınca hangi katmanın bozuk olduğunu bulur.
- `ponytail-review`: gereksiz soyutlama avı.

## Güvenlik ve kalite kapıları
- Eval yeşil; tetik testi yapıldı.
- `skill-scanner` ve `ecc:security-scan` temiz.
- Hook ve betikte sır yok: `gitleaks`.

## Tartışma konseyi
- Karar: skill mi alt ajan mı hook mu MCP mi; araç yüzeyinin genişliği.
- `ecc:council` — varsayılan Claude personaları: kullanıcı, bakımcı, güvenlik.

## Jeton bütçesi
- Keşif: küçük (~6k, tahmini). Eval: orta (~15k). Yazım: orta (~20k). MCP: büyük (~30k). Paketleme: küçük (~5k). Güvenlik/test: orta (~10k). Hepsi tahmini.
- Eval koşu çıktıları `okuyucu` alt ajanına.

## Kaçınılacaklar
- Model tabanlı derecelendirici ve k tekrarlı koşu ek model çağrısı demektir (`ecc:eval-harness`); üst sınır koy.
- Aynı işi gören kopyaları karıştırmak (`skill-creator` ile `skill-writer`, `plugin-dev:agent-development` ile `agent-development`); birini seç.

## Aday (kurulu değil)
- `fable_ajan_hook`: dosyası değiştirilemeyen alt ajanlara protokolü SubagentStart ile verir.
- `model_olc`: alt ajan modeli ölçümü.
