"""d21 kapısı: claude-mem 'code--anahtar' modu (kayıt başlığında ' | TR: ... | EN: ...') canlı aramada (mem2.ara) çalışıyor mu.
Yalnız işaretli kayıtlar. Kullanım: python -I mem_anahtar_isaretli.py <tohum> [n=40]
  TR->EN: Türkçe soru, anlatısı İngilizce kayıt · EN->TR: tersi · anahtar: aynı dil, başlık 3 / anlatı 4 sözcük · süre: arama başına ort."""
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
import ucretsiz_havuz as H  # noqa: E402

tohum, n = int(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 40
rnd = random.Random(tohum)
c = sqlite3.connect("file:" + mem2.DB + "?mode=ro", uri=True)
satir = c.execute("SELECT id,title,subtitle,narrative FROM observations WHERE project='omer-skills' AND subtitle LIKE '%| TR:%' "
                  "AND length(narrative)>300 AND id<(SELECT max(id) FROM observations)-5").fetchall()
TRK = re.compile(r"[çğıöşüÇĞİÖŞÜ]")


def tr(r):
    return bool(TRK.search(r[3] or ""))


def yeniden(parca, hedef):
    ist = ("Aşağıdaki numaralı satırlar birer iş günlüğü kaydı. Her biri için, geliştiricinin o kaydı geri bulmak için yazacağı KISA %s soruyu yaz "
           "(en çok 12 sözcük): kayıt başlığındaki sözcükleri birebir kopyalama, eş anlamlı/dolaylı anlat, dosya adı uydurma. "
           "Çıktı yalnız sorular, aynı sırayla, numarasız.\n" % hedef
           + "\n".join(f"{k + 1}. {(r[1] or '')[:90]} — {(r[3] or '')[:260]}".replace("\n", " ") for k, r in enumerate(parca)))
    y, kay, _ = H.cagir("ozet", ist, max_tokens=1200, haiku_tavan=0, etiket="mem-isaretli",
                        dogrula=lambda m: None if len([l for l in m.strip().splitlines() if l.strip()]) == len(parca) else "satır sayısı")
    return ([l.strip().lstrip("0123456789.) ") for l in y.strip().splitlines() if l.strip()]) if y else None


AG = tuple(int(x) for x in os.environ.get("AG", "").split(",")) if os.environ.get("AG") else mem2.AGIRLIK


def kol(q, i):
    t = time.time()
    b = [x[0] for x in mem2.ara(q, 5, ag=AG)]
    return {"N": int(i in b), "s": time.time() - t}


def ozet(L):
    return {"n": len(L), "isabet": round(sum(x["N"] for x in L) / max(1, len(L)), 3), "sn": round(sum(x["s"] for x in L) / max(1, len(L)), 4)}


def sozcuk(s):
    return list(dict.fromkeys(w for w in re.findall(r"[^\W\d_]{5,}", (s or "").lower())))


R = {"tohum": tohum, "isaretli_kayit": len(satir)}
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
    R[ad] = dict(ozet(S), havuz=len(havuz), atlanan=atlanan)
K = []
for r in rnd.sample(satir, min(n, len(satir))):
    wb = sozcuk(r[1])
    wa = [w for w in sozcuk(r[3]) if w not in wb]
    if len(wb) >= 3:
        K.append(kol(" ".join(rnd.sample(wb, 3)), r[0]))
    if len(wa) >= 4:
        K.append(kol(" ".join(rnd.sample(wa, 4)), r[0]))
R["anahtar"] = ozet(K)
print(json.dumps(R, indent=1))
json.dump(R, open(os.path.join(AD, "mem_anahtar_isaretli_%d_%s.json" % (tohum, "-".join(map(str, AG)))), "w", encoding="utf-8"), indent=1)
