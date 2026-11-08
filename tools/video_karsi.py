"""VIDEO-KARSILASTIRMA: H3 / LTX-2.5 / Wan2.2-5B, ayni prompt+negatif+seed+cozunurluk+kare+fps.
Kullanim: python video_karsi.py <h3|ltx|wan> <W> <H> <kare> [ram_tavan=87]
RAM tavani asilirsa ComfyUI olur (taskkill /T). Sonuc: tmp/vk-<model>-<W>x<H>-<kare>.json"""
import json, subprocess, sys, time, threading, urllib.request, psutil, os
M, WD, HT, N = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
CAP = float(sys.argv[5]) if len(sys.argv) > 5 else 89
RES = sys.argv[6] if len(sys.argv) > 6 else "2.8"
PROMPT = ("A young man in a dark denim jacket walks along a rain-soaked city street at night, neon signs "
          "reflecting in puddles, camera slowly tracking beside him, he turns his head and smiles, cinematic lighting, realistic")
NEG = "blurry, distorted, low quality, deformed face, extra fingers, watermark, text"
SEED, FPS = 42, 24
P = "http://127.0.0.1:8188"
TAG = f"vk/{M}-{WD}x{HT}-{N}"
def post(path, data=None):
    r = urllib.request.Request(P + path, data=json.dumps(data).encode() if data is not None else None, headers={"Content-Type": "application/json"})
    b = urllib.request.urlopen(r, timeout=60).read()
    return json.loads(b) if b.strip() else {}
def up():
    try: urllib.request.urlopen(P + "/system_stats", timeout=3); return True
    except Exception: return False
if up(): sys.exit("ComfyUI zaten acik; once kapat")
srv = subprocess.Popen(["C:/AI/venv-t2/Scripts/python.exe", "main.py", "--port", "8188", "--listen", "127.0.0.1",
                        "--reserve-vram", RES] + os.environ.get("VK_EK", "").split(),
                       cwd="C:/AI/ComfyUI", stdout=open(f"C:/Projeler/omer-skills/tmp/comfy-vk-{M}.log", "w"),
                       stderr=subprocess.STDOUT, creationflags=0x08000000)
def kill(): subprocess.run(["taskkill", "/PID", str(srv.pid), "/T", "/F"], capture_output=True)
peak = {"ram": 0, "vram": 0, "killed": False}
stop = False
def mon():
    while not stop:
        r = psutil.virtual_memory().percent; peak["ram"] = max(peak["ram"], r)
        try:
            o = subprocess.check_output(["nvidia-smi", "--query-gpu=memory.used,memory.total", "--format=csv,noheader,nounits"], text=True).split(",")
            peak["vram"] = max(peak["vram"], int(o[0]) / 1024)
        except Exception: pass
        if r > CAP: peak["killed"] = True; kill(); return
        time.sleep(1)
for _ in range(120):
    if up(): break
    time.sleep(2)
threading.Thread(target=mon, daemon=True).start()
def save(img, aud=None):
    g = {"vid": {"class_type": "SaveWEBM", "inputs": {"images": img, "filename_prefix": TAG, "codec": "vp9", "fps": float(FPS), "crf": 20.0}}}
    if aud: g["aud"] = {"class_type": "SaveAudio", "inputs": {"audio": aud, "filename_prefix": TAG}}
    return g
