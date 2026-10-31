import json, subprocess, sys, time, threading, urllib.request, psutil, os
MODE = sys.argv[1]  # turbo | std
STEPS = 4 if MODE == "turbo" else 20
CFG = 1.0 if MODE == "turbo" else 3.5
PROMPT = ("A red fox trots through fresh snow in a pine forest at sunrise, soft golden light, "
          "breath visible in cold air, camera slowly tracks alongside. Ambient wind and soft footsteps in snow.")
P = "http://127.0.0.1:8188"
def post(path, data=None):
    r = urllib.request.Request(P + path, data=json.dumps(data).encode() if data is not None else None,
                               headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r, timeout=60))
def up():
    try: urllib.request.urlopen(P + "/system_stats", timeout=3); return True
    except Exception: return False
srv = None
if not up():
    srv = subprocess.Popen(["C:/AI/venv-t2/Scripts/python.exe", "main.py", "--port", "8188", "--listen", "127.0.0.1"] + os.environ.get("COMFY_ARGS","").split(),
                           cwd="C:/AI/ComfyUI", stdout=open("C:/Projeler/omer-skills/tmp/comfy-h3.log", "w"),
                           stderr=subprocess.STDOUT, creationflags=0x08000000)
    for _ in range(120):
        if up(): break
        time.sleep(2)
peak = {"ram": 0, "vram": 0}
stop = False
def mon():
    while not stop:
        peak["ram"] = max(peak["ram"], psutil.virtual_memory().percent); open("C:/Projeler/omer-skills/tmp/h3_mon.log","a").write("%d %.0f\n" % (time.time(), psutil.virtual_memory().percent))
        try:
            o = subprocess.check_output(["nvidia-smi", "--query-gpu=memory.used,memory.total", "--format=csv,noheader,nounits"], text=True).split(",")
            peak["vram"] = max(peak["vram"], 100 * int(o[0]) / int(o[1]))
        except Exception: pass
        time.sleep(2)
threading.Thread(target=mon, daemon=True).start()
W = {
 "1": {"class_type": "UNETLoader", "inputs": {"unet_name": "minimax_h3_fl2va_pruned_int8_convrot.safetensors", "weight_dtype": "default"}},
 "2": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["1", 0], "lora_name": "minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors", "strength_model": 1.0}},
 "3": {"class_type": "MiniMaxH3SigmaShift", "inputs": {"model": ["2" if MODE == "turbo" else "1", 0], "shift_video": 12.0, "shift_audio": 3.0}},
 "4": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors", "type": "minimax", "device": "default"}},
 "5": {"class_type": "VAELoader", "inputs": {"vae_name": "minimax_h3_video_vae_fp16.safetensors"}},
 "6": {"class_type": "VAELoader", "inputs": {"vae_name": "minimax_h3_audio_vae_fp32.safetensors"}},
 "7": {"class_type": "MiniMaxH3ImageToVideo", "inputs": {"clip": ["4", 0], "vae": ["5", 0], "prompt": PROMPT, "width": 864, "height": 480, "length": 124}},
 "8": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["7", 0]}},
 "9": {"class_type": "CFGGuider", "inputs": {"model": ["3", 0], "positive": ["7", 0], "negative": ["8", 0], "cfg": CFG}},
 "10": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "res_multistep"}},
 "11": {"class_type": "BasicScheduler", "inputs": {"model": ["3", 0], "scheduler": "simple", "steps": STEPS, "denoise": 1.0}},
 "12": {"class_type": "RandomNoise", "inputs": {"noise_seed": 42}},
 "13": {"class_type": "SamplerCustomAdvanced", "inputs": {"noise": ["12", 0], "guider": ["9", 0], "sampler": ["10", 0], "sigmas": ["11", 0], "latent_image": ["7", 1]}},
 "14": {"class_type": "LTXVSeparateAVLatent", "inputs": {"av_latent": ["13", 0]}},
 "15": {"class_type": "VAEDecodeTiled", "inputs": {"samples": ["14", 0], "vae": ["5", 0], "tile_size": 512, "overlap": 64, "temporal_size": 64, "temporal_overlap": 8}},
 "16": {"class_type": "SaveWEBM", "inputs": {"images": ["15", 0], "filename_prefix": f"h3test/{MODE}", "codec": "vp9", "fps": 24.0, "crf": 20.0}},
 "17": {"class_type": "VAEDecodeAudio", "inputs": {"samples": ["14", 1], "vae": ["6", 0]}},
 "18": {"class_type": "SaveAudio", "inputs": {"audio": ["17", 0], "filename_prefix": f"h3test/{MODE}"}},
}
t0 = time.time()
try:
    r = post("/prompt", {"prompt": W})
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read().decode()[:3000]); sys.exit(1)
pid = r["prompt_id"]
print("queued", pid, flush=True)
while True:
    h = json.load(urllib.request.urlopen(P + "/history/" + pid, timeout=30))
    if pid in h:
        st = h[pid]["status"]
        print("status", st["status_str"], round(time.time() - t0), "s")
        if st["status_str"] != "success":
            print(json.dumps(st["messages"])[-2500:])
        print("outputs", json.dumps(h[pid]["outputs"])[:600])
        break
    time.sleep(5)
stop = True
print("PEAK RAM %", peak["ram"], "PEAK VRAM %", round(peak["vram"], 1))
