"""SUNUCU-KARAKTER-1: yerel Z-Image-Turbo (ComfyUI, fp8) ile toplu görsel.
Kullanım: python tools/sunucu_zimage.py isler.json   (liste: {cikti, prompt, seed, w, h})
ComfyUI penceresiz başlar, iş bitince kapanır. Zaten üretilmiş çıktı atlanır."""
import json, os, subprocess, sys, time, urllib.request, uuid

COMFY = r"C:\AI\ComfyUI"
URL = "http://127.0.0.1:8188"
NEG = "photo of real person, realistic skin, watermark, text, logo, extra fingers, deformed, blurry"


def akis(p, s, w, h):
    return {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": "z_image_turbo_fp8_e4m3fn.safetensors", "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen_3_4b_fp8_mixed.safetensors", "type": "lumina2", "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "ae.safetensors"}},
        "4": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["1", 0], "shift": 3.0}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": p}},
        "6": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["5", 0]}},
        "7": {"class_type": "EmptySD3LatentImage", "inputs": {"width": w, "height": h, "batch_size": 1}},
        "8": {"class_type": "KSampler", "inputs": {"model": ["4", 0], "seed": s, "steps": 8, "cfg": 1.0, "sampler_name": "res_multistep",
              "scheduler": "simple", "denoise": 1.0, "positive": ["5", 0], "negative": ["6", 0], "latent_image": ["7", 0]}},
        "9": {"class_type": "VAEDecode", "inputs": {"samples": ["8", 0], "vae": ["3", 0]}},
        "10": {"class_type": "SaveImage", "inputs": {"images": ["9", 0], "filename_prefix": "sunucu"}},
    }


def al(yol, veri=None):
    r = urllib.request.Request(URL + yol, data=json.dumps(veri).encode() if veri else None, headers={"Content-Type": "application/json"})
    return urllib.request.urlopen(r, timeout=30).read()


def main():
    isler = [j for j in json.load(open(sys.argv[1], encoding="utf-8")) if not os.path.exists(j["cikti"])]
    if not isler:
        print("BITTI: yapilacak is yok"); return
    srv = subprocess.Popen([os.path.join(COMFY, ".venv", "Scripts", "python.exe"), "main.py", "--listen", "127.0.0.1", "--disable-auto-launch"],
                           cwd=COMFY, creationflags=0x08000000, stdout=open(os.path.join(COMFY, "sunucu_zimage.log"), "ab"), stderr=subprocess.STDOUT)
    try:
        for _ in range(120):
            try: al("/system_stats"); break
            except Exception: time.sleep(2)
        else:
            raise SystemExit("ComfyUI acilmadi")
        for j in isler:
            pid = json.loads(al("/prompt", {"prompt": akis(j["prompt"], j["seed"], j.get("w", 1024), j.get("h", 1024)), "client_id": str(uuid.uuid4())}))["prompt_id"]
            for _ in range(300):
                try: g = json.loads(al("/history/" + pid))
                except Exception: g = {}
                if pid in g: break
                time.sleep(2)
            else:
                print("ZAMAN ASIMI", j["cikti"]); continue
            im = list(g[pid]["outputs"].values())[0]["images"][0]
            os.makedirs(os.path.dirname(j["cikti"]), exist_ok=True)
            open(j["cikti"], "wb").write(al("/view?filename=%s&subfolder=%s&type=%s" % (im["filename"], im["subfolder"], im["type"])))
            print("TAMAM", j["cikti"], flush=True)
    finally:
        srv.kill()
    print("BITTI")


main()
