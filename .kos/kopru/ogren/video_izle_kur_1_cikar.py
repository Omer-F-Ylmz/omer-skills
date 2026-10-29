"""VIDEO-IZLE-KUR-1 adim 2: tur<N>.tsv kalemlerinin kaynak videolarinin derin json'undan (transkript+OCR+link+komut)
kurulum ayrintisini ucretsiz modelle cikarir (Claude jetonu 0). Kullanim: python -I -X utf8 video_izle_kur_1_cikar.py <N>
Cikti: video-izle-kur-1/tur<N>-cikar.jsonl (kaldigi yerden). Model yalniz kaynakta gecen bilgiyi yazar; yoksa "yok".
"""
import csv, json, re, sys
from pathlib import Path

K = Path(r"C:/Projeler/omer-skills")
sys.path.insert(0, str(K / "tools"))
from ucretsiz_havuz import cagir

D = K / ".kos/kopru/ogren/video-izle-kur-1"
n = sys.argv[1]
OUT = D / f"tur{n}-cikar.jsonl"
bitti = {d["ad"] for d in map(json.loads, open(OUT, encoding="utf-8")) if d["durum"] == "ok"} if OUT.exists() else set()  # tur 2: model-yok/derin-yok yeniden
DERIN = [K / "docs/video-tarama/derin", K / "docs/video-tarama/derin-2"]
ISTEM = """Asagida "{ad}" ({tur}) adli arac hakkinda video(lar)in transkripti, ekran yazisi (OCR), linkler ve komutlar var.
YALNIZ bu metinde gecen bilgiyle su JSON'u yaz (uydurma yok; metinde yoksa "yok"):
{{"repo_veya_url": "...", "kurulum_komutu": "...", "ayarlar": "...", "kullanim": "...", "iddia_edilen_fayda": "...", "kanit_alinti": "metinden kisa birebir alinti"}}
Yalniz JSON yaz.
---
{metin}"""


def kod(l):
    return re.sub(r".*/(reel|p|shorts)/|.*v=|.*youtu\.be/", "", l).strip("/").split("?")[0]


def metin(link_list):
    parca = []
    for l in link_list:
        for d in DERIN:
            p = d / f"{kod(l)}.json"
            if p.exists():
                j = json.load(open(p, encoding="utf-8"))
                parca.append("BASLIK: " + str((j.get("meta") or {}).get("baslik", "")) + "\nACIKLAMA: " + str((j.get("meta") or {}).get("aciklama", ""))[:1500]
                             + "\nTRANSKRIPT: " + " ".join(s.get("t", "") for s in j.get("transkript") or [])[:5000]
                             + "\nOCR: " + " | ".join(e.get("t", "") for e in j.get("ekran") or [])[:2000]
                             + "\nLINK: " + " ".join(map(str, j.get("linkler") or [])) + "\nKOMUT: " + " ; ".join(map(str, j.get("komutlar") or [])))
                break
    return "\n=====\n".join(parca)


def dogrula(t):
    m = re.search(r"\{.*\}", t or "", re.S)
    try:
        json.loads(m.group(0))
    except Exception:
        return "json degil"


for r in csv.DictReader(open(D / f"tur{n}.tsv", encoding="utf-8"), delimiter="\t"):
    if r["ad"] in bitti:
        continue
    m = metin(r["video"].split())
    if not m:
        rec = {"ad": r["ad"], "durum": "derin-yok"}
    else:
        t, kaynak, _ = cagir("ozet", ISTEM.format(ad=r["ad"], tur=r["tür"], metin=m), max_tokens=900, dogrula=dogrula, etiket="video-izle-kur-1")
        rec = {"ad": r["ad"], "durum": "ok" if t else "model-yok", "kaynak": kaynak}
        if t:
            rec.update(json.loads(re.search(r"\{.*\}", t, re.S).group(0)))
    with open(OUT, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(r["ad"], rec["durum"], rec.get("kaynak", ""), flush=True)
print("BITTI")
