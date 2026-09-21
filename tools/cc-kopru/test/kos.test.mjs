import { test } from "node:test";
import assert from "node:assert/strict";
import os from "node:os";
import path from "node:path";
import fs from "node:fs";

import { ayarYukle, cwdCoz, komutDenetle, redakte, kirp, kos } from "../kos.mjs";

const AYAR = ayarYukle();

test("allowlist disindaki arac reddedilir", () => {
  assert.throws(() => komutDenetle("curl", ["https://x"], AYAR), /allowlist/i);
});

test("strix hic kosmaz, sebebi Docker", () => {
  assert.throws(() => komutDenetle("strix", ["--version"], AYAR), /Docker yok/);
});

test("altIzin disindaki alt komut reddedilir", () => {
  assert.throws(() => komutDenetle("git", ["push"], AYAR), /alt komut/i);
  assert.throws(() => komutDenetle("dotnet", ["nuget"], AYAR), /alt komut/i);
  assert.throws(() => komutDenetle("headroom", ["proxy"], AYAR), /alt komut/i);
});

test("altIzin icindeki alt komut gecer", () => {
  assert.equal(komutDenetle("git", ["status", "--short"], AYAR).arac, "git");
  assert.equal(komutDenetle("gitleaks", ["version"], AYAR).arac, "gitleaks");
});

test("rtk proxy reddedilir (baska komut kosturur)", () => {
  assert.throws(() => komutDenetle("rtk", ["proxy", "cmd", "/c", "whoami"], AYAR), /alt komut/i);
});

test("altYasak listesi uygulanir", () => {
  assert.throws(() => komutDenetle("semgrep", ["login"], AYAR), /alt komut/i);
  assert.throws(() => komutDenetle("playwright-cli", ["install"], AYAR), /alt komut/i);
});

test("metakarakter iceren arguman reddedilir", () => {
  assert.throws(() => komutDenetle("git", ["log", "a|b"], AYAR), /metakarakter/i);
  assert.throws(() => komutDenetle("git", ["log", "a&b"], AYAR), /metakarakter/i);
  assert.throws(() => komutDenetle("git", ["log", "a>b"], AYAR), /metakarakter/i);
});

test("cwd yalnizca izinli koklerin altinda olabilir", () => {
  assert.equal(cwdCoz("C:/Projeler/omer-skills", AYAR).toLowerCase(),
               path.resolve("C:/Projeler/omer-skills").toLowerCase());
  assert.throws(() => cwdCoz("C:/Windows/System32", AYAR), /cwd/i);
});

test("nokta nokta kacisi cozulup yeniden denetlenir", () => {
  assert.throws(() => cwdCoz("C:/Projeler/../Windows", AYAR), /cwd/i);
});

test("redaksiyon: adinda KEY gecen degiskenin degeri maskelenir", () => {
  process.env.FOO_API_KEY = "sir-degeri-12345";
  try {
    assert.equal(redakte("once sir-degeri-12345 sonra"), "once *** sonra");
  } finally {
    delete process.env.FOO_API_KEY;
  }
});

test("redaksiyon PATH degerini bozmaz (PAT eki degil, segment eslesmesi)", () => {
  const s = "yol: " + process.env.PATH.slice(0, 40);
  assert.equal(redakte(s), s);
});

test("30k tavani: bas 5k + son 25k, tam metin logda", () => {
  const uzun = "a".repeat(1000) + "b".repeat(60000) + "c".repeat(1000);
  const r = kirp(uzun, 30000);
  assert.equal(r.kirpildi, true);
  assert.ok(r.metin.length < 31000);
  assert.ok(r.metin.startsWith("a".repeat(100)));
  assert.ok(r.metin.trimEnd().endsWith("c".repeat(100)));
});

test("tavan altindaki cikti kirpilmaz", () => {
  const r = kirp("kisa", 30000);
  assert.equal(r.kirpildi, false);
  assert.equal(r.metin, "kisa");
});

test("gercek kosu: gitleaks version", async () => {
  const r = await kos({ arac: "gitleaks", args: ["version"], cwd: "C:/Projeler/omer-skills", ayar: AYAR });
  assert.equal(r.kod, 0);
  assert.match(r.cikti, /\d+\.\d+\.\d+/);
});

test("gercek kosu: graphify --version", async () => {
  const r = await kos({ arac: "graphify", args: ["--version"], cwd: "C:/Projeler/omer-skills", ayar: AYAR });
  assert.equal(r.kod, 0);
  assert.match(r.cikti, /\d+\.\d+/);
});

