"""BUL-KUR-2 adim 3 yargi: tmp/bk2/{reg,gh,gh-a,gh-b,hf}.tsv adaylarini ucretsiz havuzla hukme baglar -> docs/video-tarama/kurulum-coz-6.tsv
Ayni kalem tekrar islenmez. Haiku tavani 300 parti (havuz sonu), Sonnet yargic yok (havuz 'zor' turu en cok 40 parti)."""
import csv, json, os, re, sys, threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import ucretsiz_havuz as H
csv.field_size_limit(10**7)
R = Path(__file__).resolve().parents[1]
B = R / "tmp/bk2"
def tsv(p):
    try: return [l.rstrip("\n").split("\t") for l in open(p, encoding="utf-8")]
    except Exception: return []
items = list(csv.DictReader(open(B / "items.tsv", encoding="utf-8"), delimiter="\t"))
SIN = sys.argv[1] if len(sys.argv) > 1 else ""  # MODEL | DIGER | bos = hepsi
if SIN == "MODEL": items = [i for i in items if i["sinif"] == "MODEL"]
elif SIN == "DIGER": items = [i for i in items if i["sinif"] != "MODEL"]
cand = {}
def ekle(k, kaynak, puan, acik):
    cand.setdefault(k, {})[kaynak] = (puan, acik)
for x in tsv(B / "reg.tsv"):
    if len(x) >= 5 and x[1] != "-" and float(x[3]) >= 0.9: ekle(x[0], f"{x[1]}:{x[2]}", float(x[3]), x[4][:110])
for f in ("gh.tsv", "gh-a.tsv", "gh-b.tsv", "gh-c.tsv"):
    for x in tsv(B / f):
        if len(x) >= 3 and x[1] != "-":
            try: ekle(x[0], x[1], float(x[2]), (x[4] if len(x) > 4 else "")[:110])
            except ValueError: pass
for x in tsv(B / "hf.tsv"):
    if len(x) >= 3 and x[1] != "-": ekle(x[0], "hf:" + x[2], float(x[1]), f"indirme {x[3] if len(x)>3 else ''} lisans {x[5] if len(x)>5 else ''}")
for x in tsv(B / "winget.tsv"):
    if len(x) >= 3 and x[1] not in ("-", "HATA"): ekle(x[0], x[1], float(x[2]), (x[3] if len(x) > 3 else "")[:110])
# bilinen repo linki (ana-liste) dogrudan aday
for it in items:
    m = re.search(r"github\.com/([\w.-]+)/([\w.-]+)", it["link"] or "")
    if m: ekle(it["kalem"], "gh:" + m.group(1) + "/" + m.group(2), 0.95, "ana-listedeki repo linki")
CIK = R / "docs/video-tarama/kurulum-coz-6.tsv"
bit = {r["kalem"] for r in csv.DictReader(open(CIK, encoding="utf-8"), delimiter="\t")} if CIK.exists() else set()
KIL = threading.Lock()
ISTEM = """Her kalem bir videoda gecen arac/model adidir (OCR hatali olabilir). Altindaki adaylardan hangisi AYNI urun mu karar ver.
DOGRULANDI = aday acikca ayni urun (ad + islev uyumlu). ADAY = buyuk olasilikla ayni ama emin degil. YOK = hicbiri ayni urun degil (ad cakismasi, ilgisiz, baska islev).
Ad benzerligi tek basina yetmez: aciklama kalemin turuyle uyusmali. Uydurma yok.
YALNIZ JSON dizi: [{"i":0,"karar":"YOK","secim":-1,"puan":0.0,"neden":"kisa"}] secim = aday sirasi (0'dan) ya da -1. Her i bir kez.
"""
def isle(parti):
    t = ISTEM
    for i, (it, c) in enumerate(parti):
        t += f"\n{i}: {it['kalem']} | tur {it['sinif']} | video-baglami: {it.get('ctx','')}\n" + "".join(f"   [{j}] {a} ({p}) {d}\n" for j, (a, (p, d)) in enumerate(c))
    for tur in ("orta", "zor", "orta"):
        m, mdl, _ = H.cagir(tur, t, max_tokens=5000, zaman=150, etiket="bk2-yargi", haiku_tavan=60)
        try:
            j = json.loads(re.search(r"\[.*\]", m, re.S).group(0))
            if {x.get("i") for x in j if isinstance(x, dict)} == set(range(len(parti))):
                out = []
                for x in j:
                    it, c = parti[x["i"]]
                    s = x.get("secim", -1)
                    kay = c[s][0] if isinstance(s, int) and 0 <= s < len(c) else ""
                    k = x.get("karar", "YOK")
                    if k not in ("DOGRULANDI", "ADAY", "YOK"): k = "YOK"
                    if k != "YOK" and not kay: k = "YOK"
                    out.append((it["kalem"], it["sinif"], k, kay, x.get("puan", 0), "", str(x.get("neden", ""))[:160].replace("\t", " ") + f" [{mdl}]"))
                return out
        except Exception: pass
    return []
def main():
    yeni = not CIK.exists()
    f = open(CIK, "a", encoding="utf-8", newline=""); w = csv.writer(f, delimiter="\t")
    if yeni: w.writerow(["kalem", "sinif", "sonuc", "kaynak", "puan", "yol", "gerekce"])
    todo = []
    for it in items:
        if it["kalem"] in bit: continue
        c = sorted(cand.get(it["kalem"], {}).items(), key=lambda a: -a[1][0])[:6]
        if not c:
            sc = "arama yapilmadi" if it["sinif"] == "MODEL" else "hicbir yolda aday cikmadi"
            w.writerow([it["kalem"], it["sinif"], "YOK", "-", 0, "-", sc]); continue
        todo.append((it, c))
    f.flush()
    print("yargilanacak", len(todo), flush=True)
    P = [todo[i:i + 25] for i in range(0, len(todo), 25)]
    with ThreadPoolExecutor(3) as ex:
        for s in ex.map(isle, P):
            with KIL: w.writerows(s); f.flush()
    print("BITTI", flush=True)
if __name__ == "__main__": main()
