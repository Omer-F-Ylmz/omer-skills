"""RUFLO-2 d1 TABAN: mevcut ders sisteminin 4 ekseni (kalite · token · performans · kapsam). Salt okuma, ücretsiz."""
import collections
import json
import re
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, "C:/Projeler/omer-skills/tools/ogrenme")
import ders  # noqa: E402

D = Path("C:/Projeler/omer-skills/.kos/ogrenme")


def jl(ad):
    p = D / ad
    return [json.loads(s) for s in p.read_text(encoding="utf-8").splitlines() if s.strip()] if p.exists() else []


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    log = (D / "kanca.log").read_text(encoding="utf-8")
    puan = [float(x) for m in re.findall(r"karma \[([^\]]*)\]", log) for x in m.split(",") if x.strip()]
    hata = len(re.findall(r"damıtma: ", log))
    print(f"KALİTE karma n={len(puan)} sıfır=%{100 * sum(p == 0 for p in puan) / max(len(puan), 1):.0f} >0 ort={statistics.mean([p for p in puan if p > 0] or [0]):.1f} damıtma_hata={hata}")
    dd = ders.oku()
    akt = [x for x in dd if x["durum"] == "aktif"]
    kul = [x for x in akt if x["kullanim"]]
    print(f"  ders n={len(dd)} aktif={len(akt)} kullanılan={len(kul)} kullanılan'da yardım oranı={sum(x['yardim'] for x in kul) / max(sum(x['kullanim'] for x in kul), 1):.2f}"
          f" hiç yardım etmemiş (kullanım≥2)={sum(1 for x in kul if x['kullanim'] >= 2 and not x['yardim'])}")
    print("  ajan dağılımı:", dict(collections.Counter(x["ajan"] for x in akt).most_common(6)))
    gt = jl("getirme.jsonl")
    print(f"KAPSAM getirme n={len(gt)} kapsam={dict(collections.Counter(g['ajan'] for g in gt).most_common(6))}")
    ornek = [("*", "rapor yaz test dosyası python kod"), ("video-tarayici", "video rapor kare paket"), ("general-purpose", "python test dosyası düzelt kod"), ("claude", "ana oturum görev")]
    for ajan, g in ornek:
        t = []
        for _ in range(5):
            t0 = time.perf_counter()
            blok, ids = ders.getir(ajan, g, kosu="taban-olcum")
            t.append((time.perf_counter() - t0) * 1000)
        print(f"TOKEN/PERF ajan={ajan!r} ders={len(ids)} blok≈{len(blok) // 4} jeton getirme={statistics.median(t):.0f} ms")
