"""SITE-MALZEME-1: site malzemesi (görsel · video · image-to-3D) için tek arayüz.

Kullanım: python tools/uret_malzeme.py gorsel|video|3d --cikti DIZIN [--prompt ...] [--girdi görsel] [--bacak "p1" "p2"]
          [--kare] [--kuru] [--tavan USD] [--saglayici ad] [--adet N]
Sıra: ücretsiz/yerel (ComfyUI, HF ZeroGPU) → ucuzdan pahalıya ücretli (fal, Higgsfield). Ücretli gerçek üretim --tavan ister;
tahmin tavanı aşarsa sağlayıcı seçilmez. --kuru yalnız plan + maliyet tahmini yazar. Anahtar değerleri yazdırılmaz.
Çıkış: 0 tamam · 1 üretilemedi · 2 kural ihlali (sağlayıcı yok / tavan yok-aşıldı).
"""
import argparse
import base64
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
HIGGS_PY = Path(r"C:\Users\pc\.venvs\higgsfield\Scripts\python.exe")
FAL_ISTEK = {  # tür → (uç, istek alanı, yanıttan URL); tahminler USD/adet, fal fiyat sayfasından değil elle: DOĞRULANMADI
    "gorsel": ("fal-ai/flux/schnell", "image_url", lambda r: r["images"][0]["url"], 0.003),
    "video": ("fal-ai/ltx-video/image-to-video", "image_url", lambda r: r["video"]["url"], 0.10),
    "3d": ("fal-ai/trellis", "image_url", lambda r: r["model_mesh"]["url"], 0.02),
}
FAL_3D_PAHALI = ("tripo3d/tripo/v2.5/image-to-3d", 0.30)  # --model tripo


class Saglayici:
    ad, ucretsiz, turler = "?", False, ()

    def tahmin(self, tur, adet=1):
        raise NotImplementedError

    def hazir(self):
        raise NotImplementedError

    def uret(self, tur, prompt, girdi, cikti):
        raise NotImplementedError


class Comfy(Saglayici):
    """Yerel ComfyUI (tools/gorsel_uret.py). Video (Wan 2.2) için iş akışı bağlı değil → yalnız görsel."""
    ad, ucretsiz, turler = "comfyui", True, ("gorsel",)

    def tahmin(self, tur, adet=1):
        return 0.0

    def hazir(self):
        return (Path(r"C:\AI\ComfyUI\main.py")).exists()

    def uret(self, tur, prompt, girdi, cikti):
        py = [sys.executable, "-I", str(HERE / "gorsel_uret.py")]
        subprocess.run(py + ["ac"], check=True)
        try:
            subprocess.run(py + ["uret", "--is", "urun", "--prompt", prompt, "--cikti", str(cikti.parent)], check=True)
        finally:
            subprocess.run(py + ["kapat"])
        return cikti


class HFUzay(Saglayici):
    """HF ZeroGPU Space (tencent/Hunyuan3D-2): ücretsiz, günlük kota; kota bitince hata verir."""
    ad, ucretsiz, turler = "hf-zerogpu", True, ("3d",)

    def tahmin(self, tur, adet=1):
        return 0.0

    def hazir(self):
        try:
            import gradio_client  # noqa: F401
        except ImportError:
            return False
        return bool(os.environ.get("HF_TOKEN"))

    def uret(self, tur, prompt, girdi, cikti):
        from gradio_client import Client, handle_file
        c = Client("tencent/Hunyuan3D-2", token=os.environ["HF_TOKEN"])
        sonuc = c.predict(image=handle_file(str(girdi)), steps=30, guidance_scale=5.0, seed=1234, octree_resolution=256,
                          check_box_rembg=True, num_chunks=200000, randomize_seed=True, api_name="/shape_generation")
        src = sonuc[0]
        cikti.write_bytes(Path(src["value"] if isinstance(src, dict) else src).read_bytes())
        return cikti


