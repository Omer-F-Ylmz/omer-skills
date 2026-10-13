"""LAYA-1 kurulum (arka.py ile): ayrı venv C:/Projeler/.laya-venv · torch cu124 (RTX 4070 Ti) · laya 0.4.x · checkpoint ön-indirme + duman testi.
Kurulu hiçbir şey kaldırılmaz; ~/.claude'a dokunmaz. Anahtar gerekmez (HF açık checkpoint, Apache-2.0)."""
import subprocess
import sys

VENV = r"C:\Projeler\.laya-venv"
PY = VENV + r"\Scripts\python.exe"
NW = 0x08000000  # CREATE_NO_WINDOW


def kos(*a):
    print("$", " ".join(a), flush=True)
    r = subprocess.run(a, creationflags=NW)
    if r.returncode:
        sys.exit(f"rc {r.returncode}")


kos("uv", "venv", "--python", "3.12", VENV)
kos("uv", "pip", "install", "--python", PY, "torch", "--index-url", "https://download.pytorch.org/whl/cu124")
kos("uv", "pip", "install", "--python", PY, "laya", "scipy")
kos(PY, "-c", "import torch,laya;print('torch',torch.__version__,'cuda',torch.cuda.is_available(),'laya',laya.__version__);"
    "from laya import Router;r=Router(preload=True);"
    "q={'k':{'type':'score','instructions':'How urgent?','criteria':['no','soon','blocking']}};"
    "print(r.predict('Prod is down, nobody can log in.',q))")
print("KUR BITTI", flush=True)
