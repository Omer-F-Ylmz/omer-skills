/**
 * Sahte claude-mem worker'ı. Suit ve envanter gerçek worker'a yazmasın diye var:
 * her köprü süreci gerçek worker'da yeni oturum açıyordu (CLAUDE-MEM-1b ölçümü:
 * tek suit koşusu = 15 ENQUEUED · kuyruk +15 · park +13).
 * Üretim varsayılanı değişmez; port yalnız CLAUDE_MEM_WORKER_PORT ile aktarılır.
 */
import http from "node:http";

export async function sahteWorker() {
  const istek = [];
  const srv = http.createServer((q, y) => {
    if (q.url.startsWith("/api/sessions/observations")) istek.push(q.url);
    y.writeHead(200, { "content-type": "application/json" });
    y.end(JSON.stringify({ status: "queued", healthy: true, ready: true }));
  });
  await new Promise((r) => srv.listen(0, "127.0.0.1", r));
  return { port: srv.address().port, istek, kapat: () => new Promise((r) => srv.close(r)) };
}
