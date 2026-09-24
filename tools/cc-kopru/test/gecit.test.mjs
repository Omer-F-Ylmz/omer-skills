/**
 * KURULUM-11k K5: kanca geçidi. Desktop'ın mcp-filesystem/mcp-git çağrıları CC
 * araçlarına eşlenip CC'nin kendi hook'larından ve permissions.deny'ından geçer.
 * 3 pin: block-destructive reddi · .cs sonrası dotnet-format · bin/** okuma reddi.
 */
import { test } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { agaciKapat, okumaDeny } from "../kos.mjs";
import { ccArac } from "../gecit.mjs";

const BURASI = path.dirname(fileURLToPath(import.meta.url));
const KOK = path.resolve(BURASI, "..");
const PROJE = "C:/Projeler/omer-skills";

// ---------------------------------------------------------------- permissions.deny · Read
test("okumaDeny: Read kurallari yol uzerinde uygulanir", () => {
  const deny = ["Read(./bin/**)", "Read(**/node_modules/**)", "Bash(rm:*)"];
  assert.throws(() => okumaDeny(`${PROJE}/bin/Debug/x.dll`, deny, PROJE), /permissions\.deny/);
  assert.throws(() => okumaDeny(`${PROJE}/a/node_modules/b/i.js`, deny, PROJE), /permissions\.deny/);
  // ./bin yalniz proje kokunde; alt dizindeki bin/ CC'de de eslesmez
  assert.doesNotThrow(() => okumaDeny(`${PROJE}/src/bin.txt`, deny, PROJE));
  assert.doesNotThrow(() => okumaDeny(`${PROJE}/tools/cc-kopru/kos.mjs`, deny, PROJE));
  // Bash kurali okuma yuzeyinde uygulanmaz
  assert.doesNotThrow(() => okumaDeny(`${PROJE}/rm`, ["Bash(rm:*)"], PROJE));
});

// 11l K4: `./bin/**` proje KOKUNDEN cozuldugu icin ic ice bin dizinleri disarida kaliyordu
// — Corvano.Web/bin/Debug/net10.0/*.runtimeconfig.json gecitten OKUNDU (CC'de de ayni acik).
// Cozum ic ice `bin/Debug` · `bin/Release` · `obj` kaliplari; `**/bin/**` DEGIL, cunku
// gstack skill'inin kendi bin/ komut dizini (13 dizinde 138 dosya) okunamaz olurdu.
const DENY_11L = ["Read(./bin/**)", "Read(./obj/**)", "Read(./graphify-out/**)",
                  "Read(**/node_modules/**)", "Read(**/bin/Debug/**)",
                  "Read(**/bin/Release/**)", "Read(**/obj/**)"];

test("11l K4 · ACIGIN KENDISI: eski dort kural ic ice bin/Debug'i kacirir", () => {
  const eski = ["Read(./bin/**)", "Read(./obj/**)", "Read(./graphify-out/**)",
                "Read(**/node_modules/**)"];
  const icIce = "C:/Projeler/Corvano/Corvano.Web/bin/Debug/net10.0/Corvano.Web.runtimeconfig.json";
  assert.doesNotThrow(() => okumaDeny(icIce, eski, "C:/Projeler/Corvano"),
                      "eski liste bu yolu zaten yakaliyorsa acik yok demektir");
  assert.throws(() => okumaDeny(icIce, DENY_11L, "C:/Projeler/Corvano"), /permissions\.deny/);
});

test("11l K4 · ic ice bin/Debug · bin/Release · obj reddedilir", () => {
  for (const p of [
    "C:/Projeler/Corvano/Corvano.Web/bin/Debug/net10.0/Corvano.Web.runtimeconfig.json",
    "C:/Projeler/Corvano/Corvano.Web/bin/Release/net10.0/Corvano.Web.dll",
    "C:/Projeler/Corvano/Corvano.Web/obj/Debug/net10.0/proje.assets.json",
    `${PROJE}/bin/gizli.txt`,
    `${PROJE}/a/node_modules/b/i.js`,
  ]) assert.throws(() => okumaDeny(p, DENY_11L, PROJE), /permissions\.deny/, p);
});

test("11l K4 · README ve gstack bin komutlari okunmaya devam eder", () => {
  for (const p of [
    `${PROJE}/README.md`,
    `${PROJE}/src/bin.txt`,
    "C:/Users/pc/.claude/skills/gstack/bin/dev-setup",
    "C:/Users/pc/.claude/skills/gstack/browse/bin/gstack-browse",
  ]) assert.doesNotThrow(() => okumaDeny(p, DENY_11L, PROJE), p);
});

// ---------------------------------------------------------------- eşleme
test("ccArac: dosya ve git araclari CC matcher'larina eslenir", () => {
  assert.equal(ccArac("write_file", { path: "a.cs", content: "x" }).matcher, "Write");
  assert.equal(ccArac("edit_file", { path: "a.cs" }).matcher, "Edit");
  assert.equal(ccArac("create_directory", { path: "a" }).matcher, "Write");
  const r = ccArac("read_multiple_files", { paths: ["a.txt", "b.txt"] });
  assert.equal(r.matcher, "Read");
  assert.deepEqual(r.okunan, ["a.txt", "b.txt"]);
  assert.equal(ccArac("git_reset", { repo_path: PROJE, mode: "hard" }).girdi.command,
               "git reset --hard");
  assert.equal(ccArac("git_commit", { repo_path: PROJE, message: "x" }).matcher, "Bash");
  // salt okur git ve bilinmeyen arac eslenmez -> gecit dokunmadan iletir
  assert.equal(ccArac("git_status", { repo_path: PROJE }), null);
  assert.equal(ccArac("list_directory", { path: PROJE }), null);
});