test("timeout surec agacini kapatir", async () => {
  // graphify yerine uzun suren ama izinli bir sey yok; dogrudan icsel kosucu ile olculur
  const t0 = Date.now();
  const r = await kos({
    arac: "git", args: ["log", "--all", "-p"], cwd: "C:/Projeler/omer-skills",
    timeoutSn: 1, ayar: AYAR,
  });
  const gecen = (Date.now() - t0) / 1000;
  assert.ok(gecen < 20, "timeout 1 sn verildi, " + gecen + " sn surdu");
  if (r.sureDoldu) assert.match(r.cikti, /zaman asimi/i);
});

test("tam cikti log dosyasina yazilir", async () => {
  const r = await kos({ arac: "gitleaks", args: ["version"], cwd: "C:/Projeler/omer-skills", ayar: AYAR });
  assert.ok(r.log, "log yolu dondu");
  assert.ok(fs.existsSync(r.log), "log dosyasi var: " + r.log);
  assert.ok(r.log.startsWith(path.join(os.tmpdir(), "cc-kopru")));
});

// --- guvenlik: arguman kacakciligi (push denetimi bulgusu 1) ---

test("git -c ile config kacakciligi reddedilir", () => {
  assert.throws(() => komutDenetle("git", ["-c", "core.pager=calc.exe", "log"], AYAR),
                /alt komut|secenek/i);
});

test("alt komut ILK jeton olmali, bayragin arkasina gizlenemez", () => {
  assert.throws(() => komutDenetle("git", ["-C", "C:/Windows", "status"], AYAR),
                /alt komut|secenek/i);
});

test("tehlikeli git secenekleri reddedilir", () => {
  for (const a of ["--exec-path=C:/x", "--upload-pack=calc", "--git-dir=C:/x", "--config-env=x=y"]) {
    assert.throws(() => komutDenetle("git", ["log", a], AYAR), /secenek/i, a);
  }
});

test("ciplak bilgi bayragi tek basina gecer", () => {
  assert.equal(komutDenetle("semgrep", ["--version"], AYAR).arac, "semgrep");
  assert.equal(komutDenetle("git", ["--version"], AYAR).arac, "git");
});

test("bilgi bayragi baska argumanla birlesemez", () => {
  assert.throws(() => komutDenetle("git", ["--version", "push"], AYAR), /alt komut|secenek/i);
});

// --- 11i-FIX-2: ham argv metakarakteri, hook yeniden yazimi, kaydet govdesi ---
import { yenidenYazimKabul, memGovde, gitleaksOzet, komutSatiri } from "../kos.mjs";

test("noktali virgul de metakarakter: hook'tan ONCE ham argv'de RED", () => {
  assert.throws(() => komutDenetle("git", ["log", "-1;whoami"], AYAR), /metakarakter/i);
  assert.throws(() => komutDenetle("git", ["log", "-1\nwhoami"], AYAR), /metakarakter/i);
  // tek arguman korunur: bosluklu format degeri gecer
  assert.equal(komutDenetle("git", ["log", "-1", "--format=%h %s"], AYAR).args.length, 3);
});

test("hook yeniden yazimi yalniz rtk sarmalamasi ise kabul edilir", () => {
  assert.deepEqual(yenidenYazimKabul(["git", "status"], "rtk git status"),
                   ["rtk", "git", "status"]);
  assert.deepEqual(yenidenYazimKabul(["git", "log", "--format=%h %s"],
                                     komutSatiri("rtk", ["git", "log", "--format=%h %s"])),
                   ["rtk", "git", "log", "--format=%h %s"]);
  // argv sinirini degistiren ya da baska bir sey ekleyen her yazim yok sayilir
  assert.equal(yenidenYazimKabul(["git", "log", "-1"], "rtk git log -1; whoami"), null);
  assert.equal(yenidenYazimKabul(["git", "status"], "whoami"), null);
  assert.equal(yenidenYazimKabul(["git", "status"], "rtk git status --raw"), null);
});

test("kaydet govdesi worker semasina uyar: desktop etiketi metadata'da", () => {
  const g = memGovde("omer-skills", "baslik", "govde");
  assert.deepEqual(Object.keys(g).sort(), ["metadata", "project", "text", "title"]);
  assert.equal(g.metadata.platformSource, "desktop");
  assert.equal(g.source, undefined, "worker 'source' anahtarini reddediyor (strict sema)");
});

test("gitleaks ozeti: sayi + kural adi, bulgu degeri asla basilmaz", () => {
  const sir = "gh" + "p_" + "A".repeat(36);
  const s = gitleaksOzet([{ RuleID: "generic-api-key", Secret: sir, Match: sir }], 1);
  assert.match(s, /YAZILMADI — gitleaks: 1 bulgu \(generic-api-key\)/);
  assert.equal(s.includes(sir), false, "bulgu degeri cikti_ya girmez");
  assert.match(gitleaksOzet(null, 2), /okunamadı \(exit 2\)/);
});
