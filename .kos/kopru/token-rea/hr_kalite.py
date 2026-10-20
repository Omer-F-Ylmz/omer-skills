"""Headroom kalite + 4 eksen taban: betik üretimli, tohumlu araç-çıktısı yükleri; her yükte tek 'iğne' bilgi.
Kalite = iğne sıkıştırılmış çıktıda duruyor (doğrudan) ya da CCR hash işaretiyle geri alınabilir. Claude çağrısı YOK.
Headroom'un kendi python'uyla koş: <uv tools>/headroom-ai/Scripts/python.exe hr_kalite.py uret|skor <tohum>
Geliştiren oturum heldout/hr_<tohum>.json içeriğini OKUMAZ; yalnız skor çıktısını görür."""
import json, random, re, sys, time
from pathlib import Path

HO = Path(__file__).parent / "heldout"


def rss():  # Windows çalışma kümesi (bayt); psutil headroom ortamında yok
    import ctypes
    from ctypes import wintypes
    class C(ctypes.Structure):
        _fields_ = [("cb", wintypes.DWORD), ("pf", wintypes.DWORD)] + [(n, ctypes.c_size_t) for n in ("ws", "pws", "qpp", "qp", "qnpp", "qnp", "pf2", "ppf")]
    c = C(); c.cb = ctypes.sizeof(c)
    ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.windll.kernel32.GetCurrentProcess(), ctypes.byref(c), c.cb)
    return c.ws


def json_yuk(r, n):
    i = r.randrange(n)
    k = [{"id": j, "ad": f"gorev-{j}", "durum": "tamam", "sure": j * 3} for j in range(n)]
    k[i]["durum"] = f"HATA_{r.randrange(10**5)}"
    return json.dumps(k, ensure_ascii=False), k[i]["durum"]


def log_yuk(r, n):
    i, kod = r.randrange(n), f"kritik_{r.randrange(10**5)}"
    return "\n".join(f"2026-10-20 10:{j // 60:02d}:{j % 60:02d} INFO adim {j} tamam" if j != i else
                     f"2026-10-20 10:{j // 60:02d}:{j % 60:02d} ERROR {kod} dosya yok" for j in range(n)), kod


def arama_yuk(r, n):
    i, kod = r.randrange(n), f"hedef_{r.randrange(10**5)}"
    return "\n".join(f"src/mod{j}.py:{j * 7}: def isle_{j}(x): return x" if j != i else f"src/mod{j}.py:{j * 7}: def {kod}(x): return x * 2" for j in range(n)), kod


def fark_yuk(r, n):
    i, kod = r.randrange(n), f"yeni_{r.randrange(10**5)}"
    return "\n".join((f" satir {j} degismedi" if j != i else f"+{kod} = 1") for j in range(n)), kod


TUR = {"json": json_yuk, "log": log_yuk, "arama": arama_yuk, "fark": fark_yuk}
DIZI = ["json", "json", "json", "log", "log", "log", "arama", "arama", "fark", "fark"]


def uret(tohum):
    r, S = random.Random(int(tohum)), []
    for t in DIZI:
        m, igne = TUR[t](r, r.choice([150, 250, 400]))
        S.append({"tur": t, "yuk": m, "igne": igne})
    HO.mkdir(exist_ok=True)
    (HO / f"hr_{tohum}.json").write_text(json.dumps(S, ensure_ascii=False), encoding="utf-8")
    print("uretildi", len(S))


def skor(tohum):
    from headroom import compress
    S, R = json.loads((HO / f"hr_{tohum}.json").read_text(encoding="utf-8")), []
    for h in S:
        t, r0 = time.time(), rss()
        try:
            r = compress([{"role": "user", "content": "ne oldu?"}, {"role": "tool", "content": h["yuk"]}], model="claude-opus-5-5")
            c = r.messages[-1]["content"]
            c = c if isinstance(c, str) else json.dumps(c, ensure_ascii=False)
            hata = 0
        except Exception:  # noqa: BLE001
            c, hata, r = h["yuk"], 1, None
        dogrudan = int(h["igne"] in c)
        R.append(dict(tur=h["tur"], a=r.tokens_before if r else 0, b=r.tokens_after if r else 0, sn=round(time.time() - t, 2),
                      ram_mb=round((rss() - r0) / 1e6), dogrudan=dogrudan,
                      geri_alinir=int(dogrudan or bool(re.search(r"hash=\w+", c))), hata=hata))
    out = {}
    for ad, f in (("hepsi", lambda x: True), *[(t, lambda x, t=t: x["tur"] == t) for t in TUR]):
        L = [x for x in R if f(x)]
        a, b = sum(x["a"] for x in L), sum(x["b"] for x in L)
        out[ad] = dict(n=len(L), tasarruf_pct=round(100 * (a - b) / max(1, a), 1), dogrudan=round(sum(x["dogrudan"] for x in L) / len(L), 2),
                       geri_alinir=round(sum(x["geri_alinir"] for x in L) / len(L), 2), sn_ort=round(sum(x["sn"] for x in L) / len(L), 2),
                       passthrough=sum(1 for x in L if x["a"] and x["a"] == x["b"]), hata=sum(x["hata"] for x in L))
    print(json.dumps(out, ensure_ascii=False))
    (HO / f"hr_skor_{tohum}.json").write_text(json.dumps(dict(ozet=out, satir=R), ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    {"uret": uret, "skor": skor}[sys.argv[1]](sys.argv[2])
