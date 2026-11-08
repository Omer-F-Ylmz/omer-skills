"""sansursuz_tersine.py JSON'unu desen bazinda ozetler (kucuk cikti). Kullanim: python sansursuz_tersine_ozet.py <json>"""
import json, re, sys
import numpy as np

d = json.load(open(sys.argv[1], encoding="utf-8"))
print("a:", d["a"].split("\\")[-1], "| b:", d["b"].split("\\")[-1], "| ortak", d["ortak"],
      "| yalniz_o", len(d["yalniz_orijinal"]), "| yalniz_d", len(d["yalniz_degisen"]))
g = {}
for t in d["tensorler"]:
    g.setdefault(re.sub(r"\d+", "#", t["ad"]), []).append(t)
print(f"{'desen':58} n  deg  goreli_ort  enj1  rank1%  katmanlar")
for p, L in sorted(g.items()):
    ch = [t for t in L if t.get("fark_norm", 0) > 0]
    if not ch:
        continue
    e = [t["enerji_ilk1"] for t in ch if "enerji_ilk1" in t]
    rk = [t["rank_1pct"] for t in ch if "rank_1pct" in t]
    ly = [int(m.group(1)) for t in ch if (m := re.search(r"layers\.(\d+)\.", t["ad"]))]
    ly_s = f"{min(ly)}-{max(ly)}" if ly else "-"
    print(f"{p[:58]:58} {len(L):3d} {len(ch):3d} {np.mean([t['goreli'] for t in ch]):.2e} "
          f"{(np.mean(e) if e else float('nan')):.3f} {(int(np.median(rk)) if rk else -1):5d}  {ly_s}")
rest = [t for t in d["tensorler"] if "uW_orij" in t]
if rest:
    print("-- rank-1 tensorler: uW_yeni/uW_orij (0=tam ortogonal), sutun/satir norm orani")
    for t in rest[:6]:
        print(" ", t["ad"][-48:], f"{t['uW_yeni']/max(t['uW_orij'],1e-12):.3f}", f"{t['sutun_norm_oran']:.4f}", f"{t['satir_norm_oran']:.4f}")
    r = np.array([t["uW_yeni"] / max(t["uW_orij"], 1e-12) for t in rest])
    print("   tum rank-1:", len(rest), "| uW oran ort/medyan", round(r.mean(), 3), round(float(np.median(r)), 3))
for dim, s in d["yon_benzerlik"].items():
    print("-- yon benzerligi dim", dim, "n", len(s["adlar"]), "ort|cos|", s["ort_abs_cos"], "min", s["min"])
