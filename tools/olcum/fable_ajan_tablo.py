"""FABLE-AJAN karar: olcum.tsv + metin/ → Jev (≤1 batch, ≈$0.0001/yanıt; tavan $4'ün çok altında) → aile × model ve model toplamı.
KABUL = kalite (Jev ve regex ortalaması) ≥ taban VE çıktı jetonu ≤ taban VE $ ≤ taban. Jev erişilemezse yalnız regex.
  python tools/olcum/fable_ajan_tablo.py <cikti_dizin> [--jevsiz]
"""
import collections, json, sys
from pathlib import Path

DIZIN = Path(__file__).resolve().parent
sys.path[:0] = [str(DIZIN), str(DIZIN.parent / "jev")]
import jev_yargic  # noqa: E402

KOK = DIZIN.parents[1]


def oku(d):
    L = (d / "olcum.tsv").read_text(encoding="utf-8").splitlines()
    b = L[0].split("\t")
    return [r for r in (dict(zip(b, s.split("\t"))) for s in L[1:] if s.strip()) if r["output"] != "0"]  # out 0 = limit satırı


def tohumla(kaynak, d):
    """Yansıtma turu yalnız proto koşar; kaynak ölçümün taban satırlarını (metin + Jev puanı) eksikse d'ye kopyalar."""
    mevcut = oku(d)
    ajanlar, var = {s["ajan"] for s in mevcut}, {(s["ajan"], s["kol"], s["tekrar"]) for s in mevcut}
    yeni = [s for s in oku(kaynak) if s["kol"] == "taban" and s["ajan"] in ajanlar and (s["ajan"], "taban", s["tekrar"]) not in var]
    if not yeni:
        return
    baslik = (d / "olcum.tsv").read_text(encoding="utf-8").splitlines()[0].split("\t")
    with open(d / "olcum.tsv", "a", encoding="utf-8") as f:
        f.writelines("\t".join(s[b] for b in baslik) + "\n" for s in yeni)
    jk = json.loads((kaynak / "jev.json").read_text(encoding="utf-8")) if (kaynak / "jev.json").exists() else {}
    jd = json.loads((d / "jev.json").read_text(encoding="utf-8")) if (d / "jev.json").exists() else {}
    for s in yeni:
        k = f"{s['ajan']}__taban__{s['tekrar']}"
        (d / "metin" / f"{k}.md").write_text((kaynak / "metin" / f"{k}.md").read_text(encoding="utf-8"), encoding="utf-8")
        if k in jk:
            jd[k] = jk[k]
    (d / "jev.json").write_text(json.dumps(jd, ensure_ascii=False, indent=0), encoding="utf-8")


def jev_puanla(d, satirlar):
    """jev.json önbellek: anahtar ajan__kol__tekrar → 0-10; yalnız eksikler gönderilir."""
    yol = d / "jev.json"
    puan = json.loads(yol.read_text(encoding="utf-8")) if yol.exists() else {}
    gorev = {g["ajan"]: g for g in json.loads((KOK / "ajanlar" / "kalite3" / "gorevler.json").read_text(encoding="utf-8"))}
    eksik = [s for s in satirlar if f"{s['ajan']}__{s['kol']}__{s['tekrar']}" not in puan]
    if eksik:
        from jev.cekirdek import Tasiyici
        states = [{"gorev": gorev[s["ajan"]]["istem"], "kabul": "; ".join(m["regex"] for m in gorev[s["ajan"]]["rubrik"]),
                   "yanit": (d / "metin" / f"{s['ajan']}__{s['kol']}__{s['tekrar']}.md").read_text(encoding="utf-8")} for s in eksik]
        for s, c in zip(eksik, Tasiyici(en_fazla=2, istek_tavan=len(eksik) + 10).yargila(states, jev_yargic.SORU)):
            puan[f"{s['ajan']}__{s['kol']}__{s['tekrar']}"] = round(c["kalite"]["score"] * 2, 1)
        yol.write_text(json.dumps(puan, ensure_ascii=False, indent=0), encoding="utf-8")
    return puan


