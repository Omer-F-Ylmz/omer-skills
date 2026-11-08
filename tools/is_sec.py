"""IHTIYAC-AC-1 (4): iş metni → gereken skill/ajan/MCP/plugin/CLI kümesi. Yerel (arac_ara kart BM25 + bölüm FTS5), 0 Claude jetonu.
  python tools/is_sec.py "<iş metni>" [--json]    küme (çekirdek hariç) ; --mcp yalnız MCP adları (ajan_sira mcp alanı / mcp_profil için)
  python tools/is_sec.py --olc [--n 60] [--yeni docs/katalog/altin-yeni.jsonl]   altın küme geri çağırma: kesin (tur:ad) + aile (aynı taban ad)
Çekirdek (her zaman açık, NİHAİ 44) iş kümesine yazılmaz; CEKIRDEK sabitinde."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arac_ara as aa  # noqa: E402
import arac_kart as ak  # noqa: E402

KOK = Path(__file__).resolve().parents[1]
CEKIRDEK = ["rea", "replica-skill", "design-extractor", "arac-ara", "ertele_katalog", "claude-mem", "obsidian", "mcp-filesystem", "mcp-git", "cc-kopru"]
# CLAUDE.md kuralı: UI'ya dokunan iş → frontend-craft önce, çatışmada sırası frontend-craft > impeccable > ui-ux-pro-max > taste
UI = re.compile(r"(?i)(ui|ux|site|sayfa|landing|frontend|arayüz|arayuz|tasar[ıi]m|css|react|web)")
UI_KUME = ["frontend-craft", "impeccable", "ui-ux-pro-max", "taste"]
# tur → (kart olarak dönen öncü sayısı, aday ad listesi uzunluğu)
KOTA = {"skill": (6, 45), "ajan": (3, 15), "mcp": (4, 12), "plugin": (3, 10), "cli": (3, 8), "arac": (2, 10)}
_KS = {}


def _ajanlar():
    """ajanlar/**/*.md (paketlenmiş proje ajanları, kart.jsonl'de yok) → kart benzeri kayıtlar; ad+description frontmatter'dan."""
    var, son = set(), []
    for f in sorted((KOK / "ajanlar").rglob("*.md")):
        ust = f.read_text(encoding="utf8", errors="ignore")[:3000]
        ad = re.search(r"^name:\s*(.+)$", ust, re.M)
        ne = re.search(r"^description:\s*(.+)$", ust, re.M)
        if ad and ad.group(1).strip() not in var:
            var.add(ad.group(1).strip())
            son.append({"ad": ad.group(1).strip(), "tur": "ajan", "ne": ne.group(1).strip() if ne else "", "yol": str(f)})
    return son


def _kartlar():
    if not _KS:
        for k in aa.kartlar(None):
            _KS.setdefault(k["tur"], []).append(k)
        var = {aa.ham(k["ad"]) for k in _KS.get("ajan", [])}
        _KS["ajan"] = _KS.get("ajan", []) + [a for a in _ajanlar() if a["ad"] not in var]
    return _KS


def sec(metin, kota=None):
    c, ks, kota = ak._cfg(None), _kartlar(), kota or KOTA
    cikti = {}
    for tur, (on, aday) in kota.items():
        gr = aa.adaylar(metin, ks.get(tur, []), aday, c["db"])
        ad = [aa.ham(g[0]["ad"]) for g in gr]
        # aynı işin başka ad-alanındaki kopyaları da aday sayılır (kesin geri çağırma için)
        kopya = [aa.ham(x["ad"]) for g in gr for x in g[1]]
        cikti[tur] = {"on": ad[:on], "aday": list(dict.fromkeys(ad[on:] + kopya))}
    # departman-* yöneticileri 13 kısa ad: her işte aday (CLAUDE.md: işe uyan yönetici skill'i önce açılır)
    dep = [aa.ham(k["ad"]) for k in ks.get("skill", []) if aa.ham(k["ad"]).startswith("departman-")]
    cikti["skill"]["aday"] = list(dict.fromkeys(dep + cikti["skill"]["aday"]))
    if UI.search(metin):
        cikti["skill"]["on"] = list(dict.fromkeys(UI_KUME + cikti["skill"]["on"]))
    # öncülerin geçmişte birlikte KABUL aldığı eşler (kart.birlikte) aynı kümeye
    var = {aa.ham(k["ad"]): k for t in ks.values() for k in t}
    for tur in cikti:
        for ad in cikti[tur]["on"][:2]:
            for b in (var.get(ad) or {}).get("birlikte") or []:
                hb = var.get(aa.ham(b))
                if hb and hb["tur"] in cikti and aa.ham(b) not in cikti[hb["tur"]]["on"]:
                    cikti[hb["tur"]]["aday"].append(aa.ham(b))
    return cikti


def sec_mcp(metin, n=4):
    """Yalnız MCP türü (hızlı): mcp_profil.sec'in regex türlerine eklenen kart eşleşmesi."""
    gr = aa.adaylar(metin, _kartlar().get("mcp", []), n, ak._cfg(None)["db"])
    return [aa.ham(g[0]["ad"]) for g in gr]


def bulunan(s):
    return {f"{t}:{a}" for t, v in s.items() for a in v["on"] + v["aday"]}


def olc(n_carpan=1.0, yeni=None, ayrinti=False):
    kota = {t: (o, max(o, int(a * n_carpan))) for t, (o, a) in KOTA.items()}  # carpan: aday ad listesi uzunluğu çarpanı
    dosyalar = [aa.Path(__import__("katalog_altin").ALTIN)] + ([Path(yeni)] if yeni and Path(yeni).exists() else [])
    sonuc, kacan = [], []
    for d in dosyalar:
        t = {"d": d.name, "kesin": 0, "aile": 0, "altin": 0, "is": 0, "tam_is": 0, "ad": 0}
        for s in d.read_text(encoding="utf8").splitlines():
            g = json.loads(s)
            b = bulunan(sec(g["is"], kota))
            aile = {x.split(":", 1)[0] + ":" + aa._ailesiz({"ad": x.split(":", 1)[1]}) for x in b}
            ks = [a for a in g["altin"] if a in b]
            af = [a for a in g["altin"] if a in b or a.split(":", 1)[0] + ":" + aa._ailesiz({"ad": a.split(":", 1)[1]}) in aile]
            t["kesin"] += len(ks)
            t["aile"] += len(af)
            t["altin"] += len(g["altin"])
            t["is"] += 1
            t["tam_is"] += int(len(af) == len(g["altin"]))
            t["ad"] += len(b)
            kacan += [(d.name, g["is"][:50], a) for a in g["altin"] if a not in af]
        t["kesin_geri"] = round(t["kesin"] / t["altin"], 3)
        t["aile_geri"] = round(t["aile"] / t["altin"], 3)
        t["ort_ad"] = t["ad"] // t["is"]
        sonuc.append(t)
    return (sonuc, kacan) if ayrinti else sonuc


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if "--olc" in a:
        carpan = float(a[a.index("--n") + 1]) if "--n" in a else 1.0
        yeni = a[a.index("--yeni") + 1] if "--yeni" in a else None
        r, kacan = olc(carpan, yeni, True)
        print(json.dumps(r, ensure_ascii=False, indent=1))
        for x in kacan:
            print("KACAN", " | ".join(x))
    elif a:
        s = sec(a[0])
        if "--mcp" in a:
            print(" ".join(s["mcp"]["on"] + s["mcp"]["aday"]))
        elif "--json" in a:
            print(json.dumps({"cekirdek": CEKIRDEK, **s}, ensure_ascii=False, indent=1))
        else:
            for t, v in s.items():
                print(f"{t}: {' · '.join(v['on'])}  (+{len(v['aday'])} aday)")
    else:
        print(__doc__)
