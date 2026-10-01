"""Z-Image bf16 → fp8_e4m3fn, tensör tensör (KURULUM-GÖRSEL K6). ComfyUI .venv python'u ile koşar.

≥2 boyutlu kayan nokta ağırlıklar fp8_e4m3fn (±448'e kırpılır), 1 boyutlular (norm/bias) kaynak türünde kalır.
Kaynak RAM'e bütün alınmaz: başlık önce hesaplanır, tensörler sırayla okunup yazılır. Sonda tepe çalışma kümesi yazılır.
"""
import ctypes
import json
import struct
import sys
from pathlib import Path

import torch
from safetensors import safe_open

MODELLER = Path(r"C:\AI\ComfyUI\models\diffusion_models")
KAYNAK = Path(sys.argv[1]) if len(sys.argv) > 1 else MODELLER / "z_image_turbo_bf16.safetensors"
HEDEF = Path(sys.argv[2]) if len(sys.argv) > 2 else MODELLER / "z_image_turbo_fp8_e4m3fn.safetensors"
TUR = {"BF16": torch.bfloat16, "F16": torch.float16, "F32": torch.float32}


def cevrilir(tur, sekil):
    return tur in TUR and len(sekil) >= 2


def tepe_gb():
    class Sayac(ctypes.Structure):
        _fields_ = [("cb", ctypes.c_ulong), ("PageFaultCount", ctypes.c_ulong)] + \
                   [(ad, ctypes.c_size_t) for ad in ("Peak", "WorkingSet", "a", "b", "c", "d", "e", "f")]
    s = Sayac(cb=ctypes.sizeof(Sayac))
    assert ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.c_void_p(-1), ctypes.byref(s), s.cb)  # -1: bu süreç
    return s.Peak / 2**30


with safe_open(KAYNAK, framework="pt") as f:
    baslik, konum = {}, 0
    for ad in f.keys():
        dilim = f.get_slice(ad)
        tur, sekil = dilim.get_dtype(), dilim.get_shape()
        yeni = "F8_E4M3" if cevrilir(tur, sekil) else tur
        boy = (1 if yeni == "F8_E4M3" else f.get_tensor(ad).element_size()) * int(torch.Size(sekil).numel())
        baslik[ad] = {"dtype": yeni, "shape": sekil, "data_offsets": [konum, konum + boy]}
        konum += boy
    baslik["__metadata__"] = {**(f.metadata() or {}), "kaynak": KAYNAK.name, "cevirici": "tools/gorsel/fp8_cevir.py"}
    ham = json.dumps(baslik, separators=(",", ":")).encode()
    ham += b" " * (-len(ham) % 8)
    gecici = HEDEF.with_suffix(".part")
    with open(gecici, "wb") as out:
        out.write(struct.pack("<Q", len(ham)) + ham)
        for ad, b in baslik.items():
            if ad == "__metadata__":
                continue
            t = f.get_tensor(ad)
            if b["dtype"] == "F8_E4M3":
                t = t.float().clamp(-448, 448).to(torch.float8_e4m3fn)
            out.write(t.contiguous().view(torch.uint8).numpy().tobytes())
gecici.replace(HEDEF)
cevrilen = sum(1 for b in baslik.values() if b.get("dtype") == "F8_E4M3")
print(f"{HEDEF.name} {HEDEF.stat().st_size} bayt · {cevrilen}/{len(baslik) - 1} tensör fp8 · tepe RAM {tepe_gb():.1f} GB")
