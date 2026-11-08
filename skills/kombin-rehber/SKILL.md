---
name: kombin-rehber
description: Picks the best 1-3 proven tool combinations (skill + MCP + CLI chains, cheapest step first) for the job type - site-3d, render, video, logo-gorsel, kurulum, kod-backend, guvenlik, belge, mod, hafiza-token. Use at the start of any job to decide which tools run together and in what order. Not for running the tools themselves.
---

# kombin-rehber

1. Classify the job with one word: site-3d, render, video, logo-gorsel, kurulum, kod-backend, guvenlik, belge, mod (or hafiza-token for memory/token work).
2. Open `references/kombinler.md`, jump to that type's heading, pick the best 1-3 combos by `amac`. Do not use all of them.
3. Run the steps in listed order; each step's output feeds the next one. Cheap/local steps come first, the model judges last.
4. Always-on core (every job): beyin ara/kaydet, ruflo pattern-search/store, claude-mem, rtk, headroom, context-mode; graphify for code jobs.
5. Learning loop: at the start read prior mistakes (ruflo pattern-search "hata-dersi", beyin ara "<proje> hata"); at the end save 1-3 lessons (beyin kaydet + ruflo pattern-store).
6. In claude.ai, local CLIs (rtk, graphify, headroom) run only through the cc-kopru command; if unavailable, skip that step and say so in the report.
7. Report one line: `kombin: <id> · adimlar kullanilan/toplam`.

New combo idea after a job? Add it to your report as `kombin-oneri: <id> · amac · adimlar`; the owner approves before it is added.
6. Tool lookup: `references/arac-kartlari.md` holds one short card per installed tool (what, when, not-when, call pattern, good partners, history); `references/kombin-gecmis.md` lists tool sets that succeeded per job type. Grep them by keyword; open a tool's own SKILL.md only for detail.

- Penpot (açık kaynak, kalem logolu Figma karşılığı): MCP `penpot` kayıtlı (http://localhost:4401/mcp); sunucu `npx @penpot/mcp` + tarayıcıda Penpot eklentisi gerekir, Docker kurulmadı.

- URL hileleri (De7WIcEogeo, 30 Eki): repo URL'sinde tek kelime değiştir. `github.com/o/r` -> `gitreverse.com/o/r` (repoyu yapan prompt) ve `gitdiagram.com/o/r` (mimari diyagram). Kaynak videoda 8'in yalnız 2'si görünür, kalanı DM; doğrulanmadan listeleme. Repo incelemede ilk ucuz adım.
