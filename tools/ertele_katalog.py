"""ERTELE-1: skill/ajan ertelenmiş yükleme kataloğu (MCP ToolSearch mantığı: başta liste yok, iş gelince ara → tam metni o an oku).
python tools/ertele_katalog.py kur            → ~/.claude/ertele-dizin.json (skill + ajan adı → tanım dosyası; hiçbir dosya taşınmaz/silinmez)
python tools/ertele_katalog.py ara "<iş>"     → arac_ara kartları + kartsız tanımlarda anahtar sözcük isabeti (ad · tür · tek satır)
python tools/ertele_katalog.py tam <ad>       → tanımın tam metni (skill: SKILL.md, ajan: .md)"""
import collections
import json
import math
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
EV = Path.home() / ".claude"
DIZIN = EV / "ertele-dizin.json"


def _on_bilgi(yol):
    m = re.match(r"---\s*\n(.*?)\n---", yol.read_text(encoding="utf-8", errors="ignore"), re.S)
    alan = dict(re.findall(r"^(name|description):\s*(.*)$", m.group(1), re.M)) if m else {}
    if alan.get("description", "").strip() in ("", ">", ">-", "|", "|-", ">+", "|+"):  # YAML blok açıklama: girintili satırlar
        b = re.search(r"^description:[^\n]*\n((?:[ \t]+[^\n]*\n?)+)", m.group(1) + "\n", re.M) if m else None
        alan["description"] = " ".join(b.group(1).split()) if b else ""
    return alan.get("name", "").strip().strip("'\""), alan.get("description", "").strip().strip("'\"")[:200]


def _ekle(d, tur, ad, yol):
    if ad and ad not in d:
        d[ad] = {"tur": tur, "yol": str(yol), "acik": _on_bilgi(yol)[1]}


def kur():
    d = {}
    for kok in (KOK / ".claude", EV):
        for f in sorted((kok / "skills").glob("*/SKILL.md")) + sorted((kok / "skills").glob("*/skills/*/SKILL.md")) \
                + sorted((kok / "skills").glob("synced/*/**/SKILL.md")):  # claude.ai senkron kopyaları
            _ekle(d, "skill", _on_bilgi(f)[0] or f.parent.name, f)
            _ekle(d, "skill", f.parent.name, f)  # ön bilgideki ad klasör adından farklı olabilir ("Bug Triage")
        for f in sorted((kok / "skills").glob("**/skills/*/TALIMAT.md")):  # paket içi alt skill (SKILL.md yerine TALIMAT.md)
            _ekle(d, "skill", _on_bilgi(f)[0] or f.parent.name, f)
            _ekle(d, "skill", f.parent.name, f)
        for f in sorted((kok / "agents").glob("*.md")):
            _ekle(d, "ajan", _on_bilgi(f)[0] or f.stem, f)
    kurulu = json.loads((EV / "plugins" / "installed_plugins.json").read_text(encoding="utf-8"))
    for anahtar, kayitlar in kurulu.get("plugins", kurulu).items():
        eklenti = anahtar.split("@")[0]
        for k in kayitlar:
            p = Path(k["installPath"])
            for f in sorted(p.glob("**/SKILL.md")):
                _ekle(d, "skill", f"{eklenti}:{f.parent.name}", f)
                _ekle(d, "skill", _on_bilgi(f)[0] or f.parent.name, f)  # CC listesinde öneksiz görünen eklenti skill'i
            for f in sorted(p.glob("agents/**/*.md")):
                ic = ":".join(f.relative_to(p / "agents").with_suffix("").parts[:-1] + (_on_bilgi(f)[0] or f.stem,))
                _ekle(d, "ajan", f"{eklenti}:{ic}", f)
            for f in sorted(p.glob("commands/**/*.md")):
                _ekle(d, "komut", f"{eklenti}:{f.stem}", f)
    nz = KOK / "skills" / "ajan-getir" / "ne_zaman.tsv"  # ERTELE-3: gizli ajanların Türkçe "ne zaman" anahtarları
    for l in (nz.read_text(encoding="utf-8").splitlines() if nz.exists() else []):
        ad, _, kw = l.partition("\t")
        if ad in d:
            d[ad]["acik"] = f"{d[ad]['acik']} · ne zaman: {kw}"
    for ad, v in d.items():  # müdür →adını verdiği özel skill'ler (yalnız dizinde; skill dosyasına dokunulmaz)
        if ad.startswith("departman-") and ":" not in ad:
            metin = Path(v["yol"]).read_text(encoding="utf-8", errors="ignore")
            v["ozel"] = list(dict.fromkeys(a for a in re.findall(r"[\w:-]{3,}", metin)
                                           if a in d and d[a]["tur"] == "skill" and not a.startswith("departman-")))
    DIZIN.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return d


