import { createHash, timingSafeEqual } from "node:crypto";
import type { IncomingMessage, ServerResponse } from "node:http";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { sunucuYap } from "./sunucu.js";

// Özetler sabit uzunlukta: uzunluk farkı da zamanlamadan sızmaz.
export function yetkili(gelen: string | undefined, beklenen: string | undefined) {
  if (!gelen || !beklenen) return false;
  const oz = (x: string) => createHash("sha256").update(x).digest();
  return timingSafeEqual(oz(gelen), oz(beklenen));
}

const bitir = (res: ServerResponse, kod: number) => {
  res.writeHead(kod, { "content-type": "application/json" }).end(JSON.stringify({ error: kod === 401 ? "unauthorized" : "method not allowed" }));
};

export default async function handler(req: IncomingMessage & { body?: unknown }, res: ServerResponse) {
  const baslik = req.headers["x-jev-token"];
  if (!yetkili(typeof baslik === "string" ? baslik : undefined, process.env.JEV_MCP_TOKEN)) return bitir(res, 401);
  if (req.method !== "POST") return bitir(res, 405);
  const sunucu = sunucuYap();
  const tasima = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined, enableJsonResponse: true });
  res.on("close", () => {
    void tasima.close();
    void sunucu.close();
  });
  await sunucu.connect(tasima);
  await tasima.handleRequest(req, res, req.body);
}
