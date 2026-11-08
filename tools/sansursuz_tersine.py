"""SANSURSUZ-3 tersine: iki safetensors klasoru (orijinal, degistirilmis) tensor tensor karsilastirir.
Cikti: JSON (tensor basina fark normu, SVD rank, sol tekil vektor, yon benzerligi). Kullanim:
  python sansursuz_tersine.py <orijinal_dir> <degisen_dir> <cikti_json>
Olcum betigi; ucuncu taraf kod kopyalanmadi."""
import json, sys, glob, os
import numpy as np
import torch
from safetensors import safe_open

dev = "cuda" if torch.cuda.is_available() else "cpu"
TOP = 8


def index(d):
    out = {}
    for f in sorted(glob.glob(os.path.join(d, "*.safetensors"))):
        with safe_open(f, "pt") as s:
            for k in s.keys():
                out[k] = f
    return out


def load(path, k):
    with safe_open(path, "pt") as s:
        return s.get_tensor(k)


def main():
    a, b, cikti = sys.argv[1:4]
    ia, ib = index(a), index(b)
    ortak = sorted(set(ia) & set(ib))
    yalniz = {"yalniz_orijinal": sorted(set(ia) - set(ib))[:20], "yalniz_degisen": sorted(set(ib) - set(ia))[:20]}
    sonuc, dirs = [], {}
    for k in ortak:
        x, y = load(ia[k], k), load(ib[k], k)
        if x.shape != y.shape:
            sonuc.append({"ad": k, "shape_farkli": [list(x.shape), list(y.shape)]})
            continue
        xf, yf = x.to(dev, torch.float32), y.to(dev, torch.float32)
        d = yf - xf
        fn = float(d.norm())
        r = {"ad": k, "shape": list(x.shape), "dtype": str(x.dtype), "fark_norm": fn,
             "w_norm": float(xf.norm()), "w2_norm": float(yf.norm())}
        r["goreli"] = fn / max(r["w_norm"], 1e-12)
        if fn > 0 and d.ndim == 2 and min(d.shape) > 1:
            s = torch.linalg.svdvals(d).cpu().numpy()
            r["sv_top"] = [float(v) for v in s[:TOP]]
            r["enerji_ilk1"] = float(s[0] ** 2 / (s ** 2).sum())
            r["enerji_ilk4"] = float((s[:4] ** 2).sum() / (s ** 2).sum())
            r["rank_1pct"] = int((s > 0.01 * s[0]).sum())
            r["rank_10pct"] = int((s > 0.10 * s[0]).sum())
            if r["enerji_ilk1"] > 0.5:
                u, _, _ = torch.linalg.svd(d, full_matrices=False)
                ud = u[:, 0]
                r["uW_orij"] = float((ud @ xf).norm())   # yon bilesenin orijinaldeki buyuklugu
                r["uW_yeni"] = float((ud @ yf).norm())   # ortogonallestirme sonrasi kalinti
                r["sutun_norm_oran"] = float((yf.norm(dim=0) / xf.norm(dim=0).clamp_min(1e-12)).mean())
                r["satir_norm_oran"] = float((yf.norm(dim=1) / xf.norm(dim=1).clamp_min(1e-12)).mean())
                dirs[k] = ud.cpu().numpy().tolist()
        sonuc.append(r)
        del xf, yf, d
    sim = {}
    by_dim = {}
    for k in dirs:
        by_dim.setdefault(len(dirs[k]), []).append(k)
    for dim, kk in by_dim.items():
        M = np.array([dirs[k] for k in kk])
        M /= np.linalg.norm(M, axis=1, keepdims=True)
        C = np.abs(M @ M.T)
        iu = np.triu_indices(len(kk), 1)
        sim[str(dim)] = {"adlar": kk, "ort_abs_cos": float(C[iu].mean()) if len(kk) > 1 else None,
                         "min": float(C[iu].min()) if len(kk) > 1 else None, "C": C.round(3).tolist()}
    json.dump({"a": a, "b": b, "ortak": len(ortak), **yalniz, "tensorler": sonuc, "yon_benzerlik": sim},
              open(cikti, "w", encoding="utf-8"))
    deg = [r for r in sonuc if r.get("fark_norm", 0) > 0]
    print(f"ortak {len(ortak)} | degisen {len(deg)} | yon-tensoru {len(dirs)}")


main()
