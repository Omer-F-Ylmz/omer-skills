/** Geçit testleri için asgari MCP sunucusu: her isteğe sabit bir sonuç döner. */
import readline from "node:readline";

readline.createInterface({ input: process.stdin }).on("line", (satir) => {
  let m;
  try { m = JSON.parse(satir); } catch { return; }
  if (m.id === undefined) return;   // bildirim
  process.stdout.write(JSON.stringify({
    jsonrpc: "2.0", id: m.id,
    result: { content: [{ type: "text", text: "SAHTE-TAMAM" }] },
  }) + "\n");
});
