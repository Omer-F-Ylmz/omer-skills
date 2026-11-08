"""LISTE-CIKAR-1 kapı (2): ana listedeki her github repo'su gh api ile var mı. 404 -> gh search + bulanık eşleşme (OCR: 0<->o, rn<->m, Levenshtein<=3).
Kullanım: python -I tools/repo_dogrula.py   (önbellek: .kos/kopru/ogren/liste-cikar-1/repo-dogrula.json; kaldığı yerden)"""
import json, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

K = Path(r"C:\Projeler\omer-skills")
C = K / ".kos/kopru/ogren/liste-cikar-1"
OUT = C / "repo-dogrula.json"
GH = re.compile(r"github\.com/([\w.-]+/[\w.-]+)")
NW = 0x08000000


def gh(*a):
    p = subprocess.run(["gh", *a], capture_output=True, text=True, encoding="utf-8", errors="replace", creationflags=NW, timeout=60, env=dict(os.environ))
    return p.returncode, p.stdout, p.stderr


def ocr(s):
    return s.lower().replace("0", "o").replace("rn", "m").replace("1", "l").replace("-", "").replace("_", "").replace(".", "")


def lev(a, b):
    p = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        c = [i]
        for j, y in enumerate(b, 1):
            c.append(min(p[j] + 1, c[j - 1] + 1, p[j - 1] + (x != y)))
        p = c
    return p[-1]


def repolar():
    s = set()
    for l in (C / "det.jsonl").read_text(encoding="utf-8").splitlines():
        s |= set(json.loads(l)["repos"])
    if (C / "llm.jsonl").exists():
        for l in (C / "llm.jsonl").read_text(encoding="utf-8").splitlines():
            for k in json.loads(l)["kalemler"]:
                m = GH.search(k.get("link") or "")
                if m:
                    s.add(m.group(1).removesuffix(".git"))
    return sorted(s)


def kontrol(r):
    rc, o, e = gh("api", f"repos/{r}", "--jq", ".full_name")
    if rc == 0 and o.strip():
        return r, {"durum": 200, "tam": o.strip()}
    if "404" in e or "Not Found" in e:
        ad = r.split("/")[1]
        rc2, o2, _ = gh("search", "repos", re.sub(r"[-_.]", " ", ad), "--limit", "5", "--json", "fullName")
        best = None
        try:
            for x in json.loads(o2 or "[]"):
                n = x["fullName"]
                d = lev(ocr(n.split("/")[1]), ocr(ad))
                if d <= 3 and (best is None or d < best[0]):
                    best = (d, n)
        except Exception:
            pass
        return r, {"durum": 404, "yakin": best[1] if best else "", "uzak": best[0] if best else None}
    return r, {"durum": "hata", "e": e[:80]}


if __name__ == "__main__" and "coz" in sys.argv:
    coz(); sys.exit()
if __name__ == "__main__":
    onb = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    bekle = [r for r in repolar() if onb.get(r, {}).get("durum") in (None, "hata")]
    print("repo", len(bekle), "bekliyor", flush=True)
    with ThreadPoolExecutor(8) as ex:
        for i, (r, v) in enumerate(ex.map(kontrol, bekle), 1):
            onb[r] = v
            if i % 100 == 0:
                OUT.write_text(json.dumps(onb, ensure_ascii=False), encoding="utf-8"); print(i, flush=True)
    OUT.write_text(json.dumps(onb, ensure_ascii=False), encoding="utf-8")
    import collections
    print(collections.Counter(str(v["durum"]) for v in onb.values()), "yakin bulunan", sum(1 for v in onb.values() if v.get("yakin")))


def coz():
    """404'leri: (1) 200'lü repolara tam ad bulanık eşleşmesi, (2) sahibi gh'de varsa (fuzzy sahip) sahibin repo listesinde bulanık ad."""
    onb = json.loads(OUT.read_text(encoding="utf-8"))
    iyi = [k for k, v in onb.items() if v.get("durum") == 200]
    iyio = {k: ocr(k) for k in iyi}
    sahipler = {}
    cozulen = 0
    for k, v in onb.items():
        if v.get("durum") != 404 or v.get("yakin"):
            continue
        o = ocr(k)
        lim = max(3, len(o) // 7)
        b = min(((lev(o, io), i) for i, io in iyio.items()), default=(99, ""))
        if b[0] <= lim:
            v["yakin"], v["uzak"] = onb[b[1]]["tam"], b[0]; cozulen += 1; continue
        sah, ad = k.split("/")[0], k.split("/")[-1]
        for s in {sah} | {i.split("/")[0] for i in iyi if lev(ocr(i.split("/")[0]), ocr(sah)) <= 2}:
            if s not in sahipler:
                rc, o2, _ = gh("api", f"users/{s}/repos?per_page=100", "--jq", ".[].full_name")
                sahipler[s] = o2.split() if rc == 0 else []
            m = min(((lev(ocr(n.split("/")[1]), ocr(ad)), n) for n in sahipler[s]), default=(99, ""))
            if m[0] <= max(3, len(ad) // 5):
                v["yakin"], v["uzak"] = m[1], m[0]; cozulen += 1; break
    OUT.write_text(json.dumps(onb, ensure_ascii=False), encoding="utf-8")
    print("coz: yakin bulunan toplam", sum(1 for v in onb.values() if v.get("yakin")), "yeni", cozulen, "kalan 404", sum(1 for v in onb.values() if v.get("durum") == 404 and not v.get("yakin")))
