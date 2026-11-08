"""scroll-cinematic ücretsiz yerel hat: gorsel (Z-Image) · klip (Wan 2.2 TI2V 5B, ComfyUI) · kare (ffmpeg).
Not: gorsel --cikti yalnız Masaüstü<Proje> altına yazar.
Kullanım: python yerel_hat.py gorsel --prompt "..." --cikti hero.png
          python yerel_hat.py klip --gorsel hero.png --hareket "..." --cikti spin.mp4
          python yerel_hat.py kare --video spin.mp4 --cikti frames/spin [--adet 180] [--genislik 1600]
gorsel/klip omer-skills deposunu ister (OMER_SKILLS env, varsayılan C:/Projeler/omer-skills); kare yalnız ffmpeg ister."""
import argparse, json, os, shutil, subprocess, sys, time, urllib.request, uuid
R = os.environ.get("OMER_SKILLS", r"C:\Projeler\omer-skills")
U = "http://127.0.0.1:8188"
NEG = "blurry, distorted, warped, morphing objects, flicker, text, watermark, logo, low quality, cartoon, people, hands"

def req(p, data=None, ct="application/json"):
    r = urllib.request.Request(U + p, data=data, headers={"Content-Type": ct} if data else {})
    return json.loads(urllib.request.urlopen(r, timeout=60).read() or b"{}")

def acik():
    try: urllib.request.urlopen(U + "/system_stats", timeout=5); return True
    except Exception: return False

def arac(*a): return subprocess.run([sys.executable, os.path.join(R, "tools", "gorsel_uret.py"), *a], cwd=R)

def bos_gb():
    try:
        import psutil; return psutil.virtual_memory().available / 1e9
    except Exception: return 99

def gorsel(a):
    arac("ac")
    r = arac("uret", "--is", "foto", "--model", "zimage", "--prompt", a.prompt, "--cikti", a.cikti, "--boyut", "1344x768")
    arac("kapat"); sys.exit(r.returncode)

def yukle(path):
    b = "----" + uuid.uuid4().hex; fn = os.path.basename(path)
    body = (f"--{b}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{fn}\"\r\nContent-Type: image/png\r\n\r\n").encode() + open(path, "rb").read() + (f"\r\n--{b}\r\nContent-Disposition: form-data; name=\"overwrite\"\r\n\r\ntrue\r\n--{b}--\r\n").encode()
    return req("/upload/image", body, "multipart/form-data; boundary=" + b)["name"]

def klip(a):
    for _ in range(90):  # RAM >=13 GB boş olana dek bekle
        if bos_gb() >= 13: break
        time.sleep(20)
    else: sys.exit("RAM yetersiz (<13 GB boş)")
    if not acik():
        arac("ac")
        for _ in range(60):
            if acik(): break
            time.sleep(5)
    w = json.load(open(os.path.join(R, "tools", "gorsel", "akislar", "wan22_5b_t2v.json"), encoding="utf-8"))
    nm = yukle(a.gorsel)
    w["20"] = {"class_type": "LoadImage", "inputs": {"image": nm}}
    w["21"] = {"class_type": "ImageScale", "inputs": {"image": ["20", 0], "upscale_method": "lanczos", "width": 1024, "height": 576, "crop": "center"}}
    w["5"]["inputs"]["text"] = a.hareket; w["6"]["inputs"]["text"] = NEG
    w["7"]["inputs"].update({"width": 1024, "height": 576, "length": a.uzunluk, "start_image": ["21", 0]})
    w["8"]["inputs"]["seed"] = a.tohum; w["11"]["inputs"]["filename_prefix"] = "scroll/" + os.path.splitext(os.path.basename(a.cikti))[0]
    t0 = time.time(); pid = req("/prompt", json.dumps({"prompt": w}).encode())["prompt_id"]
    while time.time() - t0 < 2400:
        time.sleep(10); h = req("/history/" + pid)
        if pid not in h: continue
        st = h[pid].get("status", {})
        if st.get("status_str") == "error": sys.exit("HATA " + json.dumps(st)[:600])
        vid = None
        for o in h[pid]["outputs"].values():
            for k in ("videos", "images", "gifs"):
                for f in o.get(k, []): vid = f
        if not vid: sys.exit("çıktı yok")
        shutil.copy(os.path.join(r"C:\AI\ComfyUI\output", vid.get("subfolder", ""), vid["filename"]), a.cikti)
        print("klip", a.cikti, round(time.time() - t0), "sn"); arac("kapat"); return
    sys.exit("zaman aşımı")

def kare(a):
    os.makedirs(a.cikti, exist_ok=True)
    for f in os.listdir(a.cikti):
        if f.startswith("frame_") and f.endswith(".jpg"): os.remove(os.path.join(a.cikti, f))
    p = subprocess.run(["ffmpeg", "-i", a.video], capture_output=True, text=True).stderr
    d = p.split("Duration:")[1].split(",")[0].strip().split(":"); dur = int(d[0]) * 3600 + int(d[1]) * 60 + float(d[2])
    nat = float(p.split(" fps")[0].split()[-1])  # kaynak fps: üstü kare çoğaltır, akıcılık katmaz
    fps = min(a.adet / max(dur, 1), nat)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", a.video, "-vf", f"fps={fps:.4f},scale='min({a.genislik},iw)':-2:flags=lanczos", "-q:v", "3", os.path.join(a.cikti, "frame_%04d.jpg")], check=True)
    n = len([x for x in os.listdir(a.cikti) if x.startswith("frame_")]); print(f"{n} kare -> {a.cikti}; frameCount={n}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="c", required=True)
    g = sp.add_parser("gorsel"); g.add_argument("--prompt", required=True); g.add_argument("--cikti", required=True); g.set_defaults(f=gorsel)
    k = sp.add_parser("klip"); k.add_argument("--gorsel", required=True); k.add_argument("--hareket", required=True); k.add_argument("--cikti", required=True); k.add_argument("--uzunluk", type=int, default=49); k.add_argument("--tohum", type=int, default=7); k.set_defaults(f=klip)
    r = sp.add_parser("kare"); r.add_argument("--video", required=True); r.add_argument("--cikti", required=True); r.add_argument("--adet", type=int, default=180); r.add_argument("--genislik", type=int, default=1600); r.set_defaults(f=kare)
    a = ap.parse_args(); a.f(a)
