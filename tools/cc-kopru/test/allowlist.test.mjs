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

import { ayarYukle, denyDenetle, komutDenetle, yolBul } from "../kos.mjs";

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

test("npx kosmaz: --no-install bu npm surumunde yok", () => {
  red("npx", ["cowsay"]);
  red("npx", ["--no-install", "cowsay"]);
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
