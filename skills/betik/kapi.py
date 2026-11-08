"""Kapilari degerlendirir.
  python kapi.py --kapi A --ret m_ret.json --kalite m_kal.json [--kl 0.004]
  python kapi.py --kapi B --ret gguf_ret.json --taban-ret taban_ret.json
  python kapi.py --kapi C --kalite m_kal.json --taban-kalite taban_kal.json [--gecikme 8]
"""
import argparse, json

KURAL = {"A": {"hard": 1.0, "soft": 3.0, "kalite": 98.0},
         "B": {"hard_fark": 1.0}, "C": {"kalite_kaybi": 1.0, "gecikme": 15.0}}

p = argparse.ArgumentParser()
p.add_argument("--kapi", required=True, choices=list(KURAL))
p.add_argument("--ret"); p.add_argument("--kalite"); p.add_argument("--kl", type=float)
p.add_argument("--taban-ret"); p.add_argument("--taban-kalite"); p.add_argument("--gecikme", type=float)
a = p.parse_args()
k = KURAL[a.kapi]
sorun = []

if a.kapi in ("A", "B"):
    d = json.load(open(a.ret, encoding="utf-8"))
    if a.kapi == "A":
        if d["hard_yuzde"] > k["hard"]: sorun.append(f"hard {d['hard_yuzde']} > {k['hard']}")
        if d["soft_yuzde"] > k["soft"]: sorun.append(f"soft {d['soft_yuzde']} > {k['soft']}")
        q = json.load(open(a.kalite, encoding="utf-8"))
        if q["kalite_yuzde"] < k["kalite"]: sorun.append(f"kalite {q['kalite_yuzde']} < {k['kalite']}")
        if a.kl is not None and a.kl > 0.2: sorun.append(f"KL {a.kl} > 0,2 (ikinci kapi)")
        if d.get("hakem_uyusmazlik", 0) > max(3, d["n"] // 50):
            sorun.append(f"yargic uyusmazligi {d['hakem_uyusmazlik']} - elle bak")
    else:
        t = json.load(open(a.taban_ret, encoding="utf-8"))
        if d["hard_yuzde"] - t["hard_yuzde"] > k["hard_fark"]:
            sorun.append(f"GGUF ret artisi {d['hard_yuzde'] - t['hard_yuzde']:.2f} > 1 - bir ust kuant")
else:
    d = json.load(open(a.kalite, encoding="utf-8")); t = json.load(open(a.taban_kalite, encoding="utf-8"))
    kayip = t["kalite_yuzde"] - d["kalite_yuzde"]
    if kayip > k["kalite_kaybi"]: sorun.append(f"kalite kaybi {kayip:.2f} > 1")
    if a.gecikme and a.gecikme > k["gecikme"]: sorun.append(f"gecikme %{a.gecikme} > 15")

print("KAPI", a.kapi, ":", "GECTI" if not sorun else "KALDI")
for s in sorun: print(" -", s)
