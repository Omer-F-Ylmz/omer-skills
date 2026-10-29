"""ARKA-SIRA-1: arka_ajan kuyruğunu kendiliğinden yürütür (Claude yok, $0).
  python tools/arka_sira.py            tek tur (Görev Zamanlayıcı 5 dk'da bir çağırır)
  python tools/arka_sira.py --kur      "omer-arka-sira" zamanlanmış görevini kurar (pythonw, pencere yok)
  python tools/arka_sira.py --durum    kuyruk + çalışanlar
Kuyruk: .kos/kopru/arka/_sira.txt (satır başına iş adı; aynı ad tekrar yazılabilir = yeni tur).
Kural: aynı anda en fazla PARALEL iş; RAM >= RAM_TAVAN veya GPU/VRAM >= 80 ise başlatmaz.
Önceki turu olan işe sonucu 'devam_notu' olarak verilir ve kayıtlı oturumdan --resume edilir."""
import json
import os
import subprocess
import sys
import time

import psutil

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARKA = os.path.join(KOK, ".kos", "kopru", "arka")
SIRA = os.path.join(ARKA, "_sira.txt")
LOG = os.path.join(ARKA, "_sira.log")
AJAN = os.path.join(KOK, "tools", "arka_ajan.py")
PARALEL = 2
RAM_TAVAN = 85.0
GPU_TAVAN = 80.0
PENCERE_YOK = 0x08000000
GOREV = "omer-arka-sira"


def log(s):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M ") + s + "\n")


def canli_isler():
    out = []
    claude_cmd = []
    for p in psutil.process_iter(["name", "cmdline"]):
        try:
            if (p.info["name"] or "").lower() == "claude.exe":
                claude_cmd.append(" ".join(p.info["cmdline"] or []))
        except psutil.Error:
            pass
    for ad in os.listdir(ARKA):
        if ad.endswith(".json") and not ad.endswith((".mcp.json", ".eklenti.json")) and not ad.startswith("_"):
            isim = ad[:-5]
            if any(isim + ".mcp.json" in c or isim + ".eklenti.json" in c for c in claude_cmd):
                out.append(isim)
    for ad in os.listdir(ARKA):
        if not ad.endswith(".kilit"):
            continue
        try:
            pid = int(open(os.path.join(ARKA, ad)).read().strip() or 0)
        except (OSError, ValueError):
            continue
        try:
            cmd = " ".join(psutil.Process(pid).cmdline()) if pid else ""
        except (psutil.Error, OSError):
            cmd = ""
        if "arka_ajan" in cmd and ad[:-6] in cmd and ad[:-6] not in out:
            out.append(ad[:-6])
    return out


def gpu():
    try:
        r = subprocess.run(["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total", "--format=csv,noheader,nounits"],
                           capture_output=True, text=True, timeout=10, creationflags=PENCERE_YOK)
        u, m, t = [float(x) for x in r.stdout.strip().split(",")[:3]]
        return max(u, 100 * m / t)
    except Exception:
        return 0.0


def kuyruk():
    try:
        return [s.strip() for s in open(SIRA, encoding="utf-8") if s.strip() and not s.startswith("#")]
    except OSError:
        return []


def yaz_kuyruk(k):
    with open(SIRA, "w", encoding="utf-8") as f:
        f.write("\n".join(k) + ("\n" if k else ""))


def onceki_sonuc(ad):
    p = os.path.join(ARKA, ad + ".log")
    if not os.path.exists(p):
        return ""
    t = open(p, encoding="utf-8", errors="replace").read()
    i = t.rfind('"result":"')
    return t[i + 10:i + 10 + 900].replace("\\n", " ") if i >= 0 else ""


def ram_bekci():
    if psutil.virtual_memory().percent < 92:
        return
    adaylar = []
    for p in psutil.process_iter(["name", "cmdline"]):
        try:
            if (p.info["name"] or "").lower() != "claude.exe" or " -p " not in " " + " ".join(p.info["cmdline"] or []) + " ":
                continue
            for c in p.children(recursive=True):
                n = c.name().lower()
                if n in ("claude.exe", "node.exe", "conhost.exe"):
                    continue
                adaylar.append((c.memory_info().rss, c))
        except psutil.Error:
            pass
    if not adaylar:
        log(f"RAM {psutil.virtual_memory().percent} >=92 ama oldurulecek is alt sureci yok")
        return
    rss, c = max(adaylar, key=lambda x: x[0])
    if rss < 2 * 2**30:
        log(f"RAM yuksek ama en buyuk alt surec {rss/2**30:.1f}G (<2G), dokunulmadi")
        return
    cmd = " ".join(c.cmdline())[:150]
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(c.pid)], capture_output=True, creationflags=PENCERE_YOK)
    log(f"RAM-BEKCI oldurdu pid={c.pid} {rss/2**30:.1f}G :: {cmd}")


