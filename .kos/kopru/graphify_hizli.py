"""GRAPHIFY-ULTRA-1 G2: hızlı artımlı yol — graphify'ın python'uyla: <GPY> graphify_hizli.py <kök>  (stdin: köke göreli değişen yollar)
graphify'ın kendi extract()'ı yalnız değişen dosyalara; graph.json BİR kez yüklenir, o dosyaların düğüm/kenarları değiştirilir,
sarkan kenarlar atılır. _rebuild_code'un 5× json.loads + tam detect() + kümeleme + html adımları atlanır (48 sn → birkaç sn).
shortcut: yeni düğümler eski kümesini (aynı id) korur, yeni id kümesiz kalır; harita/küme tazeliği için ara sıra `--tam`."""
import json, os, subprocess, sys
from pathlib import Path
from graphify.detect import _is_ignored, _load_graphifyignore
from graphify.extract import extract

r = Path(sys.argv[1]).resolve()
yok = _load_graphifyignore(r)
rel = sorted({s.replace("\\", "/") for s in sys.stdin.read().splitlines() if s and not _is_ignored(r / s, r, yok)})
var = [r / s for s in rel if (r / s).is_file()]
x = extract(var, root=r, parallel=False) if var else {}
gyol = r / "graphify-out" / "graph.json"
g = json.loads(gyol.read_text(encoding="utf-8"))
S = set(rel)
eski = {n["id"]: n for n in g["nodes"] if n.get("source_file") in S}


def goreli(o):
    sf = o.get("source_file")
    if sf and os.path.isabs(sf):
        o["source_file"] = Path(sf).resolve().relative_to(r).as_posix()
    return o


yeni = [goreli(n) for n in x.get("nodes", [])]
for n in yeni:
    if n["id"] in eski and "community" in eski[n["id"]]:
        n.setdefault("community", eski[n["id"]]["community"])
        n.setdefault("community_name", eski[n["id"]].get("community_name"))
g["nodes"] = [n for n in g["nodes"] if n.get("source_file") not in S] + yeni
ids = {n["id"] for n in g["nodes"]}
g["links"] = [e for e in [e for e in g["links"] if e.get("source_file") not in S]
              + [goreli(e) for e in x.get("edges", x.get("links", []))] if e["source"] in ids and e["target"] in ids]
bas = subprocess.run(["git", "rev-parse", "HEAD"], cwd=r, capture_output=True, text=True).stdout.strip()
if len(bas) == 40:
    g["built_at_commit"] = bas  # anahtar sırası korunur → hafif'in son-300-bayt okuması bulur
gecici = gyol.with_suffix(".hizli.tmp")
gecici.write_text(json.dumps(g, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
os.replace(gecici, gyol)
print(f"graphify_hizli: {len(rel)} dosya · düğüm -{len(eski)} +{len(yeni)} · toplam {len(g['nodes'])}/{len(g['links'])}")
