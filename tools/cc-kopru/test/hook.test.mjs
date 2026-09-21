import { test } from "node:test";
import assert from "node:assert/strict";

import { matcherEslesir, hookTanimlari, hookKos, hookKaynaklari } from "../hook.mjs";

/** node -e ile Windows'ta kosan sahte hook uretir. */
const sahte = (govde) => ({ type: "command", command: `node -e "${govde.replace(/"/g, '\\"')}"` });

const kaynak = (olay, matcher, hook, ek = {}) => [{
  ad: "sahte",
  json: { hooks: { [olay]: [{ matcher, hooks: [{ ...hook, ...ek }] }] } },
  kok: "C:/sahte-eklenti",
}];

test("matcher regex olarak uygulanir", () => {
  assert.equal(matcherEslesir("Bash|PowerShell", "Bash"), true);
  assert.equal(matcherEslesir("Bash|PowerShell", "PowerShell"), true);
  assert.equal(matcherEslesir("Bash", "PowerShell"), false);
  assert.equal(matcherEslesir("Edit|Write", "Bash"), false);
  assert.equal(matcherEslesir(undefined, "Bash"), true, "matcher yoksa hepsi eslesir");
  assert.equal(matcherEslesir("*", "Bash"), true);
});

test("exit 2 reddi, sebep stderr'den okunur", async () => {
  const t = hookTanimlari(kaynak("PreToolUse", "Bash",
    sahte("process.stderr.write('DUR: olmaz');process.exit(2)")), []);
  const r = await hookKos(t, { hook_event_name: "PreToolUse", tool_name: "Bash", tool_input: { command: "x" } });
  assert.equal(r.karar, "red");
  assert.match(r.sebep, /DUR: olmaz/);
});

test("permissionDecision deny reddi", async () => {
  const govde = "process.stdout.write(JSON.stringify({hookSpecificOutput:{hookEventName:'PreToolUse',permissionDecision:'deny',permissionDecisionReason:'yasak'}}))";
  const t = hookTanimlari(kaynak("PreToolUse", "Bash", sahte(govde)), []);
  const r = await hookKos(t, { hook_event_name: "PreToolUse", tool_name: "Bash", tool_input: { command: "x" } });
  assert.equal(r.karar, "red");
  assert.match(r.sebep, /yasak/);
});

test("updatedInput komutu yeniden yazar", async () => {
  const govde = "process.stdout.write(JSON.stringify({hookSpecificOutput:{hookEventName:'PreToolUse',updatedInput:{command:'rtk git status'}}}))";
  const t = hookTanimlari(kaynak("PreToolUse", "Bash", sahte(govde)), []);
  const r = await hookKos(t, { hook_event_name: "PreToolUse", tool_name: "Bash", tool_input: { command: "git status" } });
  assert.equal(r.karar, "izin");
  assert.equal(r.girdi.command, "rtk git status");
});

test("additionalContext toplanir", async () => {
  const govde = "process.stdout.write(JSON.stringify({hookSpecificOutput:{hookEventName:'PreToolUse',additionalContext:'ek bilgi'}}))";
  const t = hookTanimlari(kaynak("PreToolUse", "Bash", sahte(govde)), []);
  const r = await hookKos(t, { hook_event_name: "PreToolUse", tool_name: "Bash", tool_input: { command: "x" } });
  assert.equal(r.karar, "izin");
  assert.match(r.ekBaglam, /ek bilgi/);
});

test("timeout'u asan hook oturumu kilitlemez", async () => {
  const t = hookTanimlari(kaynak("PreToolUse", "Bash",
    sahte("setTimeout(()=>{},60000)"), { timeout: 1 }), []);
  const t0 = Date.now();
  const r = await hookKos(t, { hook_event_name: "PreToolUse", tool_name: "Bash", tool_input: { command: "x" } });
  assert.ok((Date.now() - t0) / 1000 < 15, "hook timeout'ta kesildi");
  assert.equal(r.karar, "izin", "timeout reddetmez, atlanir");
});

