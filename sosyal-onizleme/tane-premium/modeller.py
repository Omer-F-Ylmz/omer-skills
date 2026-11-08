import os
for root in [r"C:\AI\ComfyUI\models",r"C:\AI\ComfyUI-T2\models",r"C:\AI\ComfyUI_windows_portable\ComfyUI\models"]:
    if not os.path.isdir(root): continue
    print("##",root)
    for d in ["diffusion_models","checkpoints","unet","text_encoders","vae","loras"]:
        p=os.path.join(root,d)
        if os.path.isdir(p):
            for f in os.listdir(p):
                fp=os.path.join(p,f)
                if os.path.isfile(fp): print(d,f,round(os.path.getsize(fp)/1e9,2),"GB")
