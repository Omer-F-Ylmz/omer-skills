"""graph.json + manifest.json'dan .graphifyignore/.gitignore'a düşen düğümleri tek geçişte budar: python graphify_buda.py <kök>
`graphify update` aynı silmeyi eski grafı iki kez json.load ederek yapar (337 MB → ~3.5 GB); burada öğe öğe raw_decode, tepe ~1 GB.
Eski dosya graph.json.once olarak kalır (kapı geçince elle silinir). GRAPHIFY-RAM-1/ULTRA-1, 14 Eki."""
import json, os, sys, time
from pathlib import Path
import psutil
from graphify.detect import _is_ignored, _load_graphifyignore

kok = Path(sys.argv[1]).resolve()
out = kok / "graphify-out"
desen, onbellek = _load_graphifyignore(kok), {}
dis = lambda sf: bool(sf) and _is_ignored(kok / sf, kok, desen, _cache=onbellek)
bas, dec = time.time(), json.JSONDecoder()
s = (out / "graph.json").read_text(encoding="utf-8")


def dizi(anahtar, i):  # s içinde "anahtar":[ ... ] öğelerini sırayla verir; bitişte son indeks
    i = s.index(f'"{anahtar}":[', i) + len(anahtar) + 4
    while s[i] != "]":
        o, i = dec.raw_decode(s, i)
        yield o, i
        if s[i] == ",":
            i += 1


bas_i = s.index('"nodes":[')
kalan, tutulan, i = 0, set(), 0
dugum = []
for o, i in dizi("nodes", 0):
    kalan += 1
    if not dis(o.get("source_file")):
        dugum.append(o); tutulan.add(o["id"])
kenar, j = [], i
for o, j in dizi("links", i):
    if o["source"] in tutulan and o["target"] in tutulan:
        kenar.append(o)
bitis = json.loads("{" + s[j + 2:])  # s[j] links'in "]"'i; kalan: hyperedges, built_at_commit
g = json.loads(s[:bas_i].rstrip(",") + "}")
assert kalan and dugum, "düğüm okunamadı"
del s
g.update(nodes=dugum, links=kenar, **bitis)
os.replace(out / "graph.json", out / "graph.json.once")
(out / "graph.json").write_text(json.dumps(g, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
m = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
m2 = {k: v for k, v in m.items() if not dis(k)}
(out / "manifest.json").write_text(json.dumps(m2, ensure_ascii=False), encoding="utf-8")
print(f"buda: düğüm {kalan}→{len(dugum)} · kenar→{len(kenar)} · manifest {len(m)}→{len(m2)} · "
      f"{(out / 'graph.json').stat().st_size / 1e6:.0f} MB · tepe RSS {psutil.Process().memory_info().peak_wset / 1e6:.0f} MB · "
      f"{time.time() - bas:.0f} sn")
