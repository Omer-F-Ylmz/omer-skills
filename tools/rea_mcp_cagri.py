"""REA-AGIR-1: REA MCP'yi ayrı node sürecinde (bellek bayraklı) koşturup tek araç çağırır; Chrome headless CDP açar.
Kullanım: python tools/rea_mcp_cagri.py <url> <arac> <json-arg|-> <cikti.json> [node-bayrakları...]
arac argümanlarında {CDP} ve {TARGET} yer tutucuları doldurulur. Tepe RAM (REA süreci) ve süre cikti.json'a yazılır."""
import json, os, subprocess, sys, tempfile, threading, time, urllib.request
import psutil

NODE = r"C:/Program Files/nodejs/node.exe"
REA = NODE.replace("node.exe", "node_modules/rea-agents/scripts/rea.mjs")
CHROME = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
NOWIN = 0x08000000


def bos_port():
    import socket
    with socket.socket() as k:  # önceki koşudan artık Chrome 9333'te kalıp başka sayfayı sunmasın
        k.bind(("127.0.0.1", 0)); return k.getsockname()[1]


PORT = bos_port()


def ram():
    return psutil.virtual_memory().percent


def chrome_ac(url):
    d = tempfile.mkdtemp(prefix="ragir-chrome-")
    p = subprocess.Popen([CHROME, "--headless=new", f"--remote-debugging-port={PORT}", f"--user-data-dir={d}",
                          "--no-first-run", "--disable-gpu", url], creationflags=NOWIN,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(60):
        try:
            l = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/list", timeout=2))
            return p, [t for t in l if t["type"] == "page"]
        except Exception:
            time.sleep(0.5)
    p.kill(); raise SystemExit("chrome açılmadı")


def main():
    url, arac, arg, cikti, *bayrak = sys.argv[1:]
    bekle_s = int(os.environ.get("BEKLE", "25"))
    ch, _ = chrome_ac(url)
    time.sleep(bekle_s)  # SPA yüklensin
    sayfalar = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/list"))
    hedef = [t for t in sayfalar if t["type"] == "page"][0]
    cdp = f"http://127.0.0.1:{PORT}"
    args = {} if arg == "-" else json.loads(arg.replace("{CDP}", cdp).replace("{TARGET}", hedef["id"]))
    env = {**os.environ, "REA_MCP_INPUT_SCHEMA_PROFILE": "compact", "REA_MCP_OUTPUT_SCHEMA_PROFILE": "off",
           "REA_MCP_MAX_RESPONSE_BYTES": "400000000"}  # yanıt diske gider; stdio bütçesi ağır sayfada (figma) yakalamayı düşürmesin
    env.pop("NODE_OPTIONS", None)
    hd = os.path.dirname(os.path.abspath(cikti))
    p = subprocess.Popen([NODE, *bayrak, REA, "mcp"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=open(cikti + ".stderr", "wb"), env=env, cwd=hd, creationflags=NOWIN)
    tepe = [0]; ram_tepe = [0]; dur = [False]

    def izle():
        pr = psutil.Process(p.pid)
        while p.poll() is None:
            try:
                rss = pr.memory_info().rss + sum(c.memory_info().rss for c in pr.children(recursive=True))
                tepe[0] = max(tepe[0], rss)
            except Exception:
                pass
            r = ram(); ram_tepe[0] = max(ram_tepe[0], r)
            if r >= 88:
                dur[0] = True; subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True)
            time.sleep(0.5)
    threading.Thread(target=izle, daemon=True).start()
    cevap = {}

    gc = open(cikti + ".gc.txt", "wb")

    def oku():
        for ln in p.stdout:
            if not ln.startswith(b"{"):
                gc.write(ln); continue
            try:
                m = json.loads(ln)
                if "id" in m: cevap[m["id"]] = m
            except Exception:
                pass
    threading.Thread(target=oku, daemon=True).start()

    def gonder(m): p.stdin.write((json.dumps(m) + "\n").encode()); p.stdin.flush()
    t0 = time.time()
    gonder({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "ragir", "version": "1"}}})
    while 1 not in cevap and time.time() - t0 < 30: time.sleep(0.2)
    gonder({"jsonrpc": "2.0", "method": "notifications/initialized"})
    t1 = time.time()
    gonder({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": arac, "arguments": args}})
    zaman_asimi = int(os.environ.get("ZAMAN_ASIMI", "420"))
    while 2 not in cevap and p.poll() is None and time.time() - t1 < zaman_asimi: time.sleep(0.5)
    sonuc = {"url": url, "arac": arac, "bayrak": bayrak, "sure_s": round(time.time() - t1, 1), "rea_rss_tepe_mb": tepe[0] // 2**20,
             "sistem_ram_tepe": ram_tepe[0], "ram_bekci_durdurdu": dur[0], "rea_cikis": p.poll(), "cevap_var": 2 in cevap}
    if 2 in cevap:
        metin = json.dumps(cevap[2], ensure_ascii=False)
        sonuc["cevap_bayt"] = len(metin)
        open(cikti.replace(".json", ".cevap.json"), "w", encoding="utf-8").write(metin)
    open(cikti, "w", encoding="utf-8").write(json.dumps(sonuc, ensure_ascii=False, indent=1))
    print(json.dumps(sonuc, ensure_ascii=False))
    subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True)
    subprocess.run(["taskkill", "/F", "/T", "/PID", str(ch.pid)], capture_output=True)


main()
