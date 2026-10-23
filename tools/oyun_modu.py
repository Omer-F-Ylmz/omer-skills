"""OYUN-MODU-1: oyun açılınca arka plan RAM'ini boşaltır, kapanınca bayrağı kaldırır.
python tools/oyun_modu.py [--kuru | --bir-kez]   (varsayılan: 5 sn yoklayan döngü)
Oyun sürecine DOKUNMAZ (yalnız adı okunur): anti-cheat. Discord/Epic/Chrome kapatılmaz, yalnız "elle kapatılabilir" listelenir.
Bayrak: .kos/kopru/oyun-modu.bayrak (her yoklamada mtime tazelenir; ajan_sira >60 sn eskiyse yok sayar). Log: .kos/kopru/oyun-modu.log"""
import json
import os
import sys
import time
import urllib.request

KOK = r"C:\Projeler\omer-skills"
K = os.path.join(KOK, ".kos", "kopru")
BAYRAK = os.path.join(K, "oyun-modu.bayrak")
LOG = os.path.join(K, "oyun-modu.log")
OYUNLAR = {"zenlesszonezero.exe", "genshinimpact.exe", "yuanshen.exe", "client-win64-shipping.exe"}
YETIM_ADLAR = {"conhost.exe", "node.exe", "python.exe", "pythonw.exe"}
# ebeveyni ölmüş olsa da dokunulmaz: MCP sunucuları, yöneticiler, bellek işçisi, bu betik
KORUNAN = ("mcp", "claude", "ajan_sira", "mem_bekci", "oyun_modu", "worker", "headroom", "graphify", "ollama", "arka.py", "kopru", "omer-skills")  # repo betikleri bilerek kopuk koşar
EL_ILE = {"discord.exe", "epicwebhelper.exe", "epicgameslauncher.exe", "chrome.exe", "msedgewebview2.exe"}
YETIM_MIN_YAS = 300  # sn: yeni doğmuş kopuk süreçler iş olabilir


def oyun_var(adlar):
    """Çalışan süreç adlarından oyun exe'si eşlemesi; bulunanları döner."""
    return sorted({a.lower() for a in adlar} & OYUNLAR)


def yetim_adaylar(procs, simdi, pid_kendi=None):
    """procs: {pid, ppid, name, create, cmd, idle, rss_mb} listesi. Ebeveyni ölmüş (yok ya da pid yeniden kullanılmış),
    boşta, ≥YETIM_MIN_YAS yaşında, korunan ifade içermeyen conhost/node/python süreçleri."""
    cesit = {p["pid"]: p for p in procs}
    out = []
    for p in procs:
        if p["name"].lower() not in YETIM_ADLAR or p["pid"] == pid_kendi:
            continue
        ata = cesit.get(p["ppid"])
        if ata is not None and ata["create"] <= p["create"]:
            continue  # ebeveyn canlı
        if not p["idle"] or simdi - p["create"] < YETIM_MIN_YAS:
            continue
        cmd = (p["cmd"] or "").lower()
        if any(k in cmd for k in KORUNAN):
            continue
        out.append(p)
    return out


def tara():
    import psutil
    ps = list(psutil.process_iter(["pid", "ppid", "name", "create_time", "cmdline", "memory_info"]))
    for p in ps:
        try:
            p.cpu_percent(None)
        except psutil.Error:
            pass
    time.sleep(1)
    procs = []
    for p in ps:
        try:
            i = p.info
            procs.append({"pid": i["pid"], "ppid": i["ppid"], "name": i["name"] or "", "create": i["create_time"] or 0,
                          "cmd": " ".join(i["cmdline"] or []), "idle": p.cpu_percent(None) < 1.0,
                          "rss_mb": (i["memory_info"].rss // 2**20) if i["memory_info"] else 0})
        except psutil.Error:
            pass
    return procs


def ram():
    import psutil
    m = psutil.virtual_memory()
    return "%%%d (%.1f/%.1f GB)" % (m.percent, m.used / 2**30, m.total / 2**30)


def log(*a):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + " ".join(str(x) for x in a) + "\n")


def ollama_modeller():
    try:
        with urllib.request.urlopen("http://127.0.0.1:11434/api/ps", timeout=5) as f:
            return json.loads(f.read() or b"{}").get("models", [])
    except OSError:
        return []


def ollama_bosalt(modeller):
    for m in modeller:
        r = urllib.request.Request("http://127.0.0.1:11434/api/generate", data=json.dumps({"model": m.get("name") or m.get("model"), "keep_alive": 0}).encode(),
                                   headers={"Content-Type": "application/json"})
        urllib.request.urlopen(r, timeout=10).read()


def kuru(procs):
    y = yetim_adaylar(procs, time.time(), os.getpid())
    mb = sum(p["rss_mb"] for p in y)
    ol = ollama_modeller()
    ol_mb = sum(m.get("size", 0) for m in ol) // 2**20
    print("RAM:", ram())
    print("kapanacak yetim süreç: %d · ~%d MB" % (len(y), mb))
    for ad in sorted({p["name"] for p in y}):
        s = [p for p in y if p["name"] == ad]
        print("  %s x%d  %d MB" % (ad, len(s), sum(p["rss_mb"] for p in s)))
    print("ollama boşalacak model: %d · ~%d MB (llama-server)" % (len(ol), ol_mb))
    print("toplam tahmin: ~%d MB" % (mb + ol_mb))
    el = {}
    for p in procs:
        if p["name"].lower() in EL_ILE:
            el[p["name"]] = el.get(p["name"], 0) + p["rss_mb"]
    print("elle kapatılabilir:", ", ".join("%s %d MB" % kv for kv in sorted(el.items())) or "-")


def etkinlestir(procs):
    import psutil
    onceki = ram()
    y = yetim_adaylar(procs, time.time(), os.getpid())
    n = 0
    for p in y:
        try:
            psutil.Process(p["pid"]).kill()
            n += 1
        except psutil.Error:
            pass
    try:
        ol = ollama_modeller()
        ollama_bosalt(ol)
    except OSError:
        ol = []
    time.sleep(2)
    log("OYUN BASLADI yetim_kapatilan=%d ollama_bosaltilan=%d RAM once=%s sonra=%s" % (n, len(ol), onceki, ram()))


def dongu():
    import psutil
    aktif = False
    while True:
        oyun = oyun_var(p.info["name"] or "" for p in psutil.process_iter(["name"]))
        if oyun:
            os.makedirs(K, exist_ok=True)
            if not aktif:
                open(BAYRAK, "w").write(",".join(oyun))
                etkinlestir(tara())
                aktif = True
            os.utime(BAYRAK, None)
        elif aktif:
            if os.path.exists(BAYRAK):
                os.remove(BAYRAK)
            log("OYUN KAPANDI bayrak kaldirildi RAM=%s" % ram())
            aktif = False
        time.sleep(5)


if __name__ == "__main__":
    if "--kuru" in sys.argv:
        kuru(tara())
    elif "--bir-kez" in sys.argv:
        etkinlestir(tara())
    else:
        dongu()
