"""VIDEO-RAM-1 asama 1: yalniz umt5 kodlayici -> kosullandirma .pt (ayri surec). RAM %87'de kendini durdurur."""
import os, sys, threading, time, psutil, torch

CUI = r"C:\AI\ComfyUI"
sys.path.insert(0, CUI)
TAVAN = 87.0
PROMPT = ("A young man in a dark denim jacket walks along a rain-soaked city street at night, neon signs "
          "reflecting in puddles, camera slowly tracking beside him, he turns his head and smiles, cinematic lighting, realistic")
NEG = "blurry, low quality, distorted, deformed face, extra fingers, watermark, text, static"
tepe = [0.0]

def bekci():
    while True:
        p = psutil.virtual_memory().percent
        tepe[0] = max(tepe[0], p)
        if p >= TAVAN:
            mi = psutil.Process().memory_info()
            print(f"RAM %{p} >= %{TAVAN}: DURDURULDU rss GB {mi.rss/1e9:.2f} private GB {getattr(mi,'private',0)/1e9:.2f}", flush=True)
            os._exit(3)
        time.sleep(0.25)

threading.Thread(target=bekci, daemon=True).start()
print("baslangic RAM %", psutil.virtual_memory().percent, flush=True)
import comfy.sd, comfy.model_management as mm, folder_paths

import comfy.utils, ctypes, safetensors
def _yukle(ckpt, safe_load=False, device=None, return_metadata=False):
    k32 = ctypes.windll.kernel32; ps = ctypes.windll.psapi
    sd = {}
    with safetensors.safe_open(ckpt, framework="pt", device="cpu") as f:
        for i, k in enumerate(f.keys()):
            t = f.get_tensor(k)
            sd[k] = t.clone() if k == "spiece_model" else t.to("cuda:0")
            if i % 20 == 0:
                ps.EmptyWorkingSet(k32.GetCurrentProcess())
    ps.EmptyWorkingSet(k32.GetCurrentProcess())
    return (sd, None) if return_metadata else sd
comfy.utils.load_torch_file = _yukle
yol = os.path.join(CUI, "models", "text_encoders", "umt5_xxl_fp8_e4m3fn_scaled.safetensors")
t0 = time.time()
clip = comfy.sd.load_clip(ckpt_paths=[yol], embedding_directory=None, clip_type=comfy.sd.CLIPType.WAN,
                     model_options={"initial_device": torch.device("cuda:0"), "load_device": torch.device("cuda:0"), "offload_device": torch.device("cuda:0")})
print("yuklendi s", round(time.time() - t0, 1), "RAM tepe %", tepe[0], flush=True)
print("RAM now %", psutil.virtual_memory().percent, "VRAM free GB", round(mm.get_free_memory()/1e9,2), flush=True)
out = {}
for ad, m in (("pos", PROMPT), ("neg", NEG)):
    print("enc", ad, "RAM %", psutil.virtual_memory().percent, flush=True)
    tok = clip.tokenize(m)
    cond = clip.encode_from_tokens_scheduled(tok)
    out[ad] = [(c[0].cpu(), {k: (v.cpu() if hasattr(v, "cpu") else v) for k, v in c[1].items()}) for c in cond]
os.makedirs(r"C:\Projeler\omer-skills\.kos\kopru\tmp", exist_ok=True)
torch.save(out, r"C:\Projeler\omer-skills\.kos\kopru\tmp\wan_cond.pt")
print("kodlandi s", round(time.time() - t0, 1), "RAM tepe %", tepe[0], "VRAM GB", round(torch.cuda.max_memory_allocated() / 1e9, 2), flush=True)