def _json(url, govde=None, anahtar="", yontem=None):
    req = urllib.request.Request(url, data=json.dumps(govde).encode() if govde is not None else None, method=yontem,
                                 headers={"Authorization": f"Key {anahtar}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


class Fal(Saglayici):
    ad, turler = "fal", ("gorsel", "video", "3d")

    def __init__(self, model=None):
        self.model = model

    def tahmin(self, tur, adet=1):
        fiyat = FAL_3D_PAHALI[1] if (tur == "3d" and self.model == "tripo") else FAL_ISTEK[tur][3]
        return fiyat * adet

    def hazir(self):
        return bool(os.environ.get("FAL_KEY"))

    def uret(self, tur, prompt, girdi, cikti):
        uc, alan, cek, _ = FAL_ISTEK[tur]
        if tur == "3d" and self.model == "tripo":
            uc = FAL_3D_PAHALI[0]
        govde = {"prompt": prompt} if prompt else {}
        if girdi:
            govde[alan] = "data:image/png;base64," + base64.b64encode(Path(girdi).read_bytes()).decode()
        k = os.environ["FAL_KEY"]
        is_ = _json(f"https://queue.fal.run/{uc}", govde, k)
        while _json(is_["status_url"], anahtar=k).get("status") != "COMPLETED":
            time.sleep(3)
        url = cek(_json(is_["response_url"], anahtar=k))
        with urllib.request.urlopen(url, timeout=300) as r:
            cikti.write_bytes(r.read())
        return cikti


class Higgsfield(Saglayici):
    """Ücretli ve en son. Model kimlikleri DOĞRULANMADI; yalnız --saglayici higgsfield ile (sırada yer almaz)."""
    ad, turler = "higgsfield", ("gorsel", "video")
    MODEL = {"gorsel": "higgsfield-ai/soul/standard", "video": "higgsfield-ai/dop/standard"}
    FIYAT = {"gorsel": 0.10, "video": 0.50}  # kredi→USD kaba tahmin

    def tahmin(self, tur, adet=1):
        return self.FIYAT[tur] * adet

    def hazir(self):
        return HIGGS_PY.exists() and bool(os.environ.get("HIGGSFIELD_API_KEY"))

    def uret(self, tur, prompt, girdi, cikti):
        kod = ("import sys,json,urllib.request,higgsfield_client as h;a=json.loads(sys.argv[2]);"
               "r=h.subscribe(sys.argv[1],arguments=a);u=(r.get('images') or [r.get('video')])[0]['url'];"
               "open(sys.argv[3],'wb').write(urllib.request.urlopen(u).read())")
        arg = {"prompt": prompt}
        if girdi:
            arg["image_url"] = "data:image/png;base64," + base64.b64encode(Path(girdi).read_bytes()).decode()
        env = dict(os.environ, HF_KEY=os.environ["HIGGSFIELD_API_KEY"])
        subprocess.run([str(HIGGS_PY), "-c", kod, self.MODEL[tur], json.dumps(arg), str(cikti)], check=True, env=env)
        return cikti


def sirala(tur, saglayicilar):
    uygun = [s for s in saglayicilar if tur in s.turler and s.hazir()]
    return sorted(uygun, key=lambda s: (not s.ucretsiz, s.tahmin(tur)))


def sec(tur, saglayicilar, tavan, adet=1):
    sira = sirala(tur, saglayicilar)
    if not sira:
        raise ValueError(f"{tur}: hazır sağlayıcı yok")
    for s in sira:
        if s.ucretsiz or (tavan is not None and s.tahmin(tur, adet) <= tavan):
            return s
    raise ValueError(f"{tur}: ücretli sağlayıcı için --tavan gerekli ya da tahmin tavanı aştı "
                     f"({sira[0].ad} ≈ ${sira[0].tahmin(tur, adet):.3f}, tavan={tavan})")


def son_kare(video, hedef):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-sseof", "-0.1", "-i", str(video), "-frames:v", "1", str(hedef)], check=True)
    return hedef


def kare_dizisi(video, dizin, fps=24, genislik=1280):
    """Kaydırmaya bağlı kare dizisi: webp kareleri dizin/kare-0001.webp …"""
    dizin.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-vf", f"fps={fps},scale={genislik}:-2",
                    "-c:v", "libwebp", "-quality", "80", str(dizin / "kare-%04d.webp")], check=True)
    return sorted(dizin.glob("kare-*.webp"))


def video_bacaklari(s, promptlar, ilk_gorsel, cikti, son_kare_fn=son_kare):
    girdi, sonuc = Path(ilk_gorsel), []
    for i, p in enumerate(promptlar, 1):
        v = s.uret("video", p, girdi, cikti / f"bacak{i}.mp4")
        sonuc.append(v)
        if i < len(promptlar):
            girdi = son_kare_fn(v, cikti / f"bacak{i}-son.png")
    return sonuc


def main(argv=None):
    a = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    a.add_argument("tur", choices=["gorsel", "video", "3d"])
    a.add_argument("--cikti", required=True)
    a.add_argument("--prompt", default="")
    a.add_argument("--girdi")
    a.add_argument("--bacak", nargs="+")
    a.add_argument("--kare", action="store_true")
    a.add_argument("--kuru", action="store_true")
    a.add_argument("--tavan", type=float)
    a.add_argument("--saglayici")
    a.add_argument("--model", choices=["tripo"])
    a.add_argument("--adet", type=int, default=1)
    n = a.parse_args(argv)
    hepsi = [Comfy(), HFUzay(), Fal(n.model), Higgsfield()]
    if n.saglayici:
        hepsi = [s for s in hepsi if s.ad == n.saglayici]
    else:
        hepsi = [s for s in hepsi if s.ad != "higgsfield"]  # Higgsfield yalnız açıkça istenince
    adet = len(n.bacak) if n.bacak else n.adet
    if n.kuru:
        for s in sirala(n.tur, hepsi) or []:
            print(f"{s.ad}: tahmin ${s.tahmin(n.tur, adet):.3f} ({'ücretsiz' if s.ucretsiz else 'ücretli'})")
        return 0
    try:
        s = sec(n.tur, hepsi, n.tavan, adet)
    except ValueError as e:
        print(e, file=sys.stderr)
        return 2
    out = Path(n.cikti)
    out.mkdir(parents=True, exist_ok=True)
    ext = {"gorsel": "png", "video": "mp4", "3d": "glb"}[n.tur]
    try:
        if n.tur == "video" and n.bacak:
            sonuc = video_bacaklari(s, n.bacak, n.girdi, out)
        else:
            sonuc = [s.uret(n.tur, n.prompt, n.girdi, out / f"{n.tur}-{s.ad}.{ext}")]
        if n.kare and n.tur == "video":
            for v in sonuc:
                kare_dizisi(v, out / f"{v.stem}-kareler")
    except Exception as e:  # noqa: BLE001 — sağlayıcı hatası kullanıcıya düz metin
        print(f"{s.ad}: {type(e).__name__}: {e}", file=sys.stderr)
        return 1
    for p in sonuc:
        print(p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
