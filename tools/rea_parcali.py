"""REA-AGIR-1 parçalı mod: ağır SPA'da analyze_web_bundle yerine yakala -> diske böl -> betik başına taze bellek tavanlı süreç -> birleştir.
Kullanım: python tools/rea_parcali.py <url> <cikti-dizini> [--capture <capture.json>] [--bekle 20] [--grup-mb 0]
Çıktı: <dizin>/ozet.json (≤60 satır özet), analiz.json (tam sonuç), olcum.json (süre/RAM/kapsama).
Kapı: sistem RAM >=%85'te yeni süreç başlamaz (bekler), >=%88'de çalışan durdurulur. Ara veri diskte, modele yalnız özet."""
import argparse, json, os, subprocess, sys, time
import psutil

HERE = os.path.dirname(os.path.abspath(__file__))
NODE = r"C:/Users/pc/AppData/Local/Microsoft/WinGet/Packages/OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe/node-v24.19.0-win-x64/node.exe"
DIST = NODE.replace("node.exe", "node_modules/rea-agents/dist")
ISCI = os.path.join(HERE, "rea_parcali_isci.mjs")
NOWIN = 0x08000000
TAVAN = "--max-old-space-size=2048"


def ram():
    return psutil.virtual_memory().percent


def kapi_bekle(en_fazla=300):
    t0 = time.time()
    while ram() >= 85 and time.time() - t0 < en_fazla:
        time.sleep(2)


def isci(args, tepe):
    """Taze node süreci; tepe RSS izlenir, RAM >=%88'de öldürülür. (cikis, durdu, tepe_mb)."""
    kapi_bekle()
    p = subprocess.Popen([NODE, TAVAN, ISCI, DIST, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=NOWIN)
    pr = psutil.Process(p.pid); durdu = False; t = 0
    while p.poll() is None:
        try:
            t = max(t, pr.memory_info().rss)
        except Exception:
            pass
        if ram() >= 88:
            durdu = True; subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True)
        time.sleep(0.2)
    p.communicate()
    tepe[0] = max(tepe[0], t)
    return p.returncode, durdu


