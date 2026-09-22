/**
 * KURULUM-11k K6(b): >8 KB çıktı `headroom mcp serve` stdio MCP'sine gider.
 * Headroom fail-open çalışıyor (router zaman aşımında içeriği aynen döndürüyor),
 * o yüzden asıl pin: kazanç yoksa ham metin kırpılır, şişmiş zarf basılmaz.
 */
import { test } from "node:test";
import assert from "node:assert/strict";
const BR = String.fromCharCode(10);

import { SIKISTIR_ESIK, TEKRAR_ESIK, ciktiHazirla, sikistir, tekrarOrani } from "../kos.mjs";

const TEKRARLI = Array.from({ length: 900 }, (_, i) =>
  `2026-09-21T23:00:00Z INFO worker-service observation queued id=${i} project=omer-skills status=ok`)
  .join("\n");

test("esik altindaki cikti Headroom'a hic gitmez", async () => {
  const kisa = "x".repeat(SIKISTIR_ESIK - 1);
  assert.equal(await sikistir(kisa), null);
  assert.equal(await ciktiHazirla(kisa, 30000), kisa);
});

test("tekrarli >8 KB cikti sikisir ve geri alma hash'i basilir", async () => {
  const z = await sikistir(TEKRARLI);
  assert.ok(z, "headroom mcp serve cevap vermedi");
  assert.ok(z.original_tokens > z.compressed_tokens,
            `kazanc yok: ${z.original_tokens} -> ${z.compressed_tokens}`);
  const c = await ciktiHazirla(TEKRARLI, 30000);
  assert.match(c, /\[headroom\] \d+ → \d+ jeton/);
  assert.match(c, /headroom_retrieve hash=[a-z0-9]+/i);
}, { timeout: 120000 });

test("kazanc yoksa ham metin kirpilir (fail-open zarfi basilmaz)", async () => {
  // karisik markdown'da router zaman asimina dusup PASSTHROUGH veriyor (11k K6b
  // olcumu: 11755 -> 11754 jeton). Girdi testte uretilir: repo dosyasina bagimli degil.
  const doc = Array.from({ length: 260 }, (_, i) =>
    `## Bolum ${i}` + BR + BR + `| a${i} | b${i} | c${i} |` + BR + "|---|---|---|" + BR
    + `Kanit ${i}: olcum ${(i * 7919) % 104729} - yol tools/cc-kopru/dosya${i}.mjs - sure ${i}ms.` + BR)
    .join(BR);
  const c = await ciktiHazirla(doc, 12000);
  if (c.includes("[headroom]")) return;            // gercekten sikistiysa da dogru
  assert.ok(c.length <= 12000 + 200, "kirpma tavani asildi: " + c.length);
  assert.ok(c.length < doc.length, "cikti hamdan buyuk olmamali");
}, { timeout: 120000 });

/**
 * KURULUM-11l K7 — yönlendirme kapısı. Ölçüm (bu dalga, aynı gövdeler):
 * tekrarlı log 3-gram tekrar 0,624 · 6,3 sn · 27006→18915 jeton (%30 kazanç);
 * karışık markdown 0,047 · 4,1 sn · 13784→1834 ama KAYIPLI — `## Bolum` başlıkları ve
 * `Kanit …` ölçüm satırları çıktıda hiç yok, yalnız tablo satırları CSV'ye dönüyor.
 * Bu yüzden kapı "kazanç" değil "içerik kaybı" gerekçesiyle duruyor.
 */
const KARISIK = Array.from({ length: 260 }, (_, i) =>
  `## Bolum ${i}` + BR + BR + `| a${i} | b${i} | c${i} |` + BR + "|---|---|---|" + BR
  + `Kanit ${i}: olcum ${(i * 7919) % 104729} - yol tools/cc-kopru/dosya${i}.mjs - sure ${i}ms.` + BR)
  .join(BR);

test("tekrar orani kalibrasyonu: tekrarli >= esik > karisik", () => {
  assert.ok(tekrarOrani(TEKRARLI) >= TEKRAR_ESIK, "tekrarli: " + tekrarOrani(TEKRARLI));
  assert.ok(tekrarOrani(KARISIK) < TEKRAR_ESIK, "karisik: " + tekrarOrani(KARISIK));
});

test("karisik markdown headroom'a hic gitmez, dogrudan kirpilir", async () => {
  assert.equal(await sikistir(KARISIK), null);
  const c = await ciktiHazirla(KARISIK, 12000);
  assert.ok(!c.includes("[headroom]"), "headroom cagrilmis");
  assert.ok(c.length <= 12000 + 200 && c.length < KARISIK.length);
});

test("router tavani asilirsa kirpmaya duser", async () => {
  assert.equal(await sikistir(TEKRARLI, 1), null);
});
