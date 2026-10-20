"""BEYIN-4 d2 kapı: tohum 2009+2010 (sorular-<tohum>.jsonl, betik üretimi), A = `beyin.py ara`, B = yalnız Read; düzenek beyin2/kapi.py.
Hakem BETİK: cevaptaki her sayı aday cevapta tam sayı olarak geçerse doğru (çok için hepsi). Ölçü: doğruluk + API girdi token'ı A/B.
Kullanım: python .claude/beyin4/kapi.py [adım...]  (adım: A2009 B2009 A2010 B2010; varsayılan hepsi; kosu/<adım>.json varsa yeniden kullanılır)
Kabul: doğruluk ≥%92 ve token A ≤ B'nin %25."""
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

D = Path(__file__).parent
sys.path.insert(0, str(D.parent / "beyin2"))
import kapi  # noqa: E402

kapi.CIKTI = D / "kosu"
kapi.CIKTI.mkdir(exist_ok=True)
TOHUM = (2009, 2010)
S = {t: [json.loads(s) for s in (D / f"sorular-{t}.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()] for t in TOHUM}


def liste(t):
    return "\n".join(f'{q["id"]}. {q["soru"]}' for q in S[t])


def calis(ad, istem, arac=None, izin=None, tur=None):
    yol = kapi.CIKTI / f"{ad}.json"
    return json.loads(yol.read_text(encoding="utf-8")) if yol.exists() else kapi.cagir(ad, istem, arac, izin, tur)


def dogru(q, cevap):
    return all(re.search(rf"(?<![\d.,]){re.escape(s)}(?!\d)", str(cevap)) for s in q["cevap"].split(";") if s.strip())


def main():
    isler = {}
    for t in TOHUM:
        isler[f"A{t}"] = (kapi.CEVAP_A + liste(t), "Bash", f"Bash({kapi.BEYIN_KOMUT}:*)", kapi.TUR)
        isler[f"B{t}"] = (kapi.CEVAP_B + liste(t), "Read", None, kapi.TUR)
    ad = sys.argv[1:] or list(isler)
    with ThreadPoolExecutor(4) as ex:
        sonuc = dict(zip(ad, ex.map(lambda k: calis(k, *isler[k]), ad)))
    rapor = []
    for t in TOHUM:
        for kol in "AB":
            if f"{kol}{t}" in sonuc:
                cev = {c.get("id"): c.get("cevap") for c in kapi.satirlar(sonuc[f"{kol}{t}"])}
                d = {q["id"]: dogru(q, cev.get(q["id"], "")) for q in S[t]}
                rapor.append(f"tohum {t} {kol}: {sum(d.values())}/{len(d)} (çok {sum(d[q['id']] for q in S[t] if q['cok'])}"
                             f"/{sum(q['cok'] for q in S[t])}) yanlış {[i for i, v in d.items() if not v]}")
        if f"A{t}" in sonuc and f"B{t}" in sonuc:
            a, b = sonuc[f"A{t}"], sonuc[f"B{t}"]
            rapor.append(f"tohum {t}: token A {kapi.girdi(a)} B {kapi.girdi(b)} = %{100 * kapi.girdi(a) / max(1, kapi.girdi(b)):.0f}"
                         f" tur A {a.get('num_turns')} B {b.get('num_turns')} ihlal A {kapi.ihlal(a)}")
    (kapi.CIKTI / "sonuc.txt").write_text("\n".join(rapor), encoding="utf-8")
    print("\n".join(rapor))


if __name__ == "__main__":
    main()
