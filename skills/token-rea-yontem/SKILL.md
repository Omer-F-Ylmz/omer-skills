---
name: token-rea-yontem
description: Method for building a better own version of a token/memory tool (reverse-engineer, 4-axis gate, held-out, backed-up approval script). Use when replacing or improving RTK, graphify, Headroom, claude-mem etc.
---

# TOKEN-REA method (7 steps, proven on sor2 and rtk2)

Goal: an own version installed NEXT TO the old tool (old one is never removed) that beats it on all four axes. One axis failing = the gate fails.

## Four-axis gate

| Axis | Measure | Must |
|---|---|---|
| Tokens | real API input tokens (tool on/off A/B), not a skill-list estimate | save more than the old tool (RTK >30%, graphify >20.6%, Headroom >28.8%) |
| Quality | fixed question/command set + a held-out set | ≥ old tool and ≥ no-tool path (≥98% on held-out) |
| Performance | wall time (cold, end to end via subprocess) and RAM | ≤ old tool |
| Usability | steps per task, retry/error rate, readable output | ≤ old tool |

## Steps

1. **Baseline** — measure the old tool on all 4 axes with a script (min Claude tokens). No quality set yet? Build one first (at least 10 items) and keep a separate held-out set.
2. **Mechanism** — read the source (open source first, no binary analysis when source exists) or reverse it: what it does · where it loses · what we can do better ≤15 lines. Take the mechanism, never copy code.
3. **Own version beside the old one** — e.g. `sor2` (graph + docstring/semantic index + free-pool query expansion + staleness check, plain-text fallback) next to `graphify query`; `rtk2` (signal-preserving summary + full output stored by id, `rtk2 ac <id>` restores it) next to `rtk`. Information is never lost, only kept out of context.
4. **Script-generated held-out** — a generator (`heldout_uret.py <kind> <seed>`) builds the set from repo history/docstrings with a seed (date+number), writes a `.lock` sha256, prints only counts. The developer never reads the set, only runs the scorer. Every gate uses a NEW seed (no tuning to the gate).
5. **Gate** — all four axes beat the old tool, held-out ≥98% → write `onay/token_rea_<tool>.py`.
6. **Approval script** — pattern: `--kuru` (dry-run plan, default) · `uygula` (copy the old config aside, then change it) · `--geri` (put the copy back). Idempotent; byte writes (no CRLF conversion); a test next to it. Applying is the owner's decision.
7. **Apply + verify** — apply on both sides: Claude Code (approval script → `~/.claude`) and Desktop/claude.ai (zip under `dist/`, `tools/skill-paket/zip_denetle.py` clean, files the skill needs inside the zip, no local paths). Verify end to end with a real task and measure real saving only on work done after the apply time.

## Rules

- Installed tools are never removed or pruned; the own version wins by A/B or it stays an option.
- No paid calls; every measurement has a numeric call ceiling.
- Order of cheapness for work: script → free cloud pool → Haiku → Sonnet → Opus.
- Report: commit · tools measured · numbers per axis · deviations. ≤15 lines.