def _dizin():
    return json.loads(DIZIN.read_text(encoding="utf-8")) if DIZIN.exists() else kur()


def _katla(s):
    return s.lower().translate(str.maketrans("çğıöşüâî", "cgiosuai"))


def _mudur(gorev, d, n=2):
    """departman-* müdür skill'leri: Türkçe katlama + 5 harflik kök eşleşmesi (araştır → arastirma)."""
    kok = {s[:4] for s in re.findall(r"\w{4,}", _katla(gorev))} | set(re.findall(r"\w[#+]+|\.net\b", _katla(gorev)))  # C#, C++, .NET
    puan = sorted(((sum(k in _katla(ad + " " + v["acik"]) for k in kok), ad) for ad, v in d.items()
                   if ad.startswith("departman-") and ":" not in ad), key=lambda x: -x[0])
    return [ad for p, ad in puan[:n] if p > 0]


def _ozel_sira(gorev, d, mudur, n=4):
    """Müdürün özel skill'leri, iş kökleriyle (5 harf) örtüşmeye göre; örtüşme yoksa müdür metnindeki sıra."""
    kok = {s[:5] for s in re.findall(r"\w{4,}", _katla(gorev))}
    oz = d[mudur].get("ozel", [])
    return sorted(oz, key=lambda a: -sum(k in _katla(a + " " + d[a]["acik"]) for k in kok))[:n]


def _bm25(gorev, d):
    """ERTELE-3: alt-dizi sayımı yerine Türkçe katlamalı 5 harflik kök BM25 (gündelik tarif → nadir, ayırt edici kök ağır basar)."""
    kel = lambda s: [w[:5] for w in re.findall(r"[a-z0-9]{3,}", _katla(s))]
    docs = {ad: kel(ad.replace(":", " ").replace("-", " ") + " " + v["acik"]) for ad, v in d.items()}
    df = collections.Counter(w for t in docs.values() for w in set(t))
    N, ort = len(docs), sum(map(len, docs.values())) / max(len(docs), 1)
    q = set(kel(gorev))
    return {ad: sum(math.log(1 + (N - df[w] + .5) / (df[w] + .5)) * t.count(w) * 2.2 / (t.count(w) + 1.2 * (.25 + .75 * len(t) / ort))
                    for w in q if w in t) for ad, t in docs.items()}


GOMME = EV / "ertele-gomme.npy"  # ERTELE-3 tur5: çok dilli gömme (Cloudflare Workers AI bge-m3), tanım dosyası başına bir satır


