"""SANSURSUZ-3: iki GGUF'u (HF uzaktan, HTTP Range ile) tensor tensor karsilastirir; 38 GB inmez.
Kullanim:
  python sansursuz_gguf_diff.py info  <repo> <dosya>                 -> tensor envanteri
  python sansursuz_gguf_diff.py diff  <repoA> <dosyaA> <repoB> <dosyaB> <cikti.json> [desen ...]
Yalniz F32/F16/BF16/Q8_0 acilir (Q8_0 gurultusu ~%0.4, rank-1 duzenleme bunun ustunde gorunur).
Olcum betigi; ucuncu taraf kod kopyalanmadi (GGUF bicimi: ggml dokumantasyonundan)."""
import json, re, struct, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
import numpy as np

H = {"User-Agent": "Mozilla/5.0"}
SZ = {0: (1, 4), 1: (1, 2), 30: (1, 2), 8: (32, 34)}  # tip -> (blok elem, blok bayt)


def rng(url, a, b):
    r = urllib.request.Request(url, headers={**H, "Range": f"bytes={a}-{b}"})
    for _ in range(4):
        try:
            return urllib.request.urlopen(r, timeout=120).read()
        except Exception as e:
            err = e
    raise err


class Buf:
    def __init__(s, b): s.b, s.o = b, 0
    def u(s, f):
        n = struct.calcsize(f); v = struct.unpack_from("<" + f, s.b, s.o)[0]; s.o += n; return v
    def st(s):
        n = s.u("Q"); v = s.b[s.o:s.o + n].decode("utf-8", "replace"); s.o += n; return v


def val(p, t):
    if t == 8: return p.st()
    if t == 9:
        et, n = p.u("I"), p.u("Q")
        return [val(p, et) for _ in range(n)] if n < 64 else (lambda _: None)([val(p, et) for _ in range(n)])
    f = {0: "B", 1: "b", 2: "H", 3: "h", 4: "I", 5: "i", 6: "f", 7: "?", 10: "Q", 11: "q", 12: "d"}[t]
    return p.u(f)


def header(repo, fn):
    url = f"https://huggingface.co/{repo}/resolve/main/{fn}"
    for n in (16, 48, 128):
        raw = rng(url, 0, n * 1024 * 1024 - 1)
        try:
            p = Buf(raw)
            assert raw[:4] == b"GGUF"
            p.o = 4; p.u("I"); nt = p.u("Q"); nk = p.u("Q")
            kv = {}
            for _ in range(nk):
                k = p.st(); t = p.u("I"); kv[k] = val(p, t)
            ts = {}
            for _ in range(nt):
                nm = p.st(); nd = p.u("I"); dims = [p.u("Q") for _ in range(nd)]
                ty = p.u("I"); off = p.u("Q"); ts[nm] = (dims, ty, off)
            al = kv.get("general.alignment", 32)
            start = (p.o + al - 1) // al * al
            return url, kv, ts, start
        except (struct.error, AssertionError, IndexError) as e:
            print("deneme", n, "MB:", repr(e), len(raw), raw[:4], file=sys.stderr)
            continue
    raise RuntimeError("baslik cok buyuk")


def nbytes(dims, ty):
    n = int(np.prod(dims)); be, bb = SZ[ty]
    return n // be * bb


def fetch(url, start, ts, nm):
    dims, ty, off = ts[nm]
    raw = rng(url, start + off, start + off + nbytes(dims, ty) - 1)
    if ty == 0: a = np.frombuffer(raw, np.float32)
    elif ty == 1: a = np.frombuffer(raw, np.float16).astype(np.float32)
    elif ty == 30: a = (np.frombuffer(raw, np.uint16).astype(np.uint32) << 16).view(np.float32)
    else:
        b = np.frombuffer(raw, np.uint8).reshape(-1, 34)
        a = (b[:, :2].copy().view(np.float16).astype(np.float32) * b[:, 2:].view(np.int8).astype(np.float32)).reshape(-1)
    return a.reshape(list(reversed(dims)))