def graph():
    if M == "h3":
        g = {
         "1": {"class_type": "UNETLoader", "inputs": {"unet_name": "minimax_h3_fl2va_pruned_int8_convrot.safetensors", "weight_dtype": "default"}},
         "2": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["1", 0], "lora_name": "minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors", "strength_model": 1.0}},
         "3": {"class_type": "MiniMaxH3SigmaShift", "inputs": {"model": ["2", 0], "shift_video": 12.0, "shift_audio": 3.0}},
         "4": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors", "type": "minimax", "device": "default"}},
         "5": {"class_type": "VAELoader", "inputs": {"vae_name": "minimax_h3_video_vae_fp16.safetensors"}},
         "6": {"class_type": "VAELoader", "inputs": {"vae_name": "minimax_h3_audio_vae_fp32.safetensors"}},
         "7": {"class_type": "MiniMaxH3ImageToVideo", "inputs": {"clip": ["4", 0], "vae": ["5", 0], "prompt": PROMPT, "width": WD, "height": HT, "length": N}},
         "8": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["7", 0]}},
         "9": {"class_type": "CFGGuider", "inputs": {"model": ["3", 0], "positive": ["7", 0], "negative": ["8", 0], "cfg": 1.0}},
         "10": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "res_multistep"}},
         "11": {"class_type": "BasicScheduler", "inputs": {"model": ["3", 0], "scheduler": "simple", "steps": 4, "denoise": 1.0}},
         "12": {"class_type": "RandomNoise", "inputs": {"noise_seed": SEED}},
         "13": {"class_type": "SamplerCustomAdvanced", "inputs": {"noise": ["12", 0], "guider": ["9", 0], "sampler": ["10", 0], "sigmas": ["11", 0], "latent_image": ["7", 1]}},
         "14": {"class_type": "LTXVSeparateAVLatent", "inputs": {"av_latent": ["13", 0]}},
         "15": {"class_type": "VAEDecodeTiled", "inputs": {"samples": ["14", 0], "vae": ["5", 0], "tile_size": 256, "overlap": 32, "temporal_size": 32, "temporal_overlap": 4}},
         "17": {"class_type": "VAEDecodeAudio", "inputs": {"samples": ["14", 1], "vae": ["6", 0]}},
        }
        g.update(save(["15", 0], ["17", 0])); return [g]
    if M == "h3iyi":
        TW, TH = int(os.environ.get("HEDEF_W", WD * 2)), int(os.environ.get("HEDEF_H", HT * 2))
        g = {
         "1": {"class_type": "UNETLoader", "inputs": {"unet_name": "minimax_h3_fl2va_pruned_int8_convrot.safetensors", "weight_dtype": "default"}},
         "2": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["1", 0], "lora_name": "minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors", "strength_model": 1.0}},
         "3": {"class_type": "MiniMaxH3SigmaShift", "inputs": {"model": ["2", 0], "shift_video": 12.0, "shift_audio": 3.0}},
         "4": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors", "type": "minimax", "device": "default"}},
         "5": {"class_type": "VAELoader", "inputs": {"vae_name": "minimax_h3_video_vae_fp16.safetensors"}},
         "6": {"class_type": "VAELoader", "inputs": {"vae_name": "minimax_h3_audio_vae_fp32.safetensors"}},
         "7": {"class_type": "MiniMaxH3ImageToVideo", "inputs": {"clip": ["4", 0], "vae": ["5", 0], "prompt": PROMPT, "width": WD, "height": HT, "length": N}},
         "8": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["7", 0]}},
         "9": {"class_type": "CFGGuider", "inputs": {"model": ["3", 0], "positive": ["7", 0], "negative": ["8", 0], "cfg": 1.0}},
         "10": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "res_multistep"}},
         "11": {"class_type": "BasicScheduler", "inputs": {"model": ["3", 0], "scheduler": "simple", "steps": 4, "denoise": 1.0}},
         "12": {"class_type": "RandomNoise", "inputs": {"noise_seed": SEED}},
         "13": {"class_type": "SamplerCustomAdvanced", "inputs": {"noise": ["12", 0], "guider": ["9", 0], "sampler": ["10", 0], "sigmas": ["11", 0], "latent_image": ["7", 1]}},
         "20": {"class_type": "LatentUpscaleModelLoader", "inputs": {"model_name": "minimax_h3_latent_upscaler_3d_conv_v1_bf16.safetensors"}},
         "21": {"class_type": "MiniMaxH3LatentUpscaleWithModel", "inputs": {"model": ["20", 0], "samples": ["13", 0], "width": TW, "height": TH}},
         "22": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["1", 0], "lora_name": os.environ.get("REFINER", "minimax_h3_open_regenerate_2k_r128_comfyui_bf16_swiglu_fixed.safetensors"), "strength_model": 1.0}},
         "23": {"class_type": "MiniMaxH3ImageToVideo", "inputs": {"clip": ["4", 0], "vae": ["5", 0], "prompt": PROMPT, "width": TW, "height": TH, "length": N}},
         "24": {"class_type": "BasicGuider", "inputs": {"model": ["22", 0], "conditioning": ["23", 0]}},
         "25": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler"}},
         "26": {"class_type": "ManualSigmas", "inputs": {"sigmas": "0.909375, 0.857143, 0.666667, 0.0"}},
         "27": {"class_type": "SamplerCustomAdvanced", "inputs": {"noise": ["12", 0], "guider": ["24", 0], "sampler": ["25", 0], "sigmas": ["26", 0], "latent_image": ["21", 0]}},
         "28": {"class_type": "LTXVSeparateAVLatent", "inputs": {"av_latent": ["27", 0]}},
         "29": {"class_type": "VAELoader", "inputs": {"vae_name": os.environ.get("SON_VAE", "sol_h3_vae.safetensors")}},
         "17": {"class_type": "VAEDecodeAudio", "inputs": {"samples": ["28", 1], "vae": ["6", 0]}},
        }
        if os.environ.get("SON_VAE"):
            g["15"] = {"class_type": "VAEDecodeTiled", "inputs": {"samples": ["28", 0], "vae": ["29", 0], "tile_size": 256, "overlap": 32, "temporal_size": 32, "temporal_overlap": 4}}
        else:
            g["15"] = {"class_type": "VAEDecode", "inputs": {"samples": ["28", 0], "vae": ["29", 0]}}
        g.update(save(["15", 0], ["17", 0])); return [g]
    if M == "pika":
        g = {
         "1": {"class_type": "UNETLoader", "inputs": {"unet_name": "minimax_h3_fl2va_pruned_int8_convrot.safetensors", "weight_dtype": "default"}},
         "2": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["1", 0], "lora_name": os.environ.get("PIKA_LORA", "pika_h3_flex_fl2va_v1_bf16.safetensors"), "strength_model": 1.0}},
         "4": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors", "type": "minimax", "device": "default"}},
         "5": {"class_type": "VAELoader", "inputs": {"vae_name": "minimax_h3_video_vae_fp16.safetensors"}},
         "6": {"class_type": "VAELoader", "inputs": {"vae_name": "minimax_h3_audio_vae_fp32.safetensors"}},
         "7": {"class_type": "MiniMaxH3ImageToVideo", "inputs": {"clip": ["4", 0], "vae": ["5", 0], "prompt": PROMPT, "width": WD, "height": HT, "length": N}},
         "9": {"class_type": "BasicGuider", "inputs": {"model": ["2", 0], "conditioning": ["7", 0]}},
         "10": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "lcm"}},
         "11": {"class_type": "ManualSigmas", "inputs": {"sigmas": "1.0, 0.972973, 0.923077, 0.8, 0.571429, 0.333333, 0.0"}},
         "12": {"class_type": "RandomNoise", "inputs": {"noise_seed": SEED}},
         "13": {"class_type": "SamplerCustomAdvanced", "inputs": {"noise": ["12", 0], "guider": ["9", 0], "sampler": ["10", 0], "sigmas": ["11", 0], "latent_image": ["7", 1]}},
         "14": {"class_type": "LTXVSeparateAVLatent", "inputs": {"av_latent": ["13", 0]}},
         "15": {"class_type": "VAEDecodeTiled", "inputs": {"samples": ["14", 0], "vae": ["5", 0], "tile_size": 256, "overlap": 32, "temporal_size": 32, "temporal_overlap": 4}},
         "17": {"class_type": "VAEDecodeAudio", "inputs": {"samples": ["14", 1], "vae": ["6", 0]}},
        }
        g.update(save(["15", 0], ["17", 0])); return [g]
    if M == "wan":
        A = {
         "3": {"class_type": "CLIPLoader", "inputs": {"clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "type": "wan", "device": "default"}},
         "5": {"class_type": "CLIPTextEncode", "inputs": {"text": PROMPT, "clip": ["3", 0]}},
         "6": {"class_type": "CLIPTextEncode", "inputs": {"text": NEG, "clip": ["3", 0]}},
         "90": {"class_type": "PreviewAny", "inputs": {"source": ["5", 0]}},
         "91": {"class_type": "PreviewAny", "inputs": {"source": ["6", 0]}}}
        g = {
         "1": {"class_type": "UnetLoaderGGUF", "inputs": {"unet_name": "Wan2.2-TI2V-5B-Q5_K_M.gguf"}},
         "2": {"class_type": "ModelSamplingSD3", "inputs": {"model": ["1", 0], "shift": 8.0}},
         "3": A["3"], "5": A["5"], "6": A["6"],
         "4": {"class_type": "VAELoader", "inputs": {"vae_name": "wan2.2_vae.safetensors"}},
         "7": {"class_type": "Wan22ImageToVideoLatent", "inputs": {"vae": ["4", 0], "width": WD, "height": HT, "length": N, "batch_size": 1}},
         "8": {"class_type": "KSampler", "inputs": {"model": ["2", 0], "seed": SEED, "steps": 20, "cfg": 5.0, "sampler_name": "uni_pc", "scheduler": "simple",
                                                   "positive": ["5", 0], "negative": ["6", 0], "latent_image": ["7", 0], "denoise": 1.0}},
         "9": {"class_type": "VAEDecodeTiled", "inputs": {"samples": ["8", 0], "vae": ["4", 0], "tile_size": 256, "overlap": 64, "temporal_size": 32, "temporal_overlap": 8}},
        }
        g.update(save(["9", 0])); return [A, g]
    A = {
     "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": "gemma4-12b-ltx-2.5-heretic-int8-convrot.safetensors", "type": "ltxv", "device": "default"}},
     "5": {"class_type": "CLIPTextEncode", "inputs": {"text": PROMPT, "clip": ["2", 0]}},
     "6": {"class_type": "CLIPTextEncode", "inputs": {"text": NEG, "clip": ["2", 0]}},
     "7": {"class_type": "LTXVConditioning", "inputs": {"positive": ["5", 0], "negative": ["6", 0], "frame_rate": float(FPS)}},
     "90": {"class_type": "PreviewAny", "inputs": {"source": ["7", 0]}}}
    g = {
     "1": {"class_type": "UnetLoaderGGUF", "inputs": {"unet_name": "ltx-2.5-22b-distilled-Q6_K.gguf"}},
     "2": A["2"], "5": A["5"], "6": A["6"], "7": A["7"],
     "3": {"class_type": "VAELoader", "inputs": {"vae_name": "ltx-2.5-video-vae-conv-bf16.safetensors"}},
     "4": {"class_type": "VAELoader", "inputs": {"vae_name": "ltx-2.5-audio-vae-bf16.safetensors"}},
     "8": {"class_type": "EmptyLTXVLatentVideo", "inputs": {"width": WD, "height": HT, "length": N, "batch_size": 1}},
     "9": {"class_type": "LTXVEmptyLatentAudio", "inputs": {"frames_number": N, "frame_rate": FPS, "batch_size": 1, "audio_vae": ["4", 0]}},
     "10": {"class_type": "LTXVConcatAVLatent", "inputs": {"video_latent": ["8", 0], "audio_latent": ["9", 0]}},
     "11": {"class_type": "CFGGuider", "inputs": {"model": ["1", 0], "positive": ["7", 0], "negative": ["7", 1], "cfg": 1.0}},
     "12": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler"}},
     "13": {"class_type": "ManualSigmas", "inputs": {"sigmas": "1.0, 0.99375, 0.9875, 0.98125, 0.975, 0.909375, 0.725, 0.421875, 0.0"}},
     "14": {"class_type": "RandomNoise", "inputs": {"noise_seed": SEED}},
     "15": {"class_type": "SamplerCustomAdvanced", "inputs": {"noise": ["14", 0], "guider": ["11", 0], "sampler": ["12", 0], "sigmas": ["13", 0], "latent_image": ["10", 0]}},
     "16": {"class_type": "LTXVSeparateAVLatent", "inputs": {"av_latent": ["15", 0]}},
     "23": {"class_type": "VAEDecodeTiled", "inputs": {"samples": ["16", 0], "vae": ["3", 0], "tile_size": 256, "overlap": 32, "temporal_size": 32, "temporal_overlap": 4}},
     "25": {"class_type": "LTXVAudioVAEDecode", "inputs": {"samples": ["16", 1], "audio_vae": ["4", 0]}},
    }
    g.update(save(["23", 0], ["25", 0])); return [A, g]
