import { test } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { ayarYukle, aracAdlari, cocukOrtam, komutDenetle, kos } from "../kos.mjs";

// 13c K0: Desktop MCP süreci kısıtlı env ile başlar; jev anahtarı yalnız jev'e gider.
const AYAR = ayarYukle();
const SAHTE = "sahte-" + "d3g3r".repeat(4);
const ADLAR = ["TYPESAFE_API_KEY", "OPENROUTER_API_KEY", "JEV_MCP_TOKEN"];
const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..", "..");

test("envGecir yalniz tanimli adlari gecirir", () => {
  assert.deepEqual(AYAR.izinli.jev.envGecir, ADLAR);
  const okunan = [];
  const e = cocukOrtam("jev", AYAR, { PATH: "p" }, (ad) => { okunan.push(ad); return SAHTE; });
  assert.deepEqual(okunan.sort(), [...ADLAR].sort());
  assert.deepEqual(Object.keys(e).filter((k) => e[k] === SAHTE).sort(), [...ADLAR].sort());
  assert.equal(e.PATH, "p");
});

test("jev disi aracta anahtar yok (surec env'inde olsa bile)", () => {
  const taban = Object.fromEntries([...ADLAR, "PATH"].map((k) => [k, SAHTE]));
  for (const arac of ["git", "node", "python", "gitleaks"]) {
    const e = cocukOrtam(arac, AYAR, taban, () => SAHTE);
    for (const ad of ADLAR) assert.equal(e[ad], undefined, `${arac} ${ad}`);
    assert.equal(e.PATH, SAHTE);
  }
});

test("gecirilen deger kopru gunlugunde yok", async () => {
  const ayar = { ...AYAR, izinli: { ...AYAR.izinli, node: { ...AYAR.izinli.node, envGecir: ["JEV_TEST_DEGER"] } } };
  const r = await kos({ arac: "node", args: ["-e", "console.log('d=' + process.env.JEV_TEST_DEGER)"], cwd: REPO,
    ayar, denetimAtla: true, kullaniciOku: (ad) => (ad === "JEV_TEST_DEGER" ? SAHTE : undefined) });
  const gunluk = fs.readFileSync(r.log, "utf8");
  assert.match(gunluk, /d=\*\*\*/);
  assert.ok(!gunluk.includes(SAHTE) && !r.cikti.includes(SAHTE));
});

test("komut enum'unda _ onekli not anahtari yok", () => {
  const adlar = aracAdlari(AYAR);
  assert.ok(adlar.includes("jev") && adlar.every((a) => !a.startsWith("_")));
  assert.throws(() => komutDenetle("_not11k", [], AYAR), /allowlist/);
});

test("video: altIzin'de whisper yok, envGecir jev ile ayni", () => {
  assert.deepEqual(AYAR.izinli.video.altIzin, ["ozet", "suz", "sor", "kare", "temizle", "oku", "adlar", "rapor-denetle", "izle", "paket", "durum", "bilgi"]);  // 12b: kayit/toplu yalniz CC; 12c: izle, paket; 15: durum, bilgi
  assert.deepEqual(AYAR.izinli.video.envGecir, ADLAR);
  for (const a of [["whisper", "x"], ["--whisper", "x"]]) assert.throws(() => komutDenetle("video", a, AYAR));
  komutDenetle("video", ["suz", "yp7gg8cG5wc", "--istek-tavan", "30"], AYAR);
  const e = cocukOrtam("video", AYAR, { PATH: "p" }, () => SAHTE);
  assert.deepEqual(Object.keys(e).filter((k) => e[k] === SAHTE).sort(), [...ADLAR].sort());
});
