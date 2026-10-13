"""LAYA-1: checkpoint indirme (xet kapalı, düz HTTP — 05:14 xet aktarımı 0 baytta takıldı) + duman testi; arka.py ile."""
import os
import subprocess
import sys
PY = r"C:\Projeler\.laya-venv\Scripts\python.exe"
env = dict(os.environ, HF_HUB_DISABLE_XET="1", PYTHONUNBUFFERED="1")
env.pop("ANTHROPIC_API_KEY", None)
kod = ("from huggingface_hub import snapshot_download as s;p=s('convaiinnovations/laya');print('indi',p,flush=True);"
       "import torch,laya;print('torch',torch.__version__,'cuda',torch.cuda.is_available(),'laya',laya.__version__,flush=True);"
       "a=laya.load('convaiinnovations/laya',subfolder='multilingual');"
       "q={'k':{'type':'score','instructions':'How urgent?','criteria':['no','soon','blocking']}};"
       "print(a.predict_batch(['Prod is down, nobody can log in.','Typo in footer'],q,batch_size=4,max_len=4096))")
r = subprocess.run([PY, "-c", kod], env=env, creationflags=0x08000000)
print("INDIR BITTI rc", r.returncode, flush=True)
sys.exit(r.returncode)
