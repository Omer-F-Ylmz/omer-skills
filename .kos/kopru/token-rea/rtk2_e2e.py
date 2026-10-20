"""rtk2 d4 uçtan uca: her komut gerçek subprocess ile; rota = hook sınıflandırması (rtk2.tur) → süzgeçliyse `python -I -S rtk2.py`, değilse doğrudan `rtk`.
  python rtk2_e2e.py egitim|held4 → rtk2_e2e_<mod>.json (held4 tek sefer; kilit rtk2_set4.lock). Kapı: her komutta sn_rtk2 ≤ sn_rtk, token ve kalite ≥ rtk."""
import hashlib, json, os, re, subprocess, sys, time
import taban as t, rtk2, rtk2_set as S

PY = ["python", "-I", "-S", str(t.BU / "rtk2.py")]
tk = lambda x: sum(t.tok(x[i:i + 150000]) for i in range(0, len(x), 150000)) if x.strip() else 0


def kos(argv, n=5):
    sn, cik = [], ""
    for _ in range(n):
        ts = time.perf_counter()
        p = subprocess.run(argv, capture_output=True, creationflags=rtk2.NW, timeout=120)
        sn.append(time.perf_counter() - ts)
        cik = (p.stdout + p.stderr).decode("utf-8", "replace")
    return cik, sorted(sn)[n // 2]


def anahtar(k, ham, br, konu):
    if k == "KONU": return konu
    if k == "BR": return br
    if k: return k
    import re; m = re.search(r"[\w./-]{12,}", ham); return m.group(0).rsplit("/", 1)[-1] if m else "?"  # d5: ad (yol değil) — agac biçimi yolu bölüyor, eksik() de ad arıyor


def siki(argv, ham, cikti):
    if argv[0] == "ls":
        return int(all(n in cikti for n in os.listdir(next((a for a in argv[1:] if not a.startswith("-")), "."))))
    return int(not rtk2.eksik(argv, ham, cikti))


mod = sys.argv[1]
if mod == "held4":
    assert hashlib.sha256(json.dumps(S.HELD4).encode()).hexdigest() == (t.BU / "rtk2_set4.lock").read_text().strip(), "held-out değişmiş"
if mod == "heldout":  # heldout <tohum>: heldout_uret.py üretir; tek sefer, kilit doğrulanır, kötü komut adları BASILMAZ ("egit…" tohumu hariç)
    kap = t.BU / "heldout"; liste = json.load((kap / f"rtk2_{sys.argv[2]}.json").open(encoding="utf-8"))
    assert hashlib.sha256(json.dumps(liste, ensure_ascii=False).encode()).hexdigest() == (kap / f"rtk2_{sys.argv[2]}.lock").read_text().strip(), "held-out değişmiş"
    mod = "heldout_" + sys.argv[2]
else:
    liste = {"egitim": S.EGITIM, "held4": S.HELD4}[mod]
os.chdir(t.KOK)
t.GOVDE, t.BASLIK = t.kur_baslik()
br = t.kos(["git", "branch", "--show-current"])[0].strip(); konu = t.kos(["git", "log", "-1", "--format=%s"])[0].strip()[:25]
sat = []
for ad, argv, k in liste:
    ham, _ = rtk2.calis(argv)
    o1, s1 = kos(["rtk", *argv])
    r = rtk2.tur(argv); suz = r is not None
    o2, s2 = kos(argv if r == "ham" else PY + argv) if suz else (o1, s1)  # "ham": hook komutu rtk'sız bırakır; None: rtk ile aynı komut, eşit sayılır
    ac = re.search(r" ac ([0-9a-f]{8})\s*$", o2)  # d6: özet + geri alma komutu; sinyal = özet + `ac` çıktısı (bilgi kaybolmaz)
    o2s = o2 + subprocess.run(PY + ["ac", ac.group(1)], capture_output=True, creationflags=rtk2.NW).stdout.decode("utf-8", "replace") if ac else o2
    key = anahtar(k, ham, br, konu)
    sat.append({"ad": ad, "rota": r if suz else "rtk", "ham": tk(ham), "rtk": tk(o1), "rtk2": tk(o2),
                "tohum_rtk": int(key in o1), "tohum_rtk2": int(key in o2s), "siki_rtk": siki(argv, ham, o1), "siki_rtk2": siki(argv, ham, o2s), "ac": int(bool(ac)),
                "sn_rtk": round(s1, 3), "sn_rtk2": round(s2, 3)})
top = {k: round(sum(s[k] for s in sat), 3) for k in sat[0] if k not in ("ad", "rota")}
print(mod, "n", len(sat), top, "count_tokens", t.SAYAC["say"])
if mod.startswith("heldout"):
    print("kapı: süre ≤ rtk", sum(x["sn_rtk2"] <= x["sn_rtk"] for x in sat), "/", len(sat), "· token ≤ rtk", sum(x["rtk2"] <= x["rtk"] for x in sat), "· sinyal rtk2", sum(x["tohum_rtk2"] and x["siki_rtk2"] for x in sat), "rtk", sum(x["tohum_rtk"] and x["siki_rtk"] for x in sat))
for r in sorted({x["rota"] for x in sat}):  # (c) rota tablosu: rota başına rtk2'nin dört eksendeki kazancı (komut adı basılmaz)
    z = [x for x in sat if x["rota"] == r]
    print("  rota", r, "n", len(z), "token rtk", sum(x["rtk"] for x in z), "rtk2", sum(x["rtk2"] for x in z), "· tok≤", sum(x["rtk2"] <= x["rtk"] for x in z), "· sn≤", sum(x["sn_rtk2"] <= x["sn_rtk"] for x in z),
          "· sinyal rtk2", sum(x["tohum_rtk2"] and x["siki_rtk2"] for x in z), "rtk", sum(x["tohum_rtk"] and x["siki_rtk"] for x in z), "· ac", sum(x["ac"] for x in z))
for s in sat:
    if mod.startswith("heldout") and "egit" not in mod:
        continue
    kotu = s["sn_rtk2"] > s["sn_rtk"] or s["rtk2"] > s["rtk"] or not (s["tohum_rtk2"] and s["siki_rtk2"]) or not (s["tohum_rtk"] and s["siki_rtk"])
    print("  " + ("!" if kotu else " "), s["ad"], s["rota"], {x: s[x] for x in ("ham", "rtk", "rtk2", "sn_rtk", "sn_rtk2", "tohum_rtk", "tohum_rtk2", "siki_rtk", "siki_rtk2")} if kotu else "")
json.dump({"satir": sat, "toplam": top}, open(t.BU / f"rtk2_e2e_{mod}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
