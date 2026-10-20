"""BEYIN-3 d2 kapı: tohum 2007+2008 (sorular-<tohum>.jsonl), A = `beyin.py ara`, B = yalnız Read; aynı düzenek (beyin2/kapi.py).
Tohum başına iki bağımsız kör hakem (A cevapları). Ölçü: doğru sayısı + API girdi token'ı A/B. Çıktı: kosu/sonuc.txt
Kullanım: python .claude/beyin3/kapi.py [adım...]  (adım: A2007 B2007 A2008 B2008; varsayılan hepsi; kosu/<adım>.json varsa yeniden kullanılır)"""
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

D = Path(__file__).parent
sys.path.insert(0, str(D.parent / "beyin2"))
import kapi  # noqa: E402

kapi.CIKTI = D / "kosu"
kapi.CIKTI.mkdir(exist_ok=True)
TOHUM = (2007, 2008)
S = {t: [json.loads(s) for s in (D / f"sorular-{t}.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()] for t in TOHUM}


def liste(t):
    return "\n".join(f'{q["id"]}. {q["soru"]}' for q in S[t])


def calis(ad, istem, arac=None, izin=None, tur=None):
    yol = kapi.CIKTI / f"{ad}.json"
    if yol.exists():
        return json.loads(yol.read_text(encoding="utf-8"))
    return kapi.cagir(ad, istem, arac, izin, tur)


def hakem(t, j, sonuc):
    cev = {c.get("id"): c.get("cevap") for c in kapi.satirlar(sonuc[f"A{t}"])}
    satir = [json.dumps({"id": q["id"], "soru": q["soru"], "referans": q["cevap"], "cok": bool(q.get("cok")),
                         "aday": cev.get(q["id"], "")}, ensure_ascii=False) for q in S[t]]
    return {p.get("id"): p.get("d", 0) for p in kapi.satirlar(calis(f"hakem{t}-{j}", kapi.HAKEM + "\n".join(satir)))}


def main():
    isler = {}
    for t in TOHUM:
        isler[f"A{t}"] = (kapi.CEVAP_A + liste(t), "Bash", f"Bash({kapi.BEYIN_KOMUT}:*)", kapi.TUR)
        isler[f"B{t}"] = (kapi.CEVAP_B + liste(t), "Read", None, kapi.TUR)
    ad = sys.argv[1:] or list(isler)
    with ThreadPoolExecutor(4) as ex:
        sonuc = dict(zip(ad, ex.map(lambda k: calis(k, *isler[k]), ad)))
    rapor = []
    isim = [(t, j) for t in TOHUM if f"A{t}" in sonuc for j in (1, 2)]
    with ThreadPoolExecutor(4) as ex:
        puan = dict(zip(isim, ex.map(lambda x: hakem(*x, sonuc), isim)))
    for (t, j), d in puan.items():
        s = S[t]
        rapor.append(f"tohum {t} hakem{j}: {sum(d.get(q['id'], 0) for q in s)}/{len(s)}"
                     f" (çok {sum(d.get(q['id'], 0) for q in s if q.get('cok'))}/{sum(bool(q.get('cok')) for q in s)})"
                     f" yanlış {[q['id'] for q in s if not d.get(q['id'])]}")
    for t in TOHUM:
        if f"A{t}" in sonuc and f"B{t}" in sonuc:
            a, b = sonuc[f"A{t}"], sonuc[f"B{t}"]
            rapor.append(f"tohum {t}: token A {kapi.girdi(a)} B {kapi.girdi(b)} = %{100 * kapi.girdi(a) / max(1, kapi.girdi(b)):.0f}"
                         f" tur A {a.get('num_turns')} B {b.get('num_turns')} ihlal A {kapi.ihlal(a)}")
    (kapi.CIKTI / "sonuc.txt").write_text("\n".join(rapor), encoding="utf-8")
    print("\n".join(rapor))


if __name__ == "__main__":
    main()
