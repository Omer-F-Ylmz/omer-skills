"""Hazır 3D varlık merdiveni (DEVAM-KURALI 3D/VARLIK): ara + indir + lisans/atıf JSON. Hesapsız, anahtarsız.
  python varlik_getir.py ara "<sorgu>" [--kaynak sketchfab|polyhaven|ambientcg] [--n 8]
  python varlik_getir.py indir objaverse <uid> <dizin>          (Sketchfab uid; objaverse paketi gerekir: pip install objaverse)
  python varlik_getir.py indir polyhaven <id> <dizin> [--cozunurluk 1k]
  python varlik_getir.py indir ambientcg <id> <dizin> [--cozunurluk 1K-JPG]
Her indirme <dizin>/atif.json'a {kaynak,id,ad,yazar,lisans,url,atif} satırı ekler; CC-BY ise atif metni kolofona girer.
Çıktı kompakt JSON (tek satır); görüntü yok. Küçük düzenleme: blender -b -P duzenle_b.py -- <gir.glb> <cik.glb> [seçenek]"""
import io, json, os, sys, urllib.parse, urllib.request, zipfile

UA = {"User-Agent": "omer-skills-varlik-getir/1.0"}
CC0 = "CC0"


def _json(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return json.load(r)


def _indir(url, yol):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r, open(yol, "wb") as f:
        f.write(r.read())
    return os.path.getsize(yol)


def _icinde(dizin, ad):
    """API'den gelen göreli ad dizin dışına çıkamaz (../ ya da mutlak yol)."""
    y = os.path.abspath(os.path.join(dizin, ad))
    if os.path.commonpath([y, os.path.abspath(dizin)]) != os.path.abspath(dizin):
        raise ValueError(f"dizin dışı yol: {ad}")
    return y


def atif(kayit, dizin):
    """atif.json'a ekler (aynı kaynak+id varsa günceller)."""
    y = os.path.join(dizin, "atif.json")
    hepsi = json.load(open(y, encoding="utf-8")) if os.path.exists(y) else []
    hepsi = [k for k in hepsi if (k["kaynak"], k["id"]) != (kayit["kaynak"], kayit["id"])] + [kayit]
    json.dump(hepsi, open(y, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return kayit


def atif_metni(ad, yazar, lisans, url):
    return "" if lisans == CC0 else f'"{ad}" — {yazar} ({url}), {lisans}'


def ara(q, kaynak, n):
    if kaynak == "sketchfab":  # genel arama hesapsız; indirme Objaverse'ten (uid aynı)
        r = _json("https://api.sketchfab.com/v3/search?" + urllib.parse.urlencode({"type": "models", "q": q, "downloadable": "true", "count": n}))
        return [{"uid": m["uid"], "ad": m["name"], "yazar": m["user"]["username"], "lisans": (m.get("license") or {}).get("label"),
                 "yuz": m.get("faceCount")} for m in r["results"][:n]]
    if kaynak == "polyhaven":
        q = q.lower()
        r = _json("https://api.polyhaven.com/assets")
        return [{"id": k, "ad": v["name"], "tur": ["hdri", "doku", "model"][v["type"]]}
                for k, v in r.items() if q in k.lower() or q in v["name"].lower() or any(q in t.lower() for t in v.get("tags", []) + v.get("categories", []))][:n]
    r = _json("https://ambientcg.com/api/v2/full_json?" + urllib.parse.urlencode({"q": q, "type": "Material", "limit": n}))
    return [{"id": a["assetId"], "ad": a.get("displayName", a["assetId"])} for a in r["foundAssets"]]


def indir(kaynak, i, dizin, coz):
    os.makedirs(dizin, exist_ok=True)
    if kaynak == "objaverse":
        import objaverse, shutil
        a = objaverse.load_annotations([i]).get(i)
        if not a:
            sys.exit(f"Objaverse'te yok: {i} (Sketchfab'den indirmek Ömer'in token'ını ister — merdiven basamak 4)")
        y = os.path.join(dizin, f"{i[:8]}.glb"); shutil.copy(objaverse.load_objects(uids=[i], download_processes=1)[i], y)
        lis = {"by": "CC-BY-4.0", "by-sa": "CC-BY-SA-4.0", "cc0": CC0}.get(a.get("license"), a.get("license"))  # by-nc vb. aynen: karar Ömer'in
        k = {"kaynak": "objaverse", "id": i, "ad": a.get("name"), "yazar": a.get("user", {}).get("username"), "lisans": lis,
             "url": a.get("viewerUrl"), "yuz": a.get("faceCount"), "dosya": [y], "kb": os.path.getsize(y) // 1024}
    elif kaynak == "polyhaven":
        info, files = _json(f"https://api.polyhaven.com/info/{i}"), _json(f"https://api.polyhaven.com/files/{i}")
        dosya = []
        if "gltf" in files:  # model: gltf + include'ları (bin, dokular)
            g = files["gltf"][coz]["gltf"]
            for ad, f in [(os.path.basename(g["url"]), g)] + list(g.get("include", {}).items()):
                y = _icinde(dizin, ad); os.makedirs(os.path.dirname(y), exist_ok=True); _indir(f["url"], y); dosya.append(y)
        elif "hdri" in files:
            f = files["hdri"][coz]["hdr"]; y = os.path.join(dizin, os.path.basename(f["url"])); _indir(f["url"], y); dosya.append(y)
        else:  # doku: harita başına jpg
            for harita, d in files.items():
                if isinstance(d, dict) and coz in d and "jpg" in d[coz]:
                    f = d[coz]["jpg"]; y = os.path.join(dizin, os.path.basename(f["url"])); _indir(f["url"], y); dosya.append(y)
        k = {"kaynak": "polyhaven", "id": i, "ad": info["name"], "yazar": ", ".join(info.get("authors", {})), "lisans": CC0,
             "url": f"https://polyhaven.com/a/{i}", "dosya": dosya}
    else:
        url = f"https://ambientcg.com/get?file={i}_{coz}.zip"
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r:
            z = zipfile.ZipFile(io.BytesIO(r.read()))
        hedef = os.path.join(dizin, i); z.extractall(hedef)
        k = {"kaynak": "ambientcg", "id": i, "ad": i, "yazar": "ambientCG", "lisans": CC0, "url": f"https://ambientcg.com/view?id={i}",
             "dosya": [os.path.join(hedef, n) for n in z.namelist()]}
    k["atif"] = atif_metni(k["ad"], k["yazar"], k["lisans"], k["url"])
    return atif(k, dizin)


def _sec(a, ad, vars_):
    return a[a.index(ad) + 1] if ad in a else vars_


if __name__ == "__main__":
    a = sys.argv[1:]
    sys.stdout.reconfigure(encoding="utf-8")
    if a[:1] == ["ara"]:
        print(json.dumps(ara(a[1], _sec(a, "--kaynak", "sketchfab"), int(_sec(a, "--n", 8))), ensure_ascii=False))
    elif a[:1] == ["indir"]:
        vars_ = {"polyhaven": "1k", "ambientcg": "1K-JPG"}.get(a[1], "")
        k = indir(a[1], a[2], a[3], _sec(a, "--cozunurluk", vars_))
        print(json.dumps({x: k[x] for x in k if x != "dosya"} | {"dosya_sayi": len(k["dosya"])}, ensure_ascii=False))
    else:
        sys.exit(__doc__)
