"""FLUX.2 klein 9B (Omer onayi 02.11): GGUF Q5_K_M + Qwen3-8B fp8mixed metin kodlayici + flux2 VAE -> ComfyUI. Kaldigi yerden devam eder."""
import os, shutil, sys
from pathlib import Path
from huggingface_hub import hf_hub_download
sys.stdout.reconfigure(encoding="utf-8")
M = Path(r"C:\AI\ComfyUI\models")
ISLER = [
    ("unsloth/FLUX.2-klein-9B-GGUF", "flux-2-klein-9b-Q5_K_M.gguf", M / "unet"),
    ("Comfy-Org/vae-text-encorder-for-flux-klein-9b", "split_files/text_encoders/qwen_3_8b_fp8mixed.safetensors", M / "text_encoders"),
    ("Comfy-Org/vae-text-encorder-for-flux-klein-9b", "split_files/vae/flux2-vae.safetensors", M / "vae"),
]
for repo, dosya, hedef in ISLER:
    son = hedef / Path(dosya).name
    if son.exists() and son.stat().st_size > 1e8:
        print("VAR", son, flush=True); continue
    if shutil.disk_usage("C:\\").free < 32e9:
        print("DUR disk alt sinira yakin", flush=True); break
    gecici = M / "_indir_tmp"
    p = Path(hf_hub_download(repo, dosya, token=os.environ.get("HF_TOKEN"), local_dir=str(gecici)))
    hedef.mkdir(parents=True, exist_ok=True)
    os.replace(p, son)
    print("INDI", son, round(son.stat().st_size / 1e9, 2), "GB", flush=True)
print("bos disk GB", round(shutil.disk_usage("C:\\").free / 1e9, 1), flush=True)
print("BITIS", flush=True)