def run(prompt):
    pid = post("/prompt", {"prompt": prompt})["prompt_id"]
    while not peak["killed"]:
        h = json.load(urllib.request.urlopen(P + "/history/" + pid, timeout=30))
        if pid in h:
            st = h[pid]["status"]
            if st["status_str"] != "success": print(json.dumps(st["messages"])[-1500:])
            return st["status_str"]
        time.sleep(3)
    return "killed"
t0 = time.time(); res = "?"
try:
    gs = graph()
    for i, g in enumerate(gs):
        res = run(g)
        if res != "success": break
        if i < len(gs) - 1:
            urllib.request.urlopen(urllib.request.Request(P + "/free", data=json.dumps({"unload_models": True, "free_memory": True}).encode(), headers={"Content-Type": "application/json"}), timeout=60).read(); time.sleep(5)
except Exception as e:
    res = "error " + str(e)[:300]
dt = round(time.time() - t0); stop = True
out = {"model": M, "w": WD, "h": HT, "n": N, "status": res, "sec": dt, "peak_ram": peak["ram"], "peak_vram_gb": round(peak["vram"], 1), "ram_killed": peak["killed"]}
print(json.dumps(out)); open(f"C:/Projeler/omer-skills/tmp/vk-{M}-{WD}x{HT}-{N}.json", "w").write(json.dumps(out))
kill()
