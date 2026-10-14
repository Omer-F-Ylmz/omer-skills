"""GRAPHIFY-ULTRA-1 G1: grep doğrulamalı soru seti → graphify query isabeti.
python graphify_ultra_g1.py [--budget 400]  → docs/kutuphane/olcum/graphify-ultra-g1.tsv + özet satırları
Soru tipleri: tanım (X nerede tanımlı) · çağıran (X'i kim çağırıyor) · modül (Z ne yapar) · md (SKILL.md başlığı).
Alt doğruluk grep'ten: sembol tek dosyada tanımlı; çağıran = adı geçen başka dosya. İsabet = beklenen yol çıktıda."""
import json, random, re, subprocess, sys
from collections import defaultdict
from pathlib import Path

BUTCE = sys.argv[sys.argv.index("--budget") + 1] if "--budget" in sys.argv else "400"
KOKLER = [("omer-skills", Path("C:/Projeler/omer-skills"), {"tanim": 4, "cagiran": 4, "modul": 2, "md": 2}),
          ("TELVE", Path("C:/Users/pc/Desktop/TELVE"), {"tanim": 3, "cagiran": 3, "modul": 2})]
TANIM = {".py": r"^\s*(?:async\s+)?(?:def|class)\s+([A-Za-z_]\w{5,})",
         ".js": r"(?:function\s+|class\s+|(?:const|let)\s+)([A-Za-z_]\w{5,})\s*(?:=\s*(?:async\s*)?\(|\(|\{|extends)",
         ".cs": r"(?:class|interface|record|void|Task<?\w*>?)\s+([A-Z]\w{5,})"}
TANIM[".ts"] = TANIM[".mjs"] = TANIM[".js"]


def dosyalar(kok):
    yollar = subprocess.run(["git", "ls-files"], cwd=kok, capture_output=True, text=True, encoding="utf-8").stdout.splitlines()
    return [y for y in yollar if Path(y).suffix in TANIM or y.endswith("SKILL.md")]


def graf_dosyalari(kok):
    g = json.loads((kok / "graphify-out/graph.json").read_text(encoding="utf-8"))
    return {n.get("source_file") for n in g["nodes"]}, {n.get("label", "").rstrip("()") for n in g["nodes"]}


def sorular(kok, kotalar, rnd):
    yollar = dosyalar(kok)
    metin = {y: (kok / y).read_text(encoding="utf-8", errors="replace") for y in yollar if (kok / y).is_file()}
    tanim = defaultdict(set)
    for y, m in metin.items():
        if Path(y).suffix in TANIM:
            for ad in re.findall(TANIM[Path(y).suffix], m, re.M):
                tanim[ad].add(y)
    tek = sorted(ad for ad, ys in tanim.items() if len(ys) == 1 and not ad.startswith("test"))
    rnd.shuffle(tek)
    s = []
    for ad in tek:
        y = next(iter(tanim[ad]))
        if sum(1 for q in s if q[0] == "tanim") < kotalar.get("tanim", 0):
            s.append(("tanim", f"{ad} nerede tanımlı", {y}))
            continue
        if sum(1 for q in s if q[0] == "cagiran") < kotalar.get("cagiran", 0):
            cag = {z for z, m in metin.items() if z != y and re.search(rf"\b{ad}\b", m)}
            if cag:
                s.append(("cagiran", f"{ad} fonksiyonunu kim çağırıyor", cag))
    kod = [y for y in metin if Path(y).suffix in TANIM and len(Path(y).stem) >= 5 and not Path(y).stem.startswith("test")]
    for y in rnd.sample(kod, kotalar.get("modul", 0)):
        s.append(("modul", f"{Path(y).stem} modülü ne yapar", {y}))
    md = [y for y in metin if y.endswith("SKILL.md")]
    for y in rnd.sample(md, min(len(md), kotalar.get("md", 0))):
        bas = re.findall(r"^#{1,2} (.+)", metin[y], re.M)
        if bas:
            s.append(("md", f"{bas[0].strip()} skill'i", {y}))
    return s


rnd = random.Random(14)
satirlar, ozet = ["kok\ttip\tsoru\tisabet\tsinif\tsatir\tkelime\tbeklenen"], []
for ad, kok, kota in KOKLER:
    gdos, gad = graf_dosyalari(kok)
    isa = 0
    ss = sorular(kok, kota, rnd)
    for tip, soru, bek in ss:
        komut = ([sys.executable, str(Path(__file__).with_name("graphify_sor.py")), soru, "--kok", str(kok)] if "--sor" in sys.argv
                 else ["graphify", "query", soru, "--budget", BUTCE])
        cik = subprocess.run(komut, cwd=kok, capture_output=True,
                             text=True, encoding="utf-8", errors="replace").stdout
        hit = any(b in cik for b in bek)
        isa += hit
        sinif = "" if hit else ("grafta-yok" if not (bek & gdos) else
                                "sembol-yok" if tip in ("tanim", "cagiran") and soru.split()[0] not in gad else "siralama")
        satirlar.append(f"{ad}\t{tip}\t{soru}\t{int(hit)}\t{sinif}\t{len(cik.splitlines())}\t{len(cik.split())}\t{';'.join(sorted(bek))[:200]}")
    ozet.append(f"{ad}: {isa}/{len(ss)}")
Path("C:/Projeler/omer-skills/docs/kutuphane/olcum/graphify-ultra-g1" + ("-sor" if "--sor" in sys.argv else "") + ".tsv").write_text("\n".join(satirlar) + "\n", encoding="utf-8")
print(" · ".join(ozet), f"(budget {BUTCE})")
for s in satirlar[1:]:
    p = s.split("\t")
    if p[3] == "0":
        print("KAÇAK", p[0], p[1], p[2][:60], p[4], p[7][:80])
