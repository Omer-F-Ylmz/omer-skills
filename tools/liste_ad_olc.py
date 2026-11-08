"""LISTE-EKSIK kapi 2: yeni kalem adlari kaynak video metninde birebir geciyor mu? olc | --yaz (aday tablosu)"""
import csv, json, random, re, sys
from pathlib import Path
K = Path(r"C:\Projeler\omer-skills"); V = K / "docs/video-tarama"
csv.field_size_limit(10**9)
def rd(p):
    return list(csv.reader(open(p, encoding="utf-8", errors="replace", newline=""), delimiter="\t", quoting=csv.QUOTE_NONE))
rows = rd(V / "ana-liste.tsv"); old = {r[0] for r in rd(V / "ana-liste.tsv.yedek-d2b")}
new = [r for r in rows[1:] if r[0] not in old]
dos = {}
for d in ("derin", "derin-2", "derin-3"):
    for f in sorted((V / d).glob("*.json")): dos.setdefault(f.stem, f)
cache = {}
def metin(i):
    if i not in cache:
        f = dos.get(i)
        if not f: cache[i] = ""; return ""
        j = json.loads(f.read_text(encoding="utf-8", errors="replace"))
        p = [json.dumps(j.get("meta", {}), ensure_ascii=False)]
        for k in ("transkript", "ekran"):
            for x in j.get(k) or []:
                p.append(x.get("t", "") if isinstance(x, dict) else str(x))
        for k in ("linkler", "komutlar"):
            p += [str(x) for x in j.get(k) or []]
        p.append(j.get("kare_aciklama") or "")
        cache[i] = "\n".join(p)
    return cache[i]
def norm(s): return re.sub(r"\s+", " ", s)
tam = ci = yok = 0; sonuc = []
for r in new:
    ids = r[3].split(",")
    T = norm(" ".join(metin(i) for i in ids)); a = norm(r[0])
    if a in T: d = "TAM"; tam += 1
    elif a.lower() in T.lower(): d = "CI"; ci += 1
    else: d = "YOK"; yok += 1
    sonuc.append((r[0], d, ids))
print(f"yeni {len(new)} TAM {tam} ({tam/len(new):.1%}) buyuk-kucuk {ci} metinde-yok {yok}")
if "--yaz" in sys.argv:
    with open(K / ".kos/kopru/ogren/liste-eksik-ad/olc.tsv", "w", encoding="utf-8") as o:
        for a, d, ids in sonuc: o.write(f"{a}\t{d}\t{','.join(ids)}\n")

# ---- kapi 2 cekme: yalniz bu dosya --cek ile calisir
if "--cek" in sys.argv:
    import difflib
    try:
        from rapidfuzz import fuzz
        oran = lambda a, b: fuzz.ratio(a, b) / 100
    except Exception:
        oran = lambda a, b: difflib.SequenceMatcher(None, a, b).ratio()
    def sikis(s):
        pos = []; out = []
        for i, c in enumerate(s):
            if c.isalnum(): out.append(c.lower()); pos.append(i)
        return "".join(out), pos
    def cek(a, T):
        if a in T: return a, "TAM"
        i = T.lower().find(a.lower())
        if i >= 0: return T[i:i+len(a)], "BK"
        adaylar = [a]
        b = re.sub(r"\([^)]*\)", "", a).strip(); b2 = re.sub(r"^(/|Prompt:\s*)", "", b).strip()
        for x in (b, b2):
            if x and x != a and len(x) >= 3: adaylar.append(x)
        Tc, pos = sikis(T)
        for x in adaylar:
            xc, _ = sikis(x)
            if len(xc) < 4 and x != a: continue
            if len(xc) >= 3:
                j = Tc.find(xc)
                if j >= 0: return T[pos[j]:pos[j+len(xc)-1]+1], "SIKIS"
        toks = [(m.start(), m.end()) for m in re.finditer(r"\S+", T)]
        best = (0, None)
        for x in adaylar:
            n = len(x.split()); xl = x.lower()
            if len(xl) < 5: continue
            for w in {max(1, n-1), n, n+1}:
                for k in range(0, len(toks) - w + 1):
                    s, e = toks[k][0], toks[k+w-1][1]
                    if abs((e - s) - len(x)) > max(4, len(x)//3): continue
                    r = oran(xl, T[s:e].lower())
                    if r > best[0]: best = (r, T[s:e])
        if best[0] >= 0.88: return best[1].strip(".,;:!?\"'()"), "BULANIK"
        return None, "YOK"
    out = []; say = {}
    for r in new:
        ids = r[3].split(","); T = norm(" ".join(metin(i) for i in ids))
        yeni, d = cek(norm(r[0]), T)
        say[d] = say.get(d, 0) + 1; out.append((r[0], yeni or "", d))
    print(say)
    with open(K / ".kos/kopru/ogren/liste-eksik-ad/cek.tsv", "w", encoding="utf-8") as o:
        for x in out: o.write("\t".join(x) + "\n")
