"""BLENDER-ARAC-2 K2: CC0 varlık indirici — Poly Haven (hdri · doku · model) + ambientCG (doku).

    python tools/varlik_indir.py ara polyhaven hdri|doku|model [--kategori studio] [--adet 10]
    python tools/varlik_indir.py ara ambientcg doku [--q Rock] [--adet 10]
    python tools/varlik_indir.py indir polyhaven|ambientcg <id> --hedef <Desktop\\<Proje>\\...> [--cozunurluk 1k|2k|4k]

İndirme yalnız Desktop\\<Proje>\\ altına (<hedef>\\<id>\\), Blender dışında. Dosyalar orijinal biçimde kalır (dönüşüm
yok; web sıkıştırması glb_hat'ın işi). Poly Haven: API md5 + boyut orijinal dosyada doğrulanır; ambientCG API özet
vermez → boyut doğrulanır, zip açılır. Her varlığa <id>.json: kaynak sayfa · lisans CC0 · yazar · sha256 + API özeti ·
tarih. Çıkış: 0 · 1 özet/boyut uyuşmazlığı (dosya silinir) ya da ağ/API hatası · 2 yol/kullanım.
"""
import argparse
import hashlib
import json
import sys
import time
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import blender_cli as bc  # noqa: E402

PH_API = "https://api.polyhaven.com"
ACG_API = "https://ambientcg.com/api/v2/full_json"
UA = {"User-Agent": "omer-skills-varlik-indir/1.0 (+https://github.com/Omer-F-Ylmz/omer-skills)"}
PH_TUR = {"hdri": "hdris", "doku": "textures", "model": "models"}
PH_HARITA = ("Diffuse", "nor_gl", "Rough")  # doku: renk · normal (GL) · pürüzlülük


def _al(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return json.loads(r.read())


def _indir(url, yol):
    """Akışla yazar → (sha256, md5, boyut)."""
    s, m, n = hashlib.sha256(), hashlib.md5(), 0
    yol.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r, open(yol, "wb") as f:
        while parca := r.read(1 << 16):
            s.update(parca)
            m.update(parca)
            n += len(parca)
            f.write(parca)
    return s.hexdigest(), m.hexdigest(), n


def _ph_dosyalar(id_, cz):
    """[(göreli yol, {url, size, md5})]; doku haritasında API'de jpg varsa o, yoksa png (dönüştürülmez)."""
    f = _al(f"{PH_API}/files/{id_}")
    if "hdri" in f:
        return [(Path(f["hdri"][cz]["hdr"]["url"]).name, f["hdri"][cz]["hdr"])]
    if "gltf" in f:
        g = f["gltf"][cz]["gltf"]
        return [(Path(g["url"]).name, g)] + list(g.get("include", {}).items())
    return [(Path(d["url"]).name, d) for d in (f[h][cz].get("jpg") or f[h][cz]["png"] for h in PH_HARITA)]


def ara(a):
    if a.kaynak == "polyhaven":
        q = {"t": PH_TUR[a.tur]} | ({"c": a.kategori} if a.kategori else {})
        v = _al(f"{PH_API}/assets?{urllib.parse.urlencode(q)}")
        print("\n".join(f"{k}\t{d.get('name', '')}" for k, d in list(v.items())[:a.adet]))
    else:
        v = _al(f"{ACG_API}?{urllib.parse.urlencode({'type': 'Material', 'q': a.q or '', 'limit': a.adet})}")
        print("\n".join(f"{d['assetId']}\t{d.get('displayName', '')}" for d in v.get("foundAssets", [])))
    return 0


def indir(a):
    hedef = Path(a.hedef) / a.id
    if not bc.proje_ici(hedef):
        print(f"yol kuralı: indirme yalnız Desktop\\<Proje>\\ altına: {hedef}", file=sys.stderr)
        return 2
    if a.kaynak == "polyhaven":
        yazar = ", ".join(_al(f"{PH_API}/info/{a.id}").get("authors", {}))
        liste = _ph_dosyalar(a.id, a.cozunurluk)
        sayfa, dogrulama = f"https://polyhaven.com/a/{a.id}", "md5 + boyut (API)"
    else:
        v = _al(f"{ACG_API}?{urllib.parse.urlencode({'id': a.id, 'include': 'downloadData'})}")["foundAssets"][0]
        d = next(x for x in v["downloadFolders"]["default"]["downloadFiletypeCategories"]["zip"]["downloads"]
                 if x["attribute"] == f"{a.cozunurluk.upper()}-JPG")
        liste = [(d["fileName"], {"url": d["downloadLink"], "size": d["size"]})]
        yazar, sayfa, dogrulama = "ambientCG", f"https://ambientcg.com/a/{a.id}", "boyut (API özet vermiyor)"
    dosyalar = []
    for ad, d in liste:
        yol = hedef / ad
        if not yol.resolve().is_relative_to(hedef.resolve()):  # API'den gelen göreli yol dışarı çıkamaz
            print(f"yol kuralı: {ad} hedef dışına çıkıyor", file=sys.stderr)
            return 2
        sha, md5, n = _indir(d["url"], yol)
        if d.get("md5", md5) != md5 or d.get("size", n) != n:
            yol.unlink()
            print(f"özet uyuşmazlığı: {ad} · md5 API {d.get('md5')} / yerel {md5} · boyut API {d.get('size')} / {n}; "
                  "dosya silindi")
            return 1
        dosyalar.append({"yol": ad, "sha256": sha, "api_ozet": d.get("md5"), "boyut": n})
        if yol.suffix == ".zip":
            with zipfile.ZipFile(yol) as z:
                z.extractall(hedef)
    kayit = {"kaynak": a.kaynak, "id": a.id, "kaynak_sayfa": sayfa, "lisans": "CC0", "yazar": yazar,
             "cozunurluk": a.cozunurluk, "dogrulama": dogrulama, "dosyalar": dosyalar, "tarih": time.strftime("%Y-%m-%d")}
    if a.kaynak == "polyhaven":
        kayit["not"] = "Powered by Poly Haven (polyhaven.com)"
    (hedef / f"{a.id}.json").write_text(json.dumps(kayit, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"json": str(hedef / f"{a.id}.json"), "dosya": len(dosyalar), "dogrulama": dogrulama},
                     ensure_ascii=False))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="CC0 varlık indirici (Poly Haven · ambientCG)")
    alt = ap.add_subparsers(dest="komut", required=True)
    r = alt.add_parser("ara")
    r.add_argument("kaynak", choices=["polyhaven", "ambientcg"])
    r.add_argument("tur", choices=list(PH_TUR))
    r.add_argument("--kategori")
    r.add_argument("--q")
    r.add_argument("--adet", type=int, default=10)
    i = alt.add_parser("indir")
    i.add_argument("kaynak", choices=["polyhaven", "ambientcg"])
    i.add_argument("id")
    i.add_argument("--hedef", required=True)
    i.add_argument("--cozunurluk", choices=["1k", "2k", "4k"], default="1k")
    a = ap.parse_args(argv)
    if a.kaynak == "ambientcg" and getattr(a, "tur", "doku") != "doku":
        print("ambientCG yalnız doku", file=sys.stderr)
        return 2
    try:
        return (ara if a.komut == "ara" else indir)(a)
    except (OSError, KeyError, StopIteration, ValueError) as e:  # URLError/HTTPError ⊂ OSError
        print(f"ağ/API hatası: {e!r}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
