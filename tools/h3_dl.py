from huggingface_hub import hf_hub_download as d
import os,time
M="C:/AI/ComfyUI/models/"
R="Comfy-Org/MiniMax-H3"
jobs=[("vae/minimax_h3_audio_vae_fp32.safetensors","vae"),
("vae/minimax_h3_video_vae_fp16.safetensors","vae"),
("loras/minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors","loras"),
("text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors","text_encoders"),
("diffusion_models/minimax_h3_fl2va_pruned_int8_convrot.safetensors","diffusion_models")]
for f,s in jobs:
    t=time.time()
    p=d(R,f,local_dir="C:/AI/indirilen/h3tmp")
    dst=M+s+"/"+os.path.basename(f)
    os.makedirs(M+s,exist_ok=True)
    os.replace(p,dst)
    print("OK",dst,os.path.getsize(dst),round(time.time()-t),"s",flush=True)
print("DONE")
