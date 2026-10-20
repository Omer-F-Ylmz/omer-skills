"""rtk2 A/B: ham ↔ rtk ↔ rtk2; token = count_tokens, kalite = tohum anahtar + sıkı sinyal (her ham ad çıktıda).
  python rtk2_ab.py egitim|held → rtk2_ab_<mod>.json  (held yalnız kapıda tek sefer; kilit: rtk2_set.lock)"""
import hashlib, json, os, sys, time
import taban as t, rtk2, rtk2_set as S


def anahtar(k, ham, br, konu):
    if k == "KONU": return konu
    if k == "BR": return br
    if k: return k
    m = rtk2.re.search(r"[\w./-]{12,}", ham); return m.group(0) if m else "?"


def sikı(argv, ham, cikti):
    if argv[0] == "ls":
        yol = next((a for a in argv[1:] if not a.startswith("-")), ".")
        return int(all(n in cikti for n in os.listdir(yol)))
    return int(not rtk2.eksik(argv, ham, cikti))


tk = lambda x: t.tok(x) if x.strip() else 0
mod = sys.argv[1]
if mod == "held":
    lock = (t.BU / "rtk2_set.lock").read_text().strip()
    assert hashlib.sha256(json.dumps(S.HELD).encode()).hexdigest() == lock, "held-out değişmiş"
liste = S.EGITIM if mod == "egitim" else S.HELD
os.chdir(t.KOK)
t.GOVDE, t.BASLIK = t.kur_baslik()
br = t.kos(["git", "branch", "--show-current"])[0].strip(); konu = t.kos(["git", "log", "-1", "--format=%s"])[0].strip()[:25]
sat = []
for ad, argv, k in liste:
    ham, _ = rtk2.calis(argv)
    ts = time.time(); o1, _ = rtk2.calis(["rtk", *argv]); s1 = time.time() - ts
    ts = time.time(); o2 = rtk2.rtk2(argv); s2 = time.time() - ts
    key = anahtar(k, ham, br, konu)
    sat.append({"ad": ad, "ham": tk(ham), "rtk": tk(o1), "rtk2": tk(o2),
                "tohum_rtk": int(key in o1), "tohum_rtk2": int(key in o2), "tohum_ham": int(key in ham),
                "sikı_rtk": sikı(argv, ham, o1), "sikı_rtk2": sikı(argv, ham, o2), "sn_rtk": round(s1, 2), "sn_rtk2": round(s2, 2)})
n = len(sat); top = {k: sum(s[k] for s in sat) for k in sat[0] if k != "ad"}
print(mod, "n", n, top, "count_tokens", t.SAYAC["say"])
for s in sat:
    if not (s["tohum_rtk2"] and s["sikı_rtk2"]) or not s["tohum_rtk"] or not s["sikı_rtk"]:
        print("  !", s["ad"], {k: s[k] for k in ("ham", "rtk", "rtk2", "tohum_rtk", "tohum_rtk2", "sikı_rtk", "sikı_rtk2")})
json.dump({"satir": sat, "toplam": top}, open(t.BU / f"rtk2_ab_{mod}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
