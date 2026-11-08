import psutil, time, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
LOG = r"C:\Projeler\omer-skills\.kos\kopru\arka\kopru_bekci.log"
RAM_SERT = 92.0
YETIM_YAS = 120
KURAL = [
    ("agent-browser", 10 * 60),
    ("--remote-debugging-port", 15 * 60),
    ("_bt1_olc.py", 20 * 60),
    ("claude.exe -p", 130 * 60),
    ("yt-dlp", 20 * 60),
    ("gallery-dl", 20 * 60),
]
KORU = ("WindowsApps\\Claude", "toplu_gozetmen.py", "kopru_bekci.py", "video_derin.py", "arka_ajan.py",
        "omniroute", "worker-service.cjs", "mcp_paylasim.py", "yonetici_gorev.py", "ucretsiz_havuz.py",
        "vram_siper.py", "gpu_sinir.py", "mem_bekci.py", "ComfyUI", "comfyui", "ollama")
MCP_IZ = ("mcp", "gecit.mjs", "sunucu.mjs", "obsidian.mjs", "tasarim.mjs", "rea-mcp", "hermes.exe", "headroom",
          "chroma", "ruflo", "qmd.js", "gsc_server", "blender", "playwright", "puppeteer", "server-filesystem",
          "arxiv", "markitdown", "cmd.EXE /c", "uvx", "npx-cli.js", "stdio")
ISIM = ("node.exe", "python.exe", "pythonw.exe", "bun.exe", "uv.exe", "uvx.exe", "cmd.exe", "conhost.exe")


def yaz(s):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(time.strftime("%m-%d %H:%M:%S ") + s + "\n")


def oldur(p, neden):
    try:
        c = " ".join(p.cmdline())[:150]
        mb = p.memory_info().rss // 2**20
        for k in p.children(recursive=True):
            k.kill()
        p.kill()
        yaz(f"KAPATILDI pid={p.pid} {mb}MB neden={neden} | {c}")
        return mb
    except Exception as e:
        yaz(f"hata pid={p.pid} {e}")
        return 0


def yetim_mi(p):
    pp = p.ppid()
    if not pp or not psutil.pid_exists(pp):
        return True
    try:
        return psutil.Process(pp).create_time() > p.create_time()
    except Exception:
        return True


def tur():
    simdi = time.time()
    kazanc = 0
    for p in psutil.process_iter(["pid", "name", "cmdline", "create_time"]):
        try:
            c = " ".join(p.info["cmdline"] or [])
            if not c or any(k in c for k in KORU):
                continue
            yas = simdi - p.info["create_time"]
            n = (p.info["name"] or "").lower()
            if n in ISIM and yas > YETIM_YAS and any(k in c for k in MCP_IZ) and yetim_mi(p):
                kazanc += oldur(p, "yetim MCP (sahibi oturum kapanmis)")
                continue
            for desen, tavan in KURAL:
                if desen in c and yas > tavan:
                    kazanc += oldur(p, f"{desen} {int(yas / 60)}dk>{tavan // 60}dk")
                    break
        except Exception:
            pass
    ram = psutil.virtual_memory().percent
    if ram >= RAM_SERT:
        aday = []
        for p in psutil.process_iter(["pid", "cmdline", "memory_info"]):
            try:
                c = " ".join(p.info["cmdline"] or [])
                if any(k in c for k in KORU):
                    continue
                if ("claude.exe -p" in c or "agent-browser" in c or "--remote-debugging-port" in c) and p.info["memory_info"]:
                    aday.append((p.info["memory_info"].rss, p))
            except Exception:
                pass
        if aday:
            aday.sort(key=lambda x: -x[0])
            kazanc += oldur(aday[0][1], f"RAM {ram}%>={RAM_SERT}")
    return kazanc


if __name__ == "__main__":
    if "--bir" in sys.argv:
        print("kazanc MB", tur(), "| RAM%", psutil.virtual_memory().percent)
        sys.exit()
    yaz("BASLADI")
    while True:
        try:
            k = tur()
            if k:
                yaz(f"tur kazanc {k}MB RAM {psutil.virtual_memory().percent}%")
        except Exception as e:
            yaz(f"tur hata {e}")
        time.sleep(30)
