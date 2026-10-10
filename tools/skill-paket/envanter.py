"""CC'de kurulu olup claude.ai'de olmayan skill'leri bulur ve metin zip'ini üretir (eski envanter_fark + eksik_topla + eksik_metin).
Girdi: claude.ai ad listesi JSON'u ({"giris": [...], "paket_uyesi": [...]}).
Çıktı (cikti_dizini): envanter-fark.tsv (eksikler) · eksik-metin.zip (<no>__<ad>/ metin dosyaları + _liste.json + _ikili.tsv).
Ad eşleştirme: ad · gstack-<ad> · claude→cc · claude- silinmiş · cc-<ad>.
Kullanım: python envanter.py <claudeai_adlar.json> <cikti_dizini> [--home <.claude'un üstü>]"""
import csv, json, re, sys, zipfile, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from paketle import metin_mi


def ai_adlar(yol):
    j = json.loads(pathlib.Path(yol).read_text(encoding="utf-8"))
    return {a.lower() for a in j["giris"]} | {a.lower() for a in j["paket_uyesi"]}


def var(ad, ai):
    a = ad.lower()
    return any(x in ai for x in (a, "gstack-" + a, a.replace("claude", "cc"), a.replace("claude-", ""), "cc-" + a))


def _fm(md):
    m = re.match(r"^﻿?---\s*\r?\n(.*?)\r?\n---", md, re.S)
    if not m:
        return None, ""
    ad = re.search(r"^name:\s*['\"]?([^'\"\r\n]+)", m.group(1), re.M)
    ac = re.search(r"^description:\s*['\"]?(.*)", m.group(1), re.M)
    return (ad.group(1).strip() if ad else None), (ac.group(1).strip().strip("'\"")[:110] if ac else "")


def _kaynaklar(h):
    out = []
    ip = h / "plugins/installed_plugins.json"
    data = json.loads(ip.read_text(encoding="utf-8")) if ip.exists() else {}
    for anahtar, girdi in data.get("plugins", data).items():
        for g in (girdi if isinstance(girdi, list) else [girdi]):
            yol = g.get("installPath") if isinstance(g, dict) else None
            if yol and pathlib.Path(yol).exists():
                out.append((anahtar, pathlib.Path(yol)))
    if (h / "skills").exists():
        out.append(("~/.claude/skills", h / "skills"))
    return out


def calistir(ai_json, cikti, home=None):
    """→ eksik skill listesi [{on, kaynak, ad, yol, aciklama}]; dosyaları cikti'ya yazar."""
    ai = ai_adlar(ai_json)
    h = pathlib.Path(home or pathlib.Path.home()) / ".claude"
    gorulen, eksik = set(), []
    for kaynak, kok in _kaynaklar(h):
        for f in sorted(kok.rglob("SKILL.md")):
            p = f.relative_to(kok).as_posix()
            if "synced/" in p or "/node_modules/" in p or ".trash" in p or p.count("/") > 4:
                continue
            ad, ac = _fm(f.read_text(encoding="utf-8", errors="replace"))
            ad = ad or f.parent.name
            if ad.lower() in gorulen:
                continue
            gorulen.add(ad.lower())
            if not var(ad, ai):
                eksik.append({"on": f"{len(eksik):03d}__{re.sub(r'[^A-Za-z0-9._-]+', '-', ad)}", "kaynak": kaynak, "ad": ad,
                              "yol": str(f.parent), "aciklama": ac})
    cikti = pathlib.Path(cikti); cikti.mkdir(parents=True, exist_ok=True)
    with open(cikti / "envanter-fark.tsv", "w", encoding="utf-8", newline="") as o:
        w = csv.writer(o, delimiter="\t", lineterminator="\n")
        w.writerow(["kaynak", "ad", "durum", "dosya", "yol", "aciklama"])
        for e in eksik:
            w.writerow([e["kaynak"], e["ad"], "EKSIK", sum(1 for x in pathlib.Path(e["yol"]).rglob("*") if x.is_file()), e["yol"], e["aciklama"]])
    ikili = []
    with zipfile.ZipFile(cikti / "eksik-metin.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for e in eksik:
            d = pathlib.Path(e["yol"])
            for f in sorted(d.rglob("*")):
                if f.is_file() and not {"node_modules", ".git"} & set(f.relative_to(d).parts):
                    v = f.read_bytes()
                    y = f"{e['on']}/{f.relative_to(d).as_posix()}"
                    if metin_mi(v):
                        z.writestr(y, v)
                    else:
                        ikili.append(f"{y}\t{len(v)}")
        z.writestr("_liste.json", json.dumps(eksik, ensure_ascii=False, indent=0))
        z.writestr("_ikili.tsv", "yol\tbayt\n" + "\n".join(ikili))
    return eksik


def main(argv):
    if len(argv) < 2:
        print(__doc__); return 2
    home = argv[argv.index("--home") + 1] if "--home" in argv else None
    eksik = calistir(argv[0], argv[1], home)
    print(f"eksik {len(eksik)} · {pathlib.Path(argv[1]) / 'envanter-fark.tsv'} · {pathlib.Path(argv[1]) / 'eksik-metin.zip'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
