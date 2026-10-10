# Kurulum turu 6b-2 (2026-10-10 akşam)

Kaynak: `kacan-adaylar.md` "Tur 6b adayları" satır 128–253. Ayrıntı: `tur6b-2-sonuc.tsv`. Betik: `tools/kurulum-turu-6b-2.sh` (log `.kos/kurulum-6b-2/`, geri-al `.kos/kurulum-6b-2/geri-al.sh`, sınıflayıcı `sinifla.py`).

## Sayılar
126 aday: KUR 7 · ZATEN 12 · HESAP 12 · AYRI-UYGULAMA 14 (ii 12 · iii 2) · RED 81 (gürültü 61 · kapsam 19 · lisans 1) · KUR-duzeltmeli 0 · ÖNERİLMEZ 0. Ömer'in %90-95 hedefi tutmadı: aday havuzunun çoğu OCR/model kimliği/site parçası, kurulabilir olan 7 aday 4 depoya iniyor.

## Kurulan (SHA pinli, kuru koşu 0 hata → gerçek koşu 0 hata)
- getsentry/skills · Apache-2.0 · d18b7aa8ba87 · 27 skill (`code-review` çakıştı, atlandı)
- getsentry/sentry-for-ai · MIT · c2313d3a826d · 34 skill (src/skills 8 + skills-legacy 26: sentry-*-sdk, sentry-fix-issues…)
- pinecone-io/skills · MIT · 885dc539fbc2 · 9 skill (pinecone-*)
- claude-plugins-official/mcp-server-dev (plugin, user scope)
Toplam 70 yeni skill, `~/.claude/skills/<ad>`; ad çakışması 0 (1 atlandı), her biri SKILL.md'li.

## Kararlar
- Sentry SDK repoları (sentry-go/java/javascript/python) kütüphane; kapsamı sentry-for-ai SDK skill'leri karşılıyor → KUR.
- Figma-Context-MCP (MIT) Figma anahtarı ister; resmi figma MCP zaten bağlı → HESAP. OpenRouterTeam/skills lisanssız → kurulmadı.
- Sentry MCP (NOASSERTION lisans, OAuth hesap) → HESAP. Fastn → HESAP.
- modelcontextprotocol/inspector: karma lisans, npx aracı → AYRI-UYGULAMA ii.
- Ollama ve yerel model etiketleri → AYRI-UYGULAMA ii; SimpleHTR, pulid-flux → iii.
- Atlanan site adayları (fetchable, litmaps, leftclick, zenith.chat…): HTTP 200 ama resmi skill/MCP/CLI bulunamadı → RED kapsam.

## Doğrulama
70/70 SKILL.md var, yinelenen ad 0. `claude plugin list`: mcp-server-dev görünür. `claude mcp list`: MCP eklenmedi (43 bağlı, değişmedi).
