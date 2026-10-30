"""SKILL-PAKET-2 FARK: CC skill'leri ↔ claude.ai kayıtları (~/.claude/skills/synced/<id>/, yalnız okunur).
Çıktı (cikti_dizini): a-eksik.tsv (claude.ai'de hiç yok) · b-kopya.tsv (claude.ai'de hem tekil hem paket içinde / iki pakette)
· c-eski.tsv (claude.ai kopyasının içeriği CC'dekinden farklı) · cc.json (tüm CC skill'leri + eşleşme).
İçerik karşılaştırması: satır kümesi (frontmatter, paket notları ve paketlemenin yol yeniden yazımları atılır); CC'de olup claude.ai'de
olmayan satır ≥ ESIK olan dosya ya da claude.ai'de olmayan yeni .md → eski (REFERANS.md'ye birleşmiş paketlerde eksik dosya sayılmaz).
Kullanım: python fark.py <cikti_dizini> [--home <.claude'un üstü>]"""
import csv, json, re, sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from envanter import _fm, _kaynaklar
from paketle import metin_mi

REPO = pathlib.Path(__file__).resolve().parents[2]


def anahtar(ad):
    a = ad.lower().strip()
    for on in ("gstack-", "cc-"):
        if a.startswith(on):
            a = a[len(on):]
    return a.replace("claude-", "").replace("claude", "cc").removesuffix("-claudeai").removesuffix("-desktop")


ESIK = 3
DIKKAT = (".md", ".py", ".js", ".mjs", ".ts", ".sh", ".ps1", ".tsv", ".json")
YOL = re.compile(r"(\.\./|_ref/|skills/[\w.-]+/|TALIMAT\.md|SKILL\.md|~/\.claude/[\w./-]+)")


def _satirlar(b):
    """Frontmatter'sız, paketleme yol yeniden yazımları ve paket notları silinmiş satır kümesi."""
    t = b.decode("utf-8", "replace").replace("\r\n", "\n").lstrip("\ufeff")
    m = re.match(r"---\n.*?\n---\n", t, re.S)
    t = t[m.end():] if m else t
    return {x for x in (YOL.sub("", l).strip() for l in t.split("\n")) if x and not x.startswith(("> Paket notu", "> Not"))}


def izler(d, ana):
    """{göreli yol: satır kümesi}; ana dosya '@' anahtarıyla; yalnız talimat/betik/veri metinleri."""
    out = {}
    for f in d.rglob("*"):
        r = f.relative_to(d).as_posix()
        if not f.is_file() or {"node_modules", ".git", "__pycache__", "agents"} & set(r.split("/")[:-1]) or r.startswith("."):
            continue
        if r != ana and not r.endswith(DIKKAT):
            continue
        v = f.read_bytes()
        if metin_mi(v):
            out["@" if r == ana else r] = _satirlar(v)
    return out


def claudeai(sync):
    """→ {anahtar: [kayıt]}; kayıt = {kayit, tur: tekil|paket, ad, dizin, ana}."""
    ai = {}
    for d in sorted(p for p in sync.iterdir() if p.is_dir()):
        if (d / "skills").is_dir() and any((d / "skills").glob("*/TALIMAT.md")):
            for t in sorted((d / "skills").glob("*/TALIMAT.md")):
                ad = _fm(t.read_text(encoding="utf-8", errors="replace"))[0] or t.parent.name
                ai.setdefault(anahtar(ad), []).append({"kayit": d.name, "tur": "paket", "ad": ad, "dizin": t.parent, "ana": "TALIMAT.md"})
        elif (d / "SKILL.md").is_file():
            ad = _fm((d / "SKILL.md").read_text(encoding="utf-8", errors="replace"))[0] or d.name
            ai.setdefault(anahtar(ad), []).append({"kayit": d.name, "tur": "tekil", "ad": ad, "dizin": d, "ana": "SKILL.md"})
    return ai


def kendi_adlar():
    return {anahtar(f.parent.name) for f in [*REPO.glob("skills/*/SKILL.md"), *REPO.glob("plugins/*/skills/*/SKILL.md")]}


