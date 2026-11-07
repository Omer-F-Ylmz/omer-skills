"""LISTE-GUNCEL-2: ana-liste.tsv durum sütununu bugünkü kurulum kaynaklarıyla günceller (yalnız kurulmadı/kanıtsız -> kurulu yönünde).
Kaynaklar: kurulum-*-sonuc.tsv (KURULDU*/ZATEN), ~/.claude/skills + agents, npm -g, uv tool, pip --user, Desktop\\Claude ile yapılanlar\\araclar klonları.
Eşleşme: normalize ad eşitliği (kalem ya da repo adı); genel adlar elenir. Kullanım: python -I tools/liste_durum_guncel.py [--yaz]"""
import collections, csv, json, re, shutil, subprocess, sys, time
from pathlib import Path

K = Path(r"C:\Projeler\omer-skills")
L = K / "docs/video-tarama/ana-liste.tsv"
HOME = Path.home()
ARAC = HOME / "Desktop/Claude ile yapılanlar/araclar"
csv.field_size_limit(10**9)
GENEL = {"core", "cli", "app", "sdk", "server", "main", "docs", "skills", "plugin", "plugins", "web", "api", "mcp", "tools", "agent", "agents", "code", "test", "demo"}
SONUC = ["docs/video-tarama/kurulum-d2-sonuc.tsv", "rapor/kurulum-omer-sonuc.tsv", "rapor/kurulum-omer2-sonuc.tsv", "rapor/kurulum-gurultu-sonuc.tsv",
         "rapor/kurulum-guvenlik-sonuc.tsv", "rapor/kurulum-ek-1107-sonuc.tsv", "rapor/kurulum-duzelt-1107-sonuc.tsv"]
KANIT = ["docs/video-tarama/kurulu-kanit.tsv", "docs/video-tarama/kurulu-kanit-yeni.tsv", "docs/video-tarama/kurulu-kanit2.tsv"]  # sonuc=KANIT: gercek komut/SKILL.md kaniti
KANIT_IDX = {}
KURULU_D = {"KURULDU", "ZATEN", "KURULDU-SARMALAYICI", "KURULDU-KAYNAK", "KURULDU-KUTUPHANE", "KURULDU-DOGRULANMADI"}
KURMADI = {"KURULMADI-SIRADA", "BULUNAMADI-KESIN", "BULUNDU-ADAY", "BULUNAMADI-ARANIYOR", "KAYITSIZ", "KURULMADI-HESAP"}
SIRA = ["KURULDU", "ZATEN", "KURULDU-SARMALAYICI", "KURULDU-KAYNAK", "KURULDU-KUTUPHANE", "KURULDU-DOGRULANMADI"]