// ---------------------------------------------------------------- uçtan uca geçit
/** Geçidi sahte sunucuyla ayağa kaldırır, istekleri yazar, cevapları toplar. */
function gecitKos(istekler, sn = 90, sunucu = "sahte-mcp.mjs") {
  return new Promise((coz, red) => {
    const p = spawn(process.execPath,
      [path.join(KOK, "gecit.mjs"), "test", "--", process.execPath, path.join(BURASI, "yardim", sunucu)],
      { cwd: KOK, shell: false, windowsHide: true });
    const cevaplar = [];
    let kalan = "", hata = "";
    p.stdout.on("data", (b) => {
      kalan += b.toString("utf8");
      const satirlar = kalan.split("\n");
      kalan = satirlar.pop();
      for (const s of satirlar) if (s.trim()) cevaplar.push(JSON.parse(s));
      if (cevaplar.length >= istekler.length) { p.kill(); coz({ cevaplar, hata }); }
    });
    p.stderr.on("data", (b) => { hata += b.toString("utf8"); });
    p.on("error", red);
    const zam = setTimeout(() => { p.kill(); red(new Error("gecit zaman asimi:\n" + hata)); }, sn * 1000);
    p.on("close", () => { clearTimeout(zam); coz({ cevaplar, hata }); });
    for (const i of istekler) p.stdin.write(JSON.stringify(i) + "\n");
  });
}

const cagri = (id, name, args) => ({
  jsonrpc: "2.0", id, method: "tools/call", params: { name, arguments: args },
});

const yasiyor = (pid) => { try { process.kill(pid, 0); return true; } catch { return false; } };

// FIX-6 K1: Desktop kapaninca stdin EOF gelir; gecit alt sunucunun stdin'ini acik
// tuttugu icin ikisi de sonsuza dek yasiyordu (yetim mcp-filesystem/mcp-git agaclari).
test("FIX-6 · stdin kapaninca gecit alt sunucusuyla birlikte kapanir", async () => {
  const p = spawn(process.execPath,
    [path.join(KOK, "gecit.mjs"), "test", "--", process.execPath, path.join(BURASI, "yardim", "sahte-mcp.mjs")],
    { cwd: KOK, stdio: ["pipe", "ignore", "ignore"], windowsHide: true });
  const kapandi = new Promise((coz) => p.on("close", () => coz(true)));
  p.stdin.end();
  const sonuc = await Promise.race([kapandi, new Promise((coz) => setTimeout(() => coz(false), 10000))]);
  if (!sonuc) agaciKapat(p.pid);
  assert.ok(sonuc, "stdin EOF sonrasi gecit acik kaldi");
});

test("FIX-6 · zaman asiminda gecit agaci teardown'da kapanir", async () => {
  const hata = await gecitKos([cagri(9, "list_directory", { path: PROJE })], 3, "sahte-asili.mjs")
    .then(() => "", (e) => e.message);
  const pid = Number(/ASILI_PID=(\d+)/.exec(hata)?.[1]);
  try {
    assert.match(hata, /zaman asimi/);
    assert.ok(pid, "alt sunucu pid'i yok:\n" + hata);
    assert.equal(yasiyor(pid), false, "alt sunucu teardown sonrasi hala acik");
  } finally {
    if (pid && yasiyor(pid)) process.kill(pid);
  }
});

test("PIN 1 · block-destructive'in engelledigi islem gecitten de reddedilir", async () => {
  const { cevaplar } = await gecitKos([cagri(1, "git_reset", { repo_path: PROJE, mode: "hard" })]);
  const c = cevaplar.find((x) => x.id === 1);
  assert.ok(c, "cevap yok");
  assert.equal(c.result.isError, true);
  assert.match(c.result.content[0].text, /DUR: yıkıcı komut|HOOK REDDETTİ/);
  assert.doesNotMatch(c.result.content[0].text, /SAHTE-TAMAM/, "istek sunucuya iletilmis");
});

test("PIN 2 · .cs yazimindan sonra dotnet-format PostToolUse'u kosar", async () => {
  const { cevaplar, hata } = await gecitKos([
    cagri(2, "write_file", { path: `${PROJE}/yok-11k.cs`, content: "class X {}" }),
  ]);
  const c = cevaplar.find((x) => x.id === 2);
  assert.ok(c, "cevap yok");
  assert.match(JSON.stringify(c.result), /SAHTE-TAMAM/, "izinli cagri iletilmeliydi");
  assert.match(hata, /user-settings\|PostToolUse\|Edit\|Write/, "dotnet-format hook'u kosmadi:\n" + hata);
});

test("PIN 3 · Desktop'tan bin/** okuma permissions.deny geregi reddedilir", async () => {
  const { cevaplar } = await gecitKos([
    cagri(3, "read_text_file", { path: `${PROJE}/bin/gizli.txt` }),
    cagri(4, "read_text_file", { path: `${PROJE}/README.md` }),
  ]);
  const red = cevaplar.find((x) => x.id === 3);
  assert.equal(red.result.isError, true);
  assert.match(red.result.content[0].text, /permissions\.deny/);
  const izin = cevaplar.find((x) => x.id === 4);
  assert.match(JSON.stringify(izin.result), /SAHTE-TAMAM/);
});
