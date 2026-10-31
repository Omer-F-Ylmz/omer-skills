from huggingface_hub import hf_hub_download as d
import os,time
M="C:/AI/ComfyUI/models/"
jobs=[("unsloth/LTX-2.5-GGUF","latent_upscale_models/ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors","latent_upscale_models"),
("diverofdark/LTX-2.5-Gemma4-12B-heretic-int8-convrot","gemma4-12b-ltx-2.5-heretic-int8-convrot.safetensors","text_encoders"),
("unsloth/LTX-2.5-GGUF","distilled/ltx-2.5-22b-distilled-Q6_K.gguf","unet")]
for r,f,s in jobs:
    t=time.time()
    p=d(r,f,local_dir="C:/AI/indirilen/ltxtmp")
    dst=M+s+"/"+os.path.basename(f)
    os.makedirs(M+s,exist_ok=True)
    os.replace(p,dst)
    print("OK",dst,os.path.getsize(dst),round(time.time()-t),"s",flush=True)
print("DONE")
