import sys, os, json, subprocess, time
KOK = os.environ.get("ARKA_KOK", r"C:\Projeler\omer-skills\.kos\kopru\arka")
CLAUDE = os.path.expanduser(r"~\.local\bin\claude.exe")
PYW = sys.executable.replace("python.exe", "pythonw.exe")
BU = os.path.abspath(__file__)

def baslat(isim):
    is_ = os.path.join(KOK, isim + ".json")
    json.load(open(is_, encoding="utf-8"))
    tn = "omer-ajan-" + isim
    tr = f'"{PYW}" "{BU}" kos {isim}'
    subprocess.run(["schtasks", "/Create", "/TN", tn, "/TR", tr, "/SC", "ONCE", "/ST", "23:59", "/SD", "01/01/2030", "/F"], check=True, capture_output=True)
    r = subprocess.run(["schtasks", "/Run", "/TN", tn], capture_output=True, text=True)
    print("baslatildi", tn, r.returncode, r.stdout.strip()[:200], r.stderr.strip()[:200])

def hafif_bayrak(j, isim):
    """Varsayılan değişmez; iş json'u "mcp" / "eklenti" / "hafif" verirse o oturumda yalnız yükleme biçimi daralır (dosya silinmez)."""
    a = []
    if "mcp" in j:
        ks = json.load(open(os.path.expanduser("~/.claude.json"), encoding="utf-8")).get("mcpServers", {})
        cfg = os.path.join(KOK, isim + ".mcp.json")
        json.dump({"mcpServers": {k: ks[k] for k in j["mcp"] if k in ks}}, open(cfg, "w", encoding="utf-8"))
        a += ["--strict-mcp-config", "--mcp-config", cfg]
    if "eklenti" in j:
        ep = json.load(open(os.path.expanduser("~/.claude/settings.json"), encoding="utf-8")).get("enabledPlugins", {})
        cfg = os.path.join(KOK, isim + ".eklenti.json")
        json.dump({"enabledPlugins": {k: k in j["eklenti"] for k in ep}}, open(cfg, "w", encoding="utf-8"))
        a += ["--settings", cfg]
    if j.get("hafif"): a += ["--disable-slash-commands"]
    return a

def kos(isim):
    j = json.load(open(os.path.join(KOK, isim + ".json"), encoding="utf-8"))
    log = os.path.join(KOK, isim + ".log")
    kilit = os.path.join(KOK, isim + ".kilit")
    if os.path.exists(kilit):
        try:
            pid = int(open(kilit).read().strip())
            canli = str(pid) in subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True, creationflags=0x08000000).stdout.split()
        except Exception:
            canli = False
        if canli:
            return
        os.replace(kilit, kilit + "-eski")
    open(kilit, "w").write(str(os.getpid()))
    argv = [CLAUDE, "-p", "--output-format", "json", "--model", j.get("model", "sonnet")]
    if j.get("effort"): argv += ["--effort", j["effort"]]
    otf = os.path.join(KOK, isim + ".oturum")
    devam = j.get("devam_id")
    if not devam and not j.get("yeni_oturum") and os.path.exists(otf):
        try:
            o = json.load(open(otf, encoding="utf-8"))
            if o.get("temiz") and o.get("girdi", 0) < 120000:
                devam = o["session_id"]
        except Exception:
            pass
    if devam: argv += ["--resume", devam]
    argv += hafif_bayrak(j, isim)
    env = dict(os.environ); env.pop("CLAUDE_CODE_EFFORT_LEVEL", None)
    t0 = time.strftime("%H:%M")
    try:
        with open(log, "w", encoding="utf-8") as f:
            f.write(f"BASLADI {t0}\n"); f.flush()
            p = subprocess.Popen(argv, cwd=j["cwd"], stdin=subprocess.PIPE, stdout=f, stderr=subprocess.STDOUT,
                                 env=env, creationflags=0x08000000)
            p.stdin.write((j["gorev"] + f"\n\n[bütçe] En fazla {j.get('max_turns', 60)} tur kullan.").encode("utf-8")); p.stdin.close()
            def agac(): subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True, creationflags=0x08000000)
            bas = time.time(); sonuc_t = None
            while True:
                try:
                    kod = p.wait(timeout=15); break
                except subprocess.TimeoutExpired:
                    pass
                if time.time() - bas > j.get("timeout_sn", 5400):
                    agac(); kod = "zaman-asimi"; break
                if sonuc_t is None and '"type":"result"' in open(log, encoding="utf-8", errors="replace").read():
                    sonuc_t = time.time()
                if sonuc_t and time.time() - sonuc_t >= 30:
                    agac(); kod = "sonuc-sonrasi-kapatildi"; break
        open(log, "a", encoding="utf-8").write(f"\nBITTI {time.strftime('%H:%M')} kod {kod}\n")
        try:
            txt = open(log, encoding="utf-8", errors="replace").read()
            i = txt.rfind('{"type":"result"') if '{"type":"result"' in txt else txt.find("{")
            r = json.loads(txt[txt.find("{", i):txt.rfind("}") + 1])
            u = r.get("usage", {})
            g = u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
            json.dump({"session_id": r.get("session_id"), "temiz": kod in (0, "sonuc-sonrasi-kapatildi") and not r.get("is_error"), "girdi": g, "tarih": time.strftime("%Y-%m-%d %H:%M")}, open(otf, "w", encoding="utf-8"))
        except Exception as e:
            open(log, "a", encoding="utf-8").write(f"oturum kaydi yok: {e}\n")
    except Exception as e:
        open(log, "a", encoding="utf-8").write(f"\nHATA {time.strftime('%H:%M')} {e}\n")
    finally:
        os.remove(kilit)
        subprocess.run(["schtasks", "/Delete", "/TN", "omer-ajan-" + isim, "/F"], capture_output=True, creationflags=0x08000000)

if __name__ == "__main__":
    {"baslat": baslat, "kos": kos}[sys.argv[1]](sys.argv[2])
