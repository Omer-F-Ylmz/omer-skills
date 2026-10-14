"""GRAPHIFY-ULTRA-1 G1/G3: kompakt graf sorusu — python graphify_sor.py "<soru>" [--kok <dizin>]
Sorudaki tanımlayıcı/dosya adları graph.json etiketlerinde birebir aranır: sembol · dosya:satır · 1 satır özet
+ çağıranlar/içerik (≤40 satır). Birebir yoksa git grep tanımı, o da yoksa `graphify query --budget 400`.
Neden: `graphify query` Türkçe soru kelimeleriyle ("nerede", "ne yapar") alakasız düğümlere dağılıyordu (G1 kaçak sınıfı 'siralama')."""
import json, re, subprocess, sys
from collections import defaultdict
from pathlib import Path

arg = sys.argv[1:]
kok = Path(arg[arg.index("--kok") + 1]) if "--kok" in arg else Path.cwd()
soru = arg[0]
g = json.loads((kok / "graphify-out/graph.json").read_text(encoding="utf-8"))
dug = {n["id"]: n for n in g["nodes"]}
ada = defaultdict(list)
for n in g["nodes"]:
    if n.get("file_type") != "rationale":
        e = n.get("label", "").rstrip("()")
        ada[e].append(n)
        if "." in e and n.get("source_location") == "L1":
            ada[e.rsplit(".", 1)[0]].append(n)  # dosya düğümü uzantısız da bulunur
gelen, giden = defaultdict(list), defaultdict(list)
for e in g["links"]:
    gelen[e["target"]].append(e)
    giden[e["source"]].append(e)


def yer(n):
    return f"{n.get('source_file')}:{n.get('source_location', '')}"


def ozet(n):
    r = [dug[e["source"]]["label"] for e in gelen[n["id"]] if e["relation"] == "rationale_for" and e["source"] in dug]
    return r[0].splitlines()[0][:90] if r else ""


cikti = []
belirtec = [t for t in dict.fromkeys(re.findall(r"[A-Za-z_][\w.\-]{3,}", soru)) if t in ada]
for t in belirtec:
    for n in ada[t][:3]:
        cikti.append(f"{n['label']} · {yer(n)} · {ozet(n)}".rstrip(" ·"))
        cag = sorted({f"{e.get('source_file')}:{e.get('source_location', '')}" for e in gelen[n["id"]]
                      if e["relation"] in ("calls", "indirect_call", "imports", "imports_from", "references")})
        if cag:
            cikti.append(f"  çağıran ({len(cag)}): " + " ".join(cag[:8]))
        ic = [dug[e["target"]]["label"] for e in giden[n["id"]] if e["relation"] in ("contains", "method") and e["target"] in dug]
        if ic:
            cikti.append(f"  içerir ({len(ic)}): " + " ".join(ic[:12]))
if not cikti:
    for t in dict.fromkeys(re.findall(r"[A-Za-z_]\w{3,}", soru)):
        r = subprocess.run(["git", "grep", "-n", "-I", "-E", rf"(def|class|function|const|let|var)\s+{t}\b"],
                           cwd=kok, capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
        cikti += [f"grep: {s[:150]}" for s in r.splitlines()[:5]]
if not cikti:
    r = subprocess.run(["graphify", "query", soru, "--budget", "400"], cwd=kok, capture_output=True,
                       text=True, encoding="utf-8", errors="replace").stdout
    cikti = [s for s in r.splitlines() if not s.lstrip().startswith("warning")]
print("\n".join(cikti[:40]))
