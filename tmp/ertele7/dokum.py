"""ERTELE-3 (1): /context tablosundan kaynak/plugin bazında jeton dökümü + listede görünen kopyalar."""
import re, json, collections
bol, satir = None, collections.defaultdict(list)
for l in open("tmp/ertele7/context-A.txt", encoding="utf-8"):
    if l.startswith("### "):
        bol = l[4:].strip()
    m = re.match(r"\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*([<\d.,k ]+)\s*\|", l)
    if bol and m and not m.group(1).startswith(("Category", "Skill", "Agent", "Name", "Tool", "Type", "---", "-")):
        t = m.group(3).strip()
        v = 10 if t.startswith("<") else float(t.rstrip("k").replace(",", "")) * (1000 if t.endswith("k") else 1)
        satir[bol].append((m.group(1), m.group(2), v))
out = {}
for b, rs in satir.items():
    if b in ("MCP Tools", "Estimated usage by category"):
        continue
    g = collections.Counter()
    for ad, kay, v in rs:
        grp = (ad.split(":")[0] + ":*") if ":" in ad else kay
        g[f"{kay} | {grp}"] += v
    out[b] = {"satir": len(rs), "toplam": round(sum(r[2] for r in rs)), "grup_ilk25": [[k, round(v)] for k, v in g.most_common(25)]}
sk = satir.get("Skills", [])
adsay = collections.Counter(a.split(":")[-1].lower() for a, k, v in sk)
out["Skills"]["ayni_kisa_ad_cok_kaynak"] = sum(n - 1 for n in adsay.values() if n > 1)
json.dump(out, open("tmp/ertele7/dokum.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for b, d in out.items():
    print(f"## {b}: {d['satir']} satır ≈{d['toplam']} jeton")
    for k, v in d["grup_ilk25"][:10]:
        print("  ", v, k)
print("ayni kisa ad fazlası:", out["Skills"]["ayni_kisa_ad_cok_kaynak"])
