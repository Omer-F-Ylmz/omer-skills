"""FABLE-AJAN ölçümü: aile başına sonnet + haiku temsilci × 2 kol (taban / proto) × tekrar; Jev + regex rubriği.

Ajan `--agents {ad: …} --agent ad` ile ana oturum olur (model ajanınki, düşürülmez); proto kolu gövdeye godmode_onsoz.enjekte
ile protokol bloğu ekler (canlıya alınacak mekanizmanın aynısı). OLCUM_MCP_HAFIF=1 → kosucu/mcp_sec boş MCP.
Bellek: claude stdout'u geçici DOSYAYA yazılır, satır satır ayrıştırılır (PIPE/communicate yok); claude ağacı Job Object ile
JOB_TAVAN_MB'de kesilir; bu süreç çalışma kümesi OZ_TAVAN_MB'yi aşarsa yeni çağrı başlatmaz.
  python tools/olcum/fable_ajan_olc.py <cikti_dizin> [--aile fe,dn,…] [--tekrar 2] [--en-fazla 96] [--usd-tavan 10] [--protokol yol]
"""
import argparse, ctypes, json, os, random, re, subprocess, sys, tempfile, time
from pathlib import Path

DIZIN = Path(__file__).resolve().parent
KOK = DIZIN.parents[1]
sys.path[:0] = [str(DIZIN), str(KOK / "tools")]
import kosucu, mcp_sec  # noqa: E402
from godmode_onsoz import enjekte  # noqa: E402

AILELER = "fe,dn,sec,qa,db,bl,oyn,ajn,ara,dok,vid,vrm"
TAVAN = 120  # görev kuralı: ≤ 120 claude -p
JOB_TAVAN_MB, OZ_TAVAN_MB = 4096, 1024
BASLIK = "ajan\taile\tmodel\tkol\ttekrar\tinput\tcache_creation\tcache_read\toutput\tusd\tsure_sn\tregex\ttur\trc\n"


def protokol_govde(yol):
    """Tek kaynak: skill gövdesi (frontmatter hariç)."""
    m = re.match(r"---\r?\n.*?\r?\n---\r?\n", t := Path(yol).read_text(encoding="utf-8"), re.S)
    return t[m.end():].strip() if m else t.strip()


def on_bilgi(yol):
    t = Path(yol).read_text(encoding="utf-8")
    m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n", t, re.S)
    alan = dict(re.findall(r"^(\w+):\s*(.*)$", m.group(1), re.M))
    return alan, t[m.end():].strip()


def sec_temsilci(aileler, gorevler):
    """Aile × model başına ad sırasıyla ilk görevli ajan (deterministik)."""
    var = {g["ajan"] for g in gorevler}
    out = []
    for aile in aileler:
        for model in ("sonnet", "haiku"):
            adlar = sorted(p for p in (KOK / "ajanlar").glob(f"**/{aile}-*.md") if p.stem in var)
            for p in adlar:
                if on_bilgi(p)[0].get("model", "").strip() == model:
                    out.append((aile, model, p))
                    break
    return out


def is_bellek(is_):
    """kosucu iş nesnesine JOB_OBJECT_LIMIT_JOB_MEMORY ekler (KILL_ON_JOB_CLOSE korunur)."""
    if not is_:
        return
    s = (ctypes.c_byte * 144)()  # JOBOBJECT_EXTENDED_LIMIT_INFORMATION (x64)
    k = ctypes.windll.kernel32
    k.QueryInformationJobObject.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_ulong, ctypes.c_void_p]
    k.QueryInformationJobObject(is_, 9, s, 144, None)
    bayrak = ctypes.c_ulong.from_buffer(s, 16)
    bayrak.value |= 0x200  # JOB_OBJECT_LIMIT_JOB_MEMORY
    ctypes.c_size_t.from_buffer(s, 120).value = JOB_TAVAN_MB << 20  # JobMemoryLimit
    k.SetInformationJobObject(is_, 9, s, 144)


def oz_bellek_mb():
    if os.name != "nt":
        return 0

    class PMC(ctypes.Structure):
        _fields_ = [("cb", ctypes.c_ulong), ("pf", ctypes.c_ulong)] + [(f"a{i}", ctypes.c_size_t) for i in range(8)]
    p = PMC()
    p.cb = ctypes.sizeof(p)
    k, ps = ctypes.windll.kernel32, ctypes.windll.psapi
    k.GetCurrentProcess.restype = ctypes.c_void_p
    ps.GetProcessMemoryInfo.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong]
    ps.GetProcessMemoryInfo(k.GetCurrentProcess(), ctypes.byref(p), p.cb)
    return p.a1 >> 20  # WorkingSetSize


