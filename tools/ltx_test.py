import json, subprocess, sys, time, threading, urllib.request, psutil, os
MODE="ltx"
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
                           cwd="C:/AI/ComfyUI", stdout=open("C:/Projeler/omer-skills/tmp/comfy-ltx.log", "w"),
                           stderr=subprocess.STDOUT, creationflags=0x08000000)
    for _ in range(120):
        if up(): break
        time.sleep(2)
peak = {"ram": 0, "vram": 0}
stop = False
def mon():
    while not stop:
        peak["ram"] = max(peak["ram"], psutil.virtual_memory().percent); open("C:/Projeler/omer-skills/tmp/ltx_mon.log","a").write("%d %.0f\n" % (time.time(), psutil.virtual_memory().percent))
        try:
            o = subprocess.check_output(["nvidia-smi", "--query-gpu=memory.used,memory.total", "--format=csv,noheader,nounits"], text=True).split(",")
            peak["vram"] = max(peak["vram"], 100 * int(o[0]) / int(o[1]))
        except Exception: pass
        time.sleep(2)
threading.Thread(target=mon, daemon=True).start()
W = {
 "1": {"class_type": "UnetLoaderGGUF", "inputs": {"unet_name": "ltx-2.5-22b-distilled-Q6_K.gguf"}},
 "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": "gemma4-12b-ltx-2.5-heretic-int8-convrot.safetensors", "type": "ltxv", "device": "default"}},
 "3": {"class_type": "VAELoader", "inputs": {"vae_name": "ltx-2.5-video-vae-conv-bf16.safetensors"}},
 "4": {"class_type": "VAELoader", "inputs": {"vae_name": "ltx-2.5-audio-vae-bf16.safetensors"}},
 "5": {"class_type": "CLIPTextEncode", "inputs": {"text": PROMPT, "clip": ["2", 0]}},
 "6": {"class_type": "CLIPTextEncode", "inputs": {"text": "blurry, distorted, low quality", "clip": ["2", 0]}},
 "7": {"class_type": "LTXVConditioning", "inputs": {"positive": ["5", 0], "negative": ["6", 0], "frame_rate": 24.0}},
 "8": {"class_type": "EmptyLTXVLatentVideo", "inputs": {"width": 960, "height": 544, "length": 121, "batch_size": 1}},
 "9": {"class_type": "LTXVEmptyLatentAudio", "inputs": {"frames_number": 121, "frame_rate": 24, "batch_size": 1, "audio_vae": ["4", 0]}},
 "10": {"class_type": "LTXVConcatAVLatent", "inputs": {"video_latent": ["8", 0], "audio_latent": ["9", 0]}},
 "11": {"class_type": "CFGGuider", "inputs": {"model": ["1", 0], "positive": ["7", 0], "negative": ["7", 1], "cfg": 1.0}},
 "12": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler"}},
 "13": {"class_type": "ManualSigmas", "inputs": {"sigmas": "1.0, 0.99375, 0.9875, 0.98125, 0.975, 0.909375, 0.725, 0.421875, 0.0"}},
 "14": {"class_type": "RandomNoise", "inputs": {"noise_seed": 42}},
 "15": {"class_type": "SamplerCustomAdvanced", "inputs": {"noise": ["14", 0], "guider": ["11", 0], "sampler": ["12", 0], "sigmas": ["13", 0], "latent_image": ["10", 0]}},
 "16": {"class_type": "LTXVSeparateAVLatent", "inputs": {"av_latent": ["15", 0]}},
 "17": {"class_type": "LatentUpscaleModelLoader", "inputs": {"model_name": "ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors"}},
 "18": {"class_type": "LTXVLatentUpsampler", "inputs": {"samples": ["16", 0], "upscale_model": ["17", 0], "vae": ["3", 0]}},
 "19": {"class_type": "LTXVConcatAVLatent", "inputs": {"video_latent": ["18", 0], "audio_latent": ["16", 1]}},
 "20": {"class_type": "ManualSigmas", "inputs": {"sigmas": "0.909375, 0.725, 0.421875, 0.0"}},
 "21": {"class_type": "SamplerCustomAdvanced", "inputs": {"noise": ["14", 0], "guider": ["11", 0], "sampler": ["12", 0], "sigmas": ["20", 0], "latent_image": ["19", 0]}},
 "22": {"class_type": "LTXVSeparateAVLatent", "inputs": {"av_latent": ["21", 0]}},
 "23": {"class_type": "VAEDecodeTiled", "inputs": {"samples": ["22", 0], "vae": ["3", 0], "tile_size": 512, "overlap": 32, "temporal_size": 64, "temporal_overlap": 8}},
 "24": {"class_type": "SaveWEBM", "inputs": {"images": ["23", 0], "filename_prefix": "ltxtest/ltx", "codec": "vp9", "fps": 24.0, "crf": 20.0}},
 "25": {"class_type": "LTXVAudioVAEDecode", "inputs": {"samples": ["22", 1], "audio_vae": ["4", 0]}},
 "26": {"class_type": "SaveAudio", "inputs": {"audio": ["25", 0], "filename_prefix": "ltxtest/ltx"}},
}
def run(prompt):
    r = post("/prompt", {"prompt": prompt})
    pid = r["prompt_id"]
    print("queued", pid, flush=True)
    while True:
        h = json.load(urllib.request.urlopen(P + "/history/" + pid, timeout=30))
        if pid in h:
            st = h[pid]["status"]
            print("status", st["status_str"], round(time.time() - t0), "s", flush=True)
            if st["status_str"] != "success":
                print(json.dumps(st["messages"])[-2500:])
            print("outputs", json.dumps(h[pid]["outputs"])[:600], flush=True)
            return st["status_str"]
        time.sleep(5)
if os.environ.get("LTX_STAGE1"):
    for k in ("17","18","19","20","21","22"): W.pop(k)
    W["23"]["inputs"]["samples"] = ["16", 0]; W["25"]["inputs"]["samples"] = ["16", 1]
    W["24"]["inputs"]["filename_prefix"] = W["26"]["inputs"]["filename_prefix"] = "ltxtest/s1"
t0 = time.time()
A = {k: W[k] for k in ("2", "5", "6", "7")}
A["90"] = {"class_type": "PreviewAny", "inputs": {"source": ["7", 0]}}
try:
    if run(A) == "success":
        urllib.request.urlopen(urllib.request.Request(P + "/free", data=b'{"unload_models": true, "free_memory": true}', headers={"Content-Type": "application/json"}), timeout=60).read()
        time.sleep(5)
        print("RAM after free", psutil.virtual_memory().percent, flush=True)
        run(W)
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read().decode()[:3000]); sys.exit(1)
stop = True
print("PEAK RAM %", peak["ram"], "PEAK VRAM %", round(peak["vram"], 1))
