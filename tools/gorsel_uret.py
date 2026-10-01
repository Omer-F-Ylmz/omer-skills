"""Yerel görsel üretimi: ac · uret · buyut · arkaplan · kapat · durum (KURULUM-GÖRSEL).

Çıkış: 0 tamam · 1 açılamadı/üretilemedi (süreç yalnız PID ile kapatılır) · 2 kural ihlali, hiçbir şey başlatılmadı.
Kurallar: çıktı yalnız <Masaüstü>\\<Proje>\\ altında; ComfyUI yalnız 127.0.0.1:8188; Blender (9876) açıkken GPU işi yok;
uzak API yok (HF indirmesi yalnız kurulumda). Her PNG'nin yanına aynı adlı .json (model · lisans · prompt · tohum · boyut · süre).
"""
import argparse
import csv
import ctypes
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from pathlib import Path

import gpu_kilit as gk  # tools/ betik klasörü; BLENDER-ARAC-2 K1 GPU kilidi

MASAUSTU = Path.home() / "Desktop"
DURUM = Path(tempfile.gettempdir()) / "gorsel-oturum.json"
COMFY = Path(r"C:\AI\ComfyUI")
REMBG = Path(r"C:\AI\rembg\.venv\Scripts\rembg.exe")
AKISLAR = Path(__file__).resolve().parent / "gorsel" / "akislar"
HOST, PORT, BLENDER_PORT = "127.0.0.1", 8188, 9876
SUNUCU = f"http://{HOST}:{PORT}"
ACILIS_SN, BEKLE_SN = 180, 600
ALTYAPI = {"node.exe", "bun.exe", "claude.exe", "uv.exe", "uvx.exe", "dotnet.exe", "python.exe", "pythonw.exe",
           "msmpeng.exe", "csrss.exe", "winlogon.exe", "dwm.exe", "explorer.exe", "system", "memory compression"}
FREN_GB = 2

VARSAYILAN_RAM_GB = 16  # MODELLER[m]["ram_gb"] yoksa; K6 tepe RAM + 2 GB ile değişir
BUYUT_RAM_GB = 3.5  # K6 buyut tepe 1.5 GB + 2

MODELLER = {
    "zimage": {"ram_gb": 4.4, "akis": "zimage.json", "lisans": "Apache-2.0 (Tongyi-MAI/Z-Image-Turbo · Comfy-Org/z_image_turbo)",
               "dosyalar": ["diffusion_models/z_image_turbo_fp8_e4m3fn.safetensors", "text_encoders/qwen_3_4b_fp8_mixed.safetensors",
                            "vae/ae.safetensors"]},
    "klein": {"ram_gb": 4.5, "akis": "klein.json", "lisans": "Apache-2.0 (black-forest-labs/FLUX.2-klein-4B · Comfy-Org/flux2-klein-4B)",
              "dosyalar": ["diffusion_models/flux-2-klein-4b.safetensors", "text_encoders/qwen_3_4b_fp8_mixed.safetensors",
                           "vae/flux2-vae.safetensors"]},
    # K2b: RAM 31.7 GB < 32 GB → kurulmadı; yönlendirilirse exit 2.
    "qwen-image": {"akis": None, "lisans": "Apache-2.0 (Qwen/Qwen-Image)",
                   "dosyalar": ["diffusion_models/qwen_image_fp8_e4m3fn.safetensors"]},
}
BUYUTUCU = ("upscale_models/RealESRGAN_x4plus.safetensors", "BSD-3-Clause (xinntao/Real-ESRGAN · Comfy-Org/Real-ESRGAN_repackaged)")
# K6 ölçümüyle seçildi: docs/gorsel/olcum.md
YONLENDIRME = {"foto": "zimage", "urun": "zimage", "doku": "zimage", "metinli": "klein", "duzenle": "klein"}


def yol_gecerli(klasor):
    try:
        return len(klasor.resolve().relative_to(MASAUSTU.resolve()).parts) >= 1
    except ValueError:
        return False


def dinleyenler(port):
    cikti = subprocess.run(["netstat", "-ano", "-p", "TCP"], capture_output=True, text=True, errors="replace").stdout
    cikti += subprocess.run(["netstat", "-ano", "-p", "TCPv6"], capture_output=True, text=True, errors="replace").stdout
    return [(p[1], int(p[4])) for p in (s.split() for s in cikti.splitlines())
            if len(p) == 5 and p[0] == "TCP" and p[1].endswith(f":{port}") and p[2].endswith(":0")]


def pid_canli(pid):
    cikti = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True, errors="replace").stdout
    return "python.exe" in cikti.lower() and str(pid) in cikti


def oldur(pid):
    # Yalnız PID ile (/T: venv başlatıcısının çocuğu ComfyUI); ad ile öldürme bu araçta yok.
    if pid_canli(pid):
        subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True, text=True, errors="replace")


