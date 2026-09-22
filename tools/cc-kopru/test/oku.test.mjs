/** KURULUM-11m-A K3 — `oku`: iskelet · sembol · aralik, deny kapısı, bayat graf. */
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { ARALIK_TAVAN, aralik, iskelet, oku, sembol } from "../oku.mjs";

const KOK = path.resolve(path.dirname(new URL(import.meta.url).pathname.slice(1)), "..", "..", "..");

/** Kendi grafını taşıyan geçici proje: gerçek graph.json'a bağlı kalmadan sınanır. */
function sahteProje({ bayat = false } = {}) {
  const kok = fs.mkdtempSync(path.join(os.tmpdir(), "oku-"));
  const kaynak = path.join(kok, "src");
  fs.mkdirSync(path.join(kok, "graphify-out"), { recursive: true });
  fs.mkdirSync(kaynak, { recursive: true });
  const dosya = path.join(kaynak, "a.mjs");
  fs.writeFileSync(dosya,
    ["// bir", "export function bir() {", "  return 1;", "}", "",
     "export function iki() {", "  return 2;", "}", ""].join("\n"), "utf8");
  fs.writeFileSync(path.join(kok, "graphify-out", "graph.json"), JSON.stringify({
    nodes: [
      { id: "a_bir", label: "bir()", source_file: "src/a.mjs", source_location: "L2" },
      { id: "a_iki", label: "iki()", source_file: "src/a.mjs", source_location: "L6" },
      { id: "b_x", label: "x()", source_file: "src/b.mjs", source_location: "L1" },
    ],
  }), "utf8");
  if (bayat) {
    const ileri = new Date(Date.now() + 60000);
    fs.utimesSync(dosya, ileri, ileri);
  }
  return { kok, dosya: "src/a.mjs" };
}

test("iskelet: semboller + satırlar, gövde yok", () => {
  const p = sahteProje();
  const c = iskelet(p.kok, p.dosya, []);
  assert.match(c, /src\/a\.mjs · 9 satır · 2 sembol/);
  assert.match(c, /L2\tbir/);
  assert.match(c, /L6\tiki/);
  assert.ok(!c.includes("return 1"), "iskelet gövde basmaz");
});

test("sembol: bitiş satırı graftan gelmiyor, sonraki kardeşin başına kadar okunur", () => {
  const p = sahteProje();
  const c = sembol(p.kok, p.dosya, "bir", []);
  assert.match(c, /L2-5/);
  assert.match(c, /return 1;/);
  assert.ok(!c.includes("return 2"), "sonraki sembolün gövdesi sızmaz");
});

test("sembol: son sembol dosya sonuna kadar okunur", () => {
  const p = sahteProje();
  assert.match(sembol(p.kok, p.dosya, "iki", []), /L6-9/);
});

test("sembol: bilinmeyen ad tahmin etmez, bilinenleri sayar", () => {
  const p = sahteProje();
  assert.match(sembol(p.kok, p.dosya, "yok", []), /Bilinen semboller: bir, iki/);
});

test("aralik: graf gerektirmez ve ARALIK_TAVAN'ı aşmaz", () => {
  const p = sahteProje();
  fs.rmSync(path.join(p.kok, "graphify-out"), { recursive: true, force: true });
  const c = aralik(p.kok, p.dosya, 2, 3, []);
  assert.match(c, /L2-3/);
  assert.ok(!c.includes("return 2"));
  const genis = aralik(p.kok, p.dosya, 1, 99999, []);
  const son = Number(/L1-(\d+)/.exec(genis)[1]);
  assert.ok(son <= ARALIK_TAVAN, `tavan aşıldı: ${son}`);
});

test("graf dosyadan eskiyse iskelet/sembol tahmin etmez", () => {
  const p = sahteProje({ bayat: true });
  assert.throws(() => iskelet(p.kok, p.dosya, []), /graph eski — graphify update \./);
  assert.throws(() => sembol(p.kok, p.dosya, "bir", []), /graph eski — graphify update \./);
  // aralik graf okumaz: bayat grafta da çalışır
  assert.match(aralik(p.kok, p.dosya, 1, 2, []), /L1-2/);
});

test("graphify-out yoksa açık mesaj döner", () => {
  const p = sahteProje();
  fs.rmSync(path.join(p.kok, "graphify-out"), { recursive: true, force: true });
  assert.throws(() => iskelet(p.kok, p.dosya, []), /graphify-out yok/);
});

test("Read deny kapısı her modda dosya okunmadan önce çalışır", () => {
  const p = sahteProje();
  const deny = ["Read(**/src/**)"];
  for (const cagri of [
    () => iskelet(p.kok, p.dosya, deny),
    () => sembol(p.kok, p.dosya, "bir", deny),
    () => aralik(p.kok, p.dosya, 1, 2, deny),
  ]) assert.throws(cagri, /permissions\.deny/);
});

test("oku(): bilinmeyen mod ve eksik ad reddedilir", () => {
  const p = sahteProje();
  assert.throws(() => oku({ kok: p.kok, mod: "baska", dosya: p.dosya, deny: [] }), /bilinmeyen mod/);
  assert.throws(() => oku({ kok: p.kok, mod: "sembol", dosya: p.dosya, deny: [] }), /'ad' zorunlu/);
});

test("gerçek depo: omer-skills .mjs ve .py dosyasında iskelet yeşil", () => {
  const graf = path.join(KOK, "graphify-out", "graph.json");
  if (!fs.existsSync(graf)) return;
  const grafT = fs.statSync(graf).mtimeMs;
  for (const [d, beklenen] of [["tools/cc-kopru/kos.mjs", /komutDenetle/], ["tools/gstack_browse.py", /Oturum/]]) {
    // Dosya graftan yeniyse doğru davranış iskelet değil, bayat uyarısıdır.
    if (fs.statSync(path.join(KOK, d)).mtimeMs > grafT) {
      assert.throws(() => iskelet(KOK, d, []), /graph eski/, d);
      continue;
    }
    assert.match(iskelet(KOK, d, []), beklenen, d);
  }
});
