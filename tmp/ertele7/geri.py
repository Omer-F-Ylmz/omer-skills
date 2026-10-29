"""ERTELE-3 (2c): 30 gizli ajan için ücretsiz modelle görev tarifi üret, katalogdan geri bulmayı ölç.
Kullanım: python -I tmp/ertele7/geri.py tarif|olc [tur]"""
import csv, json, math, os, re, sys, collections
sys.path.insert(0, "tools")
K = "tmp/ertele7/"
adlar = sorted(json.load(open(K + "gizli-adlar.json", encoding="utf-8")))
sec = [adlar[i * len(adlar) // 30] for i in range(30)]
kat = {r["ad"]: r for r in csv.DictReader(open("skills/ajan-getir/katalog.tsv", encoding="utf-8"), delimiter="\t")}


def govde(ad):
    return open(kat[ad]["yol"], encoding="utf-8", errors="ignore").read()[:2500]


def tarif(tur):
    import ucretsiz_havuz as uh
    yol = K + "tarif.jsonl"
    var = {json.loads(l)["ad"] for l in open(yol, encoding="utf-8")} if os.path.exists(yol) else set()
    for ad in sec:
        if ad in var:
            continue
        istem = ("Aşağıda bir uzman yapay zekâ ajanının tanımı var. Bu ajanın çözeceği GERÇEKÇİ, tek cümlelik, Türkçe bir kullanıcı "
                 "isteği yaz. Ajanın adını, plugin adını ve tanımdaki ayırt edici terimleri birebir KULLANMA; kullanıcı ağzından yaz. "
                 "Yalnız cümleyi döndür.\n<tanim>\n" + govde(ad) + "\n</tanim>")
        m, kim, _ = uh.cagir(tur, istem, max_tokens=300, etiket="ertele3-tarif")
        if m:
            with open(yol, "a", encoding="utf-8") as f:
                f.write(json.dumps({"ad": ad, "tarif": m.strip().strip('"'), "model": kim}, ensure_ascii=False) + "\n")
        print(ad, "→", (m or "YOK")[:90])


def _kel(s):
    s = s.lower().translate(str.maketrans("çğıöşüâî", "cgiosuai"))
    return [w[:5] for w in re.findall(r"[a-z0-9]{3,}", s)]


def bm25(sorgu, n=8):
    docs = {ad: _kel(ad.replace(":", " ").replace("-", " ") + " " + r["tek_satir"]) for ad, r in kat.items()}
    df = collections.Counter(w for d in docs.values() for w in set(d))
    N, ort = len(docs), sum(map(len, docs.values())) / len(docs)
    q = set(_kel(sorgu))
    p = {ad: sum(math.log(1 + (N - df[w] + .5) / (df[w] + .5)) * d.count(w) * 2.2 / (d.count(w) + 1.2 * (.25 + .75 * len(d) / ort))
                 for w in q if w in d) for ad, d in docs.items()}
    return [a for a, v in sorted(p.items(), key=lambda x: -x[1])[:n] if v > 0]


def olc():
    import ertele_katalog as ek
    ek.kur()
    satir = [json.loads(l) for l in open(K + "tarif.jsonl", encoding="utf-8")]
    sonuc = []
    for s in satir:
        e = ek.ara(s["tarif"])
        kisa = s["ad"].split(":")[-1]
        sonuc.append({**s, "ertele_ara": s["ad"] in e or f"{kisa} ·" in e, "bm25_8": bm25(s["tarif"])})
        sonuc[-1]["bm25_hit"] = s["ad"] in sonuc[-1]["bm25_8"]
    json.dump(sonuc, open(K + "geri.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(sonuc), "tarif · ertele ara:", sum(x["ertele_ara"] for x in sonuc), "· bm25 top8:", sum(x["bm25_hit"] for x in sonuc),
          "· biri:", sum(x["ertele_ara"] or x["bm25_hit"] for x in sonuc))
    for x in sonuc:
        if not (x["ertele_ara"] and x["bm25_hit"]):
            print(" -", x["ad"], int(x["ertele_ara"]), int(x["bm25_hit"]), "|", x["tarif"][:80])


if __name__ == "__main__":
    tarif(sys.argv[2] if len(sys.argv) > 2 else "ozet") if sys.argv[1] == "tarif" else olc()
