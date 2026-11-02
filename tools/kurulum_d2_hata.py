"""D2-HATA-1: kurulum-d2-sonuc.tsv'deki HATA + KURULDU-DOGRULANMADI kalemlerini gruplara göre yeniden dener (kök neden -> düzeltilmiş yol).
Kullanım: python tools/kurulum_d2_hata.py [--grup 0,1,...,9] [--is 3]   (8 = '0 skill': .kos/kopru/skill_sar.py ayrı koşar)
Gruplar: 1 uv derleme · 2 LLM erişilemedi · 3 release/exe yok · 4 import adı · 5 npm · 6 checkout · 7 wheel/ABI · 9 doğrulanmadı · 0 diğer"""
import csv, json, re, sys, subprocess
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import kurulum_d2 as D

D.DISK_ALT = 40 * 2**30  # görev tabanı: C: boş >= 40 GB
D.TKALEM = 600
D.TUR2 = True  # büyük repo eşiği 3 GB, HATA yeniden deneme kuralları
SADECE = set(sys.argv[sys.argv.index("--kalem") + 1].split("|")) if "--kalem" in sys.argv else set()
GRUPDOSYA = D.R / ".kos/kopru/log/d2-hata-gruplar.json"


def baslik_goc():
    """tsv başlığına 'kanit' sütunu ekler (eski satırlar 6 sütunlu kalır)."""
    t = D.SONUC.read_bytes().decode("utf-8")
    ilk, _, rest = t.partition("\n")
    if "kanit" not in ilk:
        D.SONUC.write_bytes((ilk.rstrip("\r") + "\tkanit" + ("\r" if ilk.endswith("\r") else "") + "\n" + rest).encode("utf-8"))


def grup(r):
    n = r["not"]
    if r["durum"] == "KURULDU-DOGRULANMADI": return 9
    if "LLM-ERISILEMEDI" in n: return 2
    if n.startswith("0 skill"): return 8
    if "checkout failed" in n or n.startswith("klon:"): return 6
    if "import başarısız" in n: return 4
    if re.search(r"ABI tag|no wheel|cp3\d+|--no-build|only-binary", n): return 7
    if re.search(r"release içinde exe yok|kurulum yolu yok|release indirilemedi", n): return 3
    if re.search(r"npm|\[eval\]|node", n, re.I): return 5
    if re.search(r"uv tool|pip:|setuptools|Build failures|entrypoints", n): return 1
    return 0


def uv_tool_listesi():
    c, o = D.run(["uv", "tool", "list"], 60)
    t, cur = {}, None
    for l in o.splitlines():
        m = re.match(r"^(\S+) v\S+", l)
        if m: cur = m.group(1).lower(); t[cur] = []
        elif l.strip().startswith("- ") and cur: t[cur].append(l.strip()[2:].strip())
    return t


def komut_dene(p):
    """komutu çalıştırır: (ok, kanıt). Traceback = bozuk (kök neden satırı)."""
    son = ""
    if Path(p).stem.lower() == "husky":  # husky ilk argümanı dizin sayıp git core.hooksPath'i değiştirir: çalıştırılmaz
        return True, "husky shim mevcut; çalıştırılmadı (argüman git core.hooksPath'ini bozar)"
    for a in ("--version", "--help", "-h"):
        c, o = D.run([p, a], 40)
        if "Traceback" in o:
            son = [l for l in o.splitlines() if l.strip()][-1][:90]
            return False, f"çalışınca Traceback: {son}"
        if c == 0 and o:
            return True, f"{Path(p).name} {a}: {o.splitlines()[0][:70]}"
        son = o[:60]
    return False, f"{Path(p).name} çalışmadı: {son}"


