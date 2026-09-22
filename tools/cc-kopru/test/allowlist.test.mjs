/**
 * KURULUM-11k K1: genişleyen allowlist (gh · vercel · bun · ffmpeg · npm · npx · uv
 * · node · python) ve permissions.deny köprüde.
 * Her yasak için bir RED pini, her araç için bir izinli örnek.
 */
import { test } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

import { ayarYukle, denyDenetle, komutDenetle, kos, yolBul } from "../kos.mjs";

const AYAR = ayarYukle();
const red = (arac, args) => assert.throws(() => komutDenetle(arac, args, AYAR),
  undefined, `${arac} ${args.join(" ")} reddedilmeliydi`);
const gecer = (arac, args) => assert.doesNotThrow(() => komutDenetle(arac, args, AYAR),
  `${arac} ${args.join(" ")} geçmeliydi`);

// ---------------------------------------------------------------- yolBul
test("yolBul .cmd/.exe secer, uzantisiz POSIX shim'i degil", () => {
  // `where npm` once uzantisiz sh betigini donduruyor; onu spawn etmek ENOENT verir.
  for (const arac of ["npm", "node", "gh"]) {
    const y = yolBul(arac);
    assert.ok(y, arac + " bulunamadi");
    assert.match(y, /\.(exe|cmd|bat|com)$/i, `${arac} -> ${y}`);
  }
});

// ---------------------------------------------------------------- gh
test("gh: sir basan ve geri donussuz alt komutlar reddedilir", () => {
  for (const args of [["auth", "token"], ["auth", "status", "--show-token"],
    ["repo", "delete", "x/y"], ["secret", "list"], ["ssh-key", "list"],
    ["gpg-key", "list"], ["extension", "install", "x/y"],
    ["repo", "archive", "x/y"], ["repo", "rename", "z"],
    ["repo", "edit", "--visibility", "public"]]) red("gh", args);
});

test("gh api yalniz okuma: metot ve alan yazimi reddedilir", () => {
  red("gh", ["api", "-X", "DELETE", "repos/x/y"]);
  red("gh", ["api", "--method", "POST", "repos/x/y"]);
  red("gh", ["api", "repos/x/y", "-f", "name=z"]);
  red("gh", ["api", "repos/x/y", "--raw-field", "name=z"]);
  gecer("gh", ["api", "repos/x/y"]);
  gecer("gh", ["api", "-X", "GET", "repos/x/y"]);
});

test("gh izinli ornek", () => gecer("gh", ["--version"]));

// ---------------------------------------------------------------- vercel
test("vercel: env okuma, silme ve yayin gecisleri reddedilir", () => {
  for (const args of [["env", "pull"], ["env", "ls"], ["remove", "x"],
    ["promote", "x"], ["alias", "x", "y"], ["rollback"],
    ["deploy", "--prod"], []]) red("vercel", args);
});

test("vercel izinli ornek", () => gecer("vercel", ["--version"]));

// ---------------------------------------------------------------- npm · npx
test("npm: yayin, kimlik ve jeton basan alt komutlar reddedilir", () => {
  for (const args of [["publish"], ["unpublish", "x"], ["token", "list"],
    ["login"], ["adduser"], ["owner", "ls", "x"], ["access", "list"],
    ["config", "get", "//registry.npmjs.org/:_authToken"],
    ["exec", "cowsay"], ["x", "cowsay"], ["init", "vite"]]) red("npm", args);
});

test("npm izinli ornek", () => gecer("npm", ["--version"]));

test("npx yalniz --no ile kosar: --no'suz uzak paket indirilir", () => {
  // npm 11.17 docs/content/commands/npm-exec.md:28-29 — istem `--yes` ya da `--no` ile
  // bastirilir, ve stdin TTY DEGILSE `--yes` VARSAYILIR. Koprude TTY yok: bayraksiz npx
  // uzak paketi sessizce indirip kosar. `--no-install` ayni belgede (satir 298) deprecated.
  red("npx", ["cowsay"]);
  red("npx", ["--yes", "cowsay"]);
  red("npx", ["--no-install", "cowsay"]);
  gecer("npx", ["--no", "node-which"]);
});

// 11l K2: `npx --no pixeljury --version` npm'in KENDI surumunu (11.17.0) doner, paket
// kosmaz; `npx --no -- pixeljury --version` 0.1.5 doner. Ayni sonuc rtk'siz dogrudan
// cagrida da olustugu icin kok neden npm'in npx ayristirmasi, rtk degil: `--` olmadan
// `--version` npx'in kendi bayragi sayiliyor. Kopru gerekli bayraktan sonra `--` ekler.
const argsOf = (arac, args) => komutDenetle(arac, args, AYAR).args;

