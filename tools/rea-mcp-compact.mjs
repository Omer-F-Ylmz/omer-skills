// REA MCP başlatıcı: Desktop REA sürecine config "env" bloğunu iletmiyor (23 Eki, süreç ortamında değişken YOK) ->
// full şema (compare_web_captures ~180 KB) yayınlanıp bağlayıcı reddediliyordu. Profili süreç İÇİNDE sabitler.
import { dirname, join } from "node:path";
import { pathToFileURL } from "node:url";

process.env.REA_MCP_INPUT_SCHEMA_PROFILE = "compact";
process.env.REA_MCP_OUTPUT_SCHEMA_PROFILE = "off";
const kok = join(dirname(process.execPath), "node_modules", "rea-agents");
const rea = join(kok, "scripts", "rea.mjs");
process.argv = [process.argv[0], rea, "mcp"];
await import(pathToFileURL(rea).href);
