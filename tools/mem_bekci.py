"""claude-mem bekçisi: worker (127.0.0.1:37777) kapalıysa pencere açmadan, hiçbir oturumun süreç ağacına bağlı olmadan yeniden başlatır.
Zamanlanmış görevden pythonw ile koşar (onay/mem_bekci.py). RAM >= %88 ise başlatmaz. Günlük: ~/.claude-mem/logs/mem-bekci.log"""
import ctypes
import os
import socket
import subprocess
import sys
import time

H = os.path.expanduser("~")
LOG = os.path.join(H, ".claude-mem", "logs", "mem-bekci.log")
KOK = r"C:\Projeler\omer-skills"
NODE_ADAY = [
    r"C:\Program Files\nodejs\node.exe",
    r"C:\Program Files\nodejs\node.exe",
]


class MEM(ctypes.Structure):
    _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong)] + [(n, ctypes.c_ulonglong) for n in ("t", "a", "tp", "ap", "tv", "av", "ae")]


def ram():
    m = MEM()
    m.dwLength = ctypes.sizeof(MEM)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.dwMemoryLoad


def acik():
    s = socket.socket()
    s.settimeout(1)
    try:
        return s.connect_ex(("127.0.0.1", 37777)) == 0
    finally:
        s.close()


def yaz(*a):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + " ".join(str(x) for x in a) + "\n")


def betikler():
    k = os.path.join(H, ".claude", "plugins", "cache", "thedotmack", "claude-mem")
    surumler = [v for v in os.listdir(k) if v[0].isdigit() and not os.path.exists(os.path.join(k, v, ".orphaned_at"))]
    surumler.sort(key=lambda v: [int(x) if x.isdigit() else 0 for x in v.split("-")[0].split(".")])
    return os.path.join(k, surumler[-1], "scripts")


def havuz_serve():
    """Ücretsiz havuzun yerel ucu (claude-mem yedeği, 20190) kapalıysa pencere açmadan başlatır."""
    s = socket.socket()
    s.settimeout(1)
    try:
        if s.connect_ex(("127.0.0.1", 20190)) == 0 or ram() >= 88:
            return
    finally:
        s.close()
    arg = [sys.executable, os.path.join(KOK, "tools", "ucretsiz_havuz.py"), "serve", "20190"]
    kw = dict(stdout=open(os.path.join(KOK, ".kos", "kopru", "ucretsiz", "serve.log"), "a", encoding="utf-8"), stderr=subprocess.STDOUT,
              stdin=subprocess.DEVNULL, cwd=KOK, close_fds=True)
    try:
        subprocess.Popen(arg, creationflags=0x08000000 | 0x00000200 | 0x01000000, **kw)
    except OSError:
        subprocess.Popen(arg, creationflags=0x08000000 | 0x00000200, **kw)
    yaz("havuz serve kapaliydi -> baslatildi")


def isit():
    # CM-CHROMA-FIX: soguk chroma dosyalari rastgele 4K okumayla (4,7 ms/op) dakikalar suruyor; ardisik okuma 200-370 MB/s
    d = os.path.join(H, ".claude-mem", "chroma")
    t = time.time()
    n = 0
    for kok, _, ds in os.walk(d):
        for ad in ds:
            if ad.endswith((".sqlite3", ".bin")):
                try:
                    with open(os.path.join(kok, ad), "rb", buffering=0) as f:
                        while True:
                            b = f.read(8 << 20)
                            if not b:
                                break
                            n += len(b)
                except OSError:
                    pass
    yaz("chroma isitildi", n >> 20, "MB", round(time.time() - t, 1), "sn")


def main():
    havuz_serve()
    if acik():
        return
    r = ram()
    if r >= 88:
        yaz("worker kapali ama RAM", r, "-> baslatilmadi")
        return
    isit()
    node = next((n for n in NODE_ADAY if os.path.exists(n)), "node")
    s = betikler()
    arg = [node, os.path.join(s, "bun-runner.js"), os.path.join(s, "worker-service.cjs"), "start"]
    bayrak = 0x08000000 | 0x00000200
    out = open(LOG, "a", encoding="utf-8")
    try:
        subprocess.Popen(arg, stdout=out, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, cwd=H, close_fds=True, creationflags=bayrak | 0x01000000)
    except OSError:
        subprocess.Popen(arg, stdout=out, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, cwd=H, close_fds=True, creationflags=bayrak)
    for _ in range(30):
        time.sleep(1)
        if acik():
            yaz("worker kapaliydi -> yeniden baslatildi, RAM", r)
            return
    yaz("worker 30 sn icinde acilmadi")


