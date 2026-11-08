import json
import os
import urllib.request

URL = "https://raw.githubusercontent.com/BraveOPotato/FckSignups/refs/heads/main/tools.json"
KOK = os.path.dirname(os.path.abspath(__file__))

veri = json.loads(urllib.request.urlopen(URL, timeout=60).read().decode())
araclar = veri["tools"]
with open(os.path.join(KOK, "nosignups-tools.json"), "w", encoding="utf-8") as f:
    json.dump(veri, f, ensure_ascii=False, indent=1)

satirlar = ["ad\tkategori\turl\taciklama\tlisans\tyildiz\tgithub\tdurum"]
for t in sorted(araclar, key=lambda x: (x.get("category", ""), -(x.get("stars") or 0))):
    lisans = str(t.get("license") or "?")
    durum = "AL (ticari-disi lisans, bilerek alindi)" if ("NC" in lisans.upper()) else "AL"
    satirlar.append("\t".join(str(v).replace("\t", " ").replace("\n", " ") for v in [
        t.get("name", ""), t.get("category", ""), t.get("url", ""), (t.get("description") or "")[:160],
        lisans, t.get("stars") or "", t.get("github") or "", durum]))
with open(os.path.join(KOK, "nosignups-tamami-2026-11-04.tsv"), "w", encoding="utf-8") as f:
    f.write("\n".join(satirlar) + "\n")
print(len(araclar), "arac yazildi")
