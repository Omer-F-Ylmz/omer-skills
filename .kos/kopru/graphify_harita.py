"""GRAPHIFY-ULTRA-1 G3: proje haritası ≤800 jeton — python graphify_harita.py [kök]  → .kos/kopru/harita/<kök adı>.md
Küme başına tek satır (en büyük 25: ortak dizin · düğüm · en çok bağlı 3 sembol), giriş noktaları (en çok çağrılan),
sıcak dosyalar (git son 7 gün). Graf değişince graphify_hafif sonrası yeniden koşulur; ajan keşfe buradan başlar.
shortcut: küme etiketi ortak dizinden türetilir (ücretsiz model etiketi yok), etiket kalitesi yetmezse OmniRoute taslağı."""
import json, os, subprocess, sys
from collections import Counter, defaultdict
from pathlib import Path

kok = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
g = json.loads((kok / "graphify-out/graph.json").read_text(encoding="utf-8"))
derece = Counter()
for e in g["links"]:
    if e["relation"] in ("calls", "imports", "imports_from", "references"):
        derece[e["target"]] += 1
kume = defaultdict(list)
for n in g["nodes"]:
    if n.get("file_type") == "code" and n.get("source_file"):
        kume[n.get("community")].append(n)
s = [f"# HARİTA · {kok.name} · {len(g['nodes'])} düğüm · commit {str(g.get('built_at_commit', ''))[:8]}",
     "Keşif: bu harita → `python .kos/kopru/graphify_sor.py \"<sembol/dosya>\"` → Read offset/limit (~20 satır).", "## Kümeler"]
for k, ns in sorted(kume.items(), key=lambda kv: -len(kv[1]))[:25]:
    dizin = Counter(os.path.dirname(n["source_file"]) or "." for n in ns).most_common(1)[0][0]  # commonpath çoğu kümede "." veriyordu
    ust = [n["label"] for n in sorted(ns, key=lambda n: -derece[n["id"]])[:3]]
    s.append(f"- {dizin} ({len(ns)}): {', '.join(ust)}")
s.append("## Giriş noktaları (en çok çağrılan)")
gir = [n for n in sorted(g["nodes"], key=lambda n: -derece[n["id"]]) if n.get("_callable")][:10]
s.append(" · ".join(f"{n['label']} {n['source_file']}:{n.get('source_location', '')}" for n in gir))
r = subprocess.run(["git", "log", "--since=7.days", "--name-only", "--format="], cwd=kok, capture_output=True, text=True,
                   encoding="utf-8", errors="replace").stdout.split()
kodlu = {n.get("source_file") for n in g["nodes"]}
s.append("## Sıcak dosyalar (7 gün)")
s.append(" · ".join(f"{y} ({c})" for y, c in Counter(y for y in r if y in kodlu).most_common(10)))
metin = "\n".join(s) + "\n"
hedef = Path(__file__).with_name("harita") / f"{kok.name}.md"  # graphify-out/ Read izninde kapalı
hedef.parent.mkdir(exist_ok=True)
hedef.write_text(metin, encoding="utf-8")
print(f"HARITA.md: {len(s)} satır · ~{len(metin) // 4} jeton")
