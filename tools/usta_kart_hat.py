"""IS6-ECC C: ustalik karti uretim hatti. Uretim ucretsiz havuzdan (usta_kart.uret, haric_aile=anthropic), her 200 kartta 10 rastgele
kart Sonnet ile puanlanir; dogruluk >= %98 degilse hat DURUR (durum=DURDU) ve sablon duzeltilmeden devam etmez. Artan: kartli adlar atlanir.
  python -I tools/usta_kart_hat.py [--parti 200] [--hedef 99999] [--is 3] [--kapi-n 10]
Durum: .kos/kopru/usta-kart-durum.json. Sinirlar: RAM <= %95, bos disk >= 35 GB."""
import ctypes, json, os, random, shutil, subprocess, sys, time
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).parent))
import usta_kart as UK  # noqa: E402

DURUM = KOK / ".kos/kopru/usta-kart-durum.json"
ESIK = 0.98
RAM_TAVAN, DISK_TABAN = 95, 35 * 2**30


def ram_yuzde():
    class M(ctypes.Structure):
        _fields_ = [("l", ctypes.c_ulong), ("yuk", ctypes.c_ulong)] + [(n, ctypes.c_ulonglong) for n in ("t", "b", "st", "sb", "vt", "vb", "ex")]
    m = M(); m.l = ctypes.sizeof(M)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.yuk


def kaynak_yeterli():
    """(ok, neden): RAM ve disk sinirlari."""
    r = ram_yuzde()
    if r > RAM_TAVAN:
        return False, f"RAM %{r} > %{RAM_TAVAN}"
    d = shutil.disk_usage(str(KOK)).free
    if d < DISK_TABAN:
        return False, f"disk {d // 2**30} GB < 35 GB"
    return True, ""


def gecer(ok, n):
    return n > 0 and ok / n >= ESIK


def durum_oku():
    try:
        return json.loads(DURUM.read_text(encoding="utf-8"))
    except Exception:
        return {"kapi_gecen": 0, "partiler": [], "durum": "BASLADI"}


def durum_yaz(d):
    d["guncel"] = time.strftime("%Y-%m-%d %H:%M:%S")
    DURUM.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def hakem_sonnet(kartlar, n):
    """Sonnet hakem (NIHAI 49): n rastgele kart, kaynaga gore dogru+yararli. (ok, n, reddedilenler)"""
    ornek = random.sample(kartlar, min(n, len(kartlar)))
    K = {k["ad"]: k for k in UK.kartlar()}
    par = "\n".join(f"[{i}] {c['ad']} | kaynak: {UK.kaynak(K[c['ad']])}\n kart: {json.dumps({x: c[x] for x in UK.ALANLAR}, ensure_ascii=False)}" for i, c in enumerate(ornek))
    ist = ("Hakemsin. Her kart icin: kaynak metne gore DOGRU (uydurma/yanlis yok) ve YARARLI (somut, genel gecer degil) mi? "
           'YALNIZ JSON dizisi: [{"i":0,"dogru":true,"yararli":true,"neden":"<=10 kelime"}...]\n\n' + par)
    r = subprocess.run(["claude", "-p", "--model", "claude-sonnet-5-5", "--no-session-persistence", "--tools", ""], input=ist, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=600, creationflags=0x08000000, stdin=None)
    m = r.stdout
    a = json.loads(m[m.index("["):m.rindex("]") + 1])
    ok = sum(1 for e in a if e.get("dogru") and e.get("yararli"))
    red = [(ornek[e["i"]]["ad"], e.get("neden")) for e in a if not (e.get("dogru") and e.get("yararli"))]
    return ok, len(a), red


def parti(n, is_, kapi_n):
    t0 = int(time.time())
    once = set(UK.oku_usta())
    UK.uret(n, is_)
    yeni = [c for ad, c in UK.oku_usta().items() if ad not in once and c.get("tarih", 0) >= t0]
    if not yeni:
        return {"yeni": 0, "kapi": "ATLANDI-bos"}
    ok, m, red = hakem_sonnet(yeni, kapi_n)
    return {"yeni": len(yeni), "kapi": f"{ok}/{m}", "gecti": gecer(ok, m), "red": red}


def main():
    a = sys.argv[1:]
    g = lambda ad, v: int(a[a.index(ad) + 1]) if ad in a else v  # noqa: E731
    n, hedef, is_, kapi_n = g("--parti", 200), g("--hedef", 10**6), g("--is", 3), g("--kapi-n", 10)
    d = durum_oku()
    if d.get("durum") == "DURDU" and "--devam" not in a:
        print("DURDU: kapi gecilemedi, sablon duzeltilmeden devam yok (--devam ile zorla)"); return 2
    d["durum"] = "CALISIYOR"; durum_yaz(d)
    bos = 0
    while len(UK.oku_usta()) < hedef and bos < 6:
        ok, neden = kaynak_yeterli()
        if not ok:
            d["durum"] = "BEKLIYOR-" + neden; durum_yaz(d); time.sleep(300); continue
        p = parti(n, is_, kapi_n)
        p["zaman"] = time.strftime("%H:%M:%S"); p["toplam"] = len(UK.oku_usta())
        d["partiler"].append(p)
        if p["yeni"] == 0:
            bos += 1; d["durum"] = "CALISIYOR"; durum_yaz(d); time.sleep(120); continue
        bos = 0
        if not p.get("gecti"):
            d["durum"] = "DURDU"; durum_yaz(d)
            print("KAPI KALDI", p); return 1
        d["kapi_gecen"] += p["yeni"]; d["durum"] = "CALISIYOR"; durum_yaz(d)
        print("parti", p["yeni"], "kapi", p["kapi"], "kapi_gecen", d["kapi_gecen"], "toplam", p["toplam"], flush=True)
    d["durum"] = "BITTI" if len(UK.oku_usta()) >= hedef else "BOS-HAVUZ"; durum_yaz(d)
    return 0


if __name__ == "__main__":
    sys.exit(main())