test("CLAUDE_PLUGIN_ROOT eklentinin kokune cozulur", async () => {
  const govde = "process.stdout.write(JSON.stringify({hookSpecificOutput:{hookEventName:'PreToolUse',additionalContext:process.env.CLAUDE_PLUGIN_ROOT}}))";
  const t = hookTanimlari(kaynak("PreToolUse", "Bash", sahte(govde)), []);
  const r = await hookKos(t, { hook_event_name: "PreToolUse", tool_name: "Bash", tool_input: { command: "x" } });
  assert.match(r.ekBaglam, /sahte-eklenti/);
});

test("kapaliHooklar listesindeki hook kosmaz", async () => {
  const k = kaynak("PreToolUse", "Bash", sahte("process.stderr.write('DUR');process.exit(2)"));
  const t = hookTanimlari(k, ["sahte|PreToolUse|Bash"]);
  assert.equal(t.length, 0);
  const r = await hookKos(t, { hook_event_name: "PreToolUse", tool_name: "Bash", tool_input: { command: "x" } });
  assert.equal(r.karar, "izin");
});

test("gercek CC hook'lari okunur ve block-destructive listede", () => {
  const t = hookTanimlari(hookKaynaklari("C:/Projeler/omer-skills"), []);
  assert.ok(t.length >= 4, "en az 4 hook tanimi bulundu, bulunan: " + t.length);
  assert.ok(t.some((h) => /block-destructive/.test(h.komut)), "block-destructive tanimi var");
  assert.ok(t.some((h) => /rtk/.test(h.komut)), "rtk hook tanimi var");
});

test("gercek block-destructive surec-adla-oldurmeyi reddeder", async () => {
  const t = hookTanimlari(hookKaynaklari("C:/Projeler/omer-skills"), [])
    .filter((h) => /block-destructive/.test(h.komut));
  assert.equal(t.length, 1);
  const r = await hookKos(t, {
    hook_event_name: "PreToolUse", tool_name: "Bash",
    tool_input: { command: "task" + "kill /IM kopru-yok-test.exe" },
  });
  assert.equal(r.karar, "red");
  assert.match(r.sebep, /PID|adla/i);
});

test("gercek rtk hook'u git status'u yeniden yazar", async () => {
  const t = hookTanimlari(hookKaynaklari("C:/Projeler/omer-skills"), [])
    .filter((h) => /rtk/.test(h.komut) && matcherEslesir(h.matcher, "Bash"));
  assert.ok(t.length >= 1);
  const r = await hookKos(t, {
    hook_event_name: "PreToolUse", tool_name: "Bash",
    tool_input: { command: "git status", description: "t" },
  });
  assert.equal(r.karar, "izin");
  assert.match(r.girdi.command, /^rtk git status/);
});

// --- guvenlik: ajan argv kacakciligi (push denetimi bulgusu 2) ---
import { ajanAlanDenetle } from "../kos.mjs";

test("ajan alanlari izin atlama bayragi tasiyamaz", () => {
  assert.throws(() => ajanAlanDenetle("ajan_adi", "--dangerously-skip-permissions"), /ajan_adi/);
  assert.throws(() => ajanAlanDenetle("devam_id", "--permission-mode"), /devam_id/);
  assert.throws(() => ajanAlanDenetle("model", "-p"), /model/);
  assert.throws(() => ajanAlanDenetle("model", "sonnet bypassPermissions"), /model/);
});

test("normal ajan alanlari gecer", () => {
  assert.equal(ajanAlanDenetle("model", "sonnet"), "sonnet");
  assert.equal(ajanAlanDenetle("ajan_adi", "code-reviewer"), "code-reviewer");
  assert.equal(ajanAlanDenetle("devam_id", "e03c93eb-1d0d-48a2-8df4-a2c4f1e37fb0"),
               "e03c93eb-1d0d-48a2-8df4-a2c4f1e37fb0");
});
