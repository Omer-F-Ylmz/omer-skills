import { test } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

import { OMNI_COMBO, OMNI_URL, ajanOrtami, bayrakYaz, limitTuru, omniAktif, sifirlanma } from "../omniroute.mjs";

// OMNIROUTE-1: haftalık plan limiti → yerel OmniRoute; anahtar değeri hiçbir çıktıda görünmez.
const SAHTE = "or-sahte-anahtar-1234567890";
const oku = (ad) => ({ OMNIROUTE_KEY: SAHTE, ANTHROPIC_API_KEY_AJAN: "sk-ajan-sahte-0987654321" })[ad];
const taban = { PATH: "x", ANTHROPIC_API_KEY: "sk-oturum-sahte" };

test("bayrak yok → env dokunulmaz", () => {
  const { env } = ajanOrtami(taban, { apiKredi: false, omni: false, oku });
  assert.deepEqual(env, taban);
});

test("omniroute bayrağı → BASE_URL yerel, kimlik Bearer, API anahtarı çıkar, model adları combo'ya", () => {
  const { env, sir } = ajanOrtami(taban, { apiKredi: false, omni: true, oku });
  assert.equal(env.ANTHROPIC_BASE_URL, OMNI_URL);
  assert.equal(env.ANTHROPIC_AUTH_TOKEN, SAHTE);
  assert.equal(env.KOPRU_OMNIROUTE, "1");
  assert.equal("ANTHROPIC_API_KEY" in env, false);
  for (const m of ["OPUS", "SONNET", "HAIKU"]) assert.equal(env[`ANTHROPIC_DEFAULT_${m}_MODEL`], OMNI_COMBO);
  assert.equal(sir, SAHTE);  // çağıran redaksiyon kümesine ekler
  assert.equal(taban.ANTHROPIC_API_KEY, "sk-oturum-sahte");  // taban değişmez
});

test("omniroute anahtarı yoksa env dokunulmaz, eksik adı döner (değer değil)", () => {
  const r = ajanOrtami(taban, { apiKredi: false, omni: true, oku: () => undefined });
  assert.deepEqual(r.env, taban);
  assert.equal(r.eksik, "OMNIROUTE_KEY");
});

// Metinler: 5 saatlik — 12 Eki KALİTE-3-HIZ günlüğünden (bellek notu); haftalık — CC ikilisi şablonu.
const BES = "You've hit your session limit · resets 11:40pm (Europe/Istanbul)";
const HAFTA = "You've hit your weekly limit · resets Oct 16, 5am (Europe/Istanbul)";

test("haftalık ile 5 saatlik limit ayrı tanınır; sıradan metin limit değil", () => {
  assert.equal(limitTuru(HAFTA), "haftalik");
  assert.equal(limitTuru(JSON.stringify({ result: HAFTA, is_error: true })), "haftalik");
  assert.equal(limitTuru(BES), "5saat");
  assert.equal(limitTuru("weekly rapor yazıldı; session limit konusu"), null);
  assert.equal(limitTuru(""), null);
});

test("sıfırlanma zamanı: tarihli ve yalnız saatli", () => {
  const simdi = new Date(2026, 9, 13, 6, 0);
  assert.deepEqual(sifirlanma(HAFTA, simdi), new Date(2026, 9, 16, 5, 0));
  assert.deepEqual(sifirlanma(BES, simdi), new Date(2026, 9, 13, 23, 40));
  assert.deepEqual(sifirlanma("resets 5am", simdi), new Date(2026, 9, 14, 5, 0));  // geçtiyse yarın
  assert.equal(sifirlanma("limit yok", simdi), null);
});

test("bayrak: sıfırlanma geçmeden açık, geçince kendiliğinden kalkar; bitişsiz bayrak kalıcı", () => {
  const yol = path.join(fs.mkdtempSync(path.join(os.tmpdir(), "omni-")), "omniroute.ac");
  assert.equal(omniAktif(yol), false);
  const simdi = new Date(2026, 9, 13, 6, 0);
  bayrakYaz(yol, sifirlanma(HAFTA, simdi), simdi);
  assert.equal(fs.readFileSync(yol, "utf8").includes(SAHTE), false);
  assert.equal(omniAktif(yol, new Date(2026, 9, 15, 12, 0)), true);
  assert.equal(omniAktif(yol, new Date(2026, 9, 16, 5, 1)), false);
  assert.equal(fs.existsSync(yol), false);
  fs.writeFileSync(yol, "elle açıldı\n");
  assert.equal(omniAktif(yol, new Date(2030, 0, 1)), true);
});

test("api-kredi ile birlikte → api-kredi kazanır, omniroute uygulanmaz", () => {
  const { env } = ajanOrtami(taban, { apiKredi: true, omni: true, oku });
  assert.equal(env.ANTHROPIC_API_KEY, "sk-ajan-sahte-0987654321");
  assert.equal(env.ANTHROPIC_BASE_URL, undefined);
  assert.equal(env.KOPRU_OMNIROUTE, undefined);
});