def cc_skilleri(h):
    """Kendi skill'lerimizde gerçek = repo (CC'de yalnız senkron kopyası olanlar da: jev vb.); sonra eklenti + ~/.claude/skills."""
    gorulen, out = set(), []
    for kaynak, kok in [("repo", REPO / "skills"), *[(f"repo:{p.parent.name}", p) for p in REPO.glob("plugins/*/skills")], *_kaynaklar(h)]:
        for f in sorted(kok.rglob("SKILL.md")):
            p = f.relative_to(kok).as_posix()
            if "synced/" in p or "/node_modules/" in p or ".trash" in p or p.count("/") > 4:
                continue
            ad, ac = _fm(f.read_text(encoding="utf-8", errors="replace"))
            ad = ad or f.parent.name
            if ad.lower() in gorulen:
                continue
            gorulen.add(ad.lower())
            out.append({"kaynak": kaynak, "kok": str(kok), "ad": ad, "yol": str(f.parent), "aciklama": ac})
    return out


def calistir(cikti, home=None):
    h = pathlib.Path(home or pathlib.Path.home()) / ".claude"
    sync = next(p for p in (h / "skills/synced").iterdir() if p.is_dir())
    ai, kendi = claudeai(sync), kendi_adlar()
    cc = cc_skilleri(h)
    a, c = [], []
    for s in cc:
        k = anahtar(s["ad"])
        s["kendi"] = k in kendi
        kar = ai.get(k, [])
        s["claudeai"] = [f"{x['tur']}:{x['kayit']}" for x in kar]
        if not kar:
            a.append(s); continue
        cci = izler(pathlib.Path(s["yol"]), "SKILL.md")
        farkli = []
        for x in kar:
            aii = izler(x["dizin"], x["ana"])
            ortak = [y for y in cci if y in aii]
            eksik = [y for y in cci if y not in aii and y != "@"] if "REFERANS.md" not in aii else []
            fy = [y for y in ortak if len(cci[y] - aii[y]) >= ESIK] + [f"+{y}" for y in eksik if y.endswith(".md")]
            if fy:
                farkli.append((x, fy))
        if farkli and len(farkli) == len(kar):
            c.append({**s, "eski": "; ".join(f"{x['tur']}:{x['kayit']}" for x, _ in farkli),
                      "dosyalar": ",".join(farkli[0][1][:6]) + (" …" if len(farkli[0][1]) > 6 else "")})
    b = [{"ad": v[0]["ad"], "kayitlar": "; ".join(f"{x['tur']}:{x['kayit']}" for x in v)}
         for v in ai.values() if len(v) > 1 and any(x["tur"] == "tekil" for x in v)]
    cikti = pathlib.Path(cikti); cikti.mkdir(parents=True, exist_ok=True)

    def tsv(ad, satirlar, sutun):
        with open(cikti / ad, "w", encoding="utf-8", newline="") as o:
            w = csv.writer(o, delimiter="\t", lineterminator="\n")
            w.writerow(sutun)
            for r in satirlar:
                w.writerow([str(r.get(x, "")).replace("\n", " ") for x in sutun])
    tsv("a-eksik.tsv", a, ["kendi", "kaynak", "ad", "yol", "aciklama"])
    tsv("b-kopya.tsv", b, ["ad", "kayitlar"])
    tsv("c-eski.tsv", c, ["kendi", "kaynak", "ad", "eski", "dosyalar", "yol"])
    (cikti / "cc.json").write_text(json.dumps(cc, ensure_ascii=False, indent=0), encoding="utf-8")
    kayit = sum(1 for p in sync.iterdir() if p.is_dir())
    return {"cc": len(cc), "claudeai_kayit": kayit, "a": len(a), "a_kendi": sum(s["kendi"] for s in a),
            "b": len(b), "c": len(c), "c_kendi": sum(s["kendi"] for s in c)}


if __name__ == "__main__":
    argv = sys.argv[1:]
    if not argv:
        print(__doc__); sys.exit(2)
    print(calistir(argv[0], argv[argv.index("--home") + 1] if "--home" in argv else None))
