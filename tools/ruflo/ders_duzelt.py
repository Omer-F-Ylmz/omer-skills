"""RUFLO-2 d3: son'suz koşulardan gelen haksız ders/güven düşüşünü geri hesaplar (d2 kanca düzeltmesinin geriye dönük karşılığı).
python ders_duzelt.py            → --kuru (varsayılan): ne değişeceğini yazar, dosyaya dokunmaz
python ders_duzelt.py --uygula   → dersler.jsonl yedeklenir (.bak-ruflo2d3), sonra yazılır; --geri yedeği döndürür
Kural 1: kanit == "karma 0.0" ve destek == 1 ve tur == basarisizlik → durum "gecersiz" (getir yalnız aktifi çağırır; silinmez).
Kural 2: son'suz koşunun getirdiği derslere yapılan kullanim+1 (yardim+0) geri alınır; eşik altı 'dusuk' yeniden hesaplanır."""
import json, re, shutil, sys
from collections import Counter
from pathlib import Path

D = Path("C:/Projeler/omer-skills/.kos/ogrenme")
BAK = D / "dersler.jsonl.bak-ruflo2d3"


def haksiz_kullanim():
    """kanca.log'daki her oturumun son-5 'bitti' kaydı ↔ karma; son'suz + karma 0.0 + getirme var → ders id başına sayaç."""
    say = Counter()
    for ln in (D / "kanca.log").read_text(encoding="utf-8").splitlines():
        m = re.search(r"\d\d:\d\d:\d\d (\w{8}) yargı \d+ · karma \[([^\]]*)\]", ln)
        f = m and next((D / "kuyruk").glob(m[1] + "*"), None)
        if not f:
            continue
        kay = [json.loads(s) for s in f.read_text(encoding="utf-8", errors="replace").splitlines() if s.strip()]
        getirilen = {k["ajan_id"]: k["ids"] for k in kay if k["tip"] == "getir"}
        bitti = [k for k in kay if k["tip"] == "bitti"][-5:]  # eski kanca: son'suzlar da dahil
        for k, p in zip(bitti, m[2].split(",")):
            if p.strip() == "0.0" and not (k.get("son") or "").strip():
                say.update(getirilen.get(k["ajan_id"], []))
    return say


def hesapla():
    dersler = [json.loads(s) for s in (D / "dersler.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]
    say, rapor = haksiz_kullanim(), Counter()
    for x in dersler:
        if x["kanit"] == "karma 0.0" and x["destek"] == 1 and x["tur"] == "basarisizlik" and x["durum"] != "gecersiz":
            x["durum"] = "gecersiz"
            rapor["gecersiz"] += 1
        n = min(say.get(x["id"], 0), x["kullanim"])
        if n:
            x["kullanim"] -= n
            rapor["kullanim_geri"] += n
            if x["durum"] == "dusuk" and not (x["kullanim"] >= 2 and (x["yardim"] + 1) / (x["kullanim"] + 2) < 0.34):
                x["durum"] = "aktif"
                rapor["dusuk_kalkti"] += 1
    return dersler, rapor


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--geri" in sys.argv:
        shutil.copy2(BAK, D / "dersler.jsonl")
        sys.exit(print("geri alındı"))
    once = Counter((x["durum"], x["tur"]) for x in map(json.loads, (D / "dersler.jsonl").read_text(encoding="utf-8").splitlines()))
    dersler, rapor = hesapla()
    sonra = Counter((x["durum"], x["tur"]) for x in dersler)
    print("önce", dict(once), "\nsonra", dict(sonra), "\nrapor", dict(rapor))
    if "--uygula" in sys.argv:
        if not BAK.exists():
            shutil.copy2(D / "dersler.jsonl", BAK)
        (D / "dersler.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in dersler), encoding="utf-8", newline="\n")
        print("uygulandı; yedek", BAK.name)
    else:
        print("(--kuru; dosya değişmedi)")
