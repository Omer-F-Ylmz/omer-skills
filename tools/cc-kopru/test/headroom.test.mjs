/**
 * KURULUM-11k K6(b) + 11m-A K4 — çıktı katmanı.
 * >8 KB log/JSON çıktısı `headroom mcp serve` stdio MCP'sine gider; markdown/kod
 * gitmez. Headroom fail-open çalışıyor (router zaman aşımında içeriği aynen
 * döndürüyor), o yüzden asıl pin: kazanç yoksa ham metin döner, şişmiş zarf basılmaz.
 */
import { test } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
const BR = String.fromCharCode(10);

import { LOG_DIZIN, LOG_TAVAN, SIKISTIR_ESIK, ciktiHazirla, ciktiSinifi, kirp, logBudama, logaYaz,
         sikistir } from "../kos.mjs";

const TEKRARLI = Array.from({ length: 900 }, (_, i) =>
  `2026-09-21T23:00:00Z INFO worker-service observation queued id=${i} project=omer-skills status=ok`)
  .join("\n");

/** json sinifi: olcumde %21 kazanan tek sinif (11m-A K4). */
const JSON_GOVDE = JSON.stringify(Array.from({ length: 700 }, (_, i) =>
  ({ i, seviye: "INFO", kaynak: "worker-service", olay: "observation queued",
     proje: "omer-skills", durum: "ok", sure_ms: (i * 7919) % 997 })));

const KARISIK = Array.from({ length: 260 }, (_, i) =>
  `## Bolum ${i}` + BR + BR + `| a${i} | b${i} | c${i} |` + BR + "|---|---|---|" + BR
  + `Kanit ${i}: olcum ${(i * 7919) % 104729} - yol tools/cc-kopru/dosya${i}.mjs - sure ${i}ms.` + BR)
  .join(BR);

// ---------------------------------------------------------------- sınıf kapısı
test("ciktiSinifi: log · json · markdown · kod ayrılır", () => {
  assert.equal(ciktiSinifi(TEKRARLI), "log");
  assert.equal(ciktiSinifi(KARISIK), "markdown");
  assert.equal(ciktiSinifi(JSON.stringify({ a: [1, 2], b: "x" })), "json");
  assert.equal(ciktiSinifi(["import fs from 'node:fs';", "export function a() {}",
                            "const x = 1;", "let y = 2;"].join(BR)), "kod");
  assert.equal(ciktiSinifi(""), "log");
});

test("esik altindaki cikti Headroom'a hic gitmez", async () => {
  const kisa = "x".repeat(SIKISTIR_ESIK - 1);
  assert.equal(await sikistir(kisa), null);
  assert.equal(await ciktiHazirla(kisa, 30000), kisa);
});

test("markdown >8 KB olsa da katmandan gecmez", async () => {
  const c = await ciktiHazirla(KARISIK, 12000);
  assert.ok(!c.includes("[headroom %"), "markdown sikistirilmis");
  assert.ok(c.length <= 12000 + 300 && c.length < KARISIK.length);
});

test("log sinifi katmandan cikti (11m-A K4 olcumu): sikistirilmaz", async () => {
  const c = await ciktiHazirla(TEKRARLI, 30000);
  assert.ok(!c.includes("[headroom %"), "log sikistirilmis");
});

test("ham:true katmani atlar", async () => {
  // ham yalnız KATMANI atlar; tavanda kırpma ayrı bir kapı, tavan bilerek yüksek.
  const c = await ciktiHazirla(JSON_GOVDE, 10_000_000, { ham: true });
  assert.ok(!c.includes("[headroom"), "ham cagrida headroom cagrilmis");
  assert.equal(c, JSON_GOVDE);
});

// ---------------------------------------------------------------- tam çıktı yolu
test("cagiranin log yolu varsa katman yeni dosya acmaz", async () => {
  const uzun = TEKRARLI + BR + "x".repeat(40000);
  const c = await ciktiHazirla(uzun, 12000, { log: "C:/sahte/yol.log" });
  assert.match(c, /^\[(headroom %\d+|headroom yok|kırpıldı) · tam: C:\/sahte\/yol\.log\]/);
}, { timeout: 120000 });

test("kirpilan ciktinin tamami LOG_DIZIN'e yazilir", async () => {
  const uzun = KARISIK + BR + "y".repeat(20000);
  const c = await ciktiHazirla(uzun, 12000);
  const yol = /· tam: (.+)\]/.exec(c)?.[1];
  assert.ok(yol && fs.existsSync(yol), "log dosyasi yok: " + yol);
  assert.equal(fs.readFileSync(yol, "utf8").length, uzun.length);
  fs.rmSync(yol, { force: true });
});

test("logBudama LOG_DIZIN'de son LOG_TAVAN dosyayi birakir", () => {
  fs.mkdirSync(LOG_DIZIN, { recursive: true });
  for (let i = 0; i < 5; i += 1) logaYaz("x", "budama-testi");
  assert.ok(fs.readdirSync(LOG_DIZIN).length >= 5, "log yazilmadi");
  // logaYaz her yazimda LOG_TAVAN ile budar; dizin hicbir zaman tavani asmaz.
  assert.ok(fs.readdirSync(LOG_DIZIN).length <= LOG_TAVAN, "LOG_TAVAN asildi");
  logBudama(2);
  assert.ok(fs.readdirSync(LOG_DIZIN).length <= 2, "budama calismadi");
});

