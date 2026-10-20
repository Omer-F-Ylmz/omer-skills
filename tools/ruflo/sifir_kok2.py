"""RUFLO-2 d2 C: 'son boş' kayıtların transkripti SONRADAN dolu mu (kanca erken mi okudu — yarış) yoksa gerçekten boş mu."""
import glob, json, sys, os
sys.path.insert(0, "C:/Projeler/omer-skills/tools/ruflo")
sys.argv = ["x"]
import sifir_kok as s
sys.stdout.reconfigure(encoding="utf-8")
bos = [x for x in s.ks if not (x.get("son") or "").strip()]
kok = os.path.expanduser("~/.claude/projects")
bulundu = dolu = 0
son_tur = {}
for x in bos:
    g = glob.glob(f"{kok}/*/*/subagents/agent-{x['ajan_id']}.jsonl")
    if not g:
        continue
    bulundu += 1
    son = ""
    sonuncu = None
    for ln in open(g[0], encoding="utf-8", errors="replace"):
        try:
            j = json.loads(ln)
        except ValueError:
            continue
        if j.get("type") == "assistant":
            ic = (j.get("message") or {}).get("content") or []
            tipler = [p.get("type") for p in ic if isinstance(p, dict)]
            sonuncu = tipler
            for p in ic:
                if isinstance(p, dict) and p.get("type") == "text" and p.get("text", "").strip():
                    son = p["text"]
    dolu += bool(son)
    key = tuple(sonuncu or [])
    son_tur[key] = son_tur.get(key, 0) + 1
print(f"son boş {len(bos)} · transkript bulundu {bulundu} · şimdi son metin VAR {dolu}")
print("son assistant mesajı içerik türleri:", son_tur)
