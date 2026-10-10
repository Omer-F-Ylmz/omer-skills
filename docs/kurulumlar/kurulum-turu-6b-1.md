# Kurulum turu 6b-1 (2026-10-10 akşam)

Kaynak: `kacan-adaylar.md` "Tur 6b adayları" satır 1–127. Ayrıntı: `tur6b-1-sonuc.tsv`. Betik: `tools/kurulum-turu-6b-1.sh` (log `.kos/kurulum-6b-1/`, geri-al `.kos/kurulum-6b-1/geri-al.sh`; sınıflayıcı `.kos/kurulum-6b-1/sinifla.py`).

## Sayılar
127 aday: KUR 8 · ZATEN 3 · HESAP 19 · ÖNERİLMEZ 2 · AYRI-UYGULAMA 15 (i 1 · ii 10 · iii 4) · RED 80 (gürültü 37 · kapsam 21 · lisans 16 · bulunamadı 6) · KUR-duzeltmeli 0. Hiçbiri elenmedi; RED'ler OCR/komut/model kimliği parçası veya lisanssız.

## Kurulan (SHA pinli, kuru koşu 0 hata → gerçek koşu 6 adım ok, 0 hata)
- czlonkowski/n8n-skills · MIT · cb6caa7b3ae8 · 15 skill (n8n-*, using-n8n-mcp-skills)
- google-gemini/gemini-skills · Apache-2.0 · 832c8f941143 · 3 (gemini-api-dev, gemini-live-api-dev, gemini-omni-flash-api)
- cloudflare/skills · Apache-2.0 · 0871daceb347 · 16 (cloudflare, wrangler, workers-best-practices, durable-objects, agents-sdk, web-perf…)
- netlify/context-and-tools · MIT · b5894c0e1c16 · 15 (netlify-*)
- upstash/context7 · MIT · 522c4db4fa2e · 3 (context7-cli, context7-mcp, find-docs)
- MCP (user scope, pinli): `arxiv` (blazickjp/arxiv-mcp-server 0.8.2, uvx, anahtarsız) ve `hfspace` (@llmindset/mcp-hfspace 0.5.4, anahtarsız). İkisi de Connected.
Toplam 52 yeni skill, `~/.claude/skills/<ad>`; ad çakışması 0.

## Önemli kararlar
- usestrix/strix (Apache-2.0, 9 skill): otonom saldırı/pentest ajanı → ÖNERİLMEZ, yalnız API ile incelendi, klon yok.
- vercel/next-devtools-mcp ve vercel-labs/next-skills: lisans yok, 0 SKILL.md → RED lisans (nextjs.org).
- alishahryar1/free-claude-code (16 OCR çeşidi): lisans NOASSERTION → RED lisans.
- docker/mcp-gateway: tek skill `.claude/` altında olduğu için betik kopyalamadı; Docker AYRI-UYGULAMA ii.
- smithery-ai/cli AGPL-3.0 + hesap → HESAP.
- OCR eşlemeleri: contavt7→context7 · map-hfspace→mcp-hfspace · enescinr/benescinaz…→EnesCinr/twitter-mcp · docs.n8n.lo→docs.n8n.io.
- Zaten bağlı: n8n-mcp, netlify, brave-search, figma, supabase (MCP).

## Doğrulama
52/52 SKILL.md var, yinelenen ad 0. `claude plugin list`: 195 giriş (plugin eklenmedi). `claude mcp list`: arxiv ✔, hfspace ✔ (hfspace ilk denemede MSYS yol dönüşümü yüzünden bozuk eklenmişti; MSYS_NO_PATHCONV=1 ile yeniden eklendi).