def yakala(url, dizin, bekle):
    cikti = os.path.join(dizin, "yakala.json")
    env = {**os.environ, "BEKLE": str(bekle), "ZAMAN_ASIMI": "240"}
    arg = json.dumps({"cdp_endpoint": "{CDP}", "target_id": "{TARGET}", "observation_ms": 3000, "include_script_sources": True})
    subprocess.run([sys.executable, os.path.join(HERE, "rea_mcp_cagri.py"), url, "inspect_web_page", arg, cikti, TAVAN],
                   env=env, capture_output=True, creationflags=NOWIN)
    m = json.load(open(cikti.replace(".json", ".cevap.json"), encoding="utf-8"))
    if m["result"].get("isError"):
        raise SystemExit("yakalama hatası: " + m["result"]["content"][0]["text"][:300])
    return m["result"]["structuredContent"]["normalized_result"], json.load(open(cikti, encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url"); ap.add_argument("dizin")
    ap.add_argument("--capture"); ap.add_argument("--bekle", type=int, default=20)
    a = ap.parse_args()
    d = a.dizin; os.makedirs(os.path.join(d, "ogeler"), exist_ok=True)
    t0 = time.time(); tepe = [0]; ram_tepe = ram()
    if a.capture:
        n = json.load(open(a.capture, encoding="utf-8"))["normalized_result"]; yak = {}
    else:
        n, yak = yakala(a.url, d, a.bekle)
    ogeler = n["scripts"]["items"]
    dosyalar = []
    for i, oge in enumerate(ogeler):
        if not oge["source"]["included"]:
            continue
        f = os.path.join(d, "ogeler", f"{i:04d}.json"); json.dump(oge, open(f, "w", encoding="utf-8")); dosyalar.append((i, f, oge))
        oge["source"]["artifact"].pop("text", None)  # birleştirme girdisi metinsiz
    json.dump(n, open(os.path.join(d, "inspection-metinsiz.json"), "w", encoding="utf-8"))
    ok, basarisiz = [], []
    for i, f, oge in dosyalar:
        cikti = f.replace(".json", ".acc.json")
        kod, durdu = isci(["script", f, cikti], tepe)
        ram_tepe = max(ram_tepe, ram())
        (ok if kod == 0 and os.path.exists(cikti) else basarisiz).append(
            {"i": i, "url": oge["url"], "bayt": oge["source"]["artifact"]["bytes"], "kod": kod, "ram_durdurdu": durdu})
    # tek betik tavanı aşarsa: wakaru ile modüllere aç, modüller ayrı süreçlerde analiz edilir (bulgular üst betik anahtarına yazılır)
    for b in list(basarisiz):
        i, f = b["i"], os.path.join(d, "ogeler", f"{b['i']:04d}.json")
        oge = json.load(open(f, encoding="utf-8"))
        js = os.path.join(d, "ogeler", f"{i:04d}.src.js"); wk = os.path.join(d, "ogeler", f"{i:04d}.wk")
        open(js, "w", encoding="utf-8").write(oge["source"]["artifact"]["text"])
        subprocess.run([sys.executable, os.path.join(HERE, "wakaru_kurtar.py"), js, wk], capture_output=True, creationflags=NOWIN)
        moduller = [os.path.join(k, x) for k, _, xs in os.walk(wk) for x in xs if x.endswith((".js", ".jsx", ".mjs"))]
        gec = 0
        for j, mf in enumerate(moduller):
            alt = json.loads(json.dumps(oge)); alt["source"]["artifact"]["text"] = open(mf, encoding="utf-8", errors="replace").read()
            af = os.path.join(d, "ogeler", f"{i:04d}.m{j:04d}.json"); json.dump(alt, open(af, "w", encoding="utf-8"))
            kod, _ = isci(["script", af, af.replace(".json", ".acc.json")], tepe)
            gec += kod == 0 and os.path.exists(af.replace(".json", ".acc.json"))
        b["wakaru_modul"] = len(moduller); b["wakaru_analiz_edilen"] = gec
        if moduller and gec == len(moduller):
            basarisiz.remove(b); ok.append({**b, "yol": "wakaru"})
    ok_f = [os.path.join(d, "ogeler", x) for x in sorted(os.listdir(os.path.join(d, "ogeler"))) if x.endswith(".acc.json")]
    analiz = os.path.join(d, "analiz.json")
    kod, _ = isci(["birlestir", os.path.join(d, "inspection-metinsiz.json"), analiz, *ok_f], tepe)
    olcum = {"url": a.url, "sure_s": round(time.time() - t0, 1), "isci_rss_tepe_mb": tepe[0] // 2**20,
             "sistem_ram_tepe": ram_tepe, "betik_toplam": len(ogeler), "analiz_edilecek": len(dosyalar),
             "analiz_edilen": len(ok), "basarisiz": basarisiz, "birlestirme_kodu": kod,
             "kapsama_yuzde": round(100 * len(ok) / max(1, len(dosyalar)), 1),
             "yakalama": {k: yak.get(k) for k in ("sure_s", "rea_rss_tepe_mb")}}
    json.dump(olcum, open(os.path.join(d, "olcum.json"), "w", encoding="utf-8"), indent=1)
    if kod == 0:
        r = json.load(open(analiz, encoding="utf-8"))
        g = r.get("graph", {}) if isinstance(r, dict) else {}
        ozet = {"anahtarlar": list(r.keys()), "olcum": {k: v for k, v in olcum.items() if k != "basarisiz"}}
        json.dump(ozet, open(os.path.join(d, "ozet.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in olcum.items() if k != "basarisiz"}, ensure_ascii=False), "basarisiz:", len(basarisiz))


main()
