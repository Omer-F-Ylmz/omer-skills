/**
 * KURULUM-13d K1: köprü katalog ile jev skill aynı fixture'dan aynı skill ad kümesini üretir
 * (tools/jev/tests/veri/skill_agaci.json; Python tarafı test_jev_13d.py).
 */
import { test } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { katalogTopla } from "../hook.mjs";

const FIXTURE = fileURLToPath(new URL("../../jev/tests/veri/skill_agaci.json", import.meta.url));

test("13d K1: ortak fixture — synced + etkin sürüm + marketplace alt kümesi + off + tekil", () => {
  const f = JSON.parse(fs.readFileSync(FIXTURE, "utf8"));
  const ev = fs.mkdtempSync(path.join(os.tmpdir(), "k13d-"));
  for (const [rel, icerik] of Object.entries(f.dosyalar)) {
    fs.mkdirSync(path.dirname(path.join(ev, rel)), { recursive: true });
    fs.writeFileSync(path.join(ev, rel), icerik.replaceAll("{EV}", ev.replaceAll("\\", "/")));
  }
  for (const rel of f.skilller) {
    const ad = path.basename(rel);
    fs.mkdirSync(path.join(ev, rel), { recursive: true });
    fs.writeFileSync(path.join(ev, rel, "SKILL.md"), `---\nname: ${ad}\ndescription: ${ad} açıklama\n---\n`);
  }
  assert.deepEqual(katalogTopla("skill", "", ev).map((x) => x.ad).sort(), f.beklenen);
});
