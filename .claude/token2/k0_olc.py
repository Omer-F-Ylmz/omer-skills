"""TOKEN-2 K0: TELVE taban.py'yi tüm projelere genişletir (TELVE, blender, omer-skills, mod) → iş türü × kategori + en büyük 5 israf.
Kullanım: python k0_olc.py [gun=14] — çıktı sayıya indirgenmiş; ayrıntı k0_olc.json."""
import collections, glob, json, os, re, sys, time
from pathlib import Path

sys.path.insert(0, r"C:\Users\pc\Desktop\TELVE-wt\token1\docs\r1\_ham\token1")
import taban  # noqa: E402

# iş adı = istemdeki ilk BÜYÜK-HARF etiketi, sondaki sayı/harf atılır (TOKEN-2 d1 → TOKEN, BLENDER-ARAC-1 → BLENDER-ARAC)
taban.TUR = re.compile(r"\b((?:TELVE-)?[A-ZÇĞİÖŞÜ]{3,}(?:-[A-ZÇĞİÖŞÜ]{2,})*)(?:-\d+[a-z]?)?\b")
GUN = int(sys.argv[1]) if len(sys.argv) > 1 else 14
AG = {"input_tokens": 1, "cache_read_input_tokens": 0.1, "cache_creation_input_tokens": 1.25, "output_tokens": 5}  # token_olc AGIRLIK (5m yazma)
PROJE = (("TELVE", "telve"), ("blender", "blender"), ("omer-skills", "omer-skills"), ("mod", r"(^|-)mod"))


def agir(u):
    return sum(AG[k] * (u.get(k) or 0) for k in AG)


def proje(ad):
    return next((p for p, r in PROJE if re.search(r, ad, re.I)), None)


sinir, satir = time.time() - GUN * 86400, []
for d in glob.glob(os.path.expanduser("~/.claude/projects/*")):
    p = proje(os.path.basename(d))
    for f in glob.glob(os.path.join(d, "*.jsonl")) if p else []:
        if os.path.getmtime(f) < sinir:
            continue
        try:
            o = taban.oturum(f)
        except Exception:
            continue
        if not o["adim"]:
            continue
        u, alt = o["usage"], sum(agir(a["usage"]) for a in o["alt_ajan"])
        kat = {k: 0.1 * v.get("tasima", 0) + v.get("giris", 0) for k, v in o["kategori"].items()}  # taşınan sonuç önbellek okuması olarak
        satir.append({"proje": p, "is": o["tur"] or "?", "adim": o["adim"], "agir": agir(u), "alt": alt, "cikti": 5 * u.get("output_tokens", 0),
                      "kacirma": u.get("onbellek_kacirma", 0), "ilk": u.get("ilk_baglam", 0), "kat": kat})

T = collections.defaultdict(lambda: collections.Counter())
for s in satir:
    t = T[(s["proje"], s["is"])]
    t["oturum"] += 1; t["adim"] += s["adim"]; t["agir"] += s["agir"] + s["alt"]; t["alt"] += s["alt"]; t["cikti"] += s["cikti"]
    t["kacirma"] += s["kacirma"]; t["ilk"] += s["ilk"]
    for k, v in s["kat"].items():
        t["k:" + k] += v
M = 1e6
print(f"K0 · {GUN} gün · {len(satir)} oturum · toplam {sum(t['agir'] for t in T.values()) / M:.1f}M ağırlıklı")
print("proje\tiş\toturum\tadım\tağırlıklı_M\talt%\tçıktı%\tkaçırma\tsabit_taban_k\ttop3 kategori (M)")
for (p, i), t in sorted(T.items(), key=lambda x: -x[1]["agir"])[:20]:
    k3 = sorted(((k[2:], v) for k, v in t.items() if k.startswith("k:")), key=lambda x: -x[1])[:3]
    print(f"{p}\t{i}\t{t['oturum']}\t{t['adim']}\t{t['agir'] / M:.2f}\t{100 * t['alt'] / t['agir']:.0f}\t{100 * t['cikti'] / t['agir']:.0f}\t"
          f"{t['kacirma']}\t{t['ilk'] / t['oturum'] / 1e3:.0f}\t" + " ".join(f"{k}:{v / M:.2f}" for k, v in k3))
# israf adayları: alt ajan, çıktı, önbellek kaçırma (≈ilk bağlam × 1.15 fazla yazma), sabit taban (ilk bağlam × adım × 0.1), kategori taşıma
I = collections.Counter()
for s in satir:
    I[(s["proje"], "alt_ajan")] += s["alt"]; I[(s["proje"], "cikti")] += s["cikti"]
    I[(s["proje"], "onbellek_kacirma")] += s["kacirma"] * s["ilk"] * 1.15
    I[(s["proje"], "sabit_taban")] += s["ilk"] * s["adim"] * 0.1
    for k, v in s["kat"].items():
        I[(s["proje"], k)] += v
print("EN BÜYÜK 5 İSRAF ADAYI (M ağırlıklı):", " · ".join(f"{p}/{k} {v / M:.2f}" for (p, k), v in I.most_common(5)))
Path(__file__).with_suffix(".json").write_text(json.dumps({f"{p}|{i}": dict(t) for (p, i), t in T.items()}, ensure_ascii=False), encoding="utf-8")
