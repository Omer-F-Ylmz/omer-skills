"""VIDEO-HIZ-4 ölçüm: liste (40 shorts + 10 uzun örnek), kos (süre + VRAM/GPU/RAM tepe), karsi (kalite kapısı).
Kullanım: video_hiz4_olc.py liste | kos <ad> [--es N] [--liste dosya] | karsi <ad>
Referans = docs/video-tarama/derin (eski large-v3 beam5, tüm kare OCR)."""
import difflib
import json
import os
import re
import subprocess
import sys
import threading
import time
from collections import Counter
from pathlib import Path

import psutil

KOK = Path(__file__).resolve().parents[1]
REF = KOK / "docs/video-tarama/derin"
D = KOK / ".kos/kopru/ogren/hiz4"
NW = 0x08000000


def liste(kisa=40, uzun=10):
    sh, lg = [], []
    for f in sorted(REF.glob("*.json")):
        try:
            j = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        s = (j.get("meta") or {}).get("sure")
        if not s or "youtu" not in j["url"]:
            continue
        (sh if s <= 90 else lg if 120 <= s <= 600 else []).append((hash(j["kod"]) and sum(map(ord, j["kod"])) * 7919 % 10007, j["url"]))
    D.mkdir(parents=True, exist_ok=True)
    sec = [u for _, u in sorted(sh)[:kisa]], [u for _, u in sorted(lg)[:uzun]]
    (D / "kisa.txt").write_text("\n".join(sec[0]) + "\n", encoding="utf-8")
    (D / "uzun.txt").write_text("\n".join(sec[1]) + "\n", encoding="utf-8")
    print(len(sec[0]), len(sec[1]))


def tepe(dur, out):
    while not dur.is_set():
        try:
            u, m = subprocess.run(["nvidia-smi", "--query-gpu=utilization.gpu,memory.used", "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=10, creationflags=NW).stdout.split(",")
            out["gpu"] = max(out["gpu"], float(u)); out["vram"] = max(out["vram"], float(m) / 12282 * 100)
        except Exception:
            pass
        out["ram"] = max(out["ram"], psutil.virtual_memory().percent)
        time.sleep(1)


def kos(ad, a):
    es = a[a.index("--es") + 1] if "--es" in a else "8"
    liste_ = a[a.index("--liste") + 1] if "--liste" in a else str(D / "kisa.txt")
    cikti = D / ad
    cikti.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "VD_CIKTI": str(cikti)}
    out, dur = {"gpu": 0.0, "vram": 0.0, "ram": 0.0}, threading.Event()
    th = threading.Thread(target=tepe, args=(dur, out), daemon=True); th.start()
    t0 = time.time()
    r = subprocess.run([sys.executable, str(KOK / "tools/video_derin.py"), "--es", es, "--liste", liste_], env=env, capture_output=True, text=True, creationflags=NW)
    sure = time.time() - t0
    dur.set()
    (cikti / "_log.txt").write_text(r.stdout + "\n" + r.stderr[-3000:], encoding="utf-8")
    n = len(list(cikti.glob("*.json")))
    ist = len([u for u in Path(liste_).read_text(encoding="utf-8").split()])
    sonuc = {"ad": ad, "es": es, "istenen": ist, "json": n, "sure_sn": round(sure), "sn_link": round(sure / max(1, n), 1), "saat_basi": round(3600 * n / sure), **{k: round(v) for k, v in out.items()}}
    (cikti / "_olcum.json").write_text(json.dumps(sonuc), encoding="utf-8")
    print(json.dumps(sonuc))


def kel(j):
    return re.sub(r"[^\w\s]", "", " ".join(s["t"] for s in j["transkript"]).lower()).split()


_ST = None


def dur_sozcukler():
    global _ST
    if _ST is None:
        c = Counter()
        for f in list(REF.glob("*.json"))[:600]:
            j = json.loads(f.read_text(encoding="utf-8"))
            c.update(set(t for t in tokens(" ".join(e["t"] for e in j["ekran"]) + " " + str(j.get("kare_aciklama") or ""))))
        _ST = {w for w, _ in c.most_common(300)}
    return _ST


def tokens(s):
    return [t for t in re.findall(r"[a-zçğıöşü0-9][\w.\-/@]{2,}", s.lower()) if re.search(r"[a-zçğıöşü]", t)]


def karsi(ad):
    y_d = D / ad
    st = dur_sozcukler()
    sat = []
    for p in sorted(y_d.glob("*.json")):
        if p.name.startswith("_"):
            continue
        e, y = json.loads((REF / p.name).read_text(encoding="utf-8")), json.loads(p.read_text(encoding="utf-8"))
        ke, ky = kel(e), kel(y)
        asr = difflib.SequenceMatcher(None, ke, ky, autojunk=False).ratio() if ke or ky else 1.0
        # öğe geri çağırımı: referansın ekran(OCR)+kare açıklama jetonları (yaygın 300 sözcük hariç) yeni çıktının herhangi bir alanında var mı
        yeni = set(tokens(" ".join(x["t"] for x in y["ekran"]) + " " + str(y.get("kare_aciklama") or "") + " " + " ".join(s["t"] for s in y["transkript"]) + " " + " ".join(y["linkler"] + y["komutlar"])))
        ref_oge = {t for t in tokens(" ".join(x["t"] for x in e["ekran"]) + " " + str(e.get("kare_aciklama") or "")) if t not in st}
        rec = len(ref_oge & yeni) / len(ref_oge) if ref_oge else 1.0
        ocr_ref = {t for t in tokens(" ".join(x["t"] for x in e["ekran"])) if t not in st}
        yeni_ocr = set(tokens(" ".join(x["t"] for x in y["ekran"])))
        rec_ocr = len(ocr_ref & yeni_ocr) / len(ocr_ref) if ocr_ref else 1.0
        le, ly = set(e["linkler"] + e["komutlar"]), set(y["linkler"] + y["komutlar"])
        lk = len(le & ly) / len(le) if le else 1.0
        sat.append((p.stem, asr, rec, rec_ocr, lk, y.get("asr", {}).get("kaynak")))
        print(f"{p.stem}\tasr {asr:.3f}\toge_rec {rec:.3f}\tocr_rec {rec_ocr:.3f}\tlink_komut {lk:.2f}\t{sat[-1][5]}")
    n = max(1, len(sat))
    print(f"N={len(sat)} asr_ort {sum(s[1] for s in sat) / n:.3f} asr>=0.96 {sum(s[1] >= 0.96 for s in sat)}/{len(sat)} oge_rec_ort {sum(s[2] for s in sat) / n:.3f} ocr_rec_ort {sum(s[3] for s in sat) / n:.3f} link_komut_tam {sum(s[4] >= 1 for s in sat)}/{len(sat)}")


if __name__ == "__main__":
    c = sys.argv[1]
    {"liste": lambda: liste(), "kos": lambda: kos(sys.argv[2], sys.argv[3:]), "karsi": lambda: karsi(sys.argv[2])}[c]()