def beyin():
    """Yeni biten ajan-sira oturumlarını Obsidian kasasına al (BEYIN-2); bekçiyi asla düşürmez."""
    try:
        import beyin_kanca
        n = beyin_kanca.main()
        if n:
            yaz("beyin_kanca:", n, "yeni oturum kasaya alindi")
    except Exception as e:
        yaz("beyin_kanca hata:", repr(e)[:200])


def llama_bosta(onceki, pid, cpu, simdi):
    """ram-az-1: llama-server CPU süresi önceki gözlemden ≥60 sn beri değişmediyse boşta (saf)."""
    return bool(onceki) and onceki["pid"] == pid and onceki["cpu"] == cpu and simdi - onceki["t"] >= 60


def en_buyuk_bosta(liste):
    """ram-az-1: (ad, pid, MB, cpu%) listesinden CPU'su <%1 en büyük süreç; yoksa None (saf)."""
    adaylar = [(ad, pid, mb) for ad, pid, mb, cpu in liste if cpu < 1.0]
    return max(adaylar, key=lambda x: x[2]) if adaylar else None


def ram_rapor():
    """ram-az-1: RAM %84+ ise en büyük boşta süreci ram-olay.log'a yazar (öldürmez)."""
    import psutil
    r = ram()
    if r < 84:
        return
    ps = [p for p in psutil.process_iter(["name", "memory_info"]) if p.info["memory_info"]]
    for p in ps:
        p.cpu_percent(None)
    time.sleep(1)
    liste = []
    for p in ps:
        try:
            liste.append((p.info["name"], p.pid, p.info["memory_info"].rss // 2**20, p.cpu_percent(None)))
        except psutil.Error:
            pass
    b = en_buyuk_bosta(liste)
    if b:
        with open(os.path.join(KOK, ".kos", "kopru", "ram-olay.log"), "a", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + "RAM %%%d en buyuk bosta: %s pid=%d %d MB\n" % ((r,) + b))


def ollama_bosalt():
    """BULUT-1: yerel modeller RAM yemesin. llama-server ≥60 sn boştaysa boşaltır (ram-az-1); 11434'e bağlı süreçleri (çağıran) .kos/kopru/ram-olay.log'a yazar."""
    import json
    import urllib.request
    import psutil

    def istek(yol, veri=None):
        r = urllib.request.Request("http://127.0.0.1:11434" + yol, data=None if veri is None else json.dumps(veri).encode(),
                                   headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(r, timeout=10) as f:
            return json.loads(f.read() or b"{}")

    try:
        modeller = istek("/api/ps").get("models", [])
    except OSError:  # ollama kapalı
        return
    durum = os.path.join(KOK, ".kos", "kopru", "ollama-bosta.json")
    llama = [p for p in psutil.process_iter(["name"]) if (p.info["name"] or "").lower().startswith("llama-server")]
    if not modeller or not llama:
        return
    pid, cpu, simdi = llama[0].pid, round(sum(llama[0].cpu_times()[:2]), 2), time.time()
    try:
        onceki = json.load(open(durum, encoding="utf-8"))
    except (OSError, ValueError):
        onceki = None
    if not llama_bosta(onceki, pid, cpu, simdi):
        if not onceki or onceki["pid"] != pid or onceki["cpu"] != cpu:
            json.dump({"pid": pid, "cpu": cpu, "t": simdi}, open(durum, "w", encoding="utf-8"))
        return
    caglar = sorted({psutil.Process(c.pid).name() + ":" + str(c.pid) for c in psutil.net_connections("tcp")
                     if c.raddr and c.raddr.port == 11434 and c.pid})
    for m in modeller:
        ad = m.get("name") or m.get("model")
        istek("/api/generate", {"model": ad, "keep_alive": 0})
        with open(os.path.join(KOK, ".kos", "kopru", "ram-olay.log"), "a", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + "ollama bosaltildi %s %.1fGB cagiran=%s\n" % (ad, m.get("size", 0) / 1e9, ",".join(caglar) or "?"))


def sebepler(aktif,gozlem_yas_dk, kota_yas_dk):
    """Sağlık kararı (saf): aktif oturumda gözlem 30 dk'dan eski ya da son 30 dk'da kota/429 işareti."""
    s = []
    if aktif and (gozlem_yas_dk is None or gozlem_yas_dk > 30):
        s.append("gozlem sayisi 30 dk sabit (son gozlem %s dk)" % ("yok" if gozlem_yas_dk is None else int(gozlem_yas_dk)))
    if kota_yas_dk is not None and kota_yas_dk <= 30:
        s.append("kota/429 %d dk once" % kota_yas_dk)
    return s


def saglik():
    """Model çağırmaz, pencere açmaz. Sorun varsa .kos/kopru/mem-saglik.log + kasa 90-log notu (30 dk'da en çok bir kez)."""
    import json
    import sqlite3
    simdi = time.time()
    proj = os.path.join(H, ".claude", "projects")
    aktif = any(simdi - e.stat().st_mtime < 600 for d in os.scandir(proj) if d.is_dir() for e in os.scandir(d.path) if e.name.endswith(".jsonl"))
    db = sqlite3.connect("file:" + os.path.join(H, ".claude-mem", "claude-mem.db").replace("\\", "/") + "?mode=ro", uri=True)
    ep = db.execute("select max(created_at_epoch) from observations").fetchone()[0]
    yas = None if ep is None else (simdi - ep / (1000 if ep > 1e11 else 1)) / 60
    try:
        kota = json.load(open(os.path.join(H, ".claude-mem", "quota-cooldown.json"), encoding="utf-8"))
        kyas = min((simdi - k["armedAtMs"] / 1000) / 60 for k in kota)
    except (OSError, ValueError, KeyError):
        kyas = None
    s = sebepler(aktif, yas, kyas)
    log = os.path.join(KOK, ".kos", "kopru", "mem-saglik.log")
    if not s:
        # düzelme: son satır sorunsa bir kez "sağlıklı" yaz
        if os.path.exists(log) and "sağlıklı" not in open(log, encoding="utf-8").read().splitlines()[-1]:
            with open(log, "a", encoding="utf-8") as f:
                f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + "sağlıklı\n")
        return
    if os.path.exists(log) and simdi - os.path.getmtime(log) < 1800:
        return
    satir = time.strftime("%Y-%m-%d %H:%M:%S ") + "; ".join(s)
    with open(log, "a", encoding="utf-8") as f:
        f.write(satir + "\n")
    nota = os.path.join(r"C:\Users\pc\Desktop\Obsidian", "90-log", "mem-saglik-" + time.strftime("%Y-%m-%d") + ".md")
    with open(nota, "a", encoding="utf-8") as f:
        f.write("- " + satir + "\n")


if __name__ == "__main__":
    try:
        ollama_bosalt()
    except Exception as e:
        yaz("ollama_bosalt hata:", repr(e)[:200])
    try:
        ram_rapor()
    except Exception as e:
        yaz("ram_rapor hata:", repr(e)[:200])
    main()
    try:
        saglik()
    except Exception as e:
        yaz("saglik hata:", repr(e)[:200])
    try:  # yetim süreç temizliği (≥30 dk); günlük .kos/kopru/yetim.log
        subprocess.run([sys.executable, os.path.join(KOK, ".kos", "kopru", "yetim.py"), "durdur", "--yas", "30"],
                       capture_output=True, timeout=120, creationflags=0x08000000)
    except Exception as e:
        yaz("yetim hata:", repr(e)[:200])
    try:  # VRAM kilidi (≥%80 → .kos/kopru/vram-dolu; GPU işleri bekler)
        sys.path.insert(0, os.path.join(KOK, "tools"))
        import vram_bekci
        vram_bekci.kilit_guncelle(vram_bekci.yuzde_olc())
    except Exception as e:
        yaz("vram hata:", repr(e)[:200])
    try:  # RAM büyüme alarmı (log + uyku-ozet satırı; öldürmez)
        subprocess.run([sys.executable, os.path.join(KOK, "tools", "ram", "buyume.py")],
                       capture_output=True, timeout=120, creationflags=0x08000000)
    except Exception as e:
        yaz("buyume hata:", repr(e)[:200])
    if ram() < 95:
        beyin()
