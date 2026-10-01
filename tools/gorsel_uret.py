"""Yerel görsel üretimi (KURULUM-GÖRSEL) — kırmızı aşama iskeleti."""
import subprocess
import sys
import tempfile
import time
from pathlib import Path

MASAUSTU = Path.home() / "Desktop"
DURUM = Path(tempfile.gettempdir()) / "gorsel-oturum.json"
COMFY = Path(r"C:\AI\ComfyUI")
HOST, PORT = "127.0.0.1", 8188
SUNUCU = f"http://{HOST}:{PORT}"

MODELLER = {
    "zimage": {"dosyalar": ["diffusion_models/z_image_turbo_bf16.safetensors", "text_encoders/qwen_3_4b.safetensors",
                            "vae/ae.safetensors"]},
    "klein": {"dosyalar": ["diffusion_models/flux-2-klein-4b.safetensors", "text_encoders/qwen_3_4b.safetensors",
                           "vae/flux2-vae.safetensors"]},
    "qwen-image": {"dosyalar": ["diffusion_models/qwen_image_fp8_e4m3fn.safetensors"]},
}
YONLENDIRME = {"foto": "zimage", "urun": "zimage", "doku": "zimage", "metinli": "klein", "duzenle": "klein"}


def main(argv=None):
    return 1


if __name__ == "__main__":
    sys.exit(main())
