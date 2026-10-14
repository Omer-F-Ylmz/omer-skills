"""ENVANTER-4 d2 m2b: ücretsiz model taslağının %10 Claude okuyucu doğrulaması.

python tools/kilavuz_ornek.py ornek g1 2-4,7,9-17   → .kos/kopru/envanter4/ornek/g1.md (kart + taslak çiftleri)
python tools/kilavuz_ornek.py uygula g1 karar.jsonl → hatalı alanı düzeltmeyle ya da "?" ile değiştirir, parti/grup doğruluğu,
  <%95 partileri doğrulukla yazar ve kayıtlarına "dogrulandi": false koyar
karar.jsonl satırı: {"ad","tur","yanlis":[alan],"uydurma":[alan],"duzelt":{alan: metin}?} — yalnız hatalı kayıtlar; örneklemdeki öteki kayıtlar doğru sayılır.
"""
import json, math, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import kilavuz_derin as kd
from kilavuz_taslak import araliklar, bloklar

ORN = kd.IS / "ornek"


def taslak(no):
    yol = kd.IS / "cikti" / f"p{no:03d}-t.jsonl"
    return [j for j in map(json.loads, open(yol, encoding="utf8")) if j.get("durum") != "katalog"] if yol.exists() else []


def secim(kayitlar):
    """deterministik %10 (en az 1): ada göre sıralı, eşit aralıklı"""
    s = sorted(kayitlar, key=lambda j: (j["tur"], j["ad"]))
    n = math.ceil(len(s) / 10)
    return [s[int(i * len(s) / n)] for i in range(n)] if s else []


def ornek(grup, aralik):
    ORN.mkdir(exist_ok=True)
    parca, say = [], 0
    for no in araliklar(aralik):
        kart = {f"{b[1]}:{b[0]}": b[3] for b in bloklar((kd.IS / "kart" / f"p{no:03d}.md").read_text(encoding="utf8"))}
        for j in secim(taslak(no)):
            parca.append(f"{kart[j['tur'] + ':' + j['ad']]}\nTASLAK p{no:03d}: {json.dumps(j, ensure_ascii=False)}")
            say += 1
    (ORN / f"{grup}.md").write_text("\n\n".join(parca) + "\n", encoding="utf8")
    (ORN / f"{grup}.aralik").write_text(aralik, encoding="utf8")
    print(f"{grup}: örnek {say} → {(ORN / f'{grup}.md').as_posix()}")


def uygula(grup, karar_yol, olc=""):
    """olc="--olc": yalnız parti doğruluğunu dogruluk.json'a yazar, taslağa dokunmaz (önceden uygulanmış gruplar)"""
    dyol = ORN / "dogruluk.json"
    dogs = json.loads(dyol.read_text(encoding="utf8")) if dyol.exists() else {}
    karar = {}
    for s in open(karar_yol, encoding="utf8"):
        if s.strip():
            j = json.loads(s)
            karar[f"{j['tur']}:{j['ad']}"] = j
    top_alan = top_hata = 0
    yeniden, sil = [], 0
    for no in araliklar((ORN / f"{grup}.aralik").read_text(encoding="utf8")):
        orn = secim(taslak(no))
        if not orn:
            continue
        hata = sum(len(set(karar.get(f"{j['tur']}:{j['ad']}", {}).get("yanlis", [])) | set(karar.get(f"{j['tur']}:{j['ad']}", {}).get("uydurma", [])))
                   for j in orn)
        top_alan += len(orn) * len(kd.ALAN)
        top_hata += hata
        pdog = 1 - hata / (len(orn) * len(kd.ALAN))
        if pdog < 0.95:
            yeniden.append(f"{no}:{pdog:.2f}")
        dogs[str(no)] = round(pdog, 3)
        if olc:
            continue
        yol = kd.IS / "cikti" / f"p{no:03d}-t.jsonl"
        satir = [json.loads(s) for s in open(yol, encoding="utf8")]
        for j in satir:
            k = karar.get(f"{j.get('tur')}:{j['ad']}", {})
            for a in set(k.get("uydurma", [])) | set(k.get("yanlis", [])):  # Desktop 14 Eki: okuyucu düzeltmesi yazılır, yoksa alan silinir
                yeni = k.get("duzelt", {}).get(a) or "?"
                if a in kd.ALAN and j.get(a) != yeni:
                    j[a], sil = yeni, sil + 1
            if pdog < 0.95 and j.get("durum") != "katalog":
                j["dogrulandi"] = False
        with open(yol, "w", encoding="utf8", newline="\n") as f:
            f.writelines(json.dumps(j, ensure_ascii=False) + "\n" for j in satir)
    dyol.write_text(json.dumps(dogs, sort_keys=True), encoding="utf8")
    dog = 1 - top_hata / top_alan if top_alan else 0
    print(f"{grup}: doğruluk {dog:.3f} ({top_hata}/{top_alan} alan hatalı) · uydurma silinen {sil} · <%95 parti: {yeniden or '-'}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    {"ornek": ornek, "uygula": uygula}[sys.argv[1]](*sys.argv[2:])