def _cf(model, govde, zaman=120):
    import os
    import urllib.request
    u = f"https://api.cloudflare.com/client/v4/accounts/{os.environ['CLOUDFLARE_ACCOUNT_ID']}/ai/run/{model}"
    r = urllib.request.Request(u, data=json.dumps(govde).encode(), headers={
        "Authorization": "Bearer " + os.environ["CLOUDFLARE_API_KEY"], "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r, timeout=zaman))["result"]


def _gom(metinler):
    return _cf("@cf/baai/bge-m3", {"text": metinler})["data"]


def _llm(istem, max_tokens=200):
    return _cf("@cf/meta/llama-3.3-70b-instruct-fp8-fast", {"messages": [{"role": "user", "content": istem}],
                                                           "max_tokens": max_tokens}, 60)["response"].strip()


def gom():
    """Her tanım dosyası için ad + tam açıklama (+ ne zaman) gömülür; sorgu başına yalnız sorgu gömülür."""
    import numpy as np
    d = _dizin()
    yollar = list(dict.fromkeys(v["yol"] for v in d.values()))
    adlar = collections.defaultdict(list)
    for ad, v in d.items():
        adlar[v["yol"]].append(ad.replace(":", " ").replace("-", " "))
    metin = []
    for y in yollar:
        bas = Path(y).read_text(encoding="utf-8", errors="ignore")[:6000]
        tam_acik = re.search(r"^description:[ \t]*([^\n]*(?:\n[ \t]+[^\n]*)*)", bas, re.M)
        acik = " ".join((tam_acik.group(1) if tam_acik else "").split()).lstrip(">|-+ ")
        if len(acik) < 40:  # açıklamasız tanım: gövdenin ilk metni
            acik += " " + " ".join(re.sub(r"^---.*?\n---", "", bas, flags=re.S).split())[:500]
        metin.append(f"{' / '.join(dict.fromkeys(adlar[y]))}: {acik[:700]}"[:1000])
    nz = {d[a]["yol"]: d[a]["acik"].split(" · ne zaman: ", 1)[1] for a in d if " · ne zaman: " in d[a]["acik"]}
    metin = [m + (" · " + nz[y] if y in nz else "") for m, y in zip(metin, yollar)]
    v = []
    for i in range(0, len(metin), 50):
        v += _gom(metin[i:i + 50])
    v = np.asarray(v, dtype=np.float32)
    np.save(GOMME, (v / np.linalg.norm(v, axis=1, keepdims=True)).astype(np.float16))
    (EV / "ertele-gomme.json").write_text(json.dumps(yollar, ensure_ascii=False), encoding="utf-8")
    return len(yollar)


def _anlamsal(gorev):
    """yol → kosinüs; gömme dosyası ya da ağ yoksa boş (BM25 tek başına çalışır)."""
    try:
        import numpy as np
        yollar = json.loads((EV / "ertele-gomme.json").read_text(encoding="utf-8"))
        q = np.asarray(_gom([gorev])[0], dtype=np.float32)
        return dict(zip(yollar, (np.load(GOMME).astype(np.float32) @ (q / np.linalg.norm(q))).tolist()))
    except Exception:
        return {}


def _birlesik(gorev, d, n):
    """BM25 + gömme sıra birleştirme (RRF); aynı dosyanın ikinci adı tekrar listelenmez."""
    bm = sorted(((p, ad) for ad, p in _bm25(gorev, d).items() if p > 0), reverse=True)
    an = _anlamsal(gorev)
    gm = sorted(((an[d[ad]["yol"]], ad) for ad in d if d[ad]["yol"] in an), reverse=True)
    rrf = collections.Counter()
    for liste, w in ((bm, 1.0), (gm, 1.0 if an else 0)):
        for i, (_, ad) in enumerate(liste[:200]):
            rrf[ad] += w / (60 + i)
    cikti, gor = [], set()
    for ad, _ in rrf.most_common():
        if d[ad]["yol"] not in gor:
            gor.add(d[ad]["yol"])
            cikti.append(ad)
        if len(cikti) == n:
            break
    return cikti


def ara(gorev, n=12):
    import arac_ara as aa
    d = _dizin()
    mudur = _mudur(gorev, d)
    o = [f"{ad} · müdür skill · {d[ad]['acik'][:110]}\n  → özel skill (işe en yakın): {', '.join(_ozel_sira(gorev, d, ad)) or '-'}"
         for ad in mudur]
    bir = [ad for ad in _birlesik(gorev, d, n + len(mudur)) if ad not in mudur][:n]
    o += [f"{ad} · {d[ad]['tur']} · {d[ad]['acik'][:110]}" for ad in bir]
    gor = set(bir) | set(mudur)
    kartlar = [k for k in aa.ara(gorev)["kartlar"] if k.get("tur") in ("skill", "ajan", None) and k["ad"] not in gor][:4]
    o += [f"{k['ad']} · {k.get('tur', '?')} · {(k.get('ne_yapar') or k.get('aciklama') or '')[:110]}" for k in kartlar]
    return "\n".join(o) + "\n(tam metin: python tools/ertele_katalog.py tam <ad>)"


def tam(ad):
    import arac_ara as aa
    d = _dizin()
    v = d.get(ad) or d.get(ad.split(":")[-1]) or next(  # komuttan türeyen alt ad: modernize-harden-scan → modernize-harden
        (d[k] for k in sorted(d, key=len, reverse=True) if ad.startswith(k + "-")), None)
    if v:
        metin = Path(v["yol"]).read_text(encoding="utf-8", errors="ignore")
        if v.get("ozel"):
            metin += ("\n\n---\nKATALOG: bu müdürün adını verdiği özel skill'ler (işi bunlar yapar; uygun olanı "
                      f"`python tools/ertele_katalog.py tam <ad>` ile yükle): {', '.join(v['ozel'])}\n")
        return metin
    return aa.tam(ad) or f"bulunamadı: {ad}"


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    k, *a = sys.argv[1:] or ["?"]
    print({"kur": lambda: f"{len(kur())} tanım → {DIZIN}", "gom": lambda: f"{gom()} dosya → {GOMME}", "ara": lambda: ara(" ".join(a)), "tam": lambda: tam(a[0])}.get(k, lambda: __doc__)())