def g9(r, uvt):
    k, sinif, kay = r["kalem"], r["sinif"], r["kaynak"]
    tur, _, ad = kay.partition(":")
    d = Path(r["yol"]) if r["yol"] else None
    nm = D.NPMBIN / "node_modules"
    pjn = None
    if tur == "npm": pjn = nm / ad / "package.json"
    elif d and (d / "package.json").exists() and not (d / "pyproject.toml").exists():
        try: pjn = nm / json.loads((d / "package.json").read_text(encoding="utf-8")).get("name", "?") / "package.json"
        except Exception: pjn = None
    if pjn is not None:
        if not pjn.exists():
            return D.yaz(k, sinif, kay, "HATA", r["yol"], "npm -g ls: paket global kurulu değil", f"{pjn} yok")
        j = json.loads(pjn.read_text(encoding="utf-8", errors="ignore"))
        b = j.get("bin")
        bins = list(b) if isinstance(b, dict) else ([j["name"].split("/")[-1]] if b else [])
        if not bins:
            return D.yaz(k, sinif, kay, "HATA", r["yol"], "global kurulu ama package.json 'bin' tanımlamıyor (kütüphane/monorepo kökü): komut yok", f"{pjn.name}: bin alanı yok; npm.cmd ls -g: {j.get('name')}@{j.get('version')}")
        for e in bins:
            sh = D.NPMBIN / (e + ".cmd")
            if sh.exists():
                ok, n = komut_dene(str(sh))
                if ok: return D.yaz(k, sinif, kay, "KURULDU", r["yol"], f"komut {e}: {n}", f"npm -g bin {sh} -> {n}")
                return D.yaz(k, sinif, kay, "HATA", r["yol"], f"komut {e} bulundu ama doğrulanamadı: {n}", n)
        return D.yaz(k, sinif, kay, "HATA", r["yol"], f"bin {bins} için npm -g shim (.cmd) oluşmamış", f"{D.NPMBIN} içinde {bins} yok")
    # uv / pip yolu
    dist = ad.split("/")[-1].lower()
    if d and (d / "pyproject.toml").exists():
        try:
            import tomllib
            dist = tomllib.loads((d / "pyproject.toml").read_text(encoding="utf-8"))["project"]["name"].lower()
        except Exception: pass
    for ad_ in (dist, dist.replace("_", "-"), ad.split("/")[-1].lower()):
        if ad_ in uvt:
            for e in uvt[ad_]:
                p = D.yol_bul(e)
                if Path(p).exists():
                    ok, n = komut_dene(p)
                    if ok: return D.yaz(k, sinif, kay, "KURULDU", r["yol"], f"uv tool {ad_}: {n}", f"uv tool list: {ad_} -> {e}; {n}")
                    return D.yaz(k, sinif, kay, "HATA", r["yol"], f"uv tool {ad_} komutu {e}: {n}", n)
            return D.yaz(k, sinif, kay, "HATA", r["yol"], f"uv tool {ad_} kurulu ama exe listesi boş", "uv tool list")
    return D.yaz(k, sinif, kay, "HATA", r["yol"], "npm -g ls / uv tool list / PATH taramasında kurulu paket bulunamadı", f"uv tool list adayları: {dist}")


def main():
    a = sys.argv
    gr = {int(x) for x in a[a.index("--grup") + 1].split(",")} if "--grup" in a else set(range(10))
    kac = int(a[a.index("--is") + 1]) if "--is" in a else 3
    baslik_goc()
    son = {r["kalem"]: r for r in D.oku(D.SONUC)}
    if GRUPDOSYA.exists():
        ilk = json.loads(GRUPDOSYA.read_text(encoding="utf-8"))
    else:
        ilk = {k: grup(r) for k, r in son.items() if r["durum"] in ("HATA", "KURULDU-DOGRULANMADI")}
        GRUPDOSYA.write_text(json.dumps(ilk, ensure_ascii=False, indent=0), encoding="utf-8")
    coz = {r["kalem"]: r for r in D.oku(D.KOK / "kurulum-coz.tsv")}
    for g in sorted(gr):
        ks = [k for k, v in ilk.items() if v == g and (not SADECE or k in SADECE)]
        onc = Counter(son[k]["durum"] for k in ks if k in son)
        if g == 8 or not ks: print("grup", g, "atlandı/boş", len(ks)); continue
        print("grup", g, "başladı:", len(ks), dict(onc), flush=True)
        if g == 9:
            uvt = uv_tool_listesi()
            for k in ks: g9(son[k], uvt)
        else:
            def is_(k):
                if D.dur_mu(): return D.yaz(k, son[k]["sinif"], son[k]["kaynak"], "HATA", "", "disk C: < 40 GB: durduruldu")
                D.ram_bekle()
                return D.isle(coz[k])
            with ThreadPoolExecutor(kac) as ex: list(ex.map(is_, [k for k in ks if k in coz]))
        yeni = {r["kalem"]: r for r in D.oku(D.SONUC)}
        print("grup", g, "bitti:", dict(Counter(yeni[k]["durum"] for k in ks if k in yeni)), flush=True)
    print("TOPLAM:", dict(Counter(r["durum"] for r in {r["kalem"]: r for r in D.oku(D.SONUC)}.values())))


if __name__ == "__main__":
    main()
