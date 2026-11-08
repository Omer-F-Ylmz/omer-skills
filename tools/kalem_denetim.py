"""KALEM-DENETIM (5 Kas): butun videolardan cikan HER kalemi birincil kaynaktan dogrular.
Her (video, kalem) icin: cozum turu (gh/npm/pypi/cc/diger) -> fiziksel kurulum kaniti + eslesme dogrulugu.
gh: son toplu kaydi -> yol var mi + yol gercekten o repo mu (.git/config remote ya da owner__repo klasoru)
    + eslesme: kalem adi repo adinda/README'de geciyor mu ya da rapor kaniti var mi.
npm: npm-kalem ya da global node_modules'te paket klasoru. pypi: venv-kalem site-packages dist-info. cc: yerlesik.
Cikti: .kos/kopru/kalem-denetim.tsv (kalem basina satir) + kalem-denetim-ozet.json
"""
import json, os, re, sys, glob, time
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, "tools"))
import kurulum_tamamla as T  # noqa: E402
import kurulum_coz2 as K  # noqa: E402

CIK = os.path.join(KOK, ".kos", "kopru", "kalem-denetim.tsv")
OZ = os.path.join(KOK, ".kos", "kopru", "kalem-denetim-ozet.json")
NPM = [r"C:\Projeler\_araclar\npm-kalem\node_modules", os.path.expandvars(r"%APPDATA%\npm\node_modules")]
PYP = r"C:\Projeler\_araclar\venv-kalem\Lib\site-packages"


def nrm(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower().replace("+", "plus"))


son_kayit = {}
for l in open(K.TOPLU, encoding="utf-8", errors="replace"):
    try:
        o = json.loads(l)
    except Exception:
        continue
    son_kayit[o.get("repo_istenen")] = o

kanit = {}
for l in open(K.COZ, encoding="utf-8", errors="replace"):
    try:
        o = json.loads(l)
    except Exception:
        continue
    for kl, kn in (o.get("kanit") or {}).items():
        kanit[(o.get("video"), kl)] = kn

readme_cache, remote_cache = {}, {}


def readme(y):
    if y not in readme_cache:
        s = ""
        for f in glob.glob(os.path.join(y, "README*"))[:2] + glob.glob(os.path.join(y, "SKILL.md"))[:1]:
            try:
                s += open(f, encoding="utf-8", errors="replace").read(200000)
            except Exception:
                pass
        readme_cache[y] = nrm(s)
    return readme_cache[y]


def remote(y):
    if y not in remote_cache:
        r = ""
        try:
            r = open(os.path.join(y, ".git", "config"), encoding="utf-8", errors="replace").read().lower()
        except Exception:
            pass
        remote_cache[y] = r
    return remote_cache[y]


def gh_denetle(video, kalem, hdf):
    o = son_kayit.get(hdf) or son_kayit.get("gh:" + hdf)
    if not o:
        return "KAYIT-YOK", "", "-"
    d = o.get("durum")
    if d in ("REPO-YOK", "BULUNAMADI", "DOGRULANAMADI", "BUYUK-SOR", "DISK-BEKLE", "INDIRME-HATA", "ATLANDI"):
        return d, o.get("repo") or "", "-"
    rp = o.get("repo") or hdf
    y = o.get("yol") or ""
    if not y or not os.path.isdir(y):
        return "YOL-YOK", rp, "-"
    owner, _, repo = rp.partition("/")
    gercek = os.path.basename(y.rstrip("\\/")).lower() == f"{owner}__{repo}".lower() or f"{owner}/{repo}".lower() in remote(y).replace(".git", "")
    if not gercek:
        return "AD-CAKISMASI", rp, "-"
    nk, nr = nrm(kalem), nrm(repo)
    if kanit.get((video, kalem)) == "raporda":
        es = "rapor-kaniti"
    elif len(nk) >= 3 and (nk in nr or (len(nr) >= 4 and nr in nk)):
        es = "ad"
    elif len(nk) >= 4 and nk in readme(y):
        es = "readme"
    elif kanit.get((video, kalem)) == "sonnet-bilgisi":
        es = "sonnet"
    else:
        es = "ESLESME-SUPHELI"
    return ("KURULU-SUPHELI" if es == "ESLESME-SUPHELI" else "KURULU-DOGRULANDI"), rp, es


def npm_var(p):
    if not re.fullmatch(r"(@[\w-][\w.-]*/)?[\w][\w.-]*", p or ""):
        return False
    return any(os.path.isfile(os.path.join(b, *p.split("/"), "package.json")) for b in NPM)


def pyp_var(p):
    n = nrm(p)
    try:
        return any(nrm(re.sub(r"-[\d.]+.*", "", f[:-len(".dist-info")])) == n for f in os.listdir(PYP) if f.endswith(".dist-info"))
    except Exception:
        return False


son = T.en_iyi()
satir, durum, video_say = [], Counter(), 0
for v, es in son.items():
    video_say += 1
    for kalem, d in es.items():
        if isinstance(d, dict):
            d = d.get("deger") or next((x for x in d.values() if isinstance(x, str)), "")
        s = str(d)
        if re.match(r"^(gh/|github\.com/)", s):
            s = "gh:" + re.sub(r"^(gh/|github\.com/)", "", s)
        t = s.split(":")[0] if ":" in s else "diger"
        if "cevabı yok" in s:
            t = "cevapsiz"
        hdf = s[len(t) + 1:].strip().strip("/") if ":" in s else s
        if t == "gh":
            st, rp, esl = gh_denetle(v, kalem, hdf)
        elif t == "npm":
            st, rp, esl = ("KURULU-DOGRULANDI" if npm_var(hdf) else "NPM-YOK"), hdf, "-"
        elif t == "pypi":
            st, rp, esl = ("KURULU-DOGRULANDI" if pyp_var(hdf) else "PYPI-YOK"), hdf, "-"
        elif t == "cc":
            st, rp, esl = "CC-YERLESIK", hdf, "-"
        else:
            st, rp, esl = "KURULAMAZ-" + t, hdf[:80], "-"
        durum[(t, st, esl)] += 1
        satir.append("\t".join([v, kalem.replace("\t", " "), t, hdf.replace("\t", " ")[:120], st, rp, esl]))
open(CIK, "w", encoding="utf-8").write("video\tkalem\ttur\thedef\tdurum\trepo\teslesme\n" + "\n".join(satir) + "\n")
oz = {"zaman": time.strftime("%Y-%m-%d %H:%M"), "video": video_say, "kalem": len(satir),
      "durum": {f"{a}|{b}|{c}": n for (a, b, c), n in durum.most_common()}}
json.dump(oz, open(OZ, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(oz, ensure_ascii=False, indent=1))
