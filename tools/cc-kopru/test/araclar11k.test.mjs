/**
 * KURULUM-11k K2b/K3b/K3c/K4: katalog · durum · oturum_ozeti · otomatik gözlem.
 * Ağ uçları (claude-mem worker) gerçek; hiçbir vaka `claude -p` çağırmaz.
 */
import { test } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { gozlemGovde, statuslineGovde } from "../kos.mjs";
import { aciklamaOku, eklentiKokleri, katalogTopla } from "../hook.mjs";

const SUNUCU = path.join(path.dirname(fileURLToPath(import.meta.url)), "..", "sunucu.mjs");
const PROJE = "C:/Projeler/omer-skills";

function cagir(vakalar, sure = 90000) {
  return new Promise((coz, ret) => {
    const p = spawn(process.execPath, [SUNUCU], { cwd: "C:\\Windows\\System32", shell: false });
    const sonuc = new Map();
    let tampon = "";
    const gonder = (o) => p.stdin.write(JSON.stringify(o) + "\n");
    const zam = setTimeout(() => { p.kill(); ret(new Error("sunucu yanıt vermedi")); }, sure);
    p.stdout.on("data", (b) => {
      tampon += b.toString("utf8");
      let i;
      while ((i = tampon.indexOf("\n")) >= 0) {
        const satir = tampon.slice(0, i).trim();
        tampon = tampon.slice(i + 1);
        if (!satir) continue;
        let m;
        try { m = JSON.parse(satir); } catch { continue; }
        if (m.id === 1) {
          gonder({ jsonrpc: "2.0", method: "notifications/initialized" });
          vakalar.forEach((v, n) => gonder({
            jsonrpc: "2.0", id: n + 2, method: "tools/call",
            params: { name: v.arac, arguments: v.args },
          }));
        } else if (m.id >= 2) {
          sonuc.set(m.id - 2, m.result || m.error);
          if (sonuc.size === vakalar.length) {
            clearTimeout(zam); p.kill();
            coz(vakalar.map((_, n) => sonuc.get(n)));
          }
        }
      }
    });
    gonder({
      jsonrpc: "2.0", id: 1, method: "initialize",
      params: { protocolVersion: "2024-11-05", capabilities: {}, clientInfo: { name: "t", version: "0" } },
    });
  });
}

const govde = (r) => (r?.content || [{}])[0]?.text || "";

// ---------------------------------------------------------------- K3b gövde
test("gozlem govdesi worker semasina uyar: kaynak claude-desktop", () => {
  const g = gozlemGovde("oturum-1", "cc-kopru:komut", { command: "gh --version" },
                        { stdout: "gh 2.0", exitCode: 0 }, PROJE);
  assert.equal(g.contentSessionId, "oturum-1");
  assert.equal(g.tool_name, "cc-kopru:komut");
  assert.equal(g.platformSource, "claude-desktop");
  assert.equal(g.cwd, PROJE);
  assert.deepEqual(Object.keys(g).sort(),
    ["contentSessionId", "cwd", "platformSource", "tool_input", "tool_name", "tool_response"]);
});

// ---------------------------------------------------------------- K4 gövde
test("statusline govdesi yalniz ps1'in okudugu alanlari tasir", () => {
  const g = statuslineGovde({ model: "claude-sonnet-5", girdi: 50000, okunan: 40000 });
  assert.equal(g.model.display_name, "claude-sonnet-5");
  assert.equal(typeof g.context_window.used_percentage, "number");
  assert.equal(Math.round(g.prompt_cache.hit_ratio * 100), 80);
});

test("statusline govdesi ajan hic kosmadiysa null doner", () => {
  assert.equal(statuslineGovde(null), null);
});

// ---------------------------------------------------------------- K2b katalog
test("eklenti kokleri acik plugin'leri bulur", () => {
  const k = eklentiKokleri();
  assert.ok(k.length > 3, "en az birkac acik plugin olmali");
  assert.ok(k.every((x) => x.ad && x.kok));
});

