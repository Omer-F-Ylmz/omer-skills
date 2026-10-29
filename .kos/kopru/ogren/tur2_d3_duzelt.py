"""ÖĞREN-2.tur d3: d2 kapısında hatalı alanı olan kartları kaynağa dayalı yeniden yazar (ücretsiz taslak → kapı hakemiyle yeniden doğrulama).
Kaynak = hakemin gördüğü metin (kanit'in ilk 7000 karakteri; .claude.json ise yalnız o sunucunun kaydı). Doğrulanan kart kart.jsonl'e yazılır.
Kullanım: python -X utf8 .kos/kopru/ogren/tur2_d3_duzelt.py [--yaz]"""
import importlib.util
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("tur2_kapi", KOK / ".kos/kopru/ogren/tur2_d2_kapi.py")
K = importlib.util.module_from_spec(spec)
spec.loader.exec_module(K)
h = K.h


def kaynak(k):
    yol = Path(k["kanit"])
    if yol.name == ".claude.json":
        d = json.loads(yol.read_text(encoding="utf-8"))
        sunucular = {**d.get("mcpServers", {}), **{a: v for p in d.get("projects", {}).values() for a, v in p.get("mcpServers", {}).items()}}
        return json.dumps({k["ad"]: sunucular.get(k["ad"])}, ensure_ascii=False)
    return yol.read_text(encoding="utf-8", errors="replace")[:7000]


K_ORIJ = K.istem


def istem_kaynakli(k):
    return K_ORIJ(k).split("\n\nKAYNAK:\n")[0] + "\n\nKAYNAK:\n" + kaynak(k)


def taslak(k, alanlar, src):
    p = (f"Araç kartının şu alanlarını YALNIZ aşağıdaki KAYNAK metne dayanarak yeniden yaz: {', '.join(alanlar)}. Türkçe, tek-iki cümle, kaynakta birebir geçen komut/ad/koşulu kullan; "
         "kaynakta olmayan hiçbir bilgi ekleme, çıkarım yapma; kaynakta yoksa 'belirsiz — kaynakta belirtilmemiş' yaz. "
         f"YALNIZ JSON yaz: {{{', '.join(chr(34) + a + chr(34) + ': \"...\"' for a in alanlar)}}}\n\nKART ({k['ad']}):\n{json.dumps({a: k.get(a) for a in K.ALAN}, ensure_ascii=False)}\n\nKAYNAK:\n{src}")
    m, kay, _ = h.cagir(h.H, p, max_tokens=900, dogrula=lambda m: None if K.re.search(r"\{.*\}", m or "", K.re.S) else "json-degil", etiket="tur2-d3-duzelt")
    try:
        d = json.loads(K.re.search(r"\{.*\}", m, K.re.S).group(0))
    except Exception:
        return None, kay
    return ({a: d[a] for a in alanlar if isinstance(d.get(a), str) and d[a].strip()} if all(a in d for a in alanlar) else None), kay


if __name__ == "__main__":
    hata = {}
    for l in (KOK / ".claude/ogren-tur2-d2/kapi.jsonl").read_text(encoding="utf-8").splitlines():
        r = json.loads(l)
        f = [a for a, v in r["sonuc"].items() if not v]
        if f:
            hata[r["ad"]] = f
    satirlar = (KOK / "docs/atlas/kart.jsonl").read_text(encoding="utf-8").splitlines()
    cikti, rapor = [], []
    for s in satirlar:
        k = json.loads(s)
        if k.get("kategori") == "tur2-delta" and k.get("ad") in hata:
            src = kaynak(k)
            yeni, kay = taslak(k, hata[k["ad"]], src)
            if yeni:
                aday = {**k, **yeni}
                K.istem = lambda x, _s=src: K_ORIJ(x).split("\n\nKAYNAK:\n")[0] + "\n\nKAYNAK:\n" + _s
                sonuc = K.bir(aday)["sonuc"]
                ok = all(v is True for v in sonuc.values())
                rapor.append((k["ad"], hata[k["ad"]], kay, ok, {a: yeni[a][:90] for a in yeni}))
                if ok:
                    k = aday
            else:
                rapor.append((k["ad"], hata[k["ad"]], kay, False, None))
        cikti.append(json.dumps(k, ensure_ascii=False))
    for r in rapor:
        print(r[0], "OK" if r[3] else "RED", flush=True)
    if "--yaz" in sys.argv:
        with (KOK / "docs/atlas/kart.jsonl").open("wb") as f:
            f.write(("\n".join(cikti) + "\n").encode("utf-8"))
        print("yazildi", sum(r[3] for r in rapor), "/", len(rapor))
