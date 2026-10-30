"""PROFIL-GORSEL-1 tur4: ücretsiz bulut görsel modelleriyle imza öğesi adayları.
Sıra: Cloudflare flux-1-schnell -> NVIDIA flux -> HF -> fal. Kota/hata -> sıradakine geç.
Kullanim: python tools/profil_bulut.py <marka> <n> <prompt dosyası(her satır bir prompt)>  -> <marka>/v3/aday/"""
import base64, io, json, os, sys, time, urllib.request, urllib.error
from PIL import Image

OUT = os.path.join(os.path.expanduser("~"), "Desktop", "Claude ile yapılanlar", "sosyal-oto", "marka")
UA = {"User-Agent": "Mozilla/5.0"}


def post(url, hdr, body, t=120):
    r = urllib.request.Request(url, json.dumps(body).encode(), {**UA, "Content-Type": "application/json", **hdr})
    return json.loads(urllib.request.urlopen(r, timeout=t).read())


def cf(p, seed):
    j = post(f"https://api.cloudflare.com/client/v4/accounts/{os.environ['CLOUDFLARE_ACCOUNT_ID']}/ai/run/@cf/black-forest-labs/flux-1-schnell",
             {"Authorization": "Bearer " + os.environ["CLOUDFLARE_API_KEY"]}, {"prompt": p + " variation %d" % seed, "steps": 6})
    return base64.b64decode(j["result"]["image"])


def nv(p, seed):
    j = post("https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.1-schnell",
             {"Authorization": "Bearer " + os.environ["NVIDIA_API_KEY"], "Accept": "application/json"},
             {"prompt": p, "width": 1024, "height": 1024, "seed": seed, "steps": 4})
    return base64.b64decode(j["artifacts"][0]["base64"])


def hf(p, seed):
    r = urllib.request.Request("https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell",
                               json.dumps({"inputs": p, "parameters": {"seed": seed}}).encode(),
                               {**UA, "Authorization": "Bearer " + os.environ["HF_TOKEN"], "Content-Type": "application/json"})
    return urllib.request.urlopen(r, timeout=180).read()


def fal(p, seed):
    j = post("https://fal.run/fal-ai/flux/schnell", {"Authorization": "Key " + os.environ["FAL_KEY"]},
             {"prompt": p, "seed": seed, "image_size": "square_hd", "num_inference_steps": 4}, 180)
    return urllib.request.urlopen(urllib.request.Request(j["images"][0]["url"], headers=UA), timeout=120).read()


PROV = [("cf", cf), ("nv", nv), ("hf", hf), ("fal", fal)]


def uret(p, seed, dead):
    for ad, fn in PROV:
        if ad in dead:
            continue
        try:
            b = fn(p, seed)
            Image.open(io.BytesIO(b)).verify()
            return ad, b
        except Exception as e:
            code = getattr(e, "code", "")
            print("  ", ad, "hata", type(e).__name__, code, str(e)[:80].replace(os.environ.get("FAL_KEY", "\0"), "*"))
            if code in (401, 402, 403, 404, 429) or not code:
                dead.add(ad)
    return None, None


def main():
    marka, n, pf = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    prompts = [l.strip() for l in open(pf, encoding="utf-8") if l.strip()]
    d = os.path.join(OUT, marka, "v3", "aday"); os.makedirs(d, exist_ok=True)
    dead = set()
    for i in range(n):
        p = prompts[i % len(prompts)]
        ad, b = uret(p, 100 + i, dead)
        if not b:
            print("tum saglayicilar tukendi", i); break
        fp = os.path.join(d, f"{marka}-{i:02d}-{ad}.png"); open(fp, "wb").write(b); print("ok", fp)


if __name__ == "__main__":
    main()
