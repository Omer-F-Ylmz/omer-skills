"""d13: açıklama/ekran linkinin alan adı → araç kuralının çevrimdışı etkisi (d12b oturumları yamanır → *-d13p.json; ağ/claude yok)."""
import json, re
from video import tarama as tr
import kisa_m4 as k

GENEL = ("instagram", "github", "youtube", "youtu", "linktr", "bit", "t", "x", "twitter", "facebook", "tiktok", "linkedin", "discord",
         "patreon", "google", "apple", "threads", "beacons", "stan", "wa", "gthub")


def alan_adlari(linkler):
    out = []
    for u in linkler:
        h = re.sub(r"^https?://(www\.)?", "", u.lower()).split("/")[0].split(":")[0]
        p = h.split(".")
        if len(p) >= 2 and p[-2] not in GENEL and p[0] not in GENEL:
            out.append(h)
    return list(dict.fromkeys(out))


for kay, hedef in (("oturum-d12b.json", "oturum-d13p.json"), ("oturum-sinama-d12b.json", "oturum-sinama-d13p.json")):
    o = json.loads((k.CIK / kay).read_text(encoding="utf-8"))
    for x in o["sonuc"]["form"]["videolar"]:
        s = (k.ONB / x["id"] / "paket.md").read_text(encoding="utf-8")
        var = {tr.normal(a["ad"]) for a in x["araclar"]}
        yeni = [a for a in alan_adlari([y["url"] for y in tr.link_topla({"paket": s})]) if tr.normal(a) not in var]
        x["araclar"] += [{"ad": a, "tur": "", "link": ""} for a in yeni]
        print(x["id"], "eklenen:", yeni)
    (k.CIK / hedef).write_text(json.dumps(o, ensure_ascii=False), encoding="utf-8")
