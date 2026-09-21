/**
 * KURULUM-11l B2 — sahte `claude -p` aktarıcısı (NODE_OPTIONS --import ile yüklenir).
 *
 * Gerçek uçtaki kök nedeni birebir taklit eder: ANTHROPIC_BASE_URL ile başlatılan
 * süreçte model 23 aracı görmez (headroom yerel vekili tools dizisini tek arama
 * aracına indiriyor) → yalnız metin döner, `tool_use` yoktur. Değişken yoksa araç
 * çağrılır. Köprünün kendi sürecinde de yüklendiği için yalnız aktarıcı argv'sinde
 * (`--allowedTools`) davranır, başka hiçbir süreci etkilemez.
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const argv = process.argv.slice(2);
if (argv.includes("--allowedTools")) {
  const BURASI = path.dirname(fileURLToPath(import.meta.url));
  const tamAd = argv[argv.indexOf("--allowedTools") + 1];
  const adlar = JSON.parse(fs.readFileSync(path.join(BURASI, "..", "..", "tasarim-semalar.json"), "utf8"))
    .map((s) => s.name);

  const yaz = (o) => process.stdout.write(JSON.stringify(o) + "\n");
  yaz({ type: "system", subtype: "init", tools: adlar });

  if (process.env.ANTHROPIC_BASE_URL) {
    yaz({ type: "assistant", message: { content: [{ type: "text", text: "Özür dilerim, mevcut araçlarım arasında yok." }] } });
  } else {
    yaz({ type: "assistant", message: { content: [{ type: "tool_use", id: "t1", name: tamAd, input: {} }] } });
    yaz({ type: "user", message: { content: [{ type: "tool_result", tool_use_id: "t1", content: [{ type: "text", text: "SAHTE-SONUC" }] }] } });
  }
  process.exit(0);
}