test("npx/bunx: gerekli bayraktan sonra `--` eklenir", () => {
  assert.deepEqual(argsOf("npx", ["--no", "pixeljury", "--version"]),
                   ["--no", "--", "pixeljury", "--version"]);
  assert.deepEqual(argsOf("bunx", ["--no-install", "cowsay"]),
                   ["--no-install", "--", "cowsay"]);
});

test("npx: `--` zaten varsa ikinci kez eklenmez, --no'suz RED surer", () => {
  assert.deepEqual(argsOf("npx", ["--no", "--", "pixeljury", "--version"]),
                   ["--no", "--", "pixeljury", "--version"]);
  red("npx", ["pixeljury", "--version"]);
});

test("`--` eklemesi npx disindaki araclara bulasmaz", () => {
  assert.deepEqual(argsOf("gh", ["repo", "view"]), ["repo", "view"]);
  assert.deepEqual(argsOf("uvx", ["--offline", "ruff"]), ["--offline", "ruff"]);
});

// ---------------------------------------------------------------- bun · bunx
test("bun: yayin ve indirip-kosturma yollari reddedilir", () => {
  for (const args of [["publish"], ["x", "cowsay"], ["create", "vite"],
    ["-e", "console.log(1)"]]) red("bun", args);
});

test("bunx yalniz kurulu paket (--no-install zorunlu)", () => {
  red("bunx", ["cowsay"]);
  gecer("bunx", ["--no-install", "cowsay"]);
});

test("bun izinli ornek", () => gecer("bun", ["--version"]));

// ---------------------------------------------------------------- uv · uvx
test("uv: tool run/install ve satir ici kod reddedilir", () => {
  for (const args of [["tool", "run", "cowsay"], ["tool", "install", "cowsay"],
    ["run", "python", "-c", "print(1)"]]) red("uv", args);
});

test("uvx yalniz cevrimdisi (--offline zorunlu)", () => {
  red("uvx", ["cowsay"]);
  gecer("uvx", ["--offline", "cowsay"]);
});

test("uv izinli ornek", () => {
  gecer("uv", ["--version"]);
  gecer("uv", ["pip", "list"]);
});

// ---------------------------------------------------------------- node · python
test("node/python satir ici kod reddedilir", () => {
  for (const args of [["-e", "1"], ["--eval", "1"], ["-p", "1"], ["--print", "1"],
    ["--eval=1"]]) red("node", args);
  for (const args of [["-c", "print(1)"], ["-c print(1)"]]) red("python", args);
});

test("dosyaGerek: var olmayan dosya reddedilir, gercek dosya gecer", () => {
  const dosya = path.join("C:/Projeler/omer-skills/tools/cc-kopru", "kos.mjs");
  red("node", ["yok-boyle-bir-dosya.js"]);
  gecer("node", [dosya]);
  red("python", ["C:/Windows/System32/yok.py"]);   // izinli kok disinda + yok
});

test("python -m modul dosyaGerek'e takilmaz", () => gecer("python", ["-m", "pytest", "--version"]));

test("ffmpeg izinli ornek", () => gecer("ffmpeg", ["-version"]));

// ---------------------------------------------------------------- permissions.deny
test("permissions.deny Bash kurallari koprude uygulanir", () => {
  const deny = ["Bash(rm:*)", "Bash(curl *)", "Read(./bin/**)"];
  assert.throws(() => denyDenetle("rm:-rf /", deny), /permissions\.deny/);
  assert.throws(() => denyDenetle("curl http://x", deny), /permissions\.deny/);
  assert.doesNotThrow(() => denyDenetle("gh --version", deny));
  // ciplak arac adi tum Bash'i reddeder
  assert.throws(() => denyDenetle("gh --version", ["Bash"]), /permissions\.deny/);
  // Read kurallari komut yuzeyinde uygulanmaz (karsiligi K5 gecidinde)
  assert.doesNotThrow(() => denyDenetle("node x.js", ["Read(./bin/**)"]));
});

test("gercek settings.json deny listesi okunur ve komut yuzeyinde patlamaz", () => {
  const p = path.join(os.homedir(), ".claude", "settings.json");
  const j = JSON.parse(fs.readFileSync(p, "utf8"));
  assert.ok(Array.isArray(j.permissions?.deny), "permissions.deny dizi olmali");
  assert.doesNotThrow(() => denyDenetle("gh --version", j.permissions.deny));
});