OYUN_YOL = ("\\epic games\\", "\\steamapps\\", "\\riot games\\", "\\hoyoplay\\", "\\xboxgames\\")


def oyun_acik():
    """Yalnız bilgi (Ömer 24 Eki: oyun açıkken arka işler DURMAZ, tek sınır RAM eşiği) — tur() bunu kullanmaz."""
    for p in psutil.process_iter(["exe", "name"]):
        try:
            yol = (p.info["exe"] or "").lower()
            if any(o in yol for o in OYUN_YOL) and "launcher" not in yol and "launcher" not in (p.info["name"] or "").lower():
                return p.info["name"]
        except psutil.Error:
            pass
    return ""


def tur():
    ram_bekci()
    try:
        import arka_oto  # ARKA-OTO-1: biten işleri Claude'suz değerlendir, özet/bildirim; hata turu düşürmez
        arka_oto.tara()
    except Exception as e:
        log(f"OTO hata {type(e).__name__}: {e}")
    k = kuyruk()
    if not k:
        return
    canli = canli_isler()
    ram = psutil.virtual_memory().percent
    g = gpu()
    if len(canli) >= PARALEL or ram >= RAM_TAVAN or g >= GPU_TAVAN:
        return
    for i, ad in enumerate(k):
        if ad in canli:
            continue
        js = os.path.join(ARKA, ad + ".json")
        if not os.path.exists(js):
            log(f"ATLA {ad}: json yok")
            k.pop(i)
            yaz_kuyruk(k)
            return
        try:
            j = json.load(open(js, encoding="utf-8"))
        except ValueError as e:
            log(f"ATLA {ad}: json bozuk ({e}); kuyrukta kaldi, siradakine geciliyor")
            continue
        if any(b in canli or b in k[:i] or not onceki_sonuc(b) for b in j.get("bekle", [])):
            continue
        onceki = onceki_sonuc(ad)
        if onceki:
            eski = j.get("devam_notu", "") or ""
            if eski.startswith("DEVAM (otomatik"):
                b = eski.find("\nDESKTOP YÖNÜ")
                yon = eski[b:].split(":\n", 1)[1].strip() if b >= 0 and ":\n" in eski[b:] else ""
            else:
                yon = eski.strip()
            j["devam_notu"] = ("DEVAM (otomatik kuyruk, " + time.strftime("%d %b %H:%M") + "): önceki tur sonucu: «" + onceki +
                               "». Önceki turu TEKRARLAMA; ilerleme dosyası + git log'dan kaldığın yeri bul.\n" +
                               ("\nDESKTOP YÖNÜ (bağlayıcı, önceki tur sonucundan önce gelir):\n" + yon + "\n" if yon else ""))
            j["yeni_oturum"] = False
        json.dump(j, open(js, "w", encoding="utf-8"), ensure_ascii=False)
        r = subprocess.run([sys.executable, AJAN, "baslat", ad], capture_output=True, text=True, creationflags=PENCERE_YOK)
        k.pop(i)
        yaz_kuyruk(k)
        log(f"BASLAT {ad} kod={r.returncode} ram={ram} gpu={g:.0f} canli={canli}")
        return


def durdur(ad):
    try:
        pid = int(open(os.path.join(ARKA, ad + ".kilit")).read().strip())
    except (OSError, ValueError):
        print("kilit yok", ad)
        return
    cmd = " ".join(psutil.Process(pid).cmdline()) if psutil.pid_exists(pid) else ""
    if "arka_ajan" not in cmd or ad not in cmd:
        print("canli is degil", ad, pid)
        return
    r = subprocess.run(["taskkill", "/T", "/F", "/PID", str(pid)], capture_output=True, text=True, creationflags=PENCERE_YOK)
    log(f"DURDUR {ad} pid={pid} kod={r.returncode}")
    print("durduruldu", ad, r.returncode)


def kur():
    pyw = sys.executable.replace("python.exe", "pythonw.exe")
    tr = f'"{pyw}" "{os.path.abspath(__file__)}"'
    r = subprocess.run(["schtasks", "/Create", "/TN", GOREV, "/TR", tr, "/SC", "MINUTE", "/MO", "5", "/F"], capture_output=True, text=True)
    print(r.returncode, r.stdout.strip(), r.stderr.strip())


def durum():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("canli:", canli_isler(), "RAM", psutil.virtual_memory().percent, "GPU/VRAM", round(gpu()))
    print("kuyruk:", kuyruk())
    if os.path.exists(LOG):
        print("".join(open(LOG, encoding="utf-8").readlines()[-8:]))


if __name__ == "__main__":
    a = sys.argv[1] if len(sys.argv) > 1 else ""
    if a == "--kur":
        kur()
    elif a == "--durdur":
        durdur(sys.argv[2])
    elif a == "--durum":
        durum()
    else:
        tur()
