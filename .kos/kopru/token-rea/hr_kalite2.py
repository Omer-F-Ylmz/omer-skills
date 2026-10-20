"""hr2 vs Headroom, aynı held-out yükte, aynı sayaç (tiktoken cl100k). Headroom'un python'uyla koş:
<uv tools>/headroom-ai/Scripts/python.exe hr_kalite2.py <tohum>   (önce: hr_kalite.py uret <tohum>)
Kalite = iğne çıktıda duruyor (doğrudan) ya da geri alma komutu tam metni (iğneli) döndürüyor. Süre hr2 için uçtan uca (subprocess).
Geliştiren oturum heldout/hr_<tohum>.json içeriğini OKUMAZ."""
import json, os, re, subprocess, sys, time
from pathlib import Path

import tiktoken

D = Path(__file__).parent
HR2 = str(D / "hr2.py")
E = tiktoken.get_encoding("cl100k_base")
tok = lambda s: len(E.encode(s, disallowed_special=()))
PY = os.environ.get("HR2_PY", "python")


def hr2_kos(m):
    t = time.time()
    p = subprocess.run([PY, "-I", "-S", HR2], input=m.encode("utf-8"), capture_output=True, env={**os.environ, "HR2_RAM": "1"})
    sn = time.time() - t
    return p.stdout.decode("utf-8"), sn, int(re.search(rb"ram_mb=(\d+)", p.stderr).group(1)) if b"ram_mb=" in p.stderr else 0


def headroom_kos(m):
    from headroom import compress
    t = time.time()
    c = compress([{"role": "user", "content": "ne oldu?"}, {"role": "tool", "content": m}], model="claude-opus-5-5").messages[-1]["content"]
    return (c if isinstance(c, str) else json.dumps(c, ensure_ascii=False)), time.time() - t


def geri(c, igne):  # çıktıda iğne ya da geri alma komutu iğneli tam metni verir
    if igne in c:
        return 1
    k = re.search(r"python -I -S (\S+) ac (\w+)", c)
    return int(bool(k) and igne in subprocess.run([PY, "-I", "-S", k.group(1), "ac", k.group(2)], capture_output=True).stdout.decode("utf-8"))


def skor(tohum):
    S, R = json.loads((D / "heldout" / f"hr_{tohum}.json").read_text(encoding="utf-8")), []
    for h in S:
        a = tok(h["yuk"])
        try:
            ch, snh = headroom_kos(h["yuk"])
        except Exception:  # noqa: BLE001
            ch, snh = h["yuk"], 0
        c2, sn2, ram2 = hr2_kos(h["yuk"])
        R.append(dict(tur=h["tur"], a=a, bh=tok(ch), b2=tok(c2), snh=snh, sn2=sn2, ram2=ram2,
                      dogh=int(h["igne"] in ch), dog2=int(h["igne"] in c2), geri2=geri(c2, h["igne"]), pass2=int(c2 == h["yuk"]), passh=int(ch == h["yuk"])))
    out = {}
    for ad, f in (("hepsi", lambda x: True), *[(t, lambda x, t=t: x["tur"] == t) for t in ("json", "log", "arama", "fark")]):
        L = [x for x in R if f(x)]
        a = sum(x["a"] for x in L)
        out[ad] = dict(n=len(L), tasarruf_headroom=round(100 * (a - sum(x["bh"] for x in L)) / a, 1), tasarruf_hr2=round(100 * (a - sum(x["b2"] for x in L)) / a, 1),
                       kalite_hr2=f'{sum(x["geri2"] for x in L)}/{len(L)}', dogrudan_hr2=sum(x["dog2"] for x in L), kalite_headroom_dogrudan=sum(x["dogh"] for x in L),
                       sn_headroom=round(sum(x["snh"] for x in L) / len(L), 2), sn_hr2=round(max(x["sn2"] for x in L), 2), sn_hr2_ort=round(sum(x["sn2"] for x in L) / len(L), 2),
                       ram_hr2_mb=max(x["ram2"] for x in L), pass_hr2=sum(x["pass2"] for x in L), pass_headroom=sum(x["passh"] for x in L))
    print(json.dumps(out, ensure_ascii=False))
    (D / "heldout" / f"hr2_skor_{tohum}.json").write_text(json.dumps(dict(ozet=out, satir=R), ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    skor(sys.argv[1])
