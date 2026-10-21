"""d19 kapısı: mem2 (B) vs mem2+anahtar yan dizini (N). Held-out tohumla; soru içeriği stdout'a basılmaz.
Kullanım: python -I mem_anahtar_ab.py <tohum> [n=40]
  TR->EN: Türkçe soru, İngilizce kayıt · EN->TR: İngilizce soru, Türkçe kayıt (havuz çapraz dilde yeniden ifade eder; anahtar = kayıt id, ilk 5)
  anahtar: mem_ab ile aynı (aynı dil 3 başlık / 4 anlatı sözcüğü) · süre: arama başına ortalama (süreç içi)."""
import json
import os
import random
import re
import sqlite3
import sys
import time

AD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AD)
sys.path.insert(0, os.path.join(AD, "..", "..", "..", "tools"))
import mem2  # noqa: E402
import mem_anahtar as MA  # noqa: E402
import ucretsiz_havuz as H  # noqa: E402

tohum, n = int(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 40
rnd = random.Random(tohum)
c = sqlite3.connect("file:" + mem2.DB + "?mode=ro", uri=True)
satir = c.execute("SELECT id,title,subtitle,narrative FROM observations WHERE project='omer-skills' AND length(narrative)>300 AND id<(SELECT max(id) FROM observations)-5").fetchall()
TRK = re.compile(r"[çğıöşüÇĞİÖŞÜ]")


def tr(r):
    return bool(TRK.search(" ".join(x or "" for x in r[1:3])))


def yeniden(parca, hedef):
    ist = ("Aşağıdaki numaralı satırlar birer iş günlüğü kaydı. Her biri için, geliştiricinin o kaydı geri bulmak için yazacağı KISA %s soruyu yaz "
           "(en çok 12 sözcük): kayıt başlığındaki sözcükleri birebir kopyalama, eş anlamlı/dolaylı anlat, dosya adı uydurma. "
           "Çıktı yalnız sorular, aynı sırayla, numarasız.\n" % hedef
           + "\n".join(f"{k + 1}. {(r[1] or '')[:90]} — {(r[3] or '')[:260]}".replace("\n", " ") for k, r in enumerate(parca)))
    y, kay, _ = H.cagir("ozet", ist, max_tokens=1200, haiku_tavan=0, etiket="mem-anahtar",
                        dogrula=lambda m: None if len([l for l in m.strip().splitlines() if l.strip()]) == len(parca) else "satır sayısı")
    return ([l.strip().lstrip("0123456789.) ") for l in y.strip().splitlines() if l.strip()]) if y else None


def olc(f, q):
    t = time.time()
    r = f(q)
    return [x[0] for x in r], time.time() - t


def ozet(L):
    return {"n": len(L), "B": round(sum(x["B"] for x in L) / max(1, len(L)), 3), "N": round(sum(x["N"] for x in L) / max(1, len(L)), 3),
            "sB": round(sum(x["sB"] for x in L) / max(1, len(L)), 4), "sN": round(sum(x["sN"] for x in L) / max(1, len(L)), 4)}


def kol(q, i):
    b, sb = olc(lambda s: mem2.ara(s, 5), q)
    nn, sn = olc(lambda s: MA.ara(s, 5), q)
    return {"B": int(i in b), "N": int(i in nn), "sB": sb, "sN": sn}


R = {"tohum": tohum}
for ad, kaynak_tr, hedef in (("TR->EN", False, "Türkçe"), ("EN->TR", True, "İngilizce")):
    havuz = [r for r in satir if tr(r) == kaynak_tr]
    secim = rnd.sample(havuz, min(n, len(havuz)))
    S, atlanan = [], 0
    for k in range(0, len(secim), 10):
        parca = secim[k:k + 10]
        sor = yeniden(parca, hedef)
        if not sor:
            atlanan += len(parca)
            continue
        S += [kol(q, r[0]) for r, q in zip(parca, sor)]
    R[ad] = dict(ozet(S), atlanan=atlanan, kayit_dili="TR" if kaynak_tr else "EN")


def sozcuk(s):
    return list(dict.fromkeys(w for w in re.findall(r"[^\W\d_]{5,}", (s or "").lower())))


K = []
for r in rnd.sample(satir, n):
    wb = sozcuk(r[1])
    wa = [w for w in sozcuk(r[3]) if w not in wb]
    if len(wb) >= 3:
        K.append(kol(" ".join(rnd.sample(wb, 3)), r[0]))
    if len(wa) >= 4:
        K.append(kol(" ".join(rnd.sample(wa, 4)), r[0]))
R["anahtar"] = ozet(K)
print(json.dumps(R, indent=1))
json.dump(R, open(os.path.join(AD, "mem_anahtar_ab_%d.json" % tohum), "w", encoding="utf-8"), indent=1)