def kos_ajan(istem, ad, alan, govde, model, butce=0.6, timeout=600):
    tanim = {ad: {"description": alan.get("description", ""), "prompt": govde, "model": model,
                  "tools": [x.strip() for x in alan.get("tools", "").split(",") if x.strip()]}}
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_BASE_URL"}
    env["BROWSER"] = "none"
    with tempfile.TemporaryDirectory(prefix="olcum-", ignore_cleanup_errors=True) as bos, \
            tempfile.TemporaryDirectory(prefix="mcphafif-", ignore_cleanup_errors=True) as gizli:
        args = ["claude", "-p", istem, *kosucu.ROTA, "--max-budget-usd", f"{butce:.2f}", "--model", model,
                "--agents", json.dumps(tanim, ensure_ascii=False), "--agent", ad, *mcp_sec.ek(gizli, istem)]
        akis = Path(gizli) / "akis.jsonl"
        t = time.monotonic()
        with akis.open("w", encoding="utf-8", errors="replace") as f:
            is_ = kosucu.is_olustur()
            is_bellek(is_)
            pr = subprocess.Popen(args, stdout=f, stderr=subprocess.DEVNULL, env=env, cwd=bos, creationflags=kosucu.PENCERESIZ,
                                  encoding="utf-8", errors="replace")
            kosucu.is_ata(is_, pr)
            try:
                rc = pr.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                pr.kill()
                rc = -9
            finally:
                kosucu.is_kapat(is_)
        try:
            kosucu.supur(Path(bos).name)
        except subprocess.TimeoutExpired:  # yük altında CIM sorgusu 60 sn'yi aşıyor (fable-1-d4 19:04 bu yüzden düştü); iş nesnesi zaten kapandı
            print("supur zaman aşımı (atlandı)", flush=True)
        with akis.open(encoding="utf-8", errors="replace") as f:
            o = kosucu.ayristir(f)
    o["sure"], o["rc"] = round(time.monotonic() - t, 1), rc
    return o


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("cikti")
    ap.add_argument("--aile", default=AILELER)
    ap.add_argument("--tekrar", type=int, default=2)
    ap.add_argument("--en-fazla", type=int, default=96)
    ap.add_argument("--usd-tavan", type=float, default=10.0)
    ap.add_argument("--protokol", default=str(KOK / "skills" / "calisma-protokolu" / "SKILL.md"))
    ap.add_argument("--kuru", action="store_true", help="yalnız seçimi ve çağrı sayısını yaz")
    ns = ap.parse_args(argv)
    os.environ["OLCUM_MCP_HAFIF"] = "1"
    gorevler = json.loads((KOK / "ajanlar" / "kalite3" / "gorevler.json").read_text(encoding="utf-8"))
    gorev = {g["ajan"]: g for g in gorevler}
    secim = sec_temsilci(ns.aile.split(","), gorevler)
    isler = [(a, m, p, kol, r) for r in range(1, ns.tekrar + 1) for a, m, p in secim for kol in random.Random(r).sample(["taban", "proto"], 2)]
    en_fazla = min(ns.en_fazla, TAVAN)
    print(len(secim), "temsilci,", len(isler), "iş, tavan", en_fazla, flush=True)
    for a, m, p in secim:
        print(" ", a, m, p.stem, flush=True)
    if ns.kuru:
        return
    cikti = Path(ns.cikti)
    (cikti / "metin").mkdir(parents=True, exist_ok=True)
    tsv = cikti / "olcum.tsv"
    yapildi = set()
    if tsv.exists():
        yapildi = {tuple(s.split("\t")[i] for i in (0, 3, 4)) for s in tsv.read_text(encoding="utf-8").splitlines()[1:]}
    else:
        tsv.write_text(BASLIK, encoding="utf-8")
    proto = protokol_govde(ns.protokol)
    usd, sayi = 0.0, 0
    for aile, model, p, kol, r in isler:
        if (p.stem, kol, str(r)) in yapildi:
            continue
        if sayi >= en_fazla or usd >= ns.usd_tavan or oz_bellek_mb() > OZ_TAVAN_MB:
            print("tavan: çağrı", sayi, "usd", round(usd, 2), "MB", oz_bellek_mb(), flush=True)
            break
        alan, govde = on_bilgi(p)
        if kol == "proto":
            with tempfile.TemporaryDirectory() as d:
                g = Path(d) / p.name
                g.write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
                enjekte(g, proto)
                govde = on_bilgi(g)[1]
        o = kos_ajan(gorev[p.stem]["istem"], p.stem, alan, govde, model)
        sayi, usd = sayi + 1, usd + o["usd"]
        metin = o["metin"] + "\n" + "\n".join(o["girdi"])
        (cikti / "metin" / f"{p.stem}__{kol}__{r}.md").write_text(metin, encoding="utf-8")
        i, cc, cr, out = kosucu.jeton(o["usage"])
        with tsv.open("a", encoding="utf-8") as f:
            f.write("\t".join(map(str, [p.stem, aile, model, kol, r, i, cc, cr, out, round(o["usd"], 4), o["sure"],
                                        kosucu.puanla(metin, gorev[p.stem]["rubrik"]), o["tur"], o["rc"]])) + "\n")
        print(p.stem, kol, r, "out", out, "$", round(o["usd"], 4), flush=True)
    print("bitti: çağrı", sayi, "usd", round(usd, 2), flush=True)


if __name__ == "__main__":
    main()
