import json
d=".kos/kopru/usta-haiku/ileri/"
n=json.load(open(d+"hakem15-adlar.json",encoding="utf-8")); ok=0; tot=0
for g in range(4):
    for e in json.load(open(d+f"hakem15b-{g}.json",encoding="utf-8")):
        tot+=1; a=n[g*10+e["i"]]
        if e.get("dogru") and e.get("yararli"): ok+=1
        else: print(" RED",a,e.get("neden"))
print(ok,tot,f"{ok/tot:.0%}")
