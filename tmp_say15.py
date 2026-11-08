import json
d=".kos/kopru/usta-haiku/ileri/"
a=json.load(open(d+"hakem15.json",encoding="utf-8")); n=json.load(open(d+"hakem15-adlar.json",encoding="utf-8"))
ok=sum(1 for e in a if e.get("dogru") and e.get("yararli")); print(ok,len(a),f"{ok/len(a):.0%}")
for e in a:
    if not(e.get("dogru") and e.get("yararli")): print(" RED",n[e["i"]],e.get("neden"))
