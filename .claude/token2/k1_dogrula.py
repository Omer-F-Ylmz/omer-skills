"""TOKEN-2 K1 doğrulama: 2 kol × 1 claude -p (toplam en fazla 2). Kol A = headroom varsayılan, B = HEADROOM_STABLE_BOUNDARY_BREAKPOINT=0.
Her kol: test vekili 6769 (k1_vekil.py, yer değiştirme izi) → claude -p (opus, high, MCP'siz) → durma × yer değiştirme tablosu."""
import glob, json, os, socket, subprocess, sys, time
from pathlib import Path

import psutil

KOK = Path(r"C:\Projeler\omer-skills"); D = KOK / ".claude" / "token2"
PY = Path.home() / "AppData/Local/Headroom/headroom/runtime/venv/Scripts/python.exe"
PORT = 6769
DOSYA = sorted(glob.glob(str(KOK / "tests" / "test_*.py")), key=os.path.getsize)[-30:-6]
ISTEM = ("Use the Read tool on each of these files, ONE file per call, strictly sequentially (never parallel; no Bash, Grep or Glob). "
         "After the last one, reply with exactly one line: the total number of lines that start with 'def test_'.\n" + "\n".join(DOSYA))

def bekle_port(ac=True, sure=60):
    for _ in range(sure * 2):
        try:
            socket.create_connection(("127.0.0.1", PORT), 0.5).close(); acik = True
        except OSError:
            acik = False
        if acik == ac:
            return True
        time.sleep(0.5)
    return False

def stats():
    try:
        import urllib.request
        c = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/stats", timeout=5))["summary"]["compression"]
        return {k: c.get(k) for k in ("requests_compressed", "total_tokens_removed", "total_tokens_before")}
    except Exception as e:
        return {"hata": type(e).__name__}

def kol(ad, env_ek, istem=ISTEM, cwd=KOK, tur=40, ek=(), sure=2400, vekil_ek=(), effort="high"):
    iz = D / f"k1_iz_{ad}.tsv"; iz.unlink(missing_ok=True)
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    env.update(env_ek, K1_IZ=str(iz), HEADROOM_PORT=str(PORT))
    vekil = subprocess.Popen([str(PY), str(D / "k1_vekil.py"), "proxy", "--port", str(PORT), "--no-http2", "--no-rate-limit", *vekil_ek],
                             env=env, stdout=open(D / f"k1_vekil_{ad}.log", "w"), stderr=subprocess.STDOUT,
                             creationflags=subprocess.CREATE_NO_WINDOW)
    if not bekle_port(True):
        vekil.kill(); return {"kol": ad, "hata": "vekil açılmadı"}
    t0 = time.time()
    ayar = json.dumps({"env": {"ANTHROPIC_BASE_URL": f"http://127.0.0.1:{PORT}"}})
    cenv = {k: v for k, v in env.items() if not k.startswith("HEADROOM_") and k != "K1_IZ"}
    cenv["ANTHROPIC_BASE_URL"] = f"http://127.0.0.1:{PORT}"
    # d2b: istem-r0e-B ajanı `python -m http.server` başlatıyor; torun boruyu tuttuğu için run(capture_output) zaman aşımından
    # sonra da communicate()'te asılıyordu (d1b, 50 dk log boş). → çıktı dosyaya, torunlar izlenir, bitişte/süre dolunca öldürülür.
    cikti = D / f"k1_cikti_{ad}.json"
    with open(cikti, "w", encoding="utf-8") as fo:
        p = subprocess.Popen(["claude", "-p", "--model", "opus", "--effort", effort, "--output-format", "json", "--max-turns", str(tur),
                              "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--disable-slash-commands", "--settings", ayar, *ek],
                             stdin=subprocess.PIPE, stdout=fo, stderr=subprocess.STDOUT, text=True, encoding="utf-8", env=cenv,
                             cwd=str(cwd), creationflags=subprocess.CREATE_NO_WINDOW, shell=True)
        p.stdin.write(istem); p.stdin.close()
        torun = set()
        while p.poll() is None and time.time() - t0 < sure:
            try:
                torun |= set(psutil.Process(p.pid).children(recursive=True))
            except psutil.Error:
                pass
            time.sleep(5)
        zaman_asimi = p.poll() is None
        hedef = list(torun)
        if zaman_asimi:  # d3: psutil.Process(p.pid) yalnız süreç yaşıyorken kurulur (bitmişse NoSuchProcess → k1b A kolu çöktü)
            try:
                hedef.insert(0, psutil.Process(p.pid))
            except psutil.Error:
                pass
        for c in hedef:
            try:
                c.kill()
            except psutil.Error:
                pass
        p.wait(30)
    metin = cikti.read_text(encoding="utf-8", errors="replace")
    hr = stats()
    vekil.kill(); bekle_port(False, 10)
    return ozet(ad, metin, iz, hr, time.time() - t0, p.returncode, "zaman aşımı" if zaman_asimi else "")

def ozet(ad, metin, iz, hr, sure, rc=None, hata=""):
    try:
        j = json.loads(metin); sid = j.get("session_id")
    except Exception:
        return {"kol": ad, "hata": "json yok", "rc": rc, "cikti": (metin or hata)[-300:]}
    tr = next((Path.home() / ".claude/projects").glob(f"*/{sid}.jsonl"))
    goruldu, istek = set(), []
    for l in open(tr, encoding="utf-8"):
        r = json.loads(l); m = r.get("message") or {}
        u = m.get("usage")
        if r.get("type") != "assistant" or not u or m.get("id") in goruldu:
            continue
        goruldu.add(m.get("id"))
        istek.append((u.get("input_tokens", 0), u.get("cache_read_input_tokens", 0), u.get("cache_creation_input_tokens", 0)))
    yer = [x.split("\t") for x in iz.read_text(encoding="utf-8").splitlines()] if iz.exists() else []
    durma = [i for i, (un, cr, cw) in enumerate(istek) if cw == 0 and un >= 3000]
    return {"kol": ad, "sid": sid, "sonuc": str(j.get("result", ""))[:80], "istek": len(istek), "durma": len(durma),
            "durma_idx": durma, "onbelleksiz": sum(x[0] for x in istek), "okuma": sum(x[1] for x in istek),
            "yazma": sum(x[2] for x in istek), "yer_cagri": len(yer), "yer_degisti": sum(int(x[4]) for x in yer),
            "yer_degisti_satir": [x for x in yer if x[4] == "1"][:10], "sure_sn": round(sure), "headroom": hr, "tur": j.get("num_turns"), "usd": j.get("total_cost_usd")}

if __name__ == "__main__":
    out = D / "k1_dogrula.jsonl"
    for ad, e in (("A_varsayilan", {}), ("B_stable0", {"HEADROOM_STABLE_BOUNDARY_BREAKPOINT": "0"}))[: int(sys.argv[1]) if len(sys.argv) > 1 else 2]:
        r = kol(ad, e)
        print(json.dumps(r, ensure_ascii=False), flush=True)
        with open(out, "a", encoding="utf-8") as f:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("BITTI", flush=True)
