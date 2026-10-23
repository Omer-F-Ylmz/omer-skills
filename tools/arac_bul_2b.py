"""ARAC-BUL-2 adım 1b: arac-bul-2.tsv 'bilinmiyor' satırlarını ikinci geçişte çöz (OCR düzeltmeli gh arama + havuz seçimi/düzeltmesi), kalanı kanıtla sınıfla.
Çıktı: arac-bul-2.tsv güncellenir (bilinmiyor → bulundu/uygulama/komut/ocr). İndirme yok (arac_bul_2.py --indir yapar). Kullanım: python tools/arac_bul_2b.py"""
import csv, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import arac_bul_2 as b  # noqa: E402
import arac_indir_1 as ai  # noqa: E402
import ucretsiz_havuz  # noqa: E402

ISTEM = """Her kayıt video OCR/konuşma bağlamından çıkarılmış bir araç/proje adı; ad bozuk olabilir (OCR). GitHub arama adayları verildi.
Karar ver: "repo": "<owner/repo>" — ya adaylardan biri (bağlamla uyumluysa) ya da KESİN bildiğin gerçek repo (düzeltilmiş ad); emin değilsen "" bırak, uydurma.
"sinif": repo (bir GitHub reposu) | uygulama (masaüstü/mobil uygulama/web servisi ya da öğretici videodaki örnek proje) | komut (CLI komutu/ayar/özellik) | ocr (anlamsız artık).
"kanit": bağlamdan BİREBİR ≤100 karakter alıntı. YALNIZ JSON dizisi: [{"ad":"<aynen>","repo":"...","sinif":"...","kanit":"..."}]
Kayıtlar:
"""


def tokenlar(s):
    s = re.sub(r"https?://github\.com/", "", s)
    return [w for w in re.split(r"[^A-Za-z0-9]+", s) if len(w) >= 3]


def adaylar(r, bag):
    q = []
    for x in (r["ad"], r["aday"]):
        if x:
            t = " ".join(tokenlar(x.split("/")[-1])[:4])
            if t and t not in q:
                q.append(t)
    cs = {}
    for t in q:
        for d in b.gh_ara_genis(t):
            cs[d["fullName"]] = d
    for h in bag.get("gh_ipucu", []):
        d = ai.gh_goruntule(h)
        if d:
            cs[d["nameWithOwner"]] = {"fullName": d["nameWithOwner"], "stargazersCount": d["stargazerCount"], "description": "(video ipucu)"}
    return list(cs.values())[:8]


def main():
    yol = b.CIKTI
    with open(yol, encoding="utf-8") as f:
        satir = list(csv.DictReader(f, delimiter="\t"))
    bil = [r for r in satir if r["sinif"] == "bilinmiyor"]
    bag = {}
    for r in bil:
        bag[r["ad"]] = b.baglam(r["ad"], [v for v in r["video"].split(",") if v])
    kayit = []
    for r in bil:
        kayit.append({"ad": r["ad"], "aday": r["aday"], "baslik": bag[r["ad"]]["baslik"], "konusma": bag[r["ad"]]["konusma"][:1], "ekran": bag[r["ad"]]["ekran"][:1], "kanit_eski": r["kanit"][:100], "adaylar": [f"{c['fullName']} ({c['stargazersCount']}*) {str(c.get('description') or '')[:70]}" for c in adaylar(r, bag[r["ad"]])]})
    sonuc = {}
    for i in range(0, len(kayit), 6):
        g = kayit[i:i + 6]
        y, kol, _ = ucretsiz_havuz.cagir("ozet", ISTEM + json.dumps(g, ensure_ascii=False), max_tokens=2500)
        m = re.search(r"\[.*\]", y or "", re.S)
        try:
            for o in json.loads(m.group(0)):
                if isinstance(o, dict):
                    sonuc[o.get("ad")] = o
        except (ValueError, AttributeError, TypeError):
            print("ayrıştırılamadı", kol, flush=True)
    cozulen = 0
    for r in bil:
        o = sonuc.get(r["ad"], {})
        if o.get("repo") and o["repo"].count("/") == 1:
            d = ai.gh_goruntule(o["repo"])
            if d:
                r.update(sinif="bulundu", aday=d["nameWithOwner"], link="https://github.com/" + d["nameWithOwner"], durum="indirilmedi", boyut=f"{d['diskUsage']//1024}MB", kanit=str(o.get("kanit") or "")[:100])
                cozulen += 1
                continue
        s = {"uygulama": "uygulama", "komut": "komut", "ocr": "ocr"}.get(o.get("sinif"))
        if s:
            r.update(sinif=s, kanit=str(o.get("kanit") or r["kanit"])[:100])
            if o.get("repo") and s != "repo":
                r["kanit"] += f" [repo bulunamadı: {o['repo']}]"
    tek = {}
    for r in satir:  # aynı repoya çözülen satırları birleştir
        k = r["aday"].lower() if r["sinif"] == "bulundu" and r["link"].startswith("https://github.com/") else id(r)
        tek.setdefault(k, r)
    satir = list(tek.values())
    with open(yol, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, ["ad", "sinif", "aday", "link", "durum", "boyut", "tarama", "kanit", "video"], delimiter="\t")
        w.writeheader()
        w.writerows(satir)
    import collections
    print("bilinmiyor", len(bil), "→ repo çözülen", cozulen, "| DAĞILIM", collections.Counter(r["sinif"] for r in satir))


if __name__ == "__main__":
    main()