def info(repo, fn):
    url, kv, ts, start = header(repo, fn)
    print({k: v for k, v in kv.items() if k.startswith(("general.arch", "general.name", "general.file_type")) or "block_count" in k or "expert" in k})
    pat = {}
    for n, (d, t, o) in ts.items():
        pat.setdefault(re.sub(r"\d+", "#", n), []).append((n, d, t))
    for p, L in sorted(pat.items()):
        print(f"{p:50} n={len(L):3d} tip={L[0][2]:2d} dims={L[0][1]}")


def analiz(A, B):
    d = (B - A).astype(np.float32)
    r = {"shape": list(d.shape), "fark_norm": float(np.linalg.norm(d)), "w_norm": float(np.linalg.norm(A))}
    r["goreli"] = r["fark_norm"] / max(r["w_norm"], 1e-12)
    if d.ndim == 3:  # uzmanlar: (E, out, in) -> uzman bazli
        E = d.shape[0]
        en = np.linalg.norm(d.reshape(E, -1), axis=1) / np.maximum(np.linalg.norm(A.reshape(E, -1), axis=1), 1e-12)
        r["uzman_goreli_ort"] = float(en.mean()); r["uzman_goreli_min"] = float(en.min()); r["uzman_goreli_max"] = float(en.max())
        e1, U = [], []
        for e in range(E):
            u, s, _ = np.linalg.svd(d[e], full_matrices=False)
            e1.append(float(s[0] ** 2 / (s ** 2).sum())); U.append(u[:, 0])
        r["uzman_enerji_ilk1_ort"] = float(np.mean(e1)); r["uzman_enerji_ilk1_min"] = float(np.min(e1))
        U = np.array(U)
        s0 = U[0] if abs(U).max() else U[0]
        r["uzmanlar_arasi_abs_cos_ort"] = float(np.abs(U @ U[0]).mean())
        r["_u_ort"] = (np.sign(U @ U[0])[:, None] * U).mean(0).tolist()
    elif d.ndim == 2 and d.shape[0] > 1 and d.shape[1] > 1 and r["fark_norm"] > 0:
        u, s, vh = np.linalg.svd(d, full_matrices=False)
        r["sv_top"] = [float(x) for x in s[:6]]
        r["enerji_ilk1"] = float(s[0] ** 2 / (s ** 2).sum())
        r["rank_10pct"] = int((s > 0.1 * s[0]).sum())
        r["uW_orij"] = float(np.linalg.norm(u[:, 0] @ A)); r["uW_yeni"] = float(np.linalg.norm(u[:, 0] @ B))
        r["_u"] = u[:, 0].tolist()
    return r


def diff(ra, fa, rb, fb, cikti, pats):
    ua, _, tsa, sa = header(ra, fa)
    ub, _, tsb, sb = header(rb, fb)
    ortak = [n for n in tsa if n in tsb]
    sec = [n for n in ortak if any(re.search(p, n) for p in pats)]
    print("ortak", len(ortak), "| yalniz_A", len(set(tsa) - set(tsb)), "| yalniz_B", len(set(tsb) - set(tsa)), "| secilen", len(sec))

    def is_(n):
        try:
            if tsa[n][0] != tsb[n][0]: return n, {"shape_farkli": [tsa[n][0], tsb[n][0]]}
            if tsa[n][1] not in SZ or tsb[n][1] not in SZ: return n, {"tip": [tsa[n][1], tsb[n][1]], "atlandi": True}
            r = analiz(fetch(ua, sa, tsa, n), fetch(ub, sb, tsb, n))
            r["tip"] = [tsa[n][1], tsb[n][1]]
            return n, r
        except Exception as e:
            return n, {"hata": repr(e)[:150]}
    out = {}
    with ThreadPoolExecutor(4) as ex:
        for n, r in ex.map(is_, sec):
            out[n] = r
            print(n, {k: (round(v, 5) if isinstance(v, float) else v) for k, v in r.items() if not k.startswith("_") and k not in ("shape", "sv_top")}, flush=True)
    json.dump({"A": [ra, fa], "B": [rb, fb], "tensorler": out}, open(cikti, "w"))


if __name__ == "__main__":
    m = sys.argv[1]
    if m == "info": info(*sys.argv[2:4])
    else: diff(*sys.argv[2:7], sys.argv[7:] or [r"."])
