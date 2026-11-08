"""LISTE-CIKAR-1 DOGRULAMA: v3 md'lerde birden fazla ozellik maddesi olan kalemlerin her maddesini kaynak alintiyla karsilastirir;
oznesi kalem olmayan ya da alintida gecmeyen maddeleri ve 'Videoda yapılış'i siler. Kaldigi yerden surer (- dogrulama: v1 etiketi).
Kullanim: python -I tools/liste_dogrula.py [--isci K] [--parti P] [--bas N] [--ters] [--say]"""
import csv
import json
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

K = Path(r"C:\Projeler\omer-skills")
sys.path.insert(0, str(K / "tools"))
import liste_cikar as LC  # noqa: E402
import ucretsiz_havuz as H  # noqa: E402

src = (K / "tools/liste_ozellik.py").read_text(encoding="utf-8").replace("\nmain()", "\n")
LO = {}
exec(compile(src, "liste_ozellik", "exec"), LO)
LISTE = K / "docs/video-tarama/ana-liste.tsv"
YAP = K / "docs/video-tarama/yapilis"
ETIKET = "- dogrulama: v1"
ISTEM = """Asagida kalemler var. Her kalem icin: ad, videodan ALINTI ve modelin yazdigi numarali OZELLIK maddeleri ile YAPILIS metni.
Gorevin denetim: her madde icin iki soru sor: (1) Bu maddenin oznesi gercekten BU KALEM mi (videonun ana konusu olan baska arac/urun/site/listenin tamami degil)? (2) Madde alintida gecen bilgiye mi dayaniyor (uydurma yok)? Ikisi de EVET ise maddeyi TUT, degilse AT.
YAPILIS metni de ayni iki sorudan gecmezse yapilis_tut=false.
Supheli durumda AT. Yeni madde YAZMA, maddeleri degistirme; yalniz hangi numaralarin kalacagini soyle.
CIKTI yalniz JSON dizisi: [{"ad":"<kalem adi aynen>","tut":[1,2],"yapilis_tut":true}]

"""


def maddeler(t):
    oz = t.split("## Özellikler", 1)[1].split("\n## ", 1)[0]
    return [l[2:].strip() for l in oz.splitlines() if l.startswith("- ")]


def yapilis(t):
    return t.split("## Videoda yapılış", 1)[1].split("\n## ", 1)[0].strip() if "## Videoda yapılış" in t else "-"


def yaz(p, t, tut, yap_tut):
    ms = maddeler(t)
    kalan = [m for i, m in enumerate(ms, 1) if i in tut] or ["Alıntıda bu kalem anlatılmıyor"]
    bas, kalan_t = t.split("## Özellikler", 1)
    son = kalan_t.split("\n## ", 1)[1]
    yeni = bas.replace("- kural: v3\n", f"- kural: v3\n{ETIKET}\n") + "## Özellikler\n" + "\n".join(f"- {m}" for m in kalan) + "\n\n## " + son
    if not yap_tut:
        yeni = re.sub(r"(## Videoda yapılış\n)(.*?)(\n\n## )", r"\1-\3", yeni, count=1, flags=re.S)
    p.write_text(yeni, encoding="utf-8")
    return len(ms) - len([m for i, m in enumerate(ms, 1) if i in tut])


def main():
    a = sys.argv[1:]
    g = lambda k, v: int(a[a.index(k) + 1]) if k in a else v
    csv.field_size_limit(10**7)
    rows = list(csv.DictReader(open(LISTE, encoding="utf-8", newline=""), delimiter="\t"))
    rows.sort(key=lambda r: r["kalem"], reverse="--ters" in a)
    is_ = []
    for r in rows:
        p = YAP / (LO["guvenli"](r["kalem"]) + ".md")
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8", errors="ignore")
        if "- kural: v3" in t and ETIKET not in t and len(maddeler(t)) >= 2:
            is_.append((r, p))
    if "--say" in a:
        print("dogrulanacak", len(is_))
        return
    if "--ad" in a:
        sec = set(a[a.index("--ad") + 1].split("|"))
        is_ = [x for x in is_ if x[0]["kalem"] in sec]
    is_ = is_[g("--bas", 0):]
    dos = LC.dosyalar()
    parti = g("--parti", 8)
    partiler = [is_[i:i + parti] for i in range(0, len(is_), parti)]
    say, atilan, kilit = [0], [0], threading.Lock()

    def calis(p):
        canli = [(r, f) for r, f in p if ETIKET not in f.read_text(encoding="utf-8", errors="ignore")]
        if not canli:
            return
        blok = []
        for r, f in canli:
            t = f.read_text(encoding="utf-8", errors="ignore")
            ms = "\n".join(f"{i}. {m}" for i, m in enumerate(maddeler(t), 1))
            blok.append(f"### {r['kalem']}\nALINTI: {LO['baglam'](r['kalem'], r['kaynak_video_idleri'].split(','), dos)}\nOZELLIK:\n{ms}\nYAPILIS: {yapilis(t)[:600]}")
        istem = ISTEM + "\n\n".join(blok)
        arr = None
        for den in range(4):
            try:
                y = H._haiku(istem)
                met = re.sub(r"^```\w*|```$", "", (y or "").strip(), flags=re.M).strip()
                arr = json.loads(met[met.index("["):met.rindex("]") + 1])
                break
            except Exception as e:
                time.sleep(15 * (den + 1))
                son = f"{type(e).__name__} {str(e)[:60]}"
        if arr is None:
            print("hata", canli[0][0]["kalem"], son, flush=True)
            return
        by = {x.get("ad"): x for x in arr if isinstance(x, dict)}
        with kilit:
            for r, f in canli:
                x = by.get(r["kalem"])
                if not x or not isinstance(x.get("tut"), list):
                    continue
                t = f.read_text(encoding="utf-8", errors="ignore")
                atilan[0] += yaz(f, t, {int(i) for i in x["tut"] if str(i).isdigit()}, bool(x.get("yapilis_tut", True)))
                say[0] += 1
            if say[0] % 50 < parti:
                print("kalem", say[0], "atilan madde", atilan[0], flush=True)

    with ThreadPoolExecutor(g("--isci", 4)) as ex:
        list(ex.map(calis, partiler))
    print("bitti", say[0], "/", len(is_), "atilan madde", atilan[0])


main()
