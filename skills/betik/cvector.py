"""Yon .npz -> llama.cpp control vector GGUF (F32, tensör adi direction.<katman>).
  python cvector.py --yon yon.npz --cikti cv.gguf
Kullanim: llama-server --control-vector-scaled cv.gguf <olcek>
"""
import argparse, struct
import numpy as np

p = argparse.ArgumentParser()
p.add_argument("--yon", required=True); p.add_argument("--cikti", required=True)
a = p.parse_args()
y = np.load(a.yon)
D = y["dirs"].astype(np.float32)
katman = int(y["katman"])

kv = [("general.name", 8, b"ss-control-vector"), ("general.alignment", 4, struct.pack("<I", 32))]
tens = [(f"direction.{katman}", D.shape[1], D[k]) for k in range(D.shape[0])]

with open(a.cikti, "wb") as f:
    f.write(b"GGUF" + struct.pack("<IQQ", 3, len(tens), len(kv)))
    for k, t, v in kv:
        f.write(struct.pack("<Q", len(k)) + k.encode() + struct.pack("<I", t))
        f.write(v + (b"\0" if t == 8 else b""))
    ofs = 0
    for ad, boy, _ in tens:
        f.write(struct.pack("<Q", len(ad)) + ad.encode() + struct.pack("<I", 1))
        f.write(struct.pack("<Q", boy) + struct.pack("<I", 0) + struct.pack("<Q", ofs))
        ofs += boy * 4
    f.write(b"\0" * (-f.tell() % 32))
    for _, _, v in tens:
        f.write(np.asarray(v, np.float32).tobytes())
        f.write(b"\0" * (-f.tell() % 32))
print(a.cikti, "yazildi, katman", katman, "rank", D.shape[0])
