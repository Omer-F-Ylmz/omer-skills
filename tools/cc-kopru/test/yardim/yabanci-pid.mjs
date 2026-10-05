// suit-pid.test.mjs yardımcısı: işaret dizinine node olmayan canlı bir sürecin pid'ini yazar
// (Windows'ta ölen işaretli node'un pid'i başka sürece verilince olan durum).
import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const c = spawn("ping", ["-n", "30", "127.0.0.1"], { detached: true, stdio: "ignore" });
c.unref();
fs.writeFileSync(path.join(process.env.CC_KOPRU_SUIT_ISARET, String(c.pid)), "");
fs.writeFileSync(process.env.YABANCI_DOSYA, String(c.pid));
