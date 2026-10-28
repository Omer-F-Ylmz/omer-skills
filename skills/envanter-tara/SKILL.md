---
name: envanter-tara
description: Picks tools for a job in two stages. Stage 1 a script returns a wide compressed candidate set from the whole inventory (catalog, kombin, families, graphify, source libraries, past gold picks); stage 2 you read it, add what is missing, write the 'step · tool · why' plan, then save it as a gold example so later scans learn. Use at the start of any non-trivial job before choosing skills, agents or MCP tools.
---

# envanter-tara

1. Scan (one call, intermediate results stay out of context): `python tools/envanter_tara.py "<job>"` (flags `--satir N`, `--yenile`; cache 7 days). Output is grouped: ALTIN (past gold picks, `ALTIN!` = previously missed), aile (department managers + job-type families, names only), kombin, katalog, graf, kaynak, plus always-useful versatile tools.
2. Decide yourself: the script only proposes candidates (cheap tools can miss). Read the list, add anything you know is missing, then write the plan (<=30 lines, `step · tool · why`) to a file.
3. Save: `python tools/altin_ornek.py kaydet "<job>" <plan file>`. It stores plan and tools in `.kos/kopru/altin-ornek/ornekler.jsonl`, flags tools the scan missed (they rank first next time) and writes a lesson to the second brain. `python tools/altin_ornek.py olc` prints recall of the candidate set against saved picks.

claude.ai note: the scripts need the repo; without it, use the catalog files in the zip (`yetenek.tsv`) and write the plan by hand.