def oturum_pid():
    pid = json.loads(DURUM.read_text(encoding="utf-8"))["pid"] if DURUM.exists() else None
    return pid if pid and pid_canli(pid) else None


def blender_acik():
    if dinleyenler(BLENDER_PORT):
        print(f"DUR: {BLENDER_PORT} dinleniyor; Blender GPU'yu kullanıyor, önce blender_oturum kapat")
        return True
    return False


def bos_ram_gb():
    class Durum(ctypes.Structure):
        _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong)] + \
                   [(ad, ctypes.c_ulonglong) for ad in ("toplam", "bos", "tsd", "bsd", "tsan", "bsan", "bgen")]
    d = Durum(dwLength=ctypes.sizeof(Durum))
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(d))
    return round(d.bos / 2**30, 1)


def ram_yeter(gerekli):
    bos = bos_ram_gb()
    if bos >= gerekli:
        return True
    toplam, comfy = {}, str(oturum_pid())
    for satir in csv.reader(subprocess.run(["tasklist", "/fo", "csv", "/nh"], capture_output=True, text=True).stdout.splitlines()):
        # Altyapı (MCP sunucuları, korunan araçlar, ComfyUI, oturum 0 servisleri) asla kapatma önerisi olmaz.
        # tasklist yol göstermez → python.exe tümden hariç.
        if len(satir) >= 5 and satir[0].lower() not in ALTYAPI and "headroom" not in satir[0].lower() \
                and satir[1] != comfy and satir[3] != "0":
            toplam[satir[0]] = toplam.get(satir[0], 0) + int("0" + "".join(c for c in satir[4] if c.isdigit()))
    ilk3 = sorted(toplam.items(), key=lambda x: -x[1])[:3]
    print(f"{gerekli} GB lazım, {bos} GB boş; en çok bellek tutan 3 süreç: "
          + ", ".join(f"{ad} {kb / 2**20:.1f} GB" for ad, kb in ilk3))
    return False


def ac():
    if blender_acik() or not ram_yeter(min(m.get("ram_gb", VARSAYILAN_RAM_GB) for m in MODELLER.values())):
        return 2
    if dinleyenler(PORT):
        if oturum_pid():
            print(f"zaten açık: PID {oturum_pid()}")
            return 0
        print(f"DUR: {PORT} başka bir süreçte; bu araç başlatmadı, dokunulmaz")
        return 2
    if (m := gk.al("gorsel_uret", os.getpid())):
        print(f"DUR: {m}")
        return 2
    komut = [str(COMFY / ".venv" / "Scripts" / "python.exe"), "main.py", "--listen", HOST, "--port", str(PORT),
             "--disable-auto-launch", "--cache-ram"]
    with open(DURUM.with_suffix(".log"), "w", encoding="utf-8") as log:
        pid = subprocess.Popen(komut, cwd=COMFY, stdout=log, stderr=subprocess.STDOUT,
                               creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP).pid
    gk.al("gorsel_uret", pid)  # kilit ComfyUI süreciyle yaşar; süreç ölürse kendiliğinden düşer
    for _ in range(ACILIS_SN):
        time.sleep(1)
        d = dinleyenler(PORT)
        if any(adres.rsplit(":", 1)[0] != HOST for adres, _ in d):
            oldur(pid)
            gk.birak("gorsel_uret")
            print(f"DUR: {HOST} dışı dinleme {d}; süreç PID {pid} kapatıldı")
            return 1
        if d:
            DURUM.write_text(json.dumps({"pid": pid, "baslangic": time.time()}), encoding="utf-8")
            print(f"açık: {SUNUCU} · PID {pid}")
            return 0
    oldur(pid)
    gk.birak("gorsel_uret")
    print(f"DUR: {ACILIS_SN} sn içinde {PORT} dinlenmedi; PID {pid} kapatıldı · log {DURUM.with_suffix('.log')}")
    return 1


def kapat():
    if not DURUM.exists():
        print("oturum yok")
        return 0
    pid = json.loads(DURUM.read_text(encoding="utf-8")).get("pid")
    oldur(pid)
    for _ in range(15):  # port bırakılmadan dönülürse hemen ardından gelen ac 8188'i yabancı sanır
        if not dinleyenler(PORT):
            break
        time.sleep(1)
    DURUM.unlink()
    gk.birak("gorsel_uret")
    print(f"kapatıldı: PID {pid}")
    return 0


def durum():
    print(f"port {PORT}: {dinleyenler(PORT) or 'kapalı'} · PID {oturum_pid() or 'yok'}"
          f" · modeller {[m for m in MODELLER if kurulu(m)]}")
    return 0


