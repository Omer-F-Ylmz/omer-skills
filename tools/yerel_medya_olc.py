"""YEREL-MEDYA-1 ölçüm koşucusu: ComfyUI'yı başsız açar, API akışını gönderir, 1 sn'de VRAM+RAM tepe örnekler.
Kullanım: python yerel_medya_olc.py <akis.json> <etiket> [--dolgu anahtar=deger ...]
Çıktı: tmp/yerel-medya/<etiket>.json (süre · vram_tepe_mib · ram_tepe_gb · dosyalar). ComfyUI iş bitince kapanır."""
import json, os, subprocess, sys, time, threading, urllib.request, uuid
from pathlib import Path
import psutil

COMFY = Path(r"C:\AI\ComfyUI")
CIKTI = Path(__file__).resolve().parent.parent / "tmp" / "yerel-medya"
SUNUCU = "http://127.0.0.1:8188"
RAM_TAVAN_GB = 28.5  # toplam RAM %89
VRAM_TAVAN_MIB = 11637  # %95 (Ömer 02.11; önce 9800 = %80)


def vram_mib():
    r = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"], capture_output=True, text=True)
    return int(r.stdout.split()[0])


def agac_ram_gb(p):
    try:
        toplam = p.memory_info().rss
        for c in p.children(recursive=True):
            toplam += c.memory_info().rss
        return toplam / 2**30
    except psutil.Error:
        return 0.0


def http(yol, veri=None):
    req = urllib.request.Request(SUNUCU + yol, data=json.dumps(veri).encode() if veri else None, headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())


def main():
    akis_yol, etiket = sys.argv[1], sys.argv[2]
    akis = json.loads(Path(akis_yol).read_text(encoding="utf-8"))
    CIKTI.mkdir(parents=True, exist_ok=True)
    kok = psutil.virtual_memory().used / 2**30
    proc = subprocess.Popen([str(COMFY / ".venv" / "Scripts" / "python.exe"), "main.py", "--listen", "127.0.0.1", "--port", "8188", "--disable-auto-launch", "--cache-none", *os.environ.get("YM1_EK", "").split()],
                            cwd=COMFY, creationflags=0x08000000, env={**os.environ, "HF_HUB_DISABLE_TELEMETRY": "1", "PYTHONUTF8": "1"}, stdout=open(CIKTI / f"{etiket}.log", "wb"), stderr=subprocess.STDOUT)
    p = psutil.Process(proc.pid)
    for _ in range(180):
        try:
            http("/system_stats"); break
        except Exception:
            time.sleep(1)
    tepe = {"vram": 0, "ram": 0.0, "sistem_ram": 0.0, "fren": None}
    dur = threading.Event()

    def ornekle():
        while not dur.is_set():
            tepe["vram"] = max(tepe["vram"], vram_mib())
            tepe["ram"] = max(tepe["ram"], agac_ram_gb(p))
            sis = psutil.virtual_memory().used / 2**30
            tepe["sistem_ram"] = max(tepe["sistem_ram"], sis)
            if sis > RAM_TAVAN_GB:
                tepe["fren"] = f"RAM {sis:.1f} GB > {RAM_TAVAN_GB}"
                dur.set()
            time.sleep(1)

    th = threading.Thread(target=ornekle, daemon=True); th.start()
    t0 = time.time()
    pid = http("/prompt", {"prompt": akis, "client_id": str(uuid.uuid4())})["prompt_id"]
    durum = "zaman_asimi"
    while time.time() - t0 < 1800 and not dur.is_set():
        h = http(f"/history/{pid}")
        if pid in h:
            durum = h[pid]["status"]["status_str"]; sonuc = h[pid]; break
        time.sleep(2)
    sure = time.time() - t0
    dur.set(); th.join()
    dosyalar, hata = [], None
    if tepe["fren"]:
        durum = "fren"
    elif durum == "success":
        for cikti in sonuc["outputs"].values():
            for k in ("images", "videos", "gifs"):
                for f in cikti.get(k, []):
                    dosyalar.append(str(COMFY / "output" / f.get("subfolder", "") / f["filename"]))
    elif durum == "error":
        hata = [m for m in sonuc["status"]["messages"] if m[0] == "execution_error"]
    for c in p.children(recursive=True):
        c.kill()
    proc.kill()
    out = {"etiket": etiket, "durum": durum, "sure_sn": round(sure, 1), "vram_tepe_mib": tepe["vram"], "vram_taban_mib": None,
           "comfy_ram_tepe_gb": round(tepe["ram"], 2), "sistem_ram_tepe_gb": round(tepe["sistem_ram"], 1), "sistem_ram_baslangic_gb": round(kok, 1),
           "fren": tepe["fren"], "dosyalar": dosyalar, "hata": str(hata)[:600] if hata else None}
    (CIKTI / f"{etiket}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
