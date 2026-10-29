"""ERTELE-3 (2a): settings.json'daki Agent(...) reddi katalogda mı, yol geçerli mi."""
import csv, json, os, re, sys, collections
S = json.load(open(os.path.expanduser("~/.claude/settings.json"), encoding="utf-8"))
deny = [r for r in S.get("permissions", {}).get("deny", []) if r.startswith("Agent(")]
adlar = [re.match(r"Agent\((.*)\)", r).group(1) for r in deny]
kat = {}
with open("skills/ajan-getir/katalog.tsv", encoding="utf-8") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        kat[r["ad"]] = r
yok, bozuk = [], []
for a in adlar:
    r = kat.get(a)
    if not r:
        yok.append(a)
    elif not os.path.isfile(r["yol"]):
        bozuk.append((a, r["yol"]))
grup = collections.Counter(a.split(":")[0] if ":" in a else "(yalin)" for a in adlar)
out = {"deny": len(adlar), "katalog_satir": len(kat), "katalogda_yok": yok,
       "yol_bozuk": bozuk, "grup": grup.most_common()}
json.dump(out, open("tmp/ertele7/gizli.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(adlar, open("tmp/ertele7/gizli-adlar.json", "w", encoding="utf-8"), ensure_ascii=False)
print(len(adlar), "red ·", len(kat), "katalog · yok", len(yok), "· yol bozuk", len(bozuk))
print(grup.most_common(8)); print("yok:", yok[:15]); print("bozuk:", [b[0] for b in bozuk[:10]])
