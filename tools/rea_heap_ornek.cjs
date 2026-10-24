// REA-AGIR-1: --require ile yüklenir; süreç RSS'i RSS_MB'ı geçince ana iş parçacığının örnekleme yığın profilini
// (canlı nesnelerin ayrılış yığınları) diske yazar. İşçi parçacığı kullanır: ana döngü mikro-görevlerle doluyken zamanlayıcı çalışmaz.
const { Worker, isMainThread } = require("worker_threads");
if (isMainThread) {
  const insp = require("inspector"); const s = new insp.Session(); s.connect();
  s.post("HeapProfiler.enable"); s.post("HeapProfiler.startSampling", { samplingInterval: 32768 });
  const w = new Worker(__filename, { env: process.env });
  w.on("error", (e) => require("fs").appendFileSync((process.env.HEAP_OUT || "heap-ornek.json") + ".log", "isci-hata " + e + "\n"));
  w.unref();
} else {
  const insp = require("inspector"), fs = require("fs"); const s = new insp.Session(); s.connectToMainThread();
  const esik = Number(process.env.RSS_MB || 700) * 2 ** 20, cikti = process.env.HEAP_OUT || "heap-ornek.json";
  const log = (m) => fs.appendFileSync(cikti + ".log", m + " " + Date.now() + "\n");
  const t = setInterval(() => {
    if (process.memoryUsage().rss < esik) return;
    clearInterval(t); log("esik");
    s.post("HeapProfiler.getSamplingProfile", (e, r) => { log("cevap"); fs.writeFileSync(cikti, JSON.stringify(e ? { hata: String(e) } : r)); });
  }, 100);
}