def kurulu(model):
    return all((COMFY / "models" / d).is_file() for d in MODELLER[model]["dosyalar"])


def doldur(dugum, degerler):
    if isinstance(dugum, dict):
        return {k: doldur(v, degerler) for k, v in dugum.items()}
    if isinstance(dugum, str) and dugum.startswith("$"):
        return degerler[dugum[1:]]
    return dugum


def girdiye_kopyala(png):
    (COMFY / "input").mkdir(exist_ok=True)
    shutil.copyfile(png, COMFY / "input" / png.name)
    return png.name


def kuyruk(akis):
    istek = urllib.request.Request(f"{SUNUCU}/prompt", data=json.dumps({"prompt": akis}).encode(),
                                   headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(istek) as r:
        pid = json.load(r)["prompt_id"]
    ilk = en_az = bos_ram_gb()
    for _ in range(BEKLE_SN):
        en_az = min(en_az, bos_ram_gb())
        if en_az < FREN_GB:  # acil fren: sistem donmadan ComfyUI ağacı PID ile kapatılır
            oldur(json.loads(DURUM.read_text(encoding="utf-8"))["pid"])
            DURUM.unlink()
            raise RuntimeError(f"RAM {FREN_GB} GB altına indi, ComfyUI kapatıldı · iş başında boş {ilk} GB → şimdi {en_az} GB")
        with urllib.request.urlopen(f"{SUNUCU}/history/{pid}") as r:
            gecmis = json.load(r)
        if pid in gecmis:
            break
        time.sleep(1)
    else:
        raise TimeoutError(f"{BEKLE_SN} sn içinde bitmedi")
    resimler = [g for c in gecmis[pid]["outputs"].values() for g in c.get("images", [])]
    if not resimler:
        raise RuntimeError(f"çıktı yok: {gecmis[pid].get('status')}")
    return [urllib.request.urlopen(f"{SUNUCU}/view?{urllib.parse.urlencode(g)}").read() for g in resimler]


def yaz(png, veri, meta):
    png.write_bytes(veri)
    png.with_suffix(".json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    print(png)


def referans_zinciri(akis, adlar):
    pos, neg = "23", "24"
    for k, ad in enumerate(adlar[1:], 1):
        i = [str(20 + 5 * k + j) for j in range(5)]
        akis[i[0]] = {"class_type": "LoadImage", "inputs": {"image": ad}}
        akis[i[1]] = {"class_type": "ImageScaleToTotalPixels", "inputs": {**akis["21"]["inputs"], "image": [i[0], 0]}}
        akis[i[2]] = {"class_type": "VAEEncode", "inputs": {"pixels": [i[1], 0], "vae": ["3", 0]}}
        akis[i[3]] = {"class_type": "ReferenceLatent", "inputs": {"conditioning": [pos, 0], "latent": [i[2], 0]}}
        akis[i[4]] = {"class_type": "ReferenceLatent", "inputs": {"conditioning": [neg, 0], "latent": [i[2], 0]}}
        pos, neg = i[3], i[4]
    akis["6"]["inputs"].update(positive=[pos, 0], negative=[neg, 0])
    return akis


def uret(a):
    cikti, refler = Path(a.cikti), [Path(r) for r in a.referans or []]
    if not 1 <= a.adet <= 4:
        print("DUR: --adet 1-4")
        return 2
    if (a.is_ == "duzenle") != bool(refler) or not all(r.is_file() for r in refler):
        print("DUR: --referans yalnız --is duzenle ile ve var olan dosyalarla; duzenle en az bir referans ister")
        return 2
    if not yol_gecerli(cikti):
        print(f"DUR: {cikti} <Masaüstü>\\<Proje>\\ altında değil")
        return 2
    try:
        gen, yuk = (int(x) for x in a.boyut.lower().split("x"))
    except ValueError:
        print("DUR: --boyut WxH")
        return 2
    model = a.model or YONLENDIRME[a.is_]
    if a.is_ == "duzenle" and model != "klein":
        print("DUR: referanslı düzenleme yalnız klein ile")
        return 2
    if not kurulu(model):
        print(f"DUR: {model} kurulu değil (docs/gorsel/modeller.md)")
        return 2
    if blender_acik():
        return 2
    if not oturum_pid():
        print("DUR: ComfyUI kapalı; önce `gorsel_uret.py ac`")
        return 2
    if (m := gk.al("gorsel_uret", oturum_pid())):
        print(f"DUR: {m}")
        return 2
    if not ram_yeter(MODELLER[model].get("ram_gb", VARSAYILAN_RAM_GB)):
        return 2
    oturum = json.loads(DURUM.read_text(encoding="utf-8"))
    if oturum.get("model", model) != model:
        istek = urllib.request.Request(f"{SUNUCU}/free", data=json.dumps({"unload_models": True, "free_memory": True}).encode(),
                                       headers={"Content-Type": "application/json"})
        urllib.request.urlopen(istek).close()
    DURUM.write_text(json.dumps({**oturum, "model": model}), encoding="utf-8")
    cikti.mkdir(parents=True, exist_ok=True)
    tohum =random.randrange(2**31) if a.tohum is None else a.tohum
    adlar = [girdiye_kopyala(r) for r in refler]
    sablon = json.loads((AKISLAR / ("klein_duzenle.json" if refler else MODELLER[model]["akis"])).read_text(encoding="utf-8"))
    for t in range(tohum, tohum + a.adet):
        akis = doldur(sablon, {"PROMPT": a.prompt, "TOHUM": t, "GEN": gen, "YUK": yuk, "REF": adlar[0] if adlar else ""})
        if refler:
            akis = referans_zinciri(akis, adlar)
        bas = time.time()
        try:
            veri = kuyruk(akis)[0]
        except Exception as ex:
            print(f"HATA: {ex}")
            return 1
        meta = {"model": model, "lisans": MODELLER[model]["lisans"], "prompt": a.prompt, "tohum": t,
                "boyut": f"{gen}x{yuk}", "sure": round(time.time() - bas, 1), "is": a.is_, "referans": [str(r) for r in refler]}
        yaz(cikti / f"{a.is_}-{model}-{t}-{int(bas)}.png", veri, meta)
    return 0


def girdi_gecerli(png):
    if png.suffix.lower() == ".png" and png.is_file() and yol_gecerli(png.parent):
        return True
    print(f"DUR: {png} <Masaüstü>\\<Proje>\\ altında bir .png değil")
    return False


def buyut(png, kat):
    if not girdi_gecerli(png) or blender_acik():
        return 2
    if not (COMFY / "models" / BUYUTUCU[0]).is_file() or not oturum_pid():
        print("DUR: büyütücü kurulu değil ya da ComfyUI kapalı")
        return 2
    if not ram_yeter(BUYUT_RAM_GB):
        return 2
    akis = doldur(json.loads((AKISLAR / "buyut.json").read_text(encoding="utf-8")),
                  {"GIRDI": girdiye_kopyala(png), "OLCEK": kat / 4})
    bas = time.time()
    try:
        veri = kuyruk(akis)[0]
    except Exception as ex:
        print(f"HATA: {ex}")
        return 1
    yaz(png.with_name(f"{png.stem}-x{kat}.png"), veri, {"model": "RealESRGAN_x4plus", "lisans": BUYUTUCU[1],
                                                        "girdi": str(png), "kat": kat, "sure": round(time.time() - bas, 1)})
    return 0


def arkaplan(png):
    if not girdi_gecerli(png):
        return 2
    cikti, bas = png.with_name(f"{png.stem}-arkaplansiz.png"), time.time()
    # rembg varsayılanı bria-rmbg ticari lisans ister; model her zaman açıkça birefnet-general.
    r = subprocess.run([str(REMBG), "i", "-m", "birefnet-general", str(png), str(cikti)],
                       capture_output=True, text=True, errors="replace")
    if r.returncode != 0 or not cikti.is_file():
        print(f"HATA: rembg {r.returncode}")
        return 1
    cikti.with_suffix(".json").write_text(json.dumps(
        {"model": "birefnet-general (rembg)", "lisans": "MIT (danielgatis/rembg · ZhengPeng7/BiRefNet)",
         "girdi": str(png), "sure": round(time.time() - bas, 1)}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(cikti)
    return 0


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(prog="gorsel_uret")
    alt = ap.add_subparsers(dest="komut", required=True)
    alt.add_parser("ac")
    alt.add_parser("kapat")
    alt.add_parser("durum")
    u = alt.add_parser("uret")
    u.add_argument("--is", dest="is_", required=True, choices=list(YONLENDIRME))
    u.add_argument("--model", choices=list(MODELLER))
    u.add_argument("--prompt", required=True)
    u.add_argument("--cikti", required=True)
    u.add_argument("--adet", type=int, default=1)
    u.add_argument("--boyut", default="1024x1024")
    u.add_argument("--tohum", type=int)
    u.add_argument("--referans", nargs="+")
    b = alt.add_parser("buyut")
    b.add_argument("png")
    b.add_argument("--kat", type=int, choices=[2, 4], default=2)
    alt.add_parser("arkaplan").add_argument("png")
    a = ap.parse_args(argv)
    if a.komut == "uret":
        return uret(a)
    if a.komut in ("buyut", "arkaplan"):
        return buyut(Path(a.png), a.kat) if a.komut == "buyut" else arkaplan(Path(a.png))
    return {"ac": ac, "kapat": kapat, "durum": durum}[a.komut]()


if __name__ == "__main__":
    sys.exit(main())
