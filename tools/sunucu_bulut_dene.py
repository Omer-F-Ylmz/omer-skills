"""Ucretsiz bulut gorsel yollarini tek istekle yoklar (SUNUCU-KARAKTER-1). Anahtar degeri basilmaz."""
import os, sys, json, base64, urllib.request, urllib.error

PROMPT = ("stylized 3D animated character, friendly small orange robot mascot with teal visor face and antenna, "
          "Pixar-like soft studio lighting, clean pastel background, full body, front view")
OUT = sys.argv[1] if len(sys.argv) > 1 else "."


def post(url, hdr, body, t=120):
    r = urllib.request.Request(url, json.dumps(body).encode(), {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0", **hdr})
    try:
        with urllib.request.urlopen(r, timeout=t) as f:
            return f.status, f.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()[:200]
    except Exception as e:
        return 0, str(e).encode()[:200]


def nvidia():
    k = os.environ.get("NVIDIA_API_KEY")
    return post("https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.1-schnell",
                {"Authorization": "Bearer " + k, "Accept": "application/json"},
                {"prompt": PROMPT, "width": 1024, "height": 1024, "seed": 7, "steps": 4})


def hf():
    k = os.environ.get("HF_TOKEN")
    return post("https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell",
                {"Authorization": "Bearer " + k}, {"inputs": PROMPT})


def fal():
    k = os.environ.get("FAL_KEY")
    return post("https://fal.run/fal-ai/flux/schnell", {"Authorization": "Key " + k}, {"prompt": PROMPT, "image_size": "square_hd"})


def cf():
    a = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    k = os.environ.get("CLOUDFLARE_API_KEY") or os.environ.get("CLOUDFLARE_API_TOKEN") or os.environ.get("CF_API_TOKEN")
    if not k:
        return 0, b"anahtar yok"
    return post(f"https://api.cloudflare.com/client/v4/accounts/{a}/ai/run/@cf/black-forest-labs/flux-1-schnell",
                {"Authorization": "Bearer " + k}, {"prompt": PROMPT})


for ad, fn in (("nvidia", nvidia), ("hf", hf), ("fal", fal), ("cf", cf)):
    try:
        s, b = fn()
    except Exception as e:
        s, b = -1, str(e).encode()
    print(ad, s, len(b), b[:120] if s != 200 else "OK")
    if s == 200:
        open(os.path.join(OUT, f"deneme-{ad}.bin"), "wb").write(b)