def n(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


def anahtar(ad):
    ad = str(ad).strip()
    ks = {n(ad)}
    if "/" in ad:
        ks.add(n(ad.rstrip("/").split("/")[-1]))
    for o, r in re.findall(r"github\.com/([\w.-]+)/([\w.-]+)", ad):  # tam repo bağlantısı: .../tree/... kuyruğu atılır
        ks.add(n(r.removesuffix(".git")))
    if "__" in ad:  # klon dizini owner__repo
        ks.add(n(ad.split("__", 1)[1]))
    return {k for k in ks if len(k) >= 3 and k not in GENEL}


def ocr(s):
    return n(s).replace("0", "o").replace("rn", "m").replace("1", "l")


GENEL_SON = re.compile(r"(agenttoolkit|toolkit|mcpserver|server|mcp|cli|skills?|plugin|sdk|js|py)$")


def kok(s):
    while (x := GENEL_SON.sub("", s, count=1)) != s and len(x) >= 4:
        s = x
    return s


def adaylar(kalem, link):
    ana = n(link.split("|")[0].rstrip("/").split("/")[-1]) if "github.com" in link else n(kalem)
    a = n(kalem)
    return [x for x in dict.fromkeys(ocr(y) for y in (a, ana, kok(a), kok(ana))) if len(x) >= 3 and x not in GENEL]


def sh(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=120, shell=True, encoding="utf-8", errors="replace").stdout
    except Exception:
        return ""


KAYNAK = collections.OrderedDict()  # kaynak adı -> öğe sayısı
SONUC_IDX = {}  # anahtar -> (durum, kaynak)
FS_IDX = {}  # anahtar -> (kaynak, ad)


def sonuc_oku():
    for p in SONUC:
        q = K / p
        if not q.exists():
            KAYNAK[p] = "yok"
            continue
        say = 0
        for r in csv.DictReader(open(q, encoding="utf-8-sig", errors="replace", newline=""), delimiter="\t"):
            d = (r.get("durum") or "").strip()
            if d in KURULU_D:
                say += 1
                for k in anahtar(r.get("kalem", "")):
                    o = SONUC_IDX.get(k)
                    if o is None or SIRA.index(d) < SIRA.index(o[0]):
                        SONUC_IDX[k] = (d, p)
        KAYNAK[p] = say


def kanit_oku():
    for p in KANIT:
        q = K / p
        say = 0
        for r in csv.DictReader(open(q, encoding="utf-8-sig", errors="replace", newline=""), delimiter="	"):
            if (r.get("sonuc") or "").strip() == "KANIT":
                say += 1
                for k in anahtar(r.get("kalem", "")):
                    KANIT_IDX.setdefault(k, (p, r.get("ayrinti", "")[:80]))
        KAYNAK[p] = say


def fs_ekle(src, ad):
    for k in anahtar(ad):
        FS_IDX.setdefault(k, (src, ad))


def fs_oku():
    ds = [d.name for d in (HOME / ".claude/skills").iterdir()]
    for d in ds:
        fs_ekle("~/.claude/skills", d)
    KAYNAK["~/.claude/skills (klasör)"] = len(ds)
    ag = [p.stem for p in (HOME / ".claude/agents").glob("*.md")]
    for a in ag:
        fs_ekle("~/.claude/agents", a)
    KAYNAK["~/.claude/agents (*.md)"] = len(ag)
    try:
        js = json.loads(sh("npm ls -g --depth=0 --json") or "{}").get("dependencies", {})
    except Exception:
        js = {}
    for a in js:
        fs_ekle("npm -g", a)
    KAYNAK["npm -g"] = len(js)
    uv = [l.split()[0] for l in sh("uv tool list").splitlines() if l and not l.startswith(("-", " "))]
    for a in uv:
        fs_ekle("uv tool", a)
    KAYNAK["uv tool list"] = len(uv)
    try:
        pp = json.loads(sh("python -m pip list --user --format=json") or "[]")
    except Exception:
        pp = []
    for a in pp:
        fs_ekle("pip --user", a["name"])
    KAYNAK["pip --user"] = len(pp)
    sat = 0
    if ARAC.exists():
        for d1 in ARAC.iterdir():
            if d1.is_dir():
                fs_ekle("araclar-klon", d1.name)
                sat += 1
                for d2 in d1.iterdir():
                    if d2.is_dir():
                        fs_ekle("araclar-klon", d2.name)
                        sat += 1
    KAYNAK["Desktop\\...\\araclar klonları (1+2 seviye)"] = sat


STRICT = set()


def siki_oku():
    """Gerçek kurulu kanıtı veren kaynaklar (envanter.tsv'de arastirilan/nerede=yok ve KURULACAK satırları SAYILMAZ)."""
    for k in list(FS_IDX) + list(SONUC_IDX) + list(KANIT_IDX):
        STRICT.add(ocr(k))
    for d in (HOME / ".claude/plugins/cache").iterdir():
        STRICT.add(ocr(d.name))
    O = K / ".kos/kopru/ogren/video-izle-kur-1"
    for a in json.loads((O / "kurulu-tara.json").read_text(encoding="utf-8")):
        STRICT.add(ocr(a))
    rs = list(csv.DictReader(open(K / "docs/envanter/envanter.tsv", encoding="utf-8", newline=""), delimiter="	"))
    ok = [r for r in rs if r["tur"] != "arastirilan" and r["nerede"] != "yok"]
    for r in ok:
        STRICT.add(ocr(r["ad"]))
    KAYNAK["envanter.tsv sıkı (arastirilan/yok hariç)"] = f"{len(ok)}/{len(rs)}"
    for r in csv.reader(open(O / "tablo13.tsv", encoding="utf-8", newline=""), delimiter="	"):
        if len(r) > 3 and re.search(r"calisiyor|kuruldu|KURULU|zaten kurulu", r[3]):
            STRICT.add(ocr(r[0]))
    for r in csv.reader(open(O / "envanter.tsv", encoding="utf-8", newline=""), delimiter="	"):
        if len(r) > 6 and re.search(r"KURULU|KLONLU|calisiyor|kuruldu", r[6]):
            STRICT.add(ocr(r[0]))
    KAYNAK["sıkı kurulu anahtar sayısı"] = len(STRICT)


def varyant(kalem):
    """Ad süsleri atılmış ek anahtar: sürüm (v2.0.76, 3.1), baştaki 'AI', sondaki cloud/app/skill(s)."""
    tk = [x for x in re.split(r"[\s_]+", str(kalem).strip()) if x and not re.fullmatch(r"v?\d+(\.\d+)*", x, re.I)]
    if len(tk) > 1 and tk[0].lower() == "ai":
        tk = tk[1:]
    while len(tk) > 1 and tk[-1].lower() in ("cloud", "app", "skill", "skills"):
        tk = tk[:-1]
    k = n("".join(tk))
    return {k} if len(k) >= 4 and k not in GENEL and k != n(kalem) else set()


def say(rows):
    t = collections.Counter((r["tur"], r["durum"]) for r in rows)
    return t


def main():
    yaz = "--yaz" in sys.argv
    sonuc_oku()
    fs_oku()
    kanit_oku()
    siki_oku()
    rows = list(csv.DictReader(open(L, encoding="utf-8", newline=""), delimiter="\t"))
    once = say(rows)
    degisen = []
    for r in rows:
        if r["durum"] not in KURMADI:
            continue
        ks = anahtar(r["kalem"]) | anahtar(r["repo_link"].split("|")[0].replace("https://github.com/", "")) | varyant(r["kalem"])
        s = next((SONUC_IDX[k] for k in sorted(ks) if k in SONUC_IDX), None)
        f = next((FS_IDX[k] for k in sorted(ks) if k in FS_IDX), None)
        if s:
            yeni, kan = s[0], f"kurulum sonucu {s[0]}: {s[1]}"
        elif f:
            yeni, kan = "KURULU-KANITSIZ", f"kurulu: {f[0]}:{f[1]}"
        else:
            continue
        degisen.append((r["kalem"], r["durum"], yeni))
        r["durum"], r["neden_kanit"] = yeni, kan
        r["bizde_nerede"] = "; ".join(x for x in (r["bizde_nerede"], (s[1] if s else f[0] + ":" + f[1])) if x)
    for r in rows:  # kök neden düzeltmesi: eski üretici envanter.tsv'deki arastirilan/yok/KURULACAK kayıtlarını 'kurulu' saymıştı
        if r["durum"] == "KURULU-KANITSIZ" and r["neden_kanit"].startswith("envanter/skills/plugins"):
            if not any(x in STRICT for x in adaylar(r["kalem"], r["repo_link"])):
                degisen.append((r["kalem"], "KURULU-KANITSIZ", "KURULMADI-SIRADA"))
                r["durum"], r["neden_kanit"] = "KURULMADI-SIRADA", "yalnız arastirilan/nerede=yok/KURULACAK kaydı var; kurulu kanıt yok"
    for r in rows:  # kanıtlı kurulu: KURULU-KANITSIZ -> CALISIYOR (gerçek çağrı/SKILL.md kanıtı)
        if r["durum"] == "KURULU-KANITSIZ":
            ks = anahtar(r["kalem"]) | anahtar(r["repo_link"].split("|")[0].replace("https://github.com/", ""))
            kn = next((KANIT_IDX[k] for k in sorted(ks) if k in KANIT_IDX), None)
            if kn:
                degisen.append((r["kalem"], "KURULU-KANITSIZ", "CALISIYOR"))
                r["durum"], r["neden_kanit"] = "CALISIYOR", f"kanıt {kn[0]}: {kn[1]}"
                r["bizde_nerede"] = "; ".join(x for x in (r["bizde_nerede"], kn[0]) if x)
    sonra = say(rows)
    print("degisen", len(degisen), collections.Counter((a, b) for _, a, b in degisen).most_common(12))
    print("KAYNAK", dict(KAYNAK))
    if yaz:
        with open(L, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
    Path(K / "tmp/liste_guncel2_say.json").write_text(json.dumps({"once": {f"{a}|{b}": c for (a, b), c in once.items()}, "sonra": {f"{a}|{b}": c for (a, b), c in sonra.items()},
                                                                  "degisen": degisen, "kaynak": dict(KAYNAK)}, ensure_ascii=False), encoding="utf-8")


main()
