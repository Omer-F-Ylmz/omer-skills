"""REA-AGIR-2 kalite kapısı: aynı yakalamayı normal (tek süreç) ve parçalı modda çözer, örtüşmeyi ölçer.
Kullanım: python tools/rea_parcali_kapi.py <url> <dizin> [--bekle 8]
Adımlar: rea_parcali.py (yakala + parçalı) -> dizin/yakala.cevap.json'dan normal analiz (2048 MB tavan) -> kapi.json.
Örtüşme = min(|A∩B|/|A|, |A∩B|/|B|) kümelerde; kategoriler: edge, route, endpoint, webmcp, inference(library), bundle(düğüm)."""
import argparse, json, os, subprocess, sys, time
import psutil

HERE = os.path.dirname(os.path.abspath(__file__))
NODE = r"C:/Program Files/nodejs/node.exe"
DIST = NODE.replace("node.exe", "node_modules/rea-agents/dist")
NOWIN = 0x08000000


def anahtar(o, basissiz):
    if basissiz and isinstance(o, dict):
        o = {k: v for k, v in o.items() if k != "basis"}
    return json.dumps(o, sort_keys=True, ensure_ascii=False)


def kategoriler(r):
    ob = r["observations"]
    return {"edge": ob["chunks"]["edges"], "bundle": ob["chunks"]["nodes"], "route": ob["routes"], "endpoint": ob["endpoints"],
            "webmcp": ob["webmcp_declarations"], "inference": r["inferences"]}


def karsilastir(a, b):
    ka, kb = kategoriler(a), kategoriler(b); cikti = {}
    for k in ka:
        for ad, bs in (("tam", False), ("basissiz", True)):
            A = {anahtar(x, bs) for x in ka[k]}; B = {anahtar(x, bs) for x in kb[k]}; i = len(A & B)
            cikti[f"{k}.{ad}"] = {"normal": len(ka[k]), "parcali": len(kb[k]), "normal_tekil": len(A), "parcali_tekil": len(B),
                                  "ortak": i, "ortusme_yuzde": round(100 * min(i / max(1, len(A)), i / max(1, len(B))), 2) if (A or B) else 100.0}
    return cikti


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("url"); ap.add_argument("dizin"); ap.add_argument("--bekle", default="8")
    a = ap.parse_args(); d = a.dizin; os.makedirs(d, exist_ok=True)
    t0 = time.time()
    subprocess.run([sys.executable, os.path.join(HERE, "rea_parcali.py"), a.url, d, "--bekle", a.bekle], capture_output=True, creationflags=NOWIN)
    t_parcali = time.time() - t0
    cev = os.path.join(d, "yakala.cevap.json"); nor = os.path.join(d, "analiz-normal.json")
    t1 = time.time(); tepe = 0
    p = subprocess.Popen([NODE, "--max-old-space-size=2048", os.path.join(HERE, "rea_parcali_isci.mjs"), DIST, "normal", cev, nor],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=NOWIN)
    pr = psutil.Process(p.pid)
    while p.poll() is None:
        try:
            tepe = max(tepe, pr.memory_info().rss)
        except Exception:
            pass
        if psutil.virtual_memory().percent >= 88:
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True)
        time.sleep(0.2)
    err = p.communicate()[1].decode(errors="replace")[-300:]
    sonuc = {"url": a.url, "parcali_sure_s": round(t_parcali, 1), "normal_kod": p.returncode, "normal_sure_s": round(time.time() - t1, 1),
             "normal_rss_tepe_mb": tepe // 2**20}
    if p.returncode == 0:
        sonuc["karsilastirma"] = karsilastir(json.load(open(nor, encoding="utf-8")), json.load(open(os.path.join(d, "analiz.json"), encoding="utf-8")))
    else:
        sonuc["normal_hata"] = err
    json.dump(sonuc, open(os.path.join(d, "kapi.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in sonuc.items() if k != "karsilastirma"}, ensure_ascii=False))
    for k, v in sonuc.get("karsilastirma", {}).items():
        if k.endswith(".basissiz") or k.endswith(".tam"):
            print(k, v["normal"], v["parcali"], v["ortak"], v["ortusme_yuzde"])


main()