// ---------------------------------------------------------------- canlı headroom
test("json >8 KB sikisir ve ilk satir yuzde + tam yolu tasir", async () => {
  const z = await sikistir(JSON_GOVDE);
  assert.ok(z, "headroom mcp serve cevap vermedi");
  assert.ok(z.original_tokens > z.compressed_tokens,
            `kazanc yok: ${z.original_tokens} -> ${z.compressed_tokens}`);
  const c = await ciktiHazirla(JSON_GOVDE, 30000);
  assert.match(c, /^\[headroom %[\d.]+ · tam: .+\]/);
  const yol = /· tam: (.+)\]/.exec(c)[1];
  assert.equal(fs.readFileSync(yol, "utf8"), JSON_GOVDE, "tam cikti log'da degil");
  fs.rmSync(yol, { force: true });
}, { timeout: 120000 });

test("router tavani asilirsa kirpmaya duser", async () => {
  assert.deepEqual(await sikistir(TEKRARLI, 1), { sebep: "zaman aşımı" });
});

/**
 * 11m-A-FIX-4 K3: sebep yutulmaz. Dördü de sahte sıkıştırıcıyla sınanır — gerçek
 * headroom'a gidilmez. Kök neden vekil uyumsuzluğuydu (MCP 8787, vekil 6767):
 * headroom fail-open dönüp içeriği aynen veriyordu, başlık "headroom yok" diyordu.
 */
for (const [sebep, sahte] of [
  ["zaman aşımı", async () => ({ sebep: "zaman aşımı" })],
  ["parse", async () => ({ sebep: "parse" })],
  ["bağlantı", async () => ({ sebep: "bağlantı" })],
  ["bağlantı", async (s) => ({ compressed: s, original_tokens: 10, compressed_tokens: 10,
                               proxy: { status: "unreachable" } })],
  ["kazançsız", async (s) => ({ compressed: s, original_tokens: 10, compressed_tokens: 10 })],
]) {
  test(`sebep basliga girer: ${sebep}`, async () => {
    const c = await ciktiHazirla(JSON_GOVDE, 12000,
                                 { log: "C:/sahte/yol.log", sikistirici: sahte });
    assert.ok(c.startsWith(`[headroom yok: ${sebep} · tam: C:/sahte/yol.log]`), c.slice(0, 70));
  });
}


test("sikistirma basarisizsa ham cikti + uyari satiri doner", async () => {
  // sikistir zaman asiminda null doner; ciktiHazirla uydurma yuzde basmamali.
  const uzun = JSON_GOVDE;
  const c = await ciktiHazirla(uzun, 30000, { log: "C:/sahte/yol.log" });
  assert.ok(c.startsWith("[headroom %") || c.startsWith("[headroom yok · tam: "), c.slice(0, 60));
  assert.ok(!/%NaN|%undefined/.test(c));
}, { timeout: 120000 });

// ------------------------------------------------- 11m-A-FIX K1/K2: çift katman
/**
 * rtk yeniden yazımı JSON gövdesini kendi tam-satır başlık/altlığıyla sarar. Köprünün
 * `[hook yeniden yazdı] …` satırı gövdeye girmiyor (sunucu onu `bas`'ta tutuyor);
 * sınıflamayı bozan rtk'nin kendi satırları ve köprünün kırpma etiketi.
 */
const RTK_JSON = "[+1 hidden: rtk recall 6d55025d6531]" + BR + JSON_GOVDE + BR
  + "[216 words compressed to 176 (from 28 source lines). Retrieve more: hash=e28eb3106]";

test("K1: rtk baslik/altligi ve kopru etiketi sinifi bozmaz", () => {
  assert.equal(ciktiSinifi(RTK_JSON), "json");
  assert.equal(ciktiSinifi("[kırpıldı · tam: C:/x.log]" + BR + JSON_GOVDE), "json");
  // ayiklama yalnizca tam-satir etiketlerini alir; govde sinifi degismez
  assert.equal(ciktiSinifi(TEKRARLI), "log");
  assert.equal(ciktiSinifi(KARISIK), "markdown");
});

test("K1: rtk footer'li 20K+ JSON katmandan gecer, yol cikti da tek kez", async () => {
  assert.ok(RTK_JSON.length > 20000, "fixture 20K altinda");
  const c = await ciktiHazirla(RTK_JSON, 30000, { log: "C:/sahte/yol.log" });
  assert.match(c, /^\[headroom %[\d.]+ · tam: C:\/sahte\/yol\.log\]/);
  assert.equal((c.match(/· tam: /g) || []).length, 1, "yol birden cok kez basildi");
  assert.match(c, /Retrieve more: hash=e28eb3106\]$/, "rtk recall altligi dustu");
}, { timeout: 120000 });

test("K2: kirp ciktisi etiket dahil tavani asmaz", () => {
  const uzun = "a".repeat(1000) + "b".repeat(60000) + "c".repeat(1000);
  for (const tavan of [200, 2000, 10000, 30000]) {
    const r = kirp(uzun, tavan);
    assert.equal(r.kirpildi, true);
    assert.ok(r.metin.length <= tavan, `tavan ${tavan} -> ${r.metin.length}`);
  }
});

test("K2: ciktiHazirla'nin kirpilmis ciktisi etiket dahil tavani asmaz", async () => {
  const uzun = TEKRARLI + BR + "x".repeat(40000);
  for (const tavan of [10000, 12000]) {
    const c = await ciktiHazirla(uzun, tavan, { log: "C:/sahte/yol.log" });
    assert.ok(c.length <= tavan, `tavan ${tavan} -> ${c.length}`);
  }
});
