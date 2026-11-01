"""VIDEO-RAM-1 asama 2: Wan2.2 TI2V-5B Q5 + VAE, kosullandirma wan_cond.pt'den (kodlayici yuklenmez). RAM %87'de durur.
kullanim: python wan_ornekle.py GENISLIK YUKSEKLIK KARE CIKTI.mp4"""
import os, sys, threading, time, subprocess, importlib.util, psutil, torch

CUI = r"C:\AI\ComfyUI"
sys.path.insert(0, CUI)
W, H, N, CIKTI = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
TAVAN = 87.0
sys.argv = [sys.argv[0], "--disable-pinned-memory", "--disable-smart-memory", "--cache-none"]
tepe = [0.0]

def bekci():
    while True:
        p = psutil.virtual_memory().percent
        tepe[0] = max(tepe[0], p)
        if p >= TAVAN:
            print(f"RAM %{p} >= %{TAVAN}: DURDURULDU", flush=True)
            os._exit(3)
        time.sleep(0.25)

threading.Thread(target=bekci, daemon=True).start()
print("baslangic RAM %", psutil.virtual_memory().percent, flush=True)
import comfy.sd, comfy.utils, comfy.model_management as mm, nodes, folder_paths

spec = importlib.util.spec_from_file_location("ggufpkg", CUI + r"\custom_nodes\ComfyUI-GGUF\__init__.py",
                                              submodule_search_locations=[CUI + r"\custom_nodes\ComfyUI-GGUF"])
gg = importlib.util.module_from_spec(spec); sys.modules["ggufpkg"] = gg; spec.loader.exec_module(gg)
from ggufpkg.nodes import UnetLoaderGGUF
import comfy_extras.nodes_model_advanced as nma

t0 = time.time()
cond = torch.load(r"C:\Projeler\omer-skills\.kos\kopru\tmp\wan_cond.pt")
pos = [[c[0], c[1]] for c in cond["pos"]]
neg = [[c[0], c[1]] for c in cond["neg"]]
model = UnetLoaderGGUF().load_unet("Wan2.2-TI2V-5B-Q5_K_M.gguf")[0]
ms = nma.ModelSamplingSD3()
r = ms.patch(model, 8.0) if hasattr(ms, "patch") else ms.execute(model, 8.0)
model = r[0] if isinstance(r, tuple) else r.result[0]
vae = comfy.sd.VAE(sd=comfy.utils.load_torch_file(os.path.join(CUI, "models", "vae", "wan2.2_vae.safetensors")))
print("yuklendi s", round(time.time() - t0, 1), "RAM tepe %", tepe[0], flush=True)

lat = {"samples": torch.zeros([1, 48, ((N - 1) // 4) + 1, H // 16, W // 16])}
t1 = time.time()
out = nodes.common_ksampler(model, 42, 20, 5.0, "uni_pc", "simple", pos, neg, lat, denoise=1.0)[0]
print("ornekleme s", round(time.time() - t1, 1), "RAM tepe %", tepe[0], flush=True)
torch.save(out["samples"].cpu(), "C:/Projeler/omer-skills/.kos/kopru/tmp/wan_lat.pt")
torch.cuda.empty_cache()
img = vae.decode_tiled(out["samples"], tile_x=256, tile_y=256, overlap=64, tile_t=16, overlap_t=4)
img = img.reshape(-1, *img.shape[-3:])
fr = (img.clamp(0, 1) * 255).byte().cpu().numpy()
os.makedirs(os.path.dirname(CIKTI), exist_ok=True)
p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{fr.shape[2]}x{fr.shape[1]}",
                      "-r", "24", "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", CIKTI], stdin=subprocess.PIPE)
p.stdin.write(fr.tobytes()); p.stdin.close(); p.wait()
print(f"BITTI kare {fr.shape[0]} s {round(time.time()-t0,1)} RAM tepe % {tepe[0]} VRAM tepe GB {torch.cuda.max_memory_reserved()/1e9:.2f}", flush=True)