// ---------------------------------------------------------------- npx gercek kosu (K1-ek)
test("npx --no: kurulu paket kosar, eksik paket reify'den ONCE iptal edilir", async () => {
  const cwd = path.resolve(path.dirname(new URL(import.meta.url).pathname.slice(1)), "..");
  // kurulu: node_modules/.bin/node-which -> npx PATH'ine girer, indirme yok
  const a = await kos({ arac: "npx", args: ["--no", "node-which", "node"], cwd, ayar: AYAR });
  assert.equal(a.kod, 0, a.cikti);
  assert.match(a.cikti, /node\.(exe|EXE)/);

  // eksik: libnpmexec/lib/index.js:288-291 `yes === false` -> npxArb.reify()'den ONCE atar.
  // TTY yokken bayraksiz yol ayni yerde (:294-296) "will be installed" deyip KURAR.
  const b = await kos({ arac: "npx", args: ["--no", "kesinlikle-olmayan-paket-11k"], cwd, ayar: AYAR });
  assert.notEqual(b.kod, 0);
});

// 11l K2 ucu: birim testi yesilken gercek kosu hala bozuktu — npx bir .cmd shim'i oldugu
// icin kos() shim dalinda denetimden CIKAN degil GIREN argv'yi kullaniyordu. Pin uctan uca.
test("npx gercek kosu: `--`siz bicim de paketin surumunu doner (npm'inkini degil)", async () => {
  const cwd = path.resolve(path.dirname(new URL(import.meta.url).pathname.slice(1)), "..");
  for (const args of [["--no", "pixeljury", "--version"],
                      ["--no", "--", "pixeljury", "--version"]]) {
    const r = await kos({ arac: "npx", args, cwd, ayar: AYAR });
    assert.equal(r.kod, 0, r.cikti);
    assert.match(r.cikti, /^\s*0\.\d+\.\d+\s*$/m, `npm surumu dondu: ${r.cikti}`);
  }
}, { timeout: 180000 });

// ---------------------------------------------------------------- git (11m-A K2)
test("git salt-okur alt komutlar gecer", () => {
  gecer("git", ["grep", "-n", "-e", "A", "-e", "B", "--", "docs/"]);
  gecer("git", ["ls-files", "docs/"]);
  gecer("git", ["show", "HEAD:README.md"]);
  gecer("git", ["--version"]);
});

test("git yazan/kosturan alt komutlar reddedilir", () => {
  // status · log · diff · show · branch 11i'den beri izinli; bu dalga grep + ls-files ekledi.
  for (const alt of ["commit", "push", "reset", "clean", "checkout", "filter-branch", "rm"]) {
    red("git", [alt]);
  }
});

test("git: yurutucu cagiran secenekler reddedilir (TEHLIKELI_SECENEK)", () => {
  red("git", ["-c", "core.pager=calc.exe", "grep", "x"]);
  red("git", ["--config", "core.pager=calc.exe", "grep", "x"]);
  red("git", ["--exec-path=C:/kotu", "grep", "x"]);
  red("git", ["--config-env=x", "grep", "y"]);
});

test("git: pager/cikti/filtre bayraklari reddedilir", () => {
  for (const b of [["-O"], ["--open-files-in-pager"], ["--output", "x"], ["--ext-diff"],
                   ["--textconv"], ["-f", "kalip.txt"], ["--file", "kalip.txt"]]) {
    red("git", ["grep", ...b, "x"]);
  }
  red("git", ["show", "--output", "x", "HEAD"]);
});

test("git: gitignore'u atlayan tarama bayraklari reddedilir (deny baypasi)", () => {
  for (const b of ["--no-index", "--untracked", "--no-exclude-standard"]) red("git", ["grep", b, "x"]);
});

test("git: bitisik deger ve benzersiz onek kisaltmalari da reddedilir", () => {
  for (const b of ["-Oless", "--open", "--out", "--out=x", "--ext", "--textc", "--no-ind",
                   "--no-index=1"]) {
    red("git", ["grep", b, "x"]);
  }
});

test("git: mesru uzun bayraklar onek kapisina takilmaz", () => {
  for (const b of ["--name-only", "--no-color", "--line-number", "--cached"]) {
    gecer("git", ["grep", b, "x"]);
  }
});