test("katalog skillOverrides'ta off olani elemez degil, eler", () => {
  const hepsi = katalogTopla("skill", "");
  assert.ok(hepsi.length > 10, "skill bulunmali");
  assert.ok(!hepsi.some((s) => s.kapali), "kapali skill listeye girmemeli");
  assert.ok(hepsi.every((s) => s.ad && typeof s.aciklama === "string"));
});

// 11l K3: description bir YAML blok skaleri ise (plugin-dev 3 ajan `|`, ponytail 6 skill
// `>`, dotnet-test 10 ajan) aciklama yerine gostergenin kendisi basiliyordu.
const gecici = () => fs.mkdtempSync(path.join(os.tmpdir(), "cc-kopru-11l-"));

test("aciklamaOku blok skaleri gostergesini degil ilk anlamli satiri alir", () => {
  const d = gecici();
  for (const g of ["|", ">", "|-", ">-", "|+", ">+"]) {
    const p = path.join(d, `s${g.length}${g[0] === "|" ? "b" : "k"}.md`);
    fs.writeFileSync(p, `---\nname: x\ndescription: ${g}\n  Uc ajan uretir.\n`
      + `  Ikinci satir gorunmemeli.\n---\n# govde\n`, "utf8");
    assert.equal(aciklamaOku(p), "Uc ajan uretir.", `gosterge ${g}`);
  }
});

test("aciklamaOku tek satir bicimini bozmaz", () => {
  const p = path.join(gecici(), "t.md");
  fs.writeFileSync(p, `---\nname: x\ndescription: "Tek satir aciklama."\n---\n`, "utf8");
  assert.equal(aciklamaOku(p), "Tek satir aciklama.");
});

test("katalogta artik ciplak blok skaleri gostergesi kalmadi", () => {
  const hepsi = katalogTopla("hepsi", "");
  const bozuk = hepsi.filter((x) => /^[|>][-+]?$/.test(x.aciklama));
  assert.deepEqual(bozuk.map((x) => x.ad), [], "gosterge aciklama olarak basiliyor");
});

test("katalog araci komut · ajan · skill dondurur ve filtreler", async () => {
  const [a, b] = await cagir([
    { arac: "katalog", args: { tur: "ajan" } },
    { arac: "katalog", args: { tur: "skill", ara: "ponytail" } },
  ]);
  assert.notEqual(a.isError, true, govde(a));
  assert.match(govde(a), /ajan/i);
  assert.match(govde(b), /ponytail/i);
});

test("katalog sayi=true yalniz tur basina sayi doner, liste basmaz", async () => {
  const [r] = await cagir([{ arac: "katalog", args: { sayi: true } }]);
  assert.notEqual(r.isError, true, govde(r));
  for (const t of ["komut", "ajan", "skill"]) {
    assert.match(govde(r), new RegExp(`${t}\\s+\\d+`), `${t} sayisi yok: ${govde(r)}`);
  }
  assert.doesNotMatch(govde(r), /^- \[/m, "sayi modunda liste basilmamali");
});

// ---------------------------------------------------------------- K4 durum
test("durum araci statusline satirini ve dort parcayi dondurur", async () => {
  const [r] = await cagir([{ arac: "durum", args: {} }]);
  assert.notEqual(r.isError, true, govde(r));
  for (const bolum of [/statusline/i, /headroom/i, /claude-mem/i, /günlük CC|gunluk CC/i]) {
    assert.match(govde(r), bolum);
  }
  // ajan hic kosmadi -> yapisal sinir yazilir, uydurma yuzde basilmaz
  assert.match(govde(r), /ajan çağrısı yok|ajan cagrisi yok/i);
});

// ---------------------------------------------------------------- K3c oturum özeti
test("oturum_ozeti kuyruk durumunu ve mevcut ozetleri dondurur", async () => {
  const [r] = await cagir([{ arac: "oturum_ozeti", args: { proje: PROJE } }]);
  assert.notEqual(r.isError, true, govde(r));
  assert.match(govde(r), /kuyruk|queue/i);
});