def ozet(satirlar, jev):
    """(anahtar, kol) → ortalamalar; anahtar = (aile, model) ve (*, model)."""
    t = collections.defaultdict(lambda: collections.defaultdict(list))
    for s in satirlar:
        if s["rc"] != "0":
            continue
        j = jev.get(f"{s['ajan']}__{s['kol']}__{s['tekrar']}")
        for k in ((s["aile"], s["model"]), ("*", s["model"])):
            x = t[(k, s["kol"])]
            x["regex"].append(float(s["regex"]))
            x["out"].append(int(s["output"]))
            x["usd"].append(float(s["usd"]))
            if j is not None:
                x["jev"].append(j)
    return {k: {a: round(sum(v) / len(v), 4) for a, v in x.items()} | {"n": len(x["out"])} for k, x in t.items()}


def karar(o):
    """→ [(aile, model, KABUL|RET|EKSIK, taban, proto)]; RET gerekçesi satırda (kalite↓ / out↑ / $↑)."""
    out = []
    for (aile, model) in sorted({k for k, _ in o}):
        ta, pr = o.get(((aile, model), "taban")), o.get(((aile, model), "proto"))
        if not ta or not pr:
            out.append((aile, model, "EKSIK", ta, pr))
            continue
        neden = [ad for ad, kotu in (("kalite", any(pr.get(m, 0) < ta.get(m, 0) for m in ("regex", "jev") if m in ta and m in pr)),
                                     ("out", pr["out"] > ta["out"]), ("$", pr["usd"] > ta["usd"])) if kotu]
        out.append((aile, model, "KABUL" if not neden else "RET:" + ",".join(neden), ta, pr))
    return out


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    d = Path(argv[0])
    if "--taban" in argv:
        tohumla(Path(argv[argv.index("--taban") + 1]), d)
    satirlar = oku(d)
    jev = {}
    if "--jevsiz" not in argv:
        try:
            jev = jev_puanla(d, satirlar)
        except Exception as e:  # noqa: BLE001 — jev yardımcı; karar regex'le sürer
            print("jev atlandı:", type(e).__name__, e)
    kararlar = karar(ozet(satirlar, jev))
    for aile, model, k, ta, pr in kararlar:
        f = lambda x: "-" if not x else f"r{x['regex']:.2f} j{x.get('jev', 0):.2f} out{x['out']:.0f} ${x['usd']:.4f} n{x['n']}"  # noqa: E731
        print(f"{aile}\t{model}\t{k}\ttaban {f(ta)}\tproto {f(pr)}")
    if "--yaz" in argv:  # onay/fable_ajan_uygula.py girdisi
        ad = argv[argv.index("--ad") + 1] if "--ad" in argv else "calisma-protokolu"
        yaz(KOK / "docs" / "kutuphane" / "olcum" / "fable-ajan-karar.tsv", [(a, m, k) for a, m, k, *_ in kararlar if a != "*"], ad)


def yaz(yol, kararlar, ad):
    """Birleştirir (her ölçüm dizini ayrı --yaz): yeni KABUL üstüne yazar (yansıtma turu = daha kısa sürüm), RET eski KABUL'ü silmez."""
    eski = {}
    if yol.exists():
        for s in yol.read_text(encoding="utf-8").splitlines()[1:]:
            c = s.split("\t")
            eski[(c[0], c[1])] = (c[2], c[3] if len(c) > 3 else "calisma-protokolu")
    for a, m, k in kararlar:
        if k == "KABUL" or eski.get((a, m), ("",))[0] != "KABUL":
            eski[(a, m)] = (k, ad)
    yol.write_text("aile\tmodel\tkarar\tprotokol\n" + "".join(f"{a}\t{m}\t{k}\t{p}\n" for (a, m), (k, p) in sorted(eski.items())), encoding="utf-8")


if __name__ == "__main__":
    main()
