"""d13: DF_TAVAN varyantı → yalnız metin geçişi yeniden (lite, ücretsiz; video başı ≤3 çağrı), izle önbelleği (gemini.json) aynen.
d12b oturumlarının araç listesi birleşik (izle + yeni metin) ile değiştirilir → oturum[-sinama]-<et>.json; puanı kisa_m4 verir.
Kullanım: kisa_df13.py <et> <df_tavan>   (gemini-metin.json ilk koşuda gemini-metin-d12.json'a yedeklenir)"""
import json, shutil, sys
from video import kisa, tarama as tr
import kisa_m4 as k

et, kisa.DF_TAVAN = sys.argv[1], float(sys.argv[2])
for kay in ("oturum-d12b.json", "oturum-sinama-d12b.json"):
    o = json.loads((k.CIK / kay).read_text(encoding="utf-8"))
    for x in o["sonuc"]["form"]["videolar"]:
        d = k.ONB / x["id"]
        if not (d / "gemini-metin-d12.json").is_file():
            shutil.copy(d / "gemini-metin.json", d / "gemini-metin-d12.json")
        eski = {tr.normal(a["ad"]) for a in x["araclar"]}
        g = json.loads((d / "gemini.json").read_text(encoding="utf-8"))
        m = kisa.metin_gec(d, yeniden=True)
        kisa.birlestir(g, m)
        ln = {tr.normal(a["ad"]): a["link"] for a in x["araclar"]}
        x["araclar"] = [{"ad": a["ad"], "tur": "teknik" if a["ne_dedi"] == "(teknik)" else "", "link": ln.get(tr.normal(a["ad"]), "")} for a in g["araclar"]]
        yeni = {tr.normal(a["ad"]): a["ad"] for a in g["araclar"]}
        print(x["id"], "aday", m["aday"], "+", [v for n, v in yeni.items() if n not in eski], "-", sorted(eski - yeni.keys()), flush=True)
    (k.CIK / kay.replace("d12b", et)).write_text(json.dumps(o, ensure_ascii=False), encoding="utf-8")
