import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { degerlendir, JevHata, modeller, toplu, TOPLU_UST, type Soru, type State } from "./jev.js";

const icerik = z.union([z.string(), z.record(z.string(), z.unknown()), z.array(z.unknown())]);
const soru = z.object({
  type: z.enum(["noul", "choice", "score"]),
  instructions: icerik.describe("the question; refer to state fields in `backticks`"),
  criteria: z.unknown().optional().describe("noul: {true,false}? · choice: {option: desc|null} ≤255 · score: [levels] 2-10"),
});
const sorular = z.record(z.string(), soru).describe("{name: question}; answers come back under the same names");
const model = z.enum(["jev-latest", "jev-1.13"]).optional();
const salt = { readOnlyHint: true, openWorldHint: true };

const metin = (x: unknown, isError = false) => ({ content: [{ type: "text" as const, text: JSON.stringify(x) }], ...(isError ? { isError } : {}) });
const sar = async (f: () => Promise<unknown>) => {
  try {
    return metin(await f());
  } catch (e) {
    return metin(e instanceof JevHata ? e.toJSON() : { error_type: "internal", message: "beklenmeyen hata" }, true);
  }
};

export function sunucuYap() {
  const s = new McpServer({ name: "jev", version: "0.1.0" });
  s.registerTool(
    "jev_evaluate",
    {
      description: "Judge one state with typed questions (noul=yes/no prob, choice=option+probabilities, score=level). Returns answers, usage, model, sure_ms.",
      inputSchema: { state: icerik.describe("material being judged"), questions: sorular, model },
      annotations: salt,
    },
    ({ state, questions, model }) => sar(() => degerlendir({ state: state as State, questions: questions as Record<string, Soru>, model })),
  );
  s.registerTool(
    "jev_batch",
    {
      description: `Same questions over up to ${TOPLU_UST} states (8 concurrent). One result or error per row.`,
      inputSchema: { states: z.array(icerik).min(1).max(TOPLU_UST), questions: sorular, model },
      annotations: salt,
    },
    ({ states, questions, model }) => sar(() => toplu({ states: states as State[], questions: questions as Record<string, Soru>, model })),
  );
  s.registerTool("jev_models", { description: "Allowed Jev model ids and their OpenRouter ids.", annotations: { readOnlyHint: true } }, async () => metin(modeller()));
  return s;
}
